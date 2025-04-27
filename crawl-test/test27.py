import sqlite3
import datetime
import asyncio
import aiosqlite
import concurrent.futures
import time

#오늘 날짜를 기반으로 DB 파일 생성
today_date = datetime.datetime.now().strftime("%Y-%m-%d")
db_filename = f"{today_date}_news.db"

#DB 연결 및 테이블 생성
def initialize_db():
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()

    #뉴스 데이터를 저장할 테이블 생성
    cursor.execute('''
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

#샘플 뉴스 리스트 (테스트 데이터)
news_list = [
    ("정치", "대선", "대선 후보 발표", "https://example.com/1"),
    ("경제", "주식", "코스피 상승", "https://example.com/2"),
    ("스포츠", "축구", "리그 우승", "https://example.com/3")
]

#비동기 방식으로 SQLite에 뉴스 데이터 삽입
async def insert_news_async(news_list):
    async with aiosqlite.connect(db_filename) as conn:
        cursor = await conn.cursor()
        await cursor.executemany("""
            INSERT INTO news_articles (category, keyword, title, link, timestamp)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(title) DO UPDATE SET timestamp = CURRENT_TIMESTAMP
        """, news_list)
        await conn.commit()
        #aiosqlite 라이브러리를 사용해 비동기 방식으로 데이터 삽입
        #executemany()를 이용해 여러 개의 뉴스 데이터를 한 번에 삽입
        #ON CONFLICT(title) DO UPDATE → 제목이 중복되면 timestamp만 업데이트

async def main():
    await insert_news_async(news_list)

#멀티스레딩 방식으로 뉴스 삽입
def insert_news_thread(news):
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO news_articles (category, keyword, title, link, timestamp)
        VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(title) DO UPDATE SET timestamp = CURRENT_TIMESTAMP
    """, news)

    conn.commit()
    conn.close()
    #멀티스레딩(Threading) 방식으로 SQLite에 데이터 삽입
    #ThreadPoolExecutor에서 하나씩 실행되도록 설계
    #ON CONFLICT(title) DO UPDATE → 중복 뉴스는 시간만 업데이트

#실행 흐름
if __name__ == "__main__":
    print(f"뉴스 크롤링 시작 . . .")

    # 날짜별 DB 생성
    initialize_db()
    
    #비동기 실행 (SQLite + asyncio)
    start_time = time.time()
    asyncio.run(main())
    print(f"비동기 처리 실행 시간 : {time.time() - start_time:.4f} 초")

    #멀티스레딩 실행 (ThreadPoolExecutor)
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(insert_news_thread, news_list)
    print(f"멀티스레딩 실행 시간 : {time.time() - start_time:.4f} 초")
    #initialize_db()를 호출해 DB 및 테이블을 생성
    #asyncio.run(main())을 실행해 비동기 방식으로 뉴스 삽입 & 실행 시간 출력
    #ThreadPoolExecutor를 이용해 멀티스레딩 방식으로 뉴스 삽입 & 실행 시간 출력
    #두 방식의 속도를 비교하여 어떤 방식이 더 빠른지 확인
