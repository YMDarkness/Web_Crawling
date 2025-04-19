import requests
import csv
from bs4 import BeautifulSoup

#경제 뉴스 크롤링
url = f"https://finance.naver.com/news/mainnews.naver"

#User-Agent, 요청 보내기 및 HTML 파싱
header = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
response = requests.get(url, headers=header)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

keywords = soup.select("dd.articleSubject a")

'''
#개발자 도구에서 크롤링할 태그 찾는 방법
#크롬 개발자 도구 열기
#뉴스 제목이 있는 부분 찾기
    페이지에서 가져오고 싶은 뉴스 제목을 마우스 우클릭 > 검사(inspect) 선택
    or 개발자 도구에서 elements 탭을 열고 뉴스 제목을 검색
#관련 태그 확인
    <a> 태그 안에 뉴스 제목이 들어 있는지 확인
    <div>, <span> 등의 부모 태그 안에 뉴스 제목이 있는지 확인
    class, id 속성이 있는지 확인

#css 선택자를 찾는 기준
#가져오려는 내용(텍스트, 링크 등)이 들어있는 태그
    <a>, <h1>, <h2>, <p> 등
#태그를 식별할 수 있는 클래스 또는 ID
    class="articleSubject" 같은 특정 클래스를 가진 태그가 있는지 확인
    id="newsTitle" 처럼 고유한 ID가 있는지 확인
#부모-자식 관계 고려
    특정 div 내부의 a 태그를 찾을 수도 있다

#추가 팁
    개발자 도구에서 선택자가 제대로 동작하는지 확인하는 방법
#개발자 도구에서 elemenets 탭 열기
#ctrl + shift + c 눌러 요소 선택
#ctrl + f 누르고 선택자 입력
#선택한 태그가 하이라이트되면 정확한 선택자를 찾은 것

#정리
#개발자 도구에서 원하는 요소를 찾기
#태그 안에 뉴스 제목이 있는지 확인
#고유한 class, id속성이 있는지 확인
#부모-자식 관계를 고려해서 soup.select()에 넣을 css 선택자를 만든다
#크롬 개발자 도구의 ctrl + f로 선택자가 맞는지 테스트
'''

for idx, title in enumerate(keywords, 1):
    print(f"{idx}.{title.get_text()}")
