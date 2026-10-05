import re
import os
import unicodedata
from datetime import datetime, date, timedelta
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from sqlalchemy import desc, or_
from itsdangerous import URLSafeSerializer, BadSignature
from sqlalchemy.exc import IntegrityError
from config import Config
from extensions import db, csrf, limiter
from models import User, Trip, FavoritePlace, PriceAlert, BudgetItem, BudgetOrder, Roteiro, RoteiroItem, ViagemGrupo, GrupoMembro, GrupoItem, RoteiroMembro
from services.travel import search_trip, geocode
from services.destinations import DESTINATIONS

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
csrf.init_app(app)
limiter.init_app(app)
share_serializer = URLSafeSerializer(app.config["SECRET_KEY"], salt="travel-monitor-roteiro")

with app.app_context():
    db.create_all()

CITIES = [
    ("Vitória", "ES"), ("Vila Velha", "ES"), ("Serra", "ES"), ("Cariacica", "ES"), ("Guarapari", "ES"),
    ("São Paulo", "SP"), ("Campinas", "SP"), ("Santos", "SP"), ("São José dos Campos", "SP"), ("Ribeirão Preto", "SP"),
    ("Rio de Janeiro", "RJ"), ("Niterói", "RJ"), ("Petrópolis", "RJ"), ("Cabo Frio", "RJ"), ("Angra dos Reis", "RJ"),
    ("Belo Horizonte", "MG"), ("Uberlândia", "MG"), ("Juiz de Fora", "MG"), ("Ouro Preto", "MG"), ("Poços de Caldas", "MG"),
    ("Brasília", "DF"), ("Goiânia", "GO"), ("Anápolis", "GO"), ("Cuiabá", "MT"), ("Campo Grande", "MS"),
    ("Curitiba", "PR"), ("Londrina", "PR"), ("Maringá", "PR"), ("Foz do Iguaçu", "PR"), ("Ponta Grossa", "PR"),
    ("Porto Alegre", "RS"), ("Caxias do Sul", "RS"), ("Gramado", "RS"), ("Canela", "RS"), ("Florianópolis", "SC"),
    ("Joinville", "SC"), ("Blumenau", "SC"), ("Balneário Camboriú", "SC"), ("Recife", "PE"), ("Olinda", "PE"),
    ("Porto de Galinhas", "PE"), ("Salvador", "BA"), ("Porto Seguro", "BA"), ("Feira de Santana", "BA"),
    ("Fortaleza", "CE"), ("Juazeiro do Norte", "CE"), ("Natal", "RN"), ("João Pessoa", "PB"), ("Maceió", "AL"),
    ("Aracaju", "SE"), ("São Luís", "MA"), ("Teresina", "PI"), ("Belém", "PA"), ("Santarém", "PA"),
    ("Manaus", "AM"), ("Porto Velho", "RO"), ("Rio Branco", "AC"), ("Macapá", "AP"), ("Boa Vista", "RR"),
    ("Palmas", "TO"), ("Bonito", "MS"), ("Lençóis", "BA"), ("Chapada Diamantina", "BA"), ("Maragogi", "AL"),
    ("Jericoacoara", "CE"), ("Campos do Jordão", "SP"), ("Búzios", "RJ"), ("Paraty", "RJ"), ("Ilhabela", "SP"),
    ("Ubatuba", "SP"), ("Bento Gonçalves", "RS"), ("Caldas Novas", "GO"), ("Aparecida", "SP"), ("Montes Claros", "MG"),
    ("Governador Valadares", "MG"), ("Linhares", "ES"), ("Colatina", "ES"), ("Aracruz", "ES"), ("Domingos Martins", "ES"),
    ("Venda Nova do Imigrante", "ES"), ("São Mateus", "ES"), ("Cachoeiro de Itapemirim", "ES"), ("Teixeira de Freitas", "BA"),
    ("Ilhéus", "BA"), ("Itacaré", "BA"), ("Camaçari", "BA"), ("Vitória da Conquista", "BA"), ("Caruaru", "PE"),
    ("Petrolina", "PE"), ("Campina Grande", "PB"), ("Sobral", "CE"), ("Mossoró", "RN"), ("Parnaíba", "PI"),
    ("Barreiras", "BA"), ("Cascavel", "PR"), ("Chapecó", "SC"), ("Pelotas", "RS"), ("Santa Maria", "RS"),
]

EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
PHONE_RE = re.compile(r"^[0-9+() .-]{8,25}$")


def normalize_text(value):
    return "".join(c for c in unicodedata.normalize("NFD", value.lower()) if unicodedata.category(c) != "Mn")


def normalize_phone(value):
    return re.sub(r"\D", "", str(value or ""))


def current_user():
    return db.session.get(User, session.get("user_id"))


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user_id=session.get("user_id")
        if not user_id: return redirect(url_for("login"))
        if not db.session.get(User,user_id):
            session.clear(); return redirect(url_for("login"))
        return fn(*args, **kwargs)
    return wrapper


@app.after_request
def security_headers(response):
    response.headers["X-Content-Type-Options"]="nosniff"
    response.headers["X-Frame-Options"]="DENY"
    response.headers["Referrer-Policy"]="strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"]="geolocation=(), microphone=(), camera=()"
    response.headers["Content-Security-Policy"]=("default-src 'self'; style-src 'self' https://unpkg.com; script-src 'self' https://unpkg.com; img-src 'self' data: https://*.tile.openstreetmap.org; connect-src 'self' https://api.open-meteo.com https://geocoding-api.open-meteo.com; font-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'")
    if request.path in {"/","/cadastro","/login","/dashboard","/roteiro","/orcamento","/clima","/perfil","/destinos","/grupo","/roteiro-compartilhado"}: response.headers["Cache-Control"]="no-store"
    return response


