import aiohttp
import asyncio
import sqlite3
import os
import time
import schedule
from bs4 import BeautifulSoup

#검색할 키워드
search_keywords = ["속보", "사회", "경제", "정치", "스포츠"]

#User-Agent 설정
#웹 사이트에서 봇 차단을 피하기 위해 브라우저처럼 보이도록 설정
#User-Agent 없이 요청하면 차단당할 가능성 있음
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

#SQLite 데이터베이스 연결 및 테이블 생성
db_path = "news_database.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS news_articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        keyword TEXT,
        title TEXT,
        link TEXT UNIQUE,
        timestamp TEXT           
    )
''')
conn.commit()

#비동기 함수
timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

async def fetch_news(session, keyword):
    #네이버 뉴스 검색
    search_url = f"https://search.naver.com/search.naver?where=news&query={keyword}"

    async with session.get(search_url, headers=headers) as response:
        if response.status == 200:
            html = await response.text()

            #HTML 파싱
            soup = BeautifulSoup(html, "html.parser")
            #상위 5개 뉴스 가져오기
            articles = soup.select(".news_tit")[:5]

            for article in articles:
                title = article.get_text()
                link = article['href']

                #중복 데이터 검사 (링크 기준)
                cursor.execute("SELECT * FROM news_articles WHERE link = ?", (link,))
                exsting = cursor.fetchone()

                if not exsting:
                    cursor.execute("INSERT INTO news_articles (keyword, title, link, timestamp) VALUES (?, ?, ?, ?)", 
                                   (keyword, title, link, timestamp))
                    
                    conn.commit()
                    print(f"[{keyword}] {title} ({link})")
                else:
                    print(f"[중복 스킵] {title} ({link})")

async def scrape_news():
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*(fetch_news(session, kw) for kw in search_keywords))
    print(f"뉴스 크롤링 완료")

#일정 실행 함수
def job():
    print(f"뉴스 크롤링 시작 . . .")
    asyncio.run(scrape_news())

#설정 시간마다 실행
schedule.every(30).minutes.do(job)

if __name__ == "__main__":
    print("뉴스 자동 크롤링 시스템 시작")
    #최초 실행
    job()

    #keyboardInterrut 예외 처리를 방지하기 위한 try-except문
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n[INFO] 프로그램이 정상적으로 종료되었습니다")
