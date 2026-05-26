from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.adapters.api_adapter import locais_routes

app = FastAPI(title="VeritasIA API")

# Libera o Vite (React) para conversar com a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173/2026-2-VeritasIA/"], # Porta padrão do Vite
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(locais_routes.router)