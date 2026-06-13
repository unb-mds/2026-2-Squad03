from urllib import response

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from datetime import datetime

class cnn_spider(scrapy.Spider):
    name = 'CNN'
    data = str(datetime.now().strftime("%Y-%m-%d"))

    def start_requests(self):
        yield scrapy.Request('https://www.cnnbrasil.com.br/tudo-sobre/feminicidio/') # Fazendo requisição para o link de feminicidio

    def parse(self, response, **kwargs):
        for news in response.css('ul figure'):
            if (self.data in news.css('time').attrib['datetime']):
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
