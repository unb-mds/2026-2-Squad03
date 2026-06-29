# Rotas da API (Endpoints)

Esta seção centraliza a documentação de todos os endpoints da API do VeritasIA. As rotas são responsáveis por receber as requisições HTTP do frontend ou de serviços externos e orquestrar as respostas adequadas.

---

## Autenticação

Endpoints responsáveis por gerenciar o acesso de usuários à API, incluindo validação de credenciais e emissão de tokens.

::: backend.app.adapters.api_adapter.auth_routes
    options:
      show_root_heading: false
      show_source: true
      heading_level: 3
      show_if_no_docstring: true

---

## Dashboard

Endpoints encarregados de processar e compilar as métricas da aplicação, fornecendo dados analíticos (médias, totais e crescimento) para os gráficos do frontend.

::: backend.app.adapters.api_adapter.dashboard_routes
    options:
      show_root_heading: false
      show_source: true
      heading_level: 3
      show_if_no_docstring: true

---

## Mapa (GeoJSON)

Endpoints responsáveis por exportar os dados espaciais do sistema. Utiliza a extensão PostGIS para serializar as localizações em formato GeoJSON para plotagem no mapa.

::: backend.app.adapters.api_adapter.mapa_routes
    options:
      show_root_heading: false
      show_source: true
      heading_level: 3
      show_if_no_docstring: true

---

## Notícias

Endpoints dedicados à consulta do acervo de notícias. Permitem a listagem paginada para o feed principal e a busca detalhada por ID.

::: backend.app.adapters.api_adapter.noticias_routes
    options:
      show_root_heading: false
      show_source: true
      heading_level: 3
      show_if_no_docstring: true