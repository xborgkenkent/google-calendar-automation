import os
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  # Must be set before imports

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from google_auth_oauthlib.flow import Flow
from typing import Optional
import uuid
from pathlib import Path
from google.oauth2.credentials import Credentials

router = APIRouter()

creds_store = {}
flow_store = {}


current_dir = Path(__file__).parent
CLIENT_SECRETS_FILE = current_dir / "credentials.json"
SCOPES = [
    'https://www.googleapis.com/auth/calendar.readonly',
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/tasks'
]
REDIRECT_URI = "http://127.0.0.1:8000/api/google/callback/"

@router.get("/api/google/init")
def authorize():
    """Initialize the OAuth flow and redirect user to Google's consent page"""
    try:
        flow = Flow.from_client_secrets_file(
            CLIENT_SECRETS_FILE,
            scopes=SCOPES,
            redirect_uri=REDIRECT_URI
        )

        state = str(uuid.uuid4())
        authorization_url, _ = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            state=state,
            prompt='consent'
        )
        
        flow_store[state] = flow
        
        return RedirectResponse(authorization_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Authorization initialization failed: {str(e)}")

@router.get("/api/google/callback/")
async def oauth2callback(request: Request):
    """Handle the OAuth callback from Google"""
    try:
        state = request.query_params.get("state")
        
        if not state or state not in flow_store:
            raise HTTPException(status_code=400, detail="Invalid state parameter")
            
        flow = flow_store[state]
        
        full_url = str(request.url)
        
        flow.fetch_token(authorization_response=full_url)
        credentials = flow.credentials
        
        creds_store["credentials"] = {
            "token": credentials.token,
            "refresh_token": credentials.refresh_token,
            "token_uri": credentials.token_uri,
            "client_id": credentials.client_id,
            "client_secret": credentials.client_secret,
            "scopes": credentials.scopes
        }
        del flow_store[state]
        
        return HTMLResponse("""
            <h1>Authorization successful</h1>
        """.format(credentials.token[:20]))
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return HTMLResponse(f"""
            <h1>Authorization failed</h1>
            <p>Error: {str(e)}</p>
        """, status_code=500)

def get_credentials():
    """Helper function to retrieve stored credentials and return as Credentials object"""
    stored = creds_store.get("credentials")
    if not stored:
        return None
    
    return Credentials(
        token=stored["token"],
        refresh_token=stored["refresh_token"],
        token_uri=stored["token_uri"],
        client_id=stored["client_id"],
        client_secret=stored["client_secret"],
        scopes=stored["scopes"]
    )

@router.get("/api/google/auth-status")
def auth_status():
    """Check if user is authenticated with Google"""
    creds = get_credentials()
    if creds:
        return {"authenticated": True, "token": creds["token"][:10] + "..."}
    return {"authenticated": False}