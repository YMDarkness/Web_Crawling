import pandas as pd
import numpy as np
import nltk
import os
import networkx as nx
import asyncio
import matplotlib.pyplot as plt
from konlpy.tag import Okt
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.naive_bayes import MultinomialNB
from wordcloud import WordCloud
import pdfkit
import markdown as md
from markdown2 import markdown
from nltk.tokenize import word_tokenize

#nltk 다운로드
#nltk.download()
nltk.download('punkt')
nltk.download('stopwords')
text = "Hello, this is a test sentence"
tokens = word_tokenize(text)
print(tokens)

#뉴스 데이터 불러오기
#df = pd.read_csv("2025-02-23_news_report.csv")
def load_news_data(csv_file):
    print(f"불러올 파일 경로 : {csv_file}")
    try:
        df = pd.read_csv(csv_file)
        df = df[['keyword', 'title']].dropna()
        return df
    except FileNotFoundError:
        print(f"파일을 찾을 수 없습니다 : {csv_file}")
        exit()

    df = pd.read_csv(csv_file)
    df = df[['keyword', 'title']].dropna()
    return df

#데이터 전처리 (형태소 분석)
okt = Okt()
def extract_nouns(text):
    return " ".join(okt.nouns(text))

def preprocess_data(df):
    df['nouns'] = df['title'].apply(extract_nouns)
    return df

#키워드 분석 (TF-IDF)
def analyze_keyword(df):
    vectorizer = TfidfVectorizer(max_features=10000)
    tfidf_matrix = vectorizer.fit_transform(df['nouns'])
    words = vectorizer.get_feature_names_out()
    scores = tfidf_matrix.toarray().sum(axis=0)
    return pd.DataFrame({'word' : words, 'score' : scores}).sort_values(by='score', ascending=False)

#뉴스 요약
def summarize_text(df, top_n=2):
    tfidf_matrix = TfidfVectorizer().fit_transform(df['nouns'])
    similarity_matrix = cosine_similarity(tfidf_matrix)
    graph = nx.from_numpy_array(similarity_matrix)
    scores = nx.pagerank(graph)
    ranked_sentences = sorted(((scores[i], s) for i, s in enumerate(df['title'])), reverse=True)
    return [s for _, s in ranked_sentences[:top_n]]

#감성 분석 (간단한 학습)
def train_sentiment_model():
    train_texts = ["최대 규모", "긍정적 평가", "최다 기록", "국회", "윤석열 대통령", "여야", "저출산", "소비자 물가 상승", "청년 취업률 역대 최저"]
    train_labels = ["긍정", "긍정", "긍정", "중립", "중립", "중립", "부정", "부정", "부정"]
    vectorizer = CountVectorizer()
    x_train = vectorizer.fit_transform(train_texts)
    model = MultinomialNB()
    model.fit(x_train, train_labels)
    return model, vectorizer

def predict_sentiment(df, model, vectorizer):
    x_test = vectorizer.transform(df['title'])
    df['sentiment'] = model.predict(x_test)
    return df

#결과 저장 (csv, json, markdown, pdf)
def save_result(df, tfidf_df, summary, output_file):
    df.to_csv(f'{output_file}.csv', index=False)
    df.to_json(f'{output_file}.json', force_ascii=False, indent=4)

    markdown_content = f"""
    #뉴스 분석 보고서

    ##주요 키워드
    {tfidf_df.head(10).to_markdown(index=False)}

    ##뉴스 요약
    {'\n'.join(f'- {s}' for s in summary)}

    #감성 분석 결과
    {df[['title', 'sentiment']].to_markdown(index=False)}
    """

    md_file = f'{output_file}.md'
    pdf_file = f'{output_file}.pdf'

    with open(md_file, 'w', encoding='utf-8-sig') as f:
        f.write(markdown_content)

    print(f"Markdown 파일 생성 완료 : {md_file}")

    #wkhtmltopdf 실행 파일 경로 지정
    wkhtmltopdf_path = "C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"

    #Markdown 파일 경로
    md_file = "news_analysis_report.md"
    html_file = "news_analysis_report.html"
    pdf_file = "news_analysis_report.pdf"

    #Markdown -> html 변환
    with open(md_file, "r", encoding='utf-8-sig') as f:
        md_text = f.read()
    
    #패키지 markdown과 내장 함수의 충돌
    html_text = md.markdown(md_text)

    #html 파일로 저장
    with open(html_file, "w", encoding='utf-8-sig') as f:
        f.write(html_text)

    #pdf 변환
    if os.path.exists(wkhtmltopdf_path):
        config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)
        pdfkit.from_file(html_file, pdf_file, configuration=config)
        print(f"PDF 변환 완료 : {pdf_file}")
    else:
        print("wkhtmltodf 실행 파일을 찾을 수 없습니다")

async def main():
    print("뉴스 크롤링 시작 . . .")

#실행 코드
if __name__ == "__main__":
    asyncio.run(main())
    csv_file = "2025-02-23_news_report.csv"
    output_file = "news_analysis_report"

    df = load_news_data(csv_file)
    df = preprocess_data(df)

    tfidf_df = analyze_keyword(df)
    summary = summarize_text(df)

    model, vectorizer = train_sentiment_model()
    df = predict_sentiment(df, model, vectorizer)

    save_result(df, tfidf_df, summary, output_file)
    print(f"분석 및 보고서 생성 완료")
