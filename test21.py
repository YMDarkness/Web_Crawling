import pandas as pd
from flair.models import SequenceTagger
from flair.data import Sentence

#NER 모델 로드
tagger = SequenceTagger.load("flair/ner-english-large")

#csv 파일 로드
df = pd.read_csv("2025-02-19_news_report.csv")

#NER 분석 수행 후 개체명 리스트 저장
ner_results = []
for title in df["title"]:
    #문장 객체 생성
    sentence = Sentence(title)
    #NER 실행
    tagger.predict(sentence)

    #개체명만 추출하여 저장
    entites = [(entity.text, entity.get_label("ner").value) for entity in sentence.get_spans("ner")]
    ner_results.append(entites)

#DataFrame에 추가
df["ner_entites"] = ner_results

#결과 확인
print(df[["title", "ner_entites"]])
