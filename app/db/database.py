# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings 

# Engine = conexão com o banco — criada uma vez e reutilizada
engine = create_engine(settings.DATABASE_URL)

# SessionLocal = fábrica de sessões
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = classe pai de todos os models
Base = declarative_base()