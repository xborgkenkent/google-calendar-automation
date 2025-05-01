from fastapi import APIRouter, HTTPException, Body
from googleapiclient.errors import HttpError
from app.models.google_models import EventCreate, EventUpdate
from app.services.google_services import get_calendar_service, get_tasks_service

router = APIRouter()


@router.get("/events")
def list_events():
    try:
        service = get_calendar_service()
        result = service.events().list(calendarId="primary", maxResults=10, singleEvents=True, orderBy="startTime").execute()
        events = result.get("items", [])
        
        # filtered_events = []
        # for event in events:
        #     filtered_event = {
        #         "id": event.get("id"),
        #         "summary": event.get("summary"),
        #         "start": event.get("start", {}).get("dateTime", event.get("start", {}).get("date")),
        #         "end": event.get("end", {}).get("dateTime", event.get("end", {}).get("date")),
        #         "description": event.get("description"),
        #         "location": event.get("location")
        #     }
        #     filtered_events.append(filtered_event)
            
        # return filtered_events
        return events
    except HttpError as error:
        raise HTTPException(status_code=400, detail=str(error))

@router.post("/events")
def create_event(event: EventCreate = Body(...)):
    try:
        service = get_calendar_service()
        return service.events().insert(calendarId="primary", body=event.dict()).execute()
    except HttpError as error:
        raise HTTPException(status_code=400, detail=str(error))

@router.put("/events/{event_id}")
def update_event(event_id: str, event: EventUpdate = Body(...)):
    try:
        service = get_calendar_service()
        existing_event = service.events().get(calendarId="primary", eventId=event_id).execute()
        for key, value in event.dict(exclude_unset=True).items():
            existing_event[key] = value
        return service.events().update(calendarId="primary", eventId=event_id, body=existing_event).execute()
    except HttpError as error:
        raise HTTPException(status_code=400, detail=str(error))

@router.patch("/events/{event_id}")
def partial_update_event(event_id: str, event: EventUpdate = Body(...)):
    return update_event(event_id, event)

@router.delete("/events/{event_id}")
def delete_event(event_id: str):
    try:
        service = get_calendar_service()
        service.events().delete(calendarId="primary", eventId=event_id).execute()
        return {"status": "success", "message": f"Event {event_id} deleted"}
    except HttpError as error:
        raise HTTPException(status_code=400, detail=str(error))

@router.get("/events/{event_id}")
def get_event(event_id: str):
    try:
        service = get_calendar_service()
        event = service.events().get(calendarId="primary", eventId=event_id).execute()
        filtered_event = {
                "id": event.get("id"),
                "summary": event.get("summary"),
                "start": event.get("start", {}).get("dateTime", event.get("start", {}).get("date")),
                "end": event.get("end", {}).get("dateTime", event.get("end", {}).get("date")),
                "description": event.get("description"),
                "location": event.get("location")
            }
        return filtered_event
    except HttpError as error:
        raise HTTPException(status_code=400, detail=str(error))
