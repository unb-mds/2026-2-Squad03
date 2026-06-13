import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from playwright.sync_api import sync_playwright
from datetime import date

class g1_spider(scrapy.Spider):
    name = 'g1'

    def __init__(self, urls = None, **kwargs):
        self.start_urls = urls or []

    def parse(self, response, **kwargs):

        data_da_publicacao = response.css('time').attrib['datetime']
        dia_da_publicacao = data_da_publicacao[8:10]

        if(int(dia_da_publicacao) == date.today().day): # filtrando noticias apenas do dia

            alltext = response.css('article p *::text, article p::text').getall()

            # colocanto toda a noticia em uma unica string

            news = ' '.join(
                t.strip()
                for t in alltext
                if t.strip() )

            yield { 
                    'Portal': 'G1',
                    'Title': response.css('.content-head__title::text').get(),
                    'Time': response.css('time::text').get(),
                    'Link': response.css('main > link').attrib['href'],
                    'News': news
                }

        
def play_writght():
    urls = []

    with sync_playwright() as pw:
        browser = pw.firefox.launch(headless = True)

        page1 = browser.new_page()
        page1.goto("https://g1.globo.com/busca/?q=feminicidio", wait_until='load')
        page1.locator("a").filter(has_text="Filtrar por Data").click() # Abrindo filtros
        # page1.get_by_text("Nas últimas 24 horas").click() # ativando o filtro do ultimo dia
        page1.locator('span[data-date = "now-1d"]').click()

        scroll_to_absolute_bottom(page1)

        newsContent = page1.locator('[class = widget--info__text-container] > a').all()

    
        for news in newsContent:
            urls.append(news.get_attribute(name = "href"))
        
        browser.close()

    return urls


def scroll_to_absolute_bottom(page):
    while True:
        # Pega a altura atual da página antes de rolar
        current_height = page.evaluate("document.body.scrollHeight")
        
        # Rola até o final da página atual
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        
        # Aguarda o tempo necessário para novos elementos carregarem
        page.wait_for_timeout(2000) 
        
        # Pega a nova altura após a tentativa de rolagem
        new_height = page.evaluate("document.body.scrollHeight")
        
        # Se as alturas forem iguais, a página chegou ao fim absoluto
        if new_height == current_height:
            break

def verificar_dia_mes(dia, mes):
    if (int(mes) == date.today().month): # comparando o mes com o mes atual
        if (int(dia) < date.today().day):
            return True
        else:
            return False
    else:
        return True
        


def g1_run_spider():
    
    # pegando os urls com o playwritght

    urls = play_writght() 

    settings = get_project_settings()
    settings.set(
        'FEEDS',
        {
            'scrapers/resultados/g1.json': {
                'format': 'json',
                'encoding': 'utf-8',
                'overwrite': True
            }
        }
    )
    process = CrawlerProcess(settings)
    process.crawl(g1_spider, urls)
    process.start()
