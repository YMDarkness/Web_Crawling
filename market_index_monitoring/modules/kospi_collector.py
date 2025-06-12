import requests
from bs4 import BeautifulSoup
from .base_collector import BaseCollector

# 코스피 지수 데이터 수집기

class KospiCollector(BaseCollector):
    def __init__(self):
        super().__init__('kospi')

    def fetch(self):
        self.html = requests.get("https://finance.naver.com/sise/sise_index.naver?code=KOSPI").text

    def parse(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        kospi_elem = soup.select_one('#now_value')
        self.data = {
            'kospi_index' : float(kospi_elem.text.replace(",", "").replace("원", "")) if kospi_elem else 0.0
        }

    def to_prometheus_format(self):
        lines = []
        for key, value in self.data.items():
            metric_name = f"kospi_{key}".replace(".", "_")
            lines.append(f"{metric_name} {value}")
        return '\n'.join(lines) + '\n'
