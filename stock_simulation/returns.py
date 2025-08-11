def calculate_future_returns(df, offset_days=[3, 5, 10]):
    '''
    주어진 종가 데이터를 기준으로 미래 수익률을 계산하는 함수입니다.

    각각 D+3, D+5, D+10의 수익률(%)을 계산해 새로운 칼럼으로 추가

    각 날짜 기준으로 D+3, D+5, D+10일 후의 종가 대비 현재 종가의 수익률(%)을 계산합니다.

    Parameters:
    df (pd.DataFrame): 종가 데이터가 포함된 DataFrame. '날짜'와 '종가' 칼럼이 필요합니다.
    offset_days (list): 미래 수익률을 계산할 오프셋 일수의 리스트. 기본값은 [3, 5, 10].
    '''
    
    df = df.copy()
    df.sort_values(by='날짜', inplace=True)

    for offset in offset_days:
        df[f'return_{offset}d'] = df['종가'].shift(-offset) / df['종가'] - 1

    return df
