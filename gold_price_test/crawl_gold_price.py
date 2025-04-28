import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os
import pandas as pd

#크롤링 및 csv
def gold_crwal_and_save_csv(filename = 'gold_price.csv'):
    url = f'https://finance.naver.com/marketindex/'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    #요청 및 HTML 파싱
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    #금 시세
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

    #날짜 데이터
    timeline = datetime.now().strftime('%Y-%m-%d')

    #csv 파일
    filename = filename

    if gold_index is not None:
        if os.path.exists(filename):
            df_gold = pd.read_csv(filename, encoding='utf-8-sig')
        else:
            df_gold = pd.DataFrame(
                columns=['날짜', '금_시세']
            )

        if timeline in df_gold['날짜'].values:
            print(f'[알람] 오늘 금 시세 데이터가 이미 존재합니다 \n')
        else:
            new_row = pd.DataFrame(
                [[timeline, gold_index]],
                columns=['날짜', '금_시세']
            )
            df_gold = pd.concat([df_gold, new_row], ignore_index=True)
            df_gold.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f'[알람] 금 시세 데이터 저장 완료 : ', timeline, gold_index)
    else:
        print(f'[알람] 금 시세 데이터 저장 실패 \n')

        #데이터프레임을 비어있는 형태로 만듬
        df_gold = pd.DataFrame(
            columns=['날짜', '금_시세']
        )

    #최종 데이터프레임 반환
    return df_gold
