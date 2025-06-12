import requests
from bs4 import BeautifulSoup
from .base_collector import BaseCollector

# 나스닥 종합

class IXICCollector(BaseCollector):
    def __init__(self):
        super().__init__('ixic')

    def fetch(self):
        self.html = requests.get('https://finance.naver.com/world/sise.naver?symbol=NAS@IXIC').text

    def parse(self):
        soup = BeautifulSoup(self.html, 'html.parser')        
        ixic_elem = soup.select_one('#content > div.rate_info > div.today > p.no_today')
        self.data = {
            'ixic_index' : float(ixic_elem.text.replace(",","").replace("원","")) if ixic_elem else 0.0
        }

    def to_prometheus_format(self):
        lines = []
        for key, value in self.data.items():
            metric_name = f"ixic_{key}".replace(".", "_")
            lines.append(f"{metric_name} {value}")
        return '\n'.join(lines) + '\n'
