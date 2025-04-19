import csv
import pandas as pd
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from wordcloud import WordCloud
import matplotlib.pyplot as plt

#크롤링 구간------------------------------------------------------------------
#크롤링 url
url = f"https://finance.naver.com/news/mainnews.naver"

#요청, User-Agent 설정, HTML 파싱
headers = {'User-Agent' : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

response = requests.get(url, headers=headers)
response.raise_for_status()

#HTML 파싱
soup = BeautifulSoup(response.text, 'html.parser')

#데이터 선택
dates = soup.select("dd.articleSubject a")

#날짜 설정
timeline = datetime.today().strftime("%Y-%m-%d")

#csv 파일 생성
filename = "naver_pay_wordcloud.csv"
with open(filename, mode="w", encoding="utf-8-sig", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["번호", "제목", "날짜"])

    for idx, date in enumerate(dates, 1):
        article = date.get_text(strip=True)
        writer.writerow([idx, article, timeline])

print(f"크롤링 완료 및 {filename}파일 생성 완료")

#데이터를 읽고 워드클라우드를 생성 및 시각화------------------------------------------------------------------
#csv 데이터 읽기
df = pd.read_csv(filename, encoding="utf-8-sig")

#'제목' 컬럼의 모든 텍스트를 하나로 합치기
#" ".join() > 데이터프레임의 '제목' 컬럼에서 텍스트를 하나로 합쳐주는 역할
text = " ".join(df["제목"])

#워드클라우드 생성
wordcloud = WordCloud(font_path="C:/Windows/Fonts/malgun.ttf", background_color="white", width=800, height=400).generate(text)
'''
워드클라우드 옵션 설정 > 폰트 및 배경색, 이미지 크기 조정
WordCloud() 클래스는 wordcloud 라이브러리에서 제공하는 텍스트 시각화 도구
주요 역할 > 텍스트 데이터를 기반으로 단어의 빈도를 분석하고, 빈도에 따라 단어의 크기를 조정하여 시각적으로 표현
매개변수
WordCloud(
    font_path=None,           # 사용할 폰트 경로 (한글 사용 시 필수)
    width=400,                # 이미지 너비
    height=200,               # 이미지 높이
    max_words=200,            # 표시할 최대 단어 수
    background_color='white', # 배경색 ('white' 또는 'black' 등)
    colormap='viridis',       # 색상 맵 ('viridis', 'plasma', 'inferno', 'magma' 등)
    stopwords=None,           # 제외할 단어 리스트 (불용어 처리)
    max_font_size=None,       # 최대 글자 크기
    min_font_size=4,          # 최소 글자 크기
    random_state=None,        # 랜덤 상태 (재현성 확보)
    contour_color='black',    # 테두리 색상
    contour_width=0,          # 테두리 두께
)

font_path: 한글을 제대로 출력하려면 시스템 내에 있는 한글 폰트를 지정 (예: C:/Windows/Fonts/malgun.ttf)
width, height: 워드클라우드의 이미지 크기 조정
max_words: 표시할 단어의 최대 개수
background_color: 배경색
stopwords: 분석에서 제외할 단어 목록 (예: '그리고', '하지만' 등)
colormap: 단어 색상 스타일 (기본값: 'viridis')
random_state: 랜덤 요소 고정 (결과 일관성 확보)
contour_color, contour_width: 단어 테두리 색상 및 두께 설정

예시)
wordcloud = WordCloud(
    font_path="C:/Windows/Fonts/malgun.ttf", 
    background_color="white", 
    width=800, 
    height=400,
    max_words=100,
    colormap="Blues",
    contour_color="black", 
    contour_width=1
).generate(text)

'''

#시각화
#시각화 > matplotlib 라이브러리를 활용하여 워드클라우드 이미지 표시
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()
#plt.savefig("naver_pay_wordcloud.png")
'''
plt.figure(figsiz=(10, 5)) > 그림(그래프) 크기 설정
plt.imshow(wordcloud, interpolation="bilinear") > 워드클라우드를 이미지 형태로 출력(interpolation="bilinear" > 부드러운 이미지 출력 방식)
plt.axis("off") > 축(x축, y축) 숨기기
plt.show() > 시각화된 결과를 화면에 출력
plt.savefig(저장할 이미지 파일명) > 이미지 파일로 저장
'''
