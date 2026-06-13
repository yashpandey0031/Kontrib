from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import analysis

app=FastAPI(title="kontrib API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173",
                   "https://kontrib-theta.vercel.app/"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analysis.router, prefix="/api")