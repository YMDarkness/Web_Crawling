import pandas as pd

# 결측값 처리 / 스케일링 / 윈도윙 등
# 

def fill_missing(df, method='ffill'):
    return df.fillna(method=method)

def apply_moving_averge(df, column, window=5):
    df[f'{column}_ma{window}'] = df[column].rolling(window=window).mean()
    return df

def create_windowed_dataset(df, column, window_size=10):
    X, y = [], []
    series = df[column].values
    for i in range(len(series) - window_size):
        X.append(series[i:i+window_size])
        y.append(series[i+window_size])
    return X, y
