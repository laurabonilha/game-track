import os
from pathlib import Path
from backend.app.core.__secure_config import DB_USER, DB_PASS

class Config:
    def __init__(self):
        self.DB_HOST = os.getenv("DB_HOST", "localhost")
        self.DB_PORT = os.getenv("DB_PORT", "5432")
        self.DB_NAME = os.getenv("DB_NAME", "gametrack")
        self._load_credentials()

    def _load_credentials(self):
        """Carrega credenciais SEM fallback inseguro"""
        self.DB_USER = os.getenv("DB_USER", DB_USER)
        self.DB_PASS = os.getenv("DB_PASS", DB_PASS)

    @property
    def DATABASE_URL(self):
        if not hasattr(self, "DB_USER") or not hasattr(self, "DB_PASS"):
            raise RuntimeError("Credenciais do banco não configuradas!")
        return (
            "postgresql+asyncpg://"
            f"{self.DB_USER}:{self.DB_PASS}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

config = Config()