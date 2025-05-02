import re
import json
import os
from dotenv import load_dotenv
from openai import OpenAI
import httpx

load_dotenv()

# Initialize OpenAI client
apikey = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=apikey)

# Constants
DEFAULT_TIMEZONE = "Asia/Manila"

async def generate_event_from_text(text: str) -> dict:
    """Generate event details from text input using OpenAI API"""
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
            {"role": "user", "content": text},
        ],
    )
    
    content = response.choices[0].message.content

    # Extract JSON from the response
    match = re.search(r"```json\s*({[\s\S]*?})\s*```", content)
    if not match:
        match = re.search(r"({[\s\S]*?})", content)
    
    if not match:
        raise ValueError("JSON object not found in response.")

    return json.loads(match.group(1))

def transform_to_calendar_format(raw_data: dict) -> dict:
    """Transform the raw event data into Google Calendar format"""
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