# GitHub Action - Workflow

VeritasIA está utilizando um workflow chamado ```execute-scrapy.yml``` para realizar a execução automatizado dos Scripts.

## Como funciona:

Esse workflow pode ser chamado de maneira manual ou esperando um ```Schedule``` que acontece diariamente às 23:55 no horário de Brasília.

A execução gera os mesmos resultados que foi explicado no ``` Scrapy```, no entanto, não sendo necessário a execução manual do mesmo.


### Como Testar

Vá na opção de Actions e execute o "executor scraper" selecionando a branch "Refactor/web scraping" como referencia.

<img width="1197" height="93" alt="image" src="https://github.com/user-attachments/assets/a91a7881-f1f4-4800-8991-ae523a6c3795" />

---

<img width="1839" height="946" alt="image" src="https://github.com/user-attachments/assets/e44e773c-9f9b-4ecf-8172-bc2ea93b827a" />

---

<img width="328" height="140" alt="image" src="https://github.com/user-attachments/assets/986e8873-63b5-4918-a0d0-876d0690926e" />


---

#### Resultado Esperado

Commit realizado no caminho "scrapers/resultados"

#### Exemplo:

<img width="1509" height="308" alt="image" src="https://github.com/user-attachments/assets/1cd75eac-be18-462a-9b65-2a86541db3af" />