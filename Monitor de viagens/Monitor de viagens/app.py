# Linha 1: Importa uma biblioteca/módulo necessário para executar o código abaixo.
import re
# Linha 2: Importa uma biblioteca/módulo necessário para executar o código abaixo.
import os
# Linha 3: Importa uma biblioteca/módulo necessário para executar o código abaixo.
import unicodedata
# Linha 4: Importa um módulo ou componente específico para ser usado neste arquivo.
from datetime import datetime, date, timedelta
# Linha 5: Importa um módulo ou componente específico para ser usado neste arquivo.
from functools import wraps
# Linha 6: Importa um módulo ou componente específico para ser usado neste arquivo.
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
# Linha 7: Importa um módulo ou componente específico para ser usado neste arquivo.
from sqlalchemy import desc, or_
# Linha 8: Importa um módulo ou componente específico para ser usado neste arquivo.
from itsdangerous import URLSafeSerializer, BadSignature
# Linha 9: Importa um módulo ou componente específico para ser usado neste arquivo.
from sqlalchemy.exc import IntegrityError
# Linha 10: Importa um módulo ou componente específico para ser usado neste arquivo.
from config import Config
# Linha 11: Importa um módulo ou componente específico para ser usado neste arquivo.
from extensions import db, csrf, limiter
# Linha 12: Importa um módulo ou componente específico para ser usado neste arquivo.
from models import User, Trip, FavoritePlace, PriceAlert, BudgetItem, BudgetOrder, ItineraryItem, Roteiro, RoteiroItem, ViagemGrupo, GrupoMembro, GrupoItem, RoteiroMembro
# Linha 13: Importa um módulo ou componente específico para ser usado neste arquivo.
from services.travel import search_trip, geocode
# Linha 14: Importa um módulo ou componente específico para ser usado neste arquivo.
from services.destinations import DESTINATIONS

# Linha 16: Cria ou atualiza uma variável com o valor calculado à direita.
app = Flask(__name__)
# Linha 17: Configura uma rota ou comportamento da aplicação Flask.
app.config.from_object(Config)
# Linha 18: Interage com o banco de dados por meio da camada de persistência.
db.init_app(app)
# Linha 19: Executa a instrução Python desta linha.
csrf.init_app(app)
# Linha 20: Executa a instrução Python desta linha.
limiter.init_app(app)
# Linha 21: Cria ou atualiza uma variável com o valor calculado à direita.
share_serializer = URLSafeSerializer(app.config["SECRET_KEY"], salt="travel-monitor-roteiro")

# Linha 23: Abre um recurso de forma controlada e garante seu encerramento ao final do bloco.
with app.app_context():
    # Linha 24: Interage com o banco de dados por meio da camada de persistência.
    db.create_all()

# Linha 26: Cria ou atualiza uma variável com o valor calculado à direita.
CITIES = [
    # Linha 27: Executa a instrução Python desta linha.
    ("Vitória", "ES"), ("Vila Velha", "ES"), ("Serra", "ES"), ("Cariacica", "ES"), ("Guarapari", "ES"),
    # Linha 28: Executa a instrução Python desta linha.
    ("São Paulo", "SP"), ("Campinas", "SP"), ("Santos", "SP"), ("São José dos Campos", "SP"), ("Ribeirão Preto", "SP"),
    # Linha 29: Executa a instrução Python desta linha.
    ("Rio de Janeiro", "RJ"), ("Niterói", "RJ"), ("Petrópolis", "RJ"), ("Cabo Frio", "RJ"), ("Angra dos Reis", "RJ"),
    # Linha 30: Executa a instrução Python desta linha.
    ("Belo Horizonte", "MG"), ("Uberlândia", "MG"), ("Juiz de Fora", "MG"), ("Ouro Preto", "MG"), ("Poços de Caldas", "MG"),
    # Linha 31: Executa a instrução Python desta linha.
    ("Brasília", "DF"), ("Goiânia", "GO"), ("Anápolis", "GO"), ("Cuiabá", "MT"), ("Campo Grande", "MS"),
    # Linha 32: Executa a instrução Python desta linha.
    ("Curitiba", "PR"), ("Londrina", "PR"), ("Maringá", "PR"), ("Foz do Iguaçu", "PR"), ("Ponta Grossa", "PR"),
    # Linha 33: Executa a instrução Python desta linha.
    ("Porto Alegre", "RS"), ("Caxias do Sul", "RS"), ("Gramado", "RS"), ("Canela", "RS"), ("Florianópolis", "SC"),
    # Linha 34: Executa a instrução Python desta linha.
    ("Joinville", "SC"), ("Blumenau", "SC"), ("Balneário Camboriú", "SC"), ("Recife", "PE"), ("Olinda", "PE"),
    # Linha 35: Executa a instrução Python desta linha.
    ("Porto de Galinhas", "PE"), ("Salvador", "BA"), ("Porto Seguro", "BA"), ("Feira de Santana", "BA"),
    # Linha 36: Executa a instrução Python desta linha.
    ("Fortaleza", "CE"), ("Juazeiro do Norte", "CE"), ("Natal", "RN"), ("João Pessoa", "PB"), ("Maceió", "AL"),
    # Linha 37: Executa a instrução Python desta linha.
    ("Aracaju", "SE"), ("São Luís", "MA"), ("Teresina", "PI"), ("Belém", "PA"), ("Santarém", "PA"),
    # Linha 38: Executa a instrução Python desta linha.
    ("Manaus", "AM"), ("Porto Velho", "RO"), ("Rio Branco", "AC"), ("Macapá", "AP"), ("Boa Vista", "RR"),
    # Linha 39: Executa a instrução Python desta linha.
    ("Palmas", "TO"), ("Bonito", "MS"), ("Lençóis", "BA"), ("Chapada Diamantina", "BA"), ("Maragogi", "AL"),
    # Linha 40: Executa a instrução Python desta linha.
    ("Jericoacoara", "CE"), ("Campos do Jordão", "SP"), ("Búzios", "RJ"), ("Paraty", "RJ"), ("Ilhabela", "SP"),
    # Linha 41: Executa a instrução Python desta linha.
    ("Ubatuba", "SP"), ("Bento Gonçalves", "RS"), ("Caldas Novas", "GO"), ("Aparecida", "SP"), ("Montes Claros", "MG"),
    # Linha 42: Executa a instrução Python desta linha.
    ("Governador Valadares", "MG"), ("Linhares", "ES"), ("Colatina", "ES"), ("Aracruz", "ES"), ("Domingos Martins", "ES"),
    # Linha 43: Executa a instrução Python desta linha.
    ("Venda Nova do Imigrante", "ES"), ("São Mateus", "ES"), ("Cachoeiro de Itapemirim", "ES"), ("Teixeira de Freitas", "BA"),
    # Linha 44: Executa a instrução Python desta linha.
    ("Ilhéus", "BA"), ("Itacaré", "BA"), ("Camaçari", "BA"), ("Vitória da Conquista", "BA"), ("Caruaru", "PE"),
    # Linha 45: Executa a instrução Python desta linha.
    ("Petrolina", "PE"), ("Campina Grande", "PB"), ("Sobral", "CE"), ("Mossoró", "RN"), ("Parnaíba", "PI"),
    # Linha 46: Executa a instrução Python desta linha.
    ("Barreiras", "BA"), ("Cascavel", "PR"), ("Chapecó", "SC"), ("Pelotas", "RS"), ("Santa Maria", "RS"),
# Linha 47: Executa a instrução Python desta linha.
]

# Linha 49: Cria ou atualiza uma variável com o valor calculado à direita.
EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
# Linha 50: Cria ou atualiza uma variável com o valor calculado à direita.
PHONE_RE = re.compile(r"^[0-9+() .-]{8,25}$")


# Linha 53: Declara uma função reutilizável e define seus parâmetros.
def normalize_text(value):
    # Linha 54: Encerra a função e devolve o valor calculado.
    return "".join(c for c in unicodedata.normalize("NFD", value.lower()) if unicodedata.category(c) != "Mn")


# Linha 57: Declara uma função reutilizável e define seus parâmetros.
def normalize_phone(value):
    # Linha 58: Encerra a função e devolve o valor calculado.
    return re.sub(r"\D", "", str(value or ""))


# Linha 61: Declara uma função reutilizável e define seus parâmetros.
def current_user():
    # Linha 62: Encerra a função e devolve o valor calculado.
    return db.session.get(User, session.get("user_id"))


# Linha 65: Declara uma função reutilizável e define seus parâmetros.
def login_required(fn):
    # Linha 66: Aplica um decorador à função ou classe que vem logo abaixo.
    @wraps(fn)
    # Linha 67: Declara uma função reutilizável e define seus parâmetros.
    def wrapper(*args, **kwargs):
        # Linha 68: Cria ou atualiza uma variável com o valor calculado à direita.
        user_id=session.get("user_id")
        # Linha 69: Verifica uma condição antes de executar o bloco indentado.
        if not user_id: return redirect(url_for("login"))
        # Linha 70: Verifica uma condição antes de executar o bloco indentado.
        if not db.session.get(User,user_id):
            # Linha 71: Executa a instrução Python desta linha.
            session.clear(); return redirect(url_for("login"))
        # Linha 72: Encerra a função e devolve o valor calculado.
        return fn(*args, **kwargs)
    # Linha 73: Encerra a função e devolve o valor calculado.
    return wrapper


# Linha 76: Aplica um decorador à função ou classe que vem logo abaixo.
@app.after_request
# Linha 77: Declara uma função reutilizável e define seus parâmetros.
def security_headers(response):
    # Linha 78: Cria ou atualiza uma variável com o valor calculado à direita.
    response.headers["X-Content-Type-Options"]="nosniff"
    # Linha 79: Cria ou atualiza uma variável com o valor calculado à direita.
    response.headers["X-Frame-Options"]="DENY"
    # Linha 80: Cria ou atualiza uma variável com o valor calculado à direita.
    response.headers["Referrer-Policy"]="strict-origin-when-cross-origin"
    # Linha 81: Cria ou atualiza uma variável com o valor calculado à direita.
    response.headers["Permissions-Policy"]="geolocation=(), microphone=(), camera=()"
    # Linha 82: Cria ou atualiza uma variável com o valor calculado à direita.
    response.headers["Content-Security-Policy"]=("default-src 'self'; style-src 'self' https://unpkg.com; script-src 'self' https://unpkg.com; img-src 'self' data: https://*.tile.openstreetmap.org; connect-src 'self' https://api.open-meteo.com https://geocoding-api.open-meteo.com; font-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'")
    # Linha 83: Verifica uma condição antes de executar o bloco indentado.
    if request.path in {"/","/cadastro","/login","/dashboard","/roteiro","/orcamento","/clima","/perfil","/destinos","/grupo","/roteiro-compartilhado"}: response.headers["Cache-Control"]="no-store"
    # Linha 84: Encerra a função e devolve o valor calculado.
    return response


# Linha 87: Aplica um decorador à função ou classe que vem logo abaixo.
@app.get("/")
# Linha 88: Declara uma função reutilizável e define seus parâmetros.
def login():
    # Linha 89: Verifica uma condição antes de executar o bloco indentado.
    if session.get("user_id"):
        # Linha 90: Encerra a função e devolve o valor calculado.
        return redirect(url_for("dashboard"))
    # Linha 91: Encerra a função e devolve o valor calculado.
    return render_template("login.html")


