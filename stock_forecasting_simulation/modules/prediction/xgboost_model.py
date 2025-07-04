import pandas as pd
import numpy as np
import xgboost as xgb

# XGBoost 모델
# 피처 생성(이동평균, 거래량 등), 학습/검증

class XGBoostModel:
    def __init__(self, window_size=5):
        self.window_size = window_size
        self.model = xgb.XGBRegressor(objective='reg:squarederror')

    def _create_features(self, series):
        X, y = [], []
        for i in range(len(series) - self.window_size):
            X.append(series[i:i + self.window_size])
            y.append(series[i + self.window_size])
        return np.array(X), np.array(y)
    
    def fit_predict(self, series: pd.Series, steps=5):
        X, y = self._create_features(series)
        self.model.fit(X, y)
        last_window = series[-self.window_size:].values.reshape(1, -1)
        preds = []
        for _ in range(steps):
            pred = self.model.predict(last_window)[0]
            preds.append(pred)
            last_window = np.roll(last_window, -1)
            last_window[0, -1] = pred
        return preds
    
    # series : 입력 시계열 (list 또는 series)
    # 내부적으로 윈도우 기반 예측 수행
