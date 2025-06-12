import requests
from bs4 import BeautifulSoup
from .base_collector import BaseCollector

# S&P 500 데이터 수집

class SpCollector(BaseCollector):
    def __init__(self):
        super().__init__('sp')

    def fetch(self):
        self.html = requests.get('https://finance.naver.com/world/sise.naver?symbol=SPI@SPX').text

    def parse(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        sp_elem = soup.select_one('#content > div.rate_info > div.today > p.no_today')
        self.data = {
            'sp_index' : float(sp_elem.text.replace(",","").replace("원","")) if sp_elem else 0.0
        }

    def to_prometheus_format(self):
        lines = []
        for key, value in self.data.items():
            metric_name = f"sp_{key}".replace(".","_")
            lines.append(f"{metric_name} {value}")
        return '\n'.join(lines) + '\n'
