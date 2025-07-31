from datetime import datetime
from enum import Enum
from sqlalchemy.dialects.mysql import ENUM as SQLEnum
from typing import Optional, List
from sqlalchemy import BIGINT, String, Float, Integer, JSON, DateTime, ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
class Status(str, Enum):
    FAILED = "FAILED"
    COMPLETED = "COMPLETED"
    PROGRESS = "PROGRESS"
    
class Store(Base):
    __tablename__ = "store"
    
    store_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, comment="기본키")
    place_id: Mapped[str] = mapped_column(String(100), nullable=True, comment="매장의 플레이스 ID")
    name: Mapped[str] = mapped_column(String(100), nullable=False, comment="매장명")
    address: Mapped[Optional[str]] = mapped_column(String(200), nullable=True, comment="주소")
    category: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="카테고리")
    store_image: Mapped[Optional[str]] = mapped_column(String(500), nullable=True, comment="매장 이미지")
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime, 
        nullable=False, 
        server_default=text("CURRENT_TIMESTAMP"), 
        comment="생성일시"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, 
        nullable=False, 
        server_default=text("CURRENT_TIMESTAMP"), 
        onupdate=text("CURRENT_TIMESTAMP"), 
        comment="수정일시"
    )
    
    # Relationship
    reports: Mapped[List["Report"]] = relationship("Report", back_populates="store")


class Report(Base):
    __tablename__ = "report"
    
    report_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, comment="기본키")
    request_member_id: Mapped[int] = mapped_column(BIGINT, nullable=False, comment="요청 회원 ID")
    store_id: Mapped[int] = mapped_column(
        BIGINT,
        ForeignKey("store.store_id"), 
        nullable=False, 
        comment="매장 ID"
    )
    average_review_rate: Mapped[Optional[float]] = mapped_column(Float, nullable=True, comment="평균 리뷰 점수")
    popular_keywords: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True, comment="키워드 목록")
    analytics_result: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True, comment="분석 결과")
    total_review_count: Mapped[int] = mapped_column(
        Integer, 
        nullable=False, 
        server_default="0", 
        comment="총 리뷰 수"
    )
    status: Mapped[Status] = mapped_column(
        SQLEnum(Status), 
        nullable=False, 
        default=Status.PROGRESS, 
        comment="상태"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, 
        nullable=False, 
        server_default=text("CURRENT_TIMESTAMP"), 
        comment="생성일시"
    )
    
    # Relationship
    store: Mapped["Store"] = relationship("Store", back_populates="reports")