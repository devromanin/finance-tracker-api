# -*- coding: utf-8 -*-
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.security import decode_acces_token
from app.db.database import SessionLocal
from app.db.models import User

# Esquema de autenticacao bearer - le o token do header Authorization
security = HTTPBearer()

def get_db():
    """
    Abre uma sessao do banco pada cada requisicao
    e garante que ela seja fechada ao final, mesmo em caso de erro.
    O 'yield' transforma isso numa funcao gerenciadora de contexto
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: Session = Depends(get_db),
    ) -> User:
        """
        Valida o JWT e retorna o usuario logado.
        Qualquer endpoint que depensa disso so funciona com token valido.
        """
        token = credentials.credentials

        payload = decode_acces_token(token)
        if payload is None:
             raise HTTPException(
                  status_code=status.HTTP_401_UNAUTHORIZED,
                  detail="Token malformado",
             )
        
        user = db.query(User).filter(User.id == int(user_id)).first() # type: ignore
        if user is None or not user.is_active:
             raise HTTPException(
                  status_code=status.HTTP_401_UNAUTHORIZED,
                  detail="Usuario nao encontrado",
             )
        
        return user 