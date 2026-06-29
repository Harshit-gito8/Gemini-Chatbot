import json
import os
import streamlit as st
from google import genai
from google.genai import types
from config import API_KEY


client = genai.Client(api_key=API_KEY)


HISTORY_FILE = "chat_history.json"


def load_history():
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
    except Exception:
        return []

    return []


def save_history(messages):
    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(messages, file, indent=4, ensure_ascii=False)



st.set_page_config(
    page_title="Gemini AI Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Gemini AI Assistant")
st.caption("Powered by Google Gemini 2.5 Flash")


st.sidebar.title("Gemini AI Assistant")

st.sidebar.success("🧠 Conversation Memory Enabled")
st.sidebar.success("🌐 Google Search Enabled")

st.sidebar.markdown("---")
st.sidebar.write("**Model:** Gemini 2.5 Flash")


if "messages" not in st.session_state:
    st.session_state.messages = load_history()

st.sidebar.write(f"**Messages:** {len(st.session_state.messages)}")

if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    save_history([])
    st.rerun()


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


prompt = st.chat_input("Ask me anything...")

if prompt:

   
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    save_history(st.session_state.messages)

    with st.chat_message("user"):
        st.markdown(prompt)

   
    conversation = []

    for msg in st.session_state.messages:

        role = "user" if msg["role"] == "user" else "model"

        conversation.append(
            {
                "role": role,
                "parts": [
                    {
                        "text": msg["content"]
                    }
                ]
            }
        )

  
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=conversation,
                    config=types.GenerateContentConfig(
                        tools=[
                            types.Tool(
                                google_search=types.GoogleSearch()
                            )
                        ]
                    )
                )

                reply = response.text

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": reply
                    }
                )

                save_history(st.session_state.messages)

                st.markdown(reply)

            except Exception as e:

                st.error(f"Error: {e}")
