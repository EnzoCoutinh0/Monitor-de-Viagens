# Linha 1: Importa um módulo ou componente específico para ser usado neste arquivo.
from datetime import datetime
# Linha 2: Importa um módulo ou componente específico para ser usado neste arquivo.
from argon2 import PasswordHasher
# Linha 3: Importa um módulo ou componente específico para ser usado neste arquivo.
from argon2.exceptions import VerifyMismatchError, VerificationError
# Linha 4: Importa um módulo ou componente específico para ser usado neste arquivo.
from extensions import db

# Linha 6: Cria ou atualiza uma variável com o valor calculado à direita.
ph = PasswordHasher()

# Linha 8: Declara uma classe que agrupa dados e comportamentos relacionados.
class User(db.Model):
    # Linha 9: Cria ou atualiza uma variável com o valor calculado à direita.
    __tablename__ = "usuarios"
    # Linha 10: Cria ou atualiza uma variável com o valor calculado à direita.
    id = db.Column(db.Integer, primary_key=True)
    # Linha 11: Cria ou atualiza uma variável com o valor calculado à direita.
    nome = db.Column(db.String(120), nullable=False)
    # Linha 12: Cria ou atualiza uma variável com o valor calculado à direita.
    email = db.Column(db.String(180), unique=True, nullable=False, index=True)
    # Linha 13: Cria ou atualiza uma variável com o valor calculado à direita.
    telefone = db.Column(db.String(25), unique=True, nullable=False, index=True)
    # Linha 14: Cria ou atualiza uma variável com o valor calculado à direita.
    senha = db.Column(db.String(255), nullable=False)
    # Linha 15: Cria ou atualiza uma variável com o valor calculado à direita.
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    # Linha 16: Cria ou atualiza uma variável com o valor calculado à direita.
    viagens = db.relationship("Trip", backref="usuario", lazy=True, cascade="all, delete-orphan")
    # Linha 17: Cria ou atualiza uma variável com o valor calculado à direita.
    favoritos = db.relationship("FavoritePlace", backref="usuario", lazy=True, cascade="all, delete-orphan")
    # Linha 18: Cria ou atualiza uma variável com o valor calculado à direita.
    alertas = db.relationship("PriceAlert", backref="usuario", lazy=True, cascade="all, delete-orphan")
    # Linha 19: Cria ou atualiza uma variável com o valor calculado à direita.
    carrinho = db.relationship("BudgetItem", backref="usuario", lazy=True, cascade="all, delete-orphan")
    # Linha 20: Cria ou atualiza uma variável com o valor calculado à direita.
    roteiros = db.relationship("ItineraryItem", backref="usuario", lazy=True, cascade="all, delete-orphan")
    # Linha 21: Cria ou atualiza uma variável com o valor calculado à direita.
    pedidos = db.relationship("BudgetOrder", backref="usuario", lazy=True, cascade="all, delete-orphan")

    # Linha 23: Declara uma função reutilizável e define seus parâmetros.
    def set_password(self, raw):
        # Linha 24: Cria ou atualiza uma variável com o valor calculado à direita.
        self.senha = ph.hash(raw)

    # Linha 26: Declara uma função reutilizável e define seus parâmetros.
    def check_password(self, raw):
        # Linha 27: Inicia um bloco para tratar possíveis erros sem interromper a aplicação.
        try:
            # Linha 28: Cria ou atualiza uma variável com o valor calculado à direita.
            ok = ph.verify(self.senha, raw)
            # Linha 29: Verifica uma condição antes de executar o bloco indentado.
            if ok and ph.check_needs_rehash(self.senha):
                # Linha 30: Cria ou atualiza uma variável com o valor calculado à direita.
                self.senha = ph.hash(raw)
            # Linha 31: Encerra a função e devolve o valor calculado.
            return ok
        # Linha 32: Captura um tipo de erro ocorrido no bloco try.
        except (VerifyMismatchError, VerificationError, ValueError):
            # Linha 33: Encerra a função e devolve o valor calculado.
            return False

