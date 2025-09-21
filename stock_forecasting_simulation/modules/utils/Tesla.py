import requests
import re
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

from .BaseCrawler import BaseCrawler
from .price_parser import extract_price

# 테슬라 주가

class Tesla(BaseCrawler):
    def __init__(self):
        super().__init__('tesla')

    # 수집 대상 웹페이지 요청
    def fetch_data(self):
        # self.html = requests.get('').text
        url = 'https://m.stock.naver.com/worldstock/stock/TSLA.O/total'
        wait_selector = (By.CLASS_NAME, 'GraphMain_price__H72B2')
        super().fetch_data(url, wait_selector)

    def parse_data(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        tesla_price = soup.select_one('strong.GraphMain_price__H72B2')
        
        price = 0.0
        if tesla_price:
            price = extract_price(tesla_price.text)

        self.data = {'tesla_price' : price}
        