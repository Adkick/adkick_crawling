from pydantic import BaseModel, HttpUrl, field_validator
from typing import Optional, List

class Store(BaseModel):
    title: str
    link: Optional[HttpUrl]
    category: str
    description: Optional[str] = None
    telephone: Optional[str] = None
    address: str
    roadAddress: str
    mapx: int
    mapy: int

    @field_validator("link", mode="before")
    @classmethod
    def _empty_link_to_none(cls, v):
        if v == "":
            return None
        return v

class StoreSearchResponse(BaseModel):
    lastBuildDate: str
    total: int
    start: int
    display: int
    items: List[Store]

class SimpleStore(BaseModel):
    title: str
    mapx: int
    mapy: int

class SimpleStoreResponse(BaseModel):
    items: List[SimpleStore]