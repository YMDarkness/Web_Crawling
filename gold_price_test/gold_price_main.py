from crawl_gold_price import gold_crwal_and_save_csv
from process_gold_price import process_gold_price_csv
from visualizer_gold_price import change_date_and_ARIMA_model
from gold_price_cluster import gold_price_clustering
from gold_price_simulate import gold_price_simulate

from pathlib import Path

def main():
    #base_path = Path(__file__).resolve().parent
    #csv_path = base_path / 'gold_price.csv'

    #금 시세 데이터 크롤링
    df_gold = gold_crwal_and_save_csv()
    
    #금 시세 데이터 전처리
    df_gold = process_gold_price_csv(df_gold)

    #금 시세 데이터 시각화 및 예측 (아리마 모델 활용)
    df_gold = change_date_and_ARIMA_model(df_gold)

    #금 시세 데이터 외부 요인과 연계 분석

    #금 시세 데이터 클러스터링 기반 분석
    df_gold = gold_price_clustering(df_gold)

    #금 시세 데이터 수익률 기반 전략 시뮬레이션
    df_gold = gold_price_simulate(df_gold)

    #금 시세 데이터 변동성 분석

    # 금 시세 데이터 인터랙티브 시각화 (Plotly)

    #df_gold.to_csv(csv_path, index=False)

if __name__ == '__main__':
    main()
