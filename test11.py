import aiohttp
import asyncio
import os
import time
import csv
import json
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

# 검색할 키워드
search_keywords = ["고토 히토리", "이지치 니지카", "키타 이쿠요", "야마다 료", "히로이 키쿠리"]

# User-Agent 설정
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

#최대 동시 요청 개수 설정 (네트워크 요청 제한)
semaphore = asyncio.Semaphore(5)

# 로그 저장 함수 (csv, json)
def log_download(file_path, log_data, format='csv'):
    if format == 'csv':
        file_exists = os.path.exists(file_path)
        with open(file_path, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["Keyword", "Image_Name", "Status", "Path"])
            if not file_exists:
                writer.writeheader()
            writer.writerow(log_data)
    elif format == 'json':
        if os.path.exists(file_path):
            with open(file_path, mode='r', encoding='utf-8') as f:
                logs = json.load(f)
        else:
            logs = []
        logs.append(log_data)
        with open(file_path, mode='w', encoding='utf-8') as f:
            json.dump(logs, f, ensure_ascii=False, indent=4)

#비동기 이미지 다운로드 함수
async def download_img(session, img_url, img_path, keyword):
    #요청 수 제한 적용
    async with semaphore:
        try:
            async with session.get(img_url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                if response.status == 200:
                    img_data = await response.read()
                    with open(img_path, "wb") as f:
                        f.write(img_data)

                    log_data = {
                        "Keyword" : keyword,
                        "Image_Name" : os.path.basename(img_path),
                        "Status" : "Downloaded",
                        "Path" : img_path
                    }
                    log_download(f"download_log.csv", log_data, format='csv')
                    log_download(f"download_log.json", log_data, format='json')
                    print(f"다운로드 완료 : {img_path}")
                else:
                    print(f"다운로드 실패 : {img_url}")
        except Exception as e:
            print(f"오류 발생 : {e}")

#이미지 크롤링 함수 (비동기)
async def fetch_and_download_images(session, keyword):
    safe_keyword = keyword.replace(" ", "_")
    save_dir = os.path.join("images", safe_keyword)
    os.makedirs(save_dir, exist_ok=True)

    #네이버 이미지 검색
    search_url = f"https://search.naver.com/search.naver?where=image&query={keyword}"

    #요청 보내기
    async with session.get(search_url, headers=headers) as response:
        if response.status == 200:
            html = await response.text()

            #HTML 파싱
            soup = BeautifulSoup(html, "html.parser")  # Fixed here
            image_tags = soup.select(".thumb img")

            img_download_list = []
            #상위 10개 이미지 저장
            for idx, img_tag in enumerate(image_tags[:10]):
                img_url = img_tag["src"] if 'http' in img_tag["src"] else 'https:' + img_tag["src"]
                img_path = os.path.join(save_dir, f"{safe_keyword}_{idx + 1}.jpg")
                img_download_list.append(download_img(session, img_url, img_path, keyword))

            #이미지 다운로드 병렬 처리
            await asyncio.gather(*img_download_list)

    #요청 간격 조절
    await asyncio.sleep(1)

#비동기 크롤링 메인 함수
async def async_main():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_and_download_images(session, keyword) for keyword in search_keywords]
        await asyncio.gather(*tasks)

#멀티스레딩 크롤링 함수
def fetch_images_thred(keyword):
    import requests
    safe_keyword = keyword.replace(" ", "_")
    save_dir = os.path.join("images", safe_keyword)
    os.makedirs(save_dir, exist_ok=True)
    
    #네이버 이미지 검색
    search_url = f"https://search.naver.com/search.naver?where=image&query={keyword}"

    response = requests.get(search_url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        image_tags = soup.select(".thumb img")

        #상위 10개 이미지 다운로드
        for idx, img_tag in enumerate(image_tags[:10]):  # Fixed loop
            img_url = img_tag["src"] if 'http' in img_tag["src"] else 'https:' + img_tag["src"]
            img_path = os.path.join(save_dir, f"{safe_keyword}_{idx + 1}.jpg")

            try:
                img_data = requests.get(img_url).content
                with open(img_path, "wb") as f:
                    f.write(img_data)
                print(f"스레드 다운로드 완료 : {img_path}")
            except Exception as e:
                print(f"스레드 오류 발생 : {e}")

#멀티스레딩 실행 함수
def thread_main():
    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(fetch_images_thred, search_keywords)

#실행 시간 비교
def compare_execution_time():
    print(f"\n 비동기 방식 진행 중 ...")
    start_time = time.time()
    asyncio.run(async_main())
    async_time = time.time() - start_time
    print(f"비동기 크롤링 완료 실행 시간 : {async_time : .2f}초")

    print(f"멀티스레딩 방식 진행 중 ...")
    start_time = time.time()
    thread_main()
    thread_time = time.time() - start_time
    print(f"멀티스레딩 크롤링 완료 실행 시간 : {thread_time : .2f}초")

    print(f"\n실행 시간 비교 : 비동기({async_time : .2f}초) vs 멀티스레딩({thread_time : .2f}초)")

if __name__ == "__main__":
    compare_execution_time()
