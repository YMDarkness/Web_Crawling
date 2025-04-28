import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima_model import ARIMA
import seaborn as sns

from visualizer_market import market_graph

#환율 예측 시도 (ARIMA 모델 이용)
#ARIMA 모델 구성 및 훈련
def market_ARIMA(filename='exchange_rate.csv'):
    df_market, _, _ = market_graph()

    #날짜 인덱스 설정
    df_market['날짜'] = pd.to_datetime(df_market['날짜'])
    df_market.set_index('날짜', inplace=True)

    #미국USD
    USD_model = ARIMA(df_market['미국USD'], order=(3, 1, 2))
    USD_model_fit = USD_model.fit()

    #5일 후 까지 예측
    USD_forecast = USD_model_fit.forecast(steps=5)

    #날짜 인덱스 생성
    future_USD = pd.date_range(start=df_market.index[-1] + pd.Timedelta(days=1), periods=5)

    #예측 결과 시각화
    plt.plot(df_market['미국USD'], label='실제 환율')
    plt.plot(future_USD, USD_forecast, label='예측', linestyle='--')
    plt.xticks(rotation=45)
    plt.legend()
    plt.title('미국USD 환율 5일 예측')
    plt.tight_layout()
    plt.show()

    #----------------------------------------------------------------

    #123 
    USD_model = ARIMA(df_market['미국USD'], order=(1, 2, 3))
    USD_model_fit = USD_model.fit()

    #5일 후 까지 예측
    USD_forecast = USD_model_fit.forecast(steps=5)

    #날짜 인덱스 생성
    future_USD = pd.date_range(start=df_market.index[-1] + pd.Timedelta(days=1), periods=5)

    #예측 결과 시각화
    plt.plot(df_market['미국USD'], label='실제 환율')
    plt.plot(future_USD, USD_forecast, label='예측', linestyle='--')
    plt.xticks(rotation=45)
    plt.legend()
    plt.title('미국USD 환율 5일 예측')
    plt.tight_layout()
    plt.show()

    #----------------------------------------------------------------
    '''
    #213
    USD_model = ARIMA(df_market['미국USD'], order=(2, 1, 3))
    USD_model_fit = USD_model.fit()

    #5일 후 까지 예측
    USD_forecast = USD_model_fit.forecast(steps=5)

    #날짜 인덱스 생성
    future_USD = pd.date_range(start=df_market.index[-1] + pd.Timedelta(days=1), periods=5)

    #예측 결과 시각화
    plt.plot(df_market['미국USD'], label='실제 환율')
    plt.plot(future_USD, USD_forecast, label='예측', linestyle='--')
    plt.xticks(rotation=45)
    plt.legend()
    plt.title('미국USD 환율 5일 예측')
    plt.tight_layout()
    plt.show()
    '''
    #----------------------------------------------------------------
    '''
    #321
    USD_model = ARIMA(df_market['미국USD'], order=(3, 2, 1))
    USD_model_fit = USD_model.fit()

    #5일 후 까지 예측
    USD_forecast = USD_model_fit.forecast(steps=5)

    #날짜 인덱스 생성
    future_USD = pd.date_range(start=df_market.index[-1] + pd.Timedelta(days=1), periods=5)

    #예측 결과 시각화
    plt.plot(df_market['미국USD'], label='실제 환율')
    plt.plot(future_USD, USD_forecast, label='예측', linestyle='--')
    plt.xticks(rotation=45)
    plt.legend()
    plt.title('미국USD 환율 5일 예측')
    plt.tight_layout()
    plt.show()
    '''
    #----------------------------------------------------------------

    # 기존 데이터 복사
    df_plot = df_market[['미국USD']].copy()
    # 예측 결과 붙이기
    df_forecast = pd.Series(USD_forecast.values, index=future_USD, name='미국USD')
    df_all = pd.concat([df_plot, df_forecast.to_frame()])

    # 시각화
    plt.plot(df_all.index, df_all['미국USD'], label='실제+예측')
    plt.axvline(df_market.index[-1], color='gray', linestyle=':', label='예측 시작')
    plt.axvspan(future_USD[0], future_USD[-1], color='gray', alpha=0.1)
    plt.xticks(rotation=45)
    plt.title('미국USD 환율 (실제 + 5일 예측)')
    plt.legend()
    plt.tight_layout()
    plt.show()

    #----------------------------------------------------------------

    #일본JPY(100엔)
    #일본JPY(100엔엔)
    JPY_model = ARIMA(df_market['일본JPY(100엔)'], order=(3, 1, 2))
    JPY_model_fit = JPY_model.fit()

    #5일 후 까지 예측
    JPY_forecast = JPY_model_fit.forecast(steps=5)

    #날짜 인덱스 생성
    future_JPY = pd.date_range(start=df_market.index[-1] + pd.Timedelta(days=1), periods=5)

    #예측 결과 시각화
    plt.plot(df_market['일본JPY(100엔)'], label='실제 환율')
    plt.plot(future_JPY, JPY_forecast, label='예측', linestyle='-')
    plt.xticks(rotation=45)
    plt.legend()
    plt.title('일본JPY(100엔) 환율 5일 예측')
    plt.tight_layout()
    plt.show()

    #----------------------------------------------------------------

    #123
    JPY_model = ARIMA(df_market['일본JPY(100엔)'], order=(1, 2, 3))
    JPY_model_fit = JPY_model.fit()

    #5일 후 까지 예측
    JPY_forecast = JPY_model_fit.forecast(steps=5)

    #날짜 인덱스 생성
    future_JPY = pd.date_range(start=df_market.index[-1] + pd.Timedelta(days=1), periods=5)

    #예측 결과 시각화
    plt.plot(df_market['일본JPY(100엔)'], label='실제 환율')
    plt.plot(future_JPY, JPY_forecast, label='예측', linestyle='--')
    plt.xticks(rotation=45)
    plt.legend()
    plt.title('일본JPY(100엔) 환율 5일 예측')
    plt.tight_layout()
    plt.show()

    #----------------------------------------------------------------
    '''
    #213
    JPY_model = ARIMA(df_market['일본JPY(100엔)'], order=(2, 1, 3))
    JPY_model_fit = JPY_model.fit()

    #5일 후 까지 예측
    JPY_forecast = JPY_model_fit.forecast(steps=5)

    #날짜 인덱스 생성
    future_JPY = pd.date_range(start=df_market.index[-1] + pd.Timedelta(days=1), periods=5)

    #예측 결과 시각화
    plt.plot(df_market['일본JPY(100엔)'], label='실제 환율')
    plt.plot(future_JPY, JPY_forecast, label='예측', linestyle='--')
    plt.xticks(rotation=45)
    plt.legend()
    plt.title('일본JPY(100엔) 환율 5일 예측')
    plt.tight_layout()
    plt.show()
    '''
    #----------------------------------------------------------------
    '''
    #321
    JPY_model = ARIMA(df_market['일본JPY(100엔)'], order=(3, 2, 1))
    JPY_model_fit = JPY_model.fit()

    #5일 후 까지 예측
    JPY_forecast = JPY_model_fit.forecast(steps=5)

    #날짜 인덱스 생성
    future_JPY = pd.date_range(start=df_market.index[-1] + pd.Timedelta(days=1), periods=5)

    #예측 결과 시각화
    plt.plot(df_market['일본JPY(100엔)'], label='실제 환율')
    plt.plot(future_JPY, JPY_forecast, label='예측', linestyle='--')
    plt.xticks(rotation=45)
    plt.legend()
    plt.title('일본JPY(100엔) 환율 5일 예측')
    plt.tight_layout()
    plt.show()
    '''
    #----------------------------------------------------------------

    # 기존 데이터 복사
    df_plot = df_market[['일본JPY(100엔)']].copy()
    # 예측 결과 붙이기
    df_forecast = pd.Series(USD_forecast.values, index=future_USD, name='일본JPY(100엔)')
    df_all = pd.concat([df_plot, df_forecast.to_frame()])

    # 시각화
    plt.plot(df_all.index, df_all['일본JPY(100엔)'], label='실제+예측')
    plt.axvline(df_market.index[-1], color='gray', linestyle=':', label='예측 시작')
    plt.axvspan(future_JPY[0], future_JPY[-1], color='gray', alpha=0.1)
    plt.xticks(rotation=45)
    plt.title('일본JPY(100엔) 환율 (실제 + 5일 예측)')
    plt.legend()
    plt.tight_layout()
    plt.show()

    return df_all, df_forecast, future_USD, future_JPY


