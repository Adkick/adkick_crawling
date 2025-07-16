from pydantic import BaseModel, HttpUrl, field_validator
from typing import Optional, List

class PlaceIdResponse(BaseModel):
    query: str
    place_id: Optional[str] = None
    html_snippet: Optional[str] = None