import time
import requests
import asyncio
import aiohttp

#예제 URL
URL = "https://news.naver.com/main/ranking/popularDay.naver"

#request 모듈을 이용한 동기 방식식
def fetch_news():
    #웹페이지 요청
    response = requests.get(URL)
    return response.text

#실행 시간 측정
start_time = time.time()
for _ in range(10):
    #10번 요청
    fetch_news()
end_time = time.time()

print(f"동기 방식 실행 시간 :  {end_time - start_time : .2f}초")

#asyncio + aiohttp를 이용한 비동기 방식
async def fetch_news_async(session):
    async with session.get(URL) as response:
        return await response.text()
    
async def main():
    async with aiohttp.ClientSession() as session:
        #10번 요청
        tasks = [fetch_news_async(session) for _ in range(10)]
        await asyncio.gather(*tasks)

#실행 시간 측정
start_time = time.time()
asyncio.run(main())
end_time = time.time()

print(f"비동기 방식 실행 시간 : {end_time - start_time : .2f}초")

#TCPConnector로 동시 요청 개수 제한
async def main_2():
    #동시 요청 개수 제한
    connector = aiohttp.TCPConnector(limit=5)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [fetch_news_async(session) for _ in range(10)]
        await asyncio.gather(*tasks)

#실행 시간 측정
start_time = time.time()
#동시 요청 개수 제한
asyncio.run(main_2())
end_time = time.time()

print(f"TCPConnector 방식 실행 시간 : {end_time - start_time : .2f}초")

#asyncio.Semaphore로 서버 부하 방지
#최대 5개의 요청만 동시에 실행
semaphore = asyncio.Semaphore(5)

async def fetch_news_semaphore(session):
    async with semaphore:
        async with session.get(URL) as response:
            return await response.text()

#semaphore 방식 실행
async def main_3():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_news_semaphore(session) for _ in range(10)]
        await asyncio.gather(*tasks)

#실행 시간 측정
start_time = time.time()
#semaphore 방식 실행
asyncio.run(main_3())
end_time = time.time()

print(f"semaphore 방식 실행 시간 : {end_time - start_time : .2f}초")
