import os
import time
import unicodedata
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from math import radians, sin, cos, asin, sqrt
import requests
from urllib.parse import urlparse

TIMEOUT = min(max(int(os.getenv("REQUEST_TIMEOUT", "3")), 2), 5)
UA = "TravelMonitor/4.0 (local educational project)"
OVERPASS_URLS = [
    os.getenv("OVERPASS_URL", "https://overpass-api.de/api/interpreter"),
    "https://overpass.private.coffee/api/interpreter",
    "https://maps.mail.ru/osm/tools/overpass/api/interpreter",
]
OVERPASS_CACHE = {}
OVERPASS_CACHE_TTL = 300
GEOCODE_CACHE = {}
AIRPORT_CACHE = {}
AMADEUS_TOKEN = None
AMADEUS_TOKEN_EXPIRES = 0
CLICKBUS_TOKEN = None
CLICKBUS_TOKEN_EXPIRES = 0
PUBLIC_HOTEL_DAILY_AVERAGE = 451.71

CITY_COORDS = {
    "vitoria": (-20.3155, -40.3128),
    "vila velha": (-20.3297, -40.2925),
    "serra": (-20.1286, -40.3076),
    "cariacica": (-20.2639, -40.4169),
    "guarapari": (-20.6736, -40.4978),
    "sao paulo": (-23.5505, -46.6333),
    "campinas": (-22.9099, -47.0626),
    "rio de janeiro": (-22.9068, -43.1729),
    "belo horizonte": (-19.9167, -43.9345),
    "brasilia": (-15.7939, -47.8828),
    "curitiba": (-25.4284, -49.2733),
    "porto alegre": (-30.0346, -51.2177),
    "florianopolis": (-27.5954, -48.5480),
    "recife": (-8.0476, -34.8770),
    "salvador": (-12.9777, -38.5016),
    "fortaleza": (-3.7319, -38.5267),
    "manaus": (-3.1190, -60.0217),
    "belem": (-1.4558, -48.4902),
    "goiania": (-16.6869, -49.2648),
    "cuiaba": (-15.6014, -56.0979),
    "campo grande": (-20.4697, -54.6201),
}

CITY_AIRPORTS = {
    "vitoria":"VIX","vila velha":"VIX","serra":"VIX","cariacica":"VIX","guarapari":"VIX",
    "sao paulo":"GRU","campinas":"VCP","santos":"GRU","sao jose dos campos":"GRU",
    "rio de janeiro":"GIG","niteroi":"GIG","petropolis":"GIG","cabo frio":"CFB",
    "belo horizonte":"CNF","uberlandia":"UDI","brasilia":"BSB","goiania":"GYN",
    "curitiba":"CWB","londrina":"LDB","foz do iguacu":"IGU","porto alegre":"POA",
    "florianopolis":"FLN","joinville":"JOI","blumenau":"NVT","balneario camboriu":"NVT",
    "recife":"REC","salvador":"SSA","porto seguro":"BPS","fortaleza":"FOR","natal":"NAT",
    "joao pessoa":"JPA","maceio":"MCZ","aracaju":"AJU","sao luis":"SLZ","teresina":"THE",
    "belem":"BEL","manaus":"MAO","palmas":"PMW","campo grande":"CGR","cuiaba":"CGB",
    "bonito":"BYO","jericoacoara":"JJD","maragogi":"MCZ","buzios":"CFB","paraty":"GIG",
    "ilhabela":"GRU","ubatuba":"GRU","gramado":"POA","canela":"POA",
}

def normalize_text(value):
    return "".join(c for c in unicodedata.normalize("NFD", str(value).lower()) if unicodedata.category(c) != "Mn")

def geocode(place):
    key = " ".join(normalize_text(place).split())
    if key in GEOCODE_CACHE:
        return GEOCODE_CACHE[key]

    city_key = key.split(",")[0].strip()
    if city_key in CITY_COORDS:
        lat, lon = CITY_COORDS[city_key]
        result = {"lat": lat, "lon": lon, "display_name": place}
        GEOCODE_CACHE[key] = result
        return result

    try:
        r = requests.get("https://nominatim.openstreetmap.org/search", params={"q":place,"format":"jsonv2","limit":1,"countrycodes":"br"}, headers={"User-Agent":UA}, timeout=3)
        r.raise_for_status(); data=r.json()
        if not data: return None
        result={"lat":float(data[0]["lat"]),"lon":float(data[0]["lon"]),"display_name":data[0].get("display_name",place)}
        GEOCODE_CACHE[key]=result; return result
    except (requests.RequestException,ValueError,KeyError,TypeError): return None

