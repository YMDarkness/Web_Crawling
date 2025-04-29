import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

from forect_kospi import randomforest_kospi

#볼린저 밴드 분석
def bollinger_kospi(df_kospi):
    #볼린저 밴드
    #이동 평균선을 기준으로 상단/하단에 표준편차를 더하거나 빼서 구간을 설정하는 지표
    #쉽게는 보통 N=20이 기본 설정, 20일 이동평균선을 기준으로 주가가 어느 정도의 위치에 있는지 알려준다고 생각하면 된다
    #상단선, 중심선, 하단선 3개의 선으로 나타남
    #중심선 수치를 수정하면 상단선, 하단선도 변경된다

    # 이동 평균 기준일 (예: 20일 기준)
    window=5

    df_kospi['MA20'] = df_kospi['종가'].rolling(window=window).mean()
    #20일 이동 평균선 = 최근 20일 종가의 평균값

    df_kospi['STD20'] = df_kospi['종가'].rolling(window=window).std()
    #rolling().std()는 일정 구간의 표준편차를 구해서 가격이 얼마나 출렁였는지 판단하는 데 사용
    #20일 기준 표준편차 = 최근 20일 종가의 변동성

    df_kospi['상단선'] = df_kospi['MA20'] + (df_kospi['STD20'] * 2)
    #상단밴드 = 이동평균선 + (표준편차 * 2)

    df_kospi['하단선'] = df_kospi['MA20'] - (df_kospi['STD20'] * 2)
    #하단밴드 = 이동평균선 - (표준편차 * 2)

    # 최근 100일 데이터만 시각화
    df_kospi_plot = df_kospi.tail(100).copy()
    df_kospi_plot['날짜'] = pd.to_datetime(df_kospi_plot['날짜'])

    #시각화
    plt.figure(figsize=(12, 6))

    #종가 그래프
    plt.plot(df_kospi_plot['날짜'], df_kospi_plot['종가'], label='종가', marker='o')

    #이동선 평균 그래프
    plt.plot(df_kospi_plot['날짜'], df_kospi_plot['MA20'], label='20일 이동평균', color='green', marker='o')

    #상단밴드
    plt.plot(df_kospi_plot['날짜'], df_kospi_plot['상단선'], label='상단밴드', linestyle='--', color='red')

    #하단밴드
    plt.plot(df_kospi_plot['날짜'], df_kospi_plot['하단선'], label='하단밴드', linestyle='--', color='blue')

    #상단~하단 밴드 사이 영역을 회색으로 채움
    plt.fill_between(df_kospi_plot['날짜'], df_kospi_plot['하단선'], df_kospi_plot['상단선'], color='lightgray', alpha=0.3)

    #범례
    plt.legend()

    plt.title('볼린저 밴드')
    plt.xticks(rotation=45)

    #여백 자동 조절
    plt.tight_layout()
    plt.show()

    '''
    MA20	20일 간 평균 가격
    STD20	20일 간 가격의 변동성(흩어짐 정도)
    Upper	평균 + 2 * 표준편차 → 가격이 상단 밴드를 뚫으면 과매수(overbought) 신호일 수 있음
    Lower	평균 - 2 * 표준편차 → 가격이 하단 밴드를 뚫으면 과매도(oversold) 신호일 수 있음
    '''

    return df_kospi
