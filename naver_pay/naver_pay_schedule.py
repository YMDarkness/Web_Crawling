import schedule
import time
import datetime
import holidays
import subprocess
import sys

# 공휴일 및 휴일 설정
kr_holidays = holidays.KR()

def is_business_day():
    today = datetime.date.today()

    # 평일이거나 공휴일이 아닌 경우만 True
    return today.weekday() < 5 and today not in kr_holidays

def run_tasks():
    if is_business_day():
        print('[알람] 크롤링 자동화 대기 상태')

        # 크롤링 스크립트 실행
        subprocess.run([sys.executable, 'naver_pay_main.py'])
        print('[알람] 크롤링 자동화 완료 상태')
    else:
        print('[알람] 크롤링 자동화 중지 상태')

# 크롤링 자동화 스케줄 시간 설정
schedule.every().day.at('19:00').do(run_tasks)

print('[알람] 네이버 페이 증권 뉴스 크롤링 자동화 대기 중... (평일 19시 / 휴일 및 공휴일 제외)')

while True:
    schedule.run_pending()
    time.sleep(60) # 1분마다 스케줄 확인
