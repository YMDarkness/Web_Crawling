import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import pandas as pd
import os

#웹 크롤링
def naver_pay_news_crwal(filename='naver_pay_graph_score'):
    url = f"https://finance.naver.com/news/mainnews.naver"
    headers = {'User-Agent' : 
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    titles = soup.select("dd.articleSubject a")

    timeline = datetime.today().strftime('%Y-%m-%d')
    filename = f'naver_pay_graph_score.csv'

    #CSV 파일을 불러와 추가 저장 (기존 데이터 유지 & 새 데이터 추가)
    '''
    변경된 점

    pd.read_csv()로 기존 CSV 파일을 불러오기
    기존 데이터가 있을 경우 새로운 데이터와 병합하여 저장
    to_csv()로 덮어쓰기하여 최신 상태 유지
    기존 데이터가 있다면 번호 자동 증가 (중복 방지)
    '''

    #기존 파일 로드
    if os.path.exists(filename):
        df_existing = pd.read_csv(filename, encoding='utf-8-sig')
    else:
        df_existing = pd.DataFrame(columns=['번호', '제목', '시간'])

    #새로운 데이터 수집
    new_date = []
    start_idx = len(df_existing) + 1  # 기존 번호 뒤부터 시작

    for idx, title in enumerate(titles, start=start_idx):
        article = title.get_text(strip=True)
        new_date.append([idx, article, timeline])

    #새로운 데이터를 DateFrame으로 변환
    df_new = pd.DataFrame(new_date, columns=['번호', '제목', '시간'])

    #기존 데이터와 새로운 데이터 합치기
    df_naver = pd.concat([df_existing, df_new], ignore_index=True)

    # 제목 기준으로 중복 제거 (번호나 시간은 다르더라도 같은 뉴스는 제거)
    df_naver = df_naver.drop_duplicates(subset='제목')

    #최종 데이터 저장 (덮어쓰기)
    df_naver.to_csv(filename, index=False, encoding='utf-8-sig')

    print('[알람] csv 파일 데이터 업데이트 완료')

    '''
    기존 CSV 파일 불러오기

    os.path.exists(filename)을 사용하여 파일이 존재하는지 확인
    파일이 있으면 pd.read_csv()로 기존 데이터를 불러옴
    없으면 새로운 빈 DataFrame 생성
    새로운 뉴스 데이터 추가
    titles 리스트에서 기사 제목을 추출하여 새로운 리스트 new_data에 저장
    enumerate()를 활용해 기존 데이터 개수를 고려하여 번호를 자동 증가
    기존 데이터 + 새로운 데이터 병합
    pd.concat([df_existing, df_new], ignore_index=True)를 사용해 기존 데이터와 새로운 데이터 합침
    ignore_index=True를 사용하여 번호(Index)를 재정렬
    CSV 파일 저장
    df_combined.to_csv(filename, index=False, encoding='utf-8-sig')
    기존 데이터를 덮어쓰기하여 최신 뉴스가 계속 추가되도록 함

    결과:
    이제 naver_pay_graph_score.csv 파일이 지속적으로 업데이트되며, 기존 데이터를 유지하면서도 새로운 뉴스 제목을 추가할 수 있음
    '''

    return df_naver
