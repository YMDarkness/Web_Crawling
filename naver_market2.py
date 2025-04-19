'''import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def get_exchange_history(code, start_date, end_date):
    url = f"https://finance.naver.com/marketindex/exchangeDailyQuote.naver?marketindexCd={code}&page="
    data = []
    page = 1

    while True:
        res = requests.get(url + str(page), headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(res.text, "html.parser")
        rows = soup.select("table.tbl_exchange > tbody > tr")

        if not rows:
            break

        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 2:
                date_str = cols[0].text.strip()
                rate_str = cols[1].text.strip().replace(",", "")
                try:
                    date_obj = datetime.strptime(date_str, "%Y.%m.%d")
                except:
                    continue

                if start_date <= date_obj <= end_date:
                    data.append({
                        "날짜": date_obj.strftime("%Y-%m-%d"),
                        "환율": float(rate_str)
                    })
                elif date_obj < start_date:
                    return pd.DataFrame(data)
        page += 1

# 기간 설정
start = datetime.strptime("2025-04-01", "%Y-%m-%d")
end = datetime.strptime("2025-04-18", "%Y-%m-%d")

# USD 환율
df_usd = get_exchange_history("FX_USDKRW", start, end)
df_usd.rename(columns={"환율": "USD/원"}, inplace=True)

# JPY 환율
df_jpy = get_exchange_history("FX_JPYKRW", start, end)
df_jpy.rename(columns={"환율": "JPY/원"}, inplace=True)

# 날짜 기준으로 병합
df = pd.merge(df_usd, df_jpy, on="날짜", how="outer").sort_values("날짜")

# CSV 저장
df.to_csv("exchange_rate_20250401_20250417.csv", index=False, encoding="utf-8-sig")
print(df)
'''

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

# 1. 코스피 데이터 크롤링 함수
def get_kospi_history(start_date, end_date):
    url = "https://finance.naver.com/sise/sise_index_day.naver?code=KOSPI&page={}"
    data = []
    page = 1

    while True:
        res = requests.get(url.format(page), headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(res.text, "html.parser")
        rows = soup.select("table.type_1 tr")

        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 6:
                date_str = cols[0].text.strip()
                price_str = cols[1].text.strip().replace(",", "")
                try:
                    date_obj = datetime.strptime(date_str, "%Y.%m.%d")
                    price = float(price_str)
                except:
                    continue

                if start_date <= date_obj <= end_date:
                    data.append({
                        "날짜": date_obj.strftime("%Y-%m-%d"),
                        "종가": price
                    })
                elif date_obj < start_date:
                    return pd.DataFrame(data)

        page += 1

# 2. 날짜 설정
start = datetime.strptime("2025-04-01", "%Y-%m-%d")
end = datetime.strptime("2025-04-18", "%Y-%m-%d")

# 3. 데이터 가져오기
df = get_kospi_history(start, end)
df = df.sort_values("날짜").reset_index(drop=True)

# 4. 추가 컬럼 계산
df["3일후_종가"] = df["종가"].shift(-3)
df["5일후_종가"] = df["종가"].shift(-5)
df["종가_3일평균"] = df["종가"].rolling(window=3).mean()
df["종가_5일평균"] = df["종가"].rolling(window=5).mean()
df["3일_이동평균"] = df["종가"].shift(1).rolling(window=3).mean()
df["5일_이동평균"] = df["종가"].shift(1).rolling(window=5).mean()
df["전일_대비_변화율(%)"] = df["종가"].pct_change() * 100
df["상승여부"] = df["전일_대비_변화율(%)"].apply(lambda x: "상승" if x > 0 else ("하락" if x < 0 else "변동없음"))

# 소수점 2자리로 정리
df = df.round(2)

# 5. 중복 날짜 처리: 숫자형 평균 + 상승여부는 첫 값 사용
numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns
string_cols = ["상승여부"]

df_numeric = df.groupby("날짜", as_index=False)[numeric_cols].mean()
df_string = df.groupby("날짜", as_index=False)[string_cols].first()

# 병합
df_final = pd.merge(df_numeric, df_string, on="날짜")

# 날짜 기준 정렬
df_final = df_final.sort_values("날짜").reset_index(drop=True)

# 6. 저장
df_final.to_csv("kospi_analysis_20250401_20250417.csv", index=False, encoding="utf-8-sig", float_format="%.2f")

print(df_final)

