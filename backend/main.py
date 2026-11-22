import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import analysis

app=FastAPI(title="kontrib API")

default_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://kontrib-theta.vercel.app",
    "https://tinkeryard.xyz",
    "https://www.tinkeryard.xyz",
]
configured_origins = os.getenv("CORS_ORIGINS")
allowed_origins = (
    [origin.strip() for origin in configured_origins.split(",") if origin.strip()]
    if configured_origins
    else default_origins
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_origin_regex=r"^https://([a-z0-9-]+\.)?tinkeryard\.xyz$",
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analysis.router, prefix="/api")