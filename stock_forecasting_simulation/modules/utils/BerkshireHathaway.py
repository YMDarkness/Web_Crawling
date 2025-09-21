import requests
import re
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

from .BaseCrawler import BaseCrawler
from .price_parser import extract_price

# 버크셔 헤서웨이 주가

class BerkshireHathaway(BaseCrawler):
    def __init__(self):
        super().__init__('berkshire_hathaway')

    # 수집 대상 웹페이지 요청
    def fetch_data(self):
        # self.html = requests.get('').text
        url = 'https://m.stock.naver.com/worldstock/stock/BRKa/total'
        wait_selector = (By.CLASS_NAME, 'GraphMain_price__H72B2')
        super().fetch_data(url, wait_selector)

    def parse_data(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        berkshire_price = soup.select_one('strong.GraphMain_price__H72B2')
        
        price = 0.0
        if berkshire_price:
            price = extract_price(berkshire_price.text)

        self.data = {'berkshire_hathaway_price' : price}
