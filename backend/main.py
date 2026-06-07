from fastapi import FastAPI
from routers import analysis

app=FastAPI(title="kontrib API")

app.include_router(analysis.router, prefix="/api")