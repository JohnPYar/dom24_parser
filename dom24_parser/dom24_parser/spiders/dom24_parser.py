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
            'Price': response.css('div.middle_info span.price_value::text').get().strip(),
            'Model': response.css('h1#pagetitle::text').get().strip(),
            'Description': "
                    · Длина панели: 2700 мм;
                    · Ширина панели: 250 мм;
                    · Толщина: 8мм
                    · Полезная площадь: 0,675 м2
                    · Вес панели: 1,16 кг;
                    · Количество в коробке: 10 шт;
                    · Объем коробки: 0,06 м3.


                Стеновые пластиковые панели имеют очень большой срок службы, обладают стопроцентную устойчивость к влаги и даже в стыках не пропускают влагу. Пластиковые панели устойчивы к влиянию атмосферных явлений и могут выдерживать сильные механические нагрузки.
                    · С помощью такого отделочного материала, как стеновые панели ПВХ, можно сделать быстрый, чистый и качественный ремонт;
                    · Декоративные рейки плюс гладкие вторые стены помогают помещению обрести современный вид;
                    · Пластиковые панели можно установить на разнообразные поверхности;
                    · Панели ПВХ легко скроют неровности стен;
                    · Электропроводка прячется за панели ПВХ;
                    · Звукоизоляция улучшается;
                    · Не подвергаются воздействию низких температур и могут устанавливаться в помещениях без отопления;
                    · Степень пожаробезопасности высокая, горение не поддерживается;
                    · Пластиковые панели – это экологически безопасные материалы для отделки.
                Пластиковые панели не требуют значительного ухода. Их можно использовать для отделки любых бытовых помещений: ванные комнаты, душевые, кухни, туалеты и т.п. т.к. стеновые пластиковые панели соответствуют всем гигиеническим требованиям. Чтобы поддерживать пластиковые панели в чистоте, достаточно всего лишь иногда протирать их влажной тряпкой или любым доступным моющим средством, которое не содержит абразивные элементы.
                Практически полное отсутствие отходов, пыли и грязи при отделке пластиковыми панелями также является неоспоримым достоинством.
                Особенности конструкции
                Ребра жесткости обеспечивают высокую прочность панелей, благодаря своей конструкции.
                Любая декоративная пластиковая панель имеет определенное количество изолированных ячеек, и, благодаря этому пластиковые панели имеют высокие термо- и звукоизолирующие характеристики.



                Область применения
                Пластиковые панели устанавливают на стены и потолки во влажных помещениях (санузлы, бассейны, душевые), так как панели не боятся влаги; на лоджиях, балконах, так как пластиковые панели морозоустойчивые; в жилых помещениях, так как панели пвх экологичны; на кухне и в подсобных помещениях, так как панели ПВХ легко моются.
                "
        }
