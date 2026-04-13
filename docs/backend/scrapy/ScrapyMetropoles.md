# Implementação do Scrapy
---
Utilizamos o portal de noticias:
- [Metropoles](https://www.metropoles.com/)
Para fazermos o Scrapy e coletar dados para os primeiros testes para projeto.
---
## Obter Links:
``` python
import scrapy
from scrapy.crawler import CrawlerProcess

class MetropolesFeminicidio(scrapy.Spider):
        name = 'Feminicidio'

        def start_requests(self):
            yield scrapy.Request('https://www.metropoles.com/tag/feminicidio')

        def parse(self, response, **kwargs):
            for news in response.css('.noticia__descricao').css('p').css('a'):
                yield{
                    'link': news.attrib['href']
                }

process = CrawlerProcess(settings={
        'FEEDS': {
            'result.json': {'format': 'json', 'encoding': 'utf8', 'overwrite': True}
        }
        })

process.crawl(MetropolesFeminicidio)
process.start()
```
## Scrapy utilizando os links

```python
import scrapy
from scrapy.crawler import CrawlerProcess
import json


class Metropoles(scrapy.Spider):
    name = 'Metropoles'
    def __init__(self, urls = None, **kwargs):
        self.start_urls = urls or []

    def parse(self, response, **kwargs):
        yield {
               'autor': response.css('.logo-div-container').css('a::text').getall(),
                'titulo': response.css('header').css('h1::text').get(),
                'texto': response.css('article p:not(.data)::text').getall(),
                'horario': response.css('article time::text').getall()
        }
 
process = CrawlerProcess(settings={
    'FEED_FORMAT': 'json',
    'FEED_URI': 'feminicidio.json',
    'encoding': 'utf8'
})

links = []
with open('links.json', 'r') as links_json:
    save_links = json.load(links_json)
    for i in range(len(save_links)):
        links.append(save_links[i]['link'])

process.crawl(Metropoles, urls=links)
process.start()
```

---

## Problemas
- Código rodaria um por vez, não sendo efetivo.
- Ao juntar o código não descobrimos uma forma, utilizando a lógica que pensamos, para conseguir rodar o código simultaneamente

----
# Código Refatorado

```python
import scrapy
from scrapy.crawler import CrawlerProcess

class Metropoles(scrapy.Spider):
    name = 'Metropoles'
    links = []
    i = 0

    def start_requests(self):
        yield scrapy.Request('https://www.metropoles.com/tag/feminicidio')

    def parse(self, response):
        for news in response.css('.noticia__descricao').css('p').css('a'):
            link = news.attrib['href']
            self.links.append(link)
        for self.i in range(len(self.links)):
                get = self.links[self.i]
                self.i += 1
                yield response.follow(get, self.parse_pegar)

    def parse_pegar(self, response):
        yield {
                'autor': response.css('.logo-div-container').css('a::text').getall(),
                'titulo': response.css('header').css('h1::text').get(),
                'texto': response.css('article p:not(.data)::text').getall(),
                'horario': response.css('article time::text').getall()
        }


process = CrawlerProcess(settings={
        'FEEDS': {
            'result.json': {'format': 'json', 'encoding': 'utf8', 'overwrite': False}
        }
        })

process.crawl(Metropoles)
process.start()
```
---
- Código realiza as mesmas coisas só que em um só Scrapy

# O que retorna para nós:

```json
[
"author": [NOME], "titulo": [TITULO], "horario": [HORARIO]
]
```


