from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

import scrapy
import html

from bs4 import BeautifulSoup as bs

url = 'https://www.panda-panel.ru/catalog/pvkh_paneli/dlya_vann/mechta.html'

options = webdriver.ChromeOptions()
# options.add_argument('--headless')

driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))

driver.get(url)

skus = driver.find_elements(By.CLASS_NAME, 'skuPropertyItemLink')

# print(skus)

for sku in skus:
    # driver.implicitly_wait(1000)
    # print(sku)

    sku.click()

    # driver.implicitly_wait(1000)
    time.sleep(1)

    # WebDriverWait(driver, timeout=1000)

    title = driver.find_element(By.CSS_SELECTOR, 'h1.changeName')
    # title = driver.find_element(By.XPATH, '//h1')
    # title = WebDriverWait(driver, 10000).until(lambda x: x.find_element(By.XPATH, '//h1'))

    # soup = bs(page_source, 'html.parser')
    # title = soup.find(class_='changeName').text
    print(title.text)

# sku_list = []
#
# for i in range(0, len(skus)):
#     # print(skus[i])
#     skus[i].click()
#     time.sleep(5)
#     driver.implicitly_wait(100)
#     title = driver.find_element(By.CSS_SELECTOR, 'h1.changeName')
#     sku_list.append(title.text)
#     # print(title.text)
# print(sku_list)
# skus[2].click()
# # WebDriverWait(driver, timeout=10000)
# driver.implicitly_wait(10)
# # title = driver.find_element(By.XPATH, '//h1')
# title = driver.find_element(By.CSS_SELECTOR, 'h1.changeName')
# # title = WebDriverWait(driver, 10000).until(lambda x: x.find_element(By.XPATH, '//h1'))
# print(title.text)
