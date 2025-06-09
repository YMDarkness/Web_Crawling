import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from scipy.cluster.hierarchy import dendrogram, linkage

from visualizer_gold_price import change_date_and_ARIMA_model

def gold_price_clustering(df_gold):
    df_gold.reset_index(inplace=True)

    df_gold['전일_대비_변화량(%)'] = (
        df_gold['전일_대비_변화량(%)']
        .str.replace('%','', regex=False)
        .replace(['', ' '], np.nan)
        .astype(float)
    )

    # K-means 클러스터링
    X = df_gold[['금_시세', '전일_대비_변화량(%)']].dropna()

    kmeans = KMeans(n_clusters=3, random_state=0)
    #df_gold['KMeans_클러스터'] = kmeans.fit_predict(X)
    df_gold.loc[X.index, 'KMeans_클러스터'] = kmeans.fit_predict(X)

    #시각화
    plt.figure(figsize=(12, 7))
    for c in df_gold['KMeans_클러스터'].unique():
        cluster_data = df_gold[df_gold['KMeans_클러스터'] == c]
        plt.scatter(cluster_data['금_시세'], 
                    cluster_data['전일_대비_변화량(%)'], 
                    label=f'KMeans_클러스터 {c}', s=70)
        
    # 날짜 라벨 추가
    for i in range(len(df_gold)):
        plt.text(df_gold['금_시세'][i], 
                 df_gold['전일_대비_변화량(%)'][i], 
                 df_gold['날짜'][i].strftime('%Y-%m-%d'), 
                 fontsize=8, alpha=0.7)
    
    plt.xlabel('금 시세')
    plt.ylabel('전일 대비 변화량')
    plt.legend(title='KMeans_클러스터')
    plt.title('금 시세 K-means 클러스터링 결과')
    plt.show()

    # 클러스터별 금 시세 평균 / 표준편차
    summary = df_gold.groupby('KMeans_클러스터')[['금_시세', '전일_대비_변화량(%)']].agg(['mean', 'std'])
    print(summary, '\n')

    # 클러스터별 상승/하락 일수 비율
    # 상승/하락 여부를 숫자로 치환
    df_gold['상승여부'] = df_gold['전일_대비_변화량(%)'].apply(lambda x: 1 if x > 0 else 0)
    up_ratio = df_gold.groupby('KMeans_클러스터')['상승여부'].mean()
    print(up_ratio, '\n')

    # 클러스터별 날짜 수 및 예시 날짜 보기
    cluster_counts = df_gold['KMeans_클러스터'].value_counts().sort_index()
    print(cluster_counts, '\n')

    # 각 클러스터별 대표 날짜 보기
    for i in sorted(df_gold['KMeans_클러스터'].unique()):
        dates = df_gold[df_gold['KMeans_클러스터'] == i]['날짜'].tolist()
        print(f'\nKMeans_클러스터 {i} ({len(dates)}일) : {", ".join([d.strftime("%Y-%m-%d") for d in dates[:5]])}...')

    # 종합
    summary_total = df_gold.groupby('KMeans_클러스터').agg({
        '금_시세': ['mean', 'std'],
        '전일_대비_변화량(%)': ['mean', 'std'],
        '상승여부': 'mean'
    }).rename(columns={'short_date': '날짜'})

    print(summary_total, '\n')

    # DBSCAN 클러스터링
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # DBSCAN 모델
    # eps: 거리 기준, min_samples: 최소 샘플 수, 조정 가능
    dbscan = DBSCAN(eps=0.5, min_samples=5)
    #df_gold['DBSCAN_클러스터'] = dbscan.fit_predict(X_scaled)
    df_gold.loc[X.index, 'DBSCAN_클러스터'] = dbscan.fit_predict(X_scaled)

    # DBSCAN 클러스터링 결과 시각화
    plt.figure(figsize=(12, 7))
    for label in sorted(df_gold['DBSCAN_클러스터'].unique()):
        cluster_data = df_gold[df_gold['DBSCAN_클러스터'] == label]
        label_name = f'클러스터 {label}' if label != -1 else '노이즈'
        plt.scatter(cluster_data['금_시세'], 
                    cluster_data['전일_대비_변화량(%)'], 
                    label=label_name, s=70)
        
    plt.title('DBSCAN 클러스터링 결과')
    plt.xlabel('금 시세')
    plt.ylabel('전일 대비 변화량')
    plt.grid()
    plt.legend()
    plt.show()

    # 계층적 클러스터링
    plt.figure(figsize=(12, 7))
    linked = linkage(X_scaled, method='ward')
    dendrogram(linked, 
               orientation='top',
               labels = df_gold.loc[X.index, '날짜'].dt.strftime('%Y-%m-%d').values,
               distance_sort='descending',
               show_leaf_counts=True)
    plt.title('덴드로그램 분석')
    plt.xlabel('날짜')
    plt.ylabel('거리')
    plt.grid()
    plt.show()

    # 클러스터 모델 비교
    print("K-means 클러스터링 결과 : ")
    print(df_gold.groupby('KMeans_클러스터')['금_시세'].mean())

    print("DBSCAN 클러스터링 결과 : ")
    print(df_gold.groupby('DBSCAN_클러스터')['금_시세'].mean())
    
    # 클러스터별 평균 및 표준편차
    print(df_gold.groupby('KMeans_클러스터')[['금_시세', '전일_대비_변화량(%)']].agg(['mean', 'std']))
    print(df_gold.groupby('DBSCAN_클러스터')[['금_시세', '전일_대비_변화량(%)']].agg(['mean', 'std']))

    # 클러스터 수 비교
    print(f"KMeans 클러스터 수 : {df_gold['KMeans_클러스터'].nunique()}")
    print(f"DBSCAN 클러스터 수 (노이즈 제외) : {df_gold['DBSCAN_클러스터'].nunique() - (1 if -1 in df_gold['DBSCAN_클러스터'].unique() else 0)}")

    return df_gold
