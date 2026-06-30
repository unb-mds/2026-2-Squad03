# Testes de Integração (PostgreSQL/Supabase)

Esta seção documenta a suíte de testes de integração do **VeritasIA**. Diferente dos testes unitários (que utilizam *Mocks*), esta suíte valida a comunicação real do backend com o banco de dados PostgreSQL.

Ela garante o funcionamento correto de *queries* complexas, agrupamentos (`GROUP BY`), funções espaciais do PostGIS (`ST_AsGeoJSON`) e o comportamento de *case-insensitivity* (`ILIKE`) diretamente no motor do banco de dados.

## 📊 Relatório de Execução (Última Run)

* **Total de Testes:** 4
* **Falhas / Erros:** 0 / 0
* **Taxa de Sucesso:** 100%
* **Tempo de Execução:** 52.483 segundos
* **Data da Execução:** 30/06/2026

---

## 🛠️ Infraestrutura de Isolamento (Conftest)

O arquivo `conftest.py` na camada de integração resolve o desafio de testar em um banco de dados real na nuvem (Supabase) sem afetar os dados de produção. 

Foi adotado o recurso `schema_translate_map` do SQLAlchemy. Ele intercepta e reescreve a SQL gerada pelo ORM, redirecionando todas as leituras e escritas para um schema temporário (ex: `test`), totalmente ignorando problemas de configuração de sessão (como o `search_path`) que falham ao utilizar Transaction Poolers como o PgBouncer.

::: backend.tests.integration.conftest
    options:
      show_root_heading: false
      show_source: true
      heading_level: 3

---

## 🧪 Casos de Teste (Dashboard e Mapa)

Aqui estão documentados os testes que enviam *queries* reais para validação de dados em ambiente de banco de dados.

::: backend.tests.integration.test_dashboard_integration
    options:
      show_root_heading: false
      show_source: false
      heading_level: 3