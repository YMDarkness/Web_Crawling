import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from statsmodels.tsa.arima.model import ARIMA
import seaborn as sns

from plot import plot_simulation

# 아리마 예측 모델
# 날짜형 변환

def stock_arima_model(df, ticker = '종목명', n_future=5, alpha=0.05):
    '''
    arima 모델이란

    Autoregressive Integrated Moving Average 의 약자
    시계열 데이터의 예측을 위해 고안된 통계적 모델
    자기회귀(AR), 차분(I), 이동평균(MA) 요소를 결합하여 
    시계열 데이터를 분석하고 예측하는 데 사용
    '''

    # 한글 폰트 설정
    plt.rc('font', family='Malgun Gothic')
    plt.rcParams['axes.unicode_minus'] = False

    # 날짜형 변환
    df = df.copy()
    df['날짜'] = pd.to_datetime(df['날짜'])
    df.set_index('날짜', inplace=True)

    # 아리마 모델 학습
    stock_model = ARIMA(df['종가'].astype(float), order=(5, 1, 0))
    stock_model_fit = stock_model.fit()

    # 예측 + 신뢰 구간
    fcst = stock_model_fit.get_forecast(steps=n_future)
    yhat = fcst.predicted_mean
    ci = fcst.conf_int(alpha=alpha) # 하한 / 상한

    # 미래 날짜 인덱스 생성
    future_stock = pd.date_range(start=df.index[-1] + pd.Timedelta(days=1), periods=n_future)
    yhat.index = future_stock
    ci.index = future_stock

    # 예측 시각화
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['종가'], marker='o', label='실제 종가', color='blue')
    plt.plot(yhat.index, yhat, marker='x', linestyle='--', label='예측 종가', color='orange')
    plt.fill_between(ci.index, ci.iloc[:, 0], ci.iloc[:, 1], alpha=0.2, color='gray', label='신뢰 구간')

    # 예측 구간 강조
    plt.axvline(x=df.index[-1], color='red', linestyle='--')
    plt.axvspan(df.index[-1], future_stock[-1], color='gray', alpha=0.15, label=f'{n_future}일 예측 구간')

    # 타이틀 / 레이블
    plt.title(f'{ticker} 주식 종가 예측 (ARIMA 모델 {stock_model}, {n_future}일)')
    plt.xlabel('날짜')
    plt.ylabel('종가')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
