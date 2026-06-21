from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.schemas import ChatRequest, ChatResponse
from app.llm_service import get_ai_reply, get_ai_reply_stream

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    prompt = request.prompt.strip()

    if prompt == "":
        raise HTTPException(
            status_code=400,
            detail="Prompt cannot be empty"
        )

    try:
        reply = get_ai_reply(prompt)

        return {"reply": reply}

    except Exception as e:
        print(f"Chat error: {e}")
        raise HTTPException(
            status_code=500,
            detail="AI API failure"
        )

@router.post("/chat/stream")
def chat_stream(request: ChatRequest):
    prompt = request.prompt.strip()
    if prompt == "":
        raise HTTPException(
            status_code=400,
            detail="Prompt cannot be empty"
        )
    
    return StreamingResponse(get_ai_reply_stream(prompt), media_type="text/event-stream")