from fastapi import APIRouter, HTTPException
from app.schemas import ChatRequest, ChatResponse
from app.llm_service import get_ai_reply

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