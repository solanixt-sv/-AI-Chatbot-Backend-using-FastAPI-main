import streamlit as st
import requests
import os
import socket
import threading
import time
from dotenv import load_dotenv
            try:
                response = requests.post(
                    API_URL,
                    json={"prompt": active_prompt},
                    timeout=120
                )
                if response.status_code == 200:
                    reply = response.json().get("reply", "No reply received.")
                    message_placeholder.markdown(reply)
                else:
                    message_placeholder.markdown(f"Error from backend: {response.status_code} - {response.text}")
            except requests.exceptions.RequestException as e:
                # If HTTP to the backend fails (common on Streamlit Cloud), try a local fallback
                try:
                    from app.llm_service import get_ai_reply

                    reply = get_ai_reply(active_prompt)
                    message_placeholder.markdown(reply)
                except Exception as e2:
                    message_placeholder.markdown(
                        f"Failed to connect to backend and local fallback failed: {e} / {e2}"
                    )
# and the backend isn't already running. This enables single-click deployment/running.
@st.cache_resource
def auto_start_backend():
    if "127.0.0.1:8000" in API_URL or "localhost:8000" in API_URL:
        # Check if port 8000 is already open
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            is_in_use = s.connect_ex(('127.0.0.1', 8000)) == 0
        
        if not is_in_use:
            try:
                import uvicorn
                from app.main import app
                thread = threading.Thread(
                    target=lambda: uvicorn.run(app, host="127.0.0.1", port=8000, log_level="warning"),
                    daemon=True
                )
                thread.start()
                # Allow a short moment for uvicorn to initialize and bind
                time.sleep(1.5)
            except Exception as e:
                pass

auto_start_backend()

# Inject Premium CSS Styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;800&family=Inter:wght@300;400;500;600&display=swap');

/* Apply font to headers and markdown */
html, body, [class*="css"], .stMarkdown, p, span, div, h1, h2, h3 {
    font-family: 'Outfit', 'Inter', sans-serif !important;
}

/* Glowing Title */
.glowing-title {
    background: linear-gradient(135deg, #a855f7 0%, #3b82f6 50%, #06b6d4 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 2.8rem;
    font-weight: 800;
    text-align: center;
    margin-bottom: 0.2rem;
    padding-bottom: 0.5rem;
}

.subtitle {
    font-size: 1.1rem;
    text-align: center;
    color: #94a3b8;
    margin-bottom: 2rem;
}

/* Chat bubble styling overrides */
div[data-testid="stChatMessage"] {
    background-color: rgba(255, 255, 255, 0.04) !important;
    border-radius: 16px !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    padding: 15px !important;
    margin-bottom: 12px !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

div[data-testid="stChatMessage"]:hover {
    border-color: rgba(168, 85, 247, 0.3) !important;
    box-shadow: 0 4px 20px rgba(168, 85, 247, 0.08) !important;
    transform: translateY(-2px);
}

/* App Container adjustment */
.block-container {
    padding-top: 3rem !important;
}

/* Custom indicator in sidebar */
.status-container {
    display: flex;
    align-items: center;
    background-color: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    padding: 10px 16px;
    border-radius: 12px;
    margin-bottom: 20px;
}

.status-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    margin-right: 12px;
    position: relative;
}

.pulse-green {
    background-color: #10b981;
    box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
    animation: pulse-green 1.5s infinite;
}

.pulse-red {
    background-color: #ef4444;
    box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7);
    animation: pulse-red 1.5s infinite;
}

@keyframes pulse-green {
    0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
    70% { transform: scale(1); box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }
    100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
}

