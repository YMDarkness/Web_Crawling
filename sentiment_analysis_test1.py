import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from konlpy.tag import Okt
from collections import Counter

#크롤링-----------------------------------------
url = f"https://finance.naver.com/news/mainnews.naver"

headers = {'User-Agent' : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

response = requests.get(url, headers=headers)
response.raise_for_status()

soup = BeautifulSoup(response.text, 'html.parser')

titles = soup.select("dd.articleSubject a")

timeline = datetime.today().strftime("%Y-%m-%d")

filename = 'naver_pay_konlpy.csv'
with open(filename, mode="w", encoding="utf-8-sig", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["번호", "제목", "날짜"])

    for idx, title in enumerate(titles):
        article = title.get_text(strip=True)
        writer.writerow([idx, article, timeline])

print(f"데이터 크롤링 및 {filename} 저장 완료")

#데이터 분석-----------------------------------------
df = pd.read_csv(filename, encoding="utf-8-sig")
text = " ".join(df["제목"])

#형태소 분석기
#Okt 형태소 분석기로 텍스트에서 명사만 추출
#데이터에서 감성 단어를 찾기 위해 명사만 골라내는 단계
okt = Okt()

#명사 추출
nouns = okt.nouns(text)

#감성 사전
#감성 사전이란
#긍정적인 단어와 부정적인 단어를 미리 정의해 놓은 사전
#텍스트 데이터에서 긍정적인 단어와 부정적인 단어를 추출하여 감성을 분석하는 방법
#긍정/부정 감정을 나타내는 단어의 집합
#데이터를 분류하는 기준준
positive_words = ['성장', '상승', '호재', '기대', '안정', '장세', '반등', '흑자', '상장', '전환', '제동']
negative_words = ['하락', '위기', '손실', '불안', '적자', '경고', '실패', '매수', '포기', '저점', '폭락', '적기', '피해']

#긍정/부정 단어 필터링
#추출된 명사 중 긍정 단어와 부정 단어만 따로 분류
#감성 단어 필터링을 통해 긍정/부정 감성 점수를 구할 수 있다
#람다식
#for word in nouns > 추출된 명사 리스트에서
#if word in positive_words > 감성 사전에 있는 긍정 단어만 필터링
positive_nouns = [word for word in nouns if word in positive_words]
negative_nouns = [word for word in nouns if word in negative_words]

#한 글자 단어 제외
nouns = [word for word in nouns if len(word) > 1]

#단어 빈도 수 계산
#Counter(nouns)로 단어 빈도 수 계산
#전체 워드클라우드 생성
word_count = Counter(nouns)

#워드클라우드 생성
wordcloud = WordCloud(font_path="C:/Windows/Fonts/malgun.ttf", background_color="white", width=800, height=400)
cloud = wordcloud.generate_from_frequencies(word_count)

#시각화-----------------------------------------
plt.imshow(cloud, interpolation="bilinear")
plt.axis('off')
plt.show()

#긍정 워드클라우드
#긍정 워드클라우드 생성
positive_words_count = Counter(positive_nouns)
positive_cloud = wordcloud.generate_from_frequencies(positive_words_count)
plt.title("positive word cloud")
plt.imshow(positive_cloud, interpolation="bilinear")
plt.axis('off')
plt.show()

#부정 워드클라우드
#부정 워드클라우드 생성
negative_words_count = Counter(negative_nouns)
negative_cloud = wordcloud.generate_from_frequencies(negative_words_count)
plt.title("negative word cloud")
plt.imshow(negative_cloud, interpolation="bilinear")
plt.axis('off')
plt.show()

'''
negative_words_count = Counter(negative_nouns)와 positive_words_count = Counter(positive_nouns)

Counter는 리스트의 형태의 데이터를 단어별 빈도수로 변환해주는 기능
positive_nouns, negative_nouns 리스트에서 긍정/부정 단어의 빈도수를 계산
예 Counter({'성장':2, '상승':2, '호재':1})

positive_cloud = wordcloud.generate_from_frequencies(positive_words_count)와
negative_cloud = wordcloud.generate_from_frequencies(negative_words_count)

WordCloud의 generate_from_frequencies() 함수는 단어 빈도수에 따라 워드클라우드를 생성하는 함수
단어 빈도수가 높을수록 글자가 크게 나오고, 빈도수가 낮으면 작게 표현
'''
