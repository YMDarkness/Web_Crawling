# 1. Python 이미지 사용
FROM python:3.12

# 2. 작업 디렉터리 설정
WORKDIR /app

# 3. 현재 폴더 안의 모든 파일 복사 (이제는 .dockerignore로 제외됨)
COPY requirements.txt .

# 4. 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 5. 실행 명령 (필요 시 수정 가능)
CMD ["bash"]