# Linha 94: Aplica um decorador à função ou classe que vem logo abaixo.
@app.route("/cadastro", methods=["GET", "POST"])
# Linha 95: Aplica um decorador à função ou classe que vem logo abaixo.
@limiter.limit("5 per minute", methods=["POST"])
# Linha 96: Declara uma função reutilizável e define seus parâmetros.
def cadastro():
    # Linha 97: Verifica uma condição antes de executar o bloco indentado.
    if request.method == "POST":
        # Linha 98: Cria ou atualiza uma variável com o valor calculado à direita.
        nome = request.form.get("nome", "").strip()
        # Linha 99: Cria ou atualiza uma variável com o valor calculado à direita.
        email = request.form.get("email", "").strip().lower()
        # Linha 100: Cria ou atualiza uma variável com o valor calculado à direita.
        telefone = request.form.get("telefone", "").strip()
        # Linha 101: Cria ou atualiza uma variável com o valor calculado à direita.
        telefone_login = normalize_phone(telefone)
        # Linha 102: Cria ou atualiza uma variável com o valor calculado à direita.
        senha = request.form.get("senha", "")
        # Linha 103: Cria ou atualiza uma variável com o valor calculado à direita.
        confirmar = request.form.get("confirmar_senha", "")
        # Linha 104: Verifica uma condição antes de executar o bloco indentado.
        if not nome or len(nome) > 120 or not EMAIL_RE.match(email) or not PHONE_RE.match(telefone) or not (8 <= len(telefone_login) <= 15):
            # Linha 105: Executa a instrução Python desta linha.
            flash("Confira nome, e-mail e telefone.", "error")
        # Linha 106: Verifica uma condição alternativa caso a condição anterior não tenha sido atendida.
        elif len(senha) < 15 or len(senha) > 128:
            # Linha 107: Executa a instrução Python desta linha.
            flash("Use uma senha de 15 a 128 caracteres.", "error")
        # Linha 108: Verifica uma condição alternativa caso a condição anterior não tenha sido atendida.
        elif senha != confirmar:
            # Linha 109: Executa a instrução Python desta linha.
            flash("As senhas não conferem.", "error")
        # Linha 110: Verifica uma condição alternativa caso a condição anterior não tenha sido atendida.
        elif User.query.filter_by(email=email).first():
            # Linha 111: Executa a instrução Python desta linha.
            flash("Este e-mail já está cadastrado.", "error")
        # Linha 112: Verifica uma condição alternativa caso a condição anterior não tenha sido atendida.
        elif any(normalize_phone(u.telefone) == telefone_login for u in User.query.with_entities(User.telefone).all()):
            # Linha 113: Executa a instrução Python desta linha.
            flash("Este telefone já está cadastrado.", "error")
        # Linha 114: Define o caminho executado quando as condições anteriores forem falsas.
        else:
            # Linha 115: Inicia um bloco para tratar possíveis erros sem interromper a aplicação.
            try:
                # Linha 116: Cria ou atualiza uma variável com o valor calculado à direita.
                u = User(nome=nome, email=email, telefone=telefone_login)
                # Linha 117: Executa a instrução Python desta linha.
                u.set_password(senha)
                # Linha 118: Interage com o banco de dados por meio da camada de persistência.
                db.session.add(u)
                # Linha 119: Interage com o banco de dados por meio da camada de persistência.
                db.session.commit()
                # Linha 120: Executa a instrução Python desta linha.
                flash("Conta criada com segurança. Faça login.", "success")
                # Linha 121: Encerra a função e devolve o valor calculado.
                return redirect(url_for("login"))
            # Linha 122: Captura um tipo de erro ocorrido no bloco try.
            except IntegrityError:
                # Linha 123: Interage com o banco de dados por meio da camada de persistência.
                db.session.rollback()
                # Linha 124: Executa a instrução Python desta linha.
                flash("Não foi possível criar a conta.", "error")
    # Linha 125: Encerra a função e devolve o valor calculado.
    return render_template("cadastro.html")


# Linha 128: Aplica um decorador à função ou classe que vem logo abaixo.
@app.post("/login")
# Linha 129: Aplica um decorador à função ou classe que vem logo abaixo.
@limiter.limit("5 per minute")
# Linha 130: Declara uma função reutilizável e define seus parâmetros.
def autenticar():
    # Linha 131: Cria ou atualiza uma variável com o valor calculado à direita.
    identificador = (request.form.get("identificador") or request.form.get("email") or "").strip()
    # Linha 132: Cria ou atualiza uma variável com o valor calculado à direita.
    senha = request.form.get("senha", "")

    # Linha 134: Verifica uma condição antes de executar o bloco indentado.
    if len(identificador) > 180 or len(senha) > 128:
        # Linha 135: Executa a instrução Python desta linha.
        flash("E-mail/telefone ou senha inválidos.", "error")
        # Linha 136: Encerra a função e devolve o valor calculado.
        return redirect(url_for("login"))

    # Linha 138: Verifica uma condição antes de executar o bloco indentado.
    if EMAIL_RE.match(identificador.lower()):
        # Linha 139: Cria ou atualiza uma variável com o valor calculado à direita.
        user = User.query.filter_by(email=identificador.lower()).first()
    # Linha 140: Define o caminho executado quando as condições anteriores forem falsas.
    else:
        # Linha 141: Cria ou atualiza uma variável com o valor calculado à direita.
        telefone = normalize_phone(identificador)
        # Linha 142: Interage com o banco de dados por meio da camada de persistência.
        user = User.query.filter(or_(User.telefone == identificador, User.telefone == telefone)).first()
        # Linha 143: Verifica uma condição antes de executar o bloco indentado.
        if not user:
            # Linha 144: Executa a instrução Python desta linha.
            # Compatibilidade com contas antigas que guardavam máscara no telefone.
            # Linha 145: Interage com o banco de dados por meio da camada de persistência.
            user = next((u for u in User.query.all() if normalize_phone(u.telefone) == telefone), None)

    # Linha 147: Verifica uma condição antes de executar o bloco indentado.
    if not user or not user.check_password(senha):
        # Linha 148: Executa a instrução Python desta linha.
        flash("E-mail/telefone ou senha inválidos.", "error")
        # Linha 149: Encerra a função e devolve o valor calculado.
        return redirect(url_for("login"))

    # Linha 151: Executa a instrução Python desta linha.
    session.clear()
    # Linha 152: Cria ou atualiza uma variável com o valor calculado à direita.
    session.permanent = True
    # Linha 153: Cria ou atualiza uma variável com o valor calculado à direita.
    session["user_id"] = user.id
    # Linha 154: Encerra a função e devolve o valor calculado.
    return redirect(url_for("dashboard"))


# Linha 157: Aplica um decorador à função ou classe que vem logo abaixo.
@app.post("/logout")
# Linha 158: Aplica um decorador à função ou classe que vem logo abaixo.
@login_required
# Linha 159: Declara uma função reutilizável e define seus parâmetros.
def logout():
    # Linha 160: Executa a instrução Python desta linha.
    session.clear()
    # Linha 161: Encerra a função e devolve o valor calculado.
    return redirect(url_for("login"))


# Linha 164: Aplica um decorador à função ou classe que vem logo abaixo.
@app.get("/dashboard")
# Linha 165: Aplica um decorador à função ou classe que vem logo abaixo.
@login_required
# Linha 166: Declara uma função reutilizável e define seus parâmetros.
def dashboard():
    # Linha 167: Cria ou atualiza uma variável com o valor calculado à direita.
    user=db.session.get(User,session["user_id"])
    # Linha 168: Cria ou atualiza uma variável com o valor calculado à direita.
    trips=Trip.query.filter_by(usuario_id=user.id).order_by(desc(Trip.criada_em)).limit(20).all()
    # Linha 169: Encerra a função e devolve o valor calculado.
    return render_template("dashboard.html",nome=user.nome,viagens=trips)


# Linha 172: Aplica um decorador à função ou classe que vem logo abaixo.
@app.get("/roteiro")
# Linha 173: Aplica um decorador à função ou classe que vem logo abaixo.
@login_required
# Linha 174: Declara uma função reutilizável e define seus parâmetros.
def roteiro_page():
    # Linha 175: Encerra a função e devolve o valor calculado.
    return render_template("roteiro.html", nome=current_user().nome)

# Linha 177: Aplica um decorador à função ou classe que vem logo abaixo.
@app.get("/destinos")
# Linha 178: Aplica um decorador à função ou classe que vem logo abaixo.
@login_required
# Linha 179: Declara uma função reutilizável e define seus parâmetros.
def destinos_page():
    # Linha 180: Cria ou atualiza uma variável com o valor calculado à direita.
    user = db.session.get(User, user_id())
    # Linha 181: Cria ou atualiza uma variável com o valor calculado à direita.
    favorite_destinations = {
        # Linha 182: Executa a instrução Python desta linha.
        x.nome
        # Linha 183: Percorre os itens de uma coleção ou sequência.
        for x in FavoritePlace.query.filter_by(usuario_id=user.id, lista="favorito", tipo="destino").all()
    # Linha 184: Executa a instrução Python desta linha.
    }
    # Linha 185: Encerra a função e devolve o valor calculado.
    return render_template("destinos.html", nome=user.nome, destinos=DESTINATIONS, favorite_destinations=favorite_destinations)

# Linha 187: Aplica um decorador à função ou classe que vem logo abaixo.
@app.get("/grupo")
# Linha 188: Aplica um decorador à função ou classe que vem logo abaixo.
@login_required
# Linha 189: Declara uma função reutilizável e define seus parâmetros.
def grupo_page():
    # Linha 190: Encerra a função e devolve o valor calculado.
    return render_template("grupo.html", nome=current_user().nome)

# Linha 192: Aplica um decorador à função ou classe que vem logo abaixo.
@app.get("/roteiro-compartilhado")
# Linha 193: Aplica um decorador à função ou classe que vem logo abaixo.
@login_required
# Linha 194: Declara uma função reutilizável e define seus parâmetros.
def roteiro_compartilhado_page():
    # Linha 195: Encerra a função e devolve o valor calculado.
    return render_template("compartilhado.html", nome=current_user().nome)

# Linha 197: Aplica um decorador à função ou classe que vem logo abaixo.
@app.get("/orcamento")
# Linha 198: Aplica um decorador à função ou classe que vem logo abaixo.
@login_required
# Linha 199: Declara uma função reutilizável e define seus parâmetros.
def orcamento_page():
    # Linha 200: Encerra a função e devolve o valor calculado.
    return render_template("orcamento.html", nome=current_user().nome)

# Linha 202: Aplica um decorador à função ou classe que vem logo abaixo.
@app.get("/clima")
# Linha 203: Aplica um decorador à função ou classe que vem logo abaixo.
@login_required
# Linha 204: Declara uma função reutilizável e define seus parâmetros.
def clima_page():
    # Linha 205: Encerra a função e devolve o valor calculado.
    return render_template("clima.html", nome=current_user().nome)

