from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.security import (
    authenticate_user,
    create_access_token,
    get_current_user,
    SECRET_KEY,
    ALGORITHM
)
from backend.app.core.__secure_config import ACCESS_TOKEN_EXPIRE_MINUTES, DEMO_ACCOUNT
from backend.app.schemas.schemas import UserCreate

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(401, "Credenciais inválidas")
    # Cria token com o email do usuário como "subject" (sub)
    token = create_access_token(data={"sub": user.email})
    return {"acess_token": token}

@router.post("/register")
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db())):
    pass
    
@router.get("/teste")
async def teste_route():
    return {"message": "Rota pública - acesso liberado"}

@router.get("/protegido")
async def rota_protegida(user:dict = Depends(get_current_user)):
    return {
        "message": "Você tem acesso",
        "user": user["username"],
        "email": user["email"]
    }    