# Linha 35: Declara uma classe que agrupa dados e comportamentos relacionados.
class Trip(db.Model):
    # Linha 36: Cria ou atualiza uma variável com o valor calculado à direita.
    __tablename__ = "viagens"
    # Linha 37: Cria ou atualiza uma variável com o valor calculado à direita.
    id = db.Column(db.Integer, primary_key=True)
    # Linha 38: Cria ou atualiza uma variável com o valor calculado à direita.
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    # Linha 39: Cria ou atualiza uma variável com o valor calculado à direita.
    origem = db.Column(db.String(180), nullable=False)
    # Linha 40: Cria ou atualiza uma variável com o valor calculado à direita.
    destino = db.Column(db.String(180), nullable=False)
    # Linha 41: Cria ou atualiza uma variável com o valor calculado à direita.
    data_ida = db.Column(db.Date, nullable=False)
    # Linha 42: Cria ou atualiza uma variável com o valor calculado à direita.
    data_volta = db.Column(db.Date, nullable=True)
    # Linha 43: Cria ou atualiza uma variável com o valor calculado à direita.
    criada_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

# Linha 45: Declara uma classe que agrupa dados e comportamentos relacionados.
class FavoritePlace(db.Model):
    # Linha 46: Cria ou atualiza uma variável com o valor calculado à direita.
    __tablename__ = "lugares_favoritos"
    # Linha 47: Cria ou atualiza uma variável com o valor calculado à direita.
    id = db.Column(db.Integer, primary_key=True)
    # Linha 48: Cria ou atualiza uma variável com o valor calculado à direita.
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    # Linha 49: Cria ou atualiza uma variável com o valor calculado à direita.
    nome = db.Column(db.String(180), nullable=False)
    # Linha 50: Cria ou atualiza uma variável com o valor calculado à direita.
    cidade = db.Column(db.String(180), nullable=False, default="")
    # Linha 51: Cria ou atualiza uma variável com o valor calculado à direita.
    tipo = db.Column(db.String(60), nullable=False, default="lugar")
    # Linha 52: Cria ou atualiza uma variável com o valor calculado à direita.
    latitude = db.Column(db.Float, nullable=True)
    # Linha 53: Cria ou atualiza uma variável com o valor calculado à direita.
    longitude = db.Column(db.Float, nullable=True)
    # Linha 54: Cria ou atualiza uma variável com o valor calculado à direita.
    lista = db.Column(db.String(20), nullable=False, default="favorito")  # favorito | visitar
    # Linha 55: Cria ou atualiza uma variável com o valor calculado à direita.
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

# Linha 57: Declara uma classe que agrupa dados e comportamentos relacionados.
class PriceAlert(db.Model):
    # Linha 58: Cria ou atualiza uma variável com o valor calculado à direita.
    __tablename__ = "alertas_preco"
    # Linha 59: Cria ou atualiza uma variável com o valor calculado à direita.
    id = db.Column(db.Integer, primary_key=True)
    # Linha 60: Cria ou atualiza uma variável com o valor calculado à direita.
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    # Linha 61: Cria ou atualiza uma variável com o valor calculado à direita.
    destino = db.Column(db.String(180), nullable=False)
    # Linha 62: Cria ou atualiza uma variável com o valor calculado à direita.
    tipo = db.Column(db.String(40), nullable=False, default="pacote")
    # Linha 63: Cria ou atualiza uma variável com o valor calculado à direita.
    preco_alvo = db.Column(db.Float, nullable=False)
    # Linha 64: Cria ou atualiza uma variável com o valor calculado à direita.
    ativo = db.Column(db.Boolean, nullable=False, default=True)
    # Linha 65: Cria ou atualiza uma variável com o valor calculado à direita.
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

