import sqlite3
import datetime
import asyncio
import aiohttp
import schedule
import time
from bs4 import BeautifulSoup

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
    #실제 뉴스 크롤링 URL 변경
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

    print(f"{db_filename} 파일에 뉴스 저장 완료")

    #keyboardInterrut 예외 처리를 방지하기 위한 try-except문
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n[INFO] 프로그램이 정상적으로 종료되었습니다")
