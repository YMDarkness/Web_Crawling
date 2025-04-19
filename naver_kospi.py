import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import os
from tabulate import tabulate
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

#네이버 금융 코스피 지수 
url = f"https://finance.naver.com/sise/sise_index.naver?code=KOSPI"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

#요청 및 HTML 파싱
response = requests.get(url, headers=headers)
response.raise_for_status()
soup = BeautifulSoup(response.text, 'html.parser')

#코스피 지수 가져오기
kospi_index_element = soup.select_one('#now_value')

if kospi_index_element:
    kospi_index = kospi_index_element.get_text(strip=True).replace(',', '')
    try:
        kospi_index = float(kospi_index) #숫자 변환
    except ValueError:
        print('[오류] 코스피 지수 변환 실패')
        kospi_index = None
else:
    print('[오류] 코스피 지수를 찾을 수 없음')
    kospi_index = None

#현재 날짜 가져옥기
timeline = datetime.now().strftime('%Y-%m-%d')

#데이터 저장
filename = 'kospi_index.csv'

if kospi_index is not None:
    #기존 데이터 불러오기 (없으면 빈 데이터프레임 생성)
    if os.path.exists(filename):
        df_kospi = pd.read_csv(filename, encoding='utf-8-sig')
    else:
        df_kospi = pd.DataFrame(columns=['날짜', '종가'])

    #중복 방지 : 오늘 날짜 데이터가 이미 존재하는지 확인
    if timeline in df_kospi['날짜'].values:
        print(f'[알람] 오늘 데이터가 이미 존재합니다. 중복 저장 방지')
    else:
        #새로운 데이터 추가
        new_date = pd.DataFrame([[timeline, kospi_index]], columns=['날짜', '종가'])
        df_kospi = pd.concat([df_kospi, new_date], ignore_index=True)
        df_kospi.to_csv(filename, encoding='utf-8-sig', index=False)
        print('[알람] 코스피 지수 저장 완료 : ', timeline, kospi_index)
else:
    print('[알람] 코스피 지수 데이터 저장 실패')

#csv 파일 읽기
df_kospi = pd.read_csv('kospi_index.csv', encoding='utf-8-sig')

#데이터 확인
#print(df_kospi)

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


#요일 칼럼 추가
df_kospi['요일'] = pd.to_datetime(df_kospi['날짜']).dt.day_name()
'''
pd.to_datetime(df_kospi['날짜']): 문자열 형태의 날짜를 datetime 형식으로 변환
.dt.day_name(): 해당 날짜가 무슨 요일인지 영문으로 반환 (예: Monday, Tuesday).
결과: 날짜 컬럼을 기반으로 요일 컬럼이 추가됨
'''

#3일후 상승 여부 판단
df_kospi['3일후_상승여부'] = (df_kospi['3일후_종가'] > df_kospi['종가']).map({True: '상승', False: '하락'})
'''
(df_kospi['3일후_종가'] > df_kospi['종가']): 현재 종가와 3일 후 종가를 비교해서 True/False 반환
.map({True: '상승', False: '하락'}): True → ‘상승’, False → ‘하락’으로 문자로 변환
'''
df_kospi['3일후_상승여부'] = df_kospi['3일후_상승여부'].fillna('데이터 없음')
#.fillna('데이터없음'): 만약 3일 후 종가가 없는 경우(NaN) → ‘데이터없음’으로 채움

#5일후 상승 여부 판단
df_kospi['5일후_상승여부'] = (df_kospi['5일후_종가'] > df_kospi['종가']).map({True: '상승', False: '하락'})
'''
(df_kospi['5일후_종가'] > df_kospi['종가']): 현재 종가와 5일 후 종가를 비교해서 True/False 반환
.map({True: '상승', False: '하락'}): True → ‘상승’, False → ‘하락’으로 문자로 변환
'''
df_kospi['5일후_상승여부'] = df_kospi['5일후_상승여부'].fillna('데이터 없음')
#.fillna('데이터없음'): 만약 5일 후 종가가 없는 경우(NaN) → ‘데이터없음’으로 채움

