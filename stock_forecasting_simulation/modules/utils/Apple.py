import requests
import re
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

from .BaseCrawler import BaseCrawler
from .price_parser import extract_price

# 애플 주가

class Apple(BaseCrawler):
    def __init__(self):
        super().__init__('apple')

    # 수집 대상 웹페이지 요청
    def fetch_data(self):
        # self.html = requests.get('').text
        url = 'https://m.stock.naver.com/worldstock/stock/AAPL.O/total'
        wait_selector = (By.CLASS_NAME, 'GraphMain_price__H72B2')
        super().fetch_data(url, wait_selector)
    
    def parse_data(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        apple_price = soup.select_one('strong.GraphMain_price__H72B2')
        
        price = 0.0
        if apple_price:
            price = extract_price(apple_price.text)

        self.data = {'apple_price' : price}
    