import os
import secrets
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()
SECRET = os.getenv("SECRET_KEY") or secrets.token_hex(32)

class Config:
    SECRET_KEY = SECRET
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "mysql+pymysql://root:@localhost/monitor_viagens")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "0") == "1"
    SESSION_COOKIE_NAME = "__Host-session" if SESSION_COOKIE_SECURE else "session"
    SESSION_REFRESH_EACH_REQUEST = True
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
    WTF_CSRF_TIME_LIMIT = 3600
    MAX_CONTENT_LENGTH = 64 * 1024
    RATELIMIT_STORAGE_URI = os.getenv("RATELIMIT_STORAGE_URI", "memory://")
