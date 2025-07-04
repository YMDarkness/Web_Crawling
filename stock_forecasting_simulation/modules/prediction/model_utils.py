import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error
import numpy as np
import logging

# 공통 데이터 전처리, split, 시각화 등 유틸
# 공통 윈도잉, 스케일링, train/test 분리 등

# 예측 성능 평가
def evaluate_forecast(true_values, predictions):
    mse = mean_squared_error(true_values, predictions)
    mae = mean_absolute_error(true_values, predictions)
    rmse = np.sqrt(mse)
    return {
        'MAE' : round(mae, 4),
        'MSE' : round(mse, 4),
        'RMSE' : round(rmse, 4)
    }

# 모델 실행 통합 함수
def run_model(model, series: pd.Series, steps=5, mode='series'):
    '''
    model: ARIMA, Prophet, XGBoost 인스턴스
    series : 시계열 데이터
    steps : 예측할 스텝 수
    mode : 'series (pd.Series), or 'dataframe' (for Prophet)
    '''
    try:
        if mode == 'series':
            forecast = model.fit_predict(series, steps)
        elif mode == 'dataframe':
            df = pd.DataFrame({'data' : series.index, 'value' : series.values})
            forecast = model.fit_predict(df, periods=steps)
        else:
            raise ValueError("Unsupported mode. Use 'series' or 'dataframe'.")
        return forecast
    except Exception as e:
        logging.error(f'Error running model : {e}')
        return None
    
# 예측 결과를 시각화용 포맷으로 변환
def format_forecast_ouput(timestamps, predictions, label='model'):
    '''
    timestamp : 예측할 날짜들
    predictions : 예측값 list 또는 series
    label : 모델 이름
    '''
    return pd.DataFrame({
        'timestamp' : timestamps,
        f'forecast_{label}' : predictions
    })
