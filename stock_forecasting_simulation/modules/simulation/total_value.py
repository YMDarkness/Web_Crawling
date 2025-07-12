from simulation.strategy import simple_moving_average_strategy
from simulation.backtest import run_backtest
from simulation.performance import calculate_performance
from simulation.visualization import plot_backtest

import pandas as pd

# 시뮬레이션 전체 흐름 확인

# 예시용 데이터 로드
df = pd.read_csv('sample_stock.csv', parse_dates=['date'], index_col='date')

# 전략 적용
df = simple_moving_average_strategy(df)

# 백테스트 실행
portfolio = run_backtest(df, initial_cash=1_000_000)

# 성과 지표 계산
metrics = calculate_performance(portfolio)
print(metrics)

# 시각화
plot_backtest(portfolio)