# Linha 207: Aplica um decorador à função ou classe que vem logo abaixo.
@app.get("/api/cidades")
# Linha 208: Aplica um decorador à função ou classe que vem logo abaixo.
@limiter.limit("60 per minute")
# Linha 209: Declara uma função reutilizável e define seus parâmetros.
def cidades():
    # Linha 210: Cria ou atualiza uma variável com o valor calculado à direita.
    q = normalize_text(request.args.get("q", "").strip())
    # Linha 211: Verifica uma condição antes de executar o bloco indentado.
    if len(q) < 1:
        # Linha 212: Encerra a função e devolve o valor calculado.
        return jsonify([])
    # Linha 213: Cria ou atualiza uma variável com o valor calculado à direita.
    matches = []
    # Linha 214: Percorre os itens de uma coleção ou sequência.
    for city, state in CITIES:
        # Linha 215: Cria ou atualiza uma variável com o valor calculado à direita.
        normalized = normalize_text(city)
        # Linha 216: Cria ou atualiza uma variável com o valor calculado à direita.
        score = 0 if normalized.startswith(q) else (1 if q in normalized else 2)
        # Linha 217: Verifica uma condição antes de executar o bloco indentado.
        if score < 2:
            # Linha 218: Executa a instrução Python desta linha.
            matches.append({"nome": city, "uf": state, "label": f"{city}, {state}", "score": score})
    # Linha 219: Cria ou atualiza uma variável com o valor calculado à direita.
    matches.sort(key=lambda x: (x["score"], normalize_text(x["nome"])))
    # Linha 220: Encerra a função e devolve o valor calculado.
    return jsonify(matches[:8])


# Linha 223: Aplica um decorador à função ou classe que vem logo abaixo.
@app.post("/api/viagens/pesquisar")
# Linha 224: Aplica um decorador à função ou classe que vem logo abaixo.
@login_required
# Linha 225: Aplica um decorador à função ou classe que vem logo abaixo.
@limiter.limit("10 per minute")
# Linha 226: Declara uma função reutilizável e define seus parâmetros.
def pesquisar():
    # Linha 227: Cria ou atualiza uma variável com o valor calculado à direita.
    data = request.get_json(silent=True) or {}
    # Linha 228: Cria ou atualiza uma variável com o valor calculado à direita.
    origem = (data.get("origem") or "").strip()[:180]
    # Linha 229: Cria ou atualiza uma variável com o valor calculado à direita.
    destino = (data.get("destino") or "").strip()[:180]
    # Linha 230: Cria ou atualiza uma variável com o valor calculado à direita.
    data_ida = data.get("data_ida") or ""
    # Linha 231: Verifica uma condição antes de executar o bloco indentado.
    if not origem or not destino or not data_ida:
        # Linha 232: Encerra a função e devolve o valor calculado.
        return jsonify(error="Informe origem, destino e data."), 400
    # Linha 233: Inicia um bloco para tratar possíveis erros sem interromper a aplicação.
    try:
        # Linha 234: Cria ou atualiza uma variável com o valor calculado à direita.
        d = datetime.strptime(data_ida, "%Y-%m-%d").date()
    # Linha 235: Captura um tipo de erro ocorrido no bloco try.
    except ValueError:
        # Linha 236: Encerra a função e devolve o valor calculado.
        return jsonify(error="Data inválida."), 400
    # Linha 237: Verifica uma condição antes de executar o bloco indentado.
    if d < datetime.now().date():
        # Linha 238: Encerra a função e devolve o valor calculado.
        return jsonify(error="A data da viagem não pode estar no passado."), 400
    # Linha 239: Inicia um bloco para tratar possíveis erros sem interromper a aplicação.
    try:
        # Linha 240: Cria ou atualiza uma variável com o valor calculado à direita.
        noites = max(1, min(int(data.get("noites") or 1), 30))
        # Linha 241: Cria ou atualiza uma variável com o valor calculado à direita.
        result = demo_search_result(origem,destino,d,noites) if bool(data.get("demo")) else search_trip(origem, destino, d, noites)
    # Linha 242: Captura um tipo de erro ocorrido no bloco try.
    except ValueError as exc:
        # Linha 243: Encerra a função e devolve o valor calculado.
        return jsonify(error=str(exc)), 400
    # Linha 244: Captura um tipo de erro ocorrido no bloco try.
    except Exception:
        # Linha 245: Configura uma rota ou comportamento da aplicação Flask.
        app.logger.exception("Falha na pesquisa")
        # Linha 246: Encerra a função e devolve o valor calculado.
        return jsonify(error="Não foi possível concluir a pesquisa agora. Tente novamente."), 502
    # Linha 247: Inicia um bloco para tratar possíveis erros sem interromper a aplicação.
    try:
        # Linha 248: Cria ou atualiza uma variável com o valor calculado à direita.
        trip=Trip(usuario_id=session["user_id"],origem=origem,destino=destino,data_ida=d)
        # Linha 249: Cria ou atualiza uma variável com o valor calculado à direita.
        db.session.add(trip); db.session.commit(); result["trip_id"]=trip.id
    # Linha 250: Captura um tipo de erro ocorrido no bloco try.
    except Exception:
        # Linha 251: Cria ou atualiza uma variável com o valor calculado à direita.
        db.session.rollback(); app.logger.exception("Falha ao salvar histórico da viagem"); result["trip_id"]=None
    # Linha 252: Cria ou atualiza uma variável com o valor calculado à direita.
    result["origem"] = origem
    # Linha 253: Cria ou atualiza uma variável com o valor calculado à direita.
    result["data_ida"] = data_ida
    # Linha 254: Cria ou atualiza uma variável com o valor calculado à direita.
    result["data_sources"] = result.get("data_sources") or {"osm": False, "amadeus_hotels": False, "amadeus_activities": False, "flights": bool(result.get("flights")), "buses": bool(result.get("buses"))}
    # Linha 255: Encerra a função e devolve o valor calculado.
    return jsonify(result)



# Linha 259: Declara uma função reutilizável e define seus parâmetros.
def user_id():
    # Linha 260: Encerra a função e devolve o valor calculado.
    return int(session["user_id"])


# Linha 263: Declara uma função reutilizável e define seus parâmetros.
def serialize_cart(uid):
    # Linha 264: Cria ou atualiza uma variável com o valor calculado à direita.
    items=BudgetItem.query.filter_by(usuario_id=uid).order_by(BudgetItem.id.desc()).all()
    # Linha 265: Encerra a função e devolve o valor calculado.
    return [{"id":x.id,"categoria":x.categoria,"nome":x.nome,"quantidade":x.quantidade,"preco_unitario":x.preco_unitario,"total":x.total,"origem":x.origem} for x in items]


# Linha 268: Declara uma função reutilizável e define seus parâmetros.
def demo_search_result(origem,destino,data_ida,noites):
    # Linha 269: Executa a instrução Python desta linha.
    # Dados fictícios exclusivos do modo Demonstração. Nunca são apresentados como ofertas reais.
    # Linha 270: Cria ou atualiza uma variável com o valor calculado à direita.
    base=normalize_text(destino.split(",")[0])
    # Linha 271: Cria ou atualiza uma variável com o valor calculado à direita.
    names={
        # Linha 272: Executa a instrução Python desta linha.
        "rio de janeiro":[("Hotel Atlântico Demo",4.7,389.90),("Pousada Carioca Demo",4.4,279.90),("Hotel Praia Demo",4.1,329.90)],
        # Linha 273: Executa a instrução Python desta linha.
        "salvador":[("Hotel Pelô Demo",4.6,299.90),("Pousada Bahia Demo",4.3,239.90),("Hotel Farol Demo",4.5,359.90)],
        # Linha 274: Executa a instrução Python desta linha.
        "vitoria":[("Hotel Camburi Demo",4.6,289.90),("Pousada Capixaba Demo",4.2,219.90),("Hotel Centro Demo",4.0,249.90)],
    # Linha 275: Executa a instrução Python desta linha.
    }
    # Linha 276: Cria ou atualiza uma variável com o valor calculado à direita.
    hotels=names.get(base,[(f"Hotel Central {destino.split(',')[0]}",4.4,299.90),("Hotel Vista Demo",4.2,249.90),("Pousada Conforto Demo",4.6,219.90)])
    # Linha 277: Cria ou atualiza uma variável com o valor calculado à direita.
    attractions={
        # Linha 278: Executa a instrução Python desta linha.
        "rio de janeiro":["Cristo Redentor","Pão de Açúcar","Copacabana","Jardim Botânico"],
        # Linha 279: Executa a instrução Python desta linha.
        "salvador":["Pelourinho","Farol da Barra","Elevador Lacerda","Igreja do Bonfim"],
        # Linha 280: Executa a instrução Python desta linha.
        "vitoria":["Convento da Penha","Praia de Camburi","Centro Histórico","Ilha das Caieiras"],
    # Linha 281: Executa a instrução Python desta linha.
    }.get(base,["Centro histórico","Mirante principal","Museu local","Parque da cidade"])
    # Linha 282: Cria ou atualiza uma variável com o valor calculado à direita.
    buses=[("Viação Demo Express","07:30","13:10",189.90),("Viação Demo Sul","10:20","16:40",219.90),("Viação Demo Conforto","21:00","05:20",249.90)]
    # Linha 283: Cria ou atualiza uma variável com o valor calculado à direita.
    flights=[
        # Linha 284: Executa a instrução Python desta linha.
        {"companhia":"Demo Airlines","saida":"06:20","chegada":"07:55","escalas":0,"origem_aeroporto":origem,"destino_aeroporto":destino,"preco":649.90,"real":False,"source":"Demonstração"},
        # Linha 285: Executa a instrução Python desta linha.
        {"companhia":"Demo Air","saida":"09:10","chegada":"12:45","escalas":1,"origem_aeroporto":origem,"destino_aeroporto":destino,"preco":529.90,"real":False,"source":"Demonstração"},
        # Linha 286: Executa a instrução Python desta linha.
        {"companhia":"Demo Brasil","saida":"14:30","chegada":"16:20","escalas":0,"origem_aeroporto":origem,"destino_aeroporto":destino,"preco":729.90,"real":False,"source":"Demonstração"},
    # Linha 287: Executa a instrução Python desta linha.
    ]
    # Linha 288: Cria ou atualiza uma variável com o valor calculado à direita.
    hotel_rows=[{"name":n,"rating":r,"preco":p,"distance_km":round(i*1.4+0.7,1),"type":"Hotel (simulado)","lat":None,"lon":None,"real":False,"source":"Demonstração"} for i,(n,r,p) in enumerate(hotels)]
    # Linha 289: Cria ou atualiza uma variável com o valor calculado à direita.
    place_rows=[{"name":n,"rating":4.5,"preco":0,"distance_km":round(i*1.1+0.5,1),"type":"Ponto turístico (simulado)","lat":None,"lon":None,"real":False,"source":"Demonstração"} for i,n in enumerate(attractions)]
    # Linha 290: Cria ou atualiza uma variável com o valor calculado à direita.
    bus_rows=[{"companhia":c,"saida":s,"chegada":a,"preco":p,"real":False,"source":"Demonstração"} for c,s,a,p in buses]
    # Linha 291: Encerra a função e devolve o valor calculado.
    return {"origin":{"query":origem},"destination":{"query":destino},"hotel_reference_daily_average":451.71,"hotels":hotel_rows,"hotel_message":"Hotéis fictícios para testar a interface.","attractions":place_rows,"activity_message":"Pontos turísticos fictícios para testar a interface.","flights":flights,"flight_message":"Voos fictícios: use apenas para testar a interface.","buses":bus_rows,"bus_message":"Ônibus fictícios para testar a interface.","data_sources":{"demo":True,"osm":False,"amadeus_hotels":False,"amadeus_activities":False,"flights":True,"buses":True}}


