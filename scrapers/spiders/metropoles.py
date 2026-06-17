import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from playwright.sync_api import sync_playwright
from datetime import date

class metropoles_spider(scrapy.Spider):
    name = 'metropoles'

    def __init__(self, urls = None, **kwargs):
        self.start_urls = urls or []

    def parse(self, response, **kwargs):
        data_da_publicacao = response.css('time').attrib['datetime']
        dia_da_publicacao = data_da_publicacao[8:10]
        if(int(dia_da_publicacao) == date.today().day):

            alltext = response.css('article p:not(.data)::text').getall()

            # colocanto toda a noticia em uma unica string

            news = ''
            for text in alltext:
                news += text

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
        page1.goto("https://www.metropoles.com/tag/feminicidio", wait_until='load')

        while todas_noticias_do_dia != True:
            page1.get_by_role("button", name = "Carregar mais notícias", exact = False).click()
            newsContent = page1.locator('h4 > a').all()
            urls = []
            for news in newsContent:
                urls.append(news.get_attribute(name="href"))
            
            ultima_noticia = urls[len(urls) - 1] # pegando ultima noticia da lista
            page2.goto(ultima_noticia, wait_until='load')
            data_da_publicacao = page2.locator('time').nth(0).get_attribute(name = "datetime") # data que a ultima noticia foi publicada
            mes_da_publicacao = data_da_publicacao[5:7]
            dia_da_publicacao = data_da_publicacao[8:10]
            todas_noticias_do_dia = verificar_dia_mes(dia_da_publicacao, mes_da_publicacao)
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
