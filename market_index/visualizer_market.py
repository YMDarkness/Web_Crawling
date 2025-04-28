import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt

from market_crawl import market_index

#전일 환율 계산 및 시각화
def market_graph(df_market):
    
    #날짜 데이터 변환 및 정렬
    df_market['날짜'] = pd.to_datetime(df_market['날짜'])
    df_market = df_market.sort_values('날짜')

    #전일 달러 환율
    df_market['전일_미국USD'] = df_market['미국USD'].shift(1)

    #전일 대비 변화량 계산
    df_market['전일_대비_달러_변화율(%)'] = df_market['미국USD'].pct_change() * 100
    df_market['전일_대비_달러_변화율(%)'] = df_market['전일_대비_달러_변화율(%)'].map(lambda x: f'{x:.2f}%' if pd.notna(x) else '')

    #달러 환율 상승/하락 여부
    df_market['달러_상승여부'] = df_market['미국USD'].diff().apply(lambda x: '상승' if x > 0 else ('하락' if x < 0 else '변동없음'))

    df_usd = df_market[['날짜', '미국USD', '전일_미국USD', '전일_대비_달러_변화율(%)', '달러_상승여부']]
    print(df_usd.tail().to_string(float_format='%.2f'), '\n')


    #전일 엔화 환율
    df_market['전일_일본JPY(100엔)'] = df_market['일본JPY(100엔)'].shift(1)

    #전일 대비 엔 변화량 계산
    df_market['전일_대비_엔화_변화율(%)'] = df_market['일본JPY(100엔)'].pct_change() * 100
    df_market['전일_대비_엔화_변화율(%)'] = df_market['전일_대비_엔화_변화율(%)'].map(lambda x: f'{x:.2f}%' if pd.notna(x) else '')

    #엔 환율 상승/하락 여부
    df_market['엔화_상승여부'] = df_market['일본JPY(100엔)'].diff().apply(lambda x: '상승' if x > 0 else ('하락' if x < 0 else '변동없음'))

    df_JPY = df_market[['날짜', '일본JPY(100엔)', '전일_일본JPY(100엔)', '전일_대비_엔화_변화율(%)', '엔화_상승여부']]
    print(df_JPY.tail().to_string(float_format='%.2f'))

    #csv 파일 업데이트
    df_market[['날짜', '미국USD', '전일_대비_달러_변화율(%)', '달러_상승여부', '일본JPY(100엔)', '전일_대비_엔화_변화율(%)', '엔화_상승여부']].to_csv('exchange_rate.csv', index=False, float_format='%.2f')

    # 날짜를 날짜형으로 바꾸기 (그래프용)
    df_market['날짜'] = pd.to_datetime(df_market['날짜'])

    plt.rc('font', family='Malgun Gothic')
    plt.rcParams['axes.unicode_minus'] = False

    # USD 그래프
    plt.figure(figsize=(10, 4))
    plt.plot(df_market['날짜'], df_market['미국USD'], marker='o', label='미국USD')
    plt.title('미국 USD 환율 변화')
    plt.xlabel('날짜')
    plt.ylabel('환율')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # JPY 그래프
    plt.figure(figsize=(10, 4))
    plt.plot(df_market['날짜'], df_market['일본JPY(100엔)'], marker='o', label='일본JPY(100엔)')
    plt.title('일본 JPY 환율 변화')
    plt.xlabel('날짜')
    plt.ylabel('환율')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    #USD, JPY 비교 그래프
    plt.figure(figsize=(10, 4))
    plt.plot(df_market['날짜'], df_market['미국USD'], marker='o', label='미국USD')
    plt.plot(df_market['날짜'], df_market['일본JPY(100엔)'], marker='o', color='orange', label='일본JPY(100엔)')
    plt.title('미국USD와 일본JPT(100엔) 환율 비교')
    plt.xlabel('날짜')
    plt.ylabel('환율')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    print('\n')  

    return df_market
