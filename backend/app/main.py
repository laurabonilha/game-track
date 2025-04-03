from sqlalchemy import inspect
from fastapi import FastAPI

from app.models import User, Game, Review  # Importe explicitamente

app = FastAPI()

@app.get("/")
def home():
    return {"message": "GameTrack API rodando!"}

from .db import Base, engine

def create_tables():
    print("Tabelas a serem criadas:", [t.name for t in Base.metadata.sorted_tables])
    Base.metadata.create_all(bind=engine)
    
    # Verificação
    inspector = inspect(engine)
    print("Tabelas existentes:", inspector.get_table_names())

if __name__ == "__main__":
    create_tables()