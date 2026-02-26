# -*- coding: utf-8 -*-
from datetime import datetime, timezone

from sqlalchemy import (Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Enum)
from sqlalchemy.orm import relationship
import enum

from app.db.database import Base

# Enum define os valores possíveis para um campo
# Usar enum em vez de string solta evita erros de digitação
class TransactionType(str, enum.Enum):
    INCOME = "income"    # receita
    EXPENSE = "expense"  # despesa


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    transactions = relationship("Transaction", back_populates="owner")
    categories = relationship("Category", back_populates="owner")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    color = Column(String, default="#6366f1")  # cor para o frontend usar
    is_default = Column(Boolean, default=False)  # categorias padrão do sistema
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Chave estrangeira — liga cada categoria a um usuário
    # nullable=True porque categorias padrão não pertencem a nenhum usuário
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    owner = relationship("User", back_populates="categories")

    transactions = relationship("Transaction", back_populates="category") 


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    type = Column(Enum(TransactionType), nullable=False)
    date = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=datetime.now)

    # Soft delete — em vez de apagar, marca como deletado
    # Isso preserva o histórico e facilita auditoria
    is_deleted = Column(Boolean, default=False)

    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)

    owner = relationship("User", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")


class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)       # limite definido
    month = Column(Integer, nullable=False)      # 1-12
    year = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)