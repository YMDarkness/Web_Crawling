import requests
from bs4 import BeautifulSoup
from .base_collector import BaseCollector

# WTI (서부 텍사스 중질유)

class WTICollector(BaseCollector):
    def __init__(self):
        super().__init__('wti')

    def fetch(self):
        self.html = requests.get('https://finance.naver.com/marketindex/').text

    def parse(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        wti_elem = soup.select_one('#oilGoldList > li > a.head.wti > div > span.value')
        self.data = {
            'wti_index' : float(wti_elem.text.replace(",", "").replace("원", "")) if wti_elem else 0.0
        }

    def to_prometheus_format(self):
        lines = []
        for key, value in self.data.items():
            metric_name = f"wti_{key}".replace(".", "_")
            lines.append(f"{metric_name} {value}")
        return '\n'.join(lines) + '\n'
