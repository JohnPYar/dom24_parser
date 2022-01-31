import scrapy
import html

product_id = 0
description = ''
category_name = 'Кухонные фартуки из МДФ'

# description_escape = cgi.escape(description, True)
description_escape = html.escape(description, True)


class Dom24PandaSpider(scrapy.Spider):
    name = 'dom24_panda'
    start_urls = ['https://www.panda-panel.ru/catalog/kukhonnye_fartuki/']

    def parse (self, response):
        products = response.css('div.item.product')
        for product in products:
            product_link = product.css('div.productColText a.name::attr(href)').get()
            yield response.follow(product_link, self.parse_product)

    #     проверяем на наличие пагинации на странице товаров в категории
        next_page = response.css('li.bx-pag-next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_product (self, response):
        # global product_id
        global description
        global category_name
        # product_id += 1
        yield {
            # 'product_id': product_id,
            'Category': category_name,
            'Name': response.css('h1.changeName::text').get().strip(),
            'Title': response.css('h1.changeName::text').get().strip(),
            'Image': f"https://www.panda-panel.ru{response.css('div.pictureSlider img::attr(src)').get()}",
            'Price': response.css('div#elementTools span.priceVal::text').get().replace(' руб.', '').strip(),
            'Model': response.css('h1.changeName::text').get().strip(),
            # 'Description': description_escape
        }
