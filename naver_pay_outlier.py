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
import seaborn as sns

#크롤링
url = f"https://finance.naver.com/news/mainnews.naver"
headers = {'User-Agent' : 
           "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

respones = requests.get(url, headers=headers)
respones.raise_for_status()

soup = BeautifulSoup(respones.text, 'html.parser')
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
    '성장': 2, '상승': 1, '호재': 2, '기대': 1, '안정': 2, '장세': 1, '반등': 2,
      '흑자': 2, '상장': 2, '전환': 1, '제동': 1, '들뜬': 1, '호가': 2, '회복': 2, '흥행': 2, '대성공': 3, '급등': 1,
      '강세': 2, '호황': 3, '상향': 3, '유망': 2, '신뢰': 3, '견조': 2, '탄탄': 2
}

weigthed_negative_words = {
    '하락': -1, '위기': -2, '손실': -1, '불안': -2, '적자': -3, '경고': -2, '실패': -1, 
    '매수': -2, '포기': -1, '저점': -2, '폭락': -3, '적기': -2, '피해': -1, '오류': -2, '충돌': -1, '장애': -1, '압박': -2, '급락': -3,
    '약세': -2, '불황': -3, '하향': -1, '부진': -2, '불확실': -2, '침체': -3, '둔화': -2
}

#가중치를 반영한 감성 점수 계산 함수
def calculate_weighted_sentiment_score(title):
    score = 0
    for word, weigth in weigthed_positive_words.items():
        if word in title:
            score += weigth
    for word, weigth in weigthed_negative_words.items():
        if word in title:
            score += weigth #음수
    return score

#감성 점수 계산 후 데이터프레임에 추가
df['감성 점수'] = df['제목'].apply(calculate_weighted_sentiment_score)

# 날짜별 평균 감성 점수 계산
daily_sentiment = df.groupby('시간')['감성 점수'].mean()

#감성 점수의 누적 변화
df['누적 감성 점수'] = df['감성 점수'].cumsum()

#감성 점수의 분포 확인 (히스토그램)
plt.figure(figsize=(10, 5))
sns.histplot(df['감성 점수'], bins=20, kde=True, color='blue', alpha=0.6) #히스토그램 + 밀도 함수
'''
sns.histplot -> 감성 점수의 분포를 히스토그램으로 표현
bins=20 -> 20개의 구간으로 나눠서 분석
kde=True -> 감성 점수의 밀도 곡선(확률 밀도 함수)을 함께 표시
'''
plt.axvline(df['감성 점수'].mean(), color='red', linestyle='--', label='평균')
plt.axvline(df['감성 점수'].median(), color='green', linestyle='-', label='중앙값')
#axvline() -> 감성 점수의 평균(빨간색 점선), 중앙값(초록색 점선) 표시
plt.xlabel('감성 점수')
plt.ylabel('빈도')
plt.title('감성 점수의 분포')
plt.legend()
plt.grid()
plt.show()

#이상치 탐색 (박스플롯)
plt.figure(figsize=(10, 5))
sns.boxplot(y=df['감성 점수'], color='orange')
'''
sns.boxplot() -> 감성 점수의 사분위수(Q1, Q2, Q3)와 이상치를 시각화
박스 내부 : 50%의 데이터가 포함된 범위
가로선 : 중앙값 (중앙값이 한쪽으로 치우쳐 있으면 분포가 왜곡됨)
점으로 표시된 부분 : 이상치(outlier)
'''
plt.title('감성 점수의 박스플롯')
plt.ylabel('감성 점수')
plt.grid()
plt.show()

#감성 점수의 기술 통계량 확인
#감성 점수의 기술 통계량 출력 
print(df['감성 점수'].describe())
'''
df['감성 점수'].describe() -> 감성 점수의 기본 통계 정보(평균, 최댓값, 최솟값, 표준편차 등) 출력
'''

#IQR을 이용한 이상치 탐색
Q1 = df['감성 점수'].quantile(0.25) #1 사분위수
Q3 = df['감성 점수'].quantile(0.75) #3 사분위수
IQR = Q3 - Q1 #IQR (사분위 범위)

#이상치 기준 (Q1 - 1.5 * IQR, Q3 + 1.5 * IQR)
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
'''
IQR(사분위 범위)를 이용한 이상치 탐색
이상치 기준 : Q1 - 1.5 * IQR 이하 또는 Q3 + 1.5 * IQR 이상
기준을 벗어나는 데이터 출력
'''

outliers = df[(df['감성 점수'] < lower_bound) | (df['감성 점수'] > upper_bound)]
print(f'이상치 개수 : {len(outliers)}')
print(df['감성 점수'].value_counts())
print(outliers)
