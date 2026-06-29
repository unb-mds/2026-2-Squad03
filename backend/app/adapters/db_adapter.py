"""
Adaptador de repositório para o banco de dados PostgreSQL.

Este módulo implementa o Padrão de Repositório (Repository Pattern).
Seu objetivo é isolar a lógica de acesso a dados (SQLAlchemy) das regras de 
negócio (rotas/FastAPI). Ele fornece métodos simples e diretos para realizar
operações de CRUD no banco de dados.
"""

from sqlalchemy.orm import Session
from backend.app.models import UsuarioModel, RegiaoModel, NoticiaModel

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

class PostgresRepositoryAdapter:
    """
    Classe adaptadora para manipulação de dados no PostgreSQL.

    Encapsula as operações de banco de dados, recebendo uma sessão ativa 
    e executando as transações necessárias usando os modelos do SQLAlchemy.

    Attributes:
        db (Session): Sessão ativa do banco de dados injetada na inicialização.
    """

    def __init__(self, db: Session):
        """
        Inicializa o adaptador com uma sessão do banco de dados.

        Args:
            db (Session): Instância de sessão do SQLAlchemy conectada ao banco.
        """
        # O adaptador recebe a sessão ativa do banco de dados para trabalhar
        self.db = db

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

    def salvar_usuario(self, user_data: dict) -> bool:
        """
        Cria e salva um novo usuário no banco de dados.

        Recebe um dicionário com os dados do usuário, converte para o modelo 
        ORM correspondente (`UsuarioModel`), adiciona à sessão e realiza o commit 
        da transação.

        Args:
            user_data (dict): Dicionário contendo os dados do usuário.
                Espera-se as chaves 'nome', 'email' e 'senha'.

        Returns:
            bool: Retorna True após confirmar a transação (commit) com sucesso.
        """
        # 1. Transforma o dicionário vindo do FastAPI em um Objeto do banco
        novo_usuario = UsuarioModel(
            nome=user_data.get("nome"),
            email=user_data.get("email"),
            senha=user_data.get("senha")
        )
        # 2. Avisa o SQLAlchemy que queremos inserir esse objeto
        self.db.add(novo_usuario)
        # 3. Confirma a transação no PostgreSQL (executa o INSERT)
        self.db.commit()
        return True

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+