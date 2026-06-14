import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from playwright.sync_api import sync_playwright
from datetime import date

from urllib.parse import urljoin

class metropoles_spider(scrapy.Spider):
    name = 'metropoles'

    def __init__(self, urls = None, **kwargs):
        self.start_urls = urls or []

    def parse(self, response, **kwargs):
        data_da_publicacao = response.css(
            'span.inline-block.tracking-tight.text-neutral-700::text'
        ).get()

        if not data_da_publicacao:
            return

        dia_da_publicacao = data_da_publicacao[0:2]
        if(int(dia_da_publicacao) == date.today().day):

            alltext = response.css('article p *::text, article p::text').getall()

            # colocanto toda a noticia em uma unica string

            news = ' '.join(
                t.strip()
                for t in alltext
                if t.strip() )

            yield { 
                    'portal': 'Metrópoles',
                    'title': response.css('h1::text').get(),
                    'data': data_da_publicacao,
                    'link': response.url,
                    'news': news
                }
            
        
        
def play_writght():
    urls = []

    with sync_playwright() as pw:
        todas_noticias_do_dia = False

        browser = pw.firefox.launch(headless = True)
        page1 = browser.new_page()
        page2 = browser.new_page()

        page1.goto(
            "https://www.metropoles.com/tag/feminicidio",
            wait_until="load"
        )

        while not todas_noticias_do_dia:

            page1.get_by_role(
                "button",
                name="Ver mais notícias",
                exact=False
            ).click()

            page1.wait_for_timeout(2000)

            urls = page1.locator("h3 a[href]").evaluate_all(
                """
                els => [...new Set(
                    els.map(el => el.href)
                )]
                """
            )

            print(urls)
            ultima_noticia = urls[-1]

            page2.goto(ultima_noticia, wait_until="load")

            texto = page2.locator(
                "span.inline-block.tracking-tight.text-neutral-700"
            ).first.text_content()

            data_publicacao = texto.split(",")[0]

            if not data_publicacao:
                return


            print(data_publicacao)

            dia = data_publicacao[0:2]
            mes = data_publicacao[3:5]

            todas_noticias_do_dia = verificar_dia_mes(dia, mes)

        browser.close()

    return urls
def verificar_dia_mes(dia, mes):
    if (int(mes) == date.today().month): # comparando o mes com o mes atual
        if (int(dia) < date.today().day):
            return True
        else:
            return False
    else:
        return True

def metropoles_run_spider():
    
    # pegando os urls com o playwritght

    urls = play_writght() 

    settings = get_project_settings()
    settings.set(
        'FEEDS',
        {
            'scrapers/resultados/metropoles.json': {
                'format': 'json',
                'encoding': 'utf-8',
                'overwrite': True
            }
        }
    )
    process = CrawlerProcess(settings)
    process.crawl(metropoles_spider, urls)
    process.start()

