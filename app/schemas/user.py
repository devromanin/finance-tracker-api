# -*- coding: utf-8 -*-

from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    """Dados recebidos no registro - o que o usuario envia."""
    email: EmailStr
    username: str
    password: str 


class UserResponse(BaseModel):
    """Dados retornados pela API - nunca inclui a senha."""
    id: int 
    email: str 
    username: str 
    is_active: bool

    class Config:
        from_attributes = True # permite criar a partir de um model SQLAlchemy


class LoginRequest(BaseModel):
    """Dados recebidos no login."""
    email: EmailStr
    password: str  


class TokenResponse(BaseModel):
    """Token retornado apos login bem-sucedido."""
    acces_token: str
    token_type: str = "bearer"