from naver_pay_crwal import naver_pay_news_crwal
from naver_pay_process import naver_pay_news_process
from naver_pay_wordcloud import naver_pay_news_wordcloud
from naver_pay_wordcloud import DEFAULT_SENTIMENT_DICT
from naver_pay_sentiment import plot_sentiment_trend
from naver_pay_sentimentdaily import sentiment_daily_date
#from naver_pay_weights import 
from naver_pay_graph import naver_pay_news_graph

def main():
    #크롤링
    df_naver = naver_pay_news_crwal()

    #데이터 전처리
    df_naver_process, nouns = naver_pay_news_process(df_naver)

    #감성사전과 워드클라우드
    total_score, word_score = naver_pay_news_wordcloud(df_naver_process, nouns)

    #감성점수 시각화 (이동평균, 히스토그램)
    df_result = plot_sentiment_trend(df_naver, sentiment_dict=DEFAULT_SENTIMENT_DICT)

    #시간별 감성 점수

    #날짜별 감성 점수

    #날짜별 데이터량
    df_daily = sentiment_daily_date(df_naver, df_result, DEFAULT_SENTIMENT_DICT)

    #파이그래프, 박스플롯
    naver_pay_news_graph(df_naver, sentiment_dict=DEFAULT_SENTIMENT_DICT)

if __name__ == '__main__':
    main()


'''
기능 및 구현 방법
크롤링 > 전처리 > 감성점수, 워드클라우드

감성점수 이동평균, 감성점수 분포(히스토그램)

시간별 감성점수 (시간 단위가 실제로 시간대면 ok)

날짜별 감성점수
날짜별 데이터수

파이그래프, 박스플롯
'''