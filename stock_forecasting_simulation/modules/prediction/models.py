from prediction.ariam_model import ARIMAModel
from prediction.prophet_model import ProphetModel
from prediction.xgboost_model import XGBoostModel
from prediction.model_utils import evaluate_forecast, run_model, format_forecast_ouput

import pandas as pd
import matplotlib.pyplot as plt

# 예시 데이터
df = pd.read_csv('', parse_dates=['date'])
df = df[['date', 'close']]

# 아리마 모델 예측
df_arima = ARIMAModel(df.copy())

# Prophet 모델 예측
df_prophet = ProphetModel(df.copy())

# XGBoost 모델 예측
df_xgb = XGBoostModel(df.copy())

# 결과 비교 시각화
plt.figure(figsize=(12, 6))
plt.plot(df['date'], df['close'], label = 'Actual')
plt.plot(df_arima['date'], df_arima['prediction'], label = 'ARIMA')
plt.plot(df_prophet['date'], df_prophet['prediction'], label = 'Prophet')
plt.plot(df_xgb['date'], df_xgb['prediction'], label = 'XGBoost')
plt.legend()
plt.title('Prediction Comparison')
plt.show()
