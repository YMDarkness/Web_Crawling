import requests
import re
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

from .BaseCrawler import BaseCrawler
from .price_parser import extract_price

# 아마존 주가

class Amazon(BaseCrawler):
    def __init__(self):
        super().__init__('amazon')

    # 수집 대상 웹페이지 요청
    def fetch_data(self):
        # self.html = requests.get('').text
        url = 'https://m.stock.naver.com/worldstock/stock/AMZN.O/overview'
        wait_selector = (By.CLASS_NAME, 'GraphMain_price__H72B2')
        super().fetch_data(url, wait_selector)

    def parse_data(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        amazon_price = soup.select_one('strong.GraphMain_price__H72B2')
        
        price = 0.0
        if amazon_price:
            price = extract_price(amazon_price.text)

        self.data = {'amazon_price': price}
