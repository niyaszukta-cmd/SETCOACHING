"""
Kerala SET English Literature & Linguistics - Practice App
Main entry point
"""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from utils.styles import get_css
from utils.session import init_session
from data.question_bank import TOPICS, DIFFICULTIES, QUESTION_BANK

st.set_page_config(
    page_title="Kerala SET Practice",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(get_css(), unsafe_allow_html=True)
init_session()

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📚 Kerala SET Practice")
    st.markdown("---")

    # Navigation
    pages = {
        "🏠 Home":        "home",
        "📝 Practice Quiz": "quiz",
        "🤖 AI Generator":  "ai_gen",
        "📊 Analytics":     "analytics",
        "📖 Question Bank": "bank",
    }
    for label, key in pages.items():
        if st.button(label, key=f"nav_{key}", use_container_width=True):
            st.session_state.page = key
            st.rerun()

    st.markdown("---")

    # API Key
    st.markdown("##### 🔑 Anthropic API Key")
    api_input = st.text_input(
        "API Key", value=st.session_state.api_key,
        type="password", label_visibility="collapsed",
        placeholder="sk-ant-...",
    )
    if api_input != st.session_state.api_key:
        st.session_state.api_key = api_input
        st.session_state.api_key_valid = False

    if st.session_state.api_key:
        total_q = len(QUESTION_BANK) + len(st.session_state.ai_questions)
        st.markdown(f"<small>✅ Key set &nbsp;|&nbsp; 🗂 **{total_q}** questions</small>", unsafe_allow_html=True)
    else:
        st.markdown("<small style='opacity:0.65'>Enter key to unlock AI generation</small>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<small style='opacity:0.55'>NYZTrade Education Platform<br>Kerala SET Series 2026</small>", unsafe_allow_html=True)


# ─── PAGES ────────────────────────────────────────────────────────────────────
page = st.session_state.page

if page == "home":
    from pages.home import render
    render()
elif page == "quiz":
    from pages.quiz import render
    render()
elif page == "ai_gen":
    from pages.ai_gen import render
    render()
elif page == "analytics":
    from pages.analytics import render
    render()
elif page == "bank":
    from pages.bank import render
    render()
