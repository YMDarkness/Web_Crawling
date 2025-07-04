import matplotlib.pyplot as plt

# 전략 수익률 시각화

def plot_backtest(portfolio):
    plt.figure(figsize=(12, 6))
    plt.plot(portfolio['total_value'], label='Straregy Value')
    plt.title('Backtest Result')
    plt.xlabel('Data')
    plt.ylabel('Portfolio Value')
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()
