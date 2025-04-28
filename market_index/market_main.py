from market_crawl import market_index
from visualizer_market import market_graph
from usd_jpy_correlation import usd_jpy_correlations
from market_cluster import market_clusters
from market_arima import market_ARIMA

def main():
    #환율 데이터 크롤링
    df_market = market_index()

    #환율 데이터 전처리 및 시각화
    df_market = market_graph(df_market)

    #달러-엔화 상관관계
    df_market = usd_jpy_correlations(df_market)

    #환율 데이터 클러스터링
    df_market = market_clusters(df_market)

    #아리마 모델을 이용한 환율 예측
    df_market = market_ARIMA(df_market)
    
if __name__ == '__main__':
    main()
