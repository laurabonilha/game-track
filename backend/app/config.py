import os
from pathlib import Path

class Config:
    # Configurações básicas (valores padrão)
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = "gametrack"

    def __init__(self):
        # Tenta carregar credenciais seguras
        try:
            from .__secure_config import DB_USER as secure_user, DB_PASS as secure_pass
            self.DB_USER = secure_user
            self.DB_PASS = secure_pass
        except ImportError:
            pass  # Mantém os valores padrão

    @property
    def DATABASE_URL(self):
        return f"postgresql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

class ProdConfig(Config):
    """Configurações para produção"""
    def __init__(self):
        super().__init__()  # Herda valores padrão
        self.DB_USER = os.getenv("DB_USER", self.DB_USER)  # Fallback para valor padrão
        self.DB_PASS = os.getenv("DB_PASS", self.DB_PASS)

# Configuração automática
config = ProdConfig() if os.getenv("ENV") == "prod" else Config()