# Linha 294: Declara uma função reutilizável e define seus parâmetros.
def demo_packages():
    # Linha 295: Executa a instrução Python desta linha.
    # Intentionally illustrative: these offers belong only to the budget simulator,
    # Linha 296: Executa a instrução Python desta linha.
    # never to the real flight-search results.
    # Linha 297: Encerra a função e devolve o valor calculado.
    return [
        # Linha 298: Executa a instrução Python desta linha.
        {"destino":"Vitória, ES","dias":4,"voo":899.90,"hotel":1250.00,"passeios":280.00,"transporte":180.00,"alimentacao":520.00,"total":3129.90,"destaque":"Praia + centro histórico"},
        # Linha 299: Executa a instrução Python desta linha.
        {"destino":"Rio de Janeiro, RJ","dias":5,"voo":1099.90,"hotel":1650.00,"passeios":420.00,"transporte":240.00,"alimentacao":650.00,"total":4059.90,"destaque":"Praias + Cristo + Pão de Açúcar"},
        # Linha 300: Executa a instrução Python desta linha.
        {"destino":"Salvador, BA","dias":5,"voo":949.90,"hotel":1400.00,"passeios":360.00,"transporte":220.00,"alimentacao":600.00,"total":3529.90,"destaque":"Pelourinho + praias"},
        # Linha 301: Executa a instrução Python desta linha.
        {"destino":"Florianópolis, SC","dias":5,"voo":999.90,"hotel":1450.00,"passeios":330.00,"transporte":260.00,"alimentacao":620.00,"total":3659.90,"destaque":"Praias + trilhas"},
        # Linha 302: Executa a instrução Python desta linha.
        {"destino":"Foz do Iguaçu, PR","dias":4,"voo":879.90,"hotel":1050.00,"passeios":390.00,"transporte":190.00,"alimentacao":480.00,"total":2989.90,"destaque":"Cataratas + Parque das Aves"},
        # Linha 303: Executa a instrução Python desta linha.
        {"destino":"Recife + Olinda, PE","dias":5,"voo":919.90,"hotel":1320.00,"passeios":340.00,"transporte":210.00,"alimentacao":590.00,"total":3379.90,"destaque":"Praias + cultura"},
        # Linha 304: Executa a instrução Python desta linha.
        {"destino":"Belo Horizonte, MG","dias":4,"voo":699.90,"hotel":980.00,"passeios":220.00,"transporte":170.00,"alimentacao":450.00,"total":2519.90,"destaque":"Gastronomia + Inhotim"},
        # Linha 305: Executa a instrução Python desta linha.
        {"destino":"Curitiba, PR","dias":4,"voo":749.90,"hotel":900.00,"passeios":180.00,"transporte":140.00,"alimentacao":430.00,"total":2399.90,"destaque":"Parques + centro"},
    # Linha 306: Executa a instrução Python desta linha.
    ]


# Linha 309: Aplica um decorador à função ou classe que vem logo abaixo.
@app.get("/perfil")
# Linha 310: Aplica um decorador à função ou classe que vem logo abaixo.
@login_required
# Linha 311: Declara uma função reutilizável e define seus parâmetros.
def perfil():
    # Linha 312: Cria ou atualiza uma variável com o valor calculado à direita.
    user=db.session.get(User,user_id())
    # Linha 313: Cria ou atualiza uma variável com o valor calculado à direita.
    trips=Trip.query.filter_by(usuario_id=user.id).order_by(desc(Trip.data_ida)).limit(50).all()
    # Linha 314: Cria ou atualiza uma variável com o valor calculado à direita.
    favorites=FavoritePlace.query.filter_by(usuario_id=user.id,lista="favorito").order_by(desc(FavoritePlace.criado_em)).all()
    # Linha 315: Cria ou atualiza uma variável com o valor calculado à direita.
    wishlist=FavoritePlace.query.filter_by(usuario_id=user.id,lista="visitar").order_by(desc(FavoritePlace.criado_em)).all()
    # Linha 316: Cria ou atualiza uma variável com o valor calculado à direita.
    alerts=PriceAlert.query.filter_by(usuario_id=user.id).order_by(desc(PriceAlert.criado_em)).all()
    # Linha 317: Cria ou atualiza uma variável com o valor calculado à direita.
    orders=BudgetOrder.query.filter_by(usuario_id=user.id).order_by(desc(BudgetOrder.criado_em)).limit(30).all()
    # Linha 318: Encerra a função e devolve o valor calculado.
    return render_template("perfil.html",user=user,trips=trips,favorites=favorites,wishlist=wishlist,alerts=alerts,orders=orders,today=date.today())


# Linha 321: Aplica um decorador à função ou classe que vem logo abaixo.
@app.get("/api/carrinho")
# Linha 322: Aplica um decorador à função ou classe que vem logo abaixo.
@login_required
# Linha 323: Declara uma função reutilizável e define seus parâmetros.
def cart_get():
    # Linha 324: Cria ou atualiza uma variável com o valor calculado à direita.
    items=serialize_cart(user_id()); return jsonify(items=items,total=round(sum(x["total"] for x in items),2))


# Linha 327: Aplica um decorador à função ou classe que vem logo abaixo.
@app.post("/api/carrinho")
# Linha 328: Aplica um decorador à função ou classe que vem logo abaixo.
@login_required
# Linha 329: Declara uma função reutilizável e define seus parâmetros.
def cart_add():
    # Linha 330: Cria ou atualiza uma variável com o valor calculado à direita.
    data=request.get_json(silent=True) or {}
    # Linha 331: Inicia um bloco para tratar possíveis erros sem interromper a aplicação.
    try:
        # Linha 332: Cria ou atualiza uma variável com o valor calculado à direita.
        qty=max(1,min(int(data.get("quantidade") or 1),20)); unit=float(data.get("preco_unitario"));
    # Linha 333: Cria ou atualiza uma variável com o valor calculado à direita.
    except (ValueError,TypeError): return jsonify(error="Item inválido."),400
    # Linha 334: Cria ou atualiza uma variável com o valor calculado à direita.
    nome=str(data.get("nome") or "").strip()[:220]; categoria=str(data.get("categoria") or "outro").strip()[:40]
    # Linha 335: Verifica uma condição antes de executar o bloco indentado.
    if not nome or unit<0 or unit>10000000: return jsonify(error="Item inválido."),400
    # Linha 336: Cria ou atualiza uma variável com o valor calculado à direita.
    item=BudgetItem(usuario_id=user_id(),categoria=categoria,nome=nome,quantidade=qty,preco_unitario=unit,total=round(unit*qty,2),origem="simulado")
    # Linha 337: Cria ou atualiza uma variável com o valor calculado à direita.
    db.session.add(item); db.session.commit(); return jsonify(item={"id":item.id,"categoria":item.categoria,"nome":item.nome,"quantidade":item.quantidade,"preco_unitario":item.preco_unitario,"total":item.total},total=sum(x.total for x in BudgetItem.query.filter_by(usuario_id=user_id()).all()))


# Linha 340: Aplica um decorador à função ou classe que vem logo abaixo.
@app.delete("/api/carrinho/<int:item_id>")
# Linha 341: Aplica um decorador à função ou classe que vem logo abaixo.
@login_required
# Linha 342: Declara uma função reutilizável e define seus parâmetros.
def cart_delete(item_id):
    # Linha 343: Cria ou atualiza uma variável com o valor calculado à direita.
    item=BudgetItem.query.filter_by(id=item_id,usuario_id=user_id()).first()
    # Linha 344: Verifica uma condição antes de executar o bloco indentado.
    if not item: return jsonify(error="Item não encontrado."),404
    # Linha 345: Interage com o banco de dados por meio da camada de persistência.
    db.session.delete(item); db.session.commit(); return cart_get()


# Linha 348: Aplica um decorador à função ou classe que vem logo abaixo.
@app.post("/api/carrinho/finalizar")
# Linha 349: Aplica um decorador à função ou classe que vem logo abaixo.
@login_required
# Linha 350: Declara uma função reutilizável e define seus parâmetros.
def cart_checkout():
    # Linha 351: Cria ou atualiza uma variável com o valor calculado à direita.
    items=BudgetItem.query.filter_by(usuario_id=user_id()).all()
    # Linha 352: Verifica uma condição antes de executar o bloco indentado.
    if not items: return jsonify(error="O carrinho está vazio."),400
    # Linha 353: Cria ou atualiza uma variável com o valor calculado à direita.
    total=round(sum(x.total for x in items),2)
    # Linha 354: Cria ou atualiza uma variável com o valor calculado à direita.
    order=BudgetOrder(usuario_id=user_id(),total=total,status="planejamento")
    # Linha 355: Interage com o banco de dados por meio da camada de persistência.
    db.session.add(order); db.session.commit()
    # Linha 356: Encerra a função e devolve o valor calculado.
    return jsonify(id=order.id,total=total,status=order.status)


# Linha 359: Aplica um decorador à função ou classe que vem logo abaixo.
@app.get("/api/favoritos")
# Linha 360: Aplica um decorador à função ou classe que vem logo abaixo.
@login_required
# Linha 361: Declara uma função reutilizável e define seus parâmetros.
def favorite_list():
    # Linha 362: Cria ou atualiza uma variável com o valor calculado à direita.
    items=FavoritePlace.query.filter_by(usuario_id=user_id()).order_by(desc(FavoritePlace.criado_em)).all()
    # Linha 363: Encerra a função e devolve o valor calculado.
    return jsonify(items=[{"id":x.id,"nome":x.nome,"cidade":x.cidade,"tipo":x.tipo,"lista":x.lista,"latitude":x.latitude,"longitude":x.longitude} for x in items])

# Linha 365: Aplica um decorador à função ou classe que vem logo abaixo.
@app.post("/api/favoritos")
# Linha 366: Aplica um decorador à função ou classe que vem logo abaixo.
@login_required
# Linha 367: Declara uma função reutilizável e define seus parâmetros.
def favorite_add():
    # Linha 368: Cria ou atualiza uma variável com o valor calculado à direita.
    data=request.get_json(silent=True) or {}
    # Linha 369: Cria ou atualiza uma variável com o valor calculado à direita.
    nome=str(data.get("nome") or "").strip()[:180]; cidade=str(data.get("cidade") or "").strip()[:180]; lista=str(data.get("lista") or "favorito")
    # Linha 370: Verifica uma condição antes de executar o bloco indentado.
    if lista not in {"favorito","visitar"} or not nome: return jsonify(error="Lugar inválido."),400
    # Linha 371: Cria ou atualiza uma variável com o valor calculado à direita.
    item=FavoritePlace(usuario_id=user_id(),nome=nome,cidade=cidade,tipo=str(data.get("tipo") or "lugar")[:60],latitude=data.get("latitude"),longitude=data.get("longitude"),lista=lista)
    # Linha 372: Cria ou atualiza uma variável com o valor calculado à direita.
    db.session.add(item); db.session.commit(); return jsonify(id=item.id)


