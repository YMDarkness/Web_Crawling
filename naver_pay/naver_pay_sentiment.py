import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from naver_pay_wordcloud import naver_pay_news_wordcloud

#감성점수 이동평균 및 히스토그램
def plot_sentiment_trend(df_naver, sentiment_dict):
    #감성점수 계산
    df_naver['감성점수'] = df_naver['제목'].apply(
        lambda title: sum(sentiment_dict.get(word, 0) for word in title.split())
    )

    #날짜 정리
    df_naver['시간'] = pd.to_datetime(df_naver['시간'])
    df_naver['날짜'] = df_naver['시간'].dt.date

    #날짜별 평균 감성점수 집계
    df_daily = df_naver.groupby('날짜')['감성점수'].mean().reset_index()
    df_daily['날짜'] = pd.to_datetime(df_daily['날짜']) #다시 데이터프레임 형태로

    #이동평균
    df_daily['3일_이동평균'] = df_daily['감성점수'].rolling(window=3).mean()
    df_daily['5일_이동평균'] = df_daily['감성점수'].rolling(window=5).mean()

    #시각화
    plt.figure(figsize=(12, 4))
    plt.rc('font', family='Malgun Gothic')  # 윈도우 기본 폰트 설정
    plt.rcParams['axes.unicode_minus'] = False  # 마이너스 부호 깨짐 방지
    plt.plot(df_daily['날짜'], df_daily['감성점수'], marker='o', label='일일_평균_감성점수', alpha=0.7)
    plt.plot(df_daily['날짜'], df_daily['3일_이동평균'], linestyle='--', color='orange', label='3일_이동평균')
    plt.plot(df_daily['날짜'], df_daily['5일_이동평균'], linestyle='-', color='green', label='5일_이동평균')
    plt.axhline(y=0, color='gray', linestyle='--') #중립기준
    plt.title('날짜별 평균 감성점수 및 이동평균')
    plt.xlabel('날짜')
    plt.ylabel('평균 감성점수')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    #히스토그램
    plt.figure(figsize=(12, 4))
    plt.hist(df_naver['감성점수'], bins='auto', color='skyblue', edgecolor='black')
    plt.title('감성점수 분포도(히스토그램)')
    plt.xlabel('감성점수')
    plt.ylabel('데이터(뉴스) 수')
    plt.grid(True)
    plt.show()

    return df_daily
