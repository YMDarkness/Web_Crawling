import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

#간단한 방식
#texts = ["대통령 윤석열 탄핵 소추심판", "위기의 삼성전자 과연 이대로", "금값이 금값... 폭등한 금값에.."]
#labels = ["정치", "사회", "경제"]

#vectorizer = TfidfVectorizer()
#X = vectorizer.fit_transform(texts)

#model = MultinomialNB()
#model.fit(X, labels)

#test = vectorizer.transform(["금값 폭등에 은도 껑충.. 은도 없다"])
#print(model.predict(test))

#csv 파일 로드
df = pd.read_csv("2025-02-19_news_report.csv")

#긴 문자열도 모두 출력하도록 설정 (기본값 50)
#1000자로 설정 더 늘릴 수 있음
pd.options.display.max_colwidth = 1000

#데이터 확인
#print(df.head())
#print(df.head().to_string())
print(df[["title", "keyword"]].head(10))

#데이터 분리
#뉴스 제목 (입력 데이터)
#'title' -> 뉴스 내용(입력 데이터)
#NaN 방지를 위해 str 변환
texts = df['title'].astype(str)
#카테고리 (정답 데이터)
#'keyword' -> 카테고리 레이블
labels = df['keyword'].astype(str)

#학습 데이터와 테스트 데이터 나누기 (학습 80%, 테스트 20%)
X_train, X_test, Y_train, Y_test = train_test_split(texts, labels, test_size=0.2, random_state=42)

#TF-IDF 벡터 변환
#같은 벡터 객체를 사용하도록 변경
vectorizer = TfidfVectorizer()
#학습 데이터
X_train_tfidf = vectorizer.fit_transform(X_train)
#테스트 데이터
X_test_tfidf = vectorizer.transform(X_test)
#fit_transform() -> 새로운 단어 사전을 만듬

#Naive Bayes 분류기 학습
#모델 학습
model = MultinomialNB()
model.fit(X_train_tfidf, Y_train)

#테스트 데이터 예측
Y_pred = model.predict(X_test_tfidf)

#정확도 출력
accuracy = accuracy_score(Y_test, Y_pred)
print(f"모델 정확도 : {accuracy : .4f}")

#새로운 뉴스 예측
new_text = ["금값 폭등에 은도 껑충.. 은도 없다"]
new_text_tfidf = vectorizer.transform(new_text)
predicted_category = model.predict(new_text_tfidf)

print(f"예측된 카테고리 : {predicted_category}")