# Linha 67: Declara uma classe que agrupa dados e comportamentos relacionados.
class BudgetItem(db.Model):
    # Linha 68: Cria ou atualiza uma variável com o valor calculado à direita.
    __tablename__ = "itens_carrinho"
    # Linha 69: Cria ou atualiza uma variável com o valor calculado à direita.
    id = db.Column(db.Integer, primary_key=True)
    # Linha 70: Cria ou atualiza uma variável com o valor calculado à direita.
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    # Linha 71: Cria ou atualiza uma variável com o valor calculado à direita.
    categoria = db.Column(db.String(40), nullable=False)
    # Linha 72: Cria ou atualiza uma variável com o valor calculado à direita.
    nome = db.Column(db.String(220), nullable=False)
    # Linha 73: Cria ou atualiza uma variável com o valor calculado à direita.
    quantidade = db.Column(db.Integer, nullable=False, default=1)
    # Linha 74: Cria ou atualiza uma variável com o valor calculado à direita.
    preco_unitario = db.Column(db.Float, nullable=False, default=0)
    # Linha 75: Cria ou atualiza uma variável com o valor calculado à direita.
    total = db.Column(db.Float, nullable=False, default=0)
    # Linha 76: Cria ou atualiza uma variável com o valor calculado à direita.
    origem = db.Column(db.String(40), nullable=False, default="simulado")
    # Linha 77: Cria ou atualiza uma variável com o valor calculado à direita.
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

# Linha 79: Declara uma classe que agrupa dados e comportamentos relacionados.
class BudgetOrder(db.Model):
    # Linha 80: Cria ou atualiza uma variável com o valor calculado à direita.
    __tablename__ = "pedidos_orcamento"
    # Linha 81: Cria ou atualiza uma variável com o valor calculado à direita.
    id = db.Column(db.Integer, primary_key=True)
    # Linha 82: Cria ou atualiza uma variável com o valor calculado à direita.
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    # Linha 83: Cria ou atualiza uma variável com o valor calculado à direita.
    total = db.Column(db.Float, nullable=False, default=0)
    # Linha 84: Cria ou atualiza uma variável com o valor calculado à direita.
    status = db.Column(db.String(30), nullable=False, default="planejamento")
    # Linha 85: Cria ou atualiza uma variável com o valor calculado à direita.
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

# Linha 87: Declara uma classe que agrupa dados e comportamentos relacionados.
class ItineraryItem(db.Model):
    # Linha 88: Cria ou atualiza uma variável com o valor calculado à direita.
    __tablename__ = "itens_roteiro"
    # Linha 89: Cria ou atualiza uma variável com o valor calculado à direita.
    id = db.Column(db.Integer, primary_key=True)
    # Linha 90: Cria ou atualiza uma variável com o valor calculado à direita.
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    # Linha 91: Cria ou atualiza uma variável com o valor calculado à direita.
    data = db.Column(db.Date, nullable=False)
    # Linha 92: Cria ou atualiza uma variável com o valor calculado à direita.
    horario = db.Column(db.String(5), nullable=False, default="09:00")
    # Linha 93: Cria ou atualiza uma variável com o valor calculado à direita.
    titulo = db.Column(db.String(180), nullable=False)
    # Linha 94: Cria ou atualiza uma variável com o valor calculado à direita.
    tipo = db.Column(db.String(50), nullable=False, default="atividade")
    # Linha 95: Cria ou atualiza uma variável com o valor calculado à direita.
    latitude = db.Column(db.Float, nullable=True)
    # Linha 96: Cria ou atualiza uma variável com o valor calculado à direita.
    longitude = db.Column(db.Float, nullable=True)
    # Linha 97: Cria ou atualiza uma variável com o valor calculado à direita.
    notas = db.Column(db.String(500), nullable=False, default="")
    # Linha 98: Cria ou atualiza uma variável com o valor calculado à direita.
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


