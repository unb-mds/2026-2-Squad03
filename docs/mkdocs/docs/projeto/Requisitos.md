# Não Funcionais

- Design Sensível ao Trauma: Reconhecer que os usuários podem ser vítimas e que certas informações podem servir de gatilho. Incluir botões de “saída rápida” e avisos de conteúdo.

- Arquitetura Assíncrona: Backend em FastAPI, para gerenciar múltiplas requisições e processamento de IA sem travamentos.

- Acessibilidade: Conformidade com as normas WCAG.

# Funcionais

- Coleta Automatizada: Coletar notícias diariamente de pelo menos 2 portais de notícias

- Indexar noticias com busca textual e filtros

- Mapa Interativo*: Mapa com geolocalização

- Auditoria: Fornecer link da fonte original para cada caso registrado.

- Filtro com dia/semana/mês da postagem da noticia

- Processamento de IA: Classificar notícia e extrair informações (data, local, idade da vítima e agressor)

- Sumarização Factual: Gerar resumos objetivos consolidando e identificando várias fontes para o mesmo crime.

- Opção de fazer o login para poder receber notificações

- média diaria de nóticias coletadas

- todas as nóticias coletadas que tratam sobre feminicidio

# Product Backlog

## Objetivo do produto

Desenvolver uma plataforma que reúna notícias, estatísticas e dados sobre casos de feminicídio no Brasil, permitindo visualização clara e acessível para qualquer usuário.

---

| ID   | User Story                                                | Prioridade | Status       |
| ---- | --------------------------------------------------------- | ---------- | ------------ |
| US01 | Como desenvolvedor, quero que o sistema realize a raspagem diária de grandes portais (G1, Metrópoles) e fontes regionais para que nenhuma ocorrência pública seja perdida.| Alta       | Concluido   |
| US02 | Como jornalista, quero ler um resumo objetivo e consolidado de um crime (mesmo que vindo de múltiplas fontes) para agilizar meu processo investigativo     | Alta       | Pendente|
| US03 | Como usuário, quero navegar por uma interface intuitiva   | Alta       | Pendente |
| US04 | Como usuário, quero consultar fontes oficiais             | Alta       | Pendente     |
| US05 | Como usuário, quero filtrar informações por estado/região | Média      | Pendente     |
| US06 | Como usuário, quero acompanhar dados atualizados          | Média      | Pendente     |
| US07 | Como pesquisador, quero visualizar os crimes em um mapa interativo para identificar a distribuição geográfica e tendências regionais da violência.          | Média      | Pendente     |
| US08 | Como uma vítima sob vigilância doméstica, quero um botão de "Saída Rápida" para que eu possa ocultar minha navegação instantaneamente em caso de risco.          | Média      | Pendente     |
| US09 | Como usuário sensível, quero receber um aviso antes de ler detalhes de casos pesados para decidir se estou emocionalmente apto a consumir aquela informação.        | Média      | Pendente     |
| US10 | Como membro do time, quero que o código seja testado e implantado automaticamente para garantir que melhorias cheguem ao público sem erros manuais.         | Média      | Pendente     |
| US11 | Como usuário recorrente quero poder receber notificação quando uma nova noticia for postada        | Média      | Pendente     |

---

<iframe style="border: 1px solid rgba(0, 0, 0, 0.1);" width="800" height="450" src="https://embed.figma.com/board/TERK5u1cdCHQBJgRb3m2x5/Squad-03?node-id=0-1&embed-host=share" allowfullscreen></iframe>