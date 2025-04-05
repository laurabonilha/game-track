from typing import Any, Dict
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

from sqlalchemy import select
from backend.app.core.__secure_config import SECRET_KEY, ALGORITHM, DEMO_ACCOUNT
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from backend.app.models.models import User
from backend.app.database.db import get_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def verify_password(plain_password: str, hashed_password: str):
    """Verifica se a senha corresponde ao hash"""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    """Cria token JWT com expiração"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """Valida o token e retorna usuário"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if not email:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Token inválido'
            )
        async with get_db() as session:
            result = await session.execute(select(User).where(User.email == email))
            user = result.scalars().first()
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
            return user
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Credenciais inválidas'
        )

async def authenticate_user(email: str, password: str) -> User:
    """Autenticando usuários que estão no banco"""
    async with get_db() as session:
        result = await session.execute(select(User).where(User.email == email))
        user = result.scalars().first() # Pega o primeiro resultado
        
        """ verifica se a senha confere com o hash armazenado"""
        if not user or not verify_password(password, user.password):
            return None
        return user # Retorna o objeto user completo
