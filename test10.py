import requests
from bs4 import BeautifulSoup
import os
from PIL import Image
import io
import time

# 검색할 키워드
search_keywords = ["고토 히토리", "이지치 니지카", "키타 이쿠요", "야마다 료", "히로이 키쿠리"]

# User-Agent 설정
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# 중복된 폴더명을 방지하는 함수
def get_unique_folder_name(base_folder):
    folder_name = base_folder
    counter = 1

    # 폴더가 존재하면 숫자를 붙여 새 폴더명 작성
    while os.path.exists(folder_name):
        folder_name = f"{base_folder}_{counter}"
        counter += 1

    # 최종적으로 생성된 폴더 만들기
    os.makedirs(folder_name)
    return folder_name

for keyword in search_keywords:
    # 키워드를 안전한 파일명으로 변환
    safe_keyword = keyword.replace(" ", "_")
    
    # 키워드별 폴더 생성
    save_dir = os.path.join("images", safe_keyword)
    os.makedirs(save_dir, exist_ok=True)

    # 네이버 이미지 검색
    search_url = f"https://search.naver.com/search.naver?where=image&query={keyword}"

    # 요청 보내기
    response = requests.get(search_url, headers=headers)
    response.raise_for_status()

    # HTML 파싱
    soup = BeautifulSoup(response.text, "html.parser")
    image_tags = soup.select(".thumb img")

    # 저장할 폴더 내 기존 이미지 확인
    existing_files = set(os.listdir(save_dir))

    # 이미지 최소 크기 설정 (예: 50x50)
    MIN_WIDTH, MIN_HEIGHT = 50, 50

    # 이미지 다운로드 (상위 10개)
    for idx, img_tag in enumerate(image_tags[:10]):
        img_url = img_tag["src"] if 'http' in img_tag["src"] else 'https:' + img_tag["src"]
        img_path = os.path.join(save_dir, f"{safe_keyword}_{idx + 1}.jpg")

        # 중복된 파일 확인
        if os.path.basename(img_path) in existing_files:
            print(f"이미 존재하는 이미지 파일 건너뛰기: {img_path}")
            continue

        # 이미지 다운로드 시 예외 처리
        try:
            response = requests.get(img_url, timeout=5)
            response.raise_for_status()
            img_data = response.content
        except requests.exceptions.RequestException as e:
            print(f"이미지 다운로드 실패: {img_url} ({e})")
            continue

        # 이미지 크기 확인
        try:
            img = Image.open(io.BytesIO(img_data))
            width, height = img.size
        except Exception as e:
            print(f"손상된 이미지 건너뛰기: {img_path} ({e})")
            continue

        if width < MIN_WIDTH or height < MIN_HEIGHT:
            print(f"이미지 크기가 너무 작음 건너뛰기: {img_path} ({width}x{height})")
            continue

        # 새 이미지 다운로드
        with open(img_path, "wb") as f:
            f.write(img_data)

        print(f"이미지 다운로드 완료: {img_path} ({width}x{height})")

        # 요청 간격 조절
        time.sleep(1)

print("모든 키워드에 대한 이미지를 중복 없이 크롤링 완료!")
