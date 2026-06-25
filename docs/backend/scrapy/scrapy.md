# Scrapy

O Scrapy é um Framework de código aberto da linguagem Python, desenvolvido para realizar Scraping e Crawling em páginas Web.

O Scrapy está sendo utilizado para realizar a coleta de notícias sobre Feminicídio. 

## Funcionamento no VeritasIA

Dentro do projeto existe quatro spiders, sendo eles:
- ```metropoles.py```
- ```g1Spider.py```
- ```r7Spider.py```
- ```cnnSpider.py```

Cada um desses Scripts está fazendo uma requisição para a página de cada um dos respectivos portais, onde realiza a coleta dos seguintes dados:

```json
    {
        "Portal": "portal de noticia",
        "titulo": "titulo",
        "data_publicacao": "yyyy-mm-dd hh-mm-ss",
        "fonte_url": "url",
        "conteudo": "noticia"
    }
```

### Dependências para a Execução:
Utilize os seguintes comandos para fazer a instalação das dependências para a execução dos Scripts:


```python
python -m pip instal scrapy
python -m pip install Playwright
playwright install --with-deps firefox
```

#### Como Executar: 

Executar o spider:

```python
<\2026-2-VeritasIA\scrapers> python executarSpiders.py 
```
