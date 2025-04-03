# backend/app/__init__.py
from .config import *
try:
    from .__secure_config import *  # Sobrescreve as configurações padrão
except ImportError:
    pass  # Em produção, use variáveis de ambiente ou outros métodos