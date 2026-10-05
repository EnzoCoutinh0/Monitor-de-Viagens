# Linha 1: Importa um módulo ou componente específico para ser usado neste arquivo.
from flask_sqlalchemy import SQLAlchemy
# Linha 2: Importa um módulo ou componente específico para ser usado neste arquivo.
from flask_wtf.csrf import CSRFProtect
# Linha 3: Importa um módulo ou componente específico para ser usado neste arquivo.
from flask_limiter import Limiter
# Linha 4: Importa um módulo ou componente específico para ser usado neste arquivo.
from flask_limiter.util import get_remote_address

# Linha 6: Cria ou atualiza uma variável com o valor calculado à direita.
db = SQLAlchemy()
# Linha 7: Cria ou atualiza uma variável com o valor calculado à direita.
csrf = CSRFProtect()
# Linha 8: Cria ou atualiza uma variável com o valor calculado à direita.
limiter = Limiter(key_func=get_remote_address, default_limits=["120 per minute"])
