## Sobre o Projeto

VeritasIA é um projeto de código aberto projetado para coletar notícias de canais oficiais sobre casos de feminicídio no território brasileiro. O projeto visa unificar todas as informações retiradas dos mesmos em um só local, com o intuito de entregar uma visão clara sobre a realidade da violência contra a mulher no país, promovendo informações mais acessíveis e dados brutos sobre o abuso, gerando resumos e quantidades de notícias coletadas, própicias para o uso de jornalistas ou especialistas no assunto.

<img width="1898" height="864" alt="image" src="https://github.com/user-attachments/assets/97a9b48b-62a5-4c2b-8fed-d2dcc4828e94" />

---
## Funcionalidades

- **Coleta de Notícias**: Notícias são coletadas por quatro canais de notícias e filtradas por "feminicídio".
- **Geração de Resumos**: As notícias coletadas são enviadas para a `Large Language Model` (LLM) onde ocorre o respectivo resumo.
- **Geolocalização Apróximada**: É disponibilizado um mapa com localizações apróximadas das nóticias coletadas.
    - **Mapa de Calor**: Mapa de calor com regiões com casos mais recorrentes.
- **Visualização da Nóticia**: Aba com todas as notícias coletadas pelo site, onde é disponibilizada seu respectivo resumo para evitar plágio, e vinculação dos URLs oficiais.
- **Código Aberto**: Todo o projeto é desenvolvido de forma transparente, sendo possível a participação da comunidade.

---
## Público Alvo

O projeto visa unificar e permitir uma melhor visualização dessas notícias por meio de quantidade e dados em geolocalização, com um público principal em mente:

1. **Jornalistas**: Profissionais de jornalismos que tem necessidade de coletar quantidades de casos e regiões mais recorrentes de feminicídio dentro do Brasil, além de um breve resumo sobre o acontecido.

---
## Portais Utilizados

1. **G1**
2. **Metrópoles**
3. **R7**
4. **CNN**

---
## Tecnologias Utilizadas

- **MkDocs:** Utilizado para expor toda a documentação necessária para a utilização ou entendimento do site.
- **Frontend:** Aplicações WEB utilizada para realização dos prótotipos feitos para o projeto. Vale salientar que, na navegação desta página existe: **Prototipagem**, onde pode ser visto detalhadamente todos os prótotipos realizados.
- **React:** biblioteca JavaScript de código aberto focada em criar interfaces de usuário (UI) para aplicações web e mobile.
- **Vite:** é uma ferramenta de construção e servidor de desenvolvimento para aplicações web.
- **Tailwind CSS:** é uma distribuição do sistema operacional Linux focada em privacidade e anonimato.

### Backend

- **Scrapy:** Framework utilizado para realizar Web-raspagem em sites.
- **LangChain:** Framework de código aberto projetado para facilitar a criação de aplicativos usando Modelos de Linguagem (LLMs)
- **Playwright:** Framework utilizado para realizar Web-raspagem em sites. Diferença entre **Scrapy** é que o Playwright consegue simular uma pessoa física acessando o site, dessa forma, não é limitado aos setores "Estáticos" da página.
- **FastAPI:** Framework web moderno e de altíssimo desempenho para a construção de APIs com Python.

### Banco de Dados

- **PostgreSQL:**: Sistema de gerenciamento de banco de dados (SGBD) de código aberto.

### Automação

- **GitHub Actions:** Automação integrada ao GitHub que permite criar fluxos de trabalhos, que é denominado de: "workflows".
