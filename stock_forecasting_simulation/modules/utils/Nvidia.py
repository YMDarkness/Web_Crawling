import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from .BaseCrawler import BaseCrawler

# 엔비디아 주가

class Nvidia(BaseCrawler):
    def __init__(self):
        super().__init__('nvidia')

    # 수집 대상 웹페이지 요청
    def fetch_data(self):
        # self.html = requests.get('').text
        url = 'https://m.stock.naver.com/worldstock/stock/NVDA.O/total'
        wait_selector = (By.CLASS_NAME, 'GraphMain_price__H72B2')
        super().fetch_data(url, wait_selector)

    def parse_data(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        nvidia_price = soup.select_one('strong.GraphMain_price__H72B2')
        '''
        self.data = {
            'nvidia_price' : 
            float(nvidia_price.text.replace(',','')
                  .replace('원', '')) if nvidia_price else 0.0
        }
        '''
        price = float(
            nvidia_price.text.strip().split('USD')[0].replace(',', '')
        ) if nvidia_price else 0.0
        self.data = {'nvidia_price' : price}

    '''
    def prometheus_format(self):
        lines = []
        for key, value in self.data.items():
            metric = f'nvidia_{key}'.replace('.', '')
            lines.append(f'{metric} {value}')
        return '\n'.join(lines) + '\n'
    '''
