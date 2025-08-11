def simulate_strategy(df, strategy_name='moving_avg'):
    '''
    주어진 DataFrame에 대해 지정된 전략을 시뮬레이션하는 함수입니다.

    기본 전략은 이동평균선 골든크로스 전략
    (5일 이동평균선이 20일 이동평균선을 상향 돌파하는 시점에 매수 신호로 간주)

    매수 시점에서 3일, 5일, 10일 후의 수익률의 평균과 수익률이 양(수익)이었을 확률 계산

    Parameters:
    df (pd.DataFrame): 종가 데이터가 포함된 DataFrame. '날짜'와 '종가' 칼럼이 필요합니다.
    strategy_name (str): 적용할 전략의 이름. 기본값은 'moving_avg'.
    '''

    df = df.copy()

    if strategy_name == 'moving_avg':
        df['MA_5'] = df['종가'].rolling(window=5).mean()
        df['MA_20'] = df['종가'].rolling(window=20).mean()

        # 매수 시점: 1, 매도 또는 보유 아님: 0
        df['signal'] = (df['MA_5'] > df['MA_20']).astype(int)

    # 매수 발생 시점의 수익률 계산
    result = {}
    for offset in [3, 5, 10]:
        col = f'return_{offset}d'
        result[f'avg_return_{offset}d'] = df.loc[df['signal'] == 1, col].mean()
        result[f'success_rate_{offset}d'] = (df.loc[df['signal'] == 1, col] > 0).mean()

    return result, df
