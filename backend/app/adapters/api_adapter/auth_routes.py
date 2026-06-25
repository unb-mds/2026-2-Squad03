from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.app.database import get_db

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

router = APIRouter(
    prefix="/auth",
    tags=["Autenticação"]
)

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

# 📑 Criamos Schemas do Pydantic para a rota usar (em vez de usar a Entidade de Domínio Puro)
class LoginRequest(BaseModel):
    email: str
    senha: str

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

class AuthResponse(BaseModel):
    id: int
    nome: str
    email: str
    token: str  # Caso use JWT futuramente

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

    class Config:
        from_attributes = True # Permite ler objetos normais do Python

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

# 🚀 A rota agora usa "response_model=AuthResponse" (Pydantic) e NÃO a entidade pura
@router.post("/login", response_model=AuthResponse)
def login(dados: LoginRequest, db: Session = Depends(get_db)):
    # Sua lógica de autenticação aqui...
    
    # Exemplo de retorno simulado (que bate com o AuthResponse)
    return {
        "id": 1,
        "nome": "Usuário Teste",
        "email": dados.email,
        "token": "token-falso-de-teste"
    }
    
#+-------------------------------------------++-------------------------------------------++-------------------------------------------+