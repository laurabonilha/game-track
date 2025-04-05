"""
Classe criada para definir o esquema de dados que serão passados na entrada/saída
"""

from typing import Optional
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr # Valida formato de email
    username: str
    password: str # Recebe a senha em texto puro (será hasheada depois)
    
    
class UserSchema(BaseModel):
    id: int
    email: EmailStr
    is_active: bool