import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from gold_price_cluster import gold_price_clustering

def gold_price_simulate(df_gold):
    #수익률 기반 전략 시뮬레이션

    df = df_gold.copy()

    df['MA_5'] = df['전일_대비_변화량(%)'].rolling(window=5).mean()
    df['MA_20'] = df['전일_대비_변화량(%)'].rolling(window=20).mean()

    df['signal'] = 0
    df.loc[df['MA_5'] > df['MA_20'], 'signal'] = 1
    # shift로 오늘의 신호에 따라 내일 매수
    df['position'] = df['signal'].shift(1) # 오늘의 신호 > 어제의 포지션

    # 수익률 계산 (단순 수익률)
    df['return'] = df['금_시세'].pct_change()

    # 전략 수익률 계산
    # 전략 수익률 : 포지션이 1일 때만 수익률 반영
    df['strategy_return'] = df['position'] * df['return']

    df['cumulative_return'] = (1 + df['return']).cumprod()
    df['cumulative_strategy_return'] = (1 + df['strategy_return']).cumprod()

    # 시각화
    plt.figure(figsize=(14, 6))
    plt.plot(df['날짜'], df['cumulative_return'], label='Buy & Hold 수익률', linewidth=2)
    plt.plot(df['날짜'], df['cumulative_strategy_return'], label='MA 전략 수익률', linewidth=2)
    plt.title('금 시세 수익률 시뮬레이션 (MA 전략 vs 단순 보유)')
    plt.xlabel('날짜')
    plt.ylabel('누적 수익률')
    plt.legend()
    plt.grid()
    plt.show()

    # 전략 성과지표
    total_return = df['cumulative_strategy_return'].iloc[-1] - 1
    volatility = df['strategy_return'].std()
    sharpe_ratio = df['strategy_return'].mean() / df['strategy_return'].std()

    print(f"총 수익률: {total_return:.2%}")
    print(f"변동성 (Volatility): {volatility:.4f}")
    print(f"샤프지수 (Sharpe Ratio): {sharpe_ratio:.2f}")

    return df
