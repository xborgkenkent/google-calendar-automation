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