# Linha 101: Declara uma classe que agrupa dados e comportamentos relacionados.
class Roteiro(db.Model):
    # Linha 102: Cria ou atualiza uma variável com o valor calculado à direita.
    __tablename__ = "roteiros"
    # Linha 103: Cria ou atualiza uma variável com o valor calculado à direita.
    id = db.Column(db.Integer, primary_key=True)
    # Linha 104: Cria ou atualiza uma variável com o valor calculado à direita.
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    # Linha 105: Cria ou atualiza uma variável com o valor calculado à direita.
    destino = db.Column(db.String(180), nullable=False)
    # Linha 106: Cria ou atualiza uma variável com o valor calculado à direita.
    data_inicio = db.Column(db.Date, nullable=False)
    # Linha 107: Cria ou atualiza uma variável com o valor calculado à direita.
    dias = db.Column(db.Integer, nullable=False)
    # Linha 108: Cria ou atualiza uma variável com o valor calculado à direita.
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    # Linha 109: Cria ou atualiza uma variável com o valor calculado à direita.
    itens = db.relationship("RoteiroItem", backref="roteiro", lazy=True, cascade="all, delete-orphan")

# Linha 111: Declara uma classe que agrupa dados e comportamentos relacionados.
class RoteiroItem(db.Model):
    # Linha 112: Cria ou atualiza uma variável com o valor calculado à direita.
    __tablename__ = "roteiro_itens"
    # Linha 113: Cria ou atualiza uma variável com o valor calculado à direita.
    id = db.Column(db.Integer, primary_key=True)
    # Linha 114: Cria ou atualiza uma variável com o valor calculado à direita.
    roteiro_id = db.Column(db.Integer, db.ForeignKey("roteiros.id", ondelete="CASCADE"), nullable=False, index=True)
    # Linha 115: Cria ou atualiza uma variável com o valor calculado à direita.
    dia = db.Column(db.Integer, nullable=False)
    # Linha 116: Cria ou atualiza uma variável com o valor calculado à direita.
    horario_inicio = db.Column(db.String(5), nullable=False, default="12:00")
    # Linha 117: Cria ou atualiza uma variável com o valor calculado à direita.
    horario_fim = db.Column(db.String(5), nullable=False, default="13:00")
    # Linha 118: Cria ou atualiza uma variável com o valor calculado à direita.
    titulo = db.Column(db.String(180), nullable=False)
    # Linha 119: Cria ou atualiza uma variável com o valor calculado à direita.
    tipo = db.Column(db.String(50), nullable=False, default="atividade")
    # Linha 120: Cria ou atualiza uma variável com o valor calculado à direita.
    latitude = db.Column(db.Float, nullable=True)
    # Linha 121: Cria ou atualiza uma variável com o valor calculado à direita.
    longitude = db.Column(db.Float, nullable=True)
    # Linha 122: Cria ou atualiza uma variável com o valor calculado à direita.
    notas = db.Column(db.String(500), nullable=False, default="")
    # Linha 123: Cria ou atualiza uma variável com o valor calculado à direita.
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

# Linha 125: Declara uma classe que agrupa dados e comportamentos relacionados.
class ViagemGrupo(db.Model):
    # Linha 126: Cria ou atualiza uma variável com o valor calculado à direita.
    __tablename__ = "viagens_grupo"
    # Linha 127: Cria ou atualiza uma variável com o valor calculado à direita.
    id = db.Column(db.Integer, primary_key=True)
    # Linha 128: Cria ou atualiza uma variável com o valor calculado à direita.
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    # Linha 129: Cria ou atualiza uma variável com o valor calculado à direita.
    nome = db.Column(db.String(180), nullable=False)
    # Linha 130: Cria ou atualiza uma variável com o valor calculado à direita.
    destino = db.Column(db.String(180), nullable=False)
    # Linha 131: Cria ou atualiza uma variável com o valor calculado à direita.
    data_inicio = db.Column(db.Date, nullable=True)
    # Linha 132: Cria ou atualiza uma variável com o valor calculado à direita.
    dias = db.Column(db.Integer, nullable=False, default=1)
    # Linha 133: Cria ou atualiza uma variável com o valor calculado à direita.
    descricao = db.Column(db.String(500), nullable=False, default="")
    # Linha 134: Cria ou atualiza uma variável com o valor calculado à direita.
    token = db.Column(db.String(64), unique=True, nullable=False, index=True)
    # Linha 135: Cria ou atualiza uma variável com o valor calculado à direita.
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    # Linha 136: Cria ou atualiza uma variável com o valor calculado à direita.
    membros = db.relationship("GrupoMembro", backref="grupo", lazy=True, cascade="all, delete-orphan")
    # Linha 137: Cria ou atualiza uma variável com o valor calculado à direita.
    itens = db.relationship("GrupoItem", backref="grupo", lazy=True, cascade="all, delete-orphan")

