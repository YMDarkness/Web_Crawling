import schedule
import time
import datetime
import holidays
import subprocess
import requests
import sys

# 대한민국 공휴일 설정
kr_holidays = holidays.KR()

def is_business_day():
    today = datetime.date.today()
    # 평일이며 공휴일이 아닌 경우만 True
    return today.weekday() < 5 and today not in kr_holidays

def run_tasks():
    if is_business_day():
        print("[알림] 자동화 시작 상태")
        subprocess.run([sys.executable, "kospi_test/kospi_main.py"])
        subprocess.run([sys.executable, "market_index/market_main.py"])
        subprocess.run([sys.executable, "gold_price_test/gold_price_main.py"])
        subprocess.run([sys.executable, "naver_pay/naver_pay_main.py"])
    else:
        print("[알림] 자동화 중지 상태")

# 매일 오후 7시에 실행 예약
schedule.every().day.at("19:00").do(run_tasks)

print("[알람] 자동 실행 대기 중... (매일 오후 7시 / 휴일, 공휴일 제외)")
while True:
    schedule.run_pending()
    time.sleep(60)
