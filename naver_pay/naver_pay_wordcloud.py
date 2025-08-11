from konlpy.tag import Okt
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud
import pandas as pd
import re

from naver_pay_process import naver_pay_news_process

#감성사전
DEFAULT_SENTIMENT_DICT = [
    # 긍정 (점수 1~5)
    ('성장', 3), ('상승', 2), ('호재', 4), ('기대', 2), ('안정', 3), ('반등', 3),
    ('회복', 4), ('호황', 5), ('신뢰', 4), ('유망', 3), ('상향', 4), ('강세', 3),
    ('대박', 5), ('급등', 4), ('효자상품', 4), ('완판', 4), ('쾌거', 5), ('수혜', 3),
    ('실적개선', 4), ('급성장', 4), ('호조', 3), ('이익', 3), ('자산증가', 4),
    ('호평', 3), ('매출증가', 4), ('성과', 3), ('인기', 2), ('혁신', 3), ('도약', 3),
    ('안정세', 2), ('수출호조', 4), ('신제품', 2), ('기술력', 3), ('1위', 4),
    ('낙관', 3), ('기대감', 3), ('호전', 2), ('신기록', 4), ('사상최고', 5),
    ('수익성개선', 4), ('특수', 2), ('호조세', 3), ('순이익', 3), ('선방', 3),
    ('투자유치', 4), ('대규모수주', 5), ('상한가', 5), ('급증', 3), ('지속성장', 4),

    # 부정 (점수 -1~-5)
    ('하락', -2), ('폭락', -5), ('침체', -4), ('불안', -3), ('위기', -4),
    ('적자', -4), ('손실', -3), ('부진', -3), ('둔화', -2), ('실패', -3),
    ('불확실', -3), ('하한가', -4), ('약세', -3), ('급락', -5), ('악재', -4),
    ('위축', -2), ('철수', -4), ('취소', -3), ('폐업', -5), ('부도', -5),
    ('매각', -2), ('파산', -5), ('유출', -3), ('손해', -3), ('적자전환', -4),
    ('중단', -3), ('논란', -2), ('공포', -3), ('하락세', -2), ('불황', -4),
    ('저하', -2), ('경고', -2), ('위험', -3), ('불매', -3), ('압박', -3),
    ('타격', -3), ('혼란', -3), ('고민', -2), ('갈등', -2), ('마이너스', -2),
    ('낙폭', -3), ('침체기', -3), ('적자지속', -4), ('실패작', -3), ('불안정', -3),
    ('급락세', -4), ('악화', -3), ('감소세', -2), ('수익감소', -3),

    # 중립 or 약한 감정 (참고용)
    ('보합', 0), ('횡보', 0), ('혼조', 0), ('정체', -1), ('미지수', -1),
    ('예정', 0), ('지속', 0), ('대기', 0)
]

#감성사전과 워드클라우드
def naver_pay_news_wordcloud(df_naver, sentiment_dict=DEFAULT_SENTIMENT_DICT, font_path="C:/Windows/Fonts/malgun.ttf"):
    
    #감성사전이 리스트라면 딕셔너리로 변환
    if isinstance(sentiment_dict, list):
        if all(isinstance(item, tuple) and len(item) == 2 for item in sentiment_dict):
            sentiment_dict = dict(sentiment_dict)
        else:
            raise ValueError("감성 사전은 (단어, 점수) 형태의 튜플 리스트여야 합니다.")
    
    okt = Okt()

    # 제목 컬럼에서 NaN 제거
    all_titles = df_naver['제목'].dropna().astype(str).tolist()

    #감성 점수
    nouns = []
    score_list = []
    word_score = []
    total_score = 0
    
    # 모든 제목에서 토큰화 및 감성 점수 계산
    all_tokens = []

    for title in all_titles:
        tokens = okt.morphs(title)
        all_tokens.extend(tokens)

        for token in tokens:
            if token in sentiment_dict:
                score = sentiment_dict[token]
                total_score += score
                word_score.append((token, score))
                score_list.append(score)

    print(f'[감성 점수 분석] 총 점수 : {total_score}')
    print(f'[상위 감성 단어 (상위 5개)] : {word_score[:5]}')
    
    # 모든 명사 추출
    all_nouns = []

    # 한 글자 단어 제외
    all_nouns = [word for word in nouns if len(word) > 1]

    for sentence in all_titles:
        cleaned = re.sub(r'[^가-힣\s]', '', sentence)  # 한글과 공백만 남김

        nouns = okt.nouns(cleaned)  # 명사 추출
        nouns = [word for word in nouns if len(word) > 1]

        all_nouns.extend(nouns)

    #불용어 설정
    stopwords = set(['있다', '하다', '것', '되다', '이다', '수', '더', '등', '및', '그', '저', '이'])

    #불용어 제거
    word_score = [(w, s) for (w, s) in word_score if w not in stopwords]

    #워드클라우드
    filtered_nouns = [word for word in all_nouns if word not in stopwords]
    counter = Counter(filtered_nouns)

    wordcloud = WordCloud(
        font_path=font_path,
        background_color='white',
        width=800,
        height=400
    ).generate_from_frequencies(counter)

    plt.figure(figsize=(12, 6))
    plt.rc('font', family='Malgun Gothic')  # 윈도우 기본 폰트 설정
    plt.rcParams['axes.unicode_minus'] = False  # 마이너스 부호 깨짐 방지'
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('네이버 페이 뉴스 워드클라우드 \n')
    plt.show()

    #감성점수 분포 확인
    #plot_sentiment_distribution(score_list)

    return total_score, word_score
