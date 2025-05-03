from pydantic import BaseModel
from typing import Optional

class EventRequest(BaseModel):
    summary: str
    start: dict
    end: dict
    description: Optional[str] = None
    location: Optional[str] = None

class EventResponse(BaseModel):
    id: str
    summary: str
    description: Optional[str] = None
    start: dict
    end: dict
    location: Optional[str] = None
