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

#형태소 분석 및 명사 추출
okt = Okt()
nouns = okt.nouns(text)

#감성 사전
positive_words = ['성장', '상승', '호재', '기대', '안정', '장세', '반등', '흑자', '상장',
                   '전환', '제동', '들뜬', '호가', '회복', '흥행', '대성공', '급등']
negative_words = ['하락', '위기', '손실', '불안', '적자', '경고', '실패', '매수', '포기',
                   '저점', '폭락', '적기', '피해', '오류', '충돌', '장애', '압박', '급락']

#필터링
positive_nouns = [word for word in nouns if word in positive_words]
negative_nouns = [word for word in nouns if word in negative_words]

#한 글자 단어 제외
nouns = [word for word in nouns if len(word) > 1]

#단어 빈도수 계산
count = Counter(nouns)

#워드 클라우드 및 시각화
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
    for word, weigth in weigthed_positive_words.items():
        if word in title:
            score += weigth
    for word, weigth in weigthed_negative_words.items():
        if word in title:
            score += weigth #부정 단어는 이미 음수라서 더함
    return score

#감성 점수 계산 후 데이터프레임에 추가
df['감성 점수'] = df['제목'].apply(calculate_weighted_sentiment_score)

# 날짜별 평균 감성 점수 계산
daily_sentiment = df.groupby("시간")["감성 점수"].mean()

#감성 점수 누적 합산
df['누적 감성 점수'] = df['감성 점수'].cumsum()

#부정 뉴스 비율 계산
negative_ratio = (df['감성 점수'] < 0).mean() * 100

# '시간' 컬럼을 날짜 형식으로 변환
df['시간'] = pd.to_datetime(df['시간'])

# 요일 정보 추가
df['요일'] = df['시간'].dt.day_name()  # 영어 ('Monday', 'Tuesday' 등)
# df['요일'] = df['시간'].dt.dayofweek  # 숫자로 요일 표현 (0=월요일, 6=일요일)
# dt.day_name()을 사용하여 'Monday', 'Tuesday' 등의 요일 정보를 데이터프레임에 추가

# 요일별 감성 점수 평균 계산
weekly_sentiment = df.groupby('요일')['감성 점수'].mean()

# 요일 순서 정렬 (월~일)
weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
weekly_sentiment = weekly_sentiment.reindex(weekday_order)
# groupby('요일')로 요일별 감성 점수를 계산하고, 
# reindex(weekday_order)로 요일 순서를 월요일~일요일 순서로 정리

# 한글 폰트 설정
plt.rc('font', family='Malgun Gothic')  # 윈도우 기본 폰트 설정
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 부호 깨짐 방지

# 막대 그래프 시각화
plt.figure(figsize=(10, 5))
plt.bar(weekly_sentiment.index, weekly_sentiment.values, color='skyblue')

# 그래프 설정
plt.xlabel("요일")
plt.ylabel("평균 감성 점수")
plt.title("요일별 평균 감성 점수 분석")
plt.axhline(y=0, color='gray', linestyle='--')  # 중립 기준선
# axhline(y=0, color='gray', linestyle='--')
# 0을 기준선으로 표시하여 부정/긍정 여부를 쉽게 파악 
plt.grid(axis='y')

# 값 표시
for i, v in enumerate(weekly_sentiment):
    plt.text(i, v + 0.1, f"{v:.2f}", ha='center', fontsize=10)
# plt.text()를 이용해 각 막대 위에 감성 점수를 표시

plt.show()
