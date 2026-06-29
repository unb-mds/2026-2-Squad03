"""
Rotas de autenticação da API.

Este módulo gerencia os endpoints relacionados à segurança e controle de acesso,
atuando como a camada de entrada para validação de credenciais de usuários e 
emissão de tokens de sessão (JWT/Session).

Informações Úteis:
    - Validação: Utiliza Schemas Pydantic para garantir que o payload de login 
      esteja no formato correto antes mesmo de atingir a lógica de negócio.
    - Segurança: A estrutura foi desenhada para suportar JWT (JSON Web Tokens), 
      facilitando a integração futura com autenticação stateless.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.app.database import get_db

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

# Roteador do FastAPI dedicado aos endpoints de autenticação.
router = APIRouter(
    prefix="/auth",
    tags=["Autenticação"]
)

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

class LoginRequest(BaseModel):
    """
    Schema de validação para a requisição de login.

    Define os dados que o cliente precisa enviar no corpo da requisição (payload)
    para acessar o sistema.

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

    Define a estrutura dos dados que serão retornados ao cliente após a 
    validação bem-sucedida das credenciais.

    Attributes:
        id (int): Identificador único do usuário logado.
        nome (str): Nome do usuário cadastrado.
        email (str): E-mail do usuário.
        token (str): Token de acesso para autenticar requisições futuras.
    """
    id: int
    nome: str
    email: str
    token: str

    class Config:
        """
        Configurações adicionais do Pydantic.
        """
        # Permite que o Pydantic leia atributos de objetos de classe (SQLAlchemy),
        # essencial para converter modelos ORM em JSON.
        from_attributes = True 

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

@router.post("/login", response_model=AuthResponse)
def login(dados: LoginRequest, db: Session = Depends(get_db)) -> dict:
    """
    Endpoint para autenticação de usuários.

    Recebe as credenciais (e-mail e senha) através do corpo da requisição, 
    valida essas informações (camada de lógica) e retorna os dados do usuário 
    autenticado junto com um token de acesso.

    Args:
        dados (LoginRequest): O objeto Pydantic contendo email e senha validados.
        db (Session, optional): Sessão do banco de dados injetada automaticamente 
            pelo FastAPI.

    Returns:
        dict: Um dicionário estruturado seguindo o schema `AuthResponse`, 
            contendo informações do perfil e o token de autenticação.
    """
    # [TODO] Implementar verificação de hash de senha contra o banco de dados
    
    # Exemplo de retorno simulado para testes integrados com o frontend
    return {
        "id": 1,
        "nome": "Usuário Teste",
        "email": dados.email,
        "token": "token-falso-de-teste"
    }
    
#+-------------------------------------------++-------------------------------------------++-------------------------------------------+