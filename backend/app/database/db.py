from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from backend.app.core.config import config
import os

# Configurações síncronas (para migrações, scripts rápidos)
SYNC_DATABASE_URL = config.DATABASE_URL
sync_engine = create_engine(SYNC_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)

# Configurações assíncronas (para o FastAPI)
ASYNC_DATABASE_URL = config.DATABASE_URL.replace(
    "postgresql://", "postgresql+asyncpg://", 1
)
async_engine = create_async_engine(ASYNC_DATABASE_URL)
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

# Função para DI (Dependency Injection)
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# Teste de conexão assíncrona
async def test_async_connection():
    try:
        async with async_engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        print("✅ Conexão assíncrona OK!")
    except Exception as e:
        print(f"❌ Falha assíncrona: {e}")

# Teste de conexão síncrona (opcional)
def test_sync_connection():
    try:
        with sync_engine.connect() as conn:
            conn.execute("SELECT 1")
        print("✅ Conexão síncrona OK!")
    except Exception as e:
        print(f"❌ Falha síncrona: {e}")