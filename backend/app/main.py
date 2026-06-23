# backend/app/main.py


from backend.app.database import engine, Base
import backend.app.models as models

#comando pra criar no supabase as tables 
#Base.metadata.create_all(bind=engine)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Apenas importe os arquivos de rotas que você vai usar
from backend.app.adapters.api_adapter import auth_routes, noticias_routes , mapa_routes

app = FastAPI(title="VeritasIA API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registre os dois roteadores
app.include_router(noticias_routes.router)
app.include_router(mapa_routes.router)
app.include_router(auth_routes.router)

@app.get("/")
def home():
    return {"message": "Bem-vindo a API do VeritasIA!"}