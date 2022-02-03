import scrapy
import html

product_id = 142
description = ''

description_escape = html.escape(description, True)
categories_need = {'Со вставкой хром и золото', 'На потолок белые'}


class Dom24PotolocSpider(scrapy.Spider):
    name = 'dom24_potoloc'
    start_urls = ['https://pvhmarket.ru/catalog/paneli_plastikovye/paneli_potolochnye/']

    def parse(self, response):
        global categories_need
        categories = response.css("div.name")
        for category in categories:
            if category.css('a::text').get() in categories_need:
                category_name = category.css('a::text').get().strip()
                category_name = category_name.replace('/', ' ')
                category_url = category.css('a::attr(href)').get()
                yield response.follow(category_url, self.parse_category, cb_kwargs=dict(category_name=category_name))

    def parse_category (self, response, category_name):
        products = response.css('div.catalog_item')
        if category_name == 'Со вставкой хром и золото':
            for product in products:
                # sticker_pod_zakaz = product.css('div.sticker_pod_zakaz')
                sticker_sale_text = product.css('div.sticker_sale_text')
                sticker_sovetuem = product.css('div.sticker_sovetuem')
                # price_value = product.css('span.price_value')
                # print(sticker_pod_zakaz)
                product_descript = product.css('div.item-title span::text').get()
                product_link = product.css('a.thumb.shine::attr(href)').get()
                if not sticker_sale_text and ("Реечная" in product_descript or sticker_sovetuem):
                    yield response.follow(product_link, self.parse_product, cb_kwargs=dict(category_name=category_name))

        if category_name == 'На потолок белые':
            for product in products:
                sticker_pod_zakaz = product.css('div.sticker_pod_zakaz')
                sticker_sale_text = product.css('div.sticker_sale_text')
                product_descript = product.css('div.item-title span::text').get()
                product_link = product.css('a.thumb.shine::attr(href)').get()
                if not (sticker_sale_text or sticker_pod_zakaz) and "3000" in product_descript:
                    yield response.follow(product_link, self.parse_product, cb_kwargs=dict(category_name=category_name))

    #     проверяем на наличие пагинации на странице товаров в категории
        next_page = response.css('div.nums li.flex-nav-next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse_category, cb_kwargs=dict(category_name=category_name))

    def parse_product (self, response, category_name):
        global product_id
        global description
        # product_id += 1
        images = []
        images_links = response.css('div.slides a::attr(href)').getall()
        for image_link in images_links:
            images.append('https:' + image_link.strip())
        yield {
            # 'product_id': product_id,
            'Category': category_name,
            'Name': response.css('h1#pagetitle::text').get().strip(),
            'Title': response.css('h1#pagetitle::text').get().strip(),
            'Image': images,
            'Price': response.css('div.middle_info span.price_value::text').get().strip(),
            'Model': response.css('h1#pagetitle::text').get().strip(),
            # 'Description': description_escape
        }
