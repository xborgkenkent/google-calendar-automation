from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import google_oauth, calendar_service

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

app.include_router(google_oauth.router)
app.include_router(calendar_service.router)