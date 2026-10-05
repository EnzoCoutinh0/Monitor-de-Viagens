# Linha 1: Importa uma biblioteca/módulo necessário para executar o código abaixo.
import os
# Linha 2: Importa uma biblioteca/módulo necessário para executar o código abaixo.
import time
# Linha 3: Importa uma biblioteca/módulo necessário para executar o código abaixo.
import unicodedata
# Linha 4: Importa um módulo ou componente específico para ser usado neste arquivo.
from concurrent.futures import ThreadPoolExecutor
# Linha 5: Importa um módulo ou componente específico para ser usado neste arquivo.
from datetime import datetime, timedelta
# Linha 6: Importa um módulo ou componente específico para ser usado neste arquivo.
from math import radians, sin, cos, asin, sqrt
# Linha 7: Importa uma biblioteca/módulo necessário para executar o código abaixo.
import requests
# Linha 8: Importa um módulo ou componente específico para ser usado neste arquivo.
from urllib.parse import urlparse

# Linha 10: Cria ou atualiza uma variável com o valor calculado à direita.
TIMEOUT = min(max(int(os.getenv("REQUEST_TIMEOUT", "3")), 2), 5)
# Linha 11: Cria ou atualiza uma variável com o valor calculado à direita.
UA = "TravelMonitor/4.0 (local educational project)"
# Linha 12: Cria ou atualiza uma variável com o valor calculado à direita.
OVERPASS_URLS = [
    # Linha 13: Executa a instrução Python desta linha.
    os.getenv("OVERPASS_URL", "https://overpass-api.de/api/interpreter"),
    # Linha 14: Executa a instrução Python desta linha.
    "https://overpass.private.coffee/api/interpreter",
    # Linha 15: Executa a instrução Python desta linha.
    "https://maps.mail.ru/osm/tools/overpass/api/interpreter",
# Linha 16: Executa a instrução Python desta linha.
]
# Linha 17: Cria ou atualiza uma variável com o valor calculado à direita.
OVERPASS_CACHE = {}
# Linha 18: Cria ou atualiza uma variável com o valor calculado à direita.
OVERPASS_CACHE_TTL = 300
# Linha 19: Cria ou atualiza uma variável com o valor calculado à direita.
GEOCODE_CACHE = {}
# Linha 20: Cria ou atualiza uma variável com o valor calculado à direita.
AIRPORT_CACHE = {}
# Linha 21: Cria ou atualiza uma variável com o valor calculado à direita.
AMADEUS_TOKEN = None
# Linha 22: Cria ou atualiza uma variável com o valor calculado à direita.
AMADEUS_TOKEN_EXPIRES = 0
# Linha 23: Cria ou atualiza uma variável com o valor calculado à direita.
CLICKBUS_TOKEN = None
# Linha 24: Cria ou atualiza uma variável com o valor calculado à direita.
CLICKBUS_TOKEN_EXPIRES = 0
# Linha 25: Cria ou atualiza uma variável com o valor calculado à direita.
PUBLIC_HOTEL_DAILY_AVERAGE = 451.71

# Linha 27: Cria ou atualiza uma variável com o valor calculado à direita.
CITY_COORDS = {
    # Linha 28: Executa a instrução Python desta linha.
    "vitoria": (-20.3155, -40.3128),
    # Linha 29: Executa a instrução Python desta linha.
    "vila velha": (-20.3297, -40.2925),
    # Linha 30: Executa a instrução Python desta linha.
    "serra": (-20.1286, -40.3076),
    # Linha 31: Executa a instrução Python desta linha.
    "cariacica": (-20.2639, -40.4169),
    # Linha 32: Executa a instrução Python desta linha.
    "guarapari": (-20.6736, -40.4978),
    # Linha 33: Executa a instrução Python desta linha.
    "sao paulo": (-23.5505, -46.6333),
    # Linha 34: Executa a instrução Python desta linha.
    "campinas": (-22.9099, -47.0626),
    # Linha 35: Executa a instrução Python desta linha.
    "rio de janeiro": (-22.9068, -43.1729),
    # Linha 36: Executa a instrução Python desta linha.
    "belo horizonte": (-19.9167, -43.9345),
    # Linha 37: Executa a instrução Python desta linha.
    "brasilia": (-15.7939, -47.8828),
    # Linha 38: Executa a instrução Python desta linha.
    "curitiba": (-25.4284, -49.2733),
    # Linha 39: Executa a instrução Python desta linha.
    "porto alegre": (-30.0346, -51.2177),
    # Linha 40: Executa a instrução Python desta linha.
    "florianopolis": (-27.5954, -48.5480),
    # Linha 41: Executa a instrução Python desta linha.
    "recife": (-8.0476, -34.8770),
    # Linha 42: Executa a instrução Python desta linha.
    "salvador": (-12.9777, -38.5016),
    # Linha 43: Executa a instrução Python desta linha.
    "fortaleza": (-3.7319, -38.5267),
    # Linha 44: Executa a instrução Python desta linha.
    "manaus": (-3.1190, -60.0217),
    # Linha 45: Executa a instrução Python desta linha.
    "belem": (-1.4558, -48.4902),
    # Linha 46: Executa a instrução Python desta linha.
    "goiania": (-16.6869, -49.2648),
    # Linha 47: Executa a instrução Python desta linha.
    "cuiaba": (-15.6014, -56.0979),
    # Linha 48: Executa a instrução Python desta linha.
    "campo grande": (-20.4697, -54.6201),
# Linha 49: Executa a instrução Python desta linha.
}

# Linha 51: Cria ou atualiza uma variável com o valor calculado à direita.
CITY_AIRPORTS = {
    # Linha 52: Executa a instrução Python desta linha.
    "vitoria":"VIX","vila velha":"VIX","serra":"VIX","cariacica":"VIX","guarapari":"VIX",
    # Linha 53: Executa a instrução Python desta linha.
    "sao paulo":"GRU","campinas":"VCP","santos":"GRU","sao jose dos campos":"GRU",
    # Linha 54: Executa a instrução Python desta linha.
    "rio de janeiro":"GIG","niteroi":"GIG","petropolis":"GIG","cabo frio":"CFB",
    # Linha 55: Executa a instrução Python desta linha.
    "belo horizonte":"CNF","uberlandia":"UDI","brasilia":"BSB","goiania":"GYN",
    # Linha 56: Executa a instrução Python desta linha.
    "curitiba":"CWB","londrina":"LDB","foz do iguacu":"IGU","porto alegre":"POA",
    # Linha 57: Executa a instrução Python desta linha.
    "florianopolis":"FLN","joinville":"JOI","blumenau":"NVT","balneario camboriu":"NVT",
    # Linha 58: Executa a instrução Python desta linha.
    "recife":"REC","salvador":"SSA","porto seguro":"BPS","fortaleza":"FOR","natal":"NAT",
    # Linha 59: Executa a instrução Python desta linha.
    "joao pessoa":"JPA","maceio":"MCZ","aracaju":"AJU","sao luis":"SLZ","teresina":"THE",
    # Linha 60: Executa a instrução Python desta linha.
    "belem":"BEL","manaus":"MAO","palmas":"PMW","campo grande":"CGR","cuiaba":"CGB",
    # Linha 61: Executa a instrução Python desta linha.
    "bonito":"BYO","jericoacoara":"JJD","maragogi":"MCZ","buzios":"CFB","paraty":"GIG",
    # Linha 62: Executa a instrução Python desta linha.
    "ilhabela":"GRU","ubatuba":"GRU","gramado":"POA","canela":"POA",
# Linha 63: Executa a instrução Python desta linha.
}

