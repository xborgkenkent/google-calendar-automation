from fastapi import APIRouter, HTTPException, Body
from models.openai_models import EventRequest, EventResponse
from services.openai_services import generate_event_from_text, transform_to_calendar_format
from services.google_services import create_calendar_event

router = APIRouter(tags=["ai"])

@router.post("/events/generate", response_model=EventResponse)
async def generate_and_create_event(request: EventRequest = Body(...)):
    """Generate event details from natural language and create in Google Calendar"""
    try:
        raw_event_data = await generate_event_from_text(request.val)
        calendar_event_data = transform_to_calendar_format(raw_event_data)
        created_event = create_calendar_event(calendar_event_data)
        
        return EventResponse(
            id=created_event.get("id", ""),
            summary=created_event.get("summary", ""),
            description=created_event.get("description", ""),
            start=created_event.get("start", {}).get("dateTime", ""),
            end=created_event.get("end", {}).get("dateTime", ""),
            location=created_event.get("location", "")
        )
        
    except HTTPException as e:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create event: {str(e)}")