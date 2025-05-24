import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import seaborn as sns
from scipy.cluster.hierarchy import dendrogram, linkage

from market_arima import market_ARIMA

#K-means로 환율 변화율 클러스터링 등 외 8개
def kmeans_clustering(df_market):
    #날짜 인덱스 설정
    df_market.reset_index(inplace=True)

    #K-means로 환율 변화율 클러스터링
    #K-means 적용
    X = df_market[['미국USD_변화율', '일본JPY(100엔)_변화율']]
    kmeans = KMeans(n_clusters=3, random_state=0)
    df_market['클러스터'] = kmeans.fit_predict(X)

    #시각화
    plt.figure(figsize=(12, 7))
    for c in df_market['클러스터'].unique():
        cluster_data = df_market[df_market['클러스터'] == c]
        plt.scatter(cluster_data['미국USD_변화율'], 
                    cluster_data['일본JPY(100엔)_변화율'], 
                    label=f'클러스터 {c}', s=70)
        
    #날짜 라벨 추가
    for i in range(len(df_market)):
        plt.text(df_market['미국USD_변화율'][i], 
                 df_market['일본JPY(100엔)_변화율'][i], 
                 df_market['날짜'][i].strftime('%Y-%m-%d'), 
                 fontsize=8, alpha=0.7)
        
    plt.xlabel('미국USD 변화율')
    plt.ylabel('일본JPY(100엔) 변화율')
    plt.title('K-means 클러스터링 결과')
    plt.legend(title='클러스터')
    plt.grid()
    plt.show()

    #클러스터별 변화율 평균 / 표준편차
    summary = df_market.groupby('클러스터')[['미국USD_변화율', '일본JPY(100엔)_변화율']].agg(['mean', 'std'])
    print(summary, '\n')

    #클러스터별 상승/하락 일수 비율
    #상승/하락 여부를 숫자로 치환
    df_market['미국USD_상승'] = df_market['미국USD_변화율'].apply(lambda x: 1 if x > 0 else 0)
    df_market['일본JPY(100엔)_상승'] = df_market['일본JPY(100엔)_변화율'].apply(lambda x: 1 if x > 0 else 0)

    #클러스터별 상승일 비율
    up_ratio = df_market.groupby('클러스터')[['미국USD_상승', '일본JPY(100엔)_상승']].mean()
    print(up_ratio, '\n')

    #클러스터별 날짜 수 및 예시 날짜 보가
    cluster_counts = df_market['클러스터'].value_counts().sort_index()
    print(cluster_counts, '\n')

    #각 클러스터별 대표 날짜 보기
    for i in sorted(df_market['클러스터'].unique()):
        dates = df_market[df_market['클러스터'] == i]['날짜'].tolist()
        print(f'\n클러스터 {i} ({len(dates)}일) : {", ".join([d.strftime("%Y-%m-%d") for d in dates[:5]])}... \n')

    #전체 종합표
    summary_total = df_market.groupby('클러스터').agg({
        '미국USD_변화율': ['mean', 'std'],
        '일본JPY(100엔)_변화율': ['mean', 'std'],
        '미국USD_상승': 'mean',
        '일본JPY(100엔)_상승': 'mean',
        '날짜': 'count'
    }).rename(columns={'short_date': '날짜'})

    print(summary_total, '\n')

    #클러스터별 USD / JPY 변화율 평균 (막대그래프)
    #클러스터별 평균 변화율 계산
    mean_changes = df_market.groupby('클러스터')[['미국USD_변화율', '일본JPY(100엔)_변화율']].mean().reset_index()

    plt.figure(figsize=(12, 6))
    sns.barplot(data=mean_changes.melt(id_vars='클러스터'), x='클러스터', y='value', hue='variable')
    plt.title('클러스터별 평균 변화율(%)')
    plt.xlabel('클러스터')
    plt.ylabel('평균 변화율(%)')
    plt.axhline(0, color='red', linestyle='--')
    plt.show()
    print('\n')

    #클러스터별 상승/하락 비율 (막대그래프)
    #클러스터별 상승/하락 비율을 숫자로 매핑
    df_market['미국USD_상승'] = df_market['미국USD_상승'].map({0: '하락', 1: '상승'})
    df_market['일본JPY(100엔)_상승'] = df_market['일본JPY(100엔)_상승'].map({0: '하락', 1: '상승'})

    up_ratio = df_market.groupby('클러스터')[['미국USD_상승', '일본JPY(100엔)_상승']].agg(lambda x: x.value_counts(normalize=True).max()).reset_index()
    plt.figure(figsize=(12, 6))
    sns.barplot(data=up_ratio.melt(id_vars='클러스터'), x='클러스터', y='value', hue='variable')
    plt.title('클러스터별 상승/하락 비율')
    plt.xlabel('클러스터')
    plt.ylabel('상승 확률 (0~1)')
    plt.ylim(0, 1)
    plt.show()
    print('\n')

    #클러스터별 데이터 수 (파이그래프)
    cluster_counts = df_market['클러스터'].value_counts().sort_index()

    plt.figure(figsize=(8, 8))
    plt.pie(cluster_counts, labels=cluster_counts.index, autopct='%1.1f%%', startangle=140)
    plt.title('클러스터별 데이터 수 비율')
    plt.show()
    print('\n')

    #USD / JPY 변화율 분포 및 클러스터 색상 (산점도)
    plt.figure(figsize=(12, 7))
    sns.scatterplot(data=df_market, x='미국USD_변화율', y='일본JPY(100엔)_변화율', hue='클러스터', palette='Set1', s=100)
    plt.axhline(0, color='red', linestyle='--')
    plt.axvline(0, color='red', linestyle='--')
    plt.title('USD / JPY 변화율 분포 및 클러스터 색상')
    plt.xlabel('미국USD 변화율(%)')
    plt.ylabel('일본JPY(100엔) 변화율(%)')
    plt.grid(True)
    plt.show()
    print('\n')

    #덴드로그램
    #계층적 군집 분석 수행
    linked = linkage(X, method='ward')

    plt.figure(figsize=(12, 7))
    dendrogram(linked, 
               orientation='top',
               labels=df_market['날짜'].dt.strftime('%Y-%m-%d').values,
               distance_sort='descending',
               show_leaf_counts=True)
    plt.title('덴드로그램 분석')
    plt.xlabel('날짜')
    plt.ylabel('거리')
    plt.grid()
    plt.show()

    return df_market