# Linha 65: Declara uma função reutilizável e define seus parâmetros.
def normalize_text(value):
    # Linha 66: Encerra a função e devolve o valor calculado.
    return "".join(c for c in unicodedata.normalize("NFD", str(value).lower()) if unicodedata.category(c) != "Mn")

# Linha 68: Declara uma função reutilizável e define seus parâmetros.
def geocode(place):
    # Linha 69: Cria ou atualiza uma variável com o valor calculado à direita.
    key = " ".join(normalize_text(place).split())
    # Linha 70: Verifica uma condição antes de executar o bloco indentado.
    if key in GEOCODE_CACHE:
        # Linha 71: Encerra a função e devolve o valor calculado.
        return GEOCODE_CACHE[key]

    # Linha 73: Cria ou atualiza uma variável com o valor calculado à direita.
    city_key = key.split(",")[0].strip()
    # Linha 74: Verifica uma condição antes de executar o bloco indentado.
    if city_key in CITY_COORDS:
        # Linha 75: Cria ou atualiza uma variável com o valor calculado à direita.
        lat, lon = CITY_COORDS[city_key]
        # Linha 76: Cria ou atualiza uma variável com o valor calculado à direita.
        result = {"lat": lat, "lon": lon, "display_name": place}
        # Linha 77: Cria ou atualiza uma variável com o valor calculado à direita.
        GEOCODE_CACHE[key] = result
        # Linha 78: Encerra a função e devolve o valor calculado.
        return result

    # Linha 80: Inicia um bloco para tratar possíveis erros sem interromper a aplicação.
    try:
        # Linha 81: Cria ou atualiza uma variável com o valor calculado à direita.
        r = requests.get("https://nominatim.openstreetmap.org/search", params={"q":place,"format":"jsonv2","limit":1,"countrycodes":"br"}, headers={"User-Agent":UA}, timeout=3)
        # Linha 82: Cria ou atualiza uma variável com o valor calculado à direita.
        r.raise_for_status(); data=r.json()
        # Linha 83: Verifica uma condição antes de executar o bloco indentado.
        if not data: return None
        # Linha 84: Cria ou atualiza uma variável com o valor calculado à direita.
        result={"lat":float(data[0]["lat"]),"lon":float(data[0]["lon"]),"display_name":data[0].get("display_name",place)}
        # Linha 85: Cria ou atualiza uma variável com o valor calculado à direita.
        GEOCODE_CACHE[key]=result; return result
    # Linha 86: Captura um tipo de erro ocorrido no bloco try.
    except (requests.RequestException,ValueError,KeyError,TypeError): return None

# Linha 88: Declara uma função reutilizável e define seus parâmetros.
def haversine(lat1,lon1,lat2,lon2):
    # Linha 89: Cria ou atualiza uma variável com o valor calculado à direita.
    radius=6371.0; dlat=radians(lat2-lat1); dlon=radians(lon2-lon1)
    # Linha 90: Cria ou atualiza uma variável com o valor calculado à direita.
    a=sin(dlat/2)**2+cos(radians(lat1))*cos(radians(lat2))*sin(dlon/2)**2
    # Linha 91: Encerra a função e devolve o valor calculado.
    return 2*radius*asin(sqrt(a))

# Linha 93: Declara uma função reutilizável e define seus parâmetros.
def _overpass_request(url, query):
    # Linha 94: Inicia um bloco para tratar possíveis erros sem interromper a aplicação.
    try:
        # Linha 95: Cria ou atualiza uma variável com o valor calculado à direita.
        r = requests.post(
            # Linha 96: Executa a instrução Python desta linha.
            url,
            # Linha 97: Cria ou atualiza uma variável com o valor calculado à direita.
            data=query,
            # Linha 98: Cria ou atualiza uma variável com o valor calculado à direita.
            headers={"User-Agent": UA, "Accept": "application/json"},
            # Linha 99: Cria ou atualiza uma variável com o valor calculado à direita.
            timeout=TIMEOUT,
        # Linha 100: Executa a instrução Python desta linha.
        )
        # Linha 101: Executa a instrução Python desta linha.
        r.raise_for_status()
        # Linha 102: Cria ou atualiza uma variável com o valor calculado à direita.
        elements = r.json().get("elements", [])
        # Linha 103: Encerra a função e devolve o valor calculado.
        return elements if isinstance(elements, list) else []
    # Linha 104: Captura um tipo de erro ocorrido no bloco try.
    except (requests.RequestException, ValueError, TypeError):
        # Linha 105: Encerra a função e devolve o valor calculado.
        return None


# Linha 108: Declara uma função reutilizável e define seus parâmetros.
def overpass(lat, lon):
    # Linha 109: Executa a instrução Python desta linha.
    # Cache successful OSM/Overpass results so repeating a saved search does
    # Linha 110: Executa a instrução Python desta linha.
    # not immediately hit the public services again.
    # Linha 111: Cria ou atualiza uma variável com o valor calculado à direita.
    cache_key=(round(float(lat),4),round(float(lon),4))
    # Linha 112: Cria ou atualiza uma variável com o valor calculado à direita.
    cached=OVERPASS_CACHE.get(cache_key)
    # Linha 113: Verifica uma condição antes de executar o bloco indentado.
    if cached and time.time()-cached[0] < OVERPASS_CACHE_TTL:
        # Linha 114: Encerra a função e devolve o valor calculado.
        return cached[1]

    # Linha 116: Cria ou atualiza uma variável com o valor calculado à direita.
    query=(
        # Linha 117: Executa a instrução Python desta linha.
        '[out:json][timeout:4];'
        # Linha 118: Executa a instrução Python desta linha.
        '(nwr["tourism"~"hotel|hostel|guest_house|attraction|museum|gallery|'
        # Linha 119: Executa a instrução Python desta linha.
        'theme_park|zoo|viewpoint|aquarium"](around:8000,%s,%s);'
        # Linha 120: Executa a instrução Python desta linha.
        'nwr["historic"~"monument|memorial|castle|ruins|archaeological_site"]'
        # Linha 121: Executa a instrução Python desta linha.
        '(around:8000,%s,%s);'
        # Linha 122: Cria ou atualiza uma variável com o valor calculado à direita.
        'nwr["leisure"="park"](around:8000,%s,%s););'
        # Linha 123: Executa a instrução Python desta linha.
        'out center tags;'
    # Linha 124: Executa a instrução Python desta linha.
    ) % (lat, lon, lat, lon, lat, lon)

    # Linha 126: Executa a instrução Python desta linha.
    # Use one public instance at a time and fall back only after failure.
    # Linha 127: Executa a instrução Python desta linha.
    # This is friendlier to shared Overpass infrastructure than firing the
    # Linha 128: Executa a instrução Python desta linha.
    # same query at several public servers simultaneously.
    # Linha 129: Percorre os itens de uma coleção ou sequência.
    for url in OVERPASS_URLS:
        # Linha 130: Cria ou atualiza uma variável com o valor calculado à direita.
        result=_overpass_request(url,query)
        # Linha 131: Verifica uma condição antes de executar o bloco indentado.
        if result is not None:
            # Linha 132: Cria ou atualiza uma variável com o valor calculado à direita.
            OVERPASS_CACHE[cache_key]=(time.time(),result)
            # Linha 133: Encerra a função e devolve o valor calculado.
            return result
    # Linha 134: Encerra a função e devolve o valor calculado.
    return []

