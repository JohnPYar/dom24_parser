import scrapy

product_id = 0

class Dom24Scraper(scrapy.Spider):
    name = 'dom24'
    start_urls = ['https://pvhmarket.ru/catalog/paneli_plastikovye/paneli_centurion/']

    def parse(self, response):
        categories = response.css("div.name")
        for category in categories:
            if category.css('a::text').get() != 'Под заказ':
                category_name = category.css('a::text').get().strip()
                category_name = category_name.replace('/', ' ')
                category_url = category.css('a::attr(href)').get()
                # category_url = category.css('a')
                yield response.follow(category_url, self.parse_category, cb_kwargs=dict(category_name=category_name))

    def parse_category (self, response, category_name):
        products = response.css('div.catalog_item')
        for product in products:
            sticker_pod_zakaz = product.css('div.sticker_pod_zakaz')
            price_value = product.css('span.price_value')
            # print(sticker_pod_zakaz)
            product_link = product.css('a.thumb.shine::attr(href)').get()
            if not sticker_pod_zakaz and price_value:
                yield response.follow(product_link, self.parse_product, cb_kwargs=dict(category_name=category_name))

    #     проверяем на наличие пагинации на странице товаров в категории
        next_page = response.css('div.nums li.flex-nav-next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse_category, cb_kwargs=dict(category_name=category_name))

    def parse_product (self, response, category_name):
        global product_id
        product_id += 1
        images = []
        images_links = response.css('div.slides a::attr(href)').getall()
        for image_link in images_links:
            images.append('https:' + image_link.strip())
        yield {
            'product_id': product_id,
            'Category': category_name,
            'Name': response.css('h1#pagetitle::text').get().strip(),
            'Title': response.css('h1#pagetitle::text').get().strip(),
            'Image': images,
            'Price': response.css('div.middle_info span.price_value::text').get().strip()
        }
