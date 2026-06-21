from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from app.routes import router

app = FastAPI(
    title="AI Chatbot Backend",
    version="1.0"
)

app.include_router(router)

# Mount the static directory for the professional UI
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    return RedirectResponse(url="/static/index.html")