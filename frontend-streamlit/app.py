import streamlit as st
import requests
import time
import json
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL_LINK")

COOLDOWN_SECONDS = 30  

st.set_page_config(page_title="Qonfido - FinChat", layout="wide")

st.markdown("""
<style>
    /* ---- GLOBAL DARK THEME ---- */
    .stApp {
        background-color: #343541;
    }
    
    /* All text white by default */
    body, .stMarkdown, .markdown-text-container, p, span, div {
        color: #ECECF1 !important;
    }
    
    /* ---- HEADER WITH LOGO ---- */
    .header-container {
        display: flex;
        align-items: center;
        gap: 15px;
        padding: 20px 0;
        margin-bottom: 20px;
    }
    
    .header-container img {
        height: 40px;
    }
    
    .header-container h1 {
        color: #ECECF1 !important;
        margin: 0;
        font-size: 28px;
    }

    /* ---- CHAT CONTAINER ---- */
    .chat-container {
        max-width: 900px;
        margin: 0 auto;
    }

    /* ---- MESSAGE BUBBLES ---- */
    .message-row {
        display: flex;
        padding: 20px;
        margin-bottom: 1px;
    }
    
    .user-message {
        background-color: #343541;
    }
    
    .assistant-message {
        background-color: #444654;
    }
    
    .message-content {
        max-width: 900px;
        margin: 0 auto;
        width: 100%;
        color: #ECECF1 !important;
    }
    
    .message-icon {
        width: 30px;
        height: 30px;
        border-radius: 2px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 15px;
        font-size: 18px;
        flex-shrink: 0;
    }
    
    .user-icon {
        background-color: #5436DA;
    }
    
    .assistant-icon {
        background-color: #19C37D;
    }

    /* ---- COOLDOWN BOX ---- */
    .cooldown-box {
        padding: 15px;
        border-radius: 8px;
        background: #565869;
        color: #ECECF1 !important;
        border: 1px solid #6e6e80;
        margin: 20px auto;
        max-width: 900px;
        font-size: 16px;
        text-align: center;
    }
    
    /* ---- INPUT AREA ---- */
    .stTextInput input {
        background-color: #40414F !important;
        color: #ECECF1 !important;
        border: 1px solid #565869 !important;
        border-radius: 8px !important;
    }
    
    .stSelectbox select {
        background-color: #40414F !important;
        color: #ECECF1 !important;
        border: 1px solid #565869 !important;
    }
    
    .stButton button {
        background-color: #19C37D !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
        font-weight: 600 !important;
    }
    
    .stButton button:hover {
        background-color: #1a9f6b !important;
    }
    
    /* ---- EXPANDERS ---- */
    .streamlit-expanderHeader {
        background-color: #40414F !important;
        color: #ECECF1 !important;
        border-radius: 8px !important;
    }
    
    .streamlit-expanderContent {
        background-color: #343541 !important;
        color: #ECECF1 !important;
        border: 1px solid #565869 !important;
    }
    
    /* ---- TABLES ---- */
    table {
        background-color: #40414F !important;
        color: #ECECF1 !important;
    }
    
    thead tr th {
        background-color: #565869 !important;
        color: #ECECF1 !important;
        border-bottom: 1px solid #6e6e80 !important;
    }
    
    tbody tr td {
        background-color: #40414F !important;
        color: #ECECF1 !important;
        border-bottom: 1px solid #565869 !important;
    }
    
    /* ---- SPINNER ---- */
    .stSpinner > div {
        border-top-color: #19C37D !important;
    }

</style>
""", unsafe_allow_html=True)


if "messages" not in st.session_state:
    st.session_state.messages = []

if "cooldown_until" not in st.session_state:
    st.session_state.cooldown_until = None


def call_backend(query, mode):
    payload = {"query": query, "mode": mode}
    try:
        resp = requests.post(BACKEND_URL, json=payload, timeout=30)
    except Exception as e:
        return {"answer": f"❌ Could not reach backend: {e}"}

    if resp.status_code == 500:
        return {"answer": f"⚠️ OPENROUTER RATE LIMIT REACHED ({resp.status_code}): {resp.text}. \n Please try again after an hour, the model used is a free tier option from openrouter, thus it has limited rate limit. You can access this again after sometime. Thank You!"}
    
    if resp.status_code != 200:
        return {"answer": f"❌ Backend error ({resp.status_code}): {resp.text}"}

    return resp.json()

