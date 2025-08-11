import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from kospi_XGBClassifier import kospi_model_upgrade

def kospi_simulate(df_kospi):
    # 수익률 기반 전략 시뮬레이션

    if isinstance(df_kospi, tuple):
        df_kospi = df_kospi[0] # 첫 번째 요소만 DataFrame
    df = df_kospi.copy()

    df['MA_5'] = df['전일_대비_변화량(%)'].rolling(window=5).mean()
    df['MA_20'] = df['전일_대비_변화량(%)'].rolling(window=20).mean()

    df['시그널'] = 0
    df.loc[df['MA_5'] > df['MA_20'], '시그널'] = 1

    # shift로 오늘의 신호에 따라 내일 매수
    df['포지션'] = df['시그널'].shift(1) # 오늘의 신호 > 어제의 포지션

    # 수익률 계산 (단순 수익률)
    df['수익률'] = df['코스피_지수'].pct_change()

    # 전략 수익률 계산
    # 전략 수익률 : 포지션이 1일 때만 수익률 반영
    df['전략_수익률'] = df['포지션'] * df['수익률']

    df['누적_수익률'] = (1 + df['수익률']).cumprod()
    df['누적_전략_수익률'] = (1 + df['전략_수익률']).cumprod()

    # 시각화
    plt.figure(figsize=(14, 6))
    plt.plot(df['날짜'], df['누적_수익률'], label='Buy & Hold 수익률', linewidth=2)
    plt.plot(df['날짜'], df['누적_전략_수익률'], label='MA 전략 수익률', linewidth=2)
    plt.title('코스피 지수 수익률 시뮬레이션 (MA 전략 vs 단순 보유)')
    plt.xlabel('날짜')
    plt.ylabel('누적 수익률')
    plt.legend()
    plt.grid()
    plt.show()

    # 전략 성과지표
    total_return = df['누적_전략_수익률'].iloc[-1] - 1
    volatility = df['전략_수익률'].std()
    sharpe_ratio = df['전략_수익률'].mean() / df['전략_수익률'].std()

    print('\n')
    print(f"전략 시뮬레이션 결과\n")
    print(f"총 수익률: {total_return:.2%}")
    print(f"변동성 (Volatility): {volatility:.4f}")
    print(f"샤프지수 (Sharpe Ratio): {sharpe_ratio:.2f}")

    return df
