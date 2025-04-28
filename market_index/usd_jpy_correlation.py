import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from market_crawl import market_index

#달러-엔화 상관관계
def usd_jpy_correlations(df_market):

    df_market['날짜'] = pd.to_datetime(df_market['날짜'])

    #전일 대비 변화율 계산 (pct_change : 백분율 변화율)
    df_market['미국USD_변화율'] = df_market['미국USD'].pct_change()
    df_market['일본JPY(100엔)_변화율'] = df_market['일본JPY(100엔)'].pct_change()
    #pct_change()는 하루 단위로 환율이 몇 % 변화했는지 계산

    #두 환율 변화율 사이의 상관계수 계산
    correlation = df_market[['미국USD_변화율', '일본JPY(100엔)_변화율']].corr().iloc[0, 1]
    print(f'미국USD와 일본JPY의 상관계수 : {correlation:.4f}')
    #상관계수(correlation)는 두 데이터 사이의 동조성 정도를 측정
    #1에 가까우면 같은 방향, -1에 가까우면 반대 방향으로 움직임
    #.corr()으로 전체 상관계수 행렬을 만들고 필요한 값만 추출해 확장성 확보

    #상관계수 시각화
    '''
    sns.scatterplot(
        x=df_market['미국USD_변화율'],
        y=df_market['일본JPY(100엔)_변화율'],
        data=df_market
    )
    plt.title(f'환율 변화율 상관관계 (corr={correlation:.2f})')
    plt.xlabel('미국USD_변화율')
    plt.ylabel('일본JPY(100엔)_변화율')
    plt.axhline(0, color='gray', linestyle='--')
    plt.axvline(0, color='gray', linestyle='--')
    plt.show()
    '''

    plt.figure(figsize=(10, 6))
    sns.scatterplot(
        x=df_market['미국USD_변화율'],
        y=df_market['일본JPY(100엔)_변화율'],
        data=df_market
    )
    plt.title(f'환율 변화율 상관관계 (corr={correlation:.2f})')
    plt.xlabel('미국USD_변화율')
    plt.ylabel('일본JPY(100엔)_변화율')
    plt.axhline(0, color='gray', linestyle='--')
    plt.axvline(0, color='gray', linestyle='--')

    #각 점에 날짜 라벨 추가
    for i in range(len(df_market)):
        plt.text(df_market['미국USD_변화율'].iloc[i],
                df_market['일본JPY(100엔)_변화율'].iloc[i],
                df_market['날짜'].dt.strftime('%m-%d').iloc[i],
                fontsize=8, alpha=0.7)
    plt.tight_layout()
    plt.show()

    print('\n')

    return df_market

