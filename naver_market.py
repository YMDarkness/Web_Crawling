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

#달러, 엔 환율
url = f'https://finance.naver.com/marketindex/'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

#요청 및 HTML 파싱
response = requests.get(url, headers=headers)
response.raise_for_status()
soup = BeautifulSoup(response.text, 'html.parser')

#환율 정보 가져오기
usd = soup.select_one('#exchangeList > li.on > a.head.usd > div > span.value')
jpy = soup.select_one('#exchangeList > li > a.head.jpy > div > span.value')

if usd:
    usd_index = usd.get_text(strip=True).replace(',', '')
    try:
        usd_index = float(usd_index)
    except ValueError:
        print('[오류] 달러 환율 변환 실패')
        usd_index = None
else:
    print('[오류] 달러 환율을 찾을 수 없음')
    usd_index = None

if jpy:
    jpy_index = jpy.get_text(strip=True).replace(',', '')
    try:
        jpy_index = float(jpy_index)
    except ValueError:
        print('[오류] 엔화 환율 변환 실패')
        jpy_index = None
else:
    print('[오류] 엔화 환율을 찾을 수 없음')
    jpy_index = None

#현재 날짜 가져오기
today = datetime.now().strftime('%Y-%m-%d')

#데이터 저장
filename = 'exchange_rate.csv'

if usd_index is not None and jpy_index is not None:
    if os.path.exists(filename):
        df_market = pd.read_csv(filename, encoding='utf-8-sig')
    else:
        df_market = pd.DataFrame(
            columns=['날짜', '미국USD', '일본JPY(100엔)']
        )

    if today in df_market['날짜'].values:
        print(f'[알람] 오늘 달러 환율 데이터가 이미 존재합니다')
        print(f'[알람] 오늘 엔화 환율 데이터가 이미 존재합니다')
    else:
        new_row = pd.DataFrame(
            [[today, usd_index, jpy_index]], 
            columns=['날짜', '미국USD', '일본JPY(100엔)']
        )
        df_market = pd.concat([df_market, new_row], ignore_index=True)
        df_market.to_csv(filename, encoding='utf-8-sig', index=False)
        print('[알람] 환율 데이터 저장 완료 : ',today)
        print('[미국USD] ',usd_index)
        print('[일본JPY(100엔)] ', jpy_index)
else:
    print('[알람] 환율 데이터 저장 실패')

print(f'[알람] 환율 정보는 약간의 변동이 있을 수 있습니다. 참고용으로만 사용해주세요 \n')


#csv 읽기
df_market = pd.read_csv('exchange_rate.csv', encoding='utf-8-sig')

#날자 데이터 변환 및 정렬
df_market['날짜'] =  pd.to_datetime(df_market['날짜'])
df_market = df_market.sort_values(by='날짜')

#전일 달러 환율 계산
df_market['전일_미국USD'] = df_market['미국USD'].shift(1)

#전일 대비 달러 변화량 계산
df_market['전일_대비_변화율(%)'] = df_market['미국USD'].pct_change() * 100
df_market['전일_대비_변화율(%)'] = df_market['전일_대비_변화율(%)'].map(lambda x: f'{x:.2f}%' if pd.notna(x) else '')

#달러 환율 상승/하락 여부
df_market['상승여부'] = df_market['미국USD'].diff().apply(lambda x: '상승' if x > 0 else ('하락' if x < 0 else '변동없음'))

df_USD = df_market[['날짜', '미국USD', '전일_미국USD', '전일_대비_변화율(%)', '상승여부']]
print(df_USD.tail().to_string(float_format='%.2f'), '\n')


#전일 엔 환율 계산
df_market['전일_일본JPY(100엔)'] = df_market['일본JPY(100엔)'].shift(1)

#전일 대비 엔 변화량 계산
df_market['전일_대비_변화율(%)'] = df_market['일본JPY(100엔)'].pct_change() * 100
df_market['전일_대비_변화율(%)'] = df_market['전일_대비_변화율(%)'].map(lambda x: f'{x:.2f}%' if pd.notna(x) else '')

#엔 환율 상승/하락 여부
df_market['상승여부'] = df_market['일본JPY(100엔)'].diff().apply(lambda x: '상승' if x > 0 else ('하락' if x < 0 else '변동없음'))

df_JPY = df_market[['날짜', '일본JPY(100엔)', '전일_일본JPY(100엔)', '전일_대비_변화율(%)', '상승여부']]
print(df_JPY.tail().to_string(float_format='%.2f'))


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

'''
#USD, JPY 그래프
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
'''

print('\n')


