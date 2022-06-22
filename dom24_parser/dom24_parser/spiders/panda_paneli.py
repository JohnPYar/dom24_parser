import json
import time

import scrapy
import html
from scrapy_playwright.page import PageMethod


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
        start_url = "https://www.panda-panel.ru/catalog/pvkh_paneli/dlya_vann/parizh.html"
        yield scrapy.Request(start_url, meta={
            "playwright": True,
            "playwright_include_page": True,
            "playwright_page_methods": {
            # #     # 'wait_for_selector': PageMethod('wait_for_selector', 'a.catalog-section-list-link'),
                'clickCategories': PageMethod('evaluate', 'document.querySelectorAll("a.skuPropertyItemLink").forEach(x=>x.click())')
            #     'clickAllCategories': PageMethod('eval_on_selector_all', "a.skuPropertyItemLink", "(x) => x.click();")
            # # #     'locator': PageMethod('locator', "a.catalog-section-list-link"),
            # #     # 'clicks_all_locators': PageMethod(),
            # #     # 'click': PageMethod('click', selector="a.catalog-section-list-link")
            # # #     # 'wait_for_selector': PageCoroutine('wait_for_selector', 'a.catalog-section-list-link'),
            # # #     'clickallcategories': PageCoroutine('evaluate', 'document.querySelectorAll("a.catalog-section-list-picture").forEach(x=>x.click())')
            }
        }
        )

    async def parse(self, response):
        page = response.meta["playwright_page"]
        links = page.locator("a.skuPropertyItemLink")
        await links.click()
        time.sleep(2)
        # print(links)
        # for link in links:
        #     await link.click()
        # title = page.locator('h1.changeName')
        title = await page.locator('h1.changeName').text_content()
        print(title)
