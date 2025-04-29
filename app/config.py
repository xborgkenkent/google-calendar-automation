import os

CLIENT_SECRETS_FILE = os.path.join(os.path.dirname(__file__), "credentials.json")

SCOPES = [
    'https://www.googleapis.com/auth/calendar.readonly',
    'https://www.googleapis.com/auth/calendar'
]

REDIRECT_URI = "http://127.0.0.1:8000/api/google/callback/"