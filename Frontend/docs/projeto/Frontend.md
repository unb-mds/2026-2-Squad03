# Frontend - VeritasIA

## Objetivo

Desenvolver a interface visual da aplicação VeritasIA seguindo o protótipo definido no Figma.

## Tecnologias

- React
- Vite
- CSS
- GitHub Pages

## Estrutura

O frontend está organizado na pasta `Frontend`.

Componentes iniciais:

- `Sidebar`: menu lateral da aplicação
- `StatCard`: card reutilizável para métricas
- `App`: estrutura principal do dashboard

## Páginas planejadas

- Home
- Login
- Cadastro
- Dashboard
- Notícias
- Mapa
- Sobre Nós

## Decisões iniciais

A implementação foi iniciada pelo Dashboard por ser a tela principal da aplicação.  
Os componentes foram separados para facilitar manutenção, reaproveitamento e evolução futura.

## Atualização 24/05/2026

## Objetivo

Implementar a estrutura inicial do frontend da aplicação VeritasIA, com foco no dashboard principal, navegação entre páginas, deploy e organização do código em componentes reutilizáveis.

## Implementações realizadas

### Estrutura do frontend

- Configuração do projeto com React + Vite
- Organização da pasta `Frontend`
- Configuração de rotas com React Router
- Ajuste da rota inicial para carregar o Dashboard
- Configuração do GitHub Pages
- Uso de HashRouter para compatibilidade com deploy

### Dashboard

- Criação do layout principal
- Implementação da sidebar
- Cards de métricas
- Área de gráfico temporal
- Área de distribuição por estado
- Top veículos
- Notícias por região
- Últimas notícias
- Correção da ocupação total da tela

### Componentização

- `Sidebar`
- `StatCard`
- `NewsChart`
- `TopVehicles`
- `RegionChart`
- `LatestNews`
- `AuthPrompt`

### Interatividade

- Modal inicial sugerindo login/cadastro
- Opção de continuar sem cadastro
- Fechamento do modal com botão
- Fechamento do modal ao clicar fora
- Uso de `useState`

### Visualização de dados

- Instalação e uso da biblioteca Recharts
- Criação do gráfico temporal de notícias

### Responsividade

- Ajustes iniciais para diferentes tamanhos de tela
- Correção de largura do dashboard
- Remoção da área de filtros e centralização do filtro por data no header

### Documentação

- Documentação do frontend
- Documentação do deploy
- Registro de participação
- Organização inicial da sprint

## Tecnologias utilizadas

- React
- Vite
- React Router DOM
- Recharts
- CSS
- GitHub Pages

## Critérios de aceite

- [x] Dashboard acessível na rota inicial
- [x] Rotas funcionando
- [x] Modal de login/cadastro funcional
- [x] Gráfico temporal implementado
- [x] Componentes separados
- [x] Deploy configurado
- [x] Layout ocupando a tela corretamente
- [x] Documentação inicial criada

## Próximos passos

- Criar telas completas de Login e Cadastro
- Implementar mapa real do Brasil
- Melhorar responsividade mobile
- Integrar dados reais futuramente