# Linha 136: Declara uma função reutilizável e define seus parâmetros.
def normalize_places(elements,lat,lon,limit=30):
    # Linha 137: Cria ou atualiza uma variável com o valor calculado à direita.
    out=[]; seen=set()
    # Linha 138: Percorre os itens de uma coleção ou sequência.
    for e in elements:
        # Linha 139: Cria ou atualiza uma variável com o valor calculado à direita.
        tags=e.get("tags",{}); name=(tags.get("name") or "").strip()
        # Linha 140: Verifica uma condição antes de executar o bloco indentado.
        if not name or name.casefold() in seen: continue
        # Linha 141: Cria ou atualiza uma variável com o valor calculado à direita.
        center=e.get("center",{}); plat=e.get("lat",center.get("lat")); plon=e.get("lon",center.get("lon"))
        # Linha 142: Verifica uma condição antes de executar o bloco indentado.
        if plat is None or plon is None: continue
        # Linha 143: Cria ou atualiza uma variável com o valor calculado à direita.
        seen.add(name.casefold()); raw=tags.get("stars") or tags.get("rating")
        # Linha 144: Cria ou atualiza uma variável com o valor calculado à direita.
        try: rating=float(str(raw).replace(",",".")) if raw else None
        # Linha 145: Cria ou atualiza uma variável com o valor calculado à direita.
        except (ValueError,TypeError): rating=None
        # Linha 146: Executa a instrução Python desta linha.
        out.append({"name":name,"rating":rating,"lat":plat,"lon":plon,"distance_km":round(haversine(lat,lon,plat,plon),1),"type":tags.get("tourism") or tags.get("historic") or tags.get("leisure") or "local"})
    # Linha 147: Encerra a função e devolve o valor calculado.
    return sorted(out,key=lambda x:x["distance_km"])[:limit]

# Linha 149: Declara uma função reutilizável e define seus parâmetros.
def _amadeus_access_token():
    # Linha 150: Executa a instrução Python desta linha.
    global AMADEUS_TOKEN, AMADEUS_TOKEN_EXPIRES
    # Linha 151: Cria ou atualiza uma variável com o valor calculado à direita.
    client_id=os.getenv("AMADEUS_CLIENT_ID"); client_secret=os.getenv("AMADEUS_CLIENT_SECRET")
    # Linha 152: Verifica uma condição antes de executar o bloco indentado.
    if not client_id or not client_secret: return None
    # Linha 153: Verifica uma condição antes de executar o bloco indentado.
    if AMADEUS_TOKEN and time.time()<AMADEUS_TOKEN_EXPIRES-30: return AMADEUS_TOKEN
    # Linha 154: Cria ou atualiza uma variável com o valor calculado à direita.
    base=os.getenv("AMADEUS_BASE_URL","https://api.amadeus.com").rstrip("/")
    # Linha 155: Inicia um bloco para tratar possíveis erros sem interromper a aplicação.
    try:
        # Linha 156: Cria ou atualiza uma variável com o valor calculado à direita.
        r=requests.post(f"{base}/v1/security/oauth2/token",data={"grant_type":"client_credentials","client_id":client_id,"client_secret":client_secret},timeout=4); r.raise_for_status(); data=r.json()
        # Linha 157: Cria ou atualiza uma variável com o valor calculado à direita.
        AMADEUS_TOKEN=data["access_token"]; AMADEUS_TOKEN_EXPIRES=time.time()+int(data.get("expires_in",1799)); return AMADEUS_TOKEN
    # Linha 158: Captura um tipo de erro ocorrido no bloco try.
    except (requests.RequestException,ValueError,KeyError,TypeError): return None

# Linha 160: Declara uma função reutilizável e define seus parâmetros.
def _airport_from_static(place): return CITY_AIRPORTS.get(normalize_text(place).split(",")[0].strip())

# Linha 162: Declara uma função reutilizável e define seus parâmetros.
def _airport_from_amadeus(place,token):
    # Linha 163: Cria ou atualiza uma variável com o valor calculado à direita.
    key=normalize_text(place).split(",")[0].strip()
    # Linha 164: Verifica uma condição antes de executar o bloco indentado.
    if key in AIRPORT_CACHE: return AIRPORT_CACHE[key]
    # Linha 165: Cria ou atualiza uma variável com o valor calculado à direita.
    base=os.getenv("AMADEUS_BASE_URL","https://api.amadeus.com").rstrip("/")
    # Linha 166: Inicia um bloco para tratar possíveis erros sem interromper a aplicação.
    try:
        # Linha 167: Cria ou atualiza uma variável com o valor calculado à direita.
        r=requests.get(f"{base}/v1/reference-data/locations",headers={"Authorization":f"Bearer {token}"},params={"subType":"CITY,AIRPORT","keyword":place.split(",")[0].strip(),"page[limit]":5},timeout=4); r.raise_for_status()
        # Linha 168: Percorre os itens de uma coleção ou sequência.
        for item in r.json().get("data",[]):
            # Linha 169: Cria ou atualiza uma variável com o valor calculado à direita.
            code=item.get("iataCode")
            # Linha 170: Verifica uma condição antes de executar o bloco indentado.
            if code and len(code)==3: AIRPORT_CACHE[key]=code; return code
    # Linha 171: Captura um tipo de erro ocorrido no bloco try.
    except (requests.RequestException,ValueError,TypeError): pass
    # Linha 172: Encerra a função e devolve o valor calculado.
    return None

# Linha 174: Declara uma função reutilizável e define seus parâmetros.
def resolve_airport(place,token): return _airport_from_static(place) or _airport_from_amadeus(place,token)

