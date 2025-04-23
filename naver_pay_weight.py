import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
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

#CSV 파일을 불러와 추가 저장 (기존 데이터 유지 & 새 데이터 추가)
'''
변경된 점

pd.read_csv()로 기존 CSV 파일을 불러오기
기존 데이터가 있을 경우 새로운 데이터와 병합하여 저장
to_csv()로 덮어쓰기하여 최신 상태 유지
기존 데이터가 있다면 번호 자동 증가 (중복 방지)
'''
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

'''
기존 CSV 파일 불러오기

os.path.exists(filename)을 사용하여 파일이 존재하는지 확인
파일이 있으면 pd.read_csv()로 기존 데이터를 불러옴
없으면 새로운 빈 DataFrame 생성
새로운 뉴스 데이터 추가
titles 리스트에서 기사 제목을 추출하여 새로운 리스트 new_data에 저장
enumerate()를 활용해 기존 데이터 개수를 고려하여 번호를 자동 증가
기존 데이터 + 새로운 데이터 병합
pd.concat([df_existing, df_new], ignore_index=True)를 사용해 기존 데이터와 새로운 데이터 합침
ignore_index=True를 사용하여 번호(Index)를 재정렬
CSV 파일 저장
df_combined.to_csv(filename, index=False, encoding='utf-8-sig')
기존 데이터를 덮어쓰기하여 최신 뉴스가 계속 추가되도록 함

결과:
이제 naver_pay_graph_score.csv 파일이 지속적으로 업데이트되며, 기존 데이터를 유지하면서도 새로운 뉴스 제목을 추가할 수 있음
'''

#데이터 전처리
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

#감성 단어 사전에 가중치 부여
weigthed_positive_words = {
    '성장': 2, '상승': 1, '호재': 2, '기대': 1, '안정': 2, 
    '장세': 1, '반등': 1, '흑자': 2, '상장': 1, '전환': 1, '제동': 1, '들뜬': 1, '호가': 2
}

weigthed_negative_words = {
    '하락': -1, '위기': -2, '손실': -1, '불안': -2, '적자': -1, '경고': -2, '실패': -1, 
    '매수': -1, '포기': -1, '저점': -1, '폭락': -3, '적기': -2, '피해': -1, '오류': -1, 
    '충돌': -1, '장애': -1, '압박': -1
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

#감성 점수 계싼 후 데이터프레임에 추가
df['감성 점수'] = df['제목'].apply(calculate_weighted_sentiment_score)

'''
긍정 & 부정 단어에 가중치 적용

감성 사전에서 긍정적인 단어(예: "성장", "호재")는 높은 점수 부여
부정적인 단어(예: "하락", "위기")는 높은 가중치를 주어 부정적인 감성 반영
감성 점수 계산 함수
calculate_weighted_sentiment_score(title) 함수를 사용하여 제목 내 단어를 비교 후 점수 계산
제목 안에 포함된 단어에 따라 감성 점수가 결정됨
각 뉴스 제목의 감성 점수를 데이터프레임에 추가
df['감성 점수'] = df['제목'].apply(calculate_weighted_sentiment_score)
이를 통해 각 뉴스 제목의 감성 점수가 기록됨

결과:
각 뉴스 제목에 대해 감성 점수가 계산되었으며, 긍정적인 뉴스는 높은 점수, 부정적인 뉴스는 낮은 점수를 가짐
'''

# 날짜별 평균 감성 점수 계산
daily_sentiment = df.groupby("시간")["감성 점수"].mean()

# 이동 평균(3일, 5일) 추가
daily_sentiment_ma3 = daily_sentiment.rolling(window=3).mean()
daily_sentiment_ma5 = daily_sentiment.rolling(window=5).mean()

# 그래프 시각화
plt.figure(figsize=(10, 5))
plt.plot(daily_sentiment.index, daily_sentiment.values, marker='o', linestyle='-', color='b', label="일일 감성 점수")
plt.plot(daily_sentiment_ma3.index, daily_sentiment_ma3.values, linestyle='--', color='r', label="3일 이동 평균")
plt.plot(daily_sentiment_ma5.index, daily_sentiment_ma5.values, linestyle='-.', color='g', label="5일 이동 평균")

plt.axhline(y=0, color='gray', linestyle='--')  # 중립 기준선
plt.xlabel("날짜")
plt.ylabel("평균 감성 점수")
plt.title("날짜별 뉴스 감성 점수 변화 (이동 평균 적용)")
plt.legend()
plt.xticks(rotation=45)
plt.grid()
plt.show()

'''
날짜별 감성 점수 평균 계산

df.groupby("시간")["감성 점수"].mean()
같은 날짜에 여러 뉴스가 있을 경우, 평균 감성 점수 계산
이동 평균 적용
daily_sentiment.rolling(window=3).mean() → 3일 이동 평균 계산
daily_sentiment.rolling(window=5).mean() → 5일 이동 평균 계산
이동 평균을 적용하면 단기적인 변동성을 줄이고 감성 점수 흐름을 부드럽게 확인 가능
그래프 시각화
파란색 실선: 일일 감성 점수
빨간색 점선: 3일 이동 평균
초록색 점선: 5일 이동 평균
plt.axhline(y=0, color='gray', linestyle='--')로 중립 기준선 표시

결과:
뉴스 감성 점수가 날짜별로 어떻게 변하는지 한눈에 볼 수 있으며, 이동 평균을 활용해 감성 흐름을 예측할 수 있음
'''
