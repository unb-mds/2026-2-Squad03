# Sprint 10

## Período

21/05/2026

---

## Objetivo da sprint

Finalização das interfaces do Frontend, integração da Inteligência Artificial (LLM) e preparativos para o deploy da Release 1.

---

## Issues relacionadas

1. Finalização das telas: Lista de Notícias, Detalhes, Dashboard e Mapa #42
1. Refatoração do Scraper para coleta de conteúdo integral #45
1. Configuração de rotas e testes de integração com Supabase/PostGIS #48
1. Estudo e viabilidade de deploy via Render e GitHub Pages #50

---

## Atividades realizadas

- Frontend e Design: Implementação das rotas de navegação e design das páginas de Lista de Notícias e Dashboard. Foi sugerido o uso de Wireframes no Figma para alinhar o layout final e evitar retrabalho.
- Evolução do Scraper: Decisão técnica de salvar o texto completo das notícias (título, subtítulo e corpo) no banco de dados para facilitar o processamento posterior pela IA e garantir a integridade dos dados.
- Refinamento da IA: O campo de "análise de sentimento" foi descartado por ser considerado subjetivo e custoso em termos de tokens, focando a LLM apenas em resumos factuais e filtragem de gatilhos.
- Infraestrutura e Banco de Dados: Configuração do banco de dados na nuvem via Supabase com a extensão PostGIS habilitada para consultas espaciais (ex: crimes num raio de X km).
- Metodologia de Testes: Estabelecimento da meta de 90% de cobertura de testes automatizados e definição do processo de revisão de código, onde um membro que não escreveu o código deve validar o Pull Request.

---

## Entregas da sprint

- Base de Dados Operacional: Instância do Supabase configurada com tabelas de usuários, notícias e regiões.
- Dataset Refatorado: Coleta de notícias padronizada com conteúdo integral para alimentação do pipeline de IA.
- Integração Frontend-Backend: Scripts iniciais de requisição JSON para comunicação entre as views do frontend e as rotas da API.

---

## Evidências

- Transcrição da Reunião 10: Registro detalhado das decisões técnicas e distribuição de tarefas para a reta final [26, Histórico da Conversa].
- Logs de Integração: Testes de conexão bem-sucedidos entre o backend FastAPI e o Supabase.
- GitHub Issues: Registro de progresso e encerramento de tarefas críticas para a Release 1.