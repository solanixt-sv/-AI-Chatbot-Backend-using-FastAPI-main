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
Running the Server

FastAPI server runs locally and can be tested via Swagger UI at /docs.

Workflow allows seamless interaction between user requests and the AI model.

Key Features

FastAPI backend with structured endpoints

Pydantic validation for safe input handling

Integration with Gemini LLM

Proper HTTP error responses

Secure API key management via .env


front end using streamlit 
