import google.generativeai as genai
from app.config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel('gemini-2.5-flash')

def get_ai_reply(prompt:str):
    try:
        response = model.generate_content(prompt)
        
        reply = response.text

        if not reply:
            raise ValueError("Empty response from AI")

        return reply

    except Exception as e:
        raise Exception(f"Gemini API Error: {str(e)}")

def get_ai_reply_stream(prompt:str):
    try:
        response = model.generate_content(prompt, stream=True)
        
        for chunk in response:
            if chunk.text:
                yield chunk.text

    except Exception as e:
        raise Exception(f"Gemini API Streaming Error: {str(e)}")