# Linha 375: Aplica um decorador à função ou classe que vem logo abaixo.
@app.post("/api/favoritos/destino")
# Linha 376: Aplica um decorador à função ou classe que vem logo abaixo.
@login_required
# Linha 377: Declara uma função reutilizável e define seus parâmetros.
def favorite_destination_toggle():
    # Linha 378: Cria ou atualiza uma variável com o valor calculado à direita.
    data = request.get_json(silent=True) or {}
    # Linha 379: Cria ou atualiza uma variável com o valor calculado à direita.
    cidade = str(data.get("cidade") or "").strip()[:180]
    # Linha 380: Cria ou atualiza uma variável com o valor calculado à direita.
    pais = str(data.get("pais") or "").strip()[:180]
    # Linha 381: Cria ou atualiza uma variável com o valor calculado à direita.
    uf = str(data.get("uf") or "").strip()[:10]
    # Linha 382: Verifica uma condição antes de executar o bloco indentado.
    if not cidade:
        # Linha 383: Encerra a função e devolve o valor calculado.
        return jsonify(error="Destino inválido."), 400

    # Linha 385: Cria ou atualiza uma variável com o valor calculado à direita.
    item = FavoritePlace.query.filter_by(
        # Linha 386: Cria ou atualiza uma variável com o valor calculado à direita.
        usuario_id=user_id(), nome=cidade, lista="favorito", tipo="destino"
    # Linha 387: Executa a instrução Python desta linha.
    ).first()

    # Linha 389: Verifica uma condição antes de executar o bloco indentado.
    if item:
        # Linha 390: Interage com o banco de dados por meio da camada de persistência.
        db.session.delete(item)
        # Linha 391: Interage com o banco de dados por meio da camada de persistência.
        db.session.commit()
        # Linha 392: Encerra a função e devolve o valor calculado.
        return jsonify(favorited=False)

    # Linha 394: Cria ou atualiza uma variável com o valor calculado à direita.
    cidade_exibicao = f"{cidade}, {uf}" if uf else cidade
    # Linha 395: Cria ou atualiza uma variável com o valor calculado à direita.
    item = FavoritePlace(usuario_id=user_id(), nome=cidade, cidade=cidade_exibicao,
                         # Linha 396: Cria ou atualiza uma variável com o valor calculado à direita.
                         tipo="destino", lista="favorito")
    # Linha 397: Interage com o banco de dados por meio da camada de persistência.
    db.session.add(item)
    # Linha 398: Interage com o banco de dados por meio da camada de persistência.
    db.session.commit()
    # Linha 399: Encerra a função e devolve o valor calculado.
    return jsonify(id=item.id, favorited=True)


# Linha 402: Aplica um decorador à função ou classe que vem logo abaixo.
@app.delete("/api/favoritos/<int:item_id>")
# Linha 403: Aplica um decorador à função ou classe que vem logo abaixo.
@login_required
# Linha 404: Declara uma função reutilizável e define seus parâmetros.
def favorite_delete(item_id):
    # Linha 405: Cria ou atualiza uma variável com o valor calculado à direita.
    item=FavoritePlace.query.filter_by(id=item_id,usuario_id=user_id()).first()
    # Linha 406: Verifica uma condição antes de executar o bloco indentado.
    if not item: return jsonify(error="Lugar não encontrado."),404
    # Linha 407: Cria ou atualiza uma variável com o valor calculado à direita.
    db.session.delete(item); db.session.commit(); return jsonify(ok=True)


# Linha 410: Aplica um decorador à função ou classe que vem logo abaixo.
@app.post("/api/alertas")
# Linha 411: Aplica um decorador à função ou classe que vem logo abaixo.
@login_required
# Linha 412: Declara uma função reutilizável e define seus parâmetros.
def alert_add():
    # Linha 413: Cria ou atualiza uma variável com o valor calculado à direita.
    data=request.get_json(silent=True) or {}; destino=str(data.get("destino") or "").strip()[:180]
    # Linha 414: Cria ou atualiza uma variável com o valor calculado à direita.
    try: alvo=float(data.get("preco_alvo"))
    # Linha 415: Cria ou atualiza uma variável com o valor calculado à direita.
    except (ValueError,TypeError): return jsonify(error="Preço alvo inválido."),400
    # Linha 416: Verifica uma condição antes de executar o bloco indentado.
    if not destino or alvo<=0 or alvo>10000000: return jsonify(error="Alerta inválido."),400
    # Linha 417: Cria ou atualiza uma variável com o valor calculado à direita.
    item=PriceAlert(usuario_id=user_id(),destino=destino,preco_alvo=alvo); db.session.add(item); db.session.commit(); return jsonify(id=item.id)


# Linha 420: Aplica um decorador à função ou classe que vem logo abaixo.
@app.delete("/api/alertas/<int:item_id>")
# Linha 421: Aplica um decorador à função ou classe que vem logo abaixo.
@login_required
# Linha 422: Declara uma função reutilizável e define seus parâmetros.
def alert_delete(item_id):
    # Linha 423: Cria ou atualiza uma variável com o valor calculado à direita.
    item=PriceAlert.query.filter_by(id=item_id,usuario_id=user_id()).first()
    # Linha 424: Verifica uma condição antes de executar o bloco indentado.
    if not item: return jsonify(error="Alerta não encontrado."),404
    # Linha 425: Cria ou atualiza uma variável com o valor calculado à direita.
    db.session.delete(item); db.session.commit(); return jsonify(ok=True)


# Linha 428: Aplica um decorador à função ou classe que vem logo abaixo.
@app.get("/api/alertas/verificar")
# Linha 429: Aplica um decorador à função ou classe que vem logo abaixo.
@login_required
# Linha 430: Declara uma função reutilizável e define seus parâmetros.
def alert_check():
    # Linha 431: Cria ou atualiza uma variável com o valor calculado à direita.
    packages=demo_packages(); alerts=PriceAlert.query.filter_by(usuario_id=user_id(),ativo=True).all(); hits=[]
    # Linha 432: Percorre os itens de uma coleção ou sequência.
    for a in alerts:
        # Linha 433: Percorre os itens de uma coleção ou sequência.
        for p in packages:
            # Linha 434: Verifica uma condição antes de executar o bloco indentado.
            if normalize_text(a.destino.split(",")[0]) in normalize_text(p["destino"]) and p["total"]<=a.preco_alvo:
                # Linha 435: Executa a instrução Python desta linha.
                hits.append({"destino":p["destino"],"preco":p["total"],"alvo":a.preco_alvo,"destaque":p["destaque"]})
    # Linha 436: Encerra a função e devolve o valor calculado.
    return jsonify(hits=hits)


# Linha 439: Aplica um decorador à função ou classe que vem logo abaixo.
@app.get("/api/destinos")
# Linha 440: Aplica um decorador à função ou classe que vem logo abaixo.
@login_required
# Linha 441: Declara uma função reutilizável e define seus parâmetros.
def destinos_api():
    # Linha 442: Cria ou atualiza uma variável com o valor calculado à direita.
    q=normalize_text(request.args.get("q","").strip())
    # Linha 443: Cria ou atualiza uma variável com o valor calculado à direita.
    regiao=request.args.get("regiao","").strip().lower()
    # Linha 444: Cria ou atualiza uma variável com o valor calculado à direita.
    rows=DESTINATIONS
    # Linha 445: Verifica uma condição antes de executar o bloco indentado.
    if q:
        # Linha 446: Cria ou atualiza uma variável com o valor calculado à direita.
        rows=[x for x in rows if q in normalize_text(x["cidade"]) or q in normalize_text(x["pais"]) or any(q in normalize_text(p) for p in x["pontos"])]
    # Linha 447: Verifica uma condição antes de executar o bloco indentado.
    if regiao:
        # Linha 448: Executa a instrução Python desta linha.
        rows=[x for x in rows if x["regiao"].lower()==regiao]
    # Linha 449: Encerra a função e devolve o valor calculado.
    return jsonify(destinos=rows)


# Linha 452: Aplica um decorador à função ou classe que vem logo abaixo.
@app.get("/api/destinos/<path:cidade>")
# Linha 453: Aplica um decorador à função ou classe que vem logo abaixo.
@login_required
# Linha 454: Declara uma função reutilizável e define seus parâmetros.
def destino_detail(cidade):
    # Linha 455: Cria ou atualiza uma variável com o valor calculado à direita.
    key=normalize_text(cidade)
    # Linha 456: Executa a instrução Python desta linha.
    item=next((x for x in DESTINATIONS if normalize_text(x["cidade"])==key),None)
    # Linha 457: Verifica uma condição antes de executar o bloco indentado.
    if not item: return jsonify(error="Destino não encontrado."),404
    # Linha 458: Encerra a função e devolve o valor calculado.
    return jsonify(destino=item)


# Linha 461: Aplica um decorador à função ou classe que vem logo abaixo.
@app.get("/api/orcamento/destinos")
# Linha 462: Aplica um decorador à função ou classe que vem logo abaixo.
@login_required
# Linha 463: Declara uma função reutilizável e define seus parâmetros.
def budget_destinations():
    # Linha 464: Cria ou atualiza uma variável com o valor calculado à direita.
    try: budget=max(0,float(request.args.get("orcamento",0))); nights=max(1,min(int(request.args.get("noites",4)),15)); people=max(1,min(int(request.args.get("pessoas",1)),10))
    # Linha 465: Cria ou atualiza uma variável com o valor calculado à direita.
    except (ValueError,TypeError): return jsonify(error="Parâmetros inválidos."),400
    # Linha 466: Cria ou atualiza uma variável com o valor calculado à direita.
    packages=[]
    # Linha 467: Percorre os itens de uma coleção ou sequência.
    for p in demo_packages():
        # Linha 468: Cria ou atualiza uma variável com o valor calculado à direita.
        scaled=dict(p); factor=(nights/p["dias"])*people; scaled["dias"]=nights; scaled["pessoas"]=people
        # Linha 469: Cria ou atualiza uma variável com o valor calculado à direita.
        scaled["voo"]=round(p["voo"]*people,2)
        # Linha 470: Percorre os itens de uma coleção ou sequência.
        for k in ("hotel","passeios","transporte","alimentacao"): scaled[k]=round(p[k]*factor,2)
        # Linha 471: Cria ou atualiza uma variável com o valor calculado à direita.
        scaled["total"]=round(sum(scaled[k] for k in ("voo","hotel","passeios","transporte","alimentacao")),2)
        # Linha 472: Verifica uma condição antes de executar o bloco indentado.
        if scaled["total"]<=budget or budget<=0: packages.append(scaled)
    # Linha 473: Cria ou atualiza uma variável com o valor calculado à direita.
    packages.sort(key=lambda x:x["total"])
    # Linha 474: Encerra a função e devolve o valor calculado.
    return jsonify(packages=packages,simulado=True)


