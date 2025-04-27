import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.svm import SVC

#csv 파일 로드
df = pd.read_csv("2025-02-21_news_report.csv")

#csv 칼럼 확인
print(f"csv 파일 칼럼 목록 : ",df.columns.tolist())

#keyword를 라벨로 변환
df['label'] = df['keyword'].astype("category").cat.codes
print(df[['keyword', 'label']].head())

#입력(x)와 출력(y) 설정
#뉴스 제목 (텍스트 데이터)
X = df['title']
#분류할 키워드 (숫자 라벨)
y = df['label']

#데이터 분할 (학습 80%, 테스트 20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#TF-IDF 벡터화
#vectorizer = TfidfVectorizer()
#TF-IDF 벡터화 (개선)
#최대 5000개의 단어만 선택
#불용어(stop words) 제거
#단어 조합을 고려하여 벡터화
#vectorizer = TfidfVectorizer(max_features=5000, stop_words='english', ngram_range=(1,2))
vectorizer = TfidfVectorizer(max_features=7000, stop_words='english', ngram_range=(1,3))
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

#전체 데이터를 벡터화
#title 칼럼 사용
X_tfidf = vectorizer.fit_transform(df['title'])
#라벨값
y = df['label']

#랜덤 포레스트 모델 훈련
#clf = RandomForestClassifier(n_estimators=100, random_state=42)
#clf.fit(X_train_tfidf, y_train)

#모델 개선
clf = LogisticRegression()
clf.fit(X_train_tfidf, y_train)

#모델 비교
clf = SVC(kernel='linear')
clf.fit(X_train_tfidf, y_train)

#예측 수행
y_pred = clf.predict(X_test_tfidf)

#성능 평가
accuracy = accuracy_score(y_test, y_pred)
#교차 검증 수행
scores = cross_val_score(clf, X_tfidf, y, cv=5)
print(f"모델 정확도 : {accuracy : .4f}")
print(f"분류 리포트 \n", classification_report(y_test, y_pred))
print("교차 검증 정확도:", scores.mean())
