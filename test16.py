import sqlite3
import pandas as pd
import datetime

#오늘 날짜 기반 DB 파일명 설정
today_date = datetime.datetime.now().strftime("%Y-%m-%d")
db_filename = f"{today_date}_news.db"

#SQLite에서 뉴스 데이터 로드
def load_news_date():
    conn = sqlite3.connect(db_filename)
    query = "SELECT keyword, title FROM news_articles"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

#데이터 로드 확인
news_df = load_news_date()
#상위 5개 데이터 확인
print(news_df.head())
