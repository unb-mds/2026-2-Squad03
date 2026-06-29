"""
Adaptador de repositório para o banco de dados PostgreSQL.

Este módulo implementa o Padrão de Repositório (Repository Pattern), uma técnica 
de arquitetura de software que separa a lógica de acesso a dados (SQLAlchemy) 
das regras de negócio da aplicação (rotas/FastAPI).

Informações Úteis:
    - Desacoplamento: As rotas não precisam saber como o SQLAlchemy funciona; 
      elas apenas invocam métodos do adaptador. Isso facilita a troca futura de 
      tecnologia de persistência.
    - Gerenciamento de Transações: O adaptador assume a responsabilidade de 
      `commit`, garantindo que as operações sejam atômicas.
"""

from sqlalchemy.orm import Session
from backend.app.models import UsuarioModel, RegiaoModel, NoticiaModel

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

class PostgresRepositoryAdapter:
    """
    Classe adaptadora (Repository) para manipulação de dados no PostgreSQL.

    Encapsula as operações de CRUD (Create, Read, Update, Delete), abstraindo 
    a complexidade do SQLAlchemy e expondo métodos de negócio intuitivos.

    Attributes:
        db (Session): Sessão ativa do SQLAlchemy injetada para persistência.
    """

    def __init__(self, db: Session):
        """
        Inicializa o adaptador com uma sessão de banco de dados ativa.

        Args:
            db (Session): Instância de sessão conectada ao pool de conexões do Supabase.
        """
        self.db = db

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+

    def salvar_usuario(self, user_data: dict) -> bool:
        """
        Persiste um novo registro de usuário na tabela de usuários.

        Converte um dicionário de dados (DTO) para o modelo ORM (`UsuarioModel`), 
        efetuando a inserção atômica no banco de dados.

        Args:
            user_data (dict): Dicionário contendo as credenciais.
                Chaves esperadas: 'nome', 'email', 'senha'.

        Returns:
            bool: Retorna `True` se a transação for commitada com sucesso.

        Raises:
            sqlalchemy.exc.SQLAlchemyError: Pode levantar exceções de integridade 
                (ex: e-mail duplicado) se houver violação de constraints no banco.
        """
        # 1. Mapeamento do dicionário para a entidade ORM
        novo_usuario = UsuarioModel(
            nome=user_data.get("nome"),
            email=user_data.get("email"),
            senha=user_data.get("senha")
        )
        
        # 2. Adição à fila de transações da sessão
        self.db.add(novo_usuario)
        
        # 3. Execução física no PostgreSQL
        self.db.commit()
        
        return True

#+-------------------------------------------++-------------------------------------------++-------------------------------------------+