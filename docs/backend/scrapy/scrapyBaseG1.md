# Modelo de Scrapy inicial para o G1

Utilizei scrapy e playwritght para pegar as noticias das ultimas 24h do g1 relacionadas ao feminicidio

---

para isso crei 3 arquivos

- main
- g1scrapy (aonde esta o codigo do Scrapy)
- writght (aonde esta o codigo do PlayWritght)
---

## Main

```python
from writght import play_writght
from scrapy.crawler import CrawlerProcess
from g1scrapy import G1


# Get URLs with Playwright

urls = play_writght() 


# Starting Scrapy using the links

process = CrawlerProcess(settings={
    'FEEDS': {
        'result.json': {'format': 'json'}
    }
    })

process.crawl(G1, urls=urls)
process.start()
```

---

## g1scrapy

```python
import scrapy


class G1(scrapy.Spider):
    name = 'G1'

    def __init__(self, urls = None, **kwargs):
        self.start_urls = urls or []

    def parse(self, response, **kwargs):
        alltext = response.css('.content-text__container::text').getall()


        # putting the entire news text into a single string
        news = ''
        for text in alltext:
            news += text

        yield { 
                'Title': response.css('.content-head__title::text').get(),
                'Time': response.css('time::text').get(),
                'News': news
            }
        
```
---
## writght

```python
from playwright.sync_api import sync_playwright
import time

def play_writght():
    urls = []

    with sync_playwright() as pw:
        browser = pw.firefox.launch(headless=False)

        page1 = browser.new_page()
        page1.goto("https://g1.globo.com/busca/?q=feminicidio", wait_until='load')
        page1.locator("a").filter(has_text="Filtrar por Data").click() # opening filter
        page1.get_by_text("Nas últimas 24 horas").click() # activating last day filter

        time.sleep(4)
        
        newsContent = page1.locator('[class = widget--info__text-container] > a').all()

    
        for news in newsContent:
            urls.append(news.get_attribute(name="href"))
        
        browser.close()

    return urls
```