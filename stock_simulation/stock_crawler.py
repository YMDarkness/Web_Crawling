import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from datetime import datetime
import time

# 크롤링

def crawl_recent_price(stock_code: str, days: int = 365) -> pd.DataFrame:
    '''
    네이버 금융에서 지정한 종목코드의 최근 30일간 주가 데이터를 수집
    -> 예측 모델의 정확도를 위해 30일에서 1년으로 기간을 변경

    Args:
        stock_code (str): 종목 코드 (예: '005930' 삼성전자)
        days (int): 수집할 일수 (기본값: 30일) -> (기본값: 365일)

    Returns:
        pd.DataFrame: 날짜, 종가, 시가, 고가, 저가, 거래량을 포함하는 데이터프레임

    from bs4 import BeautifulSoup가 아닌 selenium인 이유
    -> 동적 페이지 로딩이 필요한 경우가 있기 때문
    '''

    base_url = f'https://finance.naver.com/item/sise_day.nhn?code={stock_code}'
    
    # chrome 옵션 설정
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # 브라우저를 띄우지 않고 실행
    chrome_options.add_argument('--no-sandbox') # 샌드박스 모드 비활성화
    chrome_options.add_argument('--disable-dev-shm-usage')  # 리소스 제한 해제

    # 웹드라이버 설정
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options)
    driver.get(base_url)
    time.sleep(1)  # 페이지 로딩 대기

    df_total = pd.DataFrame()
    page = 1

    while len(df_total) < days:
        driver.get(f'{base_url}&page={page}')
        time.sleep(1) # 페이지 로딩 대기

        tables = pd.read_html(driver.page_source)
        df = tables[0].dropna()  # 결측치 제거

        if df.empty:
            break

        df_total = pd.concat([df_total, df], ignore_index=True)
        page += 1

    driver.quit()

    df_total =  df_total[:days].copy()
    '''df_total.columns = [
        '날짜', '종가', '전일비', '등락률', '거래량', '거래대금', '시가', '고가', '저가'
    ]'''

    # 컬럼 이름 유연하게 지정
    available_cols = df_total.shape[1]

    # 컬럼 미스매치를 방지하기 위해 동적으로 할당하거나, 예외처리
    expected_columns = [
        '날짜', '종가', '전일비', '등락률', '거래량', '거래대금', '시가', '고가', '저가'
    ]

    # 수집된 컬럼 수만큼만 적용
    df_total.columns = expected_columns[:available_cols]

    # 날짜 파싱
    df_total['날짜'] = pd.to_datetime(df_total['날짜'], errors='coerce')
    df['날짜'] = df_total['날짜']

    # 수치형 컬럼 처리
    numeric_cols = ['종가', '전일비', '등락률', '거래량', '거래대금', '시가', '고가', '저가']
    for col in numeric_cols:
        if col in df_total.columns:
            df_total[col] = (
                df_total[col]
                .astype(str)
                .str.extract(r'([\d.-]+)')[0]
                .str.replace(',', '', regex=False)
                .astype(float)
            )

    # 특정 컬럼(고가, 저가 등) 없을 경우 보완
    if '고가' not in df_total.columns:
        df_total['고가'] = df_total['시가']
    if '시가' not in df_total.columns:
        df_total['시가'] = df_total['시가']
    
    # 데이터 정렬 및 인덱스 초기화
    df_total = df_total.sort_values('날짜').reset_index(drop=True)
    df = df.sort_values('날짜').reset_index(drop=True)

    return df_total
