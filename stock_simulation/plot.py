import matplotlib.pyplot as plt

def plot_simulation(df, df_total, ticker='종목명'):
    '''
    시뮬레이션 전략이 적용된 결과를 시각화

    종가, 이동평균선, 매수 시점(신호)을 함께 시각화
    실제 어떤 시점에 전략이 매수라고 판단했는지 확인할 수 있음

    Parameters:
    df (DataFrame): 시뮬레이션 결과가 포함된 DataFrame
    ticker (str): 종목명, 그래프 제목에 사용됨
    '''

    df = df.copy()
    df.loc[:, '날짜'] = df_total['날짜'].values  # 날짜 복사
    df = df.sort_values('날짜')  # 날짜 순 정렬

    plt.figure(figsize=(14, 6))
    plt.rc('font', family='Malgun Gothic')
    plt.rcParams['axes.unicode_minus'] = False
    
    plt.plot(df['날짜'], df['종가'], label='종가', color='black')
    plt.plot(df['날짜'], df['MA_5'], label='5일_이동평균', linestyle='--', color='blue', alpha=0.5)
    plt.plot(df['날짜'], df['MA_20'], label='20일_이동평균', linestyle='--', color='orange', alpha=0.5)

    # 매수 시점 표시
    if 'signal' in df.columns:
        buy_signals = df[df['signal'] == 1]
        plt.scatter(buy_signals['날짜'], buy_signals['종가'], marker='^', color='green', label='매수 시점')

    plt.title(f'{ticker} 매수 시뮬레이션 결과')
    plt.xlabel('날짜')
    plt.ylabel('종가')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
