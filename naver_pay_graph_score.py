import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import pandas as pd
import os
from konlpy.tag import Okt
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud

#크롤링
url = f"https://finance.naver.com/news/mainnews.naver"
headers = {'User-Agent' : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

response = requests.get(url, headers=headers)
response.raise_for_status()

soup = BeautifulSoup(response.text, 'html.parser')
titles = soup.select("dd.articleSubject a")

timeline = datetime.today().strftime("%Y-%m-%d")
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

#형태소 분석
okt = Okt()

#명사 추출
nouns = okt.nouns(text)

#감성 사전
positive_words = ['성장', '상승', '호재', '기대', '안정', '장세', '반등', '흑자', '상장', '전환', '제동', '들뜬', '호가']
negative_words = ['하락', '위기', '손실', '불안', '적자', '경고', '실패', '매수', '포기', '저점', '폭락', '적기', '피해', '오류', '충돌', '장애', '압박']

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

#감성 단어 빈도 그래프
positive_count = Counter(positive_nouns)
negative_count = Counter(negative_nouns)

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

# 기사 제목별 감성 점수 계산
def calculate_sentiment_score(title):
    score = 0
    for word in positive_words:
        if word in title:
            score += 1
    for word in negative_words:
        if word in title:
            score -= 1
    return score
'''
기능
뉴스 기사 제목(title)을 입력받아 감성 점수를 계산하는 함수

positive_words 리스트에 있는 단어가 포함되면 +1
negative_words 리스트에 있는 단어가 포함되면 -1
감성 점수를 합산하여 최종적으로 반환
'''

# 감성 점수 계산 후 데이터프레임에 추가
df["감성 점수"] = df["제목"].apply(calculate_sentiment_score)
#df["제목"]의 각 행에 대해 calculate_sentiment_score() 함수를 적용하여 새로운 "감성 점수" 컬럼을 추가

# 날짜별 평균 감성 점수 계산
daily_sentiment = df.groupby("시간")["감성 점수"].mean()
'''
기능
df.groupby("시간"): "시간" 컬럼 기준으로 데이터를 그룹화
["감성 점수"].mean(): 해당 날짜(시간)의 감성 점수 평균 계산
'''

# 날짜별 감성 점수 변화 그래프 시각화
plt.figure(figsize=(10, 5))
plt.plot(daily_sentiment.index, daily_sentiment.values, marker='o', linestyle='-', color='b')
plt.axhline(y=0, color='gray', linestyle='--')  # 중립 기준선
plt.xlabel("날짜")
plt.ylabel("평균 감성 점수")
plt.title("날짜별 뉴스 감성 점수 변화")
plt.xticks(rotation=45)
plt.grid()
plt.show()
'''
그래프 주요 내용
plt.plot()을 이용해 날짜별 감성 점수 변화를 선 그래프로 표현
marker='o' → 점 추가 (각 날짜별 감성 점수)
linestyle='-' → 선을 연결하여 변화 추세 확인
plt.axhline(y=0, color='gray', linestyle='--') → 0 기준선 추가 (긍정/부정 감성 구분)
plt.xticks(rotation=45) → 날짜 가독성 향상을 위해 X축 라벨 회전

뉴스 기사 제목을 분석하여 감성 점수를 수치화
날짜별 감성 점수의 변화를 시각화하여 추세 분석 가능
긍정적/부정적 감성의 변화가 있는 날을 쉽게 확인 가능
'''
