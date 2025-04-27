import pandas as pd
from konlpy.tag import Okt

#뉴스 데이터 로드
df = pd.read_csv("2025-02-17_news_report.csv")

#기사 제목 사용 (결측값 제거)
df = df[['title']].dropna()

#형태소 분석기 (Okt)
okt = Okt()

#감성 단어 사전 (간단한 버전)
positive_words = ["좋다", "행복", "긍정", "성공", "승리", "기쁘다", "축하", "최고", "상승", "증가"]
negative_words = ["나쁘다", "우울", "실패", "패배", "슬프다", "위기", "문제", "최저", "갈등", "하락"]

#감성 분석 함수
def snetiment_analysis(text):
    #형태소 추출
    tokens = okt.morphs(text)
    pos_score = sum(1 for word in tokens if word in positive_words)
    neg_score = sum(1 for word in tokens if word in negative_words)

    #긍정/부정 판단
    if pos_score > neg_score:
        return "긍정"
    elif pos_score < neg_score:
        return "부정"
    else:
        return "중립"
    
#뉴스 제목 감성 분석 적용
df["sntiment"] = df["title"].apply(snetiment_analysis)

#감성 분석 결과 확인
print(df.head)
