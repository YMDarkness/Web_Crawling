import requests
from bs4 import BeautifulSoup
import csv
import json
import os

#검색할 키워드
search_keyword = "고토 히토리"

#저장할 폴더 생성
save_dir = "images"
os.makedirs(save_dir, exist_ok=True)

#User-Agent 설정
headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

#네이버 이미지 검색
search_url = f"https://search.naver.com/search.naver?where=image&query={search_keyword}"

#요청 보내기
response = requests.get(search_url, headers=headers)
response.raise_for_status()

#HTML 파싱
soup = BeautifulSoup(response.text, "html.parser")

#HTML 이미지 추출
image_tags = soup.select(".thumb img")

#이미지 다운로드
for idx, img_tag in enumerate(image_tags[:10]):
    #상위 10개 이미지 다운로드
    img_url = img_tag["src"] if 'http' in img_tag["src"] else "https:" + img_tag["src"]
    img_data = requests.get(img_url).content
    img_path = os.path.join(save_dir, f"image_{idx + 1}.jpg")

    with open(img_path, "wb") as f:
        f.write(img_data)
    
    print(f"이미지 저장 완료 : {img_path}")
print(f"이미지 크롤링 완료")
