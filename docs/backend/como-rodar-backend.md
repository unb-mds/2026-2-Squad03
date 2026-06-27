# Guia de Execução do Backend

Este documento detalha o processo para configurar o ambiente de desenvolvimento local, instalar as dependências e executar o servidor **FastAPI** do projeto VeritasIA.

---

## 1. Preparação do Diretório

Certifique-se de que você está na raiz da pasta `backend` no seu terminal para que os caminhos de importação e as variáveis de ambiente sejam carregados corretamente.

```bash

cd backend

2. Configuração do Ambiente Virtual
É fundamental isolar as dependências do projeto para evitar conflitos de versões.
=== "Linux / macOS" bash python -m venv .venv source .venv/bin/activate 
=== "Windows (PowerShell/CMD)" bash python -m venv .venv .venv\Scripts\activate 
!!! tip "Dica de Editor" No VS Code, após ativar o ambiente virtual, pressione Ctrl+Shift+P, digite Python: Select Interpreter e selecione o executável que aponta para a pasta .venv.
3. Configuração de Variáveis de Ambiente
O backend utiliza o arquivo .env para gerenciar segredos e conexões de banco de dados, como o Supabase.

    Na raiz da pasta /backend, crie um arquivo chamado .env.
    Adicione a sua URL de conexão seguindo o modelo abaixo:

DATABASE_URL=postgresql://postgres:[SENHA]@db.[ID_PROJETO].supabase.co:5432/postgres

4. Instalação das Dependências
Com o ambiente virtual ativado, instale as bibliotecas necessárias para a API, banco de dados e geolocalização:

pip install "fastapi[standard]" sqlalchemy psycopg2-binary geoalchemy2 pydantic python-dotenv

5. Execução do Servidor
O servidor principal está localizado em app/main.py. Utilize o comando CLI do FastAPI para o modo de desenvolvimento:

fastapi dev app/main.py

!!! info "Informação Técnica" O comando fastapi dev ativa o auto-reload, reiniciando o servidor automaticamente sempre que um arquivo for alterado. Caso prefira o método tradicional, utilize: uvicorn app.main:app --reload
6. Documentação e Testes da API
Uma das grandes vantagens do FastAPI é a geração automática de documentação interativa baseada em Swagger:

    Swagger UI (Interativo): http://127.0.0.1:8000/docs
    ReDoc (Estruturado): http://127.0.0.1:8000/redoc

Pela interface do Swagger, você pode testar endpoints como GET /noticias/ ou GET /mapa/ sem precisar do frontend.
7. Códigos de Resposta Comuns
Ao integrar com o frontend (React/Vite), monitore os seguintes status no console:
Código
	
Descrição
	
Motivo Comum
200
	
OK
	
Requisição concluída com sucesso.
201
	
Created
	
Novo registro salvo no Supabase.
404
	
Not Found
	
Notícia ou ID não localizado.
422
	
Unprocessable Entity
	
Erro de validação no JSON enviado (Pydantic).
500
	
Internal Error
	
Falha de conexão com o banco ou erro no servidor.


### Instruções para Adição no MkDocs:
Para que este arquivo apareça no menu lateral do seu site de documentação, adicione-o ao arquivo `mkdocs.yml` na raiz do projeto:

```yaml
nav:
  - Home: index.md
  - Desenvolvimento:
      - Backend: backend.md
