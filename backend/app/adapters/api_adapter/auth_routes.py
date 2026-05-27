# backend/app/adapters/api_adapter/auth_routes.py

from fastapi import APIRouter
from backend.app.domain.entities import UserAuth
from backend.app.adapters.json_adapter import JsonRepositoryAdapter

router = APIRouter(prefix="/api/auth", tags=["Autenticação"])

repo = JsonRepositoryAdapter()

@router.post("/register")
def registrar(user: UserAuth):
    print(f"Recebendo cadastro de: {user.email}")
    return {"message": "Sucesso", "data": repo.salvar_usuario(user.dict())}

@router.post("/login")
def login(user: UserAuth):
    return {"message": "Login realizado", "success": True}