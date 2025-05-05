import logging
from fastapi import HTTPException
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_oauth import get_credentials

logger = logging.getLogger(__name__)

def get_calendar_service():
    """Get authenticated Google Calendar service"""
    try:
        credentials = get_credentials()
        if not credentials:
            logger.warning("No credentials available for Google Calendar")
            raise HTTPException(status_code=401, detail="Not authorized")
        
        return build("calendar", "v3", credentials=credentials)
    except Exception as e:
        logger.error(f"Error creating Google Calendar service: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to connect to Google Calendar")

def list_calendar_events(max_results=10, time_min=None):
    """List events from primary calendar"""
    try:
        service = get_calendar_service()

        params = {
            "calendarId": "primary", 
            "maxResults": max_results, 
            "singleEvents": True, 
            "orderBy": "startTime"
        }
        
        if time_min:
            params["timeMin"] = time_min
            
        result = service.events().list(**params).execute()
        return result.get("items", [])
    except HttpError as error:
        logger.error(f"Google Calendar API error: {str(error)}")

        if error.resp.status == 404:
            raise HTTPException(status_code=404, detail="Calendar not found")
        elif error.resp.status == 403:
            raise HTTPException(status_code=403, detail="Permission denied to access calendar")
        else:
            raise HTTPException(status_code=error.resp.status, detail=str(error))
    except Exception as e:
        logger.error(f"Unexpected error in list_calendar_events: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

async def create_calendar_event(event_data):
    """Create a new event in primary calendar"""
    if not event_data.get("summary"):
        raise HTTPException(status_code=400, detail="Event summary is required")
    if not event_data.get("start", {}).get("dateTime"):
        raise HTTPException(status_code=400, detail="Event start time is required")
    if not event_data.get("end", {}).get("dateTime"):
        raise HTTPException(status_code=400, detail="Event end time is required")
        
    try:
        service = get_calendar_service()
        return service.events().insert(calendarId="primary", body=event_data).execute()
    except HttpError as error:
        logger.error(f"Google Calendar API error in create_event: {str(error)}")
        
        if "Invalid time format" in str(error):
            raise HTTPException(status_code=400, detail="Invalid date/time format")
        elif error.resp.status == 403:
            raise HTTPException(status_code=403, detail="Permission denied to create event")
        else:
            raise HTTPException(status_code=error.resp.status or 400, detail=str(error))
    except Exception as e:
        logger.error(f"Unexpected error in create_calendar_event: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

def delete_calendar_event(event_id):
    """Delete an event by ID"""
    if not event_id:
        raise HTTPException(status_code=400, detail="Event ID is required")
        
    try:
        service = get_calendar_service()
        service.events().delete(calendarId="primary", eventId=event_id).execute()
        return {"status": "success", "message": f"Event {event_id} deleted"}
    except HttpError as error:
        logger.error(f"Google Calendar API error in delete_event: {str(error)}")
        
        if error.resp.status == 404:
            raise HTTPException(status_code=404, detail=f"Event with ID '{event_id}' not found")
        elif error.resp.status == 403:
            raise HTTPException(status_code=403, detail="Permission denied to delete event")
        else:
            raise HTTPException(status_code=error.resp.status or 400, detail=str(error))
    except Exception as e:
        logger.error(f"Unexpected error in delete_calendar_event: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")