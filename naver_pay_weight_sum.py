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

#감성 점수 누적 합산
df['누적 감성 점수'] = df['감성 점수'].cumsum()
#날짜별로 감성 점수를 계속 더해가면서 변화를 확인
#긍정적인 뉴스가 많으면 누적 감성 점수가 계속 증가
#부정적인 뉴스가 많으면 누적 감성 점수가 감소
'''
활용

특정 시점 이후 뉴스 분위기의 장기적인 변화(트렌드)를 알 수 있다
예를 들어, 감성 점수가 지속적으로 하락하면 해당 기간 동안 부정적인 뉴스가 많았다는 의미미
'''

#부정 뉴스 비율 계산
negative_ratio = (df['감성 점수'] < 0).mean() * 100
#감성 점수가 음수인 뉴스 비율을 백분율로 변환
#df['감성 점수'] < 0 → 감성 점수가 음수(부정적인 뉴스)인 행만 True
#.mean() → 전체 뉴스 중에서 부정 뉴스가 차지하는 비율을 계산
#* 100 → 퍼센트 값으로 변환
'''
활용

특정 기간 동안 전체 뉴스 중에서 부정적인 뉴스의 비율을 파악할 수 있음
부정 뉴스 비율이 갑자기 높아지면 시장 분위기가 악화되었다고 해석 가능능
'''

#부정 뉴스 비율 시각화 (파이 차트 예제)
plt.figure(figsize=(5, 5))
plt.pie([negative_ratio, 100 - negative_ratio], labels=['부정 뉴스', '긍정/중립 뉴스'], autopct='%1.1f%%', colors=['red', 'blue'])
plt.title('부정 뉴스 비율')
plt.show()
#negative_ratio와 100 - negative_ratio를 리스트로 만들어 전달
#labels=['부정 뉴스', '긍정/중립 뉴스'] → 두 가지 범주로 구분
#autopct='%1.1f%%' → 퍼센트 값 표시
#colors=['red', 'blue'] → 부정 뉴스(빨강), 긍정/중립 뉴스(파랑)
'''
활용

시각적으로 부정 뉴스의 비율을 쉽게 확인할 수 있음
특정 시점에서 부정 뉴스 비율이 급증했다면 그 원인을 분석할 수 있음
'''

'''
긍정, 부정, 중립 나누기

negative_ratio = (df['감성 점수'] < 0).mean() * 100  # 부정 뉴스 비율
positive_ratio = (df['감성 점수'] > 0).mean() * 100  # 긍정 뉴스 비율
neutral_ratio = (df['감성 점수'] == 0).mean() * 100  # 중립 뉴스 비율

부정 뉴스: 감성 점수가 0보다 작을 때
긍정 뉴스: 감성 점수가 0보다 클 때
중립 뉴스: 감성 점수가 0일 때

plt.figure(figsize=(5, 5))
plt.pie(
    [negative_ratio, positive_ratio, neutral_ratio], 
    labels=['부정 뉴스', '긍정 뉴스', '중립 뉴스'], 
    autopct='%1.1f%%', 
    colors=['red', 'blue', 'green']
)
plt.title("뉴스 감성 비율")
plt.show()

labels=['부정 뉴스', '긍정 뉴스', '중립 뉴스']
colors=['red', 'blue', 'green']
빨강: 부정 뉴스
파랑: 긍정 뉴스
초록: 중립 뉴스

긍정 뉴스 비율이 많으면? → 시장 분위기가 좋음
부정 뉴스 비율이 많으면? → 시장 분위기가 나쁨
중립 뉴스 비율이 많으면? → 모호한 시기일 수도 있음
'''
