from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

import scrapy
import html

from bs4 import BeautifulSoup as bs

url = 'https://www.panda-panel.ru/catalog/pvkh_paneli/dlya_vann/mechta.html'

options = webdriver.ChromeOptions()
# options.add_argument('--headless')

driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))

driver.get(url)

sku = driver.find_element(By.LINK_TEXT, '02510')

print(sku)

sku.click()

WebDriverWait(driver, timeout=10)

title = driver.find_element(By.XPATH, '//h1')

# soup = bs(page_source, 'html.parser')
# title = soup.find(class_='changeName').text
print(title.text)
