from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import google_oauth
from app.api.google_routes import router as google_router

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
