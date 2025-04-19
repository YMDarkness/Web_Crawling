import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import pandas as pd
import os
from konlpy.tag import Okt
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter

#크롤링
url = f"https://finance.naver.com/news/mainnews.naver"
headers = {'User-Agent' : 
           "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

response = requests.get(url, headers=headers)
response.raise_for_status()

soup = BeautifulSoup(response.text, 'html.parser')
titles = soup.select("dd.articleSubject a")

timeline = datetime.today().strftime('%Y-%m-%d')
filename = f'naver_pay_graph_score.csv'

#기존 파일 로드
if os.path.exists(filename):
    df_existing = pd.read_csv(filename, encoding='utf-8-sig')
else:
    df_existing = pd.DataFrame(columns=['번호', '제목', '시간'])

#새로운 데이터 수집
new_date = []
start_idx = len(df_existing) + 1  # 기존 번호 뒤부터 시작

for idx, title in enumerate(titles, start=start_idx):
    article = title.get_text(strip=True)
    new_date.append([idx, article, timeline])

#새로운 데이터를 DateFrame으로 변환
df_new = pd.DataFrame(new_date, columns=['번호', '제목', '시간'])

#기존 데이터와 새로운 데이터 합치기
df_combined = pd.concat([df_existing, df_new], ignore_index=True)

# 제목 기준으로 중복 제거 (번호나 시간은 다르더라도 같은 뉴스는 제거)
df_combined = df_combined.drop_duplicates(subset='제목')

#최종 데이터 저장 (덮어쓰기)
df_combined.to_csv(filename, index=False, encoding='utf-8-sig')

print('csv 파일 데이터 업데이트 완료')

df = pd.read_csv('naver_pay_graph_score.csv', encoding='utf-8-sig')
df = df.drop_duplicates()
df.to_csv('naver_pay_graph_score.csv', encoding='utf-8-sig', index=False)

print(f'{filename} 데이터 누적 및 중복 제거 완료')

text = ' '.join(df['제목'])
okt = Okt()
nouns = okt.nouns(text)

#감성 사전
positive_words = ['성장', '상승', '호재', '기대', '안정', '장세', '반등', '흑자', '상장',
                   '전환', '제동', '들뜬', '호가', '회복', '흥행', '대성공', '급등']
negative_words = ['하락', '위기', '손실', '불안', '적자', '경고', '실패', '매수', '포기',
                   '저점', '폭락', '적기', '피해', '오류', '충돌', '장애', '압박', '급락']

positive_nouns = [word for word in nouns if word in positive_words]
negative_nouns = [word for word in nouns if word in negative_words]

nouns = [word for word in nouns if len(word) > 1]

count = Counter(nouns)
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

#감성 단어 사전에 가중치 부여
weigthed_positive_words = {
    '성장': 2, '상승': 1, '호재': 2, '기대': 1, '안정': 2, '장세': 1, '반등': 1,
      '흑자': 2, '상장': 1, '전환': 1, '제동': 1, '들뜬': 1, '호가': 2, '회복': 2, '흥행': 1, '대성공': 3, '급등': 1
}

weigthed_negative_words = {
    '하락': -1, '위기': -2, '손실': -1, '불안': -2, '적자': -1, '경고': -2, '실패': -1, 
    '매수': -1, '포기': -1, '저점': -1, '폭락': -3, '적기': -2, '피해': -1, '오류': -1, '충돌': -1, '장애': -1, '압박': -1, '급락': -1
}

#가중치를 반영한 감성 점수 계산 함수
def calculate_weighted_sentiment_score(title):
    score = 0
    for word, weight in weigthed_positive_words.items():
        if word in title:
            score += weight
    for word, weight in weigthed_negative_words.items():
        if word in title:
            score += weight #부정 단어는 이미 음수라서 더함
    return score

#감성 점수 계산 후 데이터프레임에 추가
df['감성 점수'] = df['제목'].apply(calculate_weighted_sentiment_score)

# 날짜별 평균 감성 점수 계산
daily_sentiment = df.groupby('시간')['감성 점수'].mean()

#감성 점수의 누적 변화
df['누적 감성 점수'] = df['감성 점수'].cumsum()
'''
cumsum() 함수

데이터를 순차적으로 더해 누적합을 계산
감성 점수가 날짜별로 쌓이는 패턴을 볼 수 있다
'''

#누적 감성 점수 시각화
plt.figure(figsize=(10, 5))
plt.plot(df['시간'], df['누적 감성 점수'], marker='o', linestyle='-', color='r')

#그래프 설정
plt.axhline(y=0, color='gray', linestyle='--') #기준선
plt.xlabel('날짜')
plt.ylabel('누적 감성 점수')
plt.title('시간 흐름에 따른 누적 감성 점수 변화')
plt.xticks(rotation=45)
plt.grid()
plt.show()
'''
plt.plot() -> 시간 흐름에 따른 감성 점수 누적 변화를 선 그래프로 표현
axhline(y=0, color='gray', linestyle='--') -> 감성 점수가 양/음으로 나뉘는 기준선 표시
xticks(rotation=45) -> 날짜가 가독성 좋게 기울어짐
'''

#이동 평균을 이용한 감성 점수 트렌드 분석
#날짜 기준 정렬
#날짜 데이터를 datetime 형식으로 변환
df['시간'] = pd.to_datetime(df['시간'])
df = df.sort_values(by='시간')
'''
datetime 변환 & 정렬 -> 날짜 데이터를 올바른 순서로 정렬
'''

#이동 평균 계산
#이동 평균을 예측할 때 결측값(NA)가 발생할 가능성이 있음
#rolling(window=7).mean()을 적용하면 7일 이전 데이터가 없을 경우 결측값이 발생
#dropna()를 사용해 제거할 수 있음
df['감성 점수 이동 평균'] = df['감성 점수'].rolling(window=7, min_periods=1).mean()
#최소 1개의 값이라도 있으면 이동 평균을 계산할 수 있어, 초반 데이터 손실을 방지할 수 있다
'''
rolling(window=7).mean() -> 7일 단위 평균값을 계산
min_periods=1 -> 최소 1개의 데이터가 있으면 평균 계산
'''

#감성 점수 변화 시각화(원본 + 이동 평균)
plt.figure(figsize=(10, 5))
#marker 색상과 스타일을 추가해 가독성을 높이는 방법
plt.plot(df['시간'], df['감성 점수'], marker='o', linestyle='-', color='blue', alpha=0.5, label='일일 감성 점수') #원본 데이터
plt.plot(df['시간'], df['감성 점수 이동 평균'],  linestyle='-', color='red', linewidth=2, label='7일 이동 평균') #이동 평균 데이터
#누적 감성 그래프의 y축 범위 조정
#y축 범위가 자동으로 설정되어 있어 그래프 해석에 어려움이 있음
#plt.ylim()을 사용해 적절한 범위를 설정하면 보기 편해짐짐
plt.ylim(df['누적 감성 점수'].min() - 10, df['누적 감성 점수'].max() + 10)

#그래프 설정
plt.axhline(y=0, color='gray', linestyle='--') #기준선
plt.xlabel('날짜')
plt.ylabel('감성 점수')
plt.title('날짜별 감성 점수 변화 (이동 평균 적용)')
plt.legend()
plt.xticks(rotation=45)
plt.grid()
plt.show()
'''
plt.plot() -> 두 번 사용ㅇ하여 원본 데이터(파랑)와 이동 평균(빨강)을 함께 표현
alpha=0.5 -> 원본 데이터를 반투명하여 가독성 향상
linewidth=2 -> 이동 평균 선을 더 강조
legend() -> 범례 추가
'''

#특정 날짜의 감성 점수가 높거나 낮게 나온 경우
df['날짜'] = df['시간'].dt.date  # 날짜만 추출
df['날짜'].value_counts().sort_index().plot(kind='bar', figsize=(12,5), title="날짜별 데이터 개수")
plt.xticks(rotation=45)
plt.show()
'''
df['시간'].dt.date → 시간에서 날짜만 추출하여 새로운 '날짜' 열을 생성
value_counts().sort_index().plot(kind='bar') → pandas의 내장 plot 기능을 이용하여 바로 막대그래프 생성
figsize=(12,5) → 그래프 크기 지정
title="날짜별 데이터 개수" → 그래프 제목 설정
matplotlib 없이 pandas만으로 간단하게 구현 가능
'''

#날짜별 데이터 개수 분석
# 날짜별 데이터 개수 계산
date_counts = df['시간'].value_counts().sort_index()

# 날짜별 데이터 개수 시각화
plt.figure(figsize=(10, 5))
plt.bar(date_counts.index, date_counts.values, color='purple', alpha=0.7)

# 그래프 설정
plt.xlabel('날짜')
plt.ylabel('데이터 개수')
plt.title('날짜별 데이터 개수 분포')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()
'''
value_counts() -> 각 날짜별 감성 데이터 개수 계산
bar() -> 날짜별 데이터 개수를 막대그래프로 표현
grid(axis='y', linestyle='--', alpha=0.7) -> 가로선 추가

value_counts().sort_index() → 날짜별 데이터 개수를 정렬한 후 별도 변수(date_counts)에 저장
plt.bar(x, y) → matplotlib의 bar() 함수 사용하여 막대그래프 직접 생성
color='purple', alpha=0.7 → 막대 색상 및 투명도 조절
grid(axis='y', linestyle='--', alpha=0.7) → y축 기준으로 점선 그리드 추가
matplotlib을 사용하여 세부적인 그래프 조정 가능

빠르게 시각화하고 싶다면? → pandas의 plot(kind='bar')을 사용
색상, 투명도, 그리드 등 세부 조정을 하고 싶다면? → matplotlib의 plt.bar() 사용
'''
