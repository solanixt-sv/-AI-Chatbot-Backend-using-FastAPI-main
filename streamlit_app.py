import streamlit as st
import requests
import os

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/chat")

st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 AI Chatbot")
st.markdown("---")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is on your mind?"):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = requests.post(
                    API_URL,
                    json={"prompt": prompt}
                )
                if response.status_code == 200:
                    reply = response.json().get("reply", "No reply received.")
                    st.markdown(reply)
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                else:
                    st.error(f"Error {response.status_code}: {response.text}")
    except Exception as e:
        st.error(f"Failed to connect to backend: {str(e)}")
