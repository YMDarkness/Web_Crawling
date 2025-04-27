from datetime import datetime
import os
import pandas as pd

from crawl_gold_price import gold_crwal_and_svae_csv

#csv 파일 읽기
def process_gold_price_csv(filename='gold_price.csv'):
    df_gold = pd.read_csv(filename, encoding='utf-8-sig')

    #데이터 정렬
    df_gold['날짜'] = pd.to_datetime(df_gold['날짜'])
    df_gold = df_gold.sort_values(by='날짜')

    #전일 대비 변화량
    df_gold['전일_금_시세'] = df_gold['금_시세'].shift(1)

    #전일 대비 변화량 계산
    df_gold['전일_대비_변화량(%)'] = df_gold['금_시세'].pct_change() * 100
    df_gold['전일_대비_변화량(%)'] = df_gold['전일_대비_변화량(%)'].map(lambda x: f'{x:.2f}%' if pd.notna(x) else '')

    #금 시세 상승여부
    df_gold['상승여부'] = df_gold['금_시세'].diff().apply(lambda x: '상승' if x > 0 else ('하락' if x < 0 else '변동없음'))

    df_golds = df_gold[['날짜', '금_시세', '전일_대비_변화량(%)', '상승여부']]
    print(df_golds.tail().to_string(float_format='%.2f'), '\n')

    #csv 업데이트
    df_gold.to_csv('gold_price.csv', index=False, encoding='utf-8-sig', float_format='%.2f')

    #특정 칼럼만 골라서 업데이트
    #df_gold[[컬럼1, 컬럼2]].to_csv('gold_price.csv', index=False, encoding='utf-8-sig', float_format='%.2f')

    #최종 데이터프레임 반환
    return df_gold, df_golds
