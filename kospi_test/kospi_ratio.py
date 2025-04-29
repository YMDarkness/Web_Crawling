import pandas as pd
from datetime import datetime

from kospi_days import day_of_kospi

#코스피 지수 상승여부 확인 및 변동성 지표
def ratio_kospi(df_kospi):
    #3일 후 상승 비율 요약 통계
    ratio = df_kospi['3일후_상승여부'].value_counts(normalize=True) * 100 # 비율로 변환 (% 단위)
    print(ratio.round(2), '\n')# 소수점 둘째 자리까지 반올림해서 출력

    #5일 후 상승 비율 요약 통계
    ratio2 = df_kospi['5일후_상승여부'].value_counts(normalize=True) * 100 # 비율로 변환 (% 단위)
    print(ratio2.round(2), '\n')# 소수점 둘째 자리까지 반올림해서 출력

    #전일 대비 변화율 컬럼 추가
    df_kospi['전일_종가'] = df_kospi['종가'].shift(1)# 전일 종가를 한 줄 위에서 가져오기
    df_kospi['전일 변화율(%)'] = ((df_kospi['종가'] - df_kospi['전일_종가']) / df_kospi['전일_종가']) * 100
    df_kospi['전일 변화율(%)'] = df_kospi['전일 변화율(%)'].round(2)# 소수점 둘째 자리로 반올림

    #3일 후 상승 확률을 요일별로 확인
    # '데이터 없음'은 제외하고 요일별 상승/하락 비율을 계산
    sangseung_ratio_by_day = (
        df_kospi[df_kospi['3일후_상승여부'] != '데이터 없음']
        .groupby('요일')['3일후_상승여부']
        .value_counts(normalize=True)
        .unstack()
        .fillna(0)# 값이 없는 경우 0으로 처리
    )
    print(sangseung_ratio_by_day.round(2), '\n') # 소수점 둘째 자리 출력

    #5일 후 상승 확률을 요일별로 확인
    # '데이터 없음'은 제외하고 요일별 상승/하락 비율을 계산
    sangseung_ratio_by_day2 = (
        df_kospi[df_kospi['5일후_상승여부'] != '데이터 없음']
        .groupby('요일')['5일후_상승여부']
        .value_counts(normalize=True)
        .unstack()
        .fillna(0)# 값이 없는 경우 0으로 처리
    )
    print(sangseung_ratio_by_day2.round(2), '\n') # 소수점 둘째 자리 출력

    #변동성 지표 추가
    #코스피 지수 데이터 로드 (날짜를 datetime 형식으로)
    df_kospi = pd.read_csv('kospi_index.csv', parse_dates=['날짜'])
    df_kospi.sort_values('날짜', inplace=True) #날짜순으로 정렬

    #3일 5일 간 종가의 표준편차를 계산하여 변동성 지표로 활용
    df_kospi['3일_표준편차'] = df_kospi['종가'].rolling(window=3).std()
    df_kospi['5일_표준편차'] = df_kospi['종가'].rolling(window=5).std()
    #rolling().std()는 일정 구간의 표준편차를 구해서 가격이 얼마나 출렁였는지 판단하는 데 사용
    #숫자가 클수록 더 불안정하다는 의미
    
    return df_kospi
