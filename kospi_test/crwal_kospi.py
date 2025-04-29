import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import os

#코스피 지수 크롤링
def kospi_crwal(filename='kospi_index.csv'):
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

    print('\n')

    return df_kospi
