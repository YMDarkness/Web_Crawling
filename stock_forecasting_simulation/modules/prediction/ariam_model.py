import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

# ARIMA 모델
# p,d,q 자동 탐지 + 학습/예측

class ARIMAModel:
    def __init__(self, order=(5, 1, 0)):
        self.order = order

    def fit_predoct(self, series: pd.Series, steps=5):
        model = ARIMA(series, order=self.order)
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=steps)
        return forecast
    
    # series = 시계열 데이터
    # order = ARIMA(p,d,q) 파라미터
    # steps = 앞으로 예측할 기간
