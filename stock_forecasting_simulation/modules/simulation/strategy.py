import pandas as pd
import numpy as np

# 매매 전략 정의

def simple_moving_average_strategy(data, short=5, long=20):
    '''
    단순 이동평균 골든크로스 전략
    - data : pd.Series (종가)
    '''
    signals = pd.DataFrame(index=data.index)
    signals['price'] = data
    signals['short_ma'] = data.rolling(window=short).mean()
    signals['long_ma'] = data.rolling(window=long).mean()

    # 매수(1), 매도(-1), 시그널
    signals['signal'] = 0
    signals['signal'][short:] = np.where(
        signals['short_ma'][short:] > signals['long_ma'][short:], 1, -1
    )
    signals['position'] = signals['signal'].shift(1)
    return signals
