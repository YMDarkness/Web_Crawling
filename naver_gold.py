import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import os
from tabulate import tabulate
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from statsmodels.tsa.arima.model import ARIMA
import seaborn as sns

#크롤링
url = f'https://finance.naver.com/marketindex/'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

#요청 및 HTML 파싱
response = requests.get(url, headers=headers)
response.raise_for_status()
soup = BeautifulSoup(response.text, 'html.parser')

#gold price
gold_price = soup.select_one('#oilGoldList > li > a.head.gold_domestic > div > span.value')

if gold_price:
    gold_index = gold_price.get_text(strip=True).replace(',', '')
    try:
        gold_index = float(gold_index)
    except ValueError:
        print('[오류] 금 시세를 조회할 수 없습니다')
        gold_index = None
else:
    print('[오류] 금 시세를 찾을 수 없습니다')
    gold_index = None

#get datetime
timeline = datetime.now().strftime('%Y-%m-%d')

#save date
filename = 'gold_price.csv'

if gold_index is not None:
    if os.path.exists(filename):
        df_gold = pd.read_csv(filename, encoding='utf-8-sig')
    else:
        df_gold = pd.DataFrame(
            columns=['날짜', '금_시세']
        )

    if timeline in df_gold['날짜'].values:
        print(f'[알람] 오늘 금 시세 데이터가 이미 존재합니다')
    else:
        new_row = pd.DataFrame(
            [[timeline, gold_index]], 
            columns=['날짜', '금_시세']
            )
        df_gold = pd.concat([df_gold, new_row], ignore_index=True)
        df_gold.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f'[알람] 금 시세 데이터 저장 완료 : ', timeline, gold_index)
else:
    print(f'[알람] 금 시세 데이터 저장 실패')


#read csv
df_gold = pd.read_csv('gold_price.csv', encoding='utf-8-sig')

#sort datetime
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

#csv update
df_gold.to_csv('gold_price.csv', index=False, encoding='utf-8-sig', float_format='%.2f')

#특정 컬럼만 골라 업데이트
#df_gold[[컬럼1, 컬럼2]].to_csv('gold_price.csv', index=False, encoding='utf-8-sig', float_format='%.2f')

#날짜 형 변환
df_gold['날짜'] = pd.to_datetime(df_gold['날짜'])

#한글 설정
plt.rc('font', family='Malgun Gothic')
plt.rcParams['axes.unicode_minus'] = False

#gold_price graph
plt.figure(figsize=(12, 6))
plt.plot(df_gold['날짜'], df_gold['금_시세'], marker='o', label='금 시세', )
plt.title('금 시세 현황')
plt.xlabel('날짜')
plt.ylabel('금 시세(원/g)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

#금 시세 예측 (ARIMA Model)
# 5 = , 1 = , 0 = 
df_gold['날짜'] = pd.to_datetime(df_gold['날짜'])
df_gold.set_index('날짜', inplace=True)

gold_model = ARIMA(df_gold['금_시세'], order=(5, 1, 0))
gold_model_fit = gold_model.fit()

'''
p - AR (AutoRegressive) 차수 - 과거 시계열 값 자체를 몇 시점까지 참고할지 결정해.
                                예: p=5면 과거 5일간의 금 시세를 참고해서 오늘을 예측해.

d - 차분 횟수 (Differencing) - 시계열 데이터를 몇 번 차분해서 **평균이 일정한 데이터(정상성)**로 만들지를 뜻해.
                                예: d=1은 1차 차분을 뜻하고, 이는 오늘 값 - 어제 값을 말해

q - MA (Moving Average) 차수 - 과거 예측 오차를 몇 시점까지 반영할지 설정해.
                                예: q=0이면 오차 항은 고려하지 않겠다는 의미야.

p=5: 이전 5일간 금 시세 값을 기반으로
d=1: 데이터가 추세를 띄므로 한 번 차분하여
q=0: 예측 오차는 반영하지 않고
금 시세를 예측하는 모델이라는 의미
'''

#최대 5일 예측
gold_forecast = gold_model_fit.forecast(steps=5)

#날짜 인덱스 생성
future_gold = pd.date_range(start=df_gold.index[-1] + pd.Timedelta(day=1), periods=5)

#예측 시각화
plt.plot(df_gold['금_시세'], label='실제 금 시세')
plt.plot(future_gold, gold_forecast, label='예측 시세', linestyle='--')
plt.xticks(rotation=45)
plt.legend()
plt.title('금 시세 5일 예측')
plt.tight_layout()
plt.show()

#-------------------------------------------------------------



#-------------------------------------------------------------



#-------------------------------------------------------------

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


#
