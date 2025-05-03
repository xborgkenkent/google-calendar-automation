import re
import json
import os
import logging
from typing import Dict, Any, Optional
from fastapi import HTTPException
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

load_dotenv()
logger = logging.getLogger(__name__)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    logger.critical("OPENAI_API_KEY environment variable is not set")
    raise RuntimeError("OPENAI_API_KEY environment variable is not set")

client = OpenAI(api_key=OPENAI_API_KEY)

DEFAULT_TIMEZONE = "Asia/Manila"

async def generate_event_from_text(text: str) -> Dict[str, Any]:
    """Generate event details from text input using OpenAI API"""
    if not text or len(text.strip()) < 3:
        raise HTTPException(status_code=400, detail="Text input is too short")
        
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a google calendar assistant. Extract event details from user input "
                        "and format as valid JSON with these fields: summary (title), description, "
                        "start (ISO datetime with timezone), end (ISO datetime with timezone), "
                        "and location."
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
            logger.warning(f"Could not extract JSON from OpenAI response: {content}")
            raise ValueError("JSON object not found in response.")

        event_data = json.loads(match.group(1))
        
        # Validate required fields
        if not event_data.get("summary"):
            raise ValueError("Event summary/title is required")
        if not event_data.get("start"):
            raise ValueError("Event start time is required")
        if not event_data.get("end"):
            raise ValueError("Event end time is required")
            
        return event_data
        
    except OpenAIError as e:
        logger.error(f"OpenAI API error: {str(e)}")
        raise HTTPException(status_code=502, detail=f"OpenAI API error: {str(e)}")
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON in OpenAI response: {content}")
        raise HTTPException(status_code=500, detail="Failed to parse event data")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error generating event: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

def transform_to_calendar_format(raw_data: Dict[str, Any]) -> Dict[str, Any]:
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