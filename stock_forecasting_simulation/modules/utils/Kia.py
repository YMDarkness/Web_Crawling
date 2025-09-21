import requests
import re
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

from .BaseCrawler import BaseCrawler
from .price_parser import extract_price

# 기아 주가

class Kia(BaseCrawler):
    def __init__(self):
        super().__init__('kia')

    # 수집 대상 웹페이지 요청
    def fetch_data(self):
        # self.html = requests.get('https://finance.naver.com/item/main.naver?code=000270').text
        url = 'https://finance.naver.com/item/main.naver?code=000270'
        wait_selector = (By.CLASS_NAME, 'no_today')
        super().fetch_data(url, wait_selector)

    def parse_data(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        kia_price = soup.select_one('p.no_today')
        
        price = 0.0
        if kia_price:
            price = extract_price(kia_price.text)

        self.data = {'kia_price' : price}
