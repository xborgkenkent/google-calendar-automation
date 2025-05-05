
import re
import json
from fastapi import APIRouter, HTTPException, Body
from dotenv import load_dotenv
import os
from openai import OpenAI
from services.google_services import create_calendar_event
from models.openai_models import EventRequest
from services.openai_services import generate_event_from_text
load_dotenv()

router = APIRouter()
api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

@router.post("/generates")
async def generate_event(event: EventRequest = Body(...)):
    """Get event summary"""
    try:
        transformed = await generate_event_from_text(event.val)
        create_calendar_event(transformed)
        return transformed

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))