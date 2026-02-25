import scrapy
from scrapy.crawler import CrawlerProcess
import json

class DivanSpider:
    name = "divan"
    start_urls = ["https://www.divan.ru/category/svetilniki"]

    def parse(self, response):
        for product in response.css('div._Ud0k'):
            yield {
                'name': product.css('div.lsooF span::text').get(),
                'price': product.css('div.pY3d2 span::text').get(),
                'url': product.css('a::attr(href)').get()
            }


process = CrawlerProcess(settings={
    'USER_AGENT': 'Mozilla/5.0',
    'FEEDS': {
        'products.json': {
            'format': 'json',
            'encoding': 'utf8',
            'indent': 2,
        },
    },
})

process.crawl(DivanSpider)
process.start()

