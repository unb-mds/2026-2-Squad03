# Arquitetura Hexagonal (Ports and Adapters)

## Visão Geral

A Arquitetura Hexagonal, também conhecida como *Ports and Adapters, é um padrão arquitetural proposto por **Alistair Cockburn* com o objetivo de desacoplar a lógica de negócio das tecnologias externas utilizadas pela aplicação.

Nessa abordagem, o núcleo da aplicação contém apenas as regras de negócio, enquanto as interações com bancos de dados, APIs, interfaces gráficas e serviços externos são realizadas por adaptadores conectados através de portas (ports).

---

## Objetivos

* Reduzir o acoplamento entre negócio e infraestrutura.
* Facilitar testes automatizados.
* Permitir substituição de tecnologias sem alterar regras de negócio.
* Melhorar a manutenibilidade e escalabilidade do sistema.

---

## Adaptação da Arquitetura Hexagonal

```python
                    +------------------+
                    |   Frontend       |
                    |  React + Vite    |
                    +--------+---------+
                             |
                             v
                    +------------------+
                    |     FastAPI      |
                    | (Adapter HTTP)   |
                    +--------+---------+
                             |
                             v
+--------------------------------------------------+
|                    Domínio                       |
|                                                  |
|  +--------------------------------------------+  |
|  | Casos de Uso                              |  |
|  +--------------------------------------------+  |
|                                                  |
|  +--------------------------------------------+  |
|  | Ports (Interfaces)                         |  |
|  +--------------------------------------------+  |
+--------------------------------------------------+
                             |
                             v
                    +------------------+
                    | Repositórios     |
                    | (Adapters)       |
                    +--------+---------+
                             |
                             v
                    Arquivos JSON
                             ^
                             |
                    +------------------+
                    |     Scrapers     |
                    | Scrapy/Playwright|
                    +------------------+
```

---

## Componentes

### Domínio

O domínio representa o núcleo da aplicação e contém:

* Regras de negócio.
* Casos de uso.
* Entidades.
* Interfaces (Ports).

O domínio não conhece tecnologias externas, frameworks ou bancos de dados.

---

### Ports

As portas definem contratos de comunicação entre o domínio e o mundo externo.

O domínio utiliza apenas a interface, sem conhecer sua implementação.

---

### Adapters

Os adaptadores implementam as portas definidas pelo domínio.

Exemplos:

* FastAPI (API REST)
* Banco de Dados

---

## Estrutura do Projeto

```python
📁 2026-2-VeritasIA
├── .github
│   └── workflows
│       └── deploy.yml
├── backend
│   ├── app
│   │   ├── adapters
│   │   │   ├── api_adapter
│   │   │   │   ├── _init_.py
│   │   │   │   ├── auth_routes.py
│   │   │   │   └── locais_routes.py
│   │   │   ├── db_adapter.py
│   │   │   └── json_adapter.py
│   │   ├── domain
│   │   │   └── entities.py
│   │   ├── ports
│   │   │   └── repository_port.py
│   │   ├── _init_.py
│   │   ├── database.py
│   │   └── main.py
│   ├── scrapers
│   └── _init_.py
├── docs
│   ├── backend
│   │   └── scrapy
│   │       ├── scrapyBaseG1.md
│   │       └── ScrapyMetropoles.md
│   ├── mkdocs
│   │   ├── docs
│   │   │   ├── assets
│   │   │   │   ├── Logo.png
│   │   │   │   ├── LogoBlack.png
│   │   │   │   └── texto.png
│   │   │   ├── backend
│   │   │   ├── dashboard
│   │   │   ├── frontend
│   │   │   ├── overrides
│   │   │   │   └── main.html
│   │   │   ├── productivity
│   │   │   ├── projeto
│   │   │   ├── stylesheets
│   │   │   │   └── extra.css
│   │   │   ├── api.md
│   │   │   ├── Backend.md
│   │   │   ├── FastAPI.md
│   │   │   ├── index.md
│   │   │   ├── LangChain.md
│   │   │   ├── openapi.json
│   │   │   ├── React.md
│   │   │   ├── Requisitos.md
│   │   │   ├── Scrapy.md
│   │   │   └── sobrenos.md
│   │   ├── overrides
│   │   └── mkdocs.yml
│   ├── projeto
│   │   ├── product-backlog.md
│   │   ├── retrospective.md
│   │   ├── roadmap.md
│   │   ├── sprint0.md
│   │   ├── sprint1.md
│   │   ├── sprint2.md
│   │   ├── sprint3.md
│   │   └── team.md
│   └── deploy.md
├── frontend
│   ├── components
│   ├── docs
│   │   ├── projeto
│   │   │   ├── Frontend.md
│   │   │   ├── github-pages.md
│   │   │   ├── particip-frontend.md
│   │   │   ├── product-backlog.md
│   │   │   ├── retrospective.md
│   │   │   ├── roadmap.md
│   │   │   ├── sprint0.md
│   │   │   ├── sprint1.md
│   │   │   ├── sprint2.md
│   │   │   ├── sprint3.md
│   │   │   └── team.md
│   │   └── auth-frontend.md
│   ├── public
│   ├── src
│   │   ├── assets
│   │   │   ├── logo.png
│   │   │   └── react.svg
│   │   ├── components
│   │   │   ├── AuthPrompt.jsx
│   │   │   ├── LatestNews.jsx
│   │   │   ├── NewsChart.jsx
│   │   │   ├── RegionChart.jsx
│   │   │   ├── Sidebar.jsx
│   │   │   ├── StatCard.jsx
│   │   │   └── TopVehicles.jsx
│   │   ├── pages
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Home.jsx
│   │   │   ├── Login.jsx
│   │   │   ├── Mapa.jsx
│   │   │   ├── Noticias.jsx
│   │   │   └── Sobre.jsx
│   │   ├── App.css
│   │   ├── App.jsx
│   │   ├── index.css
│   │   └── main.jsx
│   ├── eslint.config.js
│   ├── index.html
│   ├── package-lock.json
│   ├── package.json
│   ├── postcss.config.js
│   ├── tailwind.config.js
│   └── vite.config.js
├── scrapers
│   ├── resultados
│   └── spiders
├── .gitignore
├── banco_usuarios.json
├── gerar_arvore.py
├── LICENSE
├── package-lock.json
├── package.json
├── README.md
└── requirements.txt
```


## Benefícios para o Projeto

* Facilidade para substituir JSON por banco de dados futuramente.
* Possibilidade de trocar FastAPI sem alterar a lógica de negócio.
* Testes unitários independentes de infraestrutura.
* Melhor organização do código.
* Maior reutilização dos componentes de domínio.

---