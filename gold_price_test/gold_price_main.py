from crawl_gold_price import gold_crwal_and_save_csv
from process_gold_price import process_gold_price_csv
from visualizer_gold_price import change_date_and_ARIMA_model

def main():
    #금 시세 데이터 크롤링
    df_gold = gold_crwal_and_save_csv()
    
    #금 시세 데이터 전처리
    df_gold = process_gold_price_csv(df_gold)

    #금 시세 데이터 시각화 및 예측 (아리마 모델 활용)
    df_gold = change_date_and_ARIMA_model(df_gold)

if __name__ == '__main__':
    main()