# Linha 176: Declara uma função reutilizável e define seus parâmetros.
def _minutes_between(start,end):
    # Linha 177: Inicia um bloco para tratar possíveis erros sem interromper a aplicação.
    try:
        # Linha 178: Cria ou atualiza uma variável com o valor calculado à direita.
        a=datetime.fromisoformat(start.replace("Z","+00:00")); b=datetime.fromisoformat(end.replace("Z","+00:00")); return max(0,int((b-a).total_seconds()//60))
    # Linha 179: Captura um tipo de erro ocorrido no bloco try.
    except (ValueError,TypeError): return None

# Linha 181: Declara uma função reutilizável e define seus parâmetros.
def real_flights(origin,destination,travel_date):
    # Linha 182: Cria ou atualiza uma variável com o valor calculado à direita.
    token=_amadeus_access_token()
    # Linha 183: Verifica uma condição antes de executar o bloco indentado.
    if not token: return [],"Ofertas aéreas reais não estão configuradas. Adicione AMADEUS_CLIENT_ID e AMADEUS_CLIENT_SECRET no .env."
    # Linha 184: Cria ou atualiza uma variável com o valor calculado à direita.
    o,d=resolve_airport(origin,token),resolve_airport(destination,token)
    # Linha 185: Verifica uma condição antes de executar o bloco indentado.
    if not o or not d: return [],"Não foi possível identificar os aeroportos comerciais da rota."
    # Linha 186: Verifica uma condição antes de executar o bloco indentado.
    if o==d: return [],f"Não há voo entre essas cidades porque ambas usam o aeroporto comercial {o} como referência."
    # Linha 187: Cria ou atualiza uma variável com o valor calculado à direita.
    base=os.getenv("AMADEUS_BASE_URL","https://api.amadeus.com").rstrip("/")
    # Linha 188: Inicia um bloco para tratar possíveis erros sem interromper a aplicação.
    try:
        # Linha 189: Cria ou atualiza uma variável com o valor calculado à direita.
        r=requests.get(f"{base}/v2/shopping/flight-offers",headers={"Authorization":f"Bearer {token}"},params={"originLocationCode":o,"destinationLocationCode":d,"departureDate":travel_date.isoformat(),"adults":1,"currencyCode":"BRL","max":50},timeout=5); r.raise_for_status()
        # Linha 190: Cria ou atualiza uma variável com o valor calculado à direita.
        flights=[]
        # Linha 191: Percorre os itens de uma coleção ou sequência.
        for offer in r.json().get("data",[]):
            # Linha 192: Cria ou atualiza uma variável com o valor calculado à direita.
            its=offer.get("itineraries") or []
            # Linha 193: Verifica uma condição antes de executar o bloco indentado.
            if not its: continue
            # Linha 194: Cria ou atualiza uma variável com o valor calculado à direita.
            segs=its[0].get("segments") or []
            # Linha 195: Verifica uma condição antes de executar o bloco indentado.
            if not segs: continue
            # Linha 196: Cria ou atualiza uma variável com o valor calculado à direita.
            first,last=segs[0],segs[-1]; dep,arr=first.get("departure",{}),last.get("arrival",{}); price=offer.get("price",{}).get("grandTotal")
            # Linha 197: Verifica uma condição antes de executar o bloco indentado.
            if price is None: continue
            # Linha 198: Executa a instrução Python desta linha.
            flights.append({"companhia":(offer.get("validatingAirlineCodes") or ["-"])[0],"saida":dep.get("at","")[11:16],"chegada":arr.get("at","")[11:16],"escalas":max(0,len(segs)-1),"duracao_min":_minutes_between(dep.get("at",""),arr.get("at","")),"preco":float(price),"currency":offer.get("price",{}).get("currency","BRL"),"real":True,"origem_aeroporto":o,"destino_aeroporto":d})
        # Linha 199: Cria ou atualiza uma variável com o valor calculado à direita.
        flights.sort(key=lambda x:x["preco"]); return (flights,None) if flights else ([],"Nenhuma oferta aérea real foi retornada para essa rota e data.")
    # Linha 200: Captura um tipo de erro ocorrido no bloco try.
    except requests.HTTPError as exc:
        # Linha 201: Verifica uma condição antes de executar o bloco indentado.
        if exc.response is not None and exc.response.status_code==400: return [],"A fonte aérea recusou os parâmetros da rota/data."
        # Linha 202: Encerra a função e devolve o valor calculado.
        return [],"A fonte aérea não respondeu com uma oferta válida."
    # Linha 203: Captura um tipo de erro ocorrido no bloco try.
    except (requests.RequestException,ValueError,KeyError,TypeError): return [],"Não foi possível consultar ofertas aéreas reais agora."


# Linha 206: Declara uma função reutilizável e define seus parâmetros.
def amadeus_hotels(lat, lon, checkin, nights=1, limit=12):
    # Linha 207: Cria ou atualiza uma variável com o valor calculado à direita.
    token=_amadeus_access_token()
    # Linha 208: Verifica uma condição antes de executar o bloco indentado.
    if not token:
        # Linha 209: Encerra a função e devolve o valor calculado.
        return [], "Hotéis com preço em tempo real exigem as credenciais Amadeus no .env."
    # Linha 210: Cria ou atualiza uma variável com o valor calculado à direita.
    base=os.getenv("AMADEUS_BASE_URL","https://api.amadeus.com").rstrip("/")
    # Linha 211: Inicia um bloco para tratar possíveis erros sem interromper a aplicação.
    try:
        # Linha 212: Cria ou atualiza uma variável com o valor calculado à direita.
        r=requests.get(
            # Linha 213: Executa a instrução Python desta linha.
            f"{base}/v1/reference-data/locations/hotels/by-geocode",
            # Linha 214: Cria ou atualiza uma variável com o valor calculado à direita.
            headers={"Authorization":f"Bearer {token}"},
            # Linha 215: Cria ou atualiza uma variável com o valor calculado à direita.
            params={"latitude":lat,"longitude":lon,"radius":10,"radiusUnit":"KM","hotelSource":"ALL"},
            # Linha 216: Cria ou atualiza uma variável com o valor calculado à direita.
            timeout=5,
        # Linha 217: Executa a instrução Python desta linha.
        )
        # Linha 218: Executa a instrução Python desta linha.
        r.raise_for_status()
        # Linha 219: Cria ou atualiza uma variável com o valor calculado à direita.
        hotels=r.json().get("data",[])[:limit]
        # Linha 220: Verifica uma condição antes de executar o bloco indentado.
        if not hotels:
            # Linha 221: Encerra a função e devolve o valor calculado.
            return [], "A Amadeus não encontrou hotéis nessa área."
        # Linha 222: Cria ou atualiza uma variável com o valor calculado à direita.
        checkout=checkin+timedelta(days=max(1,int(nights)))
        # Linha 223: Cria ou atualiza uma variável com o valor calculado à direita.
        ids=[h.get("hotelId") for h in hotels if h.get("hotelId")]
        # Linha 224: Verifica uma condição antes de executar o bloco indentado.
        if not ids:
            # Linha 225: Encerra a função e devolve o valor calculado.
            return [], "A lista de hotéis não trouxe identificadores para cotação."
        # Linha 226: Cria ou atualiza uma variável com o valor calculado à direita.
        offers=[]
        # Linha 227: Executa a instrução Python desta linha.
        # The Hotel Offers endpoint accepts multiple hotelIds; keep the request small.
        # Linha 228: Percorre os itens de uma coleção ou sequência.
        for start in range(0,len(ids),10):
            # Linha 229: Cria ou atualiza uma variável com o valor calculado à direita.
            chunk=ids[start:start+10]
            # Linha 230: Cria ou atualiza uma variável com o valor calculado à direita.
            rr=requests.get(
                # Linha 231: Executa a instrução Python desta linha.
                f"{base}/v3/shopping/hotel-offers",
                # Linha 232: Cria ou atualiza uma variável com o valor calculado à direita.
                headers={"Authorization":f"Bearer {token}"},
                # Linha 233: Cria ou atualiza uma variável com o valor calculado à direita.
                params={
                    # Linha 234: Executa a instrução Python desta linha.
                    "hotelIds":",".join(chunk),
                    # Linha 235: Executa a instrução Python desta linha.
                    "adults":1,
                    # Linha 236: Executa a instrução Python desta linha.
                    "checkInDate":checkin.isoformat(),
                    # Linha 237: Executa a instrução Python desta linha.
                    "checkOutDate":checkout.isoformat(),
                    # Linha 238: Executa a instrução Python desta linha.
                    "roomQuantity":1,
                    # Linha 239: Executa a instrução Python desta linha.
                    "currency":"BRL",
                # Linha 240: Executa a instrução Python desta linha.
                },
                # Linha 241: Cria ou atualiza uma variável com o valor calculado à direita.
                timeout=8,
            # Linha 242: Executa a instrução Python desta linha.
            )
            # Linha 243: Verifica uma condição antes de executar o bloco indentado.
            if rr.status_code in (400,404):
                # Linha 244: Executa a instrução Python desta linha.
                continue
            # Linha 245: Executa a instrução Python desta linha.
            rr.raise_for_status()
            # Linha 246: Executa a instrução Python desta linha.
            offers.extend(rr.json().get("data",[]))
        # Linha 247: Verifica uma condição antes de executar o bloco indentado.
        if not offers:
            # Linha 248: Encerra a função e devolve o valor calculado.
            return [], "A Amadeus encontrou hotéis, mas nenhum quarto disponível para essas datas."
        # Linha 249: Cria ou atualiza uma variável com o valor calculado à direita.
        by_id={h.get("hotelId"):h for h in hotels}
        # Linha 250: Cria ou atualiza uma variável com o valor calculado à direita.
        out=[]
        # Linha 251: Percorre os itens de uma coleção ou sequência.
        for item in offers:
            # Linha 252: Cria ou atualiza uma variável com o valor calculado à direita.
            hotel=item.get("hotel",{})
            # Linha 253: Cria ou atualiza uma variável com o valor calculado à direita.
            hotel_id=hotel.get("hotelId")
            # Linha 254: Cria ou atualiza uma variável com o valor calculado à direita.
            source=by_id.get(hotel_id,{})
            # Linha 255: Cria ou atualiza uma variável com o valor calculado à direita.
            available=item.get("available",True)
            # Linha 256: Verifica uma condição antes de executar o bloco indentado.
            if available is False: continue
            # Linha 257: Cria ou atualiza uma variável com o valor calculado à direita.
            best=None
            # Linha 258: Percorre os itens de uma coleção ou sequência.
            for offer in item.get("offers",[]) or []:
                # Linha 259: Cria ou atualiza uma variável com o valor calculado à direita.
                raw=offer.get("price",{}).get("total") or offer.get("price",{}).get("base")
                # Linha 260: Cria ou atualiza uma variável com o valor calculado à direita.
                try: value=float(raw)
                # Linha 261: Captura um tipo de erro ocorrido no bloco try.
                except (ValueError,TypeError): continue
                # Linha 262: Verifica uma condição antes de executar o bloco indentado.
                if best is None or value<best[0]: best=(value,offer)
            # Linha 263: Verifica uma condição antes de executar o bloco indentado.
            if best is None: continue
            # Linha 264: Cria ou atualiza uma variável com o valor calculado à direita.
            value,offer=best
            # Linha 265: Cria ou atualiza uma variável com o valor calculado à direita.
            hlat=hotel.get("latitude") or source.get("geoCode",{}).get("latitude")
            # Linha 266: Cria ou atualiza uma variável com o valor calculado à direita.
            hlon=hotel.get("longitude") or source.get("geoCode",{}).get("longitude")
            # Linha 267: Cria ou atualiza uma variável com o valor calculado à direita.
            distance=round(haversine(lat,lon,float(hlat),float(hlon)),1) if hlat is not None and hlon is not None else None
            # Linha 268: Executa a instrução Python desta linha.
            out.append({
                # Linha 269: Executa a instrução Python desta linha.
                "name":hotel.get("name") or source.get("name") or "Hotel",
                # Linha 270: Executa a instrução Python desta linha.
                "hotel_id":hotel_id,
                # Linha 271: Executa a instrução Python desta linha.
                "lat":hlat,"lon":hlon,"distance_km":distance,
                # Linha 272: Executa a instrução Python desta linha.
                "type":"hotel",
                # Linha 273: Executa a instrução Python desta linha.
                "rating":None,
                # Linha 274: Executa a instrução Python desta linha.
                "preco":value,
                # Linha 275: Executa a instrução Python desta linha.
                "currency":offer.get("price",{}).get("currency") or "BRL",
                # Linha 276: Executa a instrução Python desta linha.
                "preco_noite":round(value/max(1,int(nights)),2),
                # Linha 277: Executa a instrução Python desta linha.
                "noites":max(1,int(nights)),
                # Linha 278: Executa a instrução Python desta linha.
                "quarto":(offer.get("room",{}).get("description",{}) or {}).get("text"),
                # Linha 279: Executa a instrução Python desta linha.
                "real":True,
                # Linha 280: Executa a instrução Python desta linha.
                "source":"Amadeus Hotel Search",
            # Linha 281: Executa a instrução Python desta linha.
            })
        # Linha 282: Cria ou atualiza uma variável com o valor calculado à direita.
        out.sort(key=lambda x:x["preco"])
        # Linha 283: Encerra a função e devolve o valor calculado.
        return out, None
    # Linha 284: Captura um tipo de erro ocorrido no bloco try.
    except requests.HTTPError as exc:
        # Linha 285: Verifica uma condição antes de executar o bloco indentado.
        if exc.response is not None and exc.response.status_code==400:
            # Linha 286: Encerra a função e devolve o valor calculado.
            return [], "A Amadeus recusou os parâmetros da hospedagem/data."
        # Linha 287: Encerra a função e devolve o valor calculado.
        return [], "A fonte de hospedagem não respondeu com uma cotação válida."
    # Linha 288: Captura um tipo de erro ocorrido no bloco try.
    except (requests.RequestException,ValueError,TypeError,KeyError):
        # Linha 289: Encerra a função e devolve o valor calculado.
        return [], "Não foi possível consultar preços reais de hotéis agora."


# Linha 292: Declara uma função reutilizável e define seus parâmetros.
def safe_booking_url(value):
    # Linha 293: Verifica uma condição antes de executar o bloco indentado.
    if not isinstance(value, str):
        # Linha 294: Encerra a função e devolve o valor calculado.
        return None
    # Linha 295: Cria ou atualiza uma variável com o valor calculado à direita.
    value=value.strip()
    # Linha 296: Inicia um bloco para tratar possíveis erros sem interromper a aplicação.
    try:
        # Linha 297: Cria ou atualiza uma variável com o valor calculado à direita.
        parsed=urlparse(value)
    # Linha 298: Captura um tipo de erro ocorrido no bloco try.
    except ValueError:
        # Linha 299: Encerra a função e devolve o valor calculado.
        return None
    # Linha 300: Verifica uma condição antes de executar o bloco indentado.
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        # Linha 301: Encerra a função e devolve o valor calculado.
        return None
    # Linha 302: Encerra a função e devolve o valor calculado.
    return value

# Linha 304: Declara uma função reutilizável e define seus parâmetros.
def amadeus_activities(lat, lon, limit=30):
    # Linha 305: Cria ou atualiza uma variável com o valor calculado à direita.
    token=_amadeus_access_token()
    # Linha 306: Verifica uma condição antes de executar o bloco indentado.
    if not token:
        # Linha 307: Encerra a função e devolve o valor calculado.
        return [], "Atividades comerciais reais exigem as credenciais Amadeus no .env."
    # Linha 308: Cria ou atualiza uma variável com o valor calculado à direita.
    base=os.getenv("AMADEUS_BASE_URL","https://api.amadeus.com").rstrip("/")
    # Linha 309: Inicia um bloco para tratar possíveis erros sem interromper a aplicação.
    try:
        # Linha 310: Cria ou atualiza uma variável com o valor calculado à direita.
        r=requests.get(
            # Linha 311: Executa a instrução Python desta linha.
            f"{base}/v1/shopping/activities",
            # Linha 312: Cria ou atualiza uma variável com o valor calculado à direita.
            headers={"Authorization":f"Bearer {token}"},
            # Linha 313: Cria ou atualiza uma variável com o valor calculado à direita.
            params={"latitude":lat,"longitude":lon,"radius":10},
            # Linha 314: Cria ou atualiza uma variável com o valor calculado à direita.
            timeout=6,
        # Linha 315: Executa a instrução Python desta linha.
        )
        # Linha 316: Executa a instrução Python desta linha.
        r.raise_for_status()
        # Linha 317: Cria ou atualiza uma variável com o valor calculado à direita.
        out=[]
        # Linha 318: Percorre os itens de uma coleção ou sequência.
        for item in r.json().get("data",[])[:limit]:
            # Linha 319: Cria ou atualiza uma variável com o valor calculado à direita.
            geo=item.get("geoCode",{}) or {}
            # Linha 320: Cria ou atualiza uma variável com o valor calculado à direita.
            plat,plon=geo.get("latitude"),geo.get("longitude")
            # Linha 321: Cria ou atualiza uma variável com o valor calculado à direita.
            try: rating=float(item.get("rating")) if item.get("rating") is not None else None
            # Linha 322: Cria ou atualiza uma variável com o valor calculado à direita.
            except (ValueError,TypeError): rating=None
            # Linha 323: Cria ou atualiza uma variável com o valor calculado à direita.
            raw=(item.get("price") or {}).get("amount")
            # Linha 324: Cria ou atualiza uma variável com o valor calculado à direita.
            try: price=float(raw) if raw is not None else None
            # Linha 325: Cria ou atualiza uma variável com o valor calculado à direita.
            except (ValueError,TypeError): price=None
            # Linha 326: Executa a instrução Python desta linha.
            out.append({
                # Linha 327: Executa a instrução Python desta linha.
                "name":item.get("name") or "Atividade",
                # Linha 328: Executa a instrução Python desta linha.
                "rating":rating,
                # Linha 329: Executa a instrução Python desta linha.
                "lat":plat,"lon":plon,
                # Linha 330: Executa a instrução Python desta linha.
                "distance_km":round(haversine(lat,lon,float(plat),float(plon)),1) if plat is not None and plon is not None else None,
                # Linha 331: Executa a instrução Python desta linha.
                "type":"atividade turística",
                # Linha 332: Executa a instrução Python desta linha.
                "preco":price,
                # Linha 333: Executa a instrução Python desta linha.
                "currency":(item.get("price") or {}).get("currencyCode"),
                # Linha 334: Executa a instrução Python desta linha.
                "descricao":item.get("shortDescription"),
                # Linha 335: Executa a instrução Python desta linha.
                "booking_link":safe_booking_url(item.get("bookingLink")),
                # Linha 336: Executa a instrução Python desta linha.
                "real":True,
                # Linha 337: Executa a instrução Python desta linha.
                "source":"Amadeus Destination Experiences",
            # Linha 338: Executa a instrução Python desta linha.
            })
        # Linha 339: Encerra a função e devolve o valor calculado.
        return sorted(out,key=lambda x:(x["distance_km"] if x["distance_km"] is not None else 9999)), None
    # Linha 340: Captura um tipo de erro ocorrido no bloco try.
    except (requests.RequestException,ValueError,TypeError,KeyError):
        # Linha 341: Encerra a função e devolve o valor calculado.
        return [], "Não foi possível consultar atividades turísticas reais agora."

# Linha 343: Declara uma função reutilizável e define seus parâmetros.
def _clickbus_access_token():
    # Linha 344: Executa a instrução Python desta linha.
    global CLICKBUS_TOKEN, CLICKBUS_TOKEN_EXPIRES
    # Linha 345: Cria ou atualiza uma variável com o valor calculado à direita.
    username=os.getenv("CLICKBUS_USERNAME")
    # Linha 346: Cria ou atualiza uma variável com o valor calculado à direita.
    password=os.getenv("CLICKBUS_PASSWORD")
    # Linha 347: Verifica uma condição antes de executar o bloco indentado.
    if not username or not password:
        # Linha 348: Encerra a função e devolve o valor calculado.
        return None
    # Linha 349: Verifica uma condição antes de executar o bloco indentado.
    if CLICKBUS_TOKEN and time.time()<CLICKBUS_TOKEN_EXPIRES-60:
        # Linha 350: Encerra a função e devolve o valor calculado.
        return CLICKBUS_TOKEN
    # Linha 351: Cria ou atualiza uma variável com o valor calculado à direita.
    base=os.getenv("CLICKBUS_BASE_URL","https://platform-bff-partners.stg.clickbus.net/partners/api").rstrip("/")
    # Linha 352: Inicia um bloco para tratar possíveis erros sem interromper a aplicação.
    try:
        # Linha 353: Cria ou atualiza uma variável com o valor calculado à direita.
        r=requests.post(
            # Linha 354: Executa a instrução Python desta linha.
            f"{base}/oauth/basic-token",
            # Linha 355: Cria ou atualiza uma variável com o valor calculado à direita.
            json={"grant_type":"client_credentials"},
            # Linha 356: Cria ou atualiza uma variável com o valor calculado à direita.
            headers={"Content-Type":"application/json"},
            # Linha 357: Cria ou atualiza uma variável com o valor calculado à direita.
            auth=(username,password),
            # Linha 358: Cria ou atualiza uma variável com o valor calculado à direita.
            timeout=5,
        # Linha 359: Executa a instrução Python desta linha.
        )
        # Linha 360: Cria ou atualiza uma variável com o valor calculado à direita.
        r.raise_for_status(); data=r.json()
        # Linha 361: Cria ou atualiza uma variável com o valor calculado à direita.
        CLICKBUS_TOKEN=data.get("accessToken") or data.get("access_token")
        # Linha 362: Cria ou atualiza uma variável com o valor calculado à direita.
        CLICKBUS_TOKEN_EXPIRES=time.time()+int(data.get("expiresIn") or data.get("expires_in") or 3600)
        # Linha 363: Encerra a função e devolve o valor calculado.
        return CLICKBUS_TOKEN
    # Linha 364: Captura um tipo de erro ocorrido no bloco try.
    except (requests.RequestException,ValueError,TypeError,KeyError):
        # Linha 365: Encerra a função e devolve o valor calculado.
        return None


# Linha 368: Declara uma função reutilizável e define seus parâmetros.
def _clickbus_place(city,token):
    # Linha 369: Cria ou atualiza uma variável com o valor calculado à direita.
    base=os.getenv("CLICKBUS_BASE_URL","https://platform-bff-partners.stg.clickbus.net/partners/api").rstrip("/")
    # Linha 370: Inicia um bloco para tratar possíveis erros sem interromper a aplicação.
    try:
        # Linha 371: Executa a instrução Python desta linha.
        # ClickBus requires its own place slug for the trips search.
        # Linha 372: Cria ou atualiza uma variável com o valor calculado à direita.
        r=requests.get(
            # Linha 373: Executa a instrução Python desta linha.
            f"{base}/v4/places/by-location",
            # Linha 374: Cria ou atualiza uma variável com o valor calculado à direita.
            headers={"Authorization":f"Bearer {token}","Accept":"application/json"},
            # Linha 375: Cria ou atualiza uma variável com o valor calculado à direita.
            params={"cityName":city.split(",")[0].strip(),"limit":20,"fields":"id,name,slug,terminal,city,state,country,latitude,longitude"},
            # Linha 376: Cria ou atualiza uma variável com o valor calculado à direita.
            timeout=5,
        # Linha 377: Executa a instrução Python desta linha.
        )
        # Linha 378: Cria ou atualiza uma variável com o valor calculado à direita.
        r.raise_for_status(); data=r.json()
        # Linha 379: Cria ou atualiza uma variável com o valor calculado à direita.
        items=data.get("content") or data.get("data") or []
        # Linha 380: Verifica uma condição antes de executar o bloco indentado.
        if isinstance(items,dict): items=items.get("content") or []
        # Linha 381: Verifica uma condição antes de executar o bloco indentado.
        if not items: return None
        # Linha 382: Encerra a função e devolve o valor calculado.
        return items[0].get("slug")
    # Linha 383: Captura um tipo de erro ocorrido no bloco try.
    except (requests.RequestException,ValueError,TypeError,KeyError):
        # Linha 384: Encerra a função e devolve o valor calculado.
        return None


# Linha 387: Declara uma função reutilizável e define seus parâmetros.
def real_buses(origin,destination,travel_date):
    # Linha 388: Cria ou atualiza uma variável com o valor calculado à direita.
    token=_clickbus_access_token()
    # Linha 389: Verifica uma condição antes de executar o bloco indentado.
    if not token:
        # Linha 390: Encerra a função e devolve o valor calculado.
        return [],"Ônibus reais exigem credenciais de parceiro ClickBus (CLICKBUS_USERNAME e CLICKBUS_PASSWORD) no .env."
    # Linha 391: Cria ou atualiza uma variável com o valor calculado à direita.
    from_slug=_clickbus_place(origin,token); to_slug=_clickbus_place(destination,token)
    # Linha 392: Verifica uma condição antes de executar o bloco indentado.
    if not from_slug or not to_slug:
        # Linha 393: Encerra a função e devolve o valor calculado.
        return [],"Não foi possível localizar as cidades na API ClickBus."
    # Linha 394: Cria ou atualiza uma variável com o valor calculado à direita.
    base=os.getenv("CLICKBUS_BASE_URL","https://platform-bff-partners.stg.clickbus.net/partners/api").rstrip("/")
    # Linha 395: Inicia um bloco para tratar possíveis erros sem interromper a aplicação.
    try:
        # Linha 396: Cria ou atualiza uma variável com o valor calculado à direita.
        r=requests.get(
            # Linha 397: Executa a instrução Python desta linha.
            f"{base}/v5/trips",
            # Linha 398: Cria ou atualiza uma variável com o valor calculado à direita.
            headers={"Authorization":f"Bearer {token}","Accept":"application/json"},
            # Linha 399: Cria ou atualiza uma variável com o valor calculado à direita.
            params={"from":from_slug,"to":to_slug,"departureDate":travel_date.isoformat()},
            # Linha 400: Cria ou atualiza uma variável com o valor calculado à direita.
            timeout=8,
        # Linha 401: Executa a instrução Python desta linha.
        )
        # Linha 402: Cria ou atualiza uma variável com o valor calculado à direita.
        r.raise_for_status(); payload=r.json()
        # Linha 403: Cria ou atualiza uma variável com o valor calculado à direita.
        items=payload.get("content") or payload.get("data") or payload.get("trips") or []
        # Linha 404: Verifica uma condição antes de executar o bloco indentado.
        if isinstance(items,dict): items=items.get("content") or items.get("data") or items.get("trips") or []
        # Linha 405: Cria ou atualiza uma variável com o valor calculado à direita.
        out=[]
        # Linha 406: Percorre os itens de uma coleção ou sequência.
        for x in items[:50]:
            # Linha 407: Cria ou atualiza uma variável com o valor calculado à direita.
            company=x.get("travelCompany") or {}
            # Linha 408: Cria ou atualiza uma variável com o valor calculado à direita.
            dep=x.get("departure") or {}; arr=x.get("arrival") or {}
            # Linha 409: Cria ou atualiza uma variável com o valor calculado à direita.
            price=x.get("price")
            # Linha 410: Verifica uma condição antes de executar o bloco indentado.
            if isinstance(price,dict): price=price.get("default") or price.get("discounted") or price.get("value")
            # Linha 411: Cria ou atualiza uma variável com o valor calculado à direita.
            try: price=float(price)
            # Linha 412: Captura um tipo de erro ocorrido no bloco try.
            except (ValueError,TypeError): continue
            # Linha 413: Executa a instrução Python desta linha.
            out.append({
                # Linha 414: Executa a instrução Python desta linha.
                "companhia":company.get("name") or x.get("travelCompanyName") or "Viação",
                # Linha 415: Executa a instrução Python desta linha.
                "classe":(x.get("serviceClass") or {}).get("name") if isinstance(x.get("serviceClass"),dict) else x.get("serviceClass") or x.get("busName") or "",
                # Linha 416: Executa a instrução Python desta linha.
                "saida":(dep.get("schedule") or dep).get("departureTime") or (dep.get("schedule") or dep).get("time") or dep.get("at") or "",
                # Linha 417: Executa a instrução Python desta linha.
                "chegada":(arr.get("schedule") or arr).get("arrivalTime") or (arr.get("schedule") or arr).get("time") or arr.get("at") or "",
                # Linha 418: Executa a instrução Python desta linha.
                "duracao":x.get("duration") if isinstance(x.get("duration"),str) else str(x.get("duration") or ""),
                # Linha 419: Executa a instrução Python desta linha.
                "preco":price,"currency":x.get("currency") or "BRL","available_seats":x.get("availableSeats"),"real":True,"source":"ClickBus"
            # Linha 420: Executa a instrução Python desta linha.
            })
        # Linha 421: Cria ou atualiza uma variável com o valor calculado à direita.
        out.sort(key=lambda x:x["preco"]); return (out,None) if out else ([],"Nenhuma viagem de ônibus real foi encontrada para essa rota e data.")
    # Linha 422: Captura um tipo de erro ocorrido no bloco try.
    except requests.HTTPError as exc:
        # Linha 423: Verifica uma condição antes de executar o bloco indentado.
        if exc.response is not None and exc.response.status_code==401: return [],"As credenciais ClickBus foram recusadas ou expiraram."
        # Linha 424: Encerra a função e devolve o valor calculado.
        return [],"A fonte de ônibus não respondeu com uma oferta válida."
    # Linha 425: Captura um tipo de erro ocorrido no bloco try.
    except (requests.RequestException,ValueError,TypeError,KeyError):
        # Linha 426: Encerra a função e devolve o valor calculado.
        return [],"Não foi possível consultar viagens de ônibus reais agora."

# Linha 428: Declara uma função reutilizável e define seus parâmetros.
def search_trip(origin,destination,travel_date, nights=1):
    # Linha 429: Cria ou atualiza uma variável com o valor calculado à direita.
    with ThreadPoolExecutor(max_workers=2) as pool:
        # Linha 430: Cria ou atualiza uma variável com o valor calculado à direita.
        flight_future=pool.submit(real_flights,origin,destination,travel_date)
        # Linha 431: Cria ou atualiza uma variável com o valor calculado à direita.
        geo_future=pool.submit(geocode,destination)
        # Linha 432: Cria ou atualiza uma variável com o valor calculado à direita.
        flights,flight_message=flight_future.result()
        # Linha 433: Cria ou atualiza uma variável com o valor calculado à direita.
        dest_geo=geo_future.result()
    # Linha 434: Verifica uma condição antes de executar o bloco indentado.
    if not dest_geo: raise ValueError("Não foi possível localizar o destino informado.")

    # Linha 436: Executa a instrução Python desta linha.
    # After geocoding, query independent destination sources concurrently.
    # Linha 437: Cria ou atualiza uma variável com o valor calculado à direita.
    with ThreadPoolExecutor(max_workers=3) as pool:
        # Linha 438: Cria ou atualiza uma variável com o valor calculado à direita.
        hotel_future=pool.submit(amadeus_hotels,dest_geo["lat"],dest_geo["lon"],travel_date,nights,12)
        # Linha 439: Cria ou atualiza uma variável com o valor calculado à direita.
        activity_future=pool.submit(amadeus_activities,dest_geo["lat"],dest_geo["lon"],30)
        # Linha 440: Cria ou atualiza uma variável com o valor calculado à direita.
        osm_future=pool.submit(overpass,dest_geo["lat"],dest_geo["lon"])
        # Linha 441: Cria ou atualiza uma variável com o valor calculado à direita.
        hotels,hotel_message=hotel_future.result()
        # Linha 442: Cria ou atualiza uma variável com o valor calculado à direita.
        activities,activity_message=activity_future.result()
        # Linha 443: Cria ou atualiza uma variável com o valor calculado à direita.
        elements=osm_future.result()

    # Linha 445: Executa a instrução Python desta linha.
    # If Amadeus is not configured or has no result, keep OSM as a real fallback.
    # Linha 446: Cria ou atualiza uma variável com o valor calculado à direita.
    osm_hotels=[]; osm_attractions=[]
    # Linha 447: Cria ou atualiza uma variável com o valor calculado à direita.
    attraction_types={"attraction","museum","gallery","theme_park","zoo","viewpoint","aquarium"}; historic_types={"monument","memorial","castle","ruins","archaeological_site"}
    # Linha 448: Percorre os itens de uma coleção ou sequência.
    for e in elements:
        # Linha 449: Cria ou atualiza uma variável com o valor calculado à direita.
        tags=e.get("tags",{})
        # Linha 450: Verifica uma condição antes de executar o bloco indentado.
        if tags.get("tourism") in {"hotel","hostel","guest_house"}: osm_hotels.append(e)
        # Linha 451: Verifica uma condição alternativa caso a condição anterior não tenha sido atendida.
        elif tags.get("tourism") in attraction_types or tags.get("historic") in historic_types or tags.get("leisure")=="park": osm_attractions.append(e)

    # Linha 453: Verifica uma condição antes de executar o bloco indentado.
    if not hotels:
        # Linha 454: Cria ou atualiza uma variável com o valor calculado à direita.
        hotels=normalize_places(osm_hotels,dest_geo["lat"],dest_geo["lon"],40)
        # Linha 455: Verifica uma condição antes de executar o bloco indentado.
        if hotels and not hotel_message:
            # Linha 456: Cria ou atualiza uma variável com o valor calculado à direita.
            hotel_message="Hotéis localizados no OpenStreetMap; preços individuais não estão disponíveis nessa fonte."
    # Linha 457: Verifica uma condição antes de executar o bloco indentado.
    if not activities:
        # Linha 458: Cria ou atualiza uma variável com o valor calculado à direita.
        activities=normalize_places(osm_attractions,dest_geo["lat"],dest_geo["lon"],50)
        # Linha 459: Verifica uma condição antes de executar o bloco indentado.
        if activities and not activity_message:
            # Linha 460: Cria ou atualiza uma variável com o valor calculado à direita.
            activity_message="Pontos turísticos localizados no OpenStreetMap."

    # Linha 462: Cria ou atualiza uma variável com o valor calculado à direita.
    buses,bus_message=real_buses(origin,destination,travel_date)
    # Linha 463: Encerra a função e devolve o valor calculado.
    return {
        # Linha 464: Executa a instrução Python desta linha.
        "origin":{"query":origin},"destination":dest_geo,
        # Linha 465: Executa a instrução Python desta linha.
        "hotel_reference_daily_average":PUBLIC_HOTEL_DAILY_AVERAGE,
        # Linha 466: Executa a instrução Python desta linha.
        "hotels":hotels,"hotel_message":hotel_message,
        # Linha 467: Executa a instrução Python desta linha.
        "attractions":activities,"activity_message":activity_message,
        # Linha 468: Executa a instrução Python desta linha.
        "flights":flights,"flight_message":flight_message,
        # Linha 469: Executa a instrução Python desta linha.
        "buses":buses,"bus_message":bus_message,
        # Linha 470: Executa a instrução Python desta linha.
        "data_sources":{
            # Linha 471: Executa a instrução Python desta linha.
            "osm":bool(elements),
            # Linha 472: Executa a instrução Python desta linha.
            "amadeus_hotels":any(x.get("source")=="Amadeus Hotel Search" for x in hotels),
            # Linha 473: Executa a instrução Python desta linha.
            "amadeus_activities":any(x.get("source")=="Amadeus Destination Experiences" for x in activities),
            # Linha 474: Executa a instrução Python desta linha.
            "flights":bool(flights),"buses":bool(buses)
        # Linha 475: Executa a instrução Python desta linha.
        }
    # Linha 476: Executa a instrução Python desta linha.
    }
