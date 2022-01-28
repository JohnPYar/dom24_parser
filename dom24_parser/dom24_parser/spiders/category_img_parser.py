import scrapy


class CategoryImgScraper(scrapy.Spider):
    name = 'category_img'
    start_urls = ['https://pvhmarket.ru/catalog/paneli_plastikovye/paneli_centurion/']

    def parse(self, response):
        categories = response.css('div.list.items div.item')
        for category in categories:
            category_name = category.css('.item .name .dark_link::text').get().replace('/', ' ')
            if category_name == 'Под заказ':
                continue
            category_image = category.css('div.img.shine a img::attr(src)').get()
            yield {
                'Category_name': category_name,
                'Category_img': f"https:{category_image}"
            }
