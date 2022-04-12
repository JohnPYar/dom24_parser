import json
import scrapy
import html
from scrapy_playwright.page import PageMethod
# from scrapy_playwright.page import PageCoroutine


description = ''
# description_escape = cgi.escape(description, True)
description_escape = html.escape(description, True)


class Dom24PandaPaneliSpider(scrapy.Spider):
    name = 'panda_paneli'
    # start_urls = ['https://www.panda-panel.ru/catalog/pvkh_paneli/']

    # настройки scrapy playwright
    custom_settings = {
        'DOWNLOAD_HANDLERS': {
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },
        # эту настройку здесь нельзя прописывать, только в settings.py, так как выдает ошибку
        # 'TWISTED_REACTOR': "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
    }

    # запрашиваем адрес через playwright и передаем ответ в scrapy
    def start_requests(self):
        start_url = "https://www.panda-panel.ru/catalog/pvkh_paneli/"
        yield scrapy.Request(start_url, meta={
            "playwright": True,
            # "playwright_include_page": True,
            "playwright_page_methods": {
            #     # 'wait_for_selector': PageMethod('wait_for_selector', 'a.catalog-section-list-link'),
                'clickCategories': PageMethod('evaluate', 'document.querySelectorAll("a.catalog-section-list-link").forEach(x=>x.click())'),
            # #     'clickAllCategories': PageMethod('eval_on_selector_all', "a.catalog-section-list-link", "x=>x.click()"),
            # #     'locator': PageMethod('locator', "a.catalog-section-list-link"),
            #     # 'clicks_all_locators': PageMethod(),
            #     # 'click': PageMethod('click', selector="a.catalog-section-list-link")
            # #     # 'wait_for_selector': PageCoroutine('wait_for_selector', 'a.catalog-section-list-link'),
            # #     'clickallcategories': PageCoroutine('evaluate', 'document.querySelectorAll("a.catalog-section-list-picture").forEach(x=>x.click())')
            }
        }
        )

    def parse(self, response):
        # page = response.css('title::text').get()
        # page = response.meta["playwright_page_methods"]["clickCategories"][0]
        # page = response.meta["playwright_page"]
        # title = await page.title()
        # title = response.css('title::text').get()
        # url = page.url
        # await page.close()
        # page.locator('a.catalog-section-list-link')
        # new_page = await page.click("a.catalog-section-list-link")
        # new_page = page.locator('a.catalog-section-list-link')
        # new_page = await page.locator('a.catalog-section-list-link').click()
        # page_new = response.css('title').get()
        # title = await page.text_content('title')
        # links = page.query_selector_all('a.catalog-section-list-link')
        # page.click('a.catalog-section-list-link')
        # await page.click("a.catalog-section-list-link")
        # yield {'page': page.url}
        # await page.close()
        with open('test.txt', 'a') as file:
            # await page.click('a.catalog-section-list-link')
            file.write(response.url)
            # file.write(title)
            # await page.close()
        # yield {'new_page': new_page.url}
        # yield {'page': page.url}
        # yield {'page': title}
        yield {'URL': response.url}
        # yield {'page': new_page}
        # yield links
        # title = await page.title()
        # print(new_page)
        # print(title)
        # categories = response.css('a.catalog-section-list-link')
        # for category in categories:
        #     category_name = category.css('span::text').get().strip()
        #     category_url = category.attrib['href']
        #     yield response.follow(category_url, self.parse_category, cb_kwargs=dict(category_name=category_name), meta={"playwright": True})

    # def parse_category(self, response, category_name):
    #     products = response.css('div.productColText')
    #     for product in products:
    #         product_link = product.css('a.name::attr(href)').get()
    #         yield response.follow(product_link, self.parse_product, cb_kwargs=dict(category_name=category_name), meta={"playwright": True})
    #
    # #     проверяем на наличие пагинации на странице товаров в категории
    #     next_page = response.css('li.bx-pag-next a::attr(href)').get()
    #     if next_page is not None:
    #         yield response.follow(next_page, self.parse_category, cb_kwargs=dict(category_name=category_name), meta={"playwright": True})
    #
    # def parse_product(self, response, category_name):
    #     # получаем характеристика товара в виде аттрибутов
    #     attributes = ''
    #     attrs = response.css('div.propertyList')
    #     # счетчик для определения последнего элемента массива
    #     counter = 0
    #     for attr in attrs:
    #         counter += 1
    #         name = attr.css('div.propertyName::text').get().strip()
    #         value = attr.css('div.propertyValue::text').get().strip()
    #         attributes += f"{name}---{value}"
    #         #     если элемент не последний добавляем разделитель
    #         if counter != (len(attrs) - 1):
    #             attributes += "|"
    #
    #     # проверяем наличие артикулов(вариантов) товара,
    #     # если есть, то парсим как отдельные товары через selenium, модель будет у всех одна, по главному заголовку
    #     skus_amount = len(response.css('ul.elementSkuPropertyList'))
    #     if skus_amount > 1:


        # yield {
        #     # 'product_id': product_id,
        #     'Category': category_name,
        #     'Name': response.css('h1.changeName::text').get().strip(),
        #     'Title': response.css('h1.changeName::text').get().strip(),
        #     # 'Image': f"https://www.panda-panel.ru{response.css('div.pictureSlider img::attr(src)').get()}",
        #     'Image': f"https://www.panda-panel.ru{response.css('div.pictureSlider a::attr(href)').get()}",
        #     'Price': response.css('div#elementTools span.priceVal::text').get().replace(' руб.', '').strip(),
        #     'Model': response.css('h1.changeName::text').get().strip(),
        #     # 'Description': description_escape
        #     'Description': response.css('div.changeShortDescription::text').get().strip(),
        #     'Properties': attributes
        # }
