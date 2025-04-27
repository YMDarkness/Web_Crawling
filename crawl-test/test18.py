import sqlite3
import datetime
import asyncio
import aiohttp
import schedule
import time
import csv
import smtplib
import requests
from bs4 import BeautifulSoup
from email.mime.text import MIMEText

#오늘 날짜를 기반으로 데이터베이스 파일명 생성
today_date = datetime.datetime.now().strftime("%Y-%m-%d")
db_filename = f"{today_date}_news.db"

#데이터베이스 연결 및 테이블 생성
def initialize_db():
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()

    #뉴스 데이터를 저장할 테이블 생성 (이미 존재하면 건너뜀)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS news_articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            keyword TEXT,
            title TEXT UNIQUE, --제목이 중복되지 않도록 UNIQUE 설정
            link TEXT UNIQUE, -- URL 역시 중복되지 않도록 설정
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

#비동기 방식으로 뉴스 크롤링 (HTML 파싱 방식)
async def fetch_news(session, keyword):
    #실제 뉴스 크롤링 URL로 변경
    search_url = f"https://search.naver.com/search.naver?where=news&query={keyword}"
    async with session.get(search_url) as response:
        html = await response.text()
        soup = BeautifulSoup(html, "html.parser")
        
        #뉴스 제목과 링크 추출
        news_list = []
        for item in soup.select(".news_tit"):
            title = item["title"]
            link = item['href']
            news_list.append((keyword, title, link))
        
        #SQLite에 저장
        conn = sqlite3.connect(db_filename)
        cursor = conn.cursor()

        for keyword, title, link in news_list:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            #중복 데이터 방지 (이미 저장된 링크인지 확인)
            cursor.execute("SELECT * FROM news_articles WHERE link = ?", (link,))
            if cursor.fetchone() is None:
                #중복 데이터 건너뛰기 (이미 같은 제목 또는 URL이 있으면 해당 데이터는 무시됨)
                #cursor.execute("INSERT OR IGNORE INTO news_articles (category, keyword, title, link) VALUES (?, ?, ?, ?)", (category, keyword, title, link))
                
                #중복 시 최신 데이터로 업데이트 (기존 데이터가 있으면 삭제 후 새 데이터로 교체됨)
                #cursor.execute("INSERT OR REPLACE INTO news_articles (category, keyword, title, link) VALUES (?, ?, ?, ?)", (keyword, title, link, timestamp))

                #특정 컬럼만 업데이트 (title이나 link가 중복일 경우, 새로운 데이터를 받아 업데이트할 수 있음)
                #cursor.execute("INSERT INTO news_articles (category, title, link, timestamp) VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP) ON CONFLICT(title) DO UPDATE SET timestamp = CURRENT_TIMESTAMP", (keyword, title, link, timestamp))

                cursor.execute("INSERT INTO news_articles (keyword, title, link, timestamp) VALUES (?, ?, ?, ?)", (keyword, title, link, timestamp))
                
        conn.commit()
        conn.close()

#크롤링 실행
async def scrape_news():
    search_keywords = ["정치", "사회", "경제"]

    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*(fetch_news(session, kw) for kw in search_keywords))

#실행 흐름
if __name__ == "__main__":
    print(f"뉴스 크롤링 시작 . . .")

    #날짜별 DB 파일 생성
    initialize_db()
    #뉴스 크롤링 실행
    asyncio.run(scrape_news())

    #크롤링 후 뉴스 보고서 자동 생성 & 저장
    #CSV
    def save_to_csv(news_date):
        conn = sqlite3.connect(db_filename)
        cursor = conn.cursor()

        #디버깅용 로그 추가
        print("뉴스 데이터베이스에서 데이터 가져오는 중 . . .")

        cursor.execute("SELECT keyword, title, link, timestamp FROM news_articles")
        news_data = cursor.fetchall()

        if not news_data:
            print("저장된 뉴스 데이터 없음")
            return
    
        csv_filename = f"{news_date}_news_report.csv"
    
        with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            #헤더 추가
            writer.writerow(["keyword", "title", "link", "timestamp"])
            writer.writerows(news_data)
    
        conn.close()

        print(f"CSV 파일 저장 완료 : {csv_filename}")
        return csv_filename
    
    save_to_csv(today_date)

    print(f"{db_filename} 파일에 뉴스 저장 완료")

    #keyboardInterrut 예외 처리를 방지하기 위한 try-except문
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n[INFO] 프로그램이 정상적으로 종료되었습니다")
