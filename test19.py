import pandas as pd
import matplotlib.pyplot as plt
from konlpy.tag import Okt
from sklearn.feature_extraction.text import TfidfVectorizer
from wordcloud import WordCloud

#뉴스 데이터 불러오기
#뉴스 데이터 로드
df = pd.read_csv("2025-02-16_news_report.csv")

#기사 제목과 본문만 사용
#결측값 제거
df = df[['keyword', 'title']].dropna()

#데이터 확인
print(df.head(), "\n")

#텍스트 전처리 (형태소 분석)
okt = Okt()

#뉴스 본문에서 명사만 추출하는 함수
def extract_nouns(text):
    return " ".join(okt.nouns(text))

#본문에서 명사만 추출
df["nouns"] = df["title"].apply(extract_nouns)

#데이터 확인
print(df["nouns"].head(), "\n")

#TF-IDF 적용하여 키워드 추출
#TF-IDF 벡터화
#상위 1000개 단어만 사용
vectorizer = TfidfVectorizer(max_features=1000)
tfidf_matrix = vectorizer.fit_transform(df["nouns"])

#단어 목록과 점수 확인
words = vectorizer.get_feature_names_out()
tfidf_scores = tfidf_matrix.toarray().sum(axis=0)

#단어별 점수를 데이터프레임으로 정리
tfidf_df = pd.DataFrame({"word" : words, "score" : tfidf_scores})
#중요 단어 정렬
tfidf_df = tfidf_df.sort_values(by="score", ascending=False)

#상위 20개 단어 출력
print(tfidf_df.head(20), "\n")

#키워드 시각화 (워드클라우드)
#워드클라우드 생성
wordcloud = WordCloud(font_path="malgun.ttf", background_color="white", width=800, height=400).generate_from_frequencies(
    dict(zip(tfidf_df["word"], tfidf_df["score"]))
)

#워드클라우드 출력
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()
