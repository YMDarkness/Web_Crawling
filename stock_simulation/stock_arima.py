import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from statsmodels.tsa.arima.model import ARIMA
import seaborn as sns

from plot import plot_simulation

# 아리마 예측 모델
# 날짜형 변환

def stock_arima_model(df):

    # 한글 폰트 설정
    plt.rc('font', family='Malgun Gothic')
    plt.rcParams['axes.unicode_minus'] = False

    # 날짜형 변환
    df['날짜'] = pd.to_datetime(df['날짜'])
    df.set_index('날짜', inplace=True)

    # 아리마 모델 학습
    stock_model = ARIMA(df['종가'], order=(3, 1, 0))
    stock_model_fit = stock_model.fit()

    # 최대 3일 예측
    stock_forecast = stock_model_fit.forecast(steps=3)

    # 날짜 인덱스 생성
    future_stock = pd.date_range(start=df.index[-1] + pd.Timedelta(days=1), periods=3)

    # 예측 시각화
    '''plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['종가'], label='실제 종가')
    plt.plot(future_stock, stock_forecast, label='예측 종가', linestyle='--')
    plt.xticks(rotation=45)
    plt.legend()
    plt.title('주식 가격 예측 (ARIMA)')
    plt.xlabel('날짜')
    plt.ylabel('종가')
    plt.tight_layout()
    plt.show()'''

    # 기존 데이터 복사
    df_plt = df[['종가']].copy()

    # 예측 결과 시리즈 생성 (df_forecast 재정의)
    df_forecast = pd.Series(stock_forecast.values, index=future_stock, name='종가')
    
    # 실제 + 예측 합치기
    df_all = pd.concat([df_plt, df_forecast.to_frame()])

    # 시각화
    plt.figure(figsize=(12, 6))
    plt.plot(df_plt.index, df_plt['종가'], marker='o', label='실제 종가', color='blue')
    plt.plot(df_forecast.index, df_forecast, marker='x', linestyle='--', label='예측 종가', color='orange')
    plt.axvline(x=df_plt.index[-1], color='red', linestyle='--')
    plt.axvspan(df_plt.index[-1], future_stock[-1], color='gray', alpha=0.2)
    plt.title('주식 가격 예측 (ARIMA)')
    plt.xlabel('날짜')
    plt.ylabel('종가')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
