from fastapi import APIRouter, HTTPException, Query
import asyncio

from app.services.reviews_service import reviews_fetch, reviews_parser
from app.schemas.review import ReviewsResponse

router = APIRouter()


@router.get(
    "/reviews",
    summary="네이버플레이스 리뷰 크롤링",
    response_model=ReviewsResponse,
)
async def get_reviews(
        place_id: str = Query(..., description="네이버플레이스 ID (예: 1997987484)"),
        more_reviews: int = Query(5, ge=1, le=100, description="리뷰 '더보기' 클릭 횟수"),
        print_all: bool = Query(False, description="디버그용 출력 불리언. True 시 전체 리뷰 HTML 출력")
        # sort: str = Query("recent", description="정렬 기준 (예: recent 또는 popular)")
):
    html = await asyncio.get_event_loop().run_in_executor(
        None, reviews_fetch, place_id, more_reviews
    )

    # 디버그용. True 시 리뷰 태그 전체 출력
    if print_all:
        start = html.find('<li class="place_apply_pui')
        end = html.find("</li>", start) + len("</li>")
        snippet = html[start:end] if start != -1 and end != -1 else html[:200000]
        return {"place_id": place_id, "review_count": 0, "reviews": [], "html_snippet": snippet}

    reviews = reviews_parser(html)
    if not reviews:
        raise HTTPException(status_code=404, detail="리뷰를 찾을 수 없습니다.")

    return ReviewsResponse(
        place_id=place_id,
        review_count=len(reviews),
        reviews=reviews
    )
