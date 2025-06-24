import requests
from bs4 import BeautifulSoup
from .base_collector import BaseCollector

# 휘발유

class GasolineCollector(BaseCollector):
    def __init__(self):
        super().__init__('gasoline')

    def fetch(self):
        self.html = requests.get('https://finance.naver.com/marketindex/').text

    def parse(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        gasoline_elem = soup.select_one('#oilGoldList > li > a.head.gasoline > div > span.value')
        self.data = {
            'gasoline_index' : float(gasoline_elem.text.replace(",", "").replace("원", "")) if gasoline_elem else 0.0
        }

    def to_prometheus_format(self):
        lines = []
        for key, value in self.data.items():
            metric_name = f"gasoline_{key}".replace(".", "_")
            lines.append(f"{metric_name} {value}")
        return '\n'.join(lines) + '\n'
