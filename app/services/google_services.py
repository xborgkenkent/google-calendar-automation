from fastapi import HTTPException
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from app.google_oauth import get_credentials

def get_calendar_service():
    credentials = get_credentials()
    if not credentials:
        raise HTTPException(status_code=401, detail="Not authorized")
    return build("calendar", "v3", credentials=credentials)

def get_tasks_service():
    credentials = get_credentials()
    if not credentials:
        raise HTTPException(status_code=401, detail="Not authorized")
    return build("tasks", "v1", credentials=credentials)

# Calendar event functions
def list_calendar_events(max_results=10):
    """List events from primary calendar"""
    try:
        service = get_calendar_service()
        result = service.events().list(
            calendarId="primary", 
            maxResults=max_results, 
            singleEvents=True, 
            orderBy="startTime"
        ).execute()
        return result.get("items", [])
    except HttpError as error:
        raise HTTPException(status_code=400, detail=str(error))

def create_calendar_event(event_data):
    """Create a new event in primary calendar"""
    try:
        service = get_calendar_service()
        print(event_data)
        return service.events().insert(calendarId="primary", body=event_data).execute()
    except HttpError as error:
        raise HTTPException(status_code=400, detail=str(error))

def get_calendar_event(event_id):
    """Get a specific event by ID"""
    try:
        service = get_calendar_service()
        return service.events().get(calendarId="primary", eventId=event_id).execute()
    except HttpError as error:
        raise HTTPException(status_code=400, detail=str(error))

def update_calendar_event(event_id, event_data):
    """Update an existing event by ID"""
    try:
        service = get_calendar_service()
        existing_event = get_calendar_event(event_id)
        for key, value in event_data.items():
            existing_event[key] = value
        return service.events().update(
            calendarId="primary", 
            eventId=event_id, 
            body=existing_event
        ).execute()
    except HttpError as error:
        raise HTTPException(status_code=400, detail=str(error))

def delete_calendar_event(event_id):
    """Delete an event by ID"""
    try:
        service = get_calendar_service()
        service.events().delete(calendarId="primary", eventId=event_id).execute()
        return {"status": "success", "message": f"Event {event_id} deleted"}
    except HttpError as error:
        raise HTTPException(status_code=400, detail=str(error))