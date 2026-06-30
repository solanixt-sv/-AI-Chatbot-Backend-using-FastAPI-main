AI Chatbot Backend using FastAPI (Google Gemini)
Overview

This project implements a FastAPI backend that allows users to send prompts to an AI model and receive responses.
It integrates with Google's Gemini 2.5 Flash model and demonstrates API design, input validation, and error handling.

Workflow:
User → FastAPI Backend → Gemini LLM → Response → User

Project Structure

app/main.py – FastAPI application entry point

app/schemas.py – Defines input/output validation rules

app/routes.py – Contains the API endpoints

app/llm_service.py – Handles communication with Gemini LLM

app/config.py – Loads environment variables (API key)

.env – Stores Gemini API key securely

requirements.txt – Lists Python dependencies

README.md – Project documentation

API Endpoint

POST /chat – Sends a prompt to the AI and returns the generated response.

Request Rules:

Prompt is required

Cannot be empty

Maximum 300 characters

Response:

Returns the AI-generated reply

LLM Integration

Uses Google Gemini 2.5 Flash model

API key stored securely in .env

Handles API failures, empty responses, and timeouts

Error Handling
Scenario	Status Code
Invalid request body	422
Empty prompt	400
AI API failure or empty response	500
## Running the Application Locally

You can run both the FastAPI backend and Streamlit frontend concurrently in a single command using the provided local runner script:

```bash
python run.py
```

This will automatically:
1. Start the FastAPI backend at `http://127.0.0.1:8000`.
2. Start the Streamlit frontend at `http://localhost:8501`.
3. Link the frontend to the backend service.

### Alternative (Separate Terminals)

If you prefer to run them in separate terminal sessions:

1. **Start the FastAPI Backend**:
   ```bash
   uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
   ```
2. **Start the Streamlit Frontend**:
   ```bash
   streamlit run streamlit_app.py
   ```

---

## Deployment Guide

You can deploy this application to cloud platforms using two different architectures:

### Option A: Single Service Deployment (Recommended & Free Tier Friendly)

Since `streamlit_app.py` features a **self-hosting auto-start backend mechanism**, you can deploy the entire application as a single web service. This is perfect for the free tiers of Render, Hugging Face Spaces, or Streamlit Community Cloud.

1. Create a Web Service on your hosting provider (e.g., Render) pointing to this repository.
2. Select **Python** as the runtime.
3. Set the Build Command:
   ```bash
   pip install -r requirements.txt
   ```
4. Set the Start Command:
   ```bash
   streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0
   ```
5. Add your Environment Variables:
   - `GEMINI_API_KEY`: Your Google Gemini API Key.
   - `API_URL`: Keep this as the default (`http://127.0.0.1:8000/chat`) or leave it blank. The Streamlit server will automatically run the FastAPI backend on localhost port 8000 inside the same container!

### Option B: Multi-Service Blueprint Deployment (Render)

If you prefer separate, dedicated backend and frontend services, we have provided a Render Blueprint configuration (`render.yaml`):

1. Commit your changes and push them to GitHub/GitLab.
2. Go to the **Render Dashboard** -> **New** -> **Blueprint**.
3. Connect your repository. Render will automatically detect `render.yaml` and configure:
   - A FastAPI service called `ai-chatbot-backend`.
   - A Streamlit service called `ai-chatbot-frontend`.
4. Enter your `GEMINI_API_KEY` when prompted.
5. Once deployed, get the URL of your backend service (e.g., `https://ai-chatbot-backend.onrender.com`), copy it, and update the `API_URL` environment variable of your frontend service to `https://ai-chatbot-backend.onrender.com/chat`.
