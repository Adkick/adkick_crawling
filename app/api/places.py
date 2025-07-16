import asyncio

from fastapi import APIRouter, HTTPException, Query
from app.services.place_service import place_fetcher, place_parser
from app.schemas.place import PlaceIdResponse

router = APIRouter()


@router.get(
    "/place_id",
    summary="네이버플레이스 sid 가져오기",
    response_model=PlaceIdResponse,
)
async def get_place_id(
    query:      str  = Query(..., description="상호명 검색 (예: 스타벅스 정자동점)"),
    debug_html: bool = Query(False, description="디버그용: True 시 전체 HTML 스니펫 반환")
):
    html = await asyncio.get_event_loop().run_in_executor(
        None, place_fetcher, query, debug_html
    )

    if debug_html:
        return PlaceIdResponse(query=query, html_snippet=html)

    try:
        sid = place_parser(html)
        return PlaceIdResponse(query=query, place_id=sid)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
