import requests
import re
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

from .BaseCrawler import BaseCrawler
from .price_parser import extract_price

# Kakao 주가

class Kakao(BaseCrawler):
    def __init__(self):
        super().__init__('kakao')

    # 수집 대상 웹페이지 요청
    def fetch_data(self):
        # self.html = requests.get('https://finance.naver.com/item/main.naver?code=035720').text
        url = 'https://finance.naver.com/item/main.naver?code=035720'
        wait_selector = (By.CLASS_NAME, 'no_today')
        super().fetch_data(url, wait_selector)

    def parse_data(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        kakao_price = soup.select_one('p.no_today')
        
        price = 0.0
        if kakao_price:
            price = extract_price(kakao_price.text)

        self.data = {'kakao_price' : price}
