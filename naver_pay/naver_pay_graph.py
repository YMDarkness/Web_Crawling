import pandas as pd
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import gc
from konlpy.tag import Okt
import seaborn as sns

from naver_pay_sentimentdaily import sentiment_daily_date

#형태소 + 2gram 기반 감성점수 계산 함수
def calculate_score_with_ngram(title, sentiment_dict):
    if isinstance(sentiment_dict, list):
        sentiment_dict = dict(sentiment_dict)  # 리스트를 딕셔너리로 변환

    okt = Okt()
    words = okt.morphs(title)
    bigrams = [words[i] + words[i+1] for i in range(len(words)-1)]
    all_terms = words + bigrams
    return sum(sentiment_dict.get(term, 0) for term in all_terms)

#파이그래프와 박스플롯, 바이올렛 플롯
def naver_pay_news_graph(df_naver, sentiment_dict):
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

     #감성점수의 기술 통계량
    print(df_naver['감성점수'].describe())

    #IQR을 이용한 이상치 탐색
    Q1 = df_naver['감성점수'].quantile(0.25)
    Q3 = df_naver['감성점수'].quantile(0.75)
    IQR = Q3 - Q1

    #이상치 기준
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outlier = df_naver[(df_naver['감성점수'] < lower_bound) | (df_naver['감성점수'] > upper_bound)]
    print(f'이상치 개수 : {len(outlier)}')
    print(df_naver['감성점수'].value_counts())
    print(outlier)

    #박스플롯
    plt.figure(figsize=(12, 4))
    sns.boxplot(y=df_naver['감성점수'], color='orange')
    '''
    sns.boxplot() -> 감성 점수의 사분위수(Q1, Q2, Q3)와 이상치를 시각화
    박스 내부 : 50%의 데이터가 포함된 범위
    가로선 : 중앙값 (중앙값이 한쪽으로 치우쳐 있으면 분포가 왜곡됨)
    점으로 표시된 부분 : 이상치(outlier)
    '''
    plt.title('감성점수 박스플롯')
    plt.ylabel('감성점수')
    plt.grid()
    plt.show(block=True)
    plt.close()
    gc.collect()

    plt.figure(figsize=(12, 4))
    sns.boxplot(x=df_naver['감성점수'], color='green')
    plt.title('감성점수 박스플롯 (수평)')
    plt.xlabel('감성점수')
    plt.grid()
    plt.show(block=True)
    plt.close()
    gc.collect()

    plt.figure(figsize=(14, 5))
    sns.boxplot(x='날짜', y='감성점수', data=df_naver, color='skyblue')
    plt.title('날짜별 감성점수 박스플롯')
    plt.xticks(rotation=45)
    plt.grid()
    plt.show(block=True)
    plt.close()
    gc.collect()

    #바이올렛 플롯
    plt.figure(figsize=(10, 4))
    sns.violinplot(y=df_naver['감성점수'], color='lightgreen')
    plt.title('감성점수 바이올린 플롯 (수직)')
    plt.ylabel('감성점수')
    plt.grid()
    plt.show(block=True)
    plt.close()
    gc.collect()

    plt.figure(figsize=(14, 5))
    sns.violinplot(x='날짜', y='감성점수', hue='날짜', data=df_naver, palette='pastel', legend=False)
    plt.title('날짜별 감성점수 바이올린 플롯')
    plt.xticks(rotation=45)
    plt.grid()
    plt.show(block=True)
    plt.close()
    gc.collect()

    #파이그래프 (부정비율)
    negative = (df_naver['감성점수'] < 0).mean() * 100
    positive = (df_naver['감성점수'] > 0).mean() * 100
    neutral = (df_naver['감성점수'] == 0).mean() * 100

    plt.figure(figsize=(12, 4))
    plt.pie([negative, positive, neutral], labels=['부정', '긍정', '중립'], 
            autopct='%1.1f%%',
            colors=['red', 'blue', 'green']
            )
    plt.title('뉴스비율')
    plt.show(block=True)
    plt.close()
    gc.collect()
