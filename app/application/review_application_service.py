import asyncio
from datetime import datetime
import logging
from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.database import Session as DatabaseSession
from app.models.models import Store, Report, Status
from app.redis_pubsub_gateway import RedisPubSubGateway
from app.services.channel_service import ChannelService
from app.services.place_service import place_fetcher, place_parser
from app.services.reviews_service import reviews_fetch, reviews_parser

logger = logging.getLogger()

class ReviewApplicationService:
    
    def __init__(self):
        self.pubsub_gateway = RedisPubSubGateway()
        
    async def create_report(self, member_id: int, store_name: str) -> int:
        """생성 중 상태의 리포트를 DB 생성 및 리포트 번호 반환"""
        db: Session = DatabaseSession()
        try:
            # Store 조회 또는 생성
            store = db.query(Store).filter(Store.name == store_name).first()
            if not store:
                store = Store(name=store_name, created_at=datetime.now(), updated_at=datetime.now())
                db.add(store)
                db.flush()  # store_id를 얻기 위해 flush
            
            # Report 생성
            report = Report(
                request_member_id=member_id,
                store_id=store.store_id,
                status=Status.PROGRESS,
                total_review_count=0,
                created_at=datetime.now()
            )
            db.add(report)
            db.commit()
            
            return report.report_id
        except Exception as e:
            db.rollback()
            logger.error(f"리포트 생성 실패: {e}")
            raise HTTPException(status_code=500, detail="리포트 생성에 실패했습니다.")
        finally:
            db.close()

    async def execute_review(self, member_id: int, report_id: int, store_name: str):
        """
        순차실행하되 각 단계를 별도 스레드에서 실행하여 블로킹 방지
        """
        try:
            loop = asyncio.get_event_loop()
            
            # 진행 상태 알림
            if member_id:
                channel = ChannelService.get_user_channel(member_id)
                await self.pubsub_gateway.publish_to_channel(channel, {
                    "status": "started",
                    "message": "장소 검색 중...",
                    "progress": 10
                })
            
            # 1. 상호명으로 PLACE ID 검색 (블로킹 방지)
            html = await loop.run_in_executor(None, place_fetcher, store_name, False)
            
            # 상태 업데이트
            if member_id:
                await self.pubsub_gateway.publish_to_channel(channel, {
                    "status": "processing",
                    "message": "장소 ID 추출 중...",
                    "progress": 30
                })
            
            # 2. Place ID 추출 (html이 필요하므로 순차실행)
            place_id = await loop.run_in_executor(None, place_parser, html)
            
            if not place_id:
                raise HTTPException(status_code=404, detail="장소를 찾을 수 없습니다.")
            
            # 상태 업데이트
            if member_id:
                await self.pubsub_gateway.publish_to_channel(channel, {
                    "status": "processing", 
                    "message": "리뷰 수집 중...",
                    "progress": 50
                })
            
            # 3. 리뷰 검색 (place_id가 필요하므로 순차실행)
            more_reviews = 5
            reviews_html = await loop.run_in_executor(None, reviews_fetch, place_id, more_reviews)
            
            # 상태 업데이트
            if member_id:
                await self.pubsub_gateway.publish_to_channel(channel, {
                    "status": "processing",
                    "message": "리뷰 분석 중...",
                    "progress": 70
                })
            
            # 4. 리뷰 파싱 (reviews_html이 필요하므로 순차실행)
            reviews = await loop.run_in_executor(None, reviews_parser, reviews_html)
            
            if not reviews:
                raise HTTPException(status_code=404, detail="리뷰를 찾을 수 없습니다.")
            
            logger.info(f"수집된 리뷰 수: {len(reviews)}")
            
            # TODO: 5. 리뷰 분석 (함수 구현)
            analysis_data = await loop.run_in_executor(None, self._analyze_reviews, reviews)
            
            # 상태 업데이트
            if member_id:
                await self.pubsub_gateway.publish_to_channel(channel, {
                    "status": "processing",
                    "message": "결과 저장 중...",
                    "progress": 90
                })
            
            # TODO: 6. DB 저장 (업데이트 값)
            await self._save_report_to_db(report_id, place_id, analysis_data)
            
            # 7. 완료 알림
            if member_id:
                await self.pubsub_gateway.publish_to_channel(channel, {
                    "status": "completed",
                    "message": "분석 완료!",
                    "progress": 100,
                    "data": analysis_data
                })
                
            return analysis_data
                
        except Exception as e:
            logger.error(f"리뷰 분석 실패: {e}")
            await self._update_report_status(report_id, Status.FAILED)
            if member_id:
                await self.pubsub_gateway.publish_to_channel(channel, {
                    "status": "error",
                    "message": f"분석 실패: {str(e)}",
                    "progress": 0
                })
            raise

    # TODO: 5. 리뷰 분석
    def _analyze_reviews(self, reviews):
        """동기 함수 - 리뷰 분석"""
        total_review_count = len(reviews)
        average_rating = sum(review.get('rating', 0) for review in reviews) / total_review_count if total_review_count > 0 else 0
        
        # 키워드 분석
        popular_keywords = {}
        for review in reviews:
            content = review.get('content', '')
            # 키워드 분석 로직 추가
        
        analytics_result = {
            'reviews': reviews,
            'summary': {
                'total_count': total_review_count,
                'average_rating': average_rating
            },
            'keywords': popular_keywords
        }
        
        return analytics_result

    async def _save_report_to_db(self, report_id: int, place_id: str, analysis_data: dict):
        """DB 저장을 별도 스레드에서 실행"""
        loop = asyncio.get_event_loop()
        
        def save_to_db():
            db: Session = DatabaseSession()
            try:
                report = db.query(Report).filter(Report.report_id == report_id).first()
                if not report:
                    raise HTTPException(status_code=404, detail="리포트를 찾을 수 없습니다.")
                
                # Store 정보 업데이트
                store = report.store
                if place_id:
                    store.place_id = place_id
                    
                # TODO:Report 정보 업데이트
                report.average_review_rate = analysis_data['summary']['average_rating']
                report.popular_keywords = analysis_data['keywords']
                report.analytics_result = analysis_data
                report.total_review_count = analysis_data['summary']['total_count']
                report.status = Status.COMPLETED
                report.created_at = datetime.now()
                
                db.commit()
                
            except Exception as e:
                db.rollback()
                logger.error(f"리포트 업데이트 실패: {e}")
                raise HTTPException(status_code=500, detail="리포트 업데이트에 실패했습니다.")
            finally:
                db.close()
        
        await loop.run_in_executor(None, save_to_db)
    
    async def _update_report_status(self, report_id, status: Status):
        """DB 저장을 별도 스레드에서 실행"""
        loop = asyncio.get_event_loop()
        
        def save_to_db():
            db: Session = DatabaseSession()
            try:
                report = db.query(Report).filter(Report.report_id == report_id).first()
                if not report:
                    raise HTTPException(status_code=404, detail="리포트를 찾을 수 없습니다.")
                report.status = status
                
                db.commit()
                
            except Exception as e:
                db.rollback()
                logger.error(f"리포트 업데이트 실패: {e}")
                raise HTTPException(status_code=500, detail="리포트 업데이트에 실패했습니다.")
            finally:
                db.close()
        
        await loop.run_in_executor(None, save_to_db)
        
    async def get_report(self, report_id: int) -> Optional[Report]:
        """
        완성된 리포트를 받아오기 위해 사용
        """    
        db: Session = DatabaseSession()
        try:
            report = db.query(Report).filter(Report.report_id == report_id).first()
            return report
        except Exception as e:
            logger.error(f"리포트 조회 실패: {e}")
            raise HTTPException(status_code=500, detail="리포트 조회에 실패했습니다.")
        finally:
            db.close()
    
    async def get_user_reports(self, user_id: int) -> List[Report]:
        """
        유저의 리포트를 받아오기 위해 사용
        """
        db: Session = DatabaseSession()
        try:
            reports = db.query(Report).filter(Report.request_member_id == user_id).all()
            return reports
        except Exception as e:
            logger.error(f"유저 리포트 목록 조회 실패: {e}")
            raise HTTPException(status_code=500, detail="유저 리포트 목록 조회에 실패했습니다.")
        finally:
            db.close()    