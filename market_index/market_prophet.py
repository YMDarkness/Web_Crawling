import pandas as pd
from prophet import Prophet
from prophet.plot import plot_plotly
import matplotlib.pyplot as plt

from market_kmeans import kmeans_clustering

def market_prophet(df_market):
    #prophet model용 포맷 변경
    df_USD_prophet = df_market[['date', 'usd_change']].rename(columns={'date': 'ds', 'usd_change': 'y'})

    USD_model = Prophet()
    USD_model.fit(df_USD_prophet)

    USD_future = USD_model.make_future_dataframe(periods=10)
    USD_forecast = USD_model.predict(USD_future)

    #시각화
    USD_model.plot(USD_forecast)
    plt.title(f'USD 환율 변화 예측 (Prophet model)')
    plt.show()

    #-----------------------------------------------------------------

    #prophet model용 포맷 변경
    df_JPY_prophet = df_market[['date', 'jpy_change']].rename(columns={'date': 'ds', 'jpy_change': 'y'})

    JPY_model = Prophet()
    JPY_model.fit(df_JPY_prophet)

    JPY_future = JPY_model.make_future_dataframe(periods=10)
    JPY_forecast = JPY_model.predict(JPY_future)

    #시각화
    JPY_model.plot(JPY_forecast)
    plt.title(f'JPY 환율 변화 예측 (Prophet model)')
    plt.show()

    #-----------------------------------------------------------------
    
    #예측값 병합
    df_market = df_market.merge(
        USD_forecast[['ds', 'yhat']].rename(
            columns={'ds': 'date', 'yhat': 'usd_pred'}), 
            on='date', how='left')
    
    df_market = df_market.merge(
        JPY_forecast[['ds', 'yhat']].rename(
            columns={'ds': 'date', 'yhat': 'jpy_pred'}), 
            on='date', how='left')

    return df_market
