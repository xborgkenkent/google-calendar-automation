from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import google_oauth
from api.google_routes import router as google_router
from api.openai_routes import router as openai_router
from api.google_gmail_routes import router as google_gmail_router

app = FastAPI()

origins = [
    "http://127.0.0.1",
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(google_oauth.router, prefix="/api/google", tags=["Google OAuth"])
app.include_router(google_router, prefix="/api/google", tags=["Google API"])
app.include_router(google_gmail_router, prefix="/api/google", tags=["Gmail"])
app.include_router(openai_router, prefix="/api/openai", tags=["OpenAI"])
