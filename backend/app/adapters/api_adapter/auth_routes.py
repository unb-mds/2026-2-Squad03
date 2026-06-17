from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.domain.entities import UserAuth
from backend.app.database import get_db
from backend.app.adapters.db_adapter import PostgresRepositoryAdapter # Alterado de JsonRepositoryAdapter para PostgresRepositoryAdapter

router = APIRouter(prefix="/api/auth", tags=["Autenticação"])

@router.post("/register")
def registrar(user: UserAuth, db: Session = Depends(get_db)):
    # 1. Instancia o adaptador passando a sessão ativa do Postgres
    repo = PostgresRepositoryAdapter(db) #@
    
    try:
        # 2. Executa o salvamento
        sucesso = repo.salvar_usuario(user.dict())
        return {"status": "success" if sucesso else "error"}
    except Exception as e:
        # Se o e-mail já existir, o Postgres vai lançar um erro devido à regra UNIQUE
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este e-mail já está cadastrado."
        )

@router.post("/login")
def login(user: UserAuth, db: Session = Depends(get_db)):
    # O login precisará de uma lógica para buscar o usuário por e-mail e checar a senha,
    # que faremos assim que você quiser expandir essa rota!
    return {"status": "success"}