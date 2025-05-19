# 1. Python 이미지 사용
FROM python:3.10

# 2. 작업 디렉터리 설정
WORKDIR /app

# 3. requirements 파일 복사
COPY requirements-main.txt .
COPY requirements-*.txt .

# 4. pip 최신화
RUN pip install --upgrade pip

# 5. 패키지 설치 (hash mismatch 방지 옵션 추가)
# torch 먼저 설치
RUN pip install --no-cache-dir torch==2.6.0
RUN pip install --no-cache-dir -r requirements-base.txt \
    && pip install --no-cache-dir -r requirements-nlp.txt \
    && pip install --no-cache-dir -r requirements-deeplearning.txt \
    && pip install --no-cache-dir -r requirements-crawling.txt \
    && pip install --no-cache-dir -r requirements-db.txt \
    && pip install --no-cache-dir -r requirements-visualization.txt \
    && pip install --no-cache-dir -r requirements-utils.txt \
    && pip install --no-cache-dir -r requirements-aws.txt

# 6. 앱 코드 전체 복사
COPY . .

# 7. 실행 명령
CMD ["bash"]
