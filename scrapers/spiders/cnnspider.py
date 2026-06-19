from urllib import response

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from datetime import datetime
from zoneinfo import ZoneInfo

class cnn_spider(scrapy.Spider):
    name = 'CNN'
    data = datetime.now(ZoneInfo("America/Sao_Paulo")).strftime("%Y-%m-%d")
    
    start_urls = [
        "https://www.cnnbrasil.com.br/tudo-sobre/feminicidio/"
    ]

    def parse(self, response, **kwargs):
        for news in response.css('ul figure'):
            print('data cnn: ' + news.css('time').attrib['datetime'])
            if (self.data in news.css('time').attrib['datetime']):
                print('noticia valida')
                yield response.follow(news.css('a').attrib['href'], self.parse_pegar)

    def parse_pegar(self, response):
        alltext = response.css('article p *::text, article p::text, article p strong::text').getall()

            # colocanto toda a noticia em uma unica string
        news = ' '.join(
            t.strip()
            for t in alltext
            if t.strip() )
        
        yield {
                'portal': 'CNN',
                'title': response.css('article').css('header').css('h1::text').get(),
                'data': response.css('article').css('span').css('.timestamp__date::text').getall(),
                'links': response.url,
                'news':  news,
        }

         
def cnn_run_spider():
    settings = get_project_settings()
    settings.set(
        'FEEDS',
        {
            'scrapers/resultados/cnn.json': {
                'format': 'json',
                'encoding': 'utf-8',
                'overwrite': True
            }
        }
    )
    process = CrawlerProcess(settings)
    process.crawl(cnn_spider)
    process.start()
