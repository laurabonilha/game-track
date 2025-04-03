from sqlalchemy import Column,  Integer, String, Float, Boolean
from app.db import Base

# Modelando as tabelas User, Game e Review usando SQLAlchemy

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column (String, unique=True)
    password = Column(String) # Hash será implementad posteriormente
    
class Game(Base):
    __tablename__ = "games"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    plataform = Column(String)
    genre = Column(String)
    
class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True)
    rating = Column(Float) # 0-5
    text = Column(String)
    sentiment_score = Column(Float) # -1 a 1 (NLP)