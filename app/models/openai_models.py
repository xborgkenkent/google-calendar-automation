from pydantic import BaseModel

class EventRequest(BaseModel):
    val: str