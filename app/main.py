# -*- coding: utf-8 -*-
from fastapi import FastAPI

from app.core.config import settings
from app.db.database import engine
from app.db import models 
from app.api.routes import auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    tittle="Finance Tracker API",
    description="API REST para rastreamento de gastos pessoais",
    version="1.0.0",
    docs_url="/docs" if settings.ENVIRONMENT == "development" else None,
)

# Registra os routers
app.include_router(auth.router)


@app.get("/health", tags=["Health"])
def health_check():
    """"Verifica se a API está no ar."""
    return {"status": "ok", "environment": settings.ENVIRONMENT}