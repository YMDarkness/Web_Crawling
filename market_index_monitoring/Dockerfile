FROM python:3.10

# 작업 디렉터리
WORKDIR /app

COPY . /app

# 의존성 설치
RUN pip install --no-cache-dir -r requirements.txt

# 기본 실행 명령 (flask 서버용)
# CMD ["python", "main.py"]
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "exporter:app"]
