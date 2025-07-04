import pandas as pd

# 백테스트 실행 로직

def run_backtest(signals, initial_cash=1000000):
    '''
    signals : strategy.py에서 생성한 데이터프레임
    initial_cash : 초기 자금
    '''

    portfolio = pd.DataFrame(index=signals.index)
    portfolio['price'] = signals['price']
    portfolio['position'] = signals['position'].fillna(0)

    # 일별 수익률
    portfolio['daily_return'] = portfolio['price'].pct_change().fillna(0)
    portfolio['strategy_return'] = portfolio['daily_return'] * portfolio['position']

    # 누적 수익률
    portfolio['cum_return'] = (1 + portfolio['strategy_return']).cumprod()
    portfolio['total_value'] = initial_cash * portfolio['cum_return']
    return portfolio
