from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pathlib import Path
from app.config import config
import os
from sqlalchemy import create_engine

# Adicione esta função:
def test_db_connection():
    try:
        engine = create_engine(config.DATABASE_URL)
        conn = engine.connect()
        conn.close()
        print("✅ Conexão com o banco de dados bem-sucedida!")
    except Exception as e:
        print(f"❌ Falha na conexão com o banco de dados: {e}")

# Senha e nome do banco
SQLALCHEMY_DATABASE_URL = config.DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()