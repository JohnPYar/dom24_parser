from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

url = 'https://www.panda-panel.ru/catalog/pvkh_paneli/dlya_vann/parizh.html'

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
