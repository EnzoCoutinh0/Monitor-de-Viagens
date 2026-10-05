from datetime import datetime
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError
from extensions import db

ph = PasswordHasher()

class User(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(180), unique=True, nullable=False, index=True)
    telefone = db.Column(db.String(25), unique=True, nullable=False, index=True)
    senha = db.Column(db.String(255), nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    viagens = db.relationship("Trip", backref="usuario", lazy=True, cascade="all, delete-orphan")
    favoritos = db.relationship("FavoritePlace", backref="usuario", lazy=True, cascade="all, delete-orphan")
    alertas = db.relationship("PriceAlert", backref="usuario", lazy=True, cascade="all, delete-orphan")
    carrinho = db.relationship("BudgetItem", backref="usuario", lazy=True, cascade="all, delete-orphan")
    roteiros = db.relationship("ItineraryItem", backref="usuario", lazy=True, cascade="all, delete-orphan")
    pedidos = db.relationship("BudgetOrder", backref="usuario", lazy=True, cascade="all, delete-orphan")

    def set_password(self, raw):
        self.senha = ph.hash(raw)

    def check_password(self, raw):
        try:
            ok = ph.verify(self.senha, raw)
            if ok and ph.check_needs_rehash(self.senha):
                self.senha = ph.hash(raw)
            return ok
        except (VerifyMismatchError, VerificationError, ValueError):
            return False

class Trip(db.Model):
    __tablename__ = "viagens"
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    origem = db.Column(db.String(180), nullable=False)
    destino = db.Column(db.String(180), nullable=False)
    data_ida = db.Column(db.Date, nullable=False)
    data_volta = db.Column(db.Date, nullable=True)
    criada_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

class FavoritePlace(db.Model):
    __tablename__ = "lugares_favoritos"
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    nome = db.Column(db.String(180), nullable=False)
    cidade = db.Column(db.String(180), nullable=False, default="")
    tipo = db.Column(db.String(60), nullable=False, default="lugar")
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    lista = db.Column(db.String(20), nullable=False, default="favorito")  # favorito | visitar
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

class PriceAlert(db.Model):
    __tablename__ = "alertas_preco"
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    destino = db.Column(db.String(180), nullable=False)
    tipo = db.Column(db.String(40), nullable=False, default="pacote")
    preco_alvo = db.Column(db.Float, nullable=False)
    ativo = db.Column(db.Boolean, nullable=False, default=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

class BudgetItem(db.Model):
    __tablename__ = "itens_carrinho"
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    categoria = db.Column(db.String(40), nullable=False)
    nome = db.Column(db.String(220), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False, default=1)
    preco_unitario = db.Column(db.Float, nullable=False, default=0)
    total = db.Column(db.Float, nullable=False, default=0)
    origem = db.Column(db.String(40), nullable=False, default="simulado")
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

class BudgetOrder(db.Model):
    __tablename__ = "pedidos_orcamento"
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    total = db.Column(db.Float, nullable=False, default=0)
    status = db.Column(db.String(30), nullable=False, default="planejamento")
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

class ItineraryItem(db.Model):
    __tablename__ = "itens_roteiro"
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    data = db.Column(db.Date, nullable=False)
    horario = db.Column(db.String(5), nullable=False, default="09:00")
    titulo = db.Column(db.String(180), nullable=False)
    tipo = db.Column(db.String(50), nullable=False, default="atividade")
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    notas = db.Column(db.String(500), nullable=False, default="")
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class Roteiro(db.Model):
    __tablename__ = "roteiros"
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    destino = db.Column(db.String(180), nullable=False)
    data_inicio = db.Column(db.Date, nullable=False)
    dias = db.Column(db.Integer, nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    itens = db.relationship("RoteiroItem", backref="roteiro", lazy=True, cascade="all, delete-orphan")

class RoteiroItem(db.Model):
    __tablename__ = "roteiro_itens"
    id = db.Column(db.Integer, primary_key=True)
    roteiro_id = db.Column(db.Integer, db.ForeignKey("roteiros.id", ondelete="CASCADE"), nullable=False, index=True)
    dia = db.Column(db.Integer, nullable=False)
    horario_inicio = db.Column(db.String(5), nullable=False, default="12:00")
    horario_fim = db.Column(db.String(5), nullable=False, default="13:00")
    titulo = db.Column(db.String(180), nullable=False)
    tipo = db.Column(db.String(50), nullable=False, default="atividade")
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    notas = db.Column(db.String(500), nullable=False, default="")
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

class ViagemGrupo(db.Model):
    __tablename__ = "viagens_grupo"
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    nome = db.Column(db.String(180), nullable=False)
    destino = db.Column(db.String(180), nullable=False)
    data_inicio = db.Column(db.Date, nullable=True)
    dias = db.Column(db.Integer, nullable=False, default=1)
    descricao = db.Column(db.String(500), nullable=False, default="")
    token = db.Column(db.String(64), unique=True, nullable=False, index=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    membros = db.relationship("GrupoMembro", backref="grupo", lazy=True, cascade="all, delete-orphan")
    itens = db.relationship("GrupoItem", backref="grupo", lazy=True, cascade="all, delete-orphan")

class GrupoMembro(db.Model):
    __tablename__ = "viagens_grupo_membros"
    id = db.Column(db.Integer, primary_key=True)
    grupo_id = db.Column(db.Integer, db.ForeignKey("viagens_grupo.id", ondelete="CASCADE"), nullable=False, index=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    papel = db.Column(db.String(20), nullable=False, default="membro")
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    usuario = db.relationship("User")

class RoteiroMembro(db.Model):
    __tablename__ = "roteiro_membros"
    id = db.Column(db.Integer, primary_key=True)
    roteiro_id = db.Column(db.Integer, db.ForeignKey("roteiros.id", ondelete="CASCADE"), nullable=False, index=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    papel = db.Column(db.String(20), nullable=False, default="membro")
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    usuario = db.relationship("User")

class GrupoItem(db.Model):
    __tablename__ = "viagens_grupo_itens"
    id = db.Column(db.Integer, primary_key=True)
    grupo_id = db.Column(db.Integer, db.ForeignKey("viagens_grupo.id", ondelete="CASCADE"), nullable=False, index=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    categoria = db.Column(db.String(50), nullable=False, default="atividade")
    nome = db.Column(db.String(220), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False, default=1)
    preco = db.Column(db.Float, nullable=False, default=0)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    usuario = db.relationship("User")
