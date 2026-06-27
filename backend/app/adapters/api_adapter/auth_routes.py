"""
Rotas de autenticação da API.

Este módulo gerencia os endpoints relacionados à segurança e controle de acesso,
como a validação de credenciais de usuários e a emissão de tokens de sessão.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.app.database import get_db

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

router = APIRouter(
    prefix="/auth",
    tags=["Autenticação"]
)
"""Roteador do FastAPI dedicado aos endpoints de autenticação."""

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

# 📑 Criamos Schemas do Pydantic para a rota usar (em vez de usar a Entidade de Domínio Puro)
class LoginRequest(BaseModel):
    """
    Schema de validação para a requisição de login.

    Define os dados que o cliente precisa enviar no corpo da requisição (payload)
    para tentar acessar o sistema.

    Attributes:
        email (str): O endereço de e-mail do usuário.
        senha (str): A senha em texto plano fornecida pelo usuário.
    """
    email: str
    senha: str

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

class AuthResponse(BaseModel):
    """
    Schema de serialização para a resposta de autenticação.

    Define a estrutura dos dados que serão retornados ao cliente caso o login
    seja bem-sucedido.

    Attributes:
        id (int): Identificador único do usuário logado.
        nome (str): Nome do usuário.
        email (str): E-mail do usuário.
        token (str): Token de acesso (ex: JWT) para autenticar requisições futuras.
    """
    id: int
    nome: str
    email: str
    token: str  # Caso use JWT futuramente

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

    class Config:
        """Configurações adicionais do Pydantic."""
        from_attributes = True # Permite ler objetos normais do Python

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

# 🚀 A rota agora usa "response_model=AuthResponse" (Pydantic) e NÃO a entidade pura
@router.post("/login", response_model=AuthResponse)
def login(dados: LoginRequest, db: Session = Depends(get_db)):
    """
    Endpoint para autenticação de usuários.

    Recebe as credenciais (e-mail e senha) através do corpo da requisição, 
    valida essas informações (simulado) e retorna os dados do usuário junto 
    com um token de acesso.

    Args:
        dados (LoginRequest): O payload contendo email e senha.
        db (Session, optional): Sessão do banco de dados injetada automaticamente 
            pelo FastAPI.

    Returns:
        dict: Um dicionário compatível com `AuthResponse` contendo os dados do 
            usuário e o token gerado.
    """
    # Sua lógica de autenticação aqui...
    
    # Exemplo de retorno simulado (que bate com o AuthResponse)
    return {
        "id": 1,
        "nome": "Usuário Teste",
        "email": dados.email,
        "token": "token-falso-de-teste"
    }
    
#+-------------------------------------------++-------------------------------------------++-------------------------------------------+