@app.get("/")
def login():
    if session.get("user_id"):
        return redirect(url_for("dashboard"))
    return render_template("login.html")


@app.route("/cadastro", methods=["GET", "POST"])
@limiter.limit("5 per minute", methods=["POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip().lower()
        telefone = request.form.get("telefone", "").strip()
        telefone_login = normalize_phone(telefone)
        senha = request.form.get("senha", "")
        confirmar = request.form.get("confirmar_senha", "")
        if not nome or len(nome) > 120 or not EMAIL_RE.match(email) or not PHONE_RE.match(telefone) or not (8 <= len(telefone_login) <= 15):
            flash("Confira nome, e-mail e telefone.", "error")
        elif len(senha) < 15 or len(senha) > 128:
            flash("Use uma senha de 15 a 128 caracteres.", "error")
        elif senha != confirmar:
            flash("As senhas não conferem.", "error")
        elif User.query.filter_by(email=email).first():
            flash("Este e-mail já está cadastrado.", "error")
        elif any(normalize_phone(u.telefone) == telefone_login for u in User.query.with_entities(User.telefone).all()):
            flash("Este telefone já está cadastrado.", "error")
        else:
            try:
                u = User(nome=nome, email=email, telefone=telefone_login)
                u.set_password(senha)
                db.session.add(u)
                db.session.commit()
                flash("Conta criada com segurança. Faça login.", "success")
                return redirect(url_for("login"))
            except IntegrityError:
                db.session.rollback()
                flash("Não foi possível criar a conta.", "error")
    return render_template("cadastro.html")


@app.post("/login")
@limiter.limit("5 per minute")
def autenticar():
    identificador = (request.form.get("identificador") or request.form.get("email") or "").strip()
    senha = request.form.get("senha", "")

    if len(identificador) > 180 or len(senha) > 128:
        flash("E-mail/telefone ou senha inválidos.", "error")
        return redirect(url_for("login"))

    if EMAIL_RE.match(identificador.lower()):
        user = User.query.filter_by(email=identificador.lower()).first()
    else:
        telefone = normalize_phone(identificador)
        user = User.query.filter(or_(User.telefone == identificador, User.telefone == telefone)).first()
        if not user:
            # Compatibilidade com contas antigas que guardavam máscara no telefone.
            user = next((u for u in User.query.all() if normalize_phone(u.telefone) == telefone), None)

    if not user or not user.check_password(senha):
        flash("E-mail/telefone ou senha inválidos.", "error")
        return redirect(url_for("login"))

    session.clear()
    session.permanent = True
    session["user_id"] = user.id
    return redirect(url_for("dashboard"))


@app.post("/logout")
@login_required
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.get("/dashboard")
@login_required
def dashboard():
    user=db.session.get(User,session["user_id"])
    trips=Trip.query.filter_by(usuario_id=user.id).order_by(desc(Trip.criada_em)).limit(20).all()
    return render_template("dashboard.html",nome=user.nome,viagens=trips)


@app.get("/roteiro")
@login_required
def roteiro_page():
    return render_template("roteiro.html", nome=current_user().nome)

@app.get("/destinos")
@login_required
def destinos_page():
    user = db.session.get(User, user_id())
    favorite_destinations = {
        x.nome
        for x in FavoritePlace.query.filter_by(usuario_id=user.id, lista="favorito", tipo="destino").all()
    }
    return render_template("destinos.html", nome=user.nome, destinos=DESTINATIONS, favorite_destinations=favorite_destinations)

@app.get("/grupo")
@login_required
def grupo_page():
    return render_template("grupo.html", nome=current_user().nome)

@app.get("/roteiro-compartilhado")
@login_required
def roteiro_compartilhado_page():
    return render_template("compartilhado.html", nome=current_user().nome)

@app.get("/orcamento")
@login_required
def orcamento_page():
    return render_template("orcamento.html", nome=current_user().nome)

@app.get("/clima")
@login_required
def clima_page():
    return render_template("clima.html", nome=current_user().nome)

@app.get("/api/cidades")
@limiter.limit("60 per minute")
def cidades():
    q = normalize_text(request.args.get("q", "").strip())
    if len(q) < 1:
        return jsonify([])
    matches = []
    for city, state in CITIES:
        normalized = normalize_text(city)
        score = 0 if normalized.startswith(q) else (1 if q in normalized else 2)
        if score < 2:
            matches.append({"nome": city, "uf": state, "label": f"{city}, {state}", "score": score})
    matches.sort(key=lambda x: (x["score"], normalize_text(x["nome"])))
    return jsonify(matches[:8])


@app.post("/api/viagens/pesquisar")
@login_required
@limiter.limit("10 per minute")
def pesquisar():
    data = request.get_json(silent=True) or {}
    origem = (data.get("origem") or "").strip()[:180]
    destino = (data.get("destino") or "").strip()[:180]
    data_ida = data.get("data_ida") or ""
    if not origem or not destino or not data_ida:
        return jsonify(error="Informe origem, destino e data."), 400
    try:
        d = datetime.strptime(data_ida, "%Y-%m-%d").date()
    except ValueError:
        return jsonify(error="Data inválida."), 400
    if d < datetime.now().date():
        return jsonify(error="A data da viagem não pode estar no passado."), 400
    try:
        noites = max(1, min(int(data.get("noites") or 1), 30))
        result = demo_search_result(origem,destino,d,noites) if bool(data.get("demo")) else search_trip(origem, destino, d, noites)
    except ValueError as exc:
        return jsonify(error=str(exc)), 400
    except Exception:
        app.logger.exception("Falha na pesquisa")
        return jsonify(error="Não foi possível concluir a pesquisa agora. Tente novamente."), 502
    try:
        trip=Trip(usuario_id=session["user_id"],origem=origem,destino=destino,data_ida=d)
        db.session.add(trip); db.session.commit(); result["trip_id"]=trip.id
    except Exception:
        db.session.rollback(); app.logger.exception("Falha ao salvar histórico da viagem"); result["trip_id"]=None
    result["origem"] = origem
    result["data_ida"] = data_ida
    result["data_sources"] = result.get("data_sources") or {"osm": False, "amadeus_hotels": False, "amadeus_activities": False, "flights": bool(result.get("flights")), "buses": bool(result.get("buses"))}
    return jsonify(result)



def user_id():
    return int(session["user_id"])


def serialize_cart(uid):
    items=BudgetItem.query.filter_by(usuario_id=uid).order_by(BudgetItem.id.desc()).all()
    return [{"id":x.id,"categoria":x.categoria,"nome":x.nome,"quantidade":x.quantidade,"preco_unitario":x.preco_unitario,"total":x.total,"origem":x.origem} for x in items]


def demo_search_result(origem,destino,data_ida,noites):
    # Dados fictícios exclusivos do modo Demonstração. Nunca são apresentados como ofertas reais.
    base=normalize_text(destino.split(",")[0])
    names={
        "rio de janeiro":[("Hotel Atlântico Demo",4.7,389.90),("Pousada Carioca Demo",4.4,279.90),("Hotel Praia Demo",4.1,329.90)],
        "salvador":[("Hotel Pelô Demo",4.6,299.90),("Pousada Bahia Demo",4.3,239.90),("Hotel Farol Demo",4.5,359.90)],
        "vitoria":[("Hotel Camburi Demo",4.6,289.90),("Pousada Capixaba Demo",4.2,219.90),("Hotel Centro Demo",4.0,249.90)],
    }
    hotels=names.get(base,[(f"Hotel Central {destino.split(',')[0]}",4.4,299.90),("Hotel Vista Demo",4.2,249.90),("Pousada Conforto Demo",4.6,219.90)])
    attractions={
        "rio de janeiro":["Cristo Redentor","Pão de Açúcar","Copacabana","Jardim Botânico"],
        "salvador":["Pelourinho","Farol da Barra","Elevador Lacerda","Igreja do Bonfim"],
        "vitoria":["Convento da Penha","Praia de Camburi","Centro Histórico","Ilha das Caieiras"],
    }.get(base,["Centro histórico","Mirante principal","Museu local","Parque da cidade"])
    buses=[("Viação Demo Express","07:30","13:10",189.90),("Viação Demo Sul","10:20","16:40",219.90),("Viação Demo Conforto","21:00","05:20",249.90)]
    flights=[
        {"companhia":"Demo Airlines","saida":"06:20","chegada":"07:55","escalas":0,"origem_aeroporto":origem,"destino_aeroporto":destino,"preco":649.90,"real":False,"source":"Demonstração"},
        {"companhia":"Demo Air","saida":"09:10","chegada":"12:45","escalas":1,"origem_aeroporto":origem,"destino_aeroporto":destino,"preco":529.90,"real":False,"source":"Demonstração"},
        {"companhia":"Demo Brasil","saida":"14:30","chegada":"16:20","escalas":0,"origem_aeroporto":origem,"destino_aeroporto":destino,"preco":729.90,"real":False,"source":"Demonstração"},
    ]
    hotel_rows=[{"name":n,"rating":r,"preco":p,"distance_km":round(i*1.4+0.7,1),"type":"Hotel (simulado)","lat":None,"lon":None,"real":False,"source":"Demonstração"} for i,(n,r,p) in enumerate(hotels)]
    place_rows=[{"name":n,"rating":4.5,"preco":0,"distance_km":round(i*1.1+0.5,1),"type":"Ponto turístico (simulado)","lat":None,"lon":None,"real":False,"source":"Demonstração"} for i,n in enumerate(attractions)]
    bus_rows=[{"companhia":c,"saida":s,"chegada":a,"preco":p,"real":False,"source":"Demonstração"} for c,s,a,p in buses]
    return {"origin":{"query":origem},"destination":{"query":destino},"hotel_reference_daily_average":451.71,"hotels":hotel_rows,"hotel_message":"Hotéis fictícios para testar a interface.","attractions":place_rows,"activity_message":"Pontos turísticos fictícios para testar a interface.","flights":flights,"flight_message":"Voos fictícios: use apenas para testar a interface.","buses":bus_rows,"bus_message":"Ônibus fictícios para testar a interface.","data_sources":{"demo":True,"osm":False,"amadeus_hotels":False,"amadeus_activities":False,"flights":True,"buses":True}}


def demo_packages():
    # Intentionally illustrative: these offers belong only to the budget simulator,
    # never to the real flight-search results.
    return [
        {"destino":"Vitória, ES","dias":4,"voo":899.90,"hotel":1250.00,"passeios":280.00,"transporte":180.00,"alimentacao":520.00,"total":3129.90,"destaque":"Praia + centro histórico"},
        {"destino":"Rio de Janeiro, RJ","dias":5,"voo":1099.90,"hotel":1650.00,"passeios":420.00,"transporte":240.00,"alimentacao":650.00,"total":4059.90,"destaque":"Praias + Cristo + Pão de Açúcar"},
        {"destino":"Salvador, BA","dias":5,"voo":949.90,"hotel":1400.00,"passeios":360.00,"transporte":220.00,"alimentacao":600.00,"total":3529.90,"destaque":"Pelourinho + praias"},
        {"destino":"Florianópolis, SC","dias":5,"voo":999.90,"hotel":1450.00,"passeios":330.00,"transporte":260.00,"alimentacao":620.00,"total":3659.90,"destaque":"Praias + trilhas"},
        {"destino":"Foz do Iguaçu, PR","dias":4,"voo":879.90,"hotel":1050.00,"passeios":390.00,"transporte":190.00,"alimentacao":480.00,"total":2989.90,"destaque":"Cataratas + Parque das Aves"},
        {"destino":"Recife + Olinda, PE","dias":5,"voo":919.90,"hotel":1320.00,"passeios":340.00,"transporte":210.00,"alimentacao":590.00,"total":3379.90,"destaque":"Praias + cultura"},
        {"destino":"Belo Horizonte, MG","dias":4,"voo":699.90,"hotel":980.00,"passeios":220.00,"transporte":170.00,"alimentacao":450.00,"total":2519.90,"destaque":"Gastronomia + Inhotim"},
        {"destino":"Curitiba, PR","dias":4,"voo":749.90,"hotel":900.00,"passeios":180.00,"transporte":140.00,"alimentacao":430.00,"total":2399.90,"destaque":"Parques + centro"},
    ]


@app.get("/perfil")
@login_required
def perfil():
    user=db.session.get(User,user_id())
    trips=Trip.query.filter_by(usuario_id=user.id).order_by(desc(Trip.data_ida)).limit(50).all()
    favorites=FavoritePlace.query.filter_by(usuario_id=user.id,lista="favorito").order_by(desc(FavoritePlace.criado_em)).all()
    wishlist=FavoritePlace.query.filter_by(usuario_id=user.id,lista="visitar").order_by(desc(FavoritePlace.criado_em)).all()
    alerts=PriceAlert.query.filter_by(usuario_id=user.id).order_by(desc(PriceAlert.criado_em)).all()
    orders=BudgetOrder.query.filter_by(usuario_id=user.id).order_by(desc(BudgetOrder.criado_em)).limit(30).all()
    return render_template("perfil.html",user=user,trips=trips,favorites=favorites,wishlist=wishlist,alerts=alerts,orders=orders,today=date.today())


@app.get("/api/carrinho")
@login_required
def cart_get():
    items=serialize_cart(user_id()); return jsonify(items=items,total=round(sum(x["total"] for x in items),2))


@app.post("/api/carrinho")
@login_required
def cart_add():
    data=request.get_json(silent=True) or {}
    try:
        qty=max(1,min(int(data.get("quantidade") or 1),20)); unit=float(data.get("preco_unitario"));
    except (ValueError,TypeError): return jsonify(error="Item inválido."),400
    nome=str(data.get("nome") or "").strip()[:220]; categoria=str(data.get("categoria") or "outro").strip()[:40]
    if not nome or unit<0 or unit>10000000: return jsonify(error="Item inválido."),400
    item=BudgetItem(usuario_id=user_id(),categoria=categoria,nome=nome,quantidade=qty,preco_unitario=unit,total=round(unit*qty,2),origem="simulado")
    db.session.add(item); db.session.commit(); return jsonify(item={"id":item.id,"categoria":item.categoria,"nome":item.nome,"quantidade":item.quantidade,"preco_unitario":item.preco_unitario,"total":item.total},total=sum(x.total for x in BudgetItem.query.filter_by(usuario_id=user_id()).all()))


@app.delete("/api/carrinho/<int:item_id>")
@login_required
def cart_delete(item_id):
    item=BudgetItem.query.filter_by(id=item_id,usuario_id=user_id()).first()
    if not item: return jsonify(error="Item não encontrado."),404
    db.session.delete(item); db.session.commit(); return cart_get()


@app.post("/api/carrinho/finalizar")
@login_required
def cart_checkout():
    items=BudgetItem.query.filter_by(usuario_id=user_id()).all()
    if not items: return jsonify(error="O carrinho está vazio."),400
    total=round(sum(x.total for x in items),2)
    order=BudgetOrder(usuario_id=user_id(),total=total,status="planejamento")
    db.session.add(order); db.session.commit()
    return jsonify(id=order.id,total=total,status=order.status)


@app.get("/api/favoritos")
@login_required
def favorite_list():
    items=FavoritePlace.query.filter_by(usuario_id=user_id()).order_by(desc(FavoritePlace.criado_em)).all()
    return jsonify(items=[{"id":x.id,"nome":x.nome,"cidade":x.cidade,"tipo":x.tipo,"lista":x.lista,"latitude":x.latitude,"longitude":x.longitude} for x in items])

@app.post("/api/favoritos")
@login_required
def favorite_add():
    data=request.get_json(silent=True) or {}
    nome=str(data.get("nome") or "").strip()[:180]; cidade=str(data.get("cidade") or "").strip()[:180]; lista=str(data.get("lista") or "favorito")
    if lista not in {"favorito","visitar"} or not nome: return jsonify(error="Lugar inválido."),400
    item=FavoritePlace(usuario_id=user_id(),nome=nome,cidade=cidade,tipo=str(data.get("tipo") or "lugar")[:60],latitude=data.get("latitude"),longitude=data.get("longitude"),lista=lista)
    db.session.add(item); db.session.commit(); return jsonify(id=item.id)


@app.post("/api/favoritos/destino")
@login_required
def favorite_destination_toggle():
    data = request.get_json(silent=True) or {}
    cidade = str(data.get("cidade") or "").strip()[:180]
    pais = str(data.get("pais") or "").strip()[:180]
    uf = str(data.get("uf") or "").strip()[:10]
    if not cidade:
        return jsonify(error="Destino inválido."), 400

    item = FavoritePlace.query.filter_by(
        usuario_id=user_id(), nome=cidade, lista="favorito", tipo="destino"
    ).first()

    if item:
        db.session.delete(item)
        db.session.commit()
        return jsonify(favorited=False)

    cidade_exibicao = f"{cidade}, {uf}" if uf else cidade
    item = FavoritePlace(usuario_id=user_id(), nome=cidade, cidade=cidade_exibicao,
                         tipo="destino", lista="favorito")
    db.session.add(item)
    db.session.commit()
    return jsonify(id=item.id, favorited=True)


@app.delete("/api/favoritos/<int:item_id>")
@login_required
def favorite_delete(item_id):
    item=FavoritePlace.query.filter_by(id=item_id,usuario_id=user_id()).first()
    if not item: return jsonify(error="Lugar não encontrado."),404
    db.session.delete(item); db.session.commit(); return jsonify(ok=True)


@app.post("/api/alertas")
@login_required
def alert_add():
    data=request.get_json(silent=True) or {}; destino=str(data.get("destino") or "").strip()[:180]
    try: alvo=float(data.get("preco_alvo"))
    except (ValueError,TypeError): return jsonify(error="Preço alvo inválido."),400
    if not destino or alvo<=0 or alvo>10000000: return jsonify(error="Alerta inválido."),400
    item=PriceAlert(usuario_id=user_id(),destino=destino,preco_alvo=alvo); db.session.add(item); db.session.commit(); return jsonify(id=item.id)


@app.delete("/api/alertas/<int:item_id>")
@login_required
def alert_delete(item_id):
    item=PriceAlert.query.filter_by(id=item_id,usuario_id=user_id()).first()
    if not item: return jsonify(error="Alerta não encontrado."),404
    db.session.delete(item); db.session.commit(); return jsonify(ok=True)


@app.get("/api/alertas/verificar")
@login_required
def alert_check():
    packages=demo_packages(); alerts=PriceAlert.query.filter_by(usuario_id=user_id(),ativo=True).all(); hits=[]
    for a in alerts:
        for p in packages:
            if normalize_text(a.destino.split(",")[0]) in normalize_text(p["destino"]) and p["total"]<=a.preco_alvo:
                hits.append({"destino":p["destino"],"preco":p["total"],"alvo":a.preco_alvo,"destaque":p["destaque"]})
    return jsonify(hits=hits)


@app.get("/api/destinos")
@login_required
def destinos_api():
    q=normalize_text(request.args.get("q","").strip())
    regiao=request.args.get("regiao","").strip().lower()
    rows=DESTINATIONS
    if q:
        rows=[x for x in rows if q in normalize_text(x["cidade"]) or q in normalize_text(x["pais"]) or any(q in normalize_text(p) for p in x["pontos"])]
    if regiao:
        rows=[x for x in rows if x["regiao"].lower()==regiao]
    return jsonify(destinos=rows)


@app.get("/api/destinos/<path:cidade>")
@login_required
def destino_detail(cidade):
    key=normalize_text(cidade)
    item=next((x for x in DESTINATIONS if normalize_text(x["cidade"])==key),None)
    if not item: return jsonify(error="Destino não encontrado."),404
    return jsonify(destino=item)


@app.get("/api/orcamento/destinos")
@login_required
def budget_destinations():
    try: budget=max(0,float(request.args.get("orcamento",0))); nights=max(1,min(int(request.args.get("noites",4)),15)); people=max(1,min(int(request.args.get("pessoas",1)),10))
    except (ValueError,TypeError): return jsonify(error="Parâmetros inválidos."),400
    packages=[]
    for p in demo_packages():
        scaled=dict(p); factor=(nights/p["dias"])*people; scaled["dias"]=nights; scaled["pessoas"]=people
        scaled["voo"]=round(p["voo"]*people,2)
        for k in ("hotel","passeios","transporte","alimentacao"): scaled[k]=round(p[k]*factor,2)
        scaled["total"]=round(sum(scaled[k] for k in ("voo","hotel","passeios","transporte","alimentacao")),2)
        if scaled["total"]<=budget or budget<=0: packages.append(scaled)
    packages.sort(key=lambda x:x["total"])
    return jsonify(packages=packages,simulado=True)


@app.get("/api/roteiros")
@login_required
def roteiro_list():
    owned=Roteiro.query.filter_by(usuario_id=user_id()).all()
    joined=Roteiro.query.join(RoteiroMembro).filter(RoteiroMembro.usuario_id==user_id()).all()
    rows={x.id:x for x in owned+joined}
    return jsonify(roteiros=[{"id":x.id,"destino":x.destino,"data_inicio":x.data_inicio.isoformat(),"dias":x.dias,"papel":"owner" if x.usuario_id==user_id() else "membro"} for x in sorted(rows.values(),key=lambda z:z.criado_em,reverse=True)])

@app.post("/api/roteiros")
@login_required
def roteiro_create():
    data=request.get_json(silent=True) or {}
    destino=str(data.get("destino") or "").strip()[:180]
    try: inicio=datetime.strptime(str(data.get("data_inicio")),"%Y-%m-%d").date(); dias=int(data.get("dias"))
    except (ValueError,TypeError): return jsonify(error="Informe destino, data de início e quantidade de dias válidos."),400
    if not destino or dias<1 or dias>60: return jsonify(error="A viagem deve ter entre 1 e 60 dias."),400
    if inicio < date.today(): return jsonify(error="A data de início não pode estar no passado."),400
    r=Roteiro(usuario_id=user_id(),destino=destino,data_inicio=inicio,dias=dias)
    db.session.add(r); db.session.commit(); return jsonify(id=r.id)

def roteiro_access(roteiro_id):
    r=db.session.get(Roteiro,roteiro_id)
    if not r: return None, None
    member=RoteiroMembro.query.filter_by(roteiro_id=roteiro_id,usuario_id=user_id()).first()
    if r.usuario_id==user_id(): return r, "owner"
    return (r, "member") if member else (None,None)

@app.get("/api/roteiros/<int:roteiro_id>")
@login_required
def roteiro_detail(roteiro_id):
    r,role=roteiro_access(roteiro_id)
    if not r: return jsonify(error="Roteiro não encontrado ou sem acesso."),404
    itens=RoteiroItem.query.filter_by(roteiro_id=r.id).order_by(RoteiroItem.dia,RoteiroItem.horario_inicio).all()
    return jsonify(roteiro={"id":r.id,"destino":r.destino,"data_inicio":r.data_inicio.isoformat(),"dias":r.dias,"papel":role},itens=[{"id":x.id,"dia":x.dia,"horario_inicio":x.horario_inicio,"horario_fim":x.horario_fim,"titulo":x.titulo,"tipo":x.tipo,"notas":x.notas,"latitude":x.latitude,"longitude":x.longitude} for x in itens])

@app.post("/api/roteiros/<int:roteiro_id>/itens")
@login_required
def roteiro_item_add(roteiro_id):
    r,role=roteiro_access(roteiro_id)
    if not r: return jsonify(error="Roteiro não encontrado ou sem acesso."),404
    data=request.get_json(silent=True) or {}
    try: dia=int(data.get("dia")); hi=str(data.get("horario_inicio") or ""); hf=str(data.get("horario_fim") or "")
    except (ValueError,TypeError): return jsonify(error="Dados inválidos."),400
    titulo=str(data.get("titulo") or "").strip()[:180]
    if not 1<=dia<=r.dias or not re.match(r"^([01]\d|2[0-3]):[0-5]\d$",hi) or not re.match(r"^([01]\d|2[0-3]):[0-5]\d$",hf) or not titulo:
        return jsonify(error="Informe intervalo de horário e atividade."),400
    if hi>=hf: return jsonify(error="O horário final deve ser depois do inicial."),400
    lat=lon=None
    try:
        geo=geocode(f"{titulo}, {r.destino}")
        if geo: lat,lon=geo.get("lat"),geo.get("lon")
    except Exception: pass
    item=RoteiroItem(roteiro_id=r.id,dia=dia,horario_inicio=hi,horario_fim=hf,titulo=titulo,tipo=str(data.get("tipo") or "atividade")[:50],latitude=lat,longitude=lon,notas=str(data.get("notas") or "")[:500])
    db.session.add(item); db.session.commit(); return jsonify(id=item.id,latitude=lat,longitude=lon,adicionado_por=db.session.get(User,user_id()).nome)

@app.delete("/api/roteiros/<int:roteiro_id>/itens/<int:item_id>")
@login_required
def roteiro_item_delete(roteiro_id,item_id):
    r,role=roteiro_access(roteiro_id)
    item=RoteiroItem.query.filter_by(id=item_id,roteiro_id=roteiro_id).first() if r else None
    if not item: return jsonify(error="Atividade não encontrada."),404
    db.session.delete(item); db.session.commit(); return jsonify(ok=True)

@app.delete("/api/roteiros/<int:roteiro_id>")
@login_required
def roteiro_delete(roteiro_id):
    r=Roteiro.query.filter_by(id=roteiro_id,usuario_id=user_id()).first()
    if not r: return jsonify(error="Roteiro não encontrado ou você não é o proprietário."),404
    db.session.delete(r); db.session.commit(); return jsonify(ok=True)

@app.post("/api/roteiros/<int:roteiro_id>/compartilhar")
@login_required
def roteiro_share(roteiro_id):
    r=Roteiro.query.filter_by(id=roteiro_id,usuario_id=user_id()).first()
    if not r: return jsonify(error="Apenas o proprietário pode compartilhar este roteiro."),403
    token=share_serializer.dumps({"id":r.id}); return jsonify(link=url_for("shared_route_public",token=token,_external=True))

@app.post("/api/roteiros/<int:roteiro_id>/membros")
@login_required
def roteiro_member_add(roteiro_id):
    r=Roteiro.query.filter_by(id=roteiro_id,usuario_id=user_id()).first()
    if not r: return jsonify(error="Apenas o proprietário pode adicionar membros."),403
    data=request.get_json(silent=True) or {}; email=str(data.get("email") or "").strip().lower()
    if not EMAIL_RE.match(email): return jsonify(error="Informe um e-mail válido."),400
    target=User.query.filter_by(email=email).first()
    if not target: return jsonify(error="A pessoa precisa ter uma conta no Travel Monitor para entrar como colaboradora."),404
    if target.id==r.usuario_id: return jsonify(error="O proprietário já está no roteiro."),400
    if RoteiroMembro.query.filter_by(roteiro_id=r.id,usuario_id=target.id).first(): return jsonify(error="Essa pessoa já está no roteiro."),409
    db.session.add(RoteiroMembro(roteiro_id=r.id,usuario_id=target.id,papel="membro")); db.session.commit()
    return jsonify(ok=True,membro={"id":target.id,"nome":target.nome,"email":target.email})

@app.get("/api/roteiros/<int:roteiro_id>/membros")
@login_required
def roteiro_members(roteiro_id):
    r,role=roteiro_access(roteiro_id)
    if not r: return jsonify(error="Roteiro não encontrado ou sem acesso."),404
    members=[{"id":r.usuario_id,"nome":db.session.get(User,r.usuario_id).nome,"email":db.session.get(User,r.usuario_id).email,"papel":"owner"}]
    for m in RoteiroMembro.query.filter_by(roteiro_id=r.id).all(): members.append({"id":m.usuario_id,"nome":m.usuario.nome,"email":m.usuario.email,"papel":"membro"})
    return jsonify(membros=members,papel=role)

@app.delete("/api/roteiros/<int:roteiro_id>/membros/<int:membro_id>")
@login_required
def roteiro_member_delete(roteiro_id,membro_id):
    r=Roteiro.query.filter_by(id=roteiro_id,usuario_id=user_id()).first()
    if not r: return jsonify(error="Apenas o proprietário pode remover membros."),403
    m=RoteiroMembro.query.filter_by(roteiro_id=r.id,usuario_id=membro_id).first()
    if not m: return jsonify(error="Membro não encontrado."),404
    db.session.delete(m); db.session.commit(); return jsonify(ok=True)

@app.get("/roteiro-compartilhado/<token>")
def shared_route_public(token):
    try: payload=share_serializer.loads(token)
    except BadSignature: return "Convite inválido.",404
    r=db.session.get(Roteiro,int(payload.get("id",0)))
    if not r: return "Roteiro não encontrado",404
    if not session.get("user_id"):
        return redirect(url_for("login",next=url_for("shared_route_public",token=token)))
    if r.usuario_id!=user_id() and not RoteiroMembro.query.filter_by(roteiro_id=r.id,usuario_id=user_id()).first():
        db.session.add(RoteiroMembro(roteiro_id=r.id,usuario_id=user_id(),papel="membro")); db.session.commit()
    return redirect(url_for("roteiro_compartilhado_page")+"?abrir="+str(r.id))

@app.post("/api/grupos")
@login_required
def grupo_create():
    data=request.get_json(silent=True) or {}; nome=str(data.get("nome") or "").strip()[:180]; destino=str(data.get("destino") or "").strip()[:180]
    try: dias=max(1,min(int(data.get("dias") or 1),60)); inicio=datetime.strptime(str(data.get("data_inicio") or ""),"%Y-%m-%d").date() if data.get("data_inicio") else None
    except (ValueError,TypeError): return jsonify(error="Data ou duração inválida."),400
    if not nome or not destino: return jsonify(error="Informe nome da viagem e destino."),400
    g=ViagemGrupo(usuario_id=user_id(),nome=nome,destino=destino,data_inicio=inicio,dias=dias,descricao=str(data.get("descricao") or "")[:500],token=__import__('secrets').token_urlsafe(32))
    db.session.add(g); db.session.flush(); db.session.add(GrupoMembro(grupo_id=g.id,usuario_id=user_id(),papel="owner")); db.session.commit(); return jsonify(id=g.id)

def grupo_access(gid):
    g=db.session.get(ViagemGrupo,gid)
    if not g: return None,None
    if g.usuario_id==user_id(): return g,"owner"
    if GrupoMembro.query.filter_by(grupo_id=gid,usuario_id=user_id()).first(): return g,"membro"
    return None,None

@app.get("/api/grupos")
@login_required
def grupo_list():
    owned=ViagemGrupo.query.filter_by(usuario_id=user_id()).all()
    joined=ViagemGrupo.query.join(GrupoMembro).filter(GrupoMembro.usuario_id==user_id()).all()
    rows={g.id:g for g in owned+joined}
    return jsonify(grupos=[{"id":g.id,"nome":g.nome,"destino":g.destino,"data_inicio":g.data_inicio.isoformat() if g.data_inicio else None,"dias":g.dias,"papel":"owner" if g.usuario_id==user_id() else "membro"} for g in rows.values()])

@app.get("/api/grupos/<int:gid>")
@login_required
def grupo_detail(gid):
    g,role=grupo_access(gid)
    if not g: return jsonify(error="Viagem em grupo não encontrada ou sem acesso."),404
    membros=[{"id":g.usuario_id,"nome":db.session.get(User,g.usuario_id).nome,"email":db.session.get(User,g.usuario_id).email,"papel":"owner"}]
    for m in g.membros:
        if m.usuario_id!=g.usuario_id: membros.append({"id":m.usuario_id,"nome":m.usuario.nome,"email":m.usuario.email,"papel":"membro"})
    itens=[{"id":i.id,"categoria":i.categoria,"nome":i.nome,"quantidade":i.quantidade,"preco":i.preco,"autor":i.usuario.nome} for i in sorted(g.itens,key=lambda x:x.id,reverse=True)]
    return jsonify(grupo={"id":g.id,"nome":g.nome,"destino":g.destino,"data_inicio":g.data_inicio.isoformat() if g.data_inicio else None,"dias":g.dias,"descricao":g.descricao,"papel":role,"link":url_for("grupo_invite",token=g.token,_external=True)},membros=membros,itens=itens,total=round(sum(i["preco"]*i["quantidade"] for i in itens),2))

@app.post("/api/grupos/<int:gid>/membros")
@login_required
def grupo_member_add(gid):
    g,role=grupo_access(gid)
    if not g or role!="owner": return jsonify(error="Apenas o criador pode adicionar pessoas."),403
    data=request.get_json(silent=True) or {}; email=str(data.get("email") or "").strip().lower(); target=User.query.filter_by(email=email).first()
    if not target: return jsonify(error="Usuário não encontrado. Envie o link do convite para ele criar/usar a conta."),404
    if GrupoMembro.query.filter_by(grupo_id=gid,usuario_id=target.id).first(): return jsonify(error="Essa pessoa já participa."),409
    db.session.add(GrupoMembro(grupo_id=gid,usuario_id=target.id,papel="membro")); db.session.commit(); return jsonify(ok=True)

@app.delete("/api/grupos/<int:gid>/membros/<int:uid>")
@login_required
def grupo_member_delete(gid,uid):
    g,role=grupo_access(gid)
    if not g or role!="owner": return jsonify(error="Apenas o criador pode remover pessoas."),403
    if uid==g.usuario_id: return jsonify(error="O criador não pode ser removido."),400
    m=GrupoMembro.query.filter_by(grupo_id=gid,usuario_id=uid).first()
    if not m: return jsonify(error="Membro não encontrado."),404
    db.session.delete(m); db.session.commit(); return jsonify(ok=True)

@app.post("/api/grupos/<int:gid>/itens")
@login_required
def grupo_item_add(gid):
    g,role=grupo_access(gid)
    if not g: return jsonify(error="Viagem em grupo não encontrada."),404
    data=request.get_json(silent=True) or {}; nome=str(data.get("nome") or "").strip()[:220]; categoria=str(data.get("categoria") or "atividade")[:50]
    try: qty=max(1,min(int(data.get("quantidade") or 1),50)); preco=max(0,float(data.get("preco") or 0))
    except (ValueError,TypeError): return jsonify(error="Preço ou quantidade inválidos."),400
    if not nome or preco>10000000: return jsonify(error="Item inválido."),400
    i=GrupoItem(grupo_id=gid,usuario_id=user_id(),categoria=categoria,nome=nome,quantidade=qty,preco=preco); db.session.add(i); db.session.commit(); return jsonify(ok=True,id=i.id)

@app.delete("/api/grupos/<int:gid>/itens/<int:item_id>")
@login_required
def grupo_item_delete(gid,item_id):
    g,role=grupo_access(gid)
    if not g: return jsonify(error="Viagem em grupo não encontrada."),404
    i=GrupoItem.query.filter_by(id=item_id,grupo_id=gid).first()
    if not i: return jsonify(error="Item não encontrado."),404
    db.session.delete(i); db.session.commit(); return jsonify(ok=True)

@app.get("/grupo/convite/<token>")
def grupo_invite(token):
    g=ViagemGrupo.query.filter_by(token=token).first()
    if not g: return "Convite inválido ou expirado.",404
    if not session.get("user_id"): return redirect(url_for("login",next=url_for("grupo_invite",token=token)))
    member=GrupoMembro.query.filter_by(grupo_id=g.id,usuario_id=user_id()).first()
    if not member:
        db.session.add(GrupoMembro(grupo_id=g.id,usuario_id=user_id(),papel="membro")); db.session.commit()
    return redirect(url_for("grupo_page")+"?abrir="+str(g.id))

@app.get("/api/clima")
@login_required
def weather():
    destino=str(request.args.get("destino") or "").strip()[:180]; data=str(request.args.get("data") or "")
    if not destino or not data: return jsonify(error="Destino e data são obrigatórios."),400
    try: d=datetime.strptime(data,"%Y-%m-%d").date()
    except ValueError: return jsonify(error="Data inválida."),400
    if d < date.today() or d > date.today()+timedelta(days=15): return jsonify(error="A previsão do roteiro está disponível para os próximos 16 dias."),400
    geo=geocode(destino)
    if not geo: return jsonify(error="Não foi possível localizar o destino."),404
    try:
        import requests as http
        r=http.get("https://api.open-meteo.com/v1/forecast",params={"latitude":geo["lat"],"longitude":geo["lon"],"daily":"weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max,precipitation_sum","timezone":"auto","forecast_days":16,"start_date":d.isoformat(),"end_date":min(d+timedelta(days=15),date.today()+timedelta(days=30)).isoformat()},timeout=5)
        r.raise_for_status(); payload=r.json(); daily=payload.get("daily",{})
        rows=[]
        for i,day in enumerate(daily.get("time",[])):
            rows.append({"data":day,"max":daily.get("temperature_2m_max",[None])[i],"min":daily.get("temperature_2m_min",[None])[i],"chuva":daily.get("precipitation_probability_max",[None])[i],"chuva_mm":daily.get("precipitation_sum",[None])[i],"codigo":daily.get("weather_code",[None])[i]})
        return jsonify(destino=geo["display_name"],previsao=rows)
    except Exception:
        return jsonify(error="A previsão do tempo não está disponível para essa data agora."),502

@app.errorhandler(413)
def request_too_large(_): return jsonify(error="Requisição muito grande."),413

@app.errorhandler(429)
def too_many_requests(_):
    if request.path.startswith("/api/"): return jsonify(error="Muitas tentativas. Aguarde um pouco e tente novamente."),429
    flash("Muitas tentativas. Aguarde um pouco e tente novamente.","error"); return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "0") == "1")
