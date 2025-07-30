FROM python:3.13.5-slim

# 시스템 환경 설정
ENV TZ=Asia/Seoul
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/home/app

# 시스템 패키지 업데이트 및 필수 패키지 설치
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# 작업 디렉토리 설정
WORKDIR /home/app

# requirements.txt 먼저 복사 (Docker 캐시 최적화)
COPY requirements.txt /home/app/

# Python 패키지 설치
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . /home/app/

# 권한 설정 (필요시)
RUN chmod +x /home/app

# 포트 노출
EXPOSE 80

# 애플리케이션 실행
CMD ["uvicorn", "app.main:app", \
     "--host", "0.0.0.0", \
     "--port", "80", \
     "--workers", "4"]