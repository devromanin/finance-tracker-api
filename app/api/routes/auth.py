# -*- coding: utf-8 -*-

from fastapi import APIRouter, Depends, HTTPException, status 
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.core.security import hash_password, verify_password, create_access_token
from app.db.models import User
from app.schemas.user import UserCreate, UserResponse, LoginRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserResponse, status_code=201)
def register(user_data: UserCreate, db: Session = Depends(get_db)): 
    """
    Registra um novo usuario.
    Verifica se email e username ja existem antes de criar.
    """
    # Verifica se email ja esta em uso
    existing_email = db.query(User).filter(User.email == user_data.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email ja cadastrado"
        )
    
    # Verifica se username ja esta em uso
    existing_username = db.query(User).filter(User.username == user_data.username).first()
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username ja em uso"
        )
    
    # Cria o usuario com a senha hasheada - nunca salva a senha pura
    user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hash_password(user_data.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user) # atualiza o objeto com os dados do banco (id, created_at)

    return user

@router.post("/login", response_model=TokenResponse)
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    """
    Autentica o usuario e retorna um JWT.
    Mensagem de erro generica para nao revelar se o email existe ou nao
    """
    user = db.query(User).filter(User.email == credentials.email).first()

    # Verifica usuario E senha juntos - erro generico intencional
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Conta desativada"
        )
    # 0 "sub" (subject) é o indentificador do usuario do token
    acces_token = create_access_token(data={"sub": str(user.id)})

    return TokenResponse(acces_token=acces_token)