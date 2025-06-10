from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import TimeSeriesSplit

from market_prophet import market_prophet

def market_xgboost(df_market):
    #피처 엔지니어링
    df_market = df_market.copy()

    #피처 생성
    df_market['usd_change_1'] = df_market['usd_change'].shift(1)
    df_market['usd_change_2'] = df_market['usd_change'].shift(2)
    df_market['usd_change_3'] = df_market['usd_change'].rolling(window=3).mean()  # 3일 이동평균
    df_market['usd_change_std'] = df_market['usd_change'].rolling(window=3).std()
    df_market['usd_change_diff'] = df_market['usd_change'] - df_market['usd_change'].shift(1)
    df_market['usd_change_log'] = np.log1p(df_market['usd_change'])

    df_market['jpy_change_1'] = df_market['jpy_change'].shift(1)
    df_market['jpy_change_2'] = df_market['jpy_change'].shift(2)
    df_market['jpy_change_3'] = df_market['jpy_change'].rolling(window=3).mean()  # 3일 이동평균
    df_market['jpy_change_std'] = df_market['jpy_change'].rolling(window=3).std()
    df_market['jpy_change_diff'] = df_market['jpy_change'] - df_market['jpy_change'].shift(1)
    df_market['jpy_change_log'] = np.log1p(df_market['jpy_change'])

    df_market.dropna(inplace=True)

    #XGBoost 모델 학습 및 예측
    USD_X = df_market[['usd_change_1', 'usd_change_2', 'usd_change_3',
                       'usd_change_std', 'usd_change_diff', 'usd_change_log']]
    USD_y = df_market['usd_change']

    #USD_X_train, USD_X_test, USD_y_train, USD_y_test = train_test_split(USD_X, USD_y, test_size=0.2, random_state=42)
    
    tscv = TimeSeriesSplit(n_splits=5)
    for train_index, test_index in tscv.split(USD_X):
        USD_X_train, USD_X_test = USD_X.iloc[train_index], USD_X.iloc[test_index]
        USD_y_train, USD_y_test = USD_y.iloc[train_index], USD_y.iloc[test_index]
        break # TimeSeriesSplit은 반복문을 통해서 분할된 인덱스를 얻기 때문에, 첫 번째 분할만 사용

    #XGBoost 모델 학습
    USD_model = XGBRegressor(n_estimators=100, learning_rate=0.05, max_depth=3, random_state=42)
    USD_model.fit(USD_X_train, USD_y_train)
    USD_preds = USD_model.predict(USD_X_test)

    USD_rmse = np.sqrt(mean_squared_error(USD_y_test, USD_preds))
    print(f"[USD XGBoost 결과] RMSE : {USD_rmse:.4f}")
    
    #모델 성능 비교용 로그 저장
    print(f"[USD XGBoost 결과] 예측값 평균 : {USD_preds.mean():.4f}, 실제 평균 : {USD_y_test.mean():.4f}\n")

    #예측값 저장
    df_market.loc[USD_y_test.index, 'usd_pred_xgb'] = USD_preds

    #시각화
    plt.plot(USD_y_test.index, USD_y_test, label='실제 환율 변화', color='blue', linewidth=2)
    plt.plot(USD_y_test.index, USD_preds, label='XGBoost 예측', color='orange', linestyle='--')
    plt.title('XGBoost 모델을 이용한 USD 환율 변화 예측')
    plt.legend()
    plt.show()

    #-----------------------------------------------------------------
    #XGBoost 모델 학습 및 예측
    JPY_X = df_market[['jpy_change_1', 'jpy_change_2', 'jpy_change_3',
                       'jpy_change_std', 'jpy_change_diff', 'jpy_change_log']]
    JPY_y = df_market['jpy_change']

    #JPY_X_train, JPY_X_test, JPY_y_train, JPY_y_test = train_test_split(JPY_X, JPY_y, test_size=0.2, random_state=42)
    
    tscv = TimeSeriesSplit(n_splits=5)
    for train_index, test_index in tscv.split(JPY_X):
        JPY_X_train, JPY_X_test = JPY_X.iloc[train_index], JPY_X.iloc[test_index]
        JPY_y_train, JPY_y_test = JPY_y.iloc[train_index], JPY_y.iloc[test_index]
        break # TimeSeriesSplit은 반복문을 통해서 분할된 인덱스를 얻기 때문에, 첫 번째 분할만 사용

    #XGBoost 모델 학습
    JPY_model = XGBRegressor(n_estimators=100, learning_rate=0.05, max_depth=3, random_state=42)
    JPY_model.fit(JPY_X_train, JPY_y_train)
    JPY_preds = JPY_model.predict(JPY_X_test)

    JPY_rmse = np.sqrt(mean_squared_error(JPY_y_test, JPY_preds))
    print(f"[JPY XGBoost 결과] RMSE : {JPY_rmse:.4f}")
    
    #모델 성능 비교용 로그 저장
    print(f"[JPY XGBoost 결과] 예측값 평균 : {JPY_preds.mean():.4f}, 실제 평균 : {JPY_y_test.mean():.4f}\n")

    #예측값 저장
    df_market.loc[JPY_y_test.index, 'jpy_pred_xgb'] = JPY_preds

    #시각화
    plt.plot(JPY_y_test.index, JPY_y_test, label='실제 환율 변화', color='blue', linewidth=2)
    plt.plot(JPY_y_test.index, JPY_preds, label='XGBoost 예측', color='orange', linestyle='--')
    plt.title('XGBoost 모델을 이용한 JPY 환율 변화 예측')
    plt.legend()
    plt.show()

    #-----------------------------------------------------------------

    #합체 비교
    plt.plot(USD_y_test.index, USD_y_test, label='USD 실제', color='blue', linewidth=2)
    plt.plot(USD_y_test.index, USD_preds, label='USD 예측', color='orange', linestyle='--')
    plt.plot(JPY_y_test.index, JPY_y_test, label='JPY 실제', color='green', linewidth=2)
    plt.plot(JPY_y_test.index, JPY_preds, label='JPY 예측', color='red', linestyle='--')
    plt.title('XGBoost 환율 변화 예측 (USD vs JPY)')
    plt.legend()
    plt.show()

    return df_market
