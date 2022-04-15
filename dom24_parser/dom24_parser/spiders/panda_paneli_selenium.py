import html
import time

import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

description = ''
# description_escape = cgi.escape(description, True)
description_escape = html.escape(description, True)

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

        # проверяем наличие артикулов(вариантов) товара,
        # если есть, то парсим как отдельные товары через selenium, модель будет у всех одна, по главному заголовку
        skus_amount = len(response.css('li.skuDropdownListItem'))
        if skus_amount > 1:

            driver.get(response.url)

            skus = driver.find_elements(By.CLASS_NAME, 'skuPropertyItemLink')

            for sku in skus:
                sku.click()
                time.sleep(1)

                title = driver.find_element(By.CSS_SELECTOR, 'h1.changeName')
                # title = driver.find_element(By.XPATH, '//h1')
                # title = WebDriverWait(driver, 10000).until(lambda x: x.find_element(By.XPATH, '//h1'))

                # soup = bs(page_source, 'html.parser')
                # title = soup.find(class_='changeName').text
                print(title.text)

            yield {
                'title': driver.title
            }
        # else:
        #     pass
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
