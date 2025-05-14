import pandas as pd
from konlpy.tag import Okt
from collections import Counter

from naver_pay_crwal import naver_pay_news_crwal

#데이터 전처리 및 형태소 분석
def naver_pay_news_process(df_naver):
    df_naver_process = df_naver.drop_duplicates()

    #중복없이 저장 (선택사항)
    df_naver_process.to_csv('naver_pay_graph_score.csv', encoding='utf-8-sig', index=False)

    print(f'[알람] 데이터 누적 및 중복 제거 완료')

    #제목 결합 후 형태소 분석
    text = ' '.join(df_naver_process['제목'])

    #형태소 분석
    okt = Okt()

    #명사 추출
    nouns = okt.nouns(text)

    return df_naver_process, nouns
