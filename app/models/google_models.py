from pydantic import BaseModel
from typing import Optional

class EventCreate(BaseModel):
    summary: str
    start: dict
    end: dict
    description: Optional[str] = None
    location: Optional[str] = None

class EventUpdate(BaseModel):
    summary: Optional[str] = None
    start: Optional[dict] = None
    end: Optional[dict] = None
    description: Optional[str] = None
    location: Optional[str] = None
