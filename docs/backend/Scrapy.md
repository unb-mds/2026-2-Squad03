# Passo a Passo (BASH)
---

# Crie um ambiente virtual
`
python3 -m venv venv 
`

# Ative o ambiente
- windowns 
` venv\Script\activate`
- Linux 
` source venv/bin/activate`

# Instalação
`pip install scrapy`


# Executar
` scrapy shell <link>`


# Outros Comandos
` response.css('cssPath') `

` response.xpath("xPath") `

---

---

# Exemplo de codigo Scrapy utilizando uma noticia da CNN

```python
import scrapy
from scrapy.crawler import CrawlerProcess

class Feminicidio(scrapy.Spider):
    name = 'Feminicidio'

    def start_requests(self):
        yield scrapy.Request('https://www.cnnbrasil.com.br/?search=feminicidio')

    def parse(self, response, **kwargs):
        for news in response.css("ul").css('figure'):
            yield {
                'link': news.css('a').attrib['href']
            }


process = CrawlerProcess(settings={
    'FEED_FORMAT': 'json',
    'FEED_URI': 'result.json',
})

process.crawl(Feminicidio)
process.start() 


```
# Resultado


```json
[
{"link": "https://www.cnnbrasil.com.br/nacional/sudeste/sp/filha-de-pm-morta-por-tenente-coronel-vai-receber-pensao-um-mes-apos-pedido/"},
{"link": "https://www.cnnbrasil.com.br/nacional/sudeste/sp/tarcisio-fala-sobre-aposentadoria-de-tenente-coronel-vai-para-familiares/"},
{"link": "https://www.cnnbrasil.com.br/nacional/sudeste/sp/tenente-preso-por-matar-pm-recebera-aposentadoria-mesmo-se-for-expulso/"},
{"link": "https://www.cnnbrasil.com.br/nacional/sudeste/sp/para-ela-sobrou-o-caixao-dizem-pais-de-pm-sobre-aposentadoria-de-tenente/"},
{"link": "https://www.cnnbrasil.com.br/nacional/sudeste/sp/tenente-coronel-reu-por-matar-esposa-pm-se-aposenta-com-salario-integral/"},
{"link": "https://www.cnnbrasil.com.br/nacional/sudeste/rj/homem-e-condenado-a-80-anos-de-prisao-por-matar-tres-criancas-em-paraty/"},
{"link": "https://www.cnnbrasil.com.br/nacional/sul/sc/autor-de-ataque-a-creche-em-blumenau-e-condenado-por-esfaquear-cachorro/"},
{"link": "https://www.cnnbrasil.com.br/nacional/sudeste/rj/empresas-reforcam-compromisso-no-combate-ao-feminicidio-em-evento-no-rio/"},
{"link": "https://www.cnnbrasil.com.br/nacional/sudeste/sp/secretario-de-seguranca-de-sao-paulo-detalha-combate-a-quebra-vidros/"},
{"link": "https://www.cnnbrasil.com.br/nacional/sudeste/sp/mulher-pula-do-2o-andar-com-filha-para-fugir-de-ex-em-suzano-sp/"},
{"link": "https://www.cnnbrasil.com.br/nacional/sudeste/rj/mulher-e-encontrada-morta-apos-suspeita-de-envenenamento-no-rj/"},
{"link": "https://www.cnnbrasil.com.br/nacional/nordeste/pe/adolescente-atira-em-ficante-e-e-apreendido-por-tentativa-de-feminicidio/"},
{"link": "https://www.cnnbrasil.com.br/nacional/nordeste/pe/empresario-e-indiciado-por-atirar-20-vezes-na-porta-da-ex-companheira-em-pe/"},
{"link": "https://www.cnnbrasil.com.br/nacional/sudeste/sp/feminicidios-sobem-31-em-sao-paulo-no-bimestre/"},
{"link": "https://www.cnnbrasil.com.br/nacional/nordeste/ba/homem-e-preso-apos-esfaquear-mulher-e-esconder-o-corpo-no-freezer/"}
]

```

# Estudo de PlayWright
---

# Código Inicial

esse código pega o link e o titulo de noticias sobre feminicidio publicadas no g1

```python
from playwright.sync_api import sync_playwright, expect
import time # biblioteca de timer não necessaria para o playwright

with sync_playwright() as pw:
    browser = pw.firefox.launch(headless=False) # selecionando o firefox como navegador

    page1 = browser.new_page() # criando uma nova aba
    page1.goto("https://g1.globo.com/busca/?q=feminicidio", wait_until='load') # indo para pagina do g1 ja com o filtro do feminicidio
    page1.locator("a").filter(has_text="Filtrar por Data").click() # abrindo filtro
    page1.get_by_text("Nas últimas 24 horas").click() # filtrando noticias do ultimo dia

    time.sleep(4) # timer de 4 segundos
    
    newsContent = page1.locator('[class *= widget--info__text-container] > a').all() # pegando todas as noticias

    allnews = []
    for news in newsContent:
        allnews.append({
            'Link' : news.get_attribute(name="href"),
            "Title" : news.locator('[class *= widget--info__title]').text_content()
        })
    
    browser.close()
```
