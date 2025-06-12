import requests
from bs4 import BeautifulSoup
from .base_collector import BaseCollector

# 다우존스 데이터 수집

class DJICollector(BaseCollector):
    def __init__(self):
        super().__init__('DJI')

    def fetch(self):
        self.html = requests.get('https://finance.naver.com/world/sise.naver?symbol=DJI@DJI').text

    def parse(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        dji_elem = soup.select_one('#content > div.rate_info > div.today > p.no_today')
        self.data = {
            'dji_index' : float(dji_elem.text.replace(",", "").replace("원", "")) if dji_elem else 0.0
        }

    def to_prometheus_format(self):
        lines = []
        for key, value in self.data.items():
            metric_name = f"dji_{key}".replace(".", "")
            lines.append(f"{metric_name} {value}")
        return '\n'.join(lines) + '\n'
