import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os
import pandas as pd

#달러, 엔화 크롤링
def market_index(filename='exchange_rate.csv'):
    url = f'https://finance.naver.com/marketindex/'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
    
    #요청 및 HTML 파싱
    respones = requests.get(url, headers=headers)
    respones.raise_for_status()
    soup = BeautifulSoup(respones.text, 'html.parser')

    #환율 가져오기
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
        jpy_index = jpy.get_text(strip=5).replace(',', '')
        try:
            jpy_index = float(jpy_index)
        except ValueError:
            print('[오류] 엔화 환율 변환 실패')
            jpy_index = None
    else:
        print('[오류] 엔화 환율을 찾을 수 없음')
        jpy_index = None

    #날짜 데이터
    today = datetime.now().strftime('%Y-%m-%d')

    #데이터 저장
    filename = filename

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
            print('[알람] 환율 데이터 저장 완료 : ', today)
            print('[미국USD]', usd_index)
            print('[일본JPY(100엔)]', jpy_index)
    else:
        print('[알람] 환율 데이터 저장 실패')

    print(f'[알람] 환율 정보는 약간의 변동이 있을 수 있습니다. 참고용으로만 사용해주세요')

    return df_market, usd_index, jpy_index
