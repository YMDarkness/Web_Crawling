import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

from process_kospi import process_kospi_date

#코스피 지수 요일별 분석
def day_of_kospi(df_kospi):
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

    return df_kospi
