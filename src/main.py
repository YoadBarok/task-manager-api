from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from os import environ
from fastapi.middleware.cors import CORSMiddleware
from src.app.api.api import api_router


app = FastAPI()

UI_URL = environ.get("UI_URL")

origins = [
    UI_URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_router, prefix="/api")


@app.get('/')
async def home():
    return "Go to /docs to see the documentation."