def haversine(lat1,lon1,lat2,lon2):
    radius=6371.0; dlat=radians(lat2-lat1); dlon=radians(lon2-lon1)
    a=sin(dlat/2)**2+cos(radians(lat1))*cos(radians(lat2))*sin(dlon/2)**2
    return 2*radius*asin(sqrt(a))

def _overpass_request(url, query):
    try:
        r = requests.post(
            url,
            data=query,
            headers={"User-Agent": UA, "Accept": "application/json"},
            timeout=TIMEOUT,
        )
        r.raise_for_status()
        elements = r.json().get("elements", [])
        return elements if isinstance(elements, list) else []
    except (requests.RequestException, ValueError, TypeError):
        return None


def overpass(lat, lon):
    # Cache successful OSM/Overpass results so repeating a saved search does
    # not immediately hit the public services again.
    cache_key=(round(float(lat),4),round(float(lon),4))
    cached=OVERPASS_CACHE.get(cache_key)
    if cached and time.time()-cached[0] < OVERPASS_CACHE_TTL:
        return cached[1]

    query=(
        '[out:json][timeout:4];'
        '(nwr["tourism"~"hotel|hostel|guest_house|attraction|museum|gallery|'
        'theme_park|zoo|viewpoint|aquarium"](around:8000,%s,%s);'
        'nwr["historic"~"monument|memorial|castle|ruins|archaeological_site"]'
        '(around:8000,%s,%s);'
        'nwr["leisure"="park"](around:8000,%s,%s););'
        'out center tags;'
    ) % (lat, lon, lat, lon, lat, lon)

    # Use one public instance at a time and fall back only after failure.
    # This is friendlier to shared Overpass infrastructure than firing the
    # same query at several public servers simultaneously.
    for url in OVERPASS_URLS:
        result=_overpass_request(url,query)
        if result is not None:
            OVERPASS_CACHE[cache_key]=(time.time(),result)
            return result
    return []

def normalize_places(elements,lat,lon,limit=30):
    out=[]; seen=set()
    for e in elements:
        tags=e.get("tags",{}); name=(tags.get("name") or "").strip()
        if not name or name.casefold() in seen: continue
        center=e.get("center",{}); plat=e.get("lat",center.get("lat")); plon=e.get("lon",center.get("lon"))
        if plat is None or plon is None: continue
        seen.add(name.casefold()); raw=tags.get("stars") or tags.get("rating")
        try: rating=float(str(raw).replace(",",".")) if raw else None
        except (ValueError,TypeError): rating=None
        out.append({"name":name,"rating":rating,"lat":plat,"lon":plon,"distance_km":round(haversine(lat,lon,plat,plon),1),"type":tags.get("tourism") or tags.get("historic") or tags.get("leisure") or "local"})
    return sorted(out,key=lambda x:x["distance_km"])[:limit]

def _amadeus_access_token():
    global AMADEUS_TOKEN, AMADEUS_TOKEN_EXPIRES
    client_id=os.getenv("AMADEUS_CLIENT_ID"); client_secret=os.getenv("AMADEUS_CLIENT_SECRET")
    if not client_id or not client_secret: return None
    if AMADEUS_TOKEN and time.time()<AMADEUS_TOKEN_EXPIRES-30: return AMADEUS_TOKEN
    base=os.getenv("AMADEUS_BASE_URL","https://api.amadeus.com").rstrip("/")
    try:
        r=requests.post(f"{base}/v1/security/oauth2/token",data={"grant_type":"client_credentials","client_id":client_id,"client_secret":client_secret},timeout=4); r.raise_for_status(); data=r.json()
        AMADEUS_TOKEN=data["access_token"]; AMADEUS_TOKEN_EXPIRES=time.time()+int(data.get("expires_in",1799)); return AMADEUS_TOKEN
    except (requests.RequestException,ValueError,KeyError,TypeError): return None

