from konlpy.tag import Okt
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud

from naver_pay_process import naver_pay_news_process

#감성사전
DEFAULT_SENTIMENT_DICT = {
    '성장': 2, '상승': 1, '호재': 2, '기대': 1, '안정': 2, '장세': 1, '반등': 2,
      '흑자': 2, '상장': 2, '전환': 1, '제동': 1, '들뜬': 1, '호가': 2, '회복': 2,
      '흥행': 2, '대성공': 3, '급등': 1, '강세': 2,'호황': 3, '상향': 3, '유망': 2,
      '신뢰': 3, '상승세': 1, '상승률': 1, '성공적': 2, '안정세': 1, '기대감': 2, '회복세': 1, '흑자전환': 3,
      '유망주': 2, '강세장': 2, '호재성': 2, '흥행성': 2,
      
      '하락': -1, '위기': -2, '손실': -1, '불안': -2, '적자': -3, '경고': -2, '실패': -1, 
      '매수': -2, '포기': -1, '저점': -2, '폭락': -3, '적기': -2, '피해': -1, '오류': -2,
      '충돌': -1, '장애': -1, '압박': -2, '급락': -3, '약세': -2, '불황': -3, '하향': -1,
      '부진': -2, '불확실': -2, '침체': -3, '둔화': -2, '하락세': -1, '불확실성': -2, 
      '위기감': -2, '침체기': -2, '급락세': -2,'불안정': -2, '약세장': -2, '적자지속': -3, 
      '실패작': -2, '폭락장': -3
}

#감성사전과 워드클라우드
def naver_pay_news_wordcloud(df_naver, nouns, sentiment_dict=DEFAULT_SENTIMENT_DICT, font_path="C:/Windows/Fonts/malgun.ttf"):
    #감성 점수
    total_score = 0
    word_score = []

    for word in nouns:
        if word in sentiment_dict:
            score = sentiment_dict[word]
            total_score += score
            word_score.append((word, score))

    print(f'[감성 점수 분석] 총 점수 : {total_score}')
    print(f'[상위 감성 단어 (상위 5개)] : {word_score[:5]}')

    #워드클라우드
    counter = Counter(nouns)
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

    return total_score, word_score
