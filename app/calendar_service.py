from fastapi import APIRouter, HTTPException, Body
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from app.google_oauth import get_credentials
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

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

def get_calendar_service():
    credentials = get_credentials()
    if not credentials:
        raise HTTPException(status_code=401, detail="Not authorized")
    return build("calendar", "v3", credentials=credentials)

@router.get("/events")
def list_events():
    """List all events from primary calendar"""
    try:
        service = get_calendar_service()
        result = service.events().list(
            calendarId="primary",
            maxResults=10,
            singleEvents=True,
            orderBy="startTime"
        ).execute()
        return result.get("items", [])
    except HttpError as error:
        raise HTTPException(status_code=400, detail=f"An error occurred: {error}")

def get_tasks_service():
    credentials = get_credentials()
    if not credentials:
        raise HTTPException(status_code=401, detail="Not authorized")
    return build("tasks", "v1", credentials=credentials)

@router.get("/tasks")
def list_tasks(tasklist: str = "@default"):
    """Get tasks from the specified task list"""
    try:
        service = get_tasks_service()
        tasks = service.tasks().list(
            tasklist=tasklist,
            showCompleted=False,
            showHidden=False
        ).execute()
        return tasks.get('items', [])
    except HttpError as error:
        raise HTTPException(status_code=400, detail=f"An error occurred: {error}")

@router.get("/tasklists")
def list_tasklists():
    """Get all task lists"""
    try:
        service = get_tasks_service()
        tasklists = service.tasklists().list().execute()
        return tasklists.get('items', [])
    except HttpError as error:
        raise HTTPException(status_code=400, detail=f"An error occurred: {error}")
    
@router.post("/events")
def create_event(event: EventCreate = Body(...)):
    """Create a new event"""
    try:
        service = get_calendar_service()
        created_event = service.events().insert(
            calendarId="primary",
            body=event.dict()
        ).execute()
        return created_event
    except HttpError as error:
        raise HTTPException(status_code=400, detail=f"An error occurred: {error}")

@router.put("/events/{event_id}")
def update_event(event_id: str, event: EventUpdate = Body(...)):
    """Update an existing event"""
    try:
        service = get_calendar_service()
        
        existing_event = service.events().get(
            calendarId="primary",
            eventId=event_id
        ).execute()
        
        update_data = event.dict(exclude_unset=True)
        for key, value in update_data.items():
            existing_event[key] = value
        
        updated_event = service.events().update(
            calendarId="primary",
            eventId=event_id,
            body=existing_event
        ).execute()
        
        return updated_event
    except HttpError as error:
        raise HTTPException(status_code=400, detail=f"An error occurred: {error}")

@router.patch("/events/{event_id}")
def partial_update_event(event_id: str, event: EventUpdate = Body(...)):
    """Partially update an event (same as PUT in this implementation)"""
    return update_event(event_id, event)

@router.delete("/events/{event_id}")
def delete_event(event_id: str):
    """Delete an event"""
    try:
        service = get_calendar_service()
        service.events().delete(
            calendarId="primary",
            eventId=event_id
        ).execute()
        return {"status": "success", "message": f"Event {event_id} deleted"}
    except HttpError as error:
        raise HTTPException(status_code=400, detail=f"An error occurred: {error}")

@router.get("/events/{event_id}")
def get_event(event_id: str):
    """Get a specific event by ID"""
    try:
        service = get_calendar_service()
        event = service.events().get(
            calendarId="primary",
            eventId=event_id
        ).execute()
        return event
    except HttpError as error:
        raise HTTPException(status_code=400, detail=f"An error occurred: {error}")