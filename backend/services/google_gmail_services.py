import base64
import re
from bs4 import BeautifulSoup
from fastapi import HTTPException
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_oauth import get_credentials

def get_gmail_service():
    """Get authenticated Google Gmail service"""
    try:
        credentials = get_credentials()
        if not credentials:
            raise HTTPException(status_code=401, detail="Not authorized")
        
        return build("gmail", "v1", credentials=credentials)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to connect to Google Gmail")

def list_messages(user_id='me', max_results=10):
    try:
        service = get_gmail_service()
        results = service.users().messages().list(userId=user_id, maxResults=max_results).execute()
        messages = results.get('messages', [])
        return messages
    except HttpError as error:
        if error.resp.status == 404:
            raise HTTPException(status_code=404, detail="Messages not found")
        elif error.resp.status == 403:
            raise HTTPException(status_code=403, detail="Permission denied to access messages")
        else:
            raise HTTPException(status_code=error.resp.status, detail=str(error))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
    
def get_message(user_id='me', msg_id = None):
    try:
        service = get_gmail_service()
        message = service.users().messages().get(userId=user_id, id=msg_id, format='full').execute()
        payload = message['payload']
        parts = payload.get('parts', [payload])
        body = ""

        for part in parts:
            mime_type = part.get("mimeType", "")
            data = part.get("body", {}).get("data")

            if data:
                decoded = base64.urlsafe_b64decode(data.encode("UTF-8")).decode("utf-8")
                if mime_type == "text/html":
                    body = decoded
                    break
                elif mime_type == "text/plain" and not body:
                    body = decoded

        # Extract links from the HTML/text content
        links = []
        if body:
            soup = BeautifulSoup(body, "html.parser")
            links = [a['href'] for a in soup.find_all('a', href=True)]

        return {
            'snippet': message.get('snippet', ''),
            'links': links
        }
    except HttpError as error:
        if error.resp.status == 404:
            raise HTTPException(status_code=404, detail="Message not found")
        elif error.resp.status == 403:
            raise HTTPException(status_code=403, detail="Permission denied to access message")
        else:
            raise HTTPException(status_code=error.resp.status, detail=str(error))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")