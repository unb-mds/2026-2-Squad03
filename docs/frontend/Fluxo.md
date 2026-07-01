# Fluxo do Site

## Visão Geral

O fluxo da aplicação foi projetado para oferecer uma navegação intuitiva e eficiente, permitindo que o usuário acompanhe, analise e explore notícias relacionadas à violência contra a mulher. Todas as funcionalidades principais podem ser acessadas por meio do menu lateral, proporcionando uma experiência consistente durante toda a navegação.

O sistema é dividido em quatro módulos principais:

- Dashboard
- Mapa
- Notícias
- Sobre Nós

Cada módulo possui uma finalidade específica, permitindo que o usuário alterne entre diferentes formas de visualização dos dados sem perder o contexto da aplicação.

---

## Fluxo Geral da Navegação

```text
Página Inicial
      │
      ▼
 Dashboard
      │
 ┌────┼─────────────┐
 ▼    ▼             ▼
Mapa Notícias   Sobre Nós
      │
      ▼
Detalhes da Notícia
      │
      ▼
Notícia Original
```

---

# Dashboard

O Dashboard representa a tela principal da aplicação e funciona como um centro de monitoramento das notícias coletadas.

Ao acessar esta página, o usuário encontra um resumo completo dos dados disponíveis, incluindo indicadores gerais, gráficos estatísticos e uma lista das notícias mais recentes.

Entre as principais informações apresentadas estão:

- Quantidade total de notícias;
- Média diária de publicações;
- Comparativo com períodos anteriores;
- Evolução temporal das notícias;
- Distribuição por estados;
- Veículos de comunicação com maior número de publicações;
- Distribuição das notícias por região do Brasil;
- Lista das notícias mais recentes.

Além disso, o Dashboard disponibiliza filtros por período, estado e campo de pesquisa, permitindo localizar rapidamente informações específicas.

---

# Mapa

O módulo de Mapa permite visualizar a distribuição geográfica das notícias registradas.

O usuário pode alternar entre dois modos de visualização:

- Marcadores
- Mapa de Calor

Essa funcionalidade facilita a identificação das regiões com maior incidência de casos noticiados, oferecendo uma visão espacial dos dados coletados.

---

# Notícias

A tela de Notícias apresenta todas as publicações cadastradas no sistema em formato de cartões.

Cada notícia exibe informações como:

- Veículo responsável pela publicação;
- Título;
- Resumo;
- Local do ocorrido;
- Data da publicação;
- Categoria;
- Status de verificação.

Nesta tela, o usuário pode selecionar uma notícia para visualizar seu conteúdo completo.

---

## Visualização da Notícia

Ao selecionar uma notícia, o sistema direciona o usuário para uma página contendo todas as informações disponíveis sobre aquela publicação.

São apresentados:

- Título completo;
- Veículo de origem;
- Data;
- Local;
- Texto completo da notícia;
- Resumo da análise realizada pelo sistema.

Ao final da página existe um botão que permite acessar a notícia original publicada pelo veículo de comunicação.

Esse fluxo garante que o usuário possa consultar rapidamente as informações resumidas e, caso necessário, acessar a fonte oficial da notícia.

---

# Sobre Nós

A seção Sobre Nós apresenta informações institucionais sobre o projeto.

Seu objetivo é explicar a proposta da plataforma, sua motivação, seus objetivos e a equipe responsável pelo desenvolvimento.

Essa página aproxima o usuário do projeto e fornece contexto sobre a finalidade da aplicação.

---

# Fluxo do Usuário

O fluxo principal de utilização da plataforma ocorre da seguinte maneira:

1. O usuário acessa o Dashboard.
2. Analisa os indicadores e gráficos disponíveis.
3. Caso deseje explorar os dados geograficamente, acessa o módulo Mapa.
4. Se desejar consultar notícias específicas, navega até a tela Notícias.
5. Seleciona uma notícia para visualizar seus detalhes.
6. Caso queira aprofundar a leitura, acessa a notícia original através do link disponível.
7. A qualquer momento pode retornar ao Dashboard ou navegar para qualquer outro módulo utilizando o menu lateral.

---

# Considerações

O fluxo da aplicação foi desenvolvido para minimizar a quantidade de cliques necessários para acessar as informações mais importantes.

A navegação lateral permanece disponível em todas as páginas, permitindo que o usuário alterne rapidamente entre os módulos do sistema sem interromper sua análise.

A organização das telas prioriza a visualização de dados, a facilidade de navegação e o acesso rápido às notícias, proporcionando uma experiência simples, consistente e intuitiva.