@keyframes pulse-red {
    0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7); }
    70% { transform: scale(1); box-shadow: 0 0 0 6px rgba(239, 68, 68, 0); }
    100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
}
</style>
""", unsafe_allow_html=True)

# Render Custom Header
st.markdown('<div class="glowing-title">SolanixT AI Chatbot</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">A FastAPI-backed conversational agent powered by Google Gemini</div>', unsafe_allow_html=True)

# Sidebar with status and info
with st.sidebar:
    st.image("https://img.icons8.com/nolan/256/bot.png", width=80)
    st.markdown("### Backend Status")
    
    # Check connection
    backend_online = False
    try:
        from urllib.parse import urlparse
        parsed_url = urlparse(API_URL)
        host = parsed_url.hostname or "127.0.0.1"
        port = parsed_url.port or 8000
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1.0)
            backend_online = s.connect_ex((host, port)) == 0
    except Exception:
        backend_online = False
        
    if backend_online:
        st.markdown("""
        <div class="status-container">
            <div class="status-dot pulse-green"></div>
            <div>
                <strong style="color: #10b981;">Connected</strong><br>
                <span style="font-size: 0.8rem; color: #94a3b8;">API is online and ready</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="status-container">
            <div class="status-dot pulse-red"></div>
            <div>
                <strong style="color: #ef4444;">Disconnected</strong><br>
                <span style="font-size: 0.8rem; color: #94a3b8;">API is unreachable</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.warning(f"Frontend is pointing to `{API_URL}` but no active service was detected. Start the FastAPI server to chat.")
        
    st.markdown("---")
    st.markdown("### About")
    st.write("This application demonstrates a clean separation of concerns: a FastAPI backend delivering structured, validated API endpoints, and a Streamlit web interface for conversational UX.")
    
    if st.button("Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pending_prompt = None
        st.rerun()

# Initialize message history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display conversation history
for message in st.session_state.messages:
    avatar = "👤" if message["role"] == "user" else "🤖"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Check if there is a prompt to process
active_prompt = None

if prompt := st.chat_input("What is on your mind?"):
    active_prompt = prompt
elif "pending_prompt" in st.session_state and st.session_state.pending_prompt:
    active_prompt = st.session_state.pending_prompt
    del st.session_state.pending_prompt

# Suggestion Chips / Starter Prompts (only if no messages and no pending prompt)
if not st.session_state.messages and not active_prompt:
    st.write("### Try starting with one of these:")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚀 Explain Quantum Computing", use_container_width=True):
            st.session_state.pending_prompt = "Explain Quantum Computing in simple terms."
            st.rerun()
        if st.button("✍️ Write a poem about robots", use_container_width=True):
            st.session_state.pending_prompt = "Write a short, creative poem about robots learning to paint."
            st.rerun()
    with col2:
        if st.button("💡 Brainstorm 3 app ideas", use_container_width=True):
            st.session_state.pending_prompt = "Brainstorm 3 unique web application ideas combining AI and education."
            st.rerun()
        if st.button("🐍 Python decorators explained", use_container_width=True):
            st.session_state.pending_prompt = "What are Python decorators? Show a simple practical example."
            st.rerun()

# If we have a prompt, run the processing
if active_prompt:
    # Render user message
    with st.chat_message("user", avatar="👤"):
        st.markdown(active_prompt)
    st.session_state.messages.append({"role": "user", "content": active_prompt})

    # Render assistant reply
    with st.chat_message("assistant", avatar="🤖"):
        message_placeholder = st.empty()
        with st.spinner("Analyzing and thinking..."):
            try:
                response = requests.post(
                    API_URL,
                    json={"prompt": active_prompt},
                    timeout=120
                )
                if response.status_code == 200:
                    reply = response.json().get("reply", "No reply received.")
                    message_placeholder.markdown(reply)
                else:
                    message_placeholder.markdown(f"Error from backend: {response.status_code} - {response.text}")
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                else:
                    try:
                        error_detail = response.json().get("detail", "Unknown error")
                    except Exception:
                        error_detail = response.text
                    message_placeholder.error(f"Error {response.status_code}: {error_detail}")
                    st.session_state.messages.append({"role": "assistant", "content": f"❌ Error {response.status_code}: {error_detail}"})
            except requests.exceptions.RequestException as e:
                error_msg = f"Failed to connect to FastAPI backend at {API_URL}. Details: {e}"
                message_placeholder.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": f"❌ {error_msg}"})
    st.rerun()
