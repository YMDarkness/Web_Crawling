import pandas as pd
import numpy as np

# 수익률 평가 지표

def calculate_performance(portfolio):
    total_return = portfolio['total_value'].iloc[-1] / portfolio['total_value'].ilco[0] - 1
    max_drawdown = (portfolio['total_value'] / portfolio['total_value'].cummax() - 1).min()
    volatility = portfolio['strategy_return'].std()
    sharpe_ratio = portfolio['strategy_return'].mean() / volatility * np.sqrt(252)

    return {
        'Total return' : round(total_return * 100, 2),
        'Max Drawdown' : round(max_drawdown * 100, 2),
        'Sharpe Ratio' : round(sharpe_ratio, 2)
    }
