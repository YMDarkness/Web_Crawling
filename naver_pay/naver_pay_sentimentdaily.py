import pandas as pd
from konlpy.tag import Okt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from naver_pay_sentiment import plot_sentiment_trend

def calculate_score_with_ngram(title, sentiment_dict):
    okt = Okt()
    words = okt.morphs(title)
    bigrams = [words[i] + words[i+1] for i in range(len(words)-1)]
    all_terms = words + bigrams
    return sum(sentiment_dict.get(term, 0) for term in all_terms)

#날짜별 감성점수 및 데이터(뉴스)량
def sentiment_daily_date(df_naver, df_daily, sentiment_dict):
    okt = Okt()
    
    #감성점수 계산
    df_naver['감성점수'] = df_naver['제목'].apply(
        #lambda title: sum(sentiment_dict.get(word, 0) for word in title.split())
        #lambda title: sum(sentiment_dict.get(word, 0) for word in okt.morphs(title))
        lambda title: calculate_score_with_ngram(title, sentiment_dict)
    )

    #날짜 정리
    df_naver['시간'] = pd.to_datetime(df_naver['시간'])
    df_naver['날짜'] = df_naver['시간'].dt.floor('d')

    #날짜별 감성점수 집계
    df_daily = df_naver.groupby('날짜')['감성점수'].sum().reset_index()
    df_daily['날짜'] = pd.to_datetime(df_daily['날짜'])

    #날짜별 데이터(뉴스)량 확인
    df_daily['데이터_수'] = abs(df_daily['감성점수']).cumsum()

    #부정뉴스 비율 계산
    negative_keyword = (df_daily['감성점수'] < 0).mean() * 100

    #요일 정보 추가
    df_daily['요일'] = df_naver['시간'].dt.day_name()

    #요일별 감성점수 계산
    weekly_sentiment = df_daily.groupby('요일')['감성점수'].sum()

    #요일 정렬
    weekday_sort = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekly_sentiment = weekly_sentiment.reindex(weekday_sort)

    #시각화
    plt.figure(figsize=(12, 4))
    plt.rc('font', family='Malgun Gothic')  # 윈도우 기본 폰트 설정
    plt.rcParams['axes.unicode_minus'] = False  # 마이너스 부호 깨짐 방지
    plt.bar(df_daily['날짜'], df_daily['데이터_수'], color='blue')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.xticks(rotation=45)
    plt.xlabel('요일')
    plt.ylabel('데이터 수')
    plt.title('날짜별 데이터 수')
    plt.axhline(y=0, color='gray', linestyle='--')
    plt.grid(axis='y')

    for i, v in enumerate(weekly_sentiment.values):
        plt.text(i, v + 0.1, f'{v:.2f}', ha='center', fontsize=10)
    
    print(f'부정뉴스 비율 : {negative_keyword : .2f}%')

    plt.show()

    return df_naver, df_daily
