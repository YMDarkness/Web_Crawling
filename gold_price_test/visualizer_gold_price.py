import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from statsmodels.tsa.arima.model import ARIMA
import seaborn as sns

from process_gold_price import process_gold_price_csv

#시각화 및 ARIMA 모델
#날짜형 변환
def change_date_and_ARIMA_model(df_gold):

    df_gold['날짜'] = pd.to_datetime(df_gold['날짜'])

    #한글 폰트 설정
    plt.rc('font', family='Malgun Gothic')
    plt.rcParams['axes.unicode_minus'] = False

    #시각화
    plt.figure(figsize=(12, 6))
    plt.plot(df_gold['날짜'], df_gold['금_시세'], marker='o', label='금 시세')
    plt.title('금 시세 현황')
    plt.xlabel('날짜')
    plt.ylabel('금 시세(원/g)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    #아리마 모델를 이용해 예측
    df_gold['날짜'] = pd.to_datetime(df_gold['날짜'])
    df_gold.set_index('날짜', inplace=True)

    gold_model = ARIMA(df_gold['금_시세'], order=(5, 1, 0))
    gold_model_fit = gold_model.fit()

    '''
    p - AR (AutoRegressive) 자기회기 차수 - 과거 데이터 몇 개를 참조할지
                                            예: p=5면 과거 5일간의 금 시세를 참고해서 오늘을 예측해.

    d - (Differencing) 차분 차수 - 데이터가 너무 우상향/우하향하는 걸 없애려고 몇 번 차분할지
                                            예: d=1은 1차 차분을 뜻하고, 이는 오늘 값 - 어제 값을 말해

    q - MA (Moving Average) 이동평균 차수 - 이전의 오차(예측이 빗나간 정도) 를 몇 개까지 참고할지
                                            데이터가 적거나 단순하면 0이나 1로 작게하고
                                            데이터의 급변, 반복 오차 패턴이 있으면 1 이상으로 키움
                                            예: q=0이면 오차 항은 고려하지 않겠다는 의미야.

    p는 과거 데이터, d는 안정성(추세 제거), q는 오차 조정
    → 세 가지를 조합해서 "미래를 예측"
                                
    p=5: 이전 5일간 금 시세 값을 기반으로
    d=1: 데이터가 추세를 띄므로 한 번 차분하여
    q=0: 예측 오차는 반영하지 않고
    금 시세를 예측하는 모델이라는 의미
    '''

    #최대 5일 예측
    gold_forecast = gold_model_fit.forecast(steps=5)

    #날짜 인덱스 생성
    future_gold = pd.date_range(start=df_gold.index[-1] + pd.Timedelta(days=1), periods=5)

    #예측 시각화
    plt.plot(df_gold['금_시세'], label='실제 금 시세')
    plt.plot(future_gold, gold_forecast, label='예측 시세', linestyle='--')
    plt.xticks(rotation=45)
    plt.legend()
    plt.title('금 시세 5일 예측')
    plt.tight_layout()
    plt.show()

    #-------------------------------------------------------------------------
    '''
    #차수가 3인 모델
    gold_model = ARIMA(df_gold['금_시세'], order=(3, 1, 0))
    gold_model_fit = gold_model.fit()

    #최대 3일 예측
    gold_forecast = gold_model_fit.forecast(steps=5)

    #날짜 인덱스 생성
    future_gold = pd.date_range(start=df_gold.index[-1] + pd.Timedelta(days=1), periods=5)

    #예측 시각화
    plt.plot(df_gold['금_시세'], label='실제 금 시세')
    plt.plot(future_gold, gold_forecast, label='예측 시세', linestyle='--')
    plt.xticks(rotation=45)
    plt.legend()
    plt.title('금 시세 3일 예측')
    plt.tight_layout()
    plt.show()
    '''
    #-------------------------------------------------------------------------

    #추가 사항

    #-------------------------------------------------------------------------

    #기존 데이터 복사
    df_plot = df_gold[['금_시세']].copy()

    #예측 결과 포함
    df_forecast = pd.Series(gold_forecast.values, index=future_gold, name='금-시세')
    df_all = pd.concat([df_plot, df_forecast.to_frame()])

    #시각화
    plt.plot(df_all.index, df_all['금_시세'], label='실제+예측')
    plt.axvline(df_gold.index[-1], color='gray', linestyle=':', label='예측 시작 구간')
    plt.axvspan(future_gold[0], future_gold[-1], color='gray', alpha=0.2)
    plt.xticks(rotation=45)
    plt.title('금 시세 예측 (실제 + 5일 예측)')
    plt.legend()
    plt.tight_layout()
    plt.show()


    #최종 데이터프레임 반환
    return df_gold
    #return df_all, gold_forecast, future_gold, df_gold
    #df_all = 전체 시계열 데이터 (실제 + 예측), 추가 시각화나 다른 분석할 때 유용
    #gold_forecast = 5일간 예측 수치만 따로 관리, 테이블 출력하거나 파일 저장할 때 깔끔
    #future_gold = 예측 결과에 대응되는 미래 날짜를 따로 쓸 수 있어 예측 결과를 표 형태로 정리하거나 추가 시각화할 때 필요
