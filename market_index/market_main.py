from market_crawl import market_index
from visualizer_market import market_graph
from usd_jpy_correlation import usd_jpy_correlations
from market_cluster import market_clusters
from market_arima import market_ARIMA

def main():
    #환율 데이터 크롤링
    market_index()

    #환율 데이터 전처리 및 시각화
    market_graph()

    #달러-엔화 상관관계
    usd_jpy_correlations()

    #환율 데이터 클러스터링
    market_clusters()

    #아리마 모델을 이용한 환율 예측
    market_ARIMA()
    
if __name__ == '__main__':
    main()
