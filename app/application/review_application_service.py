import asyncio

from fastapi import HTTPException

from app.services.place_service import place_fetcher, place_parser
from app.services.reviews_service import reviews_fetch, reviews_parser


class ReviewApplicationService:
    
    async def execute_review(self, store_name):
        """
        1. 상호명으로 PLACE ID 검색
        2. PLACE ID로 리뷰 검색
        3. 리뷰 분석 로직 작동
        4. DB 보고서 결과 저장
        5. 반환
        
        조건 : 크롤링 과정이 오래 걸릴 것으로 추정되므로 백그라운드로 작동 및 SSE나 WEBSOCKET과 같은 비동기 통신 사용
        
        return : 
        """
        
        # 1
        html = await asyncio.get_event_loop().run_in_executor(
            None, place_fetcher, store_name, False
        )
        # 추출된 place id
        place_id = place_parser(html)
        
        # 2
        more_reviews = 5 # 더보기 클릭 횟수
        html = await asyncio.get_event_loop().run_in_executor(
            None, reviews_fetch, place_id, more_reviews
        )
        
        reviews = reviews_parser(html)
        if not reviews:
            raise HTTPException(status_code=404, detail="리뷰를 찾을 수 없습니다.")
        
        # 3 리뷰 분석 로직 추가
    
        # 4 DB 저장
        
        # 5 return -> redis event를 통해 웹소켓 서버에 이벤트 발행 후 유저에게 전달
        