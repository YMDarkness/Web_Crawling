import sqlite3
import pandas as pd
import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation

#오늘 날짜 기반 파일명 생성
today_date = datetime.datetime.now().strftime("%Y-%m-%d")
lda = f"{today_date}_news_report_LDA.csv"

#csv 파일 로드
df = pd.read_csv("2025-02-20_news_report.csv")
print(df[['title', 'keyword', 'timestamp']].head(10))

#긴 문자열도 모두 출력하도록 설정 (기본값 50)
#1000자로 설정 더 늘릴 수 있음
pd.options.display.max_colwidth = 10000

#SQLite에서 뉴스 데이터 가져오기
db_filename = "2025-02-20_news.db"

#SQLite에 연결
conn = sqlite3.connect(db_filename)

#SQL 쿼리를 실행하여 데이터 불러오기
db = pd.read_sql_query("SELECT * FROM news_articles", conn)

#연결 종료
conn.close()

#데이터 확인
print(db.head())

#TF-IDF 벡터화 및 LDA 모델 적용
def apply_lda(news_title, num_topics=5):
    vectorizer = TfidfVectorizer(stop_words='english', max_features=10000)
    tfidf_matrix = vectorizer.fit_transform(news_title)

    lda_model = LatentDirichletAllocation(n_components=num_topics, random_state=42)
    lda_matrix = lda_model.fit_transform(tfidf_matrix)

    #각 기사에 가장 적합한 토픽 할당
    topics = lda_matrix.argmax(axis=1)
    return topics

#LDA 적용 및 결과 저장
def save_result():
    news_db = db
    if news_db.empty:
        print(f"뉴스 데이터가 없습니다")
        return
    
    #LDA 모델 적용
    news_db['topic'] = apply_lda(news_db['title'])

    #DB에 업데이트
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()
    for idx, row in news_db.iterrows():
        cursor.execute("UPDATE news_articles SET category = ? WHERE id = ?", (f"topic {row['topic']}", row['id']))
    
    conn.commit()
    conn.close()

    #csv 저장
    news_db.to_csv(lda, index=False, encoding='utf-8-sig')
    print(f"LDA 분석 결과가 {lda}에 저장되었습니다")

#실행
if __name__ == "__main__":
    save_result()
