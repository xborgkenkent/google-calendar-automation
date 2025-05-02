
import re
import json
from fastapi import APIRouter, HTTPException, Body
from dotenv import load_dotenv
import os
from openai import OpenAI
from app.services.google_services import create_calendar_event
from app.models.openai_models import EventRequest

load_dotenv()

router = APIRouter()
apikey = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=apikey)

DEFAULT_TIMEZONE = "Asia/Manila"

def transform_to_calendar_format(raw_data: dict) -> dict:
    return {
        "summary": raw_data.get("summary", ""),
        "start": {
            "dateTime": raw_data.get("start", ""),
            "timeZone": DEFAULT_TIMEZONE
        },
        "end": {
            "dateTime": raw_data.get("end", ""),
            "timeZone": DEFAULT_TIMEZONE
        },
        "description": raw_data.get("description", ""),
        "location": raw_data.get("location", "")
    }
    
@router.post("/generates")
async def generate_event(event: EventRequest = Body(...)):
    """Get event summary"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "assistant",
                    "content": (
                        "You are a google calendar assistant. JSON output should be: "
                        "{\"summary\": \"the event title\"}, "
                        "{\"description\": \"the event description\"}, "
                        "{\"start\": \"the start time\" //ex: 2025-05-02T21:00:00+08:00 }, "
                        "{\"end\": \"the end time\" //ex: 2025-05-02T23:00:00+08:00}, "
                        "{\"location\": \"the event location\"}"
                    )
                },
                {"role": "user", "content": event.val},
            ],
        )
        content = response.choices[0].message.content

        match = re.search(r"```json\s*({[\s\S]*?})\s*```", content)
        if not match:
            match = re.search(r"({[\s\S]*?})", content)
        
        if not match:
            raise ValueError("JSON object not found in response.")

        extracted_json = json.loads(match.group(1))
        transformed = transform_to_calendar_format(extracted_json)
        create_calendar_event(transformed)
        return transformed

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))