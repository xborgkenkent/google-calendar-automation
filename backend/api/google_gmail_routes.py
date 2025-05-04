from fastapi import APIRouter, Depends, HTTPException
from services.google_gmail_services import (
    list_messages,
    get_message
)

router = APIRouter(tags=["mail"])

@router.get("/messages", summary="List Gmail Messages")
def list_gmail_messages(
    user_id: str = 'me',
    max_results: int = 1
):
    """List messages from the user's Gmail account"""
    try:
        messages = list_messages(user_id=user_id, max_results=max_results)
        email_list = []
        for message in messages:
            full_msg = get_message(user_id=user_id, msg_id=message['id'])
            email_list.append(full_msg)
        return email_list
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list messages: {str(e)}")