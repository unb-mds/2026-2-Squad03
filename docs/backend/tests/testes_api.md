# Testes Unitários da API

Esta seção documenta a suíte de testes unitários do backend do **VeritasIA**. Os testes foram construídos utilizando o framework `pytest` e o `TestClient` do FastAPI, com foco no isolamento da camada de banco de dados através de *Mocking* pesado da sessão do SQLAlchemy.

## 📊 Relatório de Execução (Última Run)

Os testes automatizados garantem a estabilidade das rotas antes de qualquer *deploy*. Abaixo estão os resultados da última execução de validação:

* **Total de Testes:** 16
* **Falhas / Erros:** 0 / 0
* **Taxa de Sucesso:** 100%
* **Tempo de Execução:** 0.332 segundos
* **Data da Execução:** 30/06/2026

---

## Fixtures e Configurações (Conftest)

O arquivo `conftest.py` define a infraestrutura de testes, incluindo a intercepção da injeção de dependência (`get_db`) e a criação de *Mocks* inteligentes para a API fluente do SQLAlchemy, evitando erros de recursão.

::: backend.tests.conftest
    options:
      show_root_heading: false
      show_source: true
      heading_level: 3

---

## Fábricas de Dados (Factories)

Para manter os testes rápidos e determinísticos, utilizamos funções de fábrica que geram instâncias simuladas (fakes) dos modelos ORM, preenchendo os dados necessários para o Pydantic serializar as respostas corretamente.

::: backend.tests.factories
    options:
      show_root_heading: false
      show_source: true
      heading_level: 3

---

## Casos de Teste: Dashboard

Valida a lógica complexa de agregação do dashboard, garantindo que o cálculo de crescimento, market share de portais e filtros geográficos funcionem corretamente, mesmo com o banco de dados vazio.

::: backend.tests.test_dashboard_routes
    options:
      show_root_heading: false
      show_source: false
      heading_level: 3

---

## Casos de Teste: Mapa (GeoJSON)

Garante que os dados espaciais gerados pelo banco de dados (PostGIS) sejam serializados estritamente dentro do padrão internacional `FeatureCollection` do GeoJSON.

::: backend.tests.test_mapa_routes
    options:
      show_root_heading: false
      show_source: false
      heading_level: 3

---

## Casos de Teste: Notícias

Testes de integração de ponta a ponta na rota de listagem e busca individual, garantindo que relacionamentos (como Região) sejam aninhados corretamente no JSON e que recursos inexistentes retornem HTTP 404.

::: backend.tests.test_noticias_routes
    options:
      show_root_heading: false
      show_source: false
      heading_level: 3