import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import pandas as pd
import re
import os
from konlpy.tag import Okt
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud

#크롤링
url = f"https://finance.naver.com/news/mainnews.naver"

headers = {'User-Agent' : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

repsonse = requests.get(url, headers=headers)
repsonse.raise_for_status()

soup = BeautifulSoup(repsonse.text, 'html.parser')

titles = soup.select("dd.articleSubject a")

tiemline = datetime.today().strftime("%Y-%m-%d")

filename = f"naver_pay_graph.csv"

#파일이 존재하면 'a'로 파일을 열고, 존재하지 않으면 'w'로 파일을 열어서 데이터를 저장
#a = append
#w = write
mode = 'a' if os.path.exists(filename) else 'w'

with open(filename, mode=mode, encoding='utf-8-sig', newline='') as file:
    writer = csv.writer(file)

    #파일이 없으면 헤더를 추가
    if mode == 'w':
        writer.writerow(["번호", "제목", "시간"])

    for idx, title in enumerate(titles, 1):
        article = title.get_text(strip=True)
        writer.writerow([idx, article, tiemline])
'''
기존 방식에서는 매번 CSV 파일을 덮어쓰기('w' 모드)로 저장했지만,
현재 코드는 파일이 존재하면 추가('a') 모드로 저장하도록 변경
덕분에 기존 데이터에 새로운 데이터를 계속 누적시킬 수 있다

'w' 모드일 경우에만 헤더 추가
기존 데이터가 있을 때는 헤더를 반복해서 쓰지 않음

기사 제목을 1번부터 번호를 매기며 저장
텍스트에서 불필요한 공백 제거 (strip())
날짜 정보도 함께 저장

기존 데이터 손실 없이 누적 저장이 가능해졌고,
중복된 헤더 문제도 해결되었기 때문에,
데이터 분석 및 감성 분석에 더 효율적인 방식으로 개선
'''

print(f"데이터 크롤링 및 {filename} 저장 완료")

#데이터 전처리
#데이터 프레임으로 중복 제거
df = pd.read_csv("naver_pay_graph.csv", encoding='utf-8-sig')

df = df.drop_duplicates()
df.to_csv("naver_pay_graph.csv", index=False, encoding='utf-8-sig')

print(f"{filename} 데이터 누적 및 중복 제거 완료")

text = " ".join(df["제목"])

#공백 및 특수문자 제거
#한글과 공백만 남기기
#clean_text = re.sub(r"[^가-힣\s]",'', text)
#다중 공백 제거
#clean_text = re.sub(r"\s+", " ", clean_text).strip()

#형태소 분석
okt = Okt()

#명사 추출
nouns = okt.nouns(text)

#감성 사전
positive_words = ['성장', '상승', '호재', '기대', '안정', '장세', '반등', '흑자', '상장', '전환', '제동']
negative_words = ['하락', '위기', '손실', '불안', '적자', '경고', '실패', '매수', '포기', '저점', '폭락', '적기', '피해']

#필터링
positive_nouns = [word for word in nouns if word in positive_words]
negative_nouns = [word for word in nouns if word in negative_words]

#한 글자 단어 제외
nouns = [word for word in nouns if len(word) > 1]

#단어 빈도수 계산
count = Counter(nouns)

#워드클라우드 시각화
wordcloud = WordCloud(
    font_path="C:/Windows/Fonts/malgun.ttf", background_color="white", width=800, height=400).generate_from_frequencies(count)

plt.figure(figsize=(10, 5))
# 한글 폰트 설정
plt.rc('font', family='Malgun Gothic')  # 윈도우 기본 폰트 설정
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 부호 깨짐 방지'
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('전체 워드클라우드')
plt.show()

#감성 단어 빈도 그래프
positive_count = Counter(positive_nouns)
negative_count = Counter(negative_nouns)

#감성 단어 빈도수 데이터프레임 변환
#감성 분석 결과를 데이터프레임으로 변환하고, 빈도수 기준으로 내림차순 정렬하는 역할
'''
Counter 객체는 딕셔너리 형태
.items() 메서드를 통해 각 단어와 빈도수를 튜플 형태로 추출

Pandas 데이터프레임으로 변환
컬럼명 '단어'와 '빈도수'를 지정

빈도수 기준으로 내림차순 정렬
'''
positive_df = pd.DataFrame(list(positive_count.items()), columns=['단어', '빈도수']).sort_values(by='빈도수', ascending=False)
negative_df = pd.DataFrame(list(negative_count.items()), columns=['단어', '빈도수']).sort_values(by='빈도수', ascending=False)

#긍정 단어 시각화
plt.figure(figsize=(8, 4))
# 한글 폰트 설정
plt.rc('font', family='Malgun Gothic')  # 윈도우 기본 폰트 설정
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 부호 깨짐 방지
plt.bar(positive_df['단어'], positive_df['빈도수'], color='blue')
plt.title('긍정 단어 빈도수')
plt.xticks(rotation=45)
plt.show()

#부정 단어 시각화
plt.figure(figsize=(8, 4))
# 한글 폰트 설정
plt.rc('font', family='Malgun Gothic')  # 윈도우 기본 폰트 설정
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 부호 깨짐 방지
plt.bar(negative_df['단어'], negative_df['빈도수'], color='red')
plt.title('부정 단어 빈도수')
plt.xticks(rotation=45)
plt.show()
