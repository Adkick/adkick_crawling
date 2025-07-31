FROM python:3.13.5-slim

# 시스템 환경 설정
ENV TZ=Asia/Seoul
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/home/app


# 크롬 브라우저와 크롬 드라이버를 설치합니다.
RUN apt-get update && apt-get install -y wget curl unzip
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install -y ./google-chrome-stable_current_amd64.deb
RUN rm ./google-chrome-stable_current_amd64.deb

# 시스템 패키지 업데이트 및 필수 패키지 설치
RUN apt-get install -y gcc default-libmysqlclient-dev pkg-config \
    && rm -rf /var/lib/apt/lists/*

# 작업 디렉토리 설정
WORKDIR /home

# requirements.txt 먼저 복사 (Docker 캐시 최적화)
COPY requirements.txt /home

# Python 패키지 설치
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . /home

# 권한 설정 (필요시)
RUN chmod +x /home

# 포트 노출
EXPOSE 80

# 애플리케이션 실행
CMD ["uvicorn", "app.main:app", \
     "--host", "0.0.0.0", \
     "--port", "80", \
     "--workers", "4"]