# Linha 477: Aplica um decorador à função ou classe que vem logo abaixo.
@app.get("/api/roteiros")
# Linha 478: Aplica um decorador à função ou classe que vem logo abaixo.
@login_required
# Linha 479: Declara uma função reutilizável e define seus parâmetros.
def roteiro_list():
    # Linha 480: Cria ou atualiza uma variável com o valor calculado à direita.
    owned=Roteiro.query.filter_by(usuario_id=user_id()).all()
    # Linha 481: Interage com o banco de dados por meio da camada de persistência.
    joined=Roteiro.query.join(RoteiroMembro).filter(RoteiroMembro.usuario_id==user_id()).all()
    # Linha 482: Cria ou atualiza uma variável com o valor calculado à direita.
    rows={x.id:x for x in owned+joined}
    # Linha 483: Encerra a função e devolve o valor calculado.
    return jsonify(roteiros=[{"id":x.id,"destino":x.destino,"data_inicio":x.data_inicio.isoformat(),"dias":x.dias,"papel":"owner" if x.usuario_id==user_id() else "membro"} for x in sorted(rows.values(),key=lambda z:z.criado_em,reverse=True)])

# Linha 485: Aplica um decorador à função ou classe que vem logo abaixo.
@app.post("/api/roteiros")
# Linha 486: Aplica um decorador à função ou classe que vem logo abaixo.
@login_required
# Linha 487: Declara uma função reutilizável e define seus parâmetros.
def roteiro_create():
    # Linha 488: Cria ou atualiza uma variável com o valor calculado à direita.
    data=request.get_json(silent=True) or {}
    # Linha 489: Cria ou atualiza uma variável com o valor calculado à direita.
    destino=str(data.get("destino") or "").strip()[:180]
    # Linha 490: Cria ou atualiza uma variável com o valor calculado à direita.
    try: inicio=datetime.strptime(str(data.get("data_inicio")),"%Y-%m-%d").date(); dias=int(data.get("dias"))
    # Linha 491: Cria ou atualiza uma variável com o valor calculado à direita.
    except (ValueError,TypeError): return jsonify(error="Informe destino, data de início e quantidade de dias válidos."),400
    # Linha 492: Verifica uma condição antes de executar o bloco indentado.
    if not destino or dias<1 or dias>60: return jsonify(error="A viagem deve ter entre 1 e 60 dias."),400
    # Linha 493: Verifica uma condição antes de executar o bloco indentado.
    if inicio < date.today(): return jsonify(error="A data de início não pode estar no passado."),400
    # Linha 494: Cria ou atualiza uma variável com o valor calculado à direita.
    r=Roteiro(usuario_id=user_id(),destino=destino,data_inicio=inicio,dias=dias)
    # Linha 495: Cria ou atualiza uma variável com o valor calculado à direita.
    db.session.add(r); db.session.commit(); return jsonify(id=r.id)

# Linha 497: Declara uma função reutilizável e define seus parâmetros.
def roteiro_access(roteiro_id):
    # Linha 498: Cria ou atualiza uma variável com o valor calculado à direita.
    r=db.session.get(Roteiro,roteiro_id)
    # Linha 499: Verifica uma condição antes de executar o bloco indentado.
    if not r: return None, None
    # Linha 500: Cria ou atualiza uma variável com o valor calculado à direita.
    member=RoteiroMembro.query.filter_by(roteiro_id=roteiro_id,usuario_id=user_id()).first()
    # Linha 501: Verifica uma condição antes de executar o bloco indentado.
    if r.usuario_id==user_id(): return r, "owner"
    # Linha 502: Encerra a função e devolve o valor calculado.
    return (r, "member") if member else (None,None)

# Linha 504: Aplica um decorador à função ou classe que vem logo abaixo.
@app.get("/api/roteiros/<int:roteiro_id>")
# Linha 505: Aplica um decorador à função ou classe que vem logo abaixo.
@login_required
# Linha 506: Declara uma função reutilizável e define seus parâmetros.
def roteiro_detail(roteiro_id):
    # Linha 507: Cria ou atualiza uma variável com o valor calculado à direita.
    r,role=roteiro_access(roteiro_id)
    # Linha 508: Verifica uma condição antes de executar o bloco indentado.
    if not r: return jsonify(error="Roteiro não encontrado ou sem acesso."),404
    # Linha 509: Cria ou atualiza uma variável com o valor calculado à direita.
    itens=RoteiroItem.query.filter_by(roteiro_id=r.id).order_by(RoteiroItem.dia,RoteiroItem.horario_inicio).all()
    # Linha 510: Encerra a função e devolve o valor calculado.
    return jsonify(roteiro={"id":r.id,"destino":r.destino,"data_inicio":r.data_inicio.isoformat(),"dias":r.dias,"papel":role},itens=[{"id":x.id,"dia":x.dia,"horario_inicio":x.horario_inicio,"horario_fim":x.horario_fim,"titulo":x.titulo,"tipo":x.tipo,"notas":x.notas,"latitude":x.latitude,"longitude":x.longitude} for x in itens])

# Linha 512: Aplica um decorador à função ou classe que vem logo abaixo.
@app.post("/api/roteiros/<int:roteiro_id>/itens")
# Linha 513: Aplica um decorador à função ou classe que vem logo abaixo.
@login_required
# Linha 514: Declara uma função reutilizável e define seus parâmetros.
def roteiro_item_add(roteiro_id):
    # Linha 515: Cria ou atualiza uma variável com o valor calculado à direita.
    r,role=roteiro_access(roteiro_id)
    # Linha 516: Verifica uma condição antes de executar o bloco indentado.
    if not r: return jsonify(error="Roteiro não encontrado ou sem acesso."),404
    # Linha 517: Cria ou atualiza uma variável com o valor calculado à direita.
    data=request.get_json(silent=True) or {}
    # Linha 518: Cria ou atualiza uma variável com o valor calculado à direita.
    try: dia=int(data.get("dia")); hi=str(data.get("horario_inicio") or ""); hf=str(data.get("horario_fim") or "")
    # Linha 519: Cria ou atualiza uma variável com o valor calculado à direita.
    except (ValueError,TypeError): return jsonify(error="Dados inválidos."),400
    # Linha 520: Cria ou atualiza uma variável com o valor calculado à direita.
    titulo=str(data.get("titulo") or "").strip()[:180]
    # Linha 521: Verifica uma condição antes de executar o bloco indentado.
    if not 1<=dia<=r.dias or not re.match(r"^([01]\d|2[0-3]):[0-5]\d$",hi) or not re.match(r"^([01]\d|2[0-3]):[0-5]\d$",hf) or not titulo:
        # Linha 522: Encerra a função e devolve o valor calculado.
        return jsonify(error="Informe intervalo de horário e atividade."),400
    # Linha 523: Verifica uma condição antes de executar o bloco indentado.
    if hi>=hf: return jsonify(error="O horário final deve ser depois do inicial."),400
    # Linha 524: Cria ou atualiza uma variável com o valor calculado à direita.
    lat=lon=None
    # Linha 525: Inicia um bloco para tratar possíveis erros sem interromper a aplicação.
    try:
        # Linha 526: Cria ou atualiza uma variável com o valor calculado à direita.
        geo=geocode(f"{titulo}, {r.destino}")
        # Linha 527: Verifica uma condição antes de executar o bloco indentado.
        if geo: lat,lon=geo.get("lat"),geo.get("lon")
    # Linha 528: Captura um tipo de erro ocorrido no bloco try.
    except Exception: pass
    # Linha 529: Cria ou atualiza uma variável com o valor calculado à direita.
    item=RoteiroItem(roteiro_id=r.id,dia=dia,horario_inicio=hi,horario_fim=hf,titulo=titulo,tipo=str(data.get("tipo") or "atividade")[:50],latitude=lat,longitude=lon,notas=str(data.get("notas") or "")[:500])
    # Linha 530: Cria ou atualiza uma variável com o valor calculado à direita.
    db.session.add(item); db.session.commit(); return jsonify(id=item.id,latitude=lat,longitude=lon,adicionado_por=db.session.get(User,user_id()).nome)

# Linha 532: Aplica um decorador à função ou classe que vem logo abaixo.
@app.delete("/api/roteiros/<int:roteiro_id>/itens/<int:item_id>")
# Linha 533: Aplica um decorador à função ou classe que vem logo abaixo.
@login_required
# Linha 534: Declara uma função reutilizável e define seus parâmetros.
def roteiro_item_delete(roteiro_id,item_id):
    # Linha 535: Cria ou atualiza uma variável com o valor calculado à direita.
    r,role=roteiro_access(roteiro_id)
    # Linha 536: Cria ou atualiza uma variável com o valor calculado à direita.
    item=RoteiroItem.query.filter_by(id=item_id,roteiro_id=roteiro_id).first() if r else None
    # Linha 537: Verifica uma condição antes de executar o bloco indentado.
    if not item: return jsonify(error="Atividade não encontrada."),404
    # Linha 538: Cria ou atualiza uma variável com o valor calculado à direita.
    db.session.delete(item); db.session.commit(); return jsonify(ok=True)

# Linha 540: Aplica um decorador à função ou classe que vem logo abaixo.
@app.delete("/api/roteiros/<int:roteiro_id>")
# Linha 541: Aplica um decorador à função ou classe que vem logo abaixo.
@login_required
# Linha 542: Declara uma função reutilizável e define seus parâmetros.
def roteiro_delete(roteiro_id):
    # Linha 543: Cria ou atualiza uma variável com o valor calculado à direita.
    r=Roteiro.query.filter_by(id=roteiro_id,usuario_id=user_id()).first()
    # Linha 544: Verifica uma condição antes de executar o bloco indentado.
    if not r: return jsonify(error="Roteiro não encontrado ou você não é o proprietário."),404
    # Linha 545: Cria ou atualiza uma variável com o valor calculado à direita.
    db.session.delete(r); db.session.commit(); return jsonify(ok=True)

# Linha 547: Aplica um decorador à função ou classe que vem logo abaixo.
@app.post("/api/roteiros/<int:roteiro_id>/compartilhar")
# Linha 548: Aplica um decorador à função ou classe que vem logo abaixo.
@login_required
# Linha 549: Declara uma função reutilizável e define seus parâmetros.
def roteiro_share(roteiro_id):
    # Linha 550: Cria ou atualiza uma variável com o valor calculado à direita.
    r=Roteiro.query.filter_by(id=roteiro_id,usuario_id=user_id()).first()
    # Linha 551: Verifica uma condição antes de executar o bloco indentado.
    if not r: return jsonify(error="Apenas o proprietário pode compartilhar este roteiro."),403
    # Linha 552: Cria ou atualiza uma variável com o valor calculado à direita.
    token=share_serializer.dumps({"id":r.id}); return jsonify(link=url_for("shared_route_public",token=token,_external=True))

