# Naver Map Crawling API

## 개요
- 네이버 지도에서  
  1. 장소 검색 (키워드 → 점포 및 상호)  
  2. place_id 조회 (상호명 → Place ID)  
  3. 리뷰 크롤링 (Place ID → 리뷰 리스트)  
  기능을 FastAPI로 제공합니다.

## 주요 기능
- **장소 검색**: `/api/stores?query=<검색어>&...`  
- **place_id 조회**: `/api/place-id?keyword=<검색어>&...`  
- **리뷰 조회**:  
  - Selenium 기반 모바일/PCMap 크롤러 (`/api/reviews?place_id=...`)

## 설치 및 실행
1. 저장소 클론  
   ```bash
   git clone <REPO_URL>
   cd <REPO_DIR>
   ```

2. 가상환경 생성 및 활성화

   ```bash
   python -m venv .venv
   source .venv/bin/activate    # macOS/Linux
   .venv\Scripts\activate       # Windows
   ```
3. 의존성 설치

   ```bash
   pip install -r requirements.txt
   ```
4. 서버 실행

   ```bash
   uvicorn app.main:app --reload
   ```

## 환경 요건

* Python 3.8 이상
* (Selenium 사용 시) Chrome 및 ChromeDriver 설치
* 네트워크 연결 필요

## 사용 예시

```bash
# 장소 검색
curl "http://127.0.0.1:8000/api/stores?query=카페"

# place_id 조회
curl "http://127.0.0.1:8000/api/place-id?keyword=강남역%20카페"

# 리뷰 조회 (v5 API)
curl "http://127.0.0.1:8000/api/reviews?place_id=1137765575&page=1&size=20&sort=RECENT"
```

## 프로젝트 구조

```
naver-map-crawling
├─ .env
├─ app
│  ├─ api
│  │  ├─ place_id.py
│  │  ├─ reviews.py
│  │  └─ stores.py
│  ├─ config.py
│  ├─ main.py
│  ├─ schemas
│  │  ├─ review.py
│  │  └─ store.py
│  ├─ services
│  │  └─ reviews_service.py
│  ├─ utils
│  │  ├─ cache.py
│  └─ └─ logger.py
├─ README.md
├─ requirements.txt
└─ tests
   └─ test.py

```

## 레퍼런스

* v5 API 엔드포인트: `https://map.naver.com/v5/api/contents/reviews`