#달러-엔화 간 상관관계 분석
df_market = pd.read_csv('exchange_rate.csv', parse_dates=['날짜'])
df_market.sort_values('날짜', inplace=True)

#전일대비 변화율 계산 (pct_change : 백분율 변화율)
df_market['미국USD_변화율'] = df_market['미국USD'].pct_change()
df_market['일본JPY(100엔)_변화율'] = df_market['일본JPY(100엔)'].pct_change()
#pct_change()는 하루 단위로 환율이 몇 % 변화했는지 계산

#두 환율 변화율 사이의 상관계수 계산
correlation = df_market[['미국USD_변화율', '일본JPY(100엔)_변화율']].corr().iloc[0, 1]
print(f'미국USD와 일본JPY의 상관계수 : {correlation:.4f}')
#상관계수(correlation)는 두 데이터 사이의 동조성 정도를 측정
#1에 가까우면 같은 방향, -1에 가까우면 반대 방향으로 움직임
#.corr()으로 전체 상관계수 행렬을 만들고 필요한 값만 추출해 확장성 확보

#상관계수 시각화
'''
sns.scatterplot(
    x=df_market['미국USD_변화율'],
    y=df_market['일본JPY(100엔)_변화율'],
    data=df_market
)
plt.title(f'환율 변화율 상관관계 (corr={correlation:.2f})')
plt.xlabel('미국USD_변화율')
plt.ylabel('일본JPY(100엔)_변화율')
plt.axhline(0, color='gray', linestyle='--')
plt.axvline(0, color='gray', linestyle='--')
plt.show()
'''

plt.figure(figsize=(10, 6))
sns.scatterplot(
    x=df_market['미국USD_변화율'],
    y=df_market['일본JPY(100엔)_변화율'],
    data=df_market
)
plt.title(f'환율 변화율 상관관계 (corr={correlation:.2f})')
plt.xlabel('미국USD_변화율')
plt.ylabel('일본JPY(100엔)_변화율')
plt.axhline(0, color='gray', linestyle='--')
plt.axvline(0, color='gray', linestyle='--')

#각 점에 날짜 라벨 추가
for i in range(len(df_market)):
    plt.text(df_market['미국USD_변화율'].iloc[i],
             df_market['일본JPY(100엔)_변화율'].iloc[i],
             df_market['날짜'].dt.strftime('%m-%d').iloc[i],
             fontsize=8, alpha=0.7)

plt.tight_layout()
plt.show()

print('\n')


#변화율 기준 클러스터링 (KMeans)
df_market = df_market.dropna() #변화율 계산 후 생긴 결측값 제거
df_market_x = df_market[['미국USD_변화율', '일본JPY(100엔)_변화율']] #변화율 데이터만 추출

#3개의 그룹으로 클러스터링
kmeans = KMeans(n_clusters=3, random_state=42)
df_market['클러스터'] = kmeans.fit_predict(df_market_x)

#각 클러스터별로 변화율을 색으로 표시한 산점도 시각화
'''
sns.scatterplot(
    data=df_market,
    x='미국USD_변화율',
    y='일본JPY(100엔)_변화율',
    hue='클러스터',
    palette='viridis'
)
#seanborn의 scatterplot()은 범례도 자동 추가되고, 시각적으로 더 깔끔함
plt.xlabel('미국USD_변화율')
plt.ylabel('일본JPY(100엔)_변화율')
plt.title('환율 변화율 클러스터링')
plt.show()
'''

plt.figure(figsize=(10, 6))
sns.scatterplot(
    data=df_market,
    x='미국USD_변화율',
    y='일본JPY(100엔)_변화율',
    hue='클러스터',
    palette='viridis'
)
plt.xlabel('미국USD_변화율')
plt.ylabel('일본JPY(100엔)_변화율')
plt.title('환율 변화 클러스터링')

#각 점에 날짜 라벨 추가
for i in range(len(df_market)):
    plt.text(df_market['미국USD_변화율'].iloc[i],
             df_market['일본JPY(100엔)_변화율'].iloc[i],
             df_market['날짜'].dt.strftime('%m-%d').iloc[i],
             fontsize=8, alpha=0.7)
    
plt.tight_layout()
plt.show()
#KMeans는 환율의 움직임 패턴을 자동으로 3가지 유형으로 분류
#산점도를 통해 어떤 날이 오르고, 어떤 날은 반대로 움직이는 지 시각적으로 확인할 수 있음


#환율 예측 시도 (ARIMA)
#ARIMA 모델 구성 및 훈련 (3:자기 상관, 1:차분, 2:이동평균 성분)
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


#
