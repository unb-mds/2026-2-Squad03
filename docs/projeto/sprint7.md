# Sprint 7

## Período

<<<<<<< HEAD
07/05/2026
=======
18/06/2026
>>>>>>> main

---

## Objetivo da sprint

<<<<<<< HEAD
Definição da arquitetura híbrida do sistema e estruturação do pipeline de processamento de inteligência artificial.
=======
implementação de funcionalidades restantes

>>>>>>> main

---

## Issues relacionadas

<<<<<<< HEAD
1. Estudo e Definição da Arquitetura de Software (Hexagonal, EDA e MVC) #15
1. Planejamento do Pipeline de Dados (Scraper -> IA -> Banco de dados) #18
1. Prototipagem funcional da Página Inicial e Sistema de Cadastro #20

=======
1. [Backend/ Scrapy] Arrumar Bot Scrapy #40
1. [Backend/ LangChain] Implementação da LLM #41
1. [Front / Prototipagem] Tela de Noticia #42
1. [Front / Prototipagem] Tela "Sobre Nós" #43
1. [Backend / FastApi ] Criação das rotas que falta #44
1. [Backend / Banco de Dados] Criação do Banco de Dados #45
1. [Documentação] Web-Scrapy e seu Workflow #48
>>>>>>> main
---

## Atividades realizadas

<<<<<<< HEAD
- Definição da Arquitetura Híbrida: Decisão pela utilização de Arquitetura Hexagonal (Portas e Adaptadores) no backend para isolar a lógica de domínio (critérios de feminicídio) e Arquitetura Orientada a Eventos (EDA) para o fluxo assíncrono de dados.
- Pipeline de IA: Planejamento do fluxo onde o scraper gera a informação, o Redis atua como broker e o backend processa via LangChain e Gemini para salvar os dados finais no PostGIS.
- Padronização Técnica: Estabelecimento da PEP 8 como a convenção oficial para escrita de código e documentação em Python.
- Evolução do Scraper: Início da implementação para extração do conteúdo integral das notícias (título, subtítulo e corpo) visando evitar perda de contexto para a IA.
- Design Sensível ao Trauma: Decisão arquitetural de incluir um sistema de cadastro para gerenciar notificações e filtrar conteúdos sensíveis para as usuárias.

=======
- Fialização do scrapy
- Fialização parcial da LLM
- Criação do Banco de Dados
- Correções necessarias
- Melhora do Doc do Scrapy
>>>>>>> main
---

## Entregas da sprint

<<<<<<< HEAD
- Documentação de Arquitetura: Definição formal dos padrões técnicos que guiarão o desenvolvimento das Releases.
- Estrutura de Pastas: Organização inicial do repositório backend seguindo o modelo de portas e adaptadores.
- Protótipo de Navegação: Fluxograma do site no Figma incluindo o dashboard e a área de login.

=======
- Pull request "Refactor/web scraping - Correção do github action. issue #40"
- Pull request "Implementação do LangChain para realização de: Resumo, coleta de local e segunda verificação de feminicidio. Issue #41"
- Banco de Dados Funcional
>>>>>>> main
---

## Evidências

<<<<<<< HEAD
- Decisões registradas em reunião: Transcrições detalhando a escolha de tecnologias como FastAPI e Leaflet.js.
- Repositório estruturado: Criação dos arquivos base do sistema no GitHub.
- Fluxograma do Pipeline: Documento técnico validando o caminho da notícia desde a raspagem até a plotagem no mapa.
=======
- Issues fechadas no GitHub 
- Pull requests realizados
>>>>>>> main
