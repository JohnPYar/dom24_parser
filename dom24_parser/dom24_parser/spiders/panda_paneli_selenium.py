import html
import time

import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# description = ''
# description_escape = cgi.escape(description, True)
# description_escape = html.escape(description, True)

options = webdriver.ChromeOptions()
# options.add_argument('--headless')
driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))

class Dom24PandaPaneliSpider(scrapy.Spider):
    name = 'panda_paneli_sel'
    start_urls = ['https://www.panda-panel.ru/catalog/pvkh_paneli/']

    def parse(self, response):
        categories = response.css('a.catalog-section-list-link')
        for category in categories:
            category_name = category.css('span::text').get().strip()
            category_url = category.attrib['href']
            yield response.follow(category_url, self.parse_category, cb_kwargs=dict(category_name=category_name))

    def parse_category(self, response, category_name):
        products = response.css('div.productColText')
        for product in products:
            product_link = product.css('a.name::attr(href)').get()
            yield response.follow(product_link, self.parse_product, cb_kwargs=dict(category_name=category_name))

        #     проверяем на наличие пагинации на странице товаров в категории
        next_page = response.css('li.bx-pag-next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse_category, cb_kwargs=dict(category_name=category_name))

    def parse_product(self, response, category_name):
        global options
        global driver

        time.sleep(1)
        # получаем характеристика товара в виде аттрибутов
        attributes = ''
        attrs = response.css('div.propertyList')

        # счетчик для определения последнего элемента массива
        counter = 0
        for attr in attrs:
            counter += 1
            name = attr.css('div.propertyName::text').get().strip()
            value = attr.css('div.propertyValue::text').get().strip()
            attributes += f"{name}---{value}"
            #     если элемент не последний добавляем разделитель
            if counter != (len(attrs) - 1):
                attributes += "|"

        description = response.css('div.changeShortDescription::attr(data-first-value)').get().strip()
        description_escaped = html.escape(description, True)

        # проверяем наличие артикулов(вариантов) товара,
        # если есть, то парсим как отдельные товары через selenium, модель будет у всех одна, по главному заголовку
        model = response.css('h1.changeName::text').get().strip()
        skus_amount = len(response.css('li.skuDropdownListItem'))
        if skus_amount > 1:

            driver.get(response.url)
            # time.sleep(1)
            skus = driver.find_elements(By.CLASS_NAME, 'skuPropertyItemLink')

            #  !!!!!!!!!!!!!!
            # для решения проблемы ошибки со считыванием и выдачей данных по yield в цикле делаем два цикла:
            # в 1-м собираем данные по кликам в список, во 2-м в цикле выдаем их из списка через yield
            #  !!!!!!!!!!!!!!

            product_vars = []

            # 1-й цикл: собираем данные с кликов в список
            for sku in skus:
                # time.sleep(1)
                sku.click()
                time.sleep(1)
                artikul = driver.find_element(By.CSS_SELECTOR, 'h1.changeName')

                images = []
                images_links = driver.find_elements(By.CSS_SELECTOR, 'div.slideBox a.zoom')
                for image_link in images_links:
                    images.append('https://www.panda-panel.ru/' + image_link.get_attribute('href').strip())

                price = driver.find_element(By.CSS_SELECTOR, '#elementTools span.priceVal')

                product_vars.append({
                    'model': model,
                    'title': artikul.text.strip(),
                    'image': images,
                    'price': price.text,
                    # 'price': price.text.replace(' руб.', '').strip(),
                })

            # 2-й цикл: выдаем данные из списка через yield
            for i in product_vars:
                yield {
                    'Category': category_name,
                    'Model': i['model'],
                    'Name': i['title'],
                    'Title': i['title'],
                    'Image': i['image'],
                    'Price': i['price'],
                    # 'Description': description_escaped,
                    # 'Properties': attributes
                }

        # else:
        #     images = []
        #     images_links = response.css('div.slideBox a.zoom::attr(href)').getall()
        #     for image_link in images_links:
        #         images.append('https://www.panda-panel.ru/' + image_link.get_attribute('href').strip())
        #
        #     yield {
        #         'Category': category_name,
        #         'Name': response.css('h1.changeName::text').get().strip(),
        #         'Title': response.css('h1.changeName::text').get().strip(),
        #         'Image': images,
        #         'Price': response.css('div#elementTools span.priceVal::text').get().replace(' руб.', '').strip(),
        #         'Model': model,
        #         'Description': description_escaped,
        #         'Properties': attributes
        #     }