# Linha 554: Aplica um decorador à função ou classe que vem logo abaixo.
@app.post("/api/roteiros/<int:roteiro_id>/membros")
# Linha 555: Aplica um decorador à função ou classe que vem logo abaixo.
@login_required
# Linha 556: Declara uma função reutilizável e define seus parâmetros.
def roteiro_member_add(roteiro_id):
    # Linha 557: Cria ou atualiza uma variável com o valor calculado à direita.
    r=Roteiro.query.filter_by(id=roteiro_id,usuario_id=user_id()).first()
    # Linha 558: Verifica uma condição antes de executar o bloco indentado.
    if not r: return jsonify(error="Apenas o proprietário pode adicionar membros."),403
    # Linha 559: Cria ou atualiza uma variável com o valor calculado à direita.
    data=request.get_json(silent=True) or {}; email=str(data.get("email") or "").strip().lower()
    # Linha 560: Verifica uma condição antes de executar o bloco indentado.
    if not EMAIL_RE.match(email): return jsonify(error="Informe um e-mail válido."),400
    # Linha 561: Cria ou atualiza uma variável com o valor calculado à direita.
    target=User.query.filter_by(email=email).first()
    # Linha 562: Verifica uma condição antes de executar o bloco indentado.
    if not target: return jsonify(error="A pessoa precisa ter uma conta no Travel Monitor para entrar como colaboradora."),404
    # Linha 563: Verifica uma condição antes de executar o bloco indentado.
    if target.id==r.usuario_id: return jsonify(error="O proprietário já está no roteiro."),400
    # Linha 564: Verifica uma condição antes de executar o bloco indentado.
    if RoteiroMembro.query.filter_by(roteiro_id=r.id,usuario_id=target.id).first(): return jsonify(error="Essa pessoa já está no roteiro."),409
    # Linha 565: Cria ou atualiza uma variável com o valor calculado à direita.
    db.session.add(RoteiroMembro(roteiro_id=r.id,usuario_id=target.id,papel="membro")); db.session.commit()
    # Linha 566: Encerra a função e devolve o valor calculado.
    return jsonify(ok=True,membro={"id":target.id,"nome":target.nome,"email":target.email})

# Linha 568: Aplica um decorador à função ou classe que vem logo abaixo.
@app.get("/api/roteiros/<int:roteiro_id>/membros")
# Linha 569: Aplica um decorador à função ou classe que vem logo abaixo.
@login_required
# Linha 570: Declara uma função reutilizável e define seus parâmetros.
def roteiro_members(roteiro_id):
    # Linha 571: Cria ou atualiza uma variável com o valor calculado à direita.
    r,role=roteiro_access(roteiro_id)
    # Linha 572: Verifica uma condição antes de executar o bloco indentado.
    if not r: return jsonify(error="Roteiro não encontrado ou sem acesso."),404
    # Linha 573: Cria ou atualiza uma variável com o valor calculado à direita.
    members=[{"id":r.usuario_id,"nome":db.session.get(User,r.usuario_id).nome,"email":db.session.get(User,r.usuario_id).email,"papel":"owner"}]
    # Linha 574: Percorre os itens de uma coleção ou sequência.
    for m in RoteiroMembro.query.filter_by(roteiro_id=r.id).all(): members.append({"id":m.usuario_id,"nome":m.usuario.nome,"email":m.usuario.email,"papel":"membro"})
    # Linha 575: Encerra a função e devolve o valor calculado.
    return jsonify(membros=members,papel=role)

# Linha 577: Aplica um decorador à função ou classe que vem logo abaixo.
@app.delete("/api/roteiros/<int:roteiro_id>/membros/<int:membro_id>")
# Linha 578: Aplica um decorador à função ou classe que vem logo abaixo.
@login_required
# Linha 579: Declara uma função reutilizável e define seus parâmetros.
def roteiro_member_delete(roteiro_id,membro_id):
    # Linha 580: Cria ou atualiza uma variável com o valor calculado à direita.
    r=Roteiro.query.filter_by(id=roteiro_id,usuario_id=user_id()).first()
    # Linha 581: Verifica uma condição antes de executar o bloco indentado.
    if not r: return jsonify(error="Apenas o proprietário pode remover membros."),403
    # Linha 582: Cria ou atualiza uma variável com o valor calculado à direita.
    m=RoteiroMembro.query.filter_by(roteiro_id=r.id,usuario_id=membro_id).first()
    # Linha 583: Verifica uma condição antes de executar o bloco indentado.
    if not m: return jsonify(error="Membro não encontrado."),404
    # Linha 584: Cria ou atualiza uma variável com o valor calculado à direita.
    db.session.delete(m); db.session.commit(); return jsonify(ok=True)

# Linha 586: Aplica um decorador à função ou classe que vem logo abaixo.
@app.get("/roteiro-compartilhado/<token>")
# Linha 587: Declara uma função reutilizável e define seus parâmetros.
def shared_route_public(token):
    # Linha 588: Cria ou atualiza uma variável com o valor calculado à direita.
    try: payload=share_serializer.loads(token)
    # Linha 589: Captura um tipo de erro ocorrido no bloco try.
    except BadSignature: return "Convite inválido.",404
    # Linha 590: Cria ou atualiza uma variável com o valor calculado à direita.
    r=db.session.get(Roteiro,int(payload.get("id",0)))
    # Linha 591: Verifica uma condição antes de executar o bloco indentado.
    if not r: return "Roteiro não encontrado",404
    # Linha 592: Verifica uma condição antes de executar o bloco indentado.
    if not session.get("user_id"):
        # Linha 593: Encerra a função e devolve o valor calculado.
        return redirect(url_for("login",next=url_for("shared_route_public",token=token)))
    # Linha 594: Verifica uma condição antes de executar o bloco indentado.
    if r.usuario_id!=user_id() and not RoteiroMembro.query.filter_by(roteiro_id=r.id,usuario_id=user_id()).first():
        # Linha 595: Cria ou atualiza uma variável com o valor calculado à direita.
        db.session.add(RoteiroMembro(roteiro_id=r.id,usuario_id=user_id(),papel="membro")); db.session.commit()
    # Linha 596: Encerra a função e devolve o valor calculado.
    return redirect(url_for("roteiro_compartilhado_page")+"?abrir="+str(r.id))

# Linha 598: Aplica um decorador à função ou classe que vem logo abaixo.
@app.post("/api/grupos")
# Linha 599: Aplica um decorador à função ou classe que vem logo abaixo.
@login_required
# Linha 600: Declara uma função reutilizável e define seus parâmetros.
def grupo_create():
    # Linha 601: Cria ou atualiza uma variável com o valor calculado à direita.
    data=request.get_json(silent=True) or {}; nome=str(data.get("nome") or "").strip()[:180]; destino=str(data.get("destino") or "").strip()[:180]
    # Linha 602: Cria ou atualiza uma variável com o valor calculado à direita.
    try: dias=max(1,min(int(data.get("dias") or 1),60)); inicio=datetime.strptime(str(data.get("data_inicio") or ""),"%Y-%m-%d").date() if data.get("data_inicio") else None
    # Linha 603: Cria ou atualiza uma variável com o valor calculado à direita.
    except (ValueError,TypeError): return jsonify(error="Data ou duração inválida."),400
    # Linha 604: Verifica uma condição antes de executar o bloco indentado.
    if not nome or not destino: return jsonify(error="Informe nome da viagem e destino."),400
    # Linha 605: Cria ou atualiza uma variável com o valor calculado à direita.
    g=ViagemGrupo(usuario_id=user_id(),nome=nome,destino=destino,data_inicio=inicio,dias=dias,descricao=str(data.get("descricao") or "")[:500],token=__import__('secrets').token_urlsafe(32))
    # Linha 606: Cria ou atualiza uma variável com o valor calculado à direita.
    db.session.add(g); db.session.flush(); db.session.add(GrupoMembro(grupo_id=g.id,usuario_id=user_id(),papel="owner")); db.session.commit(); return jsonify(id=g.id)

# Linha 608: Declara uma função reutilizável e define seus parâmetros.
def grupo_access(gid):
    # Linha 609: Cria ou atualiza uma variável com o valor calculado à direita.
    g=db.session.get(ViagemGrupo,gid)
    # Linha 610: Verifica uma condição antes de executar o bloco indentado.
    if not g: return None,None
    # Linha 611: Verifica uma condição antes de executar o bloco indentado.
    if g.usuario_id==user_id(): return g,"owner"
    # Linha 612: Verifica uma condição antes de executar o bloco indentado.
    if GrupoMembro.query.filter_by(grupo_id=gid,usuario_id=user_id()).first(): return g,"membro"
    # Linha 613: Encerra a função e devolve o valor calculado.
    return None,None

# Linha 615: Aplica um decorador à função ou classe que vem logo abaixo.
@app.get("/api/grupos")
# Linha 616: Aplica um decorador à função ou classe que vem logo abaixo.
@login_required
# Linha 617: Declara uma função reutilizável e define seus parâmetros.
def grupo_list():
    # Linha 618: Cria ou atualiza uma variável com o valor calculado à direita.
    owned=ViagemGrupo.query.filter_by(usuario_id=user_id()).all()
    # Linha 619: Interage com o banco de dados por meio da camada de persistência.
    joined=ViagemGrupo.query.join(GrupoMembro).filter(GrupoMembro.usuario_id==user_id()).all()
    # Linha 620: Cria ou atualiza uma variável com o valor calculado à direita.
    rows={g.id:g for g in owned+joined}
    # Linha 621: Encerra a função e devolve o valor calculado.
    return jsonify(grupos=[{"id":g.id,"nome":g.nome,"destino":g.destino,"data_inicio":g.data_inicio.isoformat() if g.data_inicio else None,"dias":g.dias,"papel":"owner" if g.usuario_id==user_id() else "membro"} for g in rows.values()])

# Linha 623: Aplica um decorador à função ou classe que vem logo abaixo.
@app.get("/api/grupos/<int:gid>")
# Linha 624: Aplica um decorador à função ou classe que vem logo abaixo.
@login_required
# Linha 625: Declara uma função reutilizável e define seus parâmetros.
def grupo_detail(gid):
    # Linha 626: Cria ou atualiza uma variável com o valor calculado à direita.
    g,role=grupo_access(gid)
    # Linha 627: Verifica uma condição antes de executar o bloco indentado.
    if not g: return jsonify(error="Viagem em grupo não encontrada ou sem acesso."),404
    # Linha 628: Cria ou atualiza uma variável com o valor calculado à direita.
    membros=[{"id":g.usuario_id,"nome":db.session.get(User,g.usuario_id).nome,"email":db.session.get(User,g.usuario_id).email,"papel":"owner"}]
    # Linha 629: Percorre os itens de uma coleção ou sequência.
    for m in g.membros:
        # Linha 630: Verifica uma condição antes de executar o bloco indentado.
        if m.usuario_id!=g.usuario_id: membros.append({"id":m.usuario_id,"nome":m.usuario.nome,"email":m.usuario.email,"papel":"membro"})
    # Linha 631: Cria ou atualiza uma variável com o valor calculado à direita.
    itens=[{"id":i.id,"categoria":i.categoria,"nome":i.nome,"quantidade":i.quantidade,"preco":i.preco,"autor":i.usuario.nome} for i in sorted(g.itens,key=lambda x:x.id,reverse=True)]
    # Linha 632: Encerra a função e devolve o valor calculado.
    return jsonify(grupo={"id":g.id,"nome":g.nome,"destino":g.destino,"data_inicio":g.data_inicio.isoformat() if g.data_inicio else None,"dias":g.dias,"descricao":g.descricao,"papel":role,"link":url_for("grupo_invite",token=g.token,_external=True)},membros=membros,itens=itens,total=round(sum(i["preco"]*i["quantidade"] for i in itens),2))

