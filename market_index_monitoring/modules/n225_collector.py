import requests
from bs4 import BeautifulSoup
from .base_collector import BaseCollector

# 니케이 225

class N225Collector(BaseCollector):
    def __init__(self):
        super().__init__('N225')

    def fetch(self):
        self.html = requests.get('https://finance.naver.com/world/sise.naver?symbol=NII@NI225').text

    def parse(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        n225_elem = soup.select_one('#content > div.rate_info > div.today > p.no_today')
        self.data = {
            'n225_index' : float(n225_elem.text.replace(",","").replace("원","")) if n225_elem else 0.0
        }
    
    def to_prometheus_format(self):
        lines = []
        for key, value in self.data.items():
            metric_name = f"n225_{key}".replace(".", "_")
            lines.append(f"{metric_name} {value}")
        return '\n'.join(lines) + '\n'
