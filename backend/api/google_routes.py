from fastapi import APIRouter, Body, Path, Query, HTTPException
from typing import List, Optional
from datetime import datetime
from models.google_models import EventRequest, EventResponse
from services.google_services import (
    list_calendar_events,
    create_calendar_event,
    delete_calendar_event
)

router = APIRouter(tags=["calendar"])

@router.get("/events", response_model=List[EventResponse], summary="List Calendar Events")
def list_events(
    max_results: int = Query(10, ge=1, le=100, description="Maximum number of events to return"),
    start_time: Optional[datetime] = Query(None, description="Minimum start time for events (ISO format)")
):
    """List events from the primary Google Calendar"""
    
    time_min = start_time.isoformat() + "Z" if start_time else None
    
    return list_calendar_events(
        max_results=max_results,
        time_min=time_min
    )

@router.post("/events", response_model=EventResponse, status_code=201, summary="Create Calendar Event")
def create_event(event: EventRequest = Body(...)):
    """Create a new event in the primary Google Calendar"""
    try:
        return create_calendar_event(event.dict(exclude_unset=True))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create event: {str(e)}")

@router.delete("/events/{event_id}", summary="Delete Calendar Event")
def delete_event(
    event_id: str = Path(..., description="The ID of the event to delete", min_length=5)
):
    """Delete an event from the primary Google Calendar by ID"""
    return delete_calendar_event(event_id)