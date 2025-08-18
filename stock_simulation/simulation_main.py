from stock_crawler import crawl_recent_price
from returns import calculate_future_returns 
from strategy import simulate_strategy
from plot import plot_simulation
from stock_arima import stock_arima_model
from stock_xgb import stock_xgb_model

# 메인 함수

def main():
    ticker = input('시뮬레이션을 진행할 종목의 코드를 입력 (예: 005930 - 삼성전자): ').strip()
    
    # 1. 주가 데이터 크롤링
    df_total = crawl_recent_price(ticker)

    # 2. 미래 수익률 계산
    df = calculate_future_returns(df_total)

    # 3. 전략 시뮬레이션 (정확한 순서로 받기)
    result, df = simulate_strategy(df, strategy_name='moving_avg')

    # 4. 시각화
    plot_simulation(df, df_total, ticker)

    # 5. 아리마 예측 모델
    stock_arima_model(df)

    # 6. XGBoost 예측 모델
    stock_xgb_model(df)

    # 7. 결과 출력
    print('\n수익률 전략 시뮬레이션 결과: ')
    for k, v in result.items():
        print(f'{k}: {v:.2f}%')

if __name__ == '__main__':
    main()
