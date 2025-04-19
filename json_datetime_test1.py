import csv
import requests
from bs4 import BeautifulSoup
#import datetime
from datetime import datetime

#크롤링할 url
url = f"https://finance.naver.com/news/mainnews.naver"

#requests 요청, HTML 파싱, User-Agent 설정
header = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

respones = requests.get(url, headers=header)
respones.raise_for_status()

soup = BeautifulSoup(respones.text, "html.parser")

#크롤링 제목 선택
keyword = soup.select("dd.articleSubject a")

# 날짜 가져오기
#date_time = datetime.datetime.now().strftime("%Y-%m-%d")
'''
import datetime를 사용하고, datetime.datetime.now()로 현재 시간을 가져옴.
strftime("%Y-%m-%d")을 사용하여 "YYYY-MM-DD" 형식으로 날짜를 문자열로 변환.
실행하면 현재 날짜가 문자열 형태로 저장됨.
'''

date_time = datetime.today().strftime("%Y-%m-%d")
'''
from datetime import datetime를 사용하여 datetime 클래스를 직접 가져옴.
datetime.now().strftime("%Y-%m-%d")로 바로 호출할 수 있음.
'''

'''
모듈 임포트 방식

import datetime → datetime.datetime.now()
from datetime import datetime → datetime.now()
결과는 동일하지만, from datetime import datetime이 코드가 조금 더 간결해.
사용할 때 datetime을 두 번 적어야 하는지 여부

import datetime을 사용하면 datetime.datetime.now()처럼 모듈명과 클래스명을 둘 다 써야 함.
from datetime import datetime을 사용하면 datetime.now()처럼 바로 호출 가능.
'''

#csv 파일로 저장
file_name = "pay_date_time.csv"

with open(file_name, mode="w", encoding="utf-8-sig", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["번호", "제목", "시간"])

    for idx, title in enumerate(keyword, 1):
        article = title.get_text(strip=True)
        writer.writerow([idx, article, date_time])

print(f"크롤링 완료 및 {file_name}생성 완료")
