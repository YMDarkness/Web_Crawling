import requests
import re
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

from .BaseCrawler import BaseCrawler
from .price_parser import extract_price

# SK하이닉스 주가

class SKHynix(BaseCrawler):
    def __init__(self):
        super().__init__('skhynix')

    # 수집 대상 웹페이지 요청
    def fetch_data(self):
        # self.html = requests.get('https://finance.naver.com/item/main.naver?code=000660').text
        url = 'https://finance.naver.com/item/main.naver?code=000660'
        wait_selector = (By.CLASS_NAME, 'no_today')
        super().fetch_data(url, wait_selector)
    
    def parse_data(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        skhynix_price = soup.select_one('p.no_today')
        
        price = 0.0
        if skhynix_price:
            price = extract_price(skhynix_price.text)

        self.data = {'skhynix_price' : price}