def _airport_from_static(place): return CITY_AIRPORTS.get(normalize_text(place).split(",")[0].strip())

def _airport_from_amadeus(place,token):
    key=normalize_text(place).split(",")[0].strip()
    if key in AIRPORT_CACHE: return AIRPORT_CACHE[key]
    base=os.getenv("AMADEUS_BASE_URL","https://api.amadeus.com").rstrip("/")
    try:
        r=requests.get(f"{base}/v1/reference-data/locations",headers={"Authorization":f"Bearer {token}"},params={"subType":"CITY,AIRPORT","keyword":place.split(",")[0].strip(),"page[limit]":5},timeout=4); r.raise_for_status()
        for item in r.json().get("data",[]):
            code=item.get("iataCode")
            if code and len(code)==3: AIRPORT_CACHE[key]=code; return code
    except (requests.RequestException,ValueError,TypeError): pass
    return None

def resolve_airport(place,token): return _airport_from_static(place) or _airport_from_amadeus(place,token)

def _minutes_between(start,end):
    try:
        a=datetime.fromisoformat(start.replace("Z","+00:00")); b=datetime.fromisoformat(end.replace("Z","+00:00")); return max(0,int((b-a).total_seconds()//60))
    except (ValueError,TypeError): return None

def real_flights(origin,destination,travel_date):
    token=_amadeus_access_token()
    if not token: return [],"Ofertas aéreas reais não estão configuradas. Adicione AMADEUS_CLIENT_ID e AMADEUS_CLIENT_SECRET no .env."
    o,d=resolve_airport(origin,token),resolve_airport(destination,token)
    if not o or not d: return [],"Não foi possível identificar os aeroportos comerciais da rota."
    if o==d: return [],f"Não há voo entre essas cidades porque ambas usam o aeroporto comercial {o} como referência."
    base=os.getenv("AMADEUS_BASE_URL","https://api.amadeus.com").rstrip("/")
    try:
        r=requests.get(f"{base}/v2/shopping/flight-offers",headers={"Authorization":f"Bearer {token}"},params={"originLocationCode":o,"destinationLocationCode":d,"departureDate":travel_date.isoformat(),"adults":1,"currencyCode":"BRL","max":50},timeout=5); r.raise_for_status()
        flights=[]
        for offer in r.json().get("data",[]):
            its=offer.get("itineraries") or []
            if not its: continue
            segs=its[0].get("segments") or []
            if not segs: continue
            first,last=segs[0],segs[-1]; dep,arr=first.get("departure",{}),last.get("arrival",{}); price=offer.get("price",{}).get("grandTotal")
            if price is None: continue
            flights.append({"companhia":(offer.get("validatingAirlineCodes") or ["-"])[0],"saida":dep.get("at","")[11:16],"chegada":arr.get("at","")[11:16],"escalas":max(0,len(segs)-1),"duracao_min":_minutes_between(dep.get("at",""),arr.get("at","")),"preco":float(price),"currency":offer.get("price",{}).get("currency","BRL"),"real":True,"origem_aeroporto":o,"destino_aeroporto":d})
        flights.sort(key=lambda x:x["preco"]); return (flights,None) if flights else ([],"Nenhuma oferta aérea real foi retornada para essa rota e data.")
    except requests.HTTPError as exc:
        if exc.response is not None and exc.response.status_code==400: return [],"A fonte aérea recusou os parâmetros da rota/data."
        return [],"A fonte aérea não respondeu com uma oferta válida."
    except (requests.RequestException,ValueError,KeyError,TypeError): return [],"Não foi possível consultar ofertas aéreas reais agora."


def amadeus_hotels(lat, lon, checkin, nights=1, limit=12):
    token=_amadeus_access_token()
    if not token:
        return [], "Hotéis com preço em tempo real exigem as credenciais Amadeus no .env."
    base=os.getenv("AMADEUS_BASE_URL","https://api.amadeus.com").rstrip("/")
    try:
        r=requests.get(
            f"{base}/v1/reference-data/locations/hotels/by-geocode",
            headers={"Authorization":f"Bearer {token}"},
            params={"latitude":lat,"longitude":lon,"radius":10,"radiusUnit":"KM","hotelSource":"ALL"},
            timeout=5,
        )
        r.raise_for_status()
        hotels=r.json().get("data",[])[:limit]
        if not hotels:
            return [], "A Amadeus não encontrou hotéis nessa área."
        checkout=checkin+timedelta(days=max(1,int(nights)))
        ids=[h.get("hotelId") for h in hotels if h.get("hotelId")]
        if not ids:
            return [], "A lista de hotéis não trouxe identificadores para cotação."
        offers=[]
        # The Hotel Offers endpoint accepts multiple hotelIds; keep the request small.
        for start in range(0,len(ids),10):
            chunk=ids[start:start+10]
            rr=requests.get(
                f"{base}/v3/shopping/hotel-offers",
                headers={"Authorization":f"Bearer {token}"},
                params={
                    "hotelIds":",".join(chunk),
                    "adults":1,
                    "checkInDate":checkin.isoformat(),
                    "checkOutDate":checkout.isoformat(),
                    "roomQuantity":1,
                    "currency":"BRL",
                },
                timeout=8,
            )
            if rr.status_code in (400,404):
                continue
            rr.raise_for_status()
            offers.extend(rr.json().get("data",[]))
        if not offers:
            return [], "A Amadeus encontrou hotéis, mas nenhum quarto disponível para essas datas."
        by_id={h.get("hotelId"):h for h in hotels}
        out=[]
        for item in offers:
            hotel=item.get("hotel",{})
            hotel_id=hotel.get("hotelId")
            source=by_id.get(hotel_id,{})
            available=item.get("available",True)
            if available is False: continue
            best=None
            for offer in item.get("offers",[]) or []:
                raw=offer.get("price",{}).get("total") or offer.get("price",{}).get("base")
                try: value=float(raw)
                except (ValueError,TypeError): continue
                if best is None or value<best[0]: best=(value,offer)
            if best is None: continue
            value,offer=best
            hlat=hotel.get("latitude") or source.get("geoCode",{}).get("latitude")
            hlon=hotel.get("longitude") or source.get("geoCode",{}).get("longitude")
            distance=round(haversine(lat,lon,float(hlat),float(hlon)),1) if hlat is not None and hlon is not None else None
            out.append({
                "name":hotel.get("name") or source.get("name") or "Hotel",
                "hotel_id":hotel_id,
                "lat":hlat,"lon":hlon,"distance_km":distance,
                "type":"hotel",
                "rating":None,
                "preco":value,
                "currency":offer.get("price",{}).get("currency") or "BRL",
                "preco_noite":round(value/max(1,int(nights)),2),
                "noites":max(1,int(nights)),
                "quarto":(offer.get("room",{}).get("description",{}) or {}).get("text"),
                "real":True,
                "source":"Amadeus Hotel Search",
            })
        out.sort(key=lambda x:x["preco"])
        return out, None
    except requests.HTTPError as exc:
        if exc.response is not None and exc.response.status_code==400:
            return [], "A Amadeus recusou os parâmetros da hospedagem/data."
        return [], "A fonte de hospedagem não respondeu com uma cotação válida."
    except (requests.RequestException,ValueError,TypeError,KeyError):
        return [], "Não foi possível consultar preços reais de hotéis agora."


def safe_booking_url(value):
    if not isinstance(value, str):
        return None
    value=value.strip()
    try:
        parsed=urlparse(value)
    except ValueError:
        return None
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return None
    return value

def amadeus_activities(lat, lon, limit=30):
    token=_amadeus_access_token()
    if not token:
        return [], "Atividades comerciais reais exigem as credenciais Amadeus no .env."
    base=os.getenv("AMADEUS_BASE_URL","https://api.amadeus.com").rstrip("/")
    try:
        r=requests.get(
            f"{base}/v1/shopping/activities",
            headers={"Authorization":f"Bearer {token}"},
            params={"latitude":lat,"longitude":lon,"radius":10},
            timeout=6,
        )
        r.raise_for_status()
        out=[]
        for item in r.json().get("data",[])[:limit]:
            geo=item.get("geoCode",{}) or {}
            plat,plon=geo.get("latitude"),geo.get("longitude")
            try: rating=float(item.get("rating")) if item.get("rating") is not None else None
            except (ValueError,TypeError): rating=None
            raw=(item.get("price") or {}).get("amount")
            try: price=float(raw) if raw is not None else None
            except (ValueError,TypeError): price=None
            out.append({
                "name":item.get("name") or "Atividade",
                "rating":rating,
                "lat":plat,"lon":plon,
                "distance_km":round(haversine(lat,lon,float(plat),float(plon)),1) if plat is not None and plon is not None else None,
                "type":"atividade turística",
                "preco":price,
                "currency":(item.get("price") or {}).get("currencyCode"),
                "descricao":item.get("shortDescription"),
                "booking_link":safe_booking_url(item.get("bookingLink")),
                "real":True,
                "source":"Amadeus Destination Experiences",
            })
        return sorted(out,key=lambda x:(x["distance_km"] if x["distance_km"] is not None else 9999)), None
    except (requests.RequestException,ValueError,TypeError,KeyError):
        return [], "Não foi possível consultar atividades turísticas reais agora."

def _clickbus_access_token():
    global CLICKBUS_TOKEN, CLICKBUS_TOKEN_EXPIRES
    username=os.getenv("CLICKBUS_USERNAME")
    password=os.getenv("CLICKBUS_PASSWORD")
    if not username or not password:
        return None
    if CLICKBUS_TOKEN and time.time()<CLICKBUS_TOKEN_EXPIRES-60:
        return CLICKBUS_TOKEN
    base=os.getenv("CLICKBUS_BASE_URL","https://platform-bff-partners.stg.clickbus.net/partners/api").rstrip("/")
    try:
        r=requests.post(
            f"{base}/oauth/basic-token",
            json={"grant_type":"client_credentials"},
            headers={"Content-Type":"application/json"},
            auth=(username,password),
            timeout=5,
        )
        r.raise_for_status(); data=r.json()
        CLICKBUS_TOKEN=data.get("accessToken") or data.get("access_token")
        CLICKBUS_TOKEN_EXPIRES=time.time()+int(data.get("expiresIn") or data.get("expires_in") or 3600)
        return CLICKBUS_TOKEN
    except (requests.RequestException,ValueError,TypeError,KeyError):
        return None


def _clickbus_place(city,token):
    base=os.getenv("CLICKBUS_BASE_URL","https://platform-bff-partners.stg.clickbus.net/partners/api").rstrip("/")
    try:
        # ClickBus requires its own place slug for the trips search.
        r=requests.get(
            f"{base}/v4/places/by-location",
            headers={"Authorization":f"Bearer {token}","Accept":"application/json"},
            params={"cityName":city.split(",")[0].strip(),"limit":20,"fields":"id,name,slug,terminal,city,state,country,latitude,longitude"},
            timeout=5,
        )
        r.raise_for_status(); data=r.json()
        items=data.get("content") or data.get("data") or []
        if isinstance(items,dict): items=items.get("content") or []
        if not items: return None
        return items[0].get("slug")
    except (requests.RequestException,ValueError,TypeError,KeyError):
        return None


def real_buses(origin,destination,travel_date):
    token=_clickbus_access_token()
    if not token:
        return [],"Ônibus reais exigem credenciais de parceiro ClickBus (CLICKBUS_USERNAME e CLICKBUS_PASSWORD) no .env."
    from_slug=_clickbus_place(origin,token); to_slug=_clickbus_place(destination,token)
    if not from_slug or not to_slug:
        return [],"Não foi possível localizar as cidades na API ClickBus."
    base=os.getenv("CLICKBUS_BASE_URL","https://platform-bff-partners.stg.clickbus.net/partners/api").rstrip("/")
    try:
        r=requests.get(
            f"{base}/v5/trips",
            headers={"Authorization":f"Bearer {token}","Accept":"application/json"},
            params={"from":from_slug,"to":to_slug,"departureDate":travel_date.isoformat()},
            timeout=8,
        )
        r.raise_for_status(); payload=r.json()
        items=payload.get("content") or payload.get("data") or payload.get("trips") or []
        if isinstance(items,dict): items=items.get("content") or items.get("data") or items.get("trips") or []
        out=[]
        for x in items[:50]:
            company=x.get("travelCompany") or {}
            dep=x.get("departure") or {}; arr=x.get("arrival") or {}
            price=x.get("price")
            if isinstance(price,dict): price=price.get("default") or price.get("discounted") or price.get("value")
            try: price=float(price)
            except (ValueError,TypeError): continue
            out.append({
                "companhia":company.get("name") or x.get("travelCompanyName") or "Viação",
                "classe":(x.get("serviceClass") or {}).get("name") if isinstance(x.get("serviceClass"),dict) else x.get("serviceClass") or x.get("busName") or "",
                "saida":(dep.get("schedule") or dep).get("departureTime") or (dep.get("schedule") or dep).get("time") or dep.get("at") or "",
                "chegada":(arr.get("schedule") or arr).get("arrivalTime") or (arr.get("schedule") or arr).get("time") or arr.get("at") or "",
                "duracao":x.get("duration") if isinstance(x.get("duration"),str) else str(x.get("duration") or ""),
                "preco":price,"currency":x.get("currency") or "BRL","available_seats":x.get("availableSeats"),"real":True,"source":"ClickBus"
            })
        out.sort(key=lambda x:x["preco"]); return (out,None) if out else ([],"Nenhuma viagem de ônibus real foi encontrada para essa rota e data.")
    except requests.HTTPError as exc:
        if exc.response is not None and exc.response.status_code==401: return [],"As credenciais ClickBus foram recusadas ou expiraram."
        return [],"A fonte de ônibus não respondeu com uma oferta válida."
    except (requests.RequestException,ValueError,TypeError,KeyError):
        return [],"Não foi possível consultar viagens de ônibus reais agora."

def search_trip(origin,destination,travel_date, nights=1):
    with ThreadPoolExecutor(max_workers=2) as pool:
        flight_future=pool.submit(real_flights,origin,destination,travel_date)
        geo_future=pool.submit(geocode,destination)
        flights,flight_message=flight_future.result()
        dest_geo=geo_future.result()
    if not dest_geo: raise ValueError("Não foi possível localizar o destino informado.")

    # After geocoding, query independent destination sources concurrently.
    with ThreadPoolExecutor(max_workers=3) as pool:
        hotel_future=pool.submit(amadeus_hotels,dest_geo["lat"],dest_geo["lon"],travel_date,nights,12)
        activity_future=pool.submit(amadeus_activities,dest_geo["lat"],dest_geo["lon"],30)
        osm_future=pool.submit(overpass,dest_geo["lat"],dest_geo["lon"])
        hotels,hotel_message=hotel_future.result()
        activities,activity_message=activity_future.result()
        elements=osm_future.result()

    # If Amadeus is not configured or has no result, keep OSM as a real fallback.
    osm_hotels=[]; osm_attractions=[]
    attraction_types={"attraction","museum","gallery","theme_park","zoo","viewpoint","aquarium"}; historic_types={"monument","memorial","castle","ruins","archaeological_site"}
    for e in elements:
        tags=e.get("tags",{})
        if tags.get("tourism") in {"hotel","hostel","guest_house"}: osm_hotels.append(e)
        elif tags.get("tourism") in attraction_types or tags.get("historic") in historic_types or tags.get("leisure")=="park": osm_attractions.append(e)

    if not hotels:
        hotels=normalize_places(osm_hotels,dest_geo["lat"],dest_geo["lon"],40)
        if hotels and not hotel_message:
            hotel_message="Hotéis localizados no OpenStreetMap; preços individuais não estão disponíveis nessa fonte."
    if not activities:
        activities=normalize_places(osm_attractions,dest_geo["lat"],dest_geo["lon"],50)
        if activities and not activity_message:
            activity_message="Pontos turísticos localizados no OpenStreetMap."

    buses,bus_message=real_buses(origin,destination,travel_date)
    return {
        "origin":{"query":origin},"destination":dest_geo,
        "hotel_reference_daily_average":PUBLIC_HOTEL_DAILY_AVERAGE,
        "hotels":hotels,"hotel_message":hotel_message,
        "attractions":activities,"activity_message":activity_message,
        "flights":flights,"flight_message":flight_message,
        "buses":buses,"bus_message":bus_message,
        "data_sources":{
            "osm":bool(elements),
            "amadeus_hotels":any(x.get("source")=="Amadeus Hotel Search" for x in hotels),
            "amadeus_activities":any(x.get("source")=="Amadeus Destination Experiences" for x in activities),
            "flights":bool(flights),"buses":bool(buses)
        }
    }
