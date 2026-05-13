import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from playwright.sync_api import sync_playwright
import time

class g1_spider(scrapy.Spider):
    name = 'g1'

    def __init__(self, urls = None, **kwargs):
        self.start_urls = urls or []

    def parse(self, response, **kwargs):
        alltext = response.css('.content-text__container::text').getall()


        # colocanto toda a noticia em uma unica string

        news = ''
        for text in alltext:
            news += text

        yield { 
                'portal': 'G1',
                'title': response.css('.content-head__title::text').get(),
                'data': response.css('time::text').get(),
                'link': response.css('main > link').attrib['href'],
                'news': news
            }
        

def play_writght():
    urls = []

    with sync_playwright() as pw:
        browser = pw.firefox.launch(headless = False)

        page1 = browser.new_page()
        page1.goto("https://www.r7.com/tudo-sobre/feminicidio/", wait_until='load')
        page1.locator('[class = b-ultimas-list__items] > li')
        time.sleep(10)
        while True:
            try:
                # Tenta localizar o botão "ver mais"
                botao = page1.get_by_text("Veja mais Notícias")

                # Verifica se ele ainda está visível
                if botao.is_visible():
                    botao.click()
                    time.sleep(2)  # espera carregar 
                else:
                    break

            except Exception:
                # Se não encontrar mais o botão, sai do loop
                break
        
        time.sleep(2)
        
        newsContent = page1.locator('[class = b-ultimas-list__items] > a').all()

    
        for news in newsContent:
            urls.append(news.get_attribute(name="href"))
        
        browser.close()
    print(urls)

    return urls

def g1_run_spider():
    
    # pegando os urls com o playwritght

    urls = play_writght() 

    settings = get_project_settings()
    settings.set(
        'FEEDS',
        {
            './resultados/g1.json': {
                'format': 'json',
                'encoding': 'utf-8',
                'overwrite': True
            }
        }
    )
    process = CrawlerProcess(settings)
    process.crawl(g1_spider, urls)
    process.start()
