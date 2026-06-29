# Adaptadores (Adapters)

Esta seção centraliza a documentação de todos os adaptadores do projeto VeritasIA. O padrão de adaptadores é utilizado para isolar as regras de negócio da infraestrutura externa, como banco de dados e rotas da API.

---

## Adaptador de Banco de Dados (PostgreSQL)

Responsável por realizar as operações oficiais de banco de dados na nuvem utilizando SQLAlchemy.

::: backend.app.adapters.db_adapter
    options:
      show_root_heading: false
      show_source: true
      heading_level: 3
      show_if_no_docstring: true

---

## Adaptador JSON (Local/Mock)

Implementação alternativa para persistência de dados em arquivos `.json` locais, ideal para testes de desenvolvimento e ambientes onde o PostgreSQL não é necessário.

::: backend.app.adapters.json_adapter
    options:
      show_root_heading: false
      show_source: true
      heading_level: 3
      show_if_no_docstring: true

---

## Adaptadores de API (Rotas)

Responsável por registrar e rotear as requisições HTTP do FastAPI para os devidos controladores (Notícias, Mapa, Autenticação e Dashboard).

::: backend.app.adapters.api_adapter
    options:
      show_root_heading: false
      show_source: true
      heading_level: 3
      show_if_no_docstring: true