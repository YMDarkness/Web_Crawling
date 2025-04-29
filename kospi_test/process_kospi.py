import pandas as pd
from datetime import datetime

from crwal_kospi import kospi_crwal

#코스피 지수 데이터 전처리
def process_kospi_date(df_kospi):
    #날짜 데이터 변환 (데이터 프레임 형식)
    df_kospi['날짜'] = pd.to_datetime(df_kospi['날짜'])

    #날짜 기준 정렬 (오래된 날짜 -> 최신 날짜)
    df_kospi = df_kospi.sort_values(by='날짜')

    #3일 후, 5일 후 종가 추가
    #.shift(-3), .shift(-5) → 데이터를 3일, 5일 뒤로 이동
    df_kospi['3일후_종가'] = df_kospi['종가'].shift(-3)
    df_kospi['5일후_종가'] = df_kospi['종가'].shift(-5)

    #3일, 5일 이동 평균 (Moving Average) 계산
    df_kospi['종가_3일평균'] = df_kospi['종가'].rolling(window=3).mean()
    df_kospi['종가_5일평균'] = df_kospi['종가'].rolling(window=5).mean()

    #업데이트된 데이터 확인
    #print(df_kospi.tail().to_string(float_format='%.2f'))

    #csv 파일 덮어쓰기 (업데이트)
    df_kospi.to_csv('kospi_index.csv', encoding='utf-8-sig', index=False, float_format='%.2f')
    #print(f'[알람] 3일 후, 5일 후 종가 및 이동 평균이 추가되었습니다\n')

    #코스피 지수 이동 평균(3일, 5일) 계산 및 저장
    df_kospi['3일_이동평균'] = df_kospi['종가'].rolling(window=3).mean()
    df_kospi['5일_이동평균'] = df_kospi['종가'].rolling(window=5).mean()

    #코스피 지수 변화율(%) 계산 및 저장
    df_kospi['전일_대비_변화율(%)'] = df_kospi['종가'].pct_change() * 100

    #전일 대비 변화율 % 표시
    df_kospi['전일_대비_변화율(%)'] = df_kospi['전일_대비_변화율(%)'].map(lambda x: f"{x:.2f}%" if pd.notna(x) else '')

    #코스피 하락/상승 여부 표시
    df_kospi['상승여부'] = df_kospi['종가'].diff().apply(lambda x: '상승' if x > 0 else ('하락' if x < 0 else '변동없음'))

    #업데이트된 데이터 확인
    print(df_kospi.tail().to_string(float_format='%.2f'))

    #csv 파일 덮어쓰기 (업데이트)
    df_kospi.to_csv('kospi_index.csv', encoding='utf-8-sig', index=False, float_format='%.2f')
    #print(f'[알람] 3일 이동평균, 5일 이동 평균 및 전일 대비 변화율과 상승여부가 추가되었습니다')
    '''
    float_format='%.2f': 숫자 데이터(특히 float)를 소수점 아래 두 자리까지만 저장
    encoding='utf-8-sig': 한글 깨짐 방지를 위한 인코딩 방식 (Windows에서 열기 좋음)
    index=False: 인덱스 번호는 저장하지 않음
    '''

    print('\n')

    return df_kospi
