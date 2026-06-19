# backend/app/main.py


#senha db = SenhaSecreta123


from backend.app.database import engine, Base
import backend.app.models as models

# Esse comando cria as tabelas no Supabase caso elas não existam lá ainda!
Base.metadata.create_all(bind=engine)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Apenas importe os arquivos de rotas que você vai usar
from backend.app.adapters.api_adapter import locais_routes, auth_routes 

app = FastAPI(title="VeritasIA API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registre os dois roteadores
#app.include_router(locais_routes.router)
app.include_router(auth_routes.router)