#print('[알람] 요일 및 3일후, 5일후 상승 여부 정보가 추가되었습니다')

# 날짜 오름차순 정렬
df_kospi = df_kospi.sort_values(by='날짜')

# 중복 제거 추가
df_kospi['날짜'] = pd.to_datetime(df_kospi['날짜'])
df_kospi['날짜_순수'] = df_kospi['날짜'].dt.date
df_kospi = df_kospi.drop_duplicates(subset='날짜_순수', keep='last')
df_kospi['날짜'] = df_kospi['날짜'].dt.date
df_kospi = df_kospi.drop(columns='날짜_순수')

# 변화율 숫자화 (다시 한 번 확실히 처리)
df_kospi['변화율_숫자'] = df_kospi['전일_대비_변화율(%)'].str.replace('%', '').replace('', '0').astype(float)

# 꺾은선 그래프
plt.figure(figsize=(10, 5))
plt.rc('font', family='Malgun Gothic')
plt.rcParams['axes.unicode_minus'] = False

plt.plot(df_kospi['날짜'], df_kospi['변화율_숫자'], marker='o', color='blue', label='전일 대비 변화율')
plt.axhline(0, color='gray', linestyle='--')
plt.title('코스피 지수 전일 대비 변화율(%)')
plt.xlabel('날짜')
plt.ylabel('변화율 (%)')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()


#종가 이동평균
plt.figure(figsize=(10, 5))
plt.plot(df_kospi['날짜'], df_kospi['종가'], label='종가', marker='o')
plt.plot(df_kospi['날짜'], df_kospi['3일_이동평균'], label='3일 이동평균', linestyle='--')
plt.plot(df_kospi['날짜'], df_kospi['5일_이동평균'], label='5일 이동평균', linestyle='-')
plt.title('코스피 지수 이동평균')
plt.xlabel('날짜')
plt.ylabel('지수')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()


#요일별 평균 종가 비교
weekday_avg = df_kospi.groupby('요일')['종가'].mean().sort_values()# 요일별로 종가 평균을 구하고 오름차순 정렬
weekday_avg.plot(kind='bar', color='blue')# 막대그래프 그리기
plt.title('요일별 평균 종가')# 그래프 제목
plt.ylabel('평균 종가')# y축 레이블
plt.xlabel('요일')# x축 레이블
plt.xticks(rotation=45)# 요일 글씨가 겹치지 않도록 기울이기
plt.grid(True) # 눈금선 추가
plt.tight_layout()# 레이아웃 정리
plt.show()

print('\n')

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
print(sangseung_ratio_by_day2.round(2)) # 소수점 둘째 자리 출력


'''
#전일 대비 등락률을 기준으로 양/음봉 비율 구하기
#등락률이 양수면 1, 음수면 0
df_kospi['양봉'] = df_kospi['전일 변화율(%)'].apply(lambda x: 1 if x > 0 else 0)

#요일별 평균 구하기(양봉 비율)
positive_ratio = df_kospi.groupby('요일')['양봉'].mean().sort_index()

#시각화
plt.figure(figsize=(8, 5))
positive_ratio.plot(kind='bar', color='green')
plt.title('요일별 양봉 비율')
plt.ylabel('양봉 바율 (0~1)')
plt.xlabel('요일')
plt.xticks(rotation=45)
plt.ylim(0, 1)
plt.grid(axis='y')
plt.tight_layout()
plt.show()
'''


'''
#월별 양봉 비율 분석
df_kospi['월'] = pd.to_datetime(df_kospi['날짜']).dt.month

#월별 양봉 비율
monthly_positive = df_kospi.groupby('월')['양봉'].mean()

#시각화
monthly_positive.plot(kind='bar', color='red')
plt.title('월별 양봉 비율')
plt.ylabel('양봉 비율')
plt.xlabel('월')
plt.ylim(0, 1)
plt.grid(axis='y')
plt.show()
'''


'''
#누적 수익률 계산
df_kospi['수익률(%)'] = df_kospi['전일 변화율(%)'].cumsum()

#시각화
plt.plot(df_kospi['날짜'], df_kospi['수익률(%)'])
plt.title('누적 수익률(%)')
plt.xlabel('날짜')
plt.ylabel('누적 수익률(%)')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()
'''