# Linha 634: Aplica um decorador à função ou classe que vem logo abaixo.
@app.post("/api/grupos/<int:gid>/membros")
# Linha 635: Aplica um decorador à função ou classe que vem logo abaixo.
@login_required
# Linha 636: Declara uma função reutilizável e define seus parâmetros.
def grupo_member_add(gid):
    # Linha 637: Cria ou atualiza uma variável com o valor calculado à direita.
    g,role=grupo_access(gid)
    # Linha 638: Verifica uma condição antes de executar o bloco indentado.
    if not g or role!="owner": return jsonify(error="Apenas o criador pode adicionar pessoas."),403
    # Linha 639: Cria ou atualiza uma variável com o valor calculado à direita.
    data=request.get_json(silent=True) or {}; email=str(data.get("email") or "").strip().lower(); target=User.query.filter_by(email=email).first()
    # Linha 640: Verifica uma condição antes de executar o bloco indentado.
    if not target: return jsonify(error="Usuário não encontrado. Envie o link do convite para ele criar/usar a conta."),404
    # Linha 641: Verifica uma condição antes de executar o bloco indentado.
    if GrupoMembro.query.filter_by(grupo_id=gid,usuario_id=target.id).first(): return jsonify(error="Essa pessoa já participa."),409
    # Linha 642: Cria ou atualiza uma variável com o valor calculado à direita.
    db.session.add(GrupoMembro(grupo_id=gid,usuario_id=target.id,papel="membro")); db.session.commit(); return jsonify(ok=True)

# Linha 644: Aplica um decorador à função ou classe que vem logo abaixo.
@app.delete("/api/grupos/<int:gid>/membros/<int:uid>")
# Linha 645: Aplica um decorador à função ou classe que vem logo abaixo.
@login_required
# Linha 646: Declara uma função reutilizável e define seus parâmetros.
def grupo_member_delete(gid,uid):
    # Linha 647: Cria ou atualiza uma variável com o valor calculado à direita.
    g,role=grupo_access(gid)
    # Linha 648: Verifica uma condição antes de executar o bloco indentado.
    if not g or role!="owner": return jsonify(error="Apenas o criador pode remover pessoas."),403
    # Linha 649: Verifica uma condição antes de executar o bloco indentado.
    if uid==g.usuario_id: return jsonify(error="O criador não pode ser removido."),400
    # Linha 650: Cria ou atualiza uma variável com o valor calculado à direita.
    m=GrupoMembro.query.filter_by(grupo_id=gid,usuario_id=uid).first()
    # Linha 651: Verifica uma condição antes de executar o bloco indentado.
    if not m: return jsonify(error="Membro não encontrado."),404
    # Linha 652: Cria ou atualiza uma variável com o valor calculado à direita.
    db.session.delete(m); db.session.commit(); return jsonify(ok=True)

# Linha 654: Aplica um decorador à função ou classe que vem logo abaixo.
@app.post("/api/grupos/<int:gid>/itens")
# Linha 655: Aplica um decorador à função ou classe que vem logo abaixo.
@login_required
# Linha 656: Declara uma função reutilizável e define seus parâmetros.
def grupo_item_add(gid):
    # Linha 657: Cria ou atualiza uma variável com o valor calculado à direita.
    g,role=grupo_access(gid)
    # Linha 658: Verifica uma condição antes de executar o bloco indentado.
    if not g: return jsonify(error="Viagem em grupo não encontrada."),404
    # Linha 659: Cria ou atualiza uma variável com o valor calculado à direita.
    data=request.get_json(silent=True) or {}; nome=str(data.get("nome") or "").strip()[:220]; categoria=str(data.get("categoria") or "atividade")[:50]
    # Linha 660: Cria ou atualiza uma variável com o valor calculado à direita.
    try: qty=max(1,min(int(data.get("quantidade") or 1),50)); preco=max(0,float(data.get("preco") or 0))
    # Linha 661: Cria ou atualiza uma variável com o valor calculado à direita.
    except (ValueError,TypeError): return jsonify(error="Preço ou quantidade inválidos."),400
    # Linha 662: Verifica uma condição antes de executar o bloco indentado.
    if not nome or preco>10000000: return jsonify(error="Item inválido."),400
    # Linha 663: Cria ou atualiza uma variável com o valor calculado à direita.
    i=GrupoItem(grupo_id=gid,usuario_id=user_id(),categoria=categoria,nome=nome,quantidade=qty,preco=preco); db.session.add(i); db.session.commit(); return jsonify(ok=True,id=i.id)

# Linha 665: Aplica um decorador à função ou classe que vem logo abaixo.
@app.delete("/api/grupos/<int:gid>/itens/<int:item_id>")
# Linha 666: Aplica um decorador à função ou classe que vem logo abaixo.
@login_required
# Linha 667: Declara uma função reutilizável e define seus parâmetros.
def grupo_item_delete(gid,item_id):
    # Linha 668: Cria ou atualiza uma variável com o valor calculado à direita.
    g,role=grupo_access(gid)
    # Linha 669: Verifica uma condição antes de executar o bloco indentado.
    if not g: return jsonify(error="Viagem em grupo não encontrada."),404
    # Linha 670: Cria ou atualiza uma variável com o valor calculado à direita.
    i=GrupoItem.query.filter_by(id=item_id,grupo_id=gid).first()
    # Linha 671: Verifica uma condição antes de executar o bloco indentado.
    if not i: return jsonify(error="Item não encontrado."),404
    # Linha 672: Cria ou atualiza uma variável com o valor calculado à direita.
    db.session.delete(i); db.session.commit(); return jsonify(ok=True)

# Linha 674: Aplica um decorador à função ou classe que vem logo abaixo.
@app.get("/grupo/convite/<token>")
# Linha 675: Declara uma função reutilizável e define seus parâmetros.
def grupo_invite(token):
    # Linha 676: Cria ou atualiza uma variável com o valor calculado à direita.
    g=ViagemGrupo.query.filter_by(token=token).first()
    # Linha 677: Verifica uma condição antes de executar o bloco indentado.
    if not g: return "Convite inválido ou expirado.",404
    # Linha 678: Verifica uma condição antes de executar o bloco indentado.
    if not session.get("user_id"): return redirect(url_for("login",next=url_for("grupo_invite",token=token)))
    # Linha 679: Cria ou atualiza uma variável com o valor calculado à direita.
    member=GrupoMembro.query.filter_by(grupo_id=g.id,usuario_id=user_id()).first()
    # Linha 680: Verifica uma condição antes de executar o bloco indentado.
    if not member:
        # Linha 681: Cria ou atualiza uma variável com o valor calculado à direita.
        db.session.add(GrupoMembro(grupo_id=g.id,usuario_id=user_id(),papel="membro")); db.session.commit()
    # Linha 682: Encerra a função e devolve o valor calculado.
    return redirect(url_for("grupo_page")+"?abrir="+str(g.id))

# Linha 684: Aplica um decorador à função ou classe que vem logo abaixo.
@app.get("/api/clima")
# Linha 685: Aplica um decorador à função ou classe que vem logo abaixo.
@login_required
# Linha 686: Declara uma função reutilizável e define seus parâmetros.
def weather():
    # Linha 687: Cria ou atualiza uma variável com o valor calculado à direita.
    destino=str(request.args.get("destino") or "").strip()[:180]; data=str(request.args.get("data") or "")
    # Linha 688: Verifica uma condição antes de executar o bloco indentado.
    if not destino or not data: return jsonify(error="Destino e data são obrigatórios."),400
    # Linha 689: Cria ou atualiza uma variável com o valor calculado à direita.
    try: d=datetime.strptime(data,"%Y-%m-%d").date()
    # Linha 690: Cria ou atualiza uma variável com o valor calculado à direita.
    except ValueError: return jsonify(error="Data inválida."),400
    # Linha 691: Verifica uma condição antes de executar o bloco indentado.
    if d < date.today() or d > date.today()+timedelta(days=15): return jsonify(error="A previsão do roteiro está disponível para os próximos 16 dias."),400
    # Linha 692: Cria ou atualiza uma variável com o valor calculado à direita.
    geo=geocode(destino)
    # Linha 693: Verifica uma condição antes de executar o bloco indentado.
    if not geo: return jsonify(error="Não foi possível localizar o destino."),404
    # Linha 694: Inicia um bloco para tratar possíveis erros sem interromper a aplicação.
    try:
        # Linha 695: Importa uma biblioteca/módulo necessário para executar o código abaixo.
        import requests as http
        # Linha 696: Cria ou atualiza uma variável com o valor calculado à direita.
        r=http.get("https://api.open-meteo.com/v1/forecast",params={"latitude":geo["lat"],"longitude":geo["lon"],"daily":"weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max,precipitation_sum","timezone":"auto","forecast_days":16,"start_date":d.isoformat(),"end_date":min(d+timedelta(days=15),date.today()+timedelta(days=30)).isoformat()},timeout=5)
        # Linha 697: Cria ou atualiza uma variável com o valor calculado à direita.
        r.raise_for_status(); payload=r.json(); daily=payload.get("daily",{})
        # Linha 698: Cria ou atualiza uma variável com o valor calculado à direita.
        rows=[]
        # Linha 699: Percorre os itens de uma coleção ou sequência.
        for i,day in enumerate(daily.get("time",[])):
            # Linha 700: Executa a instrução Python desta linha.
            rows.append({"data":day,"max":daily.get("temperature_2m_max",[None])[i],"min":daily.get("temperature_2m_min",[None])[i],"chuva":daily.get("precipitation_probability_max",[None])[i],"chuva_mm":daily.get("precipitation_sum",[None])[i],"codigo":daily.get("weather_code",[None])[i]})
        # Linha 701: Encerra a função e devolve o valor calculado.
        return jsonify(destino=geo["display_name"],previsao=rows)
    # Linha 702: Captura um tipo de erro ocorrido no bloco try.
    except Exception:
        # Linha 703: Encerra a função e devolve o valor calculado.
        return jsonify(error="A previsão do tempo não está disponível para essa data agora."),502

# Linha 705: Aplica um decorador à função ou classe que vem logo abaixo.
@app.errorhandler(413)
# Linha 706: Declara uma função reutilizável e define seus parâmetros.
def request_too_large(_): return jsonify(error="Requisição muito grande."),413

# Linha 708: Aplica um decorador à função ou classe que vem logo abaixo.
@app.errorhandler(429)
# Linha 709: Declara uma função reutilizável e define seus parâmetros.
def too_many_requests(_):
    # Linha 710: Verifica uma condição antes de executar o bloco indentado.
    if request.path.startswith("/api/"): return jsonify(error="Muitas tentativas. Aguarde um pouco e tente novamente."),429
    # Linha 711: Executa a instrução Python desta linha.
    flash("Muitas tentativas. Aguarde um pouco e tente novamente.","error"); return redirect(url_for("login"))


# Linha 714: Executa o bloco abaixo somente quando este arquivo é executado diretamente.
if __name__ == "__main__":
    # Linha 715: Configura uma rota ou comportamento da aplicação Flask.
    app.run(debug=os.getenv("FLASK_DEBUG", "0") == "1")
