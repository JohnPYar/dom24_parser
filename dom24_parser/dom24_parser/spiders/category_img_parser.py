import scrapy


class CategoryImgScraper(scrapy.Spider):
    name = 'category_img'
    start_urls = ['https://pvhmarket.ru/catalog/paneli_plastikovye/paneli_centurion/']

    def parse(self, response):
        categories_images = response.css("div.img.shine a img::attr(src)")
        for image in categories_images:
            yield {
                'Category_img': f"https:{image.get()}"
            }