def render_cooldown():
    COOLDOWN_MESSAGES = [
        "[1/6] A short buffer is intentionally added to avoid overwhelming the free-tier model…",
        "[2/6] This helps prevent backend rate-limit errors and ensures responses stay reliable…",
        "[3/6] The 30-second cooldown keeps the system stable by giving the model room to recover…",
        "[4/6] Optimizing the model for your next response…",
        "[5/6] Preparing your chat environment…",
        "[6/6] It is almost done, Chat Responsibly!!!",
    ]
    now = datetime.utcnow()
    remaining = int((st.session_state.cooldown_until - now).total_seconds())

    if remaining > 0:
        elapsed = COOLDOWN_SECONDS - remaining
        index = int(elapsed // 5) % len(COOLDOWN_MESSAGES)
        rotating_text = COOLDOWN_MESSAGES[index]

        st.markdown(
            f"""
            <div class='cooldown-box'>
                ⏳ Please wait <b>{remaining} seconds</b><br>
                <b>{rotating_text}</b>
            </div>
            """,
            unsafe_allow_html=True,
        )
        time.sleep(1)
        st.rerun()
    else:
        st.session_state.cooldown_until = None
        st.rerun()

st.markdown("""
<div class='header-container'>
    <img src='https://www.qonfido.com/_next/static/media/logoQonfido.8b9eee0b.svg' alt='Qonfido Logo'>
    <h1>Your Personal Financial Assistant</h1>
</div>
""", unsafe_allow_html=True)

for i, msg in enumerate(st.session_state.messages):
    role = msg.get("role")
    content = msg.get("content", "")

    if role == "user":
        st.markdown(f"""
        <div class='message-row user-message'>
            <div class='message-content'>
                <div style='display: flex;'>
                    <div class='message-icon user-icon'>👤</div>
                    <div style='flex: 1;'>{content}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class='message-row assistant-message'>
            <div class='message-content'>
                <div style='display: flex;'>
                    <div class='message-icon assistant-icon'>Q</div>
                    <div style='flex: 1;'>{content}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if msg.get("sources"):
            with st.expander(f"🗂 Sources Used (message #{i})", expanded=False):
                rows = []
                for s in msg["sources"]:
                    meta = s.get("source_meta", {})
                    label = meta.get("fund_name") or meta.get("question") or "—"

                    rows.append({
                        "ID": s.get("id"),
                        "Type": s.get("type"),
                        "Label": label,
                        "Reference": s.get("source_text"),
                        "Score": round(s.get("score", 0), 4),
                    })

                st.table(rows)

        if msg.get("reasoning"):
            with st.expander(f"🧠 Model Reasoning (message #{i})", expanded=False):
                text = msg["reasoning"].get("text") if isinstance(msg["reasoning"], dict) else msg["reasoning"]
                st.markdown(f"**Reasoning:**<br>{text}", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

if st.session_state.cooldown_until:
    render_cooldown()
else:
    with st.form("chat_form", clear_on_submit=True):
        col1, col2 = st.columns([4, 1])

        with col1:
            user_input = st.text_input("Send a message...", label_visibility="collapsed",
                                       placeholder="Ask about funds, investments, or financial queries...")

        with col2:
            mode = st.selectbox(
                "Mode",
                ["hybrid", "lexical", "semantic"],
                index=0,
                label_visibility="collapsed"
            )

        submitted = st.form_submit_button("Send", use_container_width=True)

    if submitted and user_input.strip():

        st.session_state.messages.append({
            "role": "user",
            "content": f"{user_input} (search mode: {mode})"
        })

        with st.spinner("Analyzing Query.... Retrieving the best Source... Generating Response.."):
            result = call_backend(user_input, mode)

        assistant_msg = {
            "role": "assistant",
            "content": result.get("answer", "⚠️ No answer returned."),
            "sources": result.get("sources", []) or [],
            "reasoning": result.get("reasoning", None)
        }

        st.session_state.messages.append(assistant_msg)

        st.session_state.cooldown_until = datetime.utcnow() + timedelta(seconds=COOLDOWN_SECONDS)

        st.rerun()
