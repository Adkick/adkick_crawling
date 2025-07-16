from typing import List
from pydantic import BaseModel

class Review(BaseModel):
    nickname: str
    content: str
    date: str
    revisit: str

class ReviewsResponse(BaseModel):
    place_id: str
    review_count: int
    reviews: List[Review]
