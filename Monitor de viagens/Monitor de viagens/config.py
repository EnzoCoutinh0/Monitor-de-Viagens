# Linha 1: Importa uma biblioteca/módulo necessário para executar o código abaixo.
import os
# Linha 2: Importa uma biblioteca/módulo necessário para executar o código abaixo.
import secrets
# Linha 3: Importa um módulo ou componente específico para ser usado neste arquivo.
from datetime import timedelta
# Linha 4: Importa um módulo ou componente específico para ser usado neste arquivo.
from dotenv import load_dotenv

# Linha 6: Executa a instrução Python desta linha.
load_dotenv()
# Linha 7: Cria ou atualiza uma variável com o valor calculado à direita.
SECRET = os.getenv("SECRET_KEY") or secrets.token_hex(32)

# Linha 9: Declara uma classe que agrupa dados e comportamentos relacionados.
class Config:
    # Linha 10: Cria ou atualiza uma variável com o valor calculado à direita.
    SECRET_KEY = SECRET
    # Linha 11: Cria ou atualiza uma variável com o valor calculado à direita.
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "mysql+pymysql://root:@localhost/monitor_viagens")
    # Linha 12: Cria ou atualiza uma variável com o valor calculado à direita.
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Linha 13: Cria ou atualiza uma variável com o valor calculado à direita.
    SESSION_COOKIE_HTTPONLY = True
    # Linha 14: Cria ou atualiza uma variável com o valor calculado à direita.
    SESSION_COOKIE_SAMESITE = "Lax"
    # Linha 15: Executa a instrução Python desta linha.
    SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "0") == "1"
    # Linha 16: Cria ou atualiza uma variável com o valor calculado à direita.
    SESSION_COOKIE_NAME = "__Host-session" if SESSION_COOKIE_SECURE else "session"
    # Linha 17: Cria ou atualiza uma variável com o valor calculado à direita.
    SESSION_REFRESH_EACH_REQUEST = True
    # Linha 18: Cria ou atualiza uma variável com o valor calculado à direita.
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
    # Linha 19: Cria ou atualiza uma variável com o valor calculado à direita.
    WTF_CSRF_TIME_LIMIT = 3600
    # Linha 20: Cria ou atualiza uma variável com o valor calculado à direita.
    MAX_CONTENT_LENGTH = 64 * 1024
    # Linha 21: Cria ou atualiza uma variável com o valor calculado à direita.
    RATELIMIT_STORAGE_URI = os.getenv("RATELIMIT_STORAGE_URI", "memory://")
