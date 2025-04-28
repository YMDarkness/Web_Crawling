import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

from usd_jpy_correlation import usd_jpy_correlations

#변화율 기준 클러스터링 (KMeans)
def market_clusters(df_market):

    df_market = df_market.dropna() #변화율 계산 후 생긴 결측값 제거
    df_market_x = df_market[['미국USD_변화율', '일본JPY(100엔)_변화율']] #변화율 데이터만 추출

    #3개의 그룹으로 클러스터링
    kmeans = KMeans(n_clusters=3, random_state=42)
    df_market['클러스터'] = kmeans.fit_predict(df_market_x)

    #각 클러스터별로 변화율을 색으로 표시한 산점도 시각화
    '''
    sns.scatterplot(
        data=df_market,
        x='미국USD_변화율',
        y='일본JPY(100엔)_변화율',
        hue='클러스터',
        palette='viridis'
    )
    #seanborn의 scatterplot()은 범례도 자동 추가되고, 시각적으로 더 깔끔함
    plt.xlabel('미국USD_변화율')
    plt.ylabel('일본JPY(100엔)_변화율')
    plt.title('환율 변화율 클러스터링')
    plt.show()
    '''

    plt.figure(figsize=(10, 6))
    sns.scatterplot(
        data=df_market,
        x='미국USD_변화율',
        y='일본JPY(100엔)_변화율',
        hue='클러스터',
        palette='viridis'
    )
    plt.xlabel('미국USD_변화율')
    plt.ylabel('일본JPY(100엔)_변화율')
    plt.title('환율 변화 클러스터링')

    #각 점에 날짜 라벨 추가
    for i in range(len(df_market)):
        plt.text(df_market['미국USD_변화율'].iloc[i],
                df_market['일본JPY(100엔)_변화율'].iloc[i],
                df_market['날짜'].dt.strftime('%m-%d').iloc[i],
                fontsize=8, alpha=0.7)
        
    plt.tight_layout()
    plt.show()
    #KMeans는 환율의 움직임 패턴을 자동으로 3가지 유형으로 분류
    #산점도를 통해 어떤 날이 오르고, 어떤 날은 반대로 움직이는 지 시각적으로 확인할 수 있음

    print('\n')

    return df_market
