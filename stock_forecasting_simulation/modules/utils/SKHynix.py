import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from .BaseCrawler import BaseCrawler

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
        '''
        self.data = {
            'skhynix_price' : float(skhynix_price.text.replace(',', '').replace('원', '')) if skhynix_price else 0.0
        }
        '''
        price = float(
            skhynix_price.text.strip().split('KRW')[0].replace(',', '')
        ) if skhynix_price else 0.0
        self.data = {'skhynix_price' : price}
    
    '''
    def prometheus_format(self):
        lines = []
        for key, value in self.data.items():
            metric = f'skhynix_{key}'.replace('.', '')
            lines.append(f'{metric} {value}')
        return '\n'.join(lines) + '\n'
    '''
    