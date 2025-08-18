import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import TimeSeriesSplit
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

from stock_arima import stock_arima_model

def stock_xgb_model(df, n_future=3):

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
    stock_preds = stock_model.predict(X_test)

    stock_rmse = np.sqrt(mean_squared_error(y_test, stock_preds))
    print(f'\n[XGBoost 결과] RMSE : {stock_rmse:.4f}')

    # 모델 성능 비교용 로그 저장
    print(f'[XGBoost 결과] 예측값 평균 : {stock_preds.mean():.4f}')
    print(f'[XGBoost 결과] 실제값 평균 : {y_test.mean():.4f}\n')

    # 예측값 저장
    df.loc[y_test.index, 'stock_pred_xgb'] = stock_preds

    # 시각화
    plt.plot(y_test.index, y_test,label='실제 종가 변화', color='blue', linewidth=2)
    plt.plot(y_test.index, stock_preds, label='XGBoost 예측', color='orange', linestyle='--')
    plt.title('XGBoost 모델을 이용한 주가 변화 예측')
    plt.legend()
    plt.show()
