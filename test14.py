import sqlite3
import datetime
import asyncio
import aiohttp
import schedule
import time
import threading
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

#오늘 날짜를 기반으로 데이터베이스 파일명 생성
today_date = datetime.datetime.now().strftime("%Y-%m-%d")
db_filename = f"{today_date}_news.db"

#데이터베이스 연결 및 테이블 생성
def initialize_db():
    conn = sqlite3.connect(db_filename)
    curosr = conn.cursor()

    #뉴스 데이터를 저장할 테이블 생성
    curosr.execute('''
        CREATE TABLE IF NOT EXISTS news_articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            keyword TEXT,
            title TEXT UNIQUE,
            link TEXT UNIQUE,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

#비동기 방식으로 뉴스 크롤링 (HTML 파싱 방식)
async def fetch_news_async(session, keyword):
    search_url = f"https://search.naver.com/search.naver?where=news&query={keyword}"
    async with session.get(search_url) as responese:
        html = await responese.text()
        soup = BeautifulSoup(html, "html.parser")

        news_list = []
        for item in soup.select(".news_tit"):
            title = item["title"]
            link = item['href']
            news_list.append((keyword, title, link))

        conn = sqlite3.connect(db_filename)
        cursor = conn.cursor()

        for keyword, title, link in news_list:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("SELECT * FROM news_articles WHERE link = ?", (link,))
            if cursor.fetchone() is None:
                cursor.execute("INSERT INTO news_articles (keyword, title, link, timestamp) VALUES (?, ?, ?, ?)", (keyword, title, link, timestamp))

        conn.commit()
        conn.close()

#멀티스레딩 방식으로 뉴스 크롤링
def fetch_news_threading(keyword):
    search_url = f"https://search.naver.com/search.naver?where=news&query={keyword}"
    resopnse = requests.get(search_url)
    soup = BeautifulSoup(resopnse.text, "html.parser")

    news_list = []
    for item in soup.select(".news_tit"):
        title = item["title"]
        link = item['href']
        news_list.append((keyword, title, link))

    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()

    for keyword, title, link in news_list:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("SELECT * FROM news_articles WHERE link = ?", (link,))
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO news_articles (keyword, title, link, timestamp) VALUSE (?, ?, ?, ?)", (keyword, title, link, timestamp))

    conn.commit()
    conn.close()

#비동기 크롤링 실행
async def scrape_news_async():
    search_keywords = ["정치", "사회", "경제"]
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*(fetch_news_async(session, kw) for kw in search_keywords))

#멀티스레딩 크롤링 실행
def scrape_news_threading():
    search_keywords = ["정치", "사회", "경제"]
    with ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(fetch_news_threading, search_keywords)

#실행 흐름
if __name__ == "__main__":
    print(f"뉴스 크롤링 시작 . . .")
    initialize_db()

    start_time = time.time()
    asyncio.run(scrape_news_async())
    async_time = time.time() - start_time
    print(f"비동기 크롤링 실행 시간 : {async_time : .2f}초")

    start_time = time.time()
    scrape_news_threading()
    thread_time = time.time() - start_time
    print(f"멀티스레딩 크롤링 실행 시간 : {thread_time : .2f}초")

    print(f"{db_filename} 파일에 뉴스 저장 완료")
