import requests
from bs4 import BeautifulSoup
import os
import time

#검색 키워드
search_keywords = ["고토 히토리", "이지치 니지카", "키타 이쿠요", "야마다 료", "히로이 키쿠리"]

#User-Agent 설정
headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

#중복된 폴더명을 방지하는 함수
def get_unique_folder_name(base_folder):
    folder_name = base_folder
    counter = 1

    #폴더가 존재하면 숫자를 붙여 새 폴더명 작성
    while os.path.exists(folder_name):
        folder_name = f"{folder_name}({counter})"
        counter += 1

    #최종적으로 생성된 폴더 만들기
    os.makedirs(folder_name)
    return folder_name

for keyword in search_keywords:

    #키워드별 폴더 생성
    #공백을 '_'로 변경
    save_dir = get_unique_folder_name(f"images/{keyword.replace(' ', '_')}")
    os.makedirs(save_dir, exist_ok=True)

    #네이버 이미지 검색
    search_url = f"https://search.naver.com/search.naver?where=image&query={keyword}"

    #요청 보내기
    response = requests.get(search_url, headers=headers)
    response.raise_for_status()

    #HTML 파싱
    soup = BeautifulSoup(response.text, "html.parser")
    image_tags = soup.select(".thumb img")

    #이미지 다운로드
    #상위 10개의 이미지 다운로드
    for idx, img_tag in enumerate(image_tags[:10]):
        img_url = img_tag["src"] if 'http' in img_tag["src"] else 'https:' + img_tag["src"]
        img_data = requests.get(img_url).content
        img_path = os.path.join(save_dir, f"image_{idx + 1}.jpg")

        with open(img_path, "wb") as f:
            f.write(img_data)

        print(f"이미지 다운로드 완료 : {img_path}")

        #요청 간격 조절
        time.sleep(1)

print(f"모든 키워드에 대한 이미지 크롤링 완료")
