import requests
import re
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

from .BaseCrawler import BaseCrawler
from .price_parser import extract_price

# NAVER 주가

class Naver(BaseCrawler):
    def __init__(self):
        super().__init__('naver')

    # 수집 대상 웹페이지 요청
    def fetch_data(self):
        # self.html = requests.get('https://finance.naver.com/item/main.naver?code=035420').text
        url = 'https://finance.naver.com/item/main.naver?code=035420'
        wait_selector = (By.CLASS_NAME, 'no_today')
        super().fetch_data(url, wait_selector)

    def parse_data(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        naver_price = soup.select_one('p.no_today')
        
        price = 0.0
        if naver_price:
            price = extract_price(naver_price.text)

        self.data = {'naver_price' : price}
    