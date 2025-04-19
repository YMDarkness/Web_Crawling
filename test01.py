import requests
from bs4 import BeautifulSoup

url="https://example.com"
#크롤링할 웹사이트 url
response=requests.get(url)
#웹 페이지 가져오기

if response.status_code==200:
    soup=BeautifulSoup(response.text, "html.parser")
    #html 피싱
    print(soup.title.text)
    #웹 페이지의 제목 출력
else:
    print("웹 페이지를 가져오지 못했습니다", response.status_code)
    
    