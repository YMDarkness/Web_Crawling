import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import TimeSeriesSplit
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

from stock_arima import stock_arima_model

def stock_xgb_model(df, n_future=5):
    '''
    XGBoost 모델

    XGBoost(eXtreme Gradient Boosting)는 경사하강법을 활용하는 지도 학습 부스팅 알고리즘인 
    그레이디언트 부스트 Decision Trees를 사용하는 분산형 오픈 소스 머신 러닝 라이브러리
    Gradient Boosting 알고리즘을 기반으로 한 강력한 머신러닝 모델
    주로 회귀 및 분류 문제에 사용, 특히 대규모 데이터셋에서 뛰어난 성능을 발휘

    Gradient Boosting 알고리즘

    Gradient(혹은 잔차(Residual))를 이용하여 이전 모델을 보완하는 기법을 의미
    이전 학습기의 잔차를 다음 학습기가 학습하고 학습시를 계속 추가해 가면서
    줄여가는 방식
    '''

    # 피처 엔지니어링
    df = df.copy()

    # 피처 생성
    df['return_1d'] = df['종가'].pct_change()
    df['ma_3'] = df['종가'].rolling(3).mean()
    df['ma_5'] = df['종가'].rolling(5).mean()
    df['ma_3_diff'] = df['종가'] - df['ma_3']
    df['ma_5_diff'] = df['종가'] - df['ma_5']
    df['volatility_3'] = df['종가'].rolling(3).std()
    df['volatility_5'] = df['종가'].rolling(5).std()
    df['log_price'] = np.log1p(df['종가'])
    #df['target'] = df['종가'].shift(-n_future) # n일 후 종가 예측
    df['target'] = df['종가'].shift(-n_future) / df['종가'] - 1


    # target이 NaN인 행만 제거
    df.dropna(subset=['target'], inplace=True)

    # XGBoost 모델 학습 및 예측
    X = df[['return_1d', 
            'ma_3', 'ma_5', 
            'ma_3_diff', 'ma_5_diff', 
            'volatility_3', 'volatility_5', 
            'log_price']]
    y = df['target']

    # TimeSeriesSplit 개수 동적으로 조정
    n_splits = min(5, len(df) - 1)
    tscv = TimeSeriesSplit(n_splits=n_splits)

    for train_index, test_index in tscv.split(X):
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]
        break # TimeSeriesSplit은 반복문을 통해서 분할된 인데스를 얻기 때문에, 첫 번째 분할만 사용

    # XGBoost 모델 학습
    stock_model = XGBRegressor(n_estimators=200, learning_rate=0.05, max_depth=3, random_state=42)
    stock_model.fit(X_train, y_train)
    
    # 예측
    stock_preds = stock_model.predict(X_test)

    stock_rmse = np.sqrt(mean_squared_error(y_test, stock_preds))
    print(f'\n[XGBoost 결과] RMSE : {stock_rmse:.4f}')

    # 모델 성능 비교용 로그 저장
    print(f'[XGBoost 결과] 예측값 평균 : {stock_preds.mean():.4f}')
    print(f'[XGBoost 결과] 실제값 평균 : {y_test.mean():.4f}\n')

    # 예측 길이 맞추기
    if len(stock_preds) == len(y_test):
        df.loc[y_test.index, 'stock_pred_xgb'] = stock_preds
    else:
        print(f'[XGBoost 결과] 예측 길이 불일치: preds = {len(stock_preds)}, y_test = {len(y_test)}')

    # 시각화
    plt.figure(figsize=(12, 6))
    plt.plot(y_test.index, y_test, label='실제 수익률', color='blue', linewidth=2)
    plt.plot(y_test.index, stock_preds, label='XGBoost 예측 수익률', color='orange', linestyle='--')
    plt.axhline(0, color='red', linestyle=':') # 기준선 0%
    plt.title(f'XGBoost 모델을 이용한 {n_future}일 후 주가 수익률 예측')
    plt.legend()
    plt.show()
