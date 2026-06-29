# Visão Geral do Backend (FastAPI)

O backend do projeto **VeritasIA** foi construído utilizando o framework **FastAPI**, escolhido por sua alta performance, facilidade de uso e suporte nativo a operações assíncronas e documentação automática (Swagger/OpenAPI).

A arquitetura do nosso backend segue princípios de separação de responsabilidades, garantindo que a lógica de negócio, a persistência de dados e a exposição de APIs sejam módulos distintos e acopláveis.

---

## Estrutura da Arquitetura

O sistema é organizado para facilitar a manutenção e a escalabilidade:

1. **Camada de Modelos (ORM):** Gerenciada pelo SQLAlchemy, mapeia nossas entidades de banco de dados (`Usuario`, `Regiao`, `Noticia`) para objetos Python.
2. **Camada de Schemas (Pydantic):** Garante a validação de dados de entrada e serialização de saída, funcionando como um contrato entre o cliente (frontend) e o backend.
3. **Camada de Adaptadores:** Implementa o *Repository Pattern*, isolando as interações com o banco de dados (seja Postgres via SQLAlchemy ou mocks em JSON).
4. **Camada de Rotas (Routers):** Expondo os endpoints da API, organizados por domínio (Auth, Dashboard, Mapa, Notícias).



---

## Fluxo de uma Requisição

Quando uma requisição chega ao VeritasIA, o fluxo segue este caminho:

* **Requisição HTTP** -> **FastAPI Router** (Validação via Pydantic) -> **Adaptador** (Persistência/Consulta no Banco) -> **Resposta HTTP**.

### Componentes Principais

| Componente | Função |
| :--- | :--- |
| `database.py` | Configuração da `engine` e conexão com o Supabase/PostgreSQL. |
| `main.py` | Inicialização da app, CORS e agregação de todos os `routers`. |
| `models.py` | Definição das tabelas e relacionamentos espaciais (PostGIS). |
| `adapters/` | Repositórios que executam as queries (SQLAlchemy). |
| `schemas/` | Contratos de dados (Request/Response). |

---

## Como rodar o ambiente

Para garantir que o backend esteja operando corretamente, certifique-se de:

1. **Configurar o `.env`:** O arquivo deve conter a `DATABASE_URL` correta para o Supabase.
2. **Instalar dependências:** Utilize `pip install -r requirements.txt`.
3. **Execução:** Utilize o comando `uvicorn backend.app.main:app --reload`.

*A rota raiz (`/`) do sistema realiza automaticamente um teste de infraestrutura ao ser acessada, verificando a conexão com o banco e a criação das tabelas necessárias.*