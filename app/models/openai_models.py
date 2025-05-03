from pydantic import BaseModel

class EventRequest(BaseModel):
    val: str
    
class EventResponse(BaseModel):
    id: str
    summary: str
    description: str
    start: str
    end: str
    location: str