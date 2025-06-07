import requests
from bs4 import BeautifulSoup
from .base_collector import BaseCollector

# 증권 뉴스 수집기

class NewsCollector(BaseCollector):
    def __init__(self):
        super().__init__('news')

    # 수집 대상 웹페이지 요청
    def fetch(self):
        self.html = requests.get('https://finance.naver.com/news/mainnews.naver').text

    # HTML 파싱 및 주요 뉴스 데이터 추출
    def parse(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        news_elem = soup.select_one('dd.articleSubject a')
        
        self.data = {
            f'헤드라인_{i+1}' : news_elem.text.strip()
            for i, news_elem in enumerate(news_elem[:5]) # 상위 5개 뉴스 노출
        }
