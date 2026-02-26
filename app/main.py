# -*- coding: utf-8 -*-
from fastapi import FastAPI

from app.core.config import settings

app = FastAPI(
    tittle="Finance Tracker API",
    description="API REST para rastreamento de gastos pessoais",
    version="1.0.0",
    docs_url="/docs" if settings.ENVIRONMENT == "development" else None,
)

@app.get("/health", tags=["Health"])
def health_check():
    """"Verifica se a API está no ar."""
    return {"status": "ok", "environment": settings.ENVIRONMENT}