from fastapi import FastAPI
from app.routes import router

app = FastAPI(
    title="AI Chatbot Backend",
    version="1.0"
)

app.include_router(router)