from fastapi import APIRouter, Body
from app.models.google_models import EventCreate, EventUpdate
from app.services.google_services import (
    list_calendar_events,
    create_calendar_event,
    get_calendar_event,
    update_calendar_event,
    delete_calendar_event
)

router = APIRouter()

@router.get("/events")
def list_events():
    return list_calendar_events()

@router.post("/events")
def create_event(event: EventCreate = Body(...)):
    return create_calendar_event(event.dict())

@router.get("/events/{event_id}")
def get_event(event_id: str):
    return get_calendar_event(event_id)

@router.put("/events/{event_id}")
def update_event(event_id: str, event: EventUpdate = Body(...)):
    return update_calendar_event(event_id, event.dict(exclude_unset=True))

@router.patch("/events/{event_id}")
def partial_update_event(event_id: str, event: EventUpdate = Body(...)):
    return update_calendar_event(event_id, event.dict(exclude_unset=True))

@router.delete("/events/{event_id}")
def delete_event(event_id: str):
    return delete_calendar_event(event_id)