# Linha 139: Declara uma classe que agrupa dados e comportamentos relacionados.
class GrupoMembro(db.Model):
    # Linha 140: Cria ou atualiza uma variável com o valor calculado à direita.
    __tablename__ = "viagens_grupo_membros"
    # Linha 141: Cria ou atualiza uma variável com o valor calculado à direita.
    id = db.Column(db.Integer, primary_key=True)
    # Linha 142: Cria ou atualiza uma variável com o valor calculado à direita.
    grupo_id = db.Column(db.Integer, db.ForeignKey("viagens_grupo.id", ondelete="CASCADE"), nullable=False, index=True)
    # Linha 143: Cria ou atualiza uma variável com o valor calculado à direita.
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    # Linha 144: Cria ou atualiza uma variável com o valor calculado à direita.
    papel = db.Column(db.String(20), nullable=False, default="membro")
    # Linha 145: Cria ou atualiza uma variável com o valor calculado à direita.
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    # Linha 146: Cria ou atualiza uma variável com o valor calculado à direita.
    usuario = db.relationship("User")

# Linha 148: Declara uma classe que agrupa dados e comportamentos relacionados.
class RoteiroMembro(db.Model):
    # Linha 149: Cria ou atualiza uma variável com o valor calculado à direita.
    __tablename__ = "roteiro_membros"
    # Linha 150: Cria ou atualiza uma variável com o valor calculado à direita.
    id = db.Column(db.Integer, primary_key=True)
    # Linha 151: Cria ou atualiza uma variável com o valor calculado à direita.
    roteiro_id = db.Column(db.Integer, db.ForeignKey("roteiros.id", ondelete="CASCADE"), nullable=False, index=True)
    # Linha 152: Cria ou atualiza uma variável com o valor calculado à direita.
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    # Linha 153: Cria ou atualiza uma variável com o valor calculado à direita.
    papel = db.Column(db.String(20), nullable=False, default="membro")
    # Linha 154: Cria ou atualiza uma variável com o valor calculado à direita.
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    # Linha 155: Cria ou atualiza uma variável com o valor calculado à direita.
    usuario = db.relationship("User")

# Linha 157: Declara uma classe que agrupa dados e comportamentos relacionados.
class GrupoItem(db.Model):
    # Linha 158: Cria ou atualiza uma variável com o valor calculado à direita.
    __tablename__ = "viagens_grupo_itens"
    # Linha 159: Cria ou atualiza uma variável com o valor calculado à direita.
    id = db.Column(db.Integer, primary_key=True)
    # Linha 160: Cria ou atualiza uma variável com o valor calculado à direita.
    grupo_id = db.Column(db.Integer, db.ForeignKey("viagens_grupo.id", ondelete="CASCADE"), nullable=False, index=True)
    # Linha 161: Cria ou atualiza uma variável com o valor calculado à direita.
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    # Linha 162: Cria ou atualiza uma variável com o valor calculado à direita.
    categoria = db.Column(db.String(50), nullable=False, default="atividade")
    # Linha 163: Cria ou atualiza uma variável com o valor calculado à direita.
    nome = db.Column(db.String(220), nullable=False)
    # Linha 164: Cria ou atualiza uma variável com o valor calculado à direita.
    quantidade = db.Column(db.Integer, nullable=False, default=1)
    # Linha 165: Cria ou atualiza uma variável com o valor calculado à direita.
    preco = db.Column(db.Float, nullable=False, default=0)
    # Linha 166: Cria ou atualiza uma variável com o valor calculado à direita.
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    # Linha 167: Cria ou atualiza uma variável com o valor calculado à direita.
    usuario = db.relationship("User")