#변동성 지표 추가
#코스피 지수 데이터 로드 (날짜를 datetime 형식으로)
df_kospi = pd.read_csv('kospi_index.csv', parse_dates=['날짜'])
df_kospi.sort_values('날짜', inplace=True) #날짜순으로 정렬

#3일 5일 간 종가의 표준편차를 계산하여 변동성 지표로 활용
df_kospi['3일_표준편차'] = df_kospi['종가'].rolling(window=3).std()
df_kospi['5일_표준편차'] = df_kospi['종가'].rolling(window=5).std()
#rolling().std()는 일정 구간의 표준편차를 구해서 가격이 얼마나 출렁였는지 판단하는 데 사용
#숫자가 클수록 더 불안정하다는 의미


#상승/하락 예측 모델 개선 (RandomForest 사용)
#결측값 처리
# 사용 피처 + 타깃 열 포함한 데이터프레임
df_kospi_model_data = df_kospi[['종가', '3일_이동평균', '5일_이동평균', '3일_표준편차', '날짜', '상승여부']].dropna()

# 피처와 타깃 분리
#.copy() 데이터 프레임 안정성 확보
df_kospi_x = df_kospi_model_data.drop(columns='상승여부').copy()
df_kospi_y = df_kospi_model_data['상승여부'].copy()
#SettingWithCopyWarring 발생 위험 방지
#복사한 결과에 바로 스케일링, 인코딩 처리 가능

# 수치형 피처 스케일링
scaled_columns = ['종가', '3일_이동평균', '5일_이동평균', '3일_표준편차']
scaler = StandardScaler()
df_kospi_x[scaled_columns] = scaler.fit_transform(df_kospi_x[scaled_columns])

# 범주형 요일 one-hot 인코딩
df_kospi_x = pd.get_dummies(df_kospi_x)

#학습 데이터를 넣을 때 datetime64 타입(날짜형 데이터)이 포함되어 있는지 확인
if '날짜' in df_kospi_x.columns:
    df_kospi_x = df_kospi_x.drop(columns=['날짜'])
#데이터 프레임에 날짜열이 있는 걸 알 때, 명시적으로 제거하고 싶을 때 사용

#일반적으로 datetime64 타입 열을 모두 제거
df_kospi_x = df_kospi_x.select_dtypes(exclude=['datetime64[ns]', 'datetime64[ns, UTC]'])
'''
select_dtypes() : 특정 타입의 열만 선택하거나 제외할 수 있는 함수
exclude=['datetime64[ns]'] : 날짜형 타입 열을 전부 제외하겠다는 뜻
날짜 열 이름을 모를 때, 전체에서 자동으로 제거하고 싶을 때 유용
'''

# 훈련/테스트 분할
X_train, X_test, y_train, y_test = train_test_split(df_kospi_x, df_kospi_y, test_size=0.2, shuffle=False)


#랜덤포레스트 모델 생성 및 학습
df_kospi_model = RandomForestClassifier()
df_kospi_model.fit(X_train, y_train)

#에측 결과 리포트 출력 (정확도, 정밀도, 재현율 등)
print(classification_report(y_test, df_kospi_model.predict(X_test)))
#RandomForestClassifier는 여러 개의 결정 트리를 모아서 예측 정확도를 높이는 모델
#여기서는 상승/하락 예측에 사용되며, 이동평균, 변동성, 요일 같은 변수들이 예측에 기여

#모델 성능 로그 (정확도, feature importance)
#정확도 확인
y_pred = df_kospi_model.predict(X_test)
print(f'정확도 : ', accuracy_score(y_test, y_pred))

#어떤 변수가 예측에 많이 기여했는지 확인
importances = df_kospi_model.feature_importances_
feature_names = X_test.columns
df_kospi_importances = pd.DataFrame({'특징' : feature_names, '중요도' : importances})
print(df_kospi_importances.sort_values(by='중요도', ascending=False))


#볼린저 밴드 분석
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


#
