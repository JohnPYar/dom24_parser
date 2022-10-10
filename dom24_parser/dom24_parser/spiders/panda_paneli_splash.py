import scrapy


class PandaPaneliSplashSpider(scrapy.Spider):
    name = 'panda_paneli_splash'
    allowed_domains = ['https://www.panda-panel.ru']
    start_urls = ['http://https://www.panda-panel.ru/catalog/pvkh_paneli/dlya_vann/svezhest.html/']

    def parse(self, response):
        pass
