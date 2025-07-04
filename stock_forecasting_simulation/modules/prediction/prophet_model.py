import pandas as pd
from prophet import Prophet

# Prophet 모델
# 데이터 포맷 맞춤 변환 + 휴일 반영 설정 포함

class ProphetModel:
    def __init__(self):
        self.model = Prophet()

    def fit_predict(self, df: pd.DataFrame, periods=5):
        df = df.rename(columns={'data': 'ds', 'value': 'y'})
        self.model.fit(df)
        future = self.model.make_future_dataframe(periods=periods)
        forecast = self.model.predict(future)
        return forecast[['ds', 'yhat']].tail(periods)
    
    # df : data, value 컬럼을 가진 데이터프레임
    # periods = 예측할 미래 기간
