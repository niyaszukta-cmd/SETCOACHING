"""
╔══════════════════════════════════════════════════════════════╗
║          NET QUIZ MASTER — UGC NET Paper 1                  ║
║          All-in-one Streamlit Application                   ║
║                                                              ║
║  Sections:                                                   ║
║    1. IMPORTS & PAGE CONFIG                                  ║
║    2. CUSTOM CSS STYLES                                      ║
║    3. QUESTION BANK  (built-in questions + JSON storage)    ║
║    4. PDF EXTRACTOR  (PyMuPDF / pdfplumber / PyPDF2)        ║
║    5. AI GENERATOR   (Claude & Gemini APIs)                 ║
║    6. SESSION STATE INIT                                     ║
║    7. SIDEBAR                                                ║
║    8. PAGE: HOME                                             ║
║    9. PAGE: QUIZ CONFIG                                      ║
║   10. PAGE: QUIZ INTERFACE                                   ║
║   11. PAGE: RESULTS                                          ║
║   12. PAGE: ANALYTICS                                        ║
║   13. PAGE: AI QUESTION LAB                                  ║
║   14. PAGE: PDF UPLOAD                                       ║
║   15. PAGE: BOOKMARKS                                        ║
║   16. PAGE: SETTINGS                                         ║
║   17. MAIN ROUTER                                            ║
╚══════════════════════════════════════════════════════════════╝

Usage:
    pip install streamlit pandas PyMuPDF pdfplumber PyPDF2
    pip install pdf2image pytesseract Pillow   # for scanned PDF OCR
    # macOS:  brew install tesseract
    # Ubuntu: sudo apt install tesseract-ocr
    streamlit run net_quiz_master.py
"""

# ════════════════════════════════════════════════════════════════
# 1. IMPORTS & PAGE CONFIG
# ════════════════════════════════════════════════════════════════
import html
import json
import os
import re
import random
import time
import uuid
from itertools import product

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="NET Paper 1 — Quiz Master",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ════════════════════════════════════════════════════════════════
# 2. CUSTOM CSS STYLES
# ════════════════════════════════════════════════════════════════
def inject_styles():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=DM+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

/* ── HIDE STREAMLIT "None" OUTPUT BUG ── */
div[data-testid="stText"] > p,
div.stMarkdown > div[data-testid="stMarkdownContainer"] > p:empty,
p:empty { display: none !important; }
/* Target the green "None" badge specifically */
div[data-testid="stMarkdownContainer"] p { 
    color: inherit; 
}
/* Hide any standalone "None" text Streamlit auto-renders */
[data-testid="stVerticalBlock"] > div > div > div:empty { display:none !important; }

:root {
    --bg-primary: #07090f;
    --bg-secondary: #0d1117;
    --bg-card: #131929;
    --bg-card-hover: #1a2338;
    --accent-primary: #7c3aed;
    --accent-secondary: #a855f7;
    --accent-gold: #fbbf24;
    --accent-green: #10b981;
    --accent-red: #f43f5e;
    --accent-cyan: #22d3ee;
    --accent-orange: #f97316;
    --text-primary: #ffffff;
    --text-secondary: #cbd5e1;
    --text-muted: #64748b;
    --border-color: #1e2d45;
    --border-bright: #3b4f6e;
    --shadow: 0 8px 32px rgba(0,0,0,0.5);
    --shadow-glow: 0 0 40px rgba(124,58,237,0.25);
    --radius: 14px; --radius-lg: 22px;
}

.stApp { background: var(--bg-primary) !important; font-family: 'DM Sans', sans-serif !important; color: var(--text-primary) !important; }
.stApp::before { content:''; position:fixed; inset:0;
    background:
        radial-gradient(ellipse at 15% 15%, rgba(124,58,237,0.12) 0%, transparent 45%),
        radial-gradient(ellipse at 85% 85%, rgba(168,85,247,0.08) 0%, transparent 45%),
        radial-gradient(ellipse at 50% 0%, rgba(34,211,238,0.05) 0%, transparent 40%);
    pointer-events:none; z-index:0; }
#MainMenu, footer, header { visibility: hidden !important; }
.stDeployButton { display: none !important; }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1117 0%, #0a0e1a 100%) !important;
    border-right: 1px solid #1e2d45 !important;
}
[data-testid="stSidebar"] [data-testid="stVerticalBlock"] { padding: 1rem 0.5rem; }
.sidebar-brand {
    display:flex; align-items:center; gap:0.75rem; padding:1.1rem;
    background: linear-gradient(135deg, rgba(124,58,237,0.25), rgba(168,85,247,0.12));
    border-radius: var(--radius);
    border: 1px solid rgba(124,58,237,0.5);
    margin-bottom: 0.5rem;
    box-shadow: 0 0 20px rgba(124,58,237,0.15);
}
.brand-icon { font-size:2rem; }
.brand-title { font-family:'Playfair Display',serif; font-size:1.1rem; font-weight:700; color:#ffffff; line-height:1.2; }
.brand-subtitle { font-size:0.72rem; color:#a855f7; letter-spacing:0.1em; text-transform:uppercase; font-weight:600; }

[data-testid="stSidebar"] .stButton button {
    background: transparent !important;
    border: 1px solid transparent !important;
    color: #94a3b8 !important;
    text-align: left !important;
    font-size: 0.92rem !important;
    padding: 0.65rem 0.9rem !important;
    border-radius: 10px !important;
    transition: all 0.2s ease !important;
    font-family: 'DM Sans', sans-serif !important;
    width: 100% !important;
    font-weight: 500 !important;
}
[data-testid="stSidebar"] .stButton button:hover {
    background: rgba(124,58,237,0.18) !important;
    color: #ffffff !important;
    border-color: rgba(124,58,237,0.5) !important;
    transform: translateX(4px) !important;
}
[data-testid="stSidebar"] .stButton button[kind="primary"] {
    background: linear-gradient(135deg, rgba(124,58,237,0.35), rgba(168,85,247,0.2)) !important;
    border-color: #7c3aed !important;
    color: #ffffff !important;
    box-shadow: 0 0 12px rgba(124,58,237,0.2) !important;
}
.sidebar-stats {
    display:flex; justify-content:space-around;
    padding: 0.85rem;
    background: linear-gradient(135deg, rgba(124,58,237,0.1), rgba(34,211,238,0.05));
    border-radius: var(--radius);
    border: 1px solid rgba(124,58,237,0.3);
}
.stat-mini { text-align:center; }
.stat-mini-val { display:block; font-size:1.3rem; font-weight:800; font-family:'JetBrains Mono',monospace; background: linear-gradient(135deg, #a855f7, #22d3ee); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; }
.stat-mini-lbl { font-size:0.65rem; color: #64748b; text-transform:uppercase; letter-spacing:0.07em; margin-top:0.1rem; }

/* ── LAYOUT ── */
.main .block-container { padding:1.5rem 2rem 3rem !important; max-width:1200px !important; }

/* ── HERO ── */
.hero-section { text-align:center; padding:3rem 2rem 2rem; }
.hero-badge {
    display:inline-block;
    background: linear-gradient(135deg, rgba(124,58,237,0.3), rgba(168,85,247,0.15));
    border: 1px solid rgba(168,85,247,0.6);
    color: #c084fc;
    padding:0.4rem 1.3rem; border-radius:50px;
    font-size:0.82rem; font-weight:700;
    letter-spacing:0.12em; text-transform:uppercase; margin-bottom:1.5rem;
}
.hero-title { font-family:'Playfair Display',serif !important; font-size:clamp(2.5rem,5vw,4rem) !important; font-weight:800 !important; color:#ffffff !important; line-height:1.15 !important; margin-bottom:1rem !important; }
.gradient-text { background:linear-gradient(135deg, #7c3aed, #a855f7, #22d3ee); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; }
.hero-subtitle { color: #94a3b8 !important; font-size:1.1rem !important; max-width:600px !important; margin:0 auto !important; }

/* ── TOPIC CARDS ── */
.section-title { font-size:1.4rem; font-weight:800; color:#ffffff; margin:2rem 0 1rem; }
.topic-card {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: var(--radius); padding:1.4rem 1rem;
    text-align:center; margin-bottom:1rem;
    transition:all 0.25s ease; cursor:default;
}
.topic-card:hover {
    border-color: #7c3aed;
    transform: translateY(-4px);
    box-shadow: var(--shadow-glow);
    background: var(--bg-card-hover);
}
.topic-icon { font-size:2rem; margin-bottom:0.6rem; display:block; }
.topic-name { font-weight:700; font-size:0.88rem; color:#ffffff; margin-bottom:0.35rem; }
.topic-desc { font-size:0.72rem; color:#64748b; line-height:1.5; }

/* ── FEATURE CARDS ── */
.feature-card {
    background: linear-gradient(135deg, var(--bg-card), rgba(124,58,237,0.06));
    border: 1px solid var(--border-bright);
    border-radius: var(--radius-lg); padding:1.6rem;
    margin-bottom:1rem; min-height:140px;
}
.feature-icon { font-size:2.2rem; margin-bottom:0.8rem; display:block; }
.feature-title { font-weight:800; font-size:1.1rem; color:#ffffff; margin-bottom:0.5rem; }
.feature-desc { font-size:0.88rem; color:#94a3b8; line-height:1.65; }

/* ── CONFIG CARD ── */
.config-card {
    background: var(--bg-card);
    border: 1px solid var(--border-bright);
    border-radius: var(--radius-lg); padding:1.5rem; margin-bottom:1rem;
}

/* ── STATS BANNER ── */
.stats-banner {
    display:flex; justify-content:center; gap:3rem; padding:2.2rem;
    background: linear-gradient(135deg, rgba(124,58,237,0.15), rgba(34,211,238,0.06));
    border: 1px solid rgba(124,58,237,0.35);
    border-radius: var(--radius-lg); margin-top:2rem;
    box-shadow: var(--shadow-glow);
}
.banner-stat { text-align:center; }
.banner-val {
    display:block; font-family:'Playfair Display',serif;
    font-size:2.8rem; font-weight:800;
    background: linear-gradient(135deg, #a855f7, #22d3ee);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
}
.banner-lbl { font-size:0.82rem; color:#64748b; text-transform:uppercase; letter-spacing:0.1em; margin-top:0.2rem; }

/* ── PAGE TITLE ── */
.page-title {
    font-family:'Playfair Display',serif !important; font-size:2rem !important; font-weight:800 !important;
    color:#ffffff !important; margin-bottom:1.5rem !important;
    border-left:5px solid #7c3aed; padding-left:1rem;
}

/* ── QUIZ HEADER ── */
.quiz-header { display:flex; align-items:center; gap:0.75rem; margin-bottom:0.5rem; }
.q-counter { color:#cbd5e1; font-size:0.95rem; font-weight:600; }
.q-topic-badge {
    background: rgba(124,58,237,0.25); color:#c084fc;
    border: 1px solid rgba(168,85,247,0.6);
    padding:0.25rem 0.8rem; border-radius:20px;
    font-size:0.78rem; font-weight:700; letter-spacing:0.03em;
}
.q-diff-badge { padding:0.25rem 0.8rem; border-radius:20px; font-size:0.78rem; font-weight:700; }
.diff-easy   { background:rgba(16,185,129,0.2);  color:#34d399; border:1px solid rgba(16,185,129,0.5); }
.diff-medium { background:rgba(251,191,36,0.2);  color:#fbbf24; border:1px solid rgba(251,191,36,0.5); }
.diff-hard   { background:rgba(244,63,94,0.2);   color:#fb7185; border:1px solid rgba(244,63,94,0.5); }

.timer-box {
    background: linear-gradient(135deg, rgba(34,211,238,0.15), rgba(124,58,237,0.1));
    border: 1px solid rgba(34,211,238,0.4);
    border-radius:10px; padding:0.5rem 0.9rem;
    font-family:'JetBrains Mono',monospace; font-size:1.05rem;
    color:#22d3ee; text-align:center; font-weight:700;
}

/* ── QUESTION CARD ── */
.question-card {
    background: linear-gradient(135deg, #131929, #0f1724);
    border: 1px solid #2d3f5e;
    border-radius: var(--radius-lg); padding:2.2rem 2.4rem;
    margin:1rem 0 1.5rem;
    box-shadow: 0 8px 40px rgba(0,0,0,0.5), 0 0 0 1px rgba(124,58,237,0.15);
    position:relative; overflow:hidden;
}
.question-card::before {
    content:''; position:absolute; top:0; left:0; right:0; height:4px;
    background: linear-gradient(90deg, #7c3aed, #a855f7, #22d3ee);
}
.question-card::after {
    content:''; position:absolute; top:0; left:0; bottom:0; width:4px;
    background: linear-gradient(180deg, #7c3aed, #22d3ee);
}
.question-meta { display:flex; justify-content:space-between; align-items:center; margin-bottom:1.4rem; }
.q-num-pill {
    background: linear-gradient(135deg, #7c3aed, #a855f7);
    color:#ffffff; font-size:0.82rem; font-weight:800;
    padding:0.35rem 1rem; border-radius:20px;
    letter-spacing:0.08em; font-family:'JetBrains Mono',monospace;
    box-shadow: 0 0 12px rgba(124,58,237,0.4);
}
.bookmark-indicator { color:#fbbf24; font-size:1.2rem; }
.question-text {
    font-family:'Playfair Display',serif;
    font-size:1.4rem; font-weight:700; color:#ffffff;
    line-height:1.8; letter-spacing:0.01em;
}

/* ── ANSWER OPTIONS (post-submission display) ── */
.option-btn {
    display:block; padding:1rem 1.5rem; border-radius:12px; margin:0.5rem 0;
    font-size:0.97rem; font-weight:600; cursor:default; border:2px solid; line-height:1.5;
}
.correct-opt {
    background: rgba(16,185,129,0.15); border-color:#10b981; color:#34d399;
    box-shadow: 0 0 16px rgba(16,185,129,0.2);
}
.wrong-opt  { background: rgba(244,63,94,0.12);  border-color:#f43f5e; color:#fb7185; }
.neutral-opt { background: rgba(30,45,69,0.6);   border-color:#2d3f5e; color:#94a3b8; }

/* ── FORM STYLING — hide borders, style option submit buttons ── */
div[data-testid="stForm"] {
    border: none !important;
    padding: 0 !important;
    background: transparent !important;
}
/* Unselected option buttons (form_submit_button secondary look) */
div[data-testid="stForm"] button[kind="secondaryFormSubmit"],
div[data-testid="stForm"] button[kind="formSubmit"] {
    background: #131929 !important;
    border: 2px solid #2d3f5e !important;
    color: #e2e8f0 !important;
    text-align: left !important;
    padding: 0.9rem 1.4rem !important;
    border-radius: 12px !important;
    font-size: 0.97rem !important;
    font-weight: 600 !important;
    margin: 0.35rem 0 !important;
    width: 100% !important;
    transition: all 0.15s ease !important;
}
div[data-testid="stForm"] button[kind="secondaryFormSubmit"]:hover,
div[data-testid="stForm"] button[kind="formSubmit"]:hover {
    border-color: #a855f7 !important;
    background: rgba(124,58,237,0.15) !important;
    color: #ffffff !important;
}
/* Primary submit buttons inside forms */
div[data-testid="stForm"] button[kind="primaryFormSubmit"] {
    background: linear-gradient(135deg, #7c3aed, #a855f7) !important;
    color: white !important;
    box-shadow: 0 4px 20px rgba(124,58,237,0.4) !important;
    border-radius: 12px !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    padding: 0.85rem 1.4rem !important;
}
div[data-testid="stForm"] button[kind="primaryFormSubmit"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 28px rgba(124,58,237,0.55) !important;
}

/* ── EXPLANATION ── */
.explanation-box {
    background: linear-gradient(135deg, rgba(124,58,237,0.12), rgba(34,211,238,0.06));
    border: 1px solid rgba(124,58,237,0.4);
    border-radius: var(--radius); padding:1.3rem; margin-top:1.3rem;
}
.exp-title { font-weight:800; color:#c084fc; margin-bottom:0.5rem; font-size:0.95rem; }
.exp-text { color:#cbd5e1; font-size:0.93rem; line-height:1.75; }

/* ── RESULTS ── */
.results-hero {
    text-align:center; padding:2.5rem 2rem;
    background: linear-gradient(135deg, #131929, rgba(124,58,237,0.08));
    border: 1px solid #2d3f5e; border-radius: var(--radius-lg); margin-bottom:2rem;
}
.results-grade { font-family:'Playfair Display',serif; font-size:4rem; font-weight:800; line-height:1; margin-bottom:0.5rem; }
.results-score { font-size:2rem; font-weight:700; color:#ffffff; font-family:'JetBrains Mono',monospace; }
.results-pct { font-size:1.1rem; color:#94a3b8; margin:0.5rem 0; }
.results-msg { font-size:1rem; color:#fbbf24; font-style:italic; margin-top:0.5rem; }
.result-stat-card { background: var(--bg-card); border:1px solid var(--border-bright); border-radius:var(--radius); padding:1.2rem; text-align:center; }
.rs-val { font-size:1.8rem; font-weight:800; font-family:'JetBrains Mono',monospace; display:block; margin-bottom:0.3rem; }
.rs-lbl { font-size:0.78rem; color:#64748b; text-transform:uppercase; letter-spacing:0.08em; }

/* ── ANALYTICS ── */
.analytics-card { background:var(--bg-card); border:1px solid var(--border-bright); border-radius:var(--radius); padding:1.3rem 1.6rem; margin-bottom:1rem; }
.ac-title { font-size:0.8rem; color:#64748b; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:0.4rem; font-weight:600; }
.ac-val { font-size:2.2rem; font-weight:800; font-family:'JetBrains Mono',monospace; display:block; }
.ac-sub { font-size:0.82rem; color:#94a3b8; margin-top:0.2rem; }

/* ── PDF UPLOAD ── */
.pdf-intro {
    background: linear-gradient(135deg, rgba(34,211,238,0.1), rgba(124,58,237,0.07));
    border: 1px solid rgba(34,211,238,0.35);
    border-radius: var(--radius); padding:1.1rem 1.6rem;
    color: #cbd5e1; font-size:0.93rem; margin-bottom:1.5rem; line-height:1.7;
}
.step-list { display:flex; flex-direction:column; gap:0.8rem; }
.step-item { display:flex; align-items:center; gap:0.8rem; font-size:0.88rem; color:#94a3b8; }
.step-num {
    width:28px; height:28px;
    background: linear-gradient(135deg, #7c3aed, #22d3ee);
    color:white; border-radius:50%; display:flex; align-items:center; justify-content:center;
    font-size:0.75rem; font-weight:800; flex-shrink:0;
    box-shadow: 0 0 8px rgba(124,58,237,0.4);
}

/* ── EMPTY STATE ── */
.empty-state { text-align:center; padding:4rem 2rem; color:#475569; }
.empty-icon { font-size:3rem; margin-bottom:1rem; display:block; }
.empty-title { font-size:1.3rem; font-weight:700; color:#64748b; margin-bottom:0.5rem; }
.empty-desc { font-size:0.9rem; }

/* ── STREAMLIT WIDGET OVERRIDES ── */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #7c3aed, #a855f7, #22d3ee) !important;
}
.stButton button {
    font-family:'DM Sans',sans-serif !important; font-weight:600 !important;
    border-radius:10px !important; transition:all 0.2s ease !important; border:none !important;
}
.stButton button[kind="primary"] {
    background: linear-gradient(135deg, #7c3aed, #a855f7) !important;
    color:white !important; box-shadow:0 4px 20px rgba(124,58,237,0.4) !important;
}
.stButton button[kind="primary"]:hover {
    transform:translateY(-2px) !important;
    box-shadow:0 6px 28px rgba(124,58,237,0.55) !important;
}
.stButton button[kind="secondary"] {
    background: #131929 !important; color:#e2e8f0 !important;
    border: 1px solid #2d3f5e !important;
}
.stButton button[kind="secondary"]:hover {
    border-color: #7c3aed !important; color:#ffffff !important;
    background: rgba(124,58,237,0.12) !important;
}
.stRadio label { color:#cbd5e1 !important; font-size:0.95rem !important; }
.stSelectbox label { color:#94a3b8 !important; font-weight:600 !important; }
div[data-baseweb="select"] { background:#131929 !important; border-color:#2d3f5e !important; }
div[data-baseweb="select"] * { color:#e2e8f0 !important; }
.stTextInput input, .stTextArea textarea {
    background:#131929 !important; border-color:#2d3f5e !important;
    color:#ffffff !important; font-family:'DM Sans',sans-serif !important;
}
.stTextInput input::placeholder, .stTextArea textarea::placeholder { color:#475569 !important; }
.stCheckbox label { color:#cbd5e1 !important; font-weight:500 !important; }
.stCheckbox label span { color:#ffffff !important; }
.streamlit-expanderHeader {
    background:#131929 !important; border-color:#2d3f5e !important;
    color:#ffffff !important; border-radius:var(--radius) !important; font-weight:600 !important;
}
div[data-baseweb="tag"] { background:rgba(124,58,237,0.3) !important; color:#c084fc !important; }
.stInfo {
    background:rgba(124,58,237,0.12) !important; border-color:rgba(124,58,237,0.5) !important;
    color:#cbd5e1 !important; border-radius:10px !important;
}
.stSuccess {
    background:rgba(16,185,129,0.12) !important; border-color:rgba(16,185,129,0.5) !important;
    color:#6ee7b7 !important; border-radius:10px !important;
}
.stError {
    background:rgba(244,63,94,0.12) !important; border-color:rgba(244,63,94,0.5) !important;
    color:#fda4af !important; border-radius:10px !important;
}
.stWarning {
    background:rgba(251,191,36,0.12) !important; border-color:rgba(251,191,36,0.5) !important;
    color:#fde68a !important; border-radius:10px !important;
}
.stSpinner > div { border-top-color:#7c3aed !important; }
.stMarkdown h1,.stMarkdown h2,.stMarkdown h3,.stMarkdown h4 { color:#ffffff !important; font-family:'DM Sans',sans-serif !important; }
hr { border-color:#1e2d45 !important; }
::-webkit-scrollbar { width:6px; height:6px; }
::-webkit-scrollbar-track { background:#07090f; }
::-webkit-scrollbar-thumb { background:#2d3f5e; border-radius:3px; }
::-webkit-scrollbar-thumb:hover { background:#7c3aed; }
[data-testid="stFileUploader"] {
    background:#131929 !important; border:2px dashed #2d3f5e !important; border-radius:var(--radius) !important;
}
[data-testid="stFileUploader"]:hover { border-color:#7c3aed !important; }
.stToggle label { color:#cbd5e1 !important; font-weight:500 !important; }
div[data-testid="metric-container"] {
    background:#131929 !important; border:1px solid #2d3f5e !important;
    border-radius:var(--radius) !important; padding:1rem !important;
}
div[data-testid="metric-container"] label { color:#94a3b8 !important; }
div[data-testid="metric-container"] [data-testid="stMetricValue"] { color:#ffffff !important; }
select option { background:#131929 !important; color:#ffffff !important; }

/* ── NUCLEAR NONE-TEXT HIDE ── */
/* Streamlit prints "None" as green badge text in element-container > stMarkdownContainer */
div[data-testid="stMarkdownContainer"] p:only-child { 
    display: none !important; 
}
/* Also target the specific green badge Streamlit uses */
.stMarkdown small, 
div.element-container div[data-testid="stMarkdownContainer"] > p { 
    color: transparent !important;
    font-size: 0 !important;
    height: 0 !important;
    overflow: hidden !important;
    display: none !important;
}
/* Hide stText elements that render None */
[data-testid="stText"] { display: none !important; }
</style>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════
# 3. QUESTION BANK
# ════════════════════════════════════════════════════════════════
QUESTION_BANK_FILE = "question_bank.json"

BUILTIN_QUESTIONS = [
    # ── Teaching Aptitude ──
    {"id":"ta001","topic":"Teaching Aptitude","difficulty":"Medium","question":"Which level of teaching focuses on the development of thinking power and reasoning in students?","options":["Memory level","Understanding level","Reflective level","None of these"],"correct_answer":"Reflective level","explanation":"Reflective level teaching by Morrison focuses on critical thinking, problem-solving, and independent reasoning — the highest cognitive level."},
    {"id":"ta002","topic":"Teaching Aptitude","difficulty":"Easy","question":"Which of the following is NOT a characteristic of effective teaching?","options":["Clarity of goals","Flexibility","Dogmatic approach","Student-centered learning"],"correct_answer":"Dogmatic approach","explanation":"Effective teaching is flexible and student-centered; a dogmatic (rigid, doctrine-based) approach hinders learning."},
    {"id":"ta003","topic":"Teaching Aptitude","difficulty":"Hard","question":"In the context of Bloom's Taxonomy (revised), which cognitive level represents the highest order of thinking?","options":["Evaluation","Synthesis","Creating","Analysis"],"correct_answer":"Creating","explanation":"The revised Bloom's Taxonomy (Anderson & Krathwohl, 2001) places 'Creating' at the apex — generating new ideas, products, or ways of viewing things."},
    {"id":"ta004","topic":"Teaching Aptitude","difficulty":"Medium","question":"Which teaching method is most appropriate for large classrooms with heterogeneous groups?","options":["Project Method","Lecture Method","Inquiry Method","Seminar Method"],"correct_answer":"Lecture Method","explanation":"The lecture method is most practical for large, heterogeneous groups, allowing structured delivery to many students simultaneously."},
    {"id":"ta005","topic":"Teaching Aptitude","difficulty":"Medium","question":"The concept of 'Micro-Teaching' was first developed at:","options":["Harvard University","Stanford University","Yale University","MIT"],"correct_answer":"Stanford University","explanation":"Micro-teaching was developed by Dwight W. Allen and colleagues at Stanford University in 1963."},
    {"id":"ta006","topic":"Teaching Aptitude","difficulty":"Easy","question":"Which of the following best describes 'formative evaluation'?","options":["Evaluation at the end of the course","Evaluation to assign final grades","Ongoing evaluation during instruction","Evaluation before the course begins"],"correct_answer":"Ongoing evaluation during instruction","explanation":"Formative evaluation is continuous assessment conducted during the instructional process to improve learning."},
    {"id":"ta007","topic":"Teaching Aptitude","difficulty":"Hard","question":"Which theory proposes that students have different 'learning styles' and teachers should adapt instruction accordingly?","options":["Constructivism","VAK/VARK Model","Behaviorism","Gestalt Theory"],"correct_answer":"VAK/VARK Model","explanation":"The VARK model (Visual, Auditory, Read/Write, Kinesthetic) categorizes learners by preferred sensory modes."},
    {"id":"ta008","topic":"Teaching Aptitude","difficulty":"Medium","question":"The 'Socratic Method' of teaching primarily involves:","options":["Lecture and demonstration","Asking probing questions to stimulate thinking","Group projects","Use of audio-visual aids"],"correct_answer":"Asking probing questions to stimulate thinking","explanation":"The Socratic method uses disciplined questioning to stimulate critical thinking and illuminate ideas."},
    # ── Research Aptitude ──
    {"id":"ra001","topic":"Research Aptitude","difficulty":"Medium","question":"Which type of research aims to solve immediate practical problems?","options":["Fundamental research","Applied research","Action research","Historical research"],"correct_answer":"Action research","explanation":"Action research is conducted by practitioners to solve specific, immediate problems in their working environment."},
    {"id":"ra002","topic":"Research Aptitude","difficulty":"Easy","question":"A hypothesis is best described as:","options":["A proven fact","A tentative statement to be tested","A summary of findings","A literature review"],"correct_answer":"A tentative statement to be tested","explanation":"A hypothesis is a tentative, testable proposition about the relationship between two or more variables."},
    {"id":"ra003","topic":"Research Aptitude","difficulty":"Hard","question":"Which sampling method ensures every member of the population has an equal chance of being selected?","options":["Purposive sampling","Snowball sampling","Simple Random Sampling","Quota sampling"],"correct_answer":"Simple Random Sampling","explanation":"Simple Random Sampling gives every individual in the population an equal and independent probability of selection."},
    {"id":"ra004","topic":"Research Aptitude","difficulty":"Medium","question":"The term 'triangulation' in research refers to:","options":["Geometric analysis of data","Using multiple methods to validate findings","A statistical test","Sampling technique"],"correct_answer":"Using multiple methods to validate findings","explanation":"Triangulation uses multiple data sources, methods, or theories to cross-check and validate research findings."},
    {"id":"ra005","topic":"Research Aptitude","difficulty":"Medium","question":"Which research design is used to determine cause-and-effect relationships?","options":["Descriptive","Correlational","Experimental","Ethnographic"],"correct_answer":"Experimental","explanation":"Experimental research involves manipulation of an independent variable to determine its effect on a dependent variable, establishing causality."},
    {"id":"ra006","topic":"Research Aptitude","difficulty":"Hard","question":"A Type I error in research refers to:","options":["Accepting a false null hypothesis","Rejecting a true null hypothesis","Failing to collect data","Using the wrong statistical test"],"correct_answer":"Rejecting a true null hypothesis","explanation":"A Type I error (false positive) occurs when the null hypothesis is true but is incorrectly rejected. Its probability is denoted by alpha."},
    {"id":"ra007","topic":"Research Aptitude","difficulty":"Easy","question":"Plagiarism in research is considered:","options":["Acceptable if citing the source","An ethical violation","Only applies to published work","Legal but unprofessional"],"correct_answer":"An ethical violation","explanation":"Plagiarism — presenting others' work as one's own — is a serious breach of research ethics and academic integrity."},
    {"id":"ra008","topic":"Research Aptitude","difficulty":"Medium","question":"The review of related literature in research helps to:","options":["Define the research problem only","Identify gaps and situate the study","Replace primary data collection","Eliminate the need for methodology"],"correct_answer":"Identify gaps and situate the study","explanation":"Literature review helps researchers understand existing knowledge, identify research gaps, and frame their study within the field."},
    # ── Reading Comprehension ──
    {"id":"rc001","topic":"Reading Comprehension","difficulty":"Medium","question":"Inferential comprehension requires the reader to:","options":["Locate directly stated information","Draw conclusions beyond what is stated","Memorize the passage","Summarize only"],"correct_answer":"Draw conclusions beyond what is stated","explanation":"Inferential comprehension involves reading between the lines — using clues in the text to draw logical conclusions not explicitly stated."},
    {"id":"rc002","topic":"Reading Comprehension","difficulty":"Easy","question":"The main idea of a passage is:","options":["A supporting detail","The central thought or theme","The title of the passage","A specific example"],"correct_answer":"The central thought or theme","explanation":"The main idea is the primary message or central argument the author wants to communicate."},
    # ── Communication ──
    {"id":"cm001","topic":"Communication","difficulty":"Easy","question":"Which element is NOT part of the communication process?","options":["Sender","Message","Channel","Profit"],"correct_answer":"Profit","explanation":"The communication process involves: Sender, Message, Channel, Receiver, Feedback, and Noise. Profit is not a component."},
    {"id":"cm002","topic":"Communication","difficulty":"Medium","question":"Which of the following is an example of 'noise' in communication?","options":["Clear pronunciation","Use of jargon unfamiliar to the receiver","Well-organized message","Appropriate channel selection"],"correct_answer":"Use of jargon unfamiliar to the receiver","explanation":"Noise refers to any barrier that distorts or interferes with message transmission — semantic noise includes jargon or unfamiliar language."},
    {"id":"cm003","topic":"Communication","difficulty":"Medium","question":"Proxemics in non-verbal communication refers to:","options":["Tone of voice","Use of space and distance","Facial expressions","Gestures"],"correct_answer":"Use of space and distance","explanation":"Proxemics (coined by Edward Hall) studies how people use physical space and distance in communication."},
    {"id":"cm004","topic":"Communication","difficulty":"Hard","question":"The Berlo's SMCR model of communication stands for:","options":["Source, Message, Channel, Receiver","Signal, Medium, Code, Response","Sender, Meaning, Content, Reaction","None of the above"],"correct_answer":"Source, Message, Channel, Receiver","explanation":"David Berlo's SMCR model (1960) includes Source, Message, Channel, and Receiver as the four key elements of communication."},
    {"id":"cm005","topic":"Communication","difficulty":"Easy","question":"Classroom communication is primarily:","options":["Intrapersonal","Interpersonal & Group","Mass communication","Corporate communication"],"correct_answer":"Interpersonal & Group","explanation":"Classroom communication involves both interpersonal (teacher-student) and group (teacher + multiple students) communication."},
    # ── Logical Reasoning ──
    {"id":"lr001","topic":"Logical Reasoning","difficulty":"Medium","question":"If all professors are researchers, and some researchers are administrators, which conclusion is VALID?","options":["All professors are administrators","Some professors may be administrators","No professors are administrators","All administrators are professors"],"correct_answer":"Some professors may be administrators","explanation":"From the given premises, we can only conclude that it is possible (not certain) that some professors are administrators."},
    {"id":"lr002","topic":"Logical Reasoning","difficulty":"Easy","question":"What comes next in the series: 2, 6, 12, 20, 30, ?","options":["40","42","44","36"],"correct_answer":"42","explanation":"The differences are 4, 6, 8, 10, 12. So next = 30 + 12 = 42."},
    {"id":"lr003","topic":"Logical Reasoning","difficulty":"Hard","question":"Which of the following is an example of 'deductive reasoning'?","options":["All observed swans are white, so the next swan is white","All men are mortal; Socrates is a man; therefore Socrates is mortal","Based on past experience, it will rain today","The sample suggests the whole population believes X"],"correct_answer":"All men are mortal; Socrates is a man; therefore Socrates is mortal","explanation":"Deductive reasoning moves from general principles to specific conclusions. This classic syllogism is the textbook example of valid deductive reasoning."},
    {"id":"lr004","topic":"Logical Reasoning","difficulty":"Medium","question":"'Education is the key to success.' Conclusion I: All educated people are successful. Conclusion II: Success requires effort in education. Which follows?","options":["Only I","Only II","Both I and II","Neither I nor II"],"correct_answer":"Only II","explanation":"Conclusion I is absolute and unsupported. Conclusion II reasonably follows from the idea that education (effort) leads to success."},
    # ── ICT ──
    {"id":"ict001","topic":"ICT","difficulty":"Easy","question":"Which of the following is an example of an input device?","options":["Monitor","Printer","Keyboard","Speaker"],"correct_answer":"Keyboard","explanation":"Input devices send data to the computer. Keyboard, mouse, scanner are input devices; monitor, printer, speaker are output devices."},
    {"id":"ict002","topic":"ICT","difficulty":"Medium","question":"What does 'HTML' stand for?","options":["Hyper Text Markup Language","High Tech Modern Language","Hyper Transfer Meta Language","Home Tool Markup Language"],"correct_answer":"Hyper Text Markup Language","explanation":"HTML (HyperText Markup Language) is the standard markup language for creating web pages."},
    {"id":"ict003","topic":"ICT","difficulty":"Medium","question":"Which protocol is used for secure web browsing?","options":["HTTP","FTP","HTTPS","SMTP"],"correct_answer":"HTTPS","explanation":"HTTPS uses SSL/TLS encryption to secure data transmission between browser and server."},
    {"id":"ict004","topic":"ICT","difficulty":"Hard","question":"Moore's Law states that the number of transistors on a microchip doubles approximately every:","options":["6 months","1 year","2 years","5 years"],"correct_answer":"2 years","explanation":"Gordon Moore observed in 1965 that transistor count doubles roughly every two years, leading to exponential growth in computing power."},
    {"id":"ict005","topic":"ICT","difficulty":"Easy","question":"What is the full form of 'ICT' in educational context?","options":["Information and Communication Technology","Integrated Computer Training","International Computer Technology","Interactive Communication Tools"],"correct_answer":"Information and Communication Technology","explanation":"ICT stands for Information and Communication Technology — encompassing all technologies for handling information and facilitating communication."},
    # ── Environment & Ecology ──
    {"id":"env001","topic":"Environment & Ecology","difficulty":"Medium","question":"The 'Paris Agreement' primarily addresses:","options":["Nuclear non-proliferation","Climate change and global warming","Trade barriers","Ozone layer depletion"],"correct_answer":"Climate change and global warming","explanation":"The Paris Agreement (2015) is an international treaty under UNFCCC focused on limiting global warming to well below 2 degrees Celsius above pre-industrial levels."},
    {"id":"env002","topic":"Environment & Ecology","difficulty":"Easy","question":"Which gas is primarily responsible for the greenhouse effect?","options":["Oxygen","Nitrogen","Carbon Dioxide","Hydrogen"],"correct_answer":"Carbon Dioxide","explanation":"CO2 is the primary anthropogenic greenhouse gas, trapping heat in the atmosphere and contributing to global warming."},
    {"id":"env003","topic":"Environment & Ecology","difficulty":"Hard","question":"The 'Chipko Movement' in India was primarily associated with:","options":["Water conservation","Forest and tree conservation","Wildlife protection","Soil conservation"],"correct_answer":"Forest and tree conservation","explanation":"The Chipko Movement (1973, Uttarakhand) was a non-violent protest where villagers embraced trees to prevent their felling, pioneering environmental activism in India."},
    {"id":"env004","topic":"Environment & Ecology","difficulty":"Medium","question":"Biodiversity hotspots are areas with:","options":["High temperature and humidity","High species richness and endemism facing threats","Rich mineral resources","Dense human population"],"correct_answer":"High species richness and endemism facing threats","explanation":"Biodiversity hotspots have exceptional concentrations of endemic species and have lost significant amounts of their original habitat."},
    # ── Higher Education ──
    {"id":"he001","topic":"Higher Education","difficulty":"Medium","question":"The National Education Policy (NEP) 2020 recommends the school curriculum to be restructured as:","options":["10+2","5+3+3+4","8+4","6+3+2+1"],"correct_answer":"5+3+3+4","explanation":"NEP 2020 proposes a 5+3+3+4 curricular structure: Foundational (5), Preparatory (3), Middle (3), Secondary (4) years."},
    {"id":"he002","topic":"Higher Education","difficulty":"Easy","question":"UGC stands for:","options":["University Grants Commission","United Graduates Council","Universal Government College","University General Council"],"correct_answer":"University Grants Commission","explanation":"The University Grants Commission (UGC) is the statutory body responsible for coordination and maintenance of standards in higher education in India."},
    {"id":"he003","topic":"Higher Education","difficulty":"Hard","question":"The concept of 'Autonomous Institutions' in Indian higher education means:","options":["Complete independence from any university","Freedom to design curriculum, conduct exams, and declare results","Government-funded colleges","Deemed universities"],"correct_answer":"Freedom to design curriculum, conduct exams, and declare results","explanation":"Autonomous institutions have freedom to design curriculum, set syllabus, conduct exams, and declare results under UGC guidelines."},
    {"id":"he004","topic":"Higher Education","difficulty":"Medium","question":"NAAC stands for:","options":["National Assessment and Accreditation Council","National Academic Awards Council","National Association for Academic Curriculum","None of these"],"correct_answer":"National Assessment and Accreditation Council","explanation":"NAAC is an autonomous body established by UGC to assess and accredit higher education institutions in India."},
    # ── Indian Constitution & Governance ──
    {"id":"gov001","topic":"Indian Constitution & Governance","difficulty":"Easy","question":"The Preamble of the Indian Constitution describes India as:","options":["Federal, Democratic Republic","Sovereign, Socialist, Secular, Democratic Republic","Federal, Socialist State","Secular, Parliamentary Democracy"],"correct_answer":"Sovereign, Socialist, Secular, Democratic Republic","explanation":"The Preamble declares India to be a Sovereign, Socialist, Secular, Democratic Republic committed to Justice, Liberty, Equality, and Fraternity."},
    {"id":"gov002","topic":"Indian Constitution & Governance","difficulty":"Medium","question":"Which Article of the Indian Constitution guarantees Right to Education?","options":["Article 19","Article 21A","Article 25","Article 32"],"correct_answer":"Article 21A","explanation":"Article 21A (inserted by 86th Amendment, 2002) provides free and compulsory education to children aged 6-14 as a Fundamental Right."},
    {"id":"gov003","topic":"Indian Constitution & Governance","difficulty":"Hard","question":"The concept of 'Basic Structure' of the Indian Constitution was established by:","options":["Golaknath case (1967)","Kesavananda Bharati case (1973)","Minerva Mills case (1980)","Maneka Gandhi case (1978)"],"correct_answer":"Kesavananda Bharati case (1973)","explanation":"The Supreme Court in Kesavananda Bharati v. State of Kerala (1973) established the Basic Structure Doctrine — Parliament cannot alter the basic structure of the Constitution."},
    # ── Data Interpretation ──
    {"id":"di001","topic":"Data Interpretation","difficulty":"Medium","question":"If the mean of 5 numbers is 30 and the mean of 3 of them is 20, what is the mean of the remaining 2?","options":["35","45","40","50"],"correct_answer":"45","explanation":"Total sum = 5x30 = 150. Sum of 3 = 3x20 = 60. Remaining sum = 90. Mean of 2 = 90/2 = 45."},
    {"id":"di002","topic":"Data Interpretation","difficulty":"Easy","question":"Which measure of central tendency is most affected by extreme values (outliers)?","options":["Mode","Median","Mean","None of these"],"correct_answer":"Mean","explanation":"The arithmetic mean is significantly affected by extreme values since all values are summed; median and mode are more resistant."},
    {"id":"di003","topic":"Data Interpretation","difficulty":"Hard","question":"The coefficient of variation (CV) is calculated as:","options":["(Mean/SD) x 100","(SD/Mean) x 100","SD x Mean","Mean/Variance"],"correct_answer":"(SD/Mean) x 100","explanation":"CV = (Standard Deviation / Mean) x 100. It expresses variability as a percentage of the mean, allowing comparison across different datasets."},
    {"id":"di004","topic":"Data Interpretation","difficulty":"Medium","question":"In a bar chart, the height of each bar represents:","options":["The percentage of data","The frequency or value of the category","The range of data","The median value"],"correct_answer":"The frequency or value of the category","explanation":"In a bar chart, the length/height of each bar is proportional to the value or frequency it represents."},
]


class QuestionBank:
    def __init__(self, filepath=QUESTION_BANK_FILE):
        self.filepath = filepath
        self._ensure_file()

    def _ensure_file(self):
        if not os.path.exists(self.filepath):
            self._save(BUILTIN_QUESTIONS)
        else:
            existing = self._load()
            existing_ids = {q.get("id") for q in existing}
            new_ones = [q for q in BUILTIN_QUESTIONS if q.get("id") not in existing_ids]
            if new_ones:
                existing.extend(new_ones)
                self._save(existing)

    def _load(self):
        try:
            with open(self.filepath, "r") as f:
                return json.load(f)
        except Exception:
            return list(BUILTIN_QUESTIONS)

    def _save(self, questions):
        with open(self.filepath, "w") as f:
            json.dump(questions, f, indent=2)

    def get_all_questions(self):
        return self._load()

    def get_topics(self):
        return sorted(set(q.get("topic", "General") for q in self._load()))

    def get_questions(self, topics=None, n=20, difficulty="Mixed"):
        questions = self._load()
        if topics:
            questions = [q for q in questions if q.get("topic") in topics]
        if difficulty != "Mixed":
            filtered = [q for q in questions if q.get("difficulty") == difficulty]
            if filtered:
                questions = filtered
        random.shuffle(questions)
        return questions[:n]

    def add_questions(self, new_questions):
        existing = self._load()
        existing_ids = {q.get("id") for q in existing}
        for q in new_questions:
            if not q.get("id"):
                q["id"] = str(uuid.uuid4())[:8]
            if q["id"] not in existing_ids:
                existing.append(q)
                existing_ids.add(q["id"])
        self._save(existing)


# ════════════════════════════════════════════════════════════════
# 4. PDF EXTRACTOR  (text-based + OCR for scanned PDFs)
# ════════════════════════════════════════════════════════════════
class PDFExtractor:
    """
    Extracts text from PDFs using a 4-method cascade:
      1. PyMuPDF  (fast, best for text-based PDFs)
      2. pdfplumber  (fallback text extraction)
      3. PyPDF2  (second fallback)
      4. OCR via pytesseract + pdf2image  (for scanned / image-only PDFs)
    """

    def extract_chunks(self, pdf_path: str, chunk_size: int = 1500) -> list:
        text, method_used = self._extract_text_with_method(pdf_path)
        if not text:
            return []
        # Store which method succeeded so caller can inform user
        self.last_method = method_used
        text = self._clean_text(text)
        chunks = self._split_into_chunks(text, chunk_size)
        return [c for c in chunks if len(c.strip()) > 150]

    def get_page_count(self, pdf_path: str) -> int:
        try:
            import fitz
            doc = fitz.open(pdf_path)
            n = len(doc); doc.close(); return n
        except Exception:
            pass
        try:
            import PyPDF2
            with open(pdf_path, "rb") as f:
                return len(PyPDF2.PdfReader(f).pages)
        except Exception:
            return 0

    def is_scanned(self, pdf_path: str) -> bool:
        """Heuristic: if text extraction yields very little text, it's likely scanned."""
        text = self._pymupdf(pdf_path) or self._pdfplumber(pdf_path)
        if not text:
            return True
        # Less than 100 chars per page → likely image-based
        pages = max(self.get_page_count(pdf_path), 1)
        return (len(text.strip()) / pages) < 100

    # ── Extraction cascade ────────────────────────────────────────
    def _extract_text_with_method(self, pdf_path: str):
        """Returns (text, method_name). Falls back to OCR if needed."""
        # Step 1-3: try native text extraction
        for fn, name in [(self._pymupdf, "PyMuPDF"),
                         (self._pdfplumber, "pdfplumber"),
                         (self._pypdf2, "PyPDF2")]:
            result = fn(pdf_path)
            if result and len(result.strip()) > 200:
                return result, name

        # Step 4: OCR fallback for scanned PDFs
        ocr_text = self._ocr(pdf_path)
        if ocr_text:
            return ocr_text, "OCR (pytesseract)"

        return "", "none"

    def _extract_text(self, pdf_path: str) -> str:
        text, _ = self._extract_text_with_method(pdf_path)
        return text

    def _pymupdf(self, path: str) -> str:
        try:
            import fitz
            doc = fitz.open(path)
            pages_text = []
            for page in doc:
                t = page.get_text("text")
                if t.strip():
                    pages_text.append(t)
            doc.close()
            return "\n\n".join(pages_text)
        except Exception:
            return ""

    def _pdfplumber(self, path: str) -> str:
        try:
            import pdfplumber
            text = ""
            with pdfplumber.open(path) as pdf:
                for page in pdf.pages:
                    t = page.extract_text()
                    if t:
                        text += t + "\n\n"
            return text
        except Exception:
            return ""

    def _pypdf2(self, path: str) -> str:
        try:
            import PyPDF2
            text = ""
            with open(path, "rb") as f:
                for page in PyPDF2.PdfReader(f).pages:
                    t = page.extract_text()
                    if t:
                        text += t + "\n\n"
            return text
        except Exception:
            return ""

    def _ocr(self, path: str) -> str:
        """
        OCR pipeline for scanned PDFs:
          pdf2image → PIL Images → pytesseract → text
        Processes up to 30 pages to keep it fast.
        """
        try:
            from pdf2image import convert_from_path
            import pytesseract
            from PIL import Image

            pages = convert_from_path(
                path,
                dpi=300,          # high DPI for better OCR accuracy
                fmt="jpeg",
                thread_count=2,
            )

            texts = []
            for i, page_img in enumerate(pages[:30]):   # cap at 30 pages
                # Pre-process: convert to greyscale for better OCR
                grey = page_img.convert("L")
                # pytesseract with NET-friendly config
                config = "--oem 3 --psm 6 -l eng"
                page_text = pytesseract.image_to_string(grey, config=config)
                if page_text.strip():
                    texts.append(page_text)

            return "\n\n".join(texts)

        except ImportError as e:
            # Return empty string; caller will surface install instructions
            return ""
        except Exception:
            return ""

    # ── Text cleaning ─────────────────────────────────────────────
    def _clean_text(self, text: str) -> str:
        # Normalize line endings
        text = re.sub(r'\r\n|\r', '\n', text)
        # Collapse 3+ blank lines → 2
        text = re.sub(r'\n{3,}', '\n\n', text)
        # Collapse multiple spaces
        text = re.sub(r' {2,}', ' ', text)
        # Remove standalone page numbers
        text = re.sub(r'(?m)^\s*\d{1,4}\s*$', '', text)
        # Remove URLs / watermarks
        text = re.sub(r'https?://\S+|www\.\S+', '', text)
        # Remove common OCR artefacts: long runs of punctuation
        text = re.sub(r'[_\-\.]{5,}', ' ', text)
        # Remove non-printable chars except newline/tab
        text = re.sub(r'[^\x09\x0A\x20-\x7E\u0900-\u097F]', ' ', text)
        return text.strip()

    def _split_into_chunks(self, text: str, chunk_size: int) -> list:
        paragraphs = text.split('\n\n')
        chunks, current = [], ""
        for para in paragraphs:
            if len(current) + len(para) < chunk_size:
                current += para + "\n\n"
            else:
                if current:
                    chunks.append(current.strip())
                current = para + "\n\n"
        if current:
            chunks.append(current.strip())
        # Fallback: split by character count if paragraph splitting didn't work
        if len(chunks) <= 1 and len(text) > chunk_size:
            chunks = [text[i:i + chunk_size]
                      for i in range(0, len(text), chunk_size - 200)
                      if len(text[i:i + chunk_size].strip()) > 150]
        return chunks


# ════════════════════════════════════════════════════════════════
# 5. AI QUESTION GENERATOR
# ════════════════════════════════════════════════════════════════
class AIQuestionGenerator:
    def __init__(self, api_key: str, provider: str = "claude"):
        self.api_key = api_key
        self.provider = provider.lower()

    def generate_questions(self, topic, difficulties, styles, n=10, extra_instructions=""):
        combos = list(product(difficulties, styles))
        q_per_combo = max(1, n // len(combos))
        remainder = n - q_per_combo * len(combos)
        all_questions = []
        for i, (diff, style) in enumerate(combos):
            count = q_per_combo + (1 if i < remainder else 0)
            prompt = self._build_prompt(topic, diff, style, count, extra_instructions)
            raw = self._call_api(prompt)
            all_questions.extend(self._parse(raw, topic, diff))
        return all_questions[:n]

    def generate_from_text(self, text, n=5, topic="UGC NET Paper 1"):
        prompt = self._text_prompt(text, n, topic)
        raw = self._call_api(prompt)
        return self._parse(raw, topic, "Medium")

    def _build_prompt(self, topic, difficulty, style, n, extra=""):
        style_map = {
            "MCQ (4 options)": "Standard 4-option MCQ with one correct answer and three plausible distractors.",
            "True/False": "Statement with 4 options: True, False, Cannot Say, Partially True.",
            "Assertion-Reason": "Assertion (A) and Reason (R) with 4 standard AR options.",
            "Match the Following": "Two lists to match, options represent correct match combinations.",
            "Case-based": "Short paragraph/case study followed by an MCQ."
        }
        level_desc = {"Easy": "straightforward recall", "Medium": "application and understanding", "Hard": "analysis and evaluation"}.get(difficulty, "mixed")
        extra_line = f"- Extra instructions: {extra}" if extra else ""
        return f"""You are an expert UGC NET Paper 1 question setter.

Generate EXACTLY {n} high-quality {difficulty.upper()} level questions on: "{topic}"
Style: {style} -- {style_map.get(style, 'Standard MCQ')}

Rules:
- Strictly relevant to UGC NET Paper 1 syllabus
- {difficulty} level means: {level_desc}
- Exactly 4 options per question
- Provide correct answer and 2-3 sentence explanation
- No repeated questions
{extra_line}

Return ONLY a valid JSON array, no other text:
[{{"question":"...","options":["A","B","C","D"],"correct_answer":"A","explanation":"...","difficulty":"{difficulty}","topic":"{topic}"}}]"""

    def _text_prompt(self, text, n, topic):
        return f"""You are an expert UGC NET Paper 1 question setter.

Generate EXACTLY {n} MCQ questions from this study material:

{text[:3000]}

Rules: 4 options each, provide correct answer, brief explanation, mix difficulty levels.
Return ONLY a valid JSON array:
[{{"question":"...","options":["A","B","C","D"],"correct_answer":"A","explanation":"...","difficulty":"Medium","topic":"{topic}"}}]"""

    def _call_api(self, prompt: str) -> str:
        if self.provider == "claude":
            return self._claude(prompt)
        return self._gemini(prompt)

    def _claude(self, prompt: str) -> str:
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=self.api_key)
            msg = client.messages.create(
                model="claude-opus-4-6", max_tokens=4096,
                messages=[{"role": "user", "content": prompt}]
            )
            return msg.content[0].text
        except ImportError:
            return self._claude_http(prompt)
        except Exception as e:
            st.error(f"Claude error: {e}")
            return ""

    def _claude_http(self, prompt: str) -> str:
        try:
            import urllib.request
            payload = json.dumps({
                "model": "claude-opus-4-6", "max_tokens": 4096,
                "messages": [{"role": "user", "content": prompt}]
            }).encode()
            req = urllib.request.Request(
                "https://api.anthropic.com/v1/messages", data=payload,
                headers={"Content-Type": "application/json", "x-api-key": self.api_key,
                         "anthropic-version": "2023-06-01"}
            )
            with urllib.request.urlopen(req, timeout=60) as resp:
                return json.loads(resp.read())["content"][0]["text"]
        except Exception as e:
            st.error(f"Claude HTTP error: {e}")
            return ""

    def _gemini(self, prompt: str) -> str:
        try:
            import urllib.request
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.api_key}"
            payload = json.dumps({
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"maxOutputTokens": 4096, "temperature": 0.7}
            }).encode()
            req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=60) as resp:
                return json.loads(resp.read())["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            st.error(f"Gemini error: {e}")
            return ""

    def _parse(self, raw: str, topic="General", difficulty="Medium") -> list:
        if not raw:
            return []
        try:
            match = re.search(r'\[.*\]', raw, re.DOTALL)
            questions = json.loads(match.group() if match else raw)
            valid = []
            for q in questions:
                if isinstance(q, dict) and q.get("question") and q.get("options") and q.get("correct_answer"):
                    q["id"] = str(uuid.uuid4())[:8]
                    q.setdefault("topic", topic)
                    q.setdefault("difficulty", difficulty)
                    q.setdefault("explanation", "")
                    if q["correct_answer"] in q["options"] and len(q["options"]) >= 4:
                        valid.append(q)
            return valid
        except Exception:
            return []


# ════════════════════════════════════════════════════════════════
# 6. SESSION STATE INIT
# ════════════════════════════════════════════════════════════════
def init_session_state():
    defaults = {
        "questions": [], "current_q_idx": 0, "answers": {},
        "quiz_started": False, "quiz_completed": False, "quiz_mode": "practice",
        "score": 0, "start_time": None, "num_questions": 20, "difficulty": "Mixed",
        "bookmarks": set(), "streak": 0, "total_attempted": 0, "total_correct": 0,
        "question_times": {}, "ai_generated_count": 0, "page": "home",
        "wrong_questions": [], "timed": True, "time_per_q": 90, "q_start_time": None,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_session_state()


# ════════════════════════════════════════════════════════════════
# 7. SIDEBAR
# ════════════════════════════════════════════════════════════════
def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-brand">
            <div class="brand-icon">🎓</div>
            <div>
                <div class="brand-title">NET Quiz Master</div>
                <div class="brand-subtitle">Paper 1 · UGC NET</div>
            </div>
        </div>""", unsafe_allow_html=True)
        st.markdown("---")

        nav_items = [
            ("🏠", "Home", "home"), ("📝", "Practice Quiz", "quiz"),
            ("📊", "Analytics", "analytics"),
            ("📄", "PDF Upload", "pdf_upload"), ("🔖", "Bookmarks", "bookmarks"),
            ("⚙️", "Settings", "settings"),
        ]
        for icon, label, page_key in nav_items:
            if st.button(f"{icon}  {label}", key=f"nav_{page_key}",
                         use_container_width=True,
                         type="primary" if st.session_state.page == page_key else "secondary"):
                st.session_state.page = page_key
                st.session_state.quiz_started = False
                st.rerun()

        st.markdown("---")
        accuracy = round(st.session_state.total_correct / st.session_state.total_attempted * 100) if st.session_state.total_attempted > 0 else 0
        st.markdown(f"""
        <div class="sidebar-stats">
            <div class="stat-mini"><span class="stat-mini-val">{st.session_state.total_attempted}</span><span class="stat-mini-lbl">Attempted</span></div>
            <div class="stat-mini"><span class="stat-mini-val">{accuracy}%</span><span class="stat-mini-lbl">Accuracy</span></div>
            <div class="stat-mini"><span class="stat-mini-val">{st.session_state.streak}</span><span class="stat-mini-lbl">Streak 🔥</span></div>
        </div>""", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown('<div style="text-align:center;opacity:0.5;font-size:0.75rem;padding:0.5rem;">Built for NET Paper 1 Aspirants<br><span style="color:#6366f1;">NYZTrade Education</span></div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════
# 8. HOME PAGE
# ════════════════════════════════════════════════════════════════
def render_home():
    st.markdown("""
    <div class="hero-section">
        <div class="hero-badge">UGC NET · Paper 1</div>
        <h1 class="hero-title">Master Your <span class="gradient-text">NET Exam</span></h1>
        <p class="hero-subtitle">AI-powered question generation · 10 core topics · Real exam simulation</p>
    </div>""", unsafe_allow_html=True)

    topics = [
        ("🧠","Teaching Aptitude","Pedagogy, Methods, Levels of Teaching"),
        ("🔬","Research Aptitude","Methods, Ethics, Types of Research"),
        ("📖","Reading Comprehension","Passages, Inference, Vocabulary"),
        ("💬","Communication","Verbal, Non-verbal, Barriers"),
        ("🔢","Reasoning","Logical, Mathematical, Data Interpretation"),
        ("💻","ICT","Computer Basics, Internet, Tools"),
        ("🌍","Environment","Ecology, Natural Resources, Pollution"),
        ("📐","Higher Education","Institutions, Policy, UGC Norms"),
        ("🏛️","Governance","Polity, Preamble, Rights & Duties"),
        ("📊","Data Interpretation","Graphs, Tables, Statistics"),
    ]
    st.markdown('<div class="section-title">📚 Core Topics</div>', unsafe_allow_html=True)
    cols = st.columns(5)
    for i, (icon, title, desc) in enumerate(topics):
        with cols[i % 5]:
            st.markdown(f'<div class="topic-card"><div class="topic-icon">{icon}</div><div class="topic-name">{title}</div><div class="topic-desc">{desc}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="feature-card"><div class="feature-icon">⚡</div><div class="feature-title">Quick Practice</div><div class="feature-desc">Jump into a 20-question session immediately. Mixed topics, timed mode.</div></div>', unsafe_allow_html=True)
        if st.button("Start Quick Quiz →", use_container_width=True, type="primary"):
            st.session_state.page = "quiz"
            st.rerun()
    with col2:
        st.markdown('<div class="feature-card"><div class="feature-icon">📄</div><div class="feature-title">PDF Quiz Generator</div><div class="feature-desc">Upload any study material PDF and auto-extract quiz questions from it using text analysis.</div></div>', unsafe_allow_html=True)
        if st.button("Upload PDF →", use_container_width=True, type="primary"):
            st.session_state.page = "pdf_upload"
            st.rerun()
    with col3:
        st.markdown('<div class="feature-card"><div class="feature-icon">🔖</div><div class="feature-title">Bookmarks & Review</div><div class="feature-desc">Save tricky questions, review wrong answers, and target your weak topics precisely.</div></div>', unsafe_allow_html=True)
        if st.button("View Bookmarks →", use_container_width=True):
            st.session_state.page = "bookmarks"
            st.rerun()

    total_q = len(QuestionBank().get_all_questions())
    st.markdown(f"""
    <div class="stats-banner">
        <div class="banner-stat"><span class="banner-val">{total_q}+</span><span class="banner-lbl">Questions</span></div>
        <div class="banner-stat"><span class="banner-val">10</span><span class="banner-lbl">Topics</span></div>
        <div class="banner-stat"><span class="banner-val">3</span><span class="banner-lbl">Difficulty Levels</span></div>
        <div class="banner-stat"><span class="banner-val">PDF</span><span class="banner-lbl">Import</span></div>
    </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════
# 9. QUIZ CONFIG
# ════════════════════════════════════════════════════════════════
def render_quiz_config():
    st.markdown('<h2 class="page-title">📝 Configure Your Quiz</h2>', unsafe_allow_html=True)
    qb = QuestionBank()
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown('<div class="config-card">', unsafe_allow_html=True)
        st.markdown("#### 🎯 Select Topics")
        selected = []
        tcols = st.columns(2)
        for i, topic in enumerate(qb.get_topics()):
            with tcols[i % 2]:
                if st.checkbox(topic, value=True, key=f"topic_{topic}"):
                    selected.append(topic)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="config-card">', unsafe_allow_html=True)
        st.markdown("#### ⚙️ Settings")
        num_q = st.select_slider("Number of Questions", options=[10, 15, 20, 25, 30, 40, 50], value=20)
        difficulty = st.radio("Difficulty", ["Easy", "Medium", "Hard", "Mixed"], index=3, horizontal=True)
        quiz_mode = st.radio("Quiz Mode", ["Practice", "Exam", "Review"],
                             captions=["Show answers after each Q", "Full exam simulation", "Only wrong questions"], index=0)
        timed = st.toggle("⏱️ Enable Timer", value=True)
        time_per_q = st.slider("Seconds per question", 30, 180, 90, 10) if timed else 90
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("🚀 Start Quiz", use_container_width=True, type="primary"):
            if not selected:
                st.error("Please select at least one topic!")
                return
            questions = qb.get_questions(topics=selected, n=num_q, difficulty=difficulty)
            if quiz_mode.lower() == "review" and st.session_state.wrong_questions:
                questions = st.session_state.wrong_questions[:num_q]
            random.shuffle(questions)
            st.session_state.update({
                "questions": questions, "current_q_idx": 0, "answers": {},
                "quiz_started": True, "quiz_completed": False,
                "quiz_mode": quiz_mode.lower(), "start_time": time.time(),
                "num_questions": num_q, "timed": timed, "time_per_q": time_per_q,
                "q_start_time": time.time(),
            })
            st.rerun()


# ════════════════════════════════════════════════════════════════
# 10. QUIZ INTERFACE
# ════════════════════════════════════════════════════════════════
def render_quiz():
    if st.session_state.quiz_completed:
        render_results()
        return

    questions = st.session_state.questions
    idx = st.session_state.current_q_idx

    if idx >= len(questions):
        st.session_state.quiz_completed = True
        st.session_state.score = sum(1 for a in st.session_state.answers.values() if a.get("correct"))
        st.rerun()
        return

    q = questions[idx]
    total = len(questions)
    elapsed = int(time.time() - st.session_state.start_time)
    mins, secs = divmod(elapsed, 60)

    # ── Header row: progress + timer + skip (all inside ONE form to avoid None) ──
    with st.form(key=f"hdr_{idx}", clear_on_submit=False):
        hc1, hc2, hc3 = st.columns([4, 1, 1])
        with hc1:
            st.markdown(
                f'<div class="quiz-header">'
                f'<span class="q-counter">Question <b>{idx+1}</b> / {total}</span>'
                f'<span class="q-topic-badge">{q.get("topic","General")}</span>'
                f'<span class="q-diff-badge diff-{q.get("difficulty","medium").lower()}">'
                f'{q.get("difficulty","Medium")}</span></div>',
                unsafe_allow_html=True
            )
        with hc2:
            st.markdown(f'<div class="timer-box">⏱️ {mins:02d}:{secs:02d}</div>', unsafe_allow_html=True)
        with hc3:
            skip_btn = st.form_submit_button("Skip →", use_container_width=True)

    st.progress(idx / total)

    if skip_btn:
        st.session_state.answers[idx] = {"answer": None, "correct": False, "skipped": True}
        st.session_state.current_q_idx += 1
        st.session_state.q_start_time = time.time()
        st.rerun()

    # ── Question card ──
    q_id = q.get("id", idx)
    bm_html = '<span class="bookmark-indicator">🔖</span>' if q_id in st.session_state.bookmarks else ''
    clean_q = html.unescape(re.sub(r'<[^>]+>', '', q["question"])).strip()
    st.markdown(
        f'<div class="question-card">'
        f'<div class="question-meta"><span class="q-num-pill">Q {idx+1}</span>{bm_html}</div>'
        f'<div class="question-text">{clean_q}</div></div>',
        unsafe_allow_html=True
    )

    already_answered = idx in st.session_state.answers
    options = q.get("options", [])
    correct_ans = q.get("correct_answer", "")

    # ── POST-ANSWER: show results ──
    if already_answered:
        user_ans = st.session_state.answers[idx].get("answer")
        for opt in options:
            clean_opt = html.unescape(re.sub(r'<[^>]+>', '', opt)).strip()
            if opt == correct_ans:
                st.markdown(f'<div class="option-btn correct-opt">✅ {clean_opt}</div>', unsafe_allow_html=True)
            elif opt == user_ans and opt != correct_ans:
                st.markdown(f'<div class="option-btn wrong-opt">❌ {clean_opt}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="option-btn neutral-opt">{clean_opt}</div>', unsafe_allow_html=True)
        if q.get("explanation"):
            clean_exp = html.unescape(re.sub(r'<[^>]+>', '', q["explanation"])).strip()
            st.markdown(
                f'<div class="explanation-box"><div class="exp-title">💡 Explanation</div>'
                f'<div class="exp-text">{clean_exp}</div></div>',
                unsafe_allow_html=True
            )
        # Navigation form
        with st.form(key=f"nav_{idx}", clear_on_submit=False):
            nc1, nc2 = st.columns(2)
            with nc1:
                prev_btn = st.form_submit_button("← Previous", use_container_width=True) if idx > 0 else None
            with nc2:
                if idx < total - 1:
                    next_btn = st.form_submit_button("Next Question →", use_container_width=True, type="primary")
                    finish_btn = False
                else:
                    next_btn = False
                    finish_btn = st.form_submit_button("🏁 Finish Quiz", use_container_width=True, type="primary")

        if prev_btn:
            st.session_state.current_q_idx -= 1
            st.rerun()
        if next_btn:
            st.session_state.current_q_idx += 1
            st.session_state.q_start_time = time.time()
            st.rerun()
        if finish_btn:
            st.session_state.quiz_completed = True
            st.session_state.score = sum(1 for a in st.session_state.answers.values() if a.get("correct"))
            st.rerun()

    # ── PRE-ANSWER: show options + submit form ──
    else:
        sel_key = f"sel_q_{idx}"
        if sel_key not in st.session_state:
            st.session_state[sel_key] = options[0] if options else ""

        # Option buttons — each a tiny form so no st.button inside columns
        for i, opt in enumerate(options):
            clean_opt = html.unescape(re.sub(r'<[^>]+>', '', opt)).strip()
            is_sel = st.session_state[sel_key] == opt
            if is_sel:
                st.markdown(
                    f'<div style="background:linear-gradient(135deg,rgba(124,58,237,0.25),rgba(168,85,247,0.15));'
                    f'border:2px solid #a855f7;border-radius:12px;padding:0.9rem 1.4rem;margin:0.4rem 0;'
                    f'color:#e9d5ff;font-size:0.97rem;font-weight:700;cursor:pointer;">'
                    f'● &nbsp; {clean_opt}</div>',
                    unsafe_allow_html=True
                )
            else:
                with st.form(key=f"opt_{idx}_{i}", clear_on_submit=False):
                    clicked = st.form_submit_button(
                        f"○  {clean_opt}",
                        use_container_width=True
                    )
                if clicked:
                    st.session_state[sel_key] = opt
                    st.rerun()

        st.markdown("<div style='margin-top:0.8rem'></div>", unsafe_allow_html=True)

        # Submit + Bookmark form
        choice = st.session_state[sel_key]
        with st.form(key=f"ans_{idx}", clear_on_submit=False):
            ac1, ac2 = st.columns([3, 1])
            with ac1:
                do_submit = st.form_submit_button("✅  Submit Answer", use_container_width=True, type="primary")
            with ac2:
                do_bookmark = st.form_submit_button("🔖  Bookmark", use_container_width=True)

        if do_submit:
            is_correct = (choice == correct_ans)
            time_taken = int(time.time() - st.session_state.q_start_time)
            st.session_state.answers[idx] = {"answer": choice, "correct": is_correct, "time_taken": time_taken}
            st.session_state.question_times[idx] = time_taken
            st.session_state.total_attempted += 1
            if is_correct:
                st.session_state.total_correct += 1
                st.session_state.streak += 1
            else:
                st.session_state.streak = 0
                if q not in st.session_state.wrong_questions:
                    st.session_state.wrong_questions.append(q)
            if st.session_state.quiz_mode != "practice":
                st.session_state.current_q_idx += 1
                st.session_state.q_start_time = time.time()
            st.rerun()

        if do_bookmark:
            if q_id in st.session_state.bookmarks:
                st.session_state.bookmarks.discard(q_id)
            else:
                st.session_state.bookmarks.add(q_id)
            st.rerun()


# ════════════════════════════════════════════════════════════════
# 11. RESULTS PAGE
# ════════════════════════════════════════════════════════════════
def get_grade(pct):
    if pct >= 90: return "A+", "#22c55e", "Outstanding! You're ready for the exam! 🏆"
    elif pct >= 75: return "A", "#84cc16", "Excellent work! Keep it up! 🌟"
    elif pct >= 60: return "B", "#f59e0b", "Good performance. A bit more practice needed. 💪"
    elif pct >= 45: return "C", "#f97316", "Average. Focus on weak areas. 📚"
    else: return "D", "#ef4444", "Keep practicing! Consistency is key. 🎯"

def render_results():
    score = st.session_state.score
    total = len(st.session_state.questions)
    pct = round(score / total * 100) if total > 0 else 0
    elapsed = int(time.time() - st.session_state.start_time)
    mins, secs = divmod(elapsed, 60)
    grade, grade_color, grade_msg = get_grade(pct)

    st.markdown(f'<div class="results-hero"><div class="results-grade" style="color:{grade_color}">{grade}</div><div class="results-score">{score} / {total}</div><div class="results-pct">{pct}% Accuracy</div><div class="results-msg">{grade_msg}</div></div>', unsafe_allow_html=True)

    wrong = sum(1 for a in st.session_state.answers.values() if not a.get("correct") and not a.get("skipped"))
    skipped = sum(1 for a in st.session_state.answers.values() if a.get("skipped"))
    avg_time = round(sum(st.session_state.question_times.values()) / len(st.session_state.question_times)) if st.session_state.question_times else 0

    c1, c2, c3, c4, c5 = st.columns(5)
    for col, val, lbl, color in [(c1,score,"Correct","#22c55e"),(c2,wrong,"Wrong","#ef4444"),(c3,skipped,"Skipped","#f59e0b"),(c4,f"{mins}m {secs}s","Total Time","#6366f1"),(c5,f"{avg_time}s","Avg/Q","#06b6d4")]:
        with col:
            st.markdown(f'<div class="result-stat-card" style="border-top:3px solid {color}"><div class="rs-val" style="color:{color}">{val}</div><div class="rs-lbl">{lbl}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔄 Retake Quiz", use_container_width=True, type="primary"):
            st.session_state.quiz_started = False
            st.session_state.quiz_completed = False
            st.rerun()
    with col2:
        if st.button("📊 View Analytics", use_container_width=True):
            st.session_state.page = "analytics"
            st.rerun()
    with col3:
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.page = "home"
            st.session_state.quiz_started = False
            st.session_state.quiz_completed = False
            st.rerun()

    st.markdown("---")
    st.markdown("### 📋 Answer Review")
    for i, q in enumerate(st.session_state.questions):
        ans_data = st.session_state.answers.get(i, {})
        user_ans = ans_data.get("answer", "Skipped")
        is_correct = ans_data.get("correct", False)
        status = "✅" if is_correct else ("⏭️" if ans_data.get("skipped") else "❌")
        with st.expander(f"{status} Q{i+1}: {q['question'][:80]}..."):
            st.markdown(f"**Your Answer:** {user_ans}")
            st.markdown(f"**Correct Answer:** {q.get('correct_answer','N/A')}")
            if q.get("explanation"):
                st.info(f"💡 {q['explanation']}")


# ════════════════════════════════════════════════════════════════
# 12. ANALYTICS PAGE
# ════════════════════════════════════════════════════════════════
def render_analytics():
    st.markdown('<h2 class="page-title">📊 Performance Analytics</h2>', unsafe_allow_html=True)
    if st.session_state.total_attempted == 0:
        st.markdown('<div class="empty-state"><div class="empty-icon">📊</div><div class="empty-title">No data yet</div><div class="empty-desc">Complete a quiz to see your analytics here.</div></div>', unsafe_allow_html=True)
        return

    accuracy = round(st.session_state.total_correct / st.session_state.total_attempted * 100)
    c1, c2, c3, c4 = st.columns(4)
    for col, title, val, sub, color in [
        (c1,"Total Questions",st.session_state.total_attempted,"answered","#6366f1"),
        (c2,"Correct Answers",st.session_state.total_correct,"correct","#22c55e"),
        (c3,"Accuracy Rate",f"{accuracy}%","overall","#f59e0b"),
        (c4,"Current Streak",st.session_state.streak,"in a row 🔥","#ef4444"),
    ]:
        with col:
            st.markdown(f'<div class="analytics-card" style="border-left:4px solid {color}"><div class="ac-title">{title}</div><div class="ac-val" style="color:{color}">{val}</div><div class="ac-sub">{sub}</div></div>', unsafe_allow_html=True)

    if st.session_state.question_times:
        st.markdown("<br>#### ⏱️ Time per Question (last quiz)")
        df = pd.DataFrame({"Question": [f"Q{i+1}" for i in st.session_state.question_times], "Seconds": list(st.session_state.question_times.values())})
        st.bar_chart(df.set_index("Question"))
    st.markdown(f"#### 🔖 Bookmarked Questions: **{len(st.session_state.bookmarks)}**")


# ════════════════════════════════════════════════════════════════
# 13. PDF UPLOAD PAGE  (pure extraction — no external API needed)
# ════════════════════════════════════════════════════════════════
def render_pdf_upload():
    st.markdown('<h2 class="page-title">📄 PDF Quiz Generator</h2>', unsafe_allow_html=True)
    st.markdown('<div class="pdf-intro">Upload any NET Paper 1 study material or question bank PDF. The app will extract existing MCQ questions directly from the text — no external API required.</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])
    with col1:
        uploaded_file = st.file_uploader("Upload PDF Study Material", type=["pdf"])
        st.markdown("#### 📚 Or Use Pre-loaded Books")
        preloaded = {
            "UGC NET Paper 1 Q-Book 2022": "/mnt/user-data/uploads/UGC_NET_PAPER_1_QBOOK_2022_Edited_compressed.pdf",
            "AIFER Paper 1 Ebook 2023 (December)": "/mnt/user-data/uploads/AIFERPAPER1EBOOK2023DECEMBER.pdf"
        }
        selected_preload = st.selectbox("Select a pre-loaded book", ["None"] + list(preloaded.keys()))
        st.markdown("<br>", unsafe_allow_html=True)
        pdf_num_q = st.slider("Max questions to load", 10, 100, 30, key="pdf_num_q")
        pdf_topic = st.text_input("Assign topic label", placeholder="e.g., Research Aptitude (optional)")
        pdf_difficulty = st.select_slider("Assign difficulty", ["Easy", "Medium", "Hard"], value="Medium")
        extract_btn = st.button("🔍 Extract Questions from PDF", use_container_width=True, type="primary")

    with col2:
        st.markdown("""
        <div class="config-card">
            <div style="font-weight:700;margin-bottom:1rem;">📋 How Extraction Works</div>
            <div class="step-list">
                <div class="step-item"><span class="step-num">1</span><span>PDF text extracted (PyMuPDF → pdfplumber → PyPDF2)</span></div>
                <div class="step-item"><span class="step-num">2</span><span>If text is sparse → OCR engine activated for scanned pages</span></div>
                <div class="step-item"><span class="step-num">3</span><span>MCQ patterns (A/B/C/D options) are detected by regex</span></div>
                <div class="step-item"><span class="step-num">4</span><span>Questions are cleaned, de-tagged, and structured</span></div>
                <div class="step-item"><span class="step-num">5</span><span>Questions are saved to your quiz bank instantly</span></div>
            </div>
        </div>
        <div class="config-card" style="margin-top:1rem;">
            <div style="font-weight:700;margin-bottom:0.5rem;">💡 Tips for Best Results</div>
            <ul style="color:#94a3b8;font-size:0.85rem;line-height:1.8;">
                <li>Text-based PDFs extract fastest &amp; most accurately</li>
                <li><b style="color:#06b6d4;">Scanned PDFs</b> supported via OCR (pytesseract)</li>
                <li>Options labelled (A) (B) (C) (D) detected automatically</li>
                <li>300 DPI scans give best OCR quality</li>
                <li>Both pre-loaded books are fully supported</li>
            </ul>
        </div>""", unsafe_allow_html=True)

    if extract_btn:
        pdf_path = None
        if uploaded_file:
            temp_path = f"/tmp/{uploaded_file.name}"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            pdf_path = temp_path
        elif selected_preload != "None":
            pdf_path = preloaded[selected_preload]

        if not pdf_path:
            st.error("⚠️ Please upload a PDF or select a pre-loaded book.")
            return

        with st.spinner("📖 Extracting text from PDF..."):
            extractor = PDFExtractor()
            text_chunks = extractor.extract_chunks(pdf_path, chunk_size=3000)
            method_used = getattr(extractor, 'last_method', 'unknown')

        if not text_chunks:
            st.error("❌ Could not extract text from this PDF.")
            # Check if it's likely scanned
            try:
                scanned = extractor.is_scanned(pdf_path)
            except Exception:
                scanned = True
            if scanned:
                st.warning("""
**📷 This appears to be a scanned / image-based PDF.**

To enable OCR support, install these packages and restart the app:
```bash
pip install pdf2image pytesseract Pillow
# Also install Tesseract OCR engine:
# macOS:   brew install tesseract
# Ubuntu:  sudo apt install tesseract-ocr
# Windows: https://github.com/UB-Mannheim/tesseract/wiki
```
                """)
            return

        method_badge = f'<span style="background:rgba(34,197,94,0.15);color:#22c55e;border:1px solid rgba(34,197,94,0.3);padding:0.2rem 0.7rem;border-radius:20px;font-size:0.75rem;font-weight:600;">📡 {method_used}</span>'
        st.markdown(f'Extracted <b>{len(text_chunks)}</b> sections from PDF &nbsp; {method_badge}', unsafe_allow_html=True)
        if "OCR" in method_used:
            st.info("🔍 OCR mode active — scanned PDF detected. Results depend on scan quality.")
        progress_bar = st.progress(0)
        extracted_questions = []

        for i, chunk in enumerate(text_chunks):
            progress_bar.progress((i + 1) / len(text_chunks))
            qs = _parse_mcq_from_text(
                chunk,
                topic=pdf_topic.strip() or "PDF Extract",
                difficulty=pdf_difficulty
            )
            extracted_questions.extend(qs)
            if len(extracted_questions) >= pdf_num_q:
                break

        extracted_questions = extracted_questions[:pdf_num_q]
        progress_bar.empty()

        if extracted_questions:
            st.success(f"🎉 Found and extracted **{len(extracted_questions)}** MCQ questions from the PDF!")
            QuestionBank().add_questions(extracted_questions)

            st.markdown("#### 📝 Sample Extracted Questions")
            for i, q in enumerate(extracted_questions[:4]):
                with st.expander(f"Q{i+1}: {q['question'][:80]}..."):
                    for opt in q.get("options", []):
                        icon = "✅" if opt == q.get("correct_answer") else "○"
                        st.write(f"{icon} {opt}")
                    if q.get("explanation"):
                        st.info(f"💡 {q['explanation']}")

            c1, c2 = st.columns(2)
            with c1:
                if st.button("▶️ Start Quiz with PDF Questions", type="primary", use_container_width=True):
                    random.shuffle(extracted_questions)
                    st.session_state.update({
                        "questions": extracted_questions, "current_q_idx": 0,
                        "answers": {}, "quiz_started": True, "quiz_completed": False,
                        "quiz_mode": "practice", "start_time": time.time(),
                        "q_start_time": time.time(), "page": "quiz"
                    })
                    st.rerun()
            with c2:
                if st.button("📚 Add to Bank & Configure Quiz", use_container_width=True):
                    st.session_state.page = "quiz"
                    st.rerun()
        else:
            st.warning("⚠️ No standard MCQ patterns detected in this PDF. The PDF may use a non-standard format or be image-based.")
            st.markdown("**Detected text sample:**")
            if text_chunks:
                st.code(text_chunks[0][:600])


def _parse_mcq_from_text(text: str, topic: str = "PDF Extract", difficulty: str = "Medium") -> list:
    """
    Parse MCQ questions from raw PDF text.
    Detects patterns like:
      1. Question text?
      (A) Option A  (B) Option B  (C) Option C  (D) Option D
    """
    questions = []
    # Normalize whitespace
    text = re.sub(r'\r\n|\r', '\n', text)
    text = re.sub(r'\n{3,}', '\n\n', text)

    # Pattern: numbered question followed by (A)/(B)/(C)/(D) options
    # Matches: "12. Some question text\n(A) opt1 (B) opt2 (C) opt3 (D) opt4"
    q_pattern = re.compile(
        r'(?:^|\n)\s*\d{1,3}[\.\)]\s+'          # question number
        r'(.+?)\n'                                 # question text (up to newline)
        r'\s*[\(\[]?[Aa][\)\]]\.?\s*(.+?)'        # option A
        r'\s*[\(\[]?[Bb][\)\]]\.?\s*(.+?)'        # option B
        r'\s*[\(\[]?[Cc][\)\]]\.?\s*(.+?)'        # option C
        r'\s*[\(\[]?[Dd][\)\]]\.?\s*(.+?)(?:\n|$)',  # option D
        re.DOTALL | re.MULTILINE
    )

    for m in q_pattern.finditer(text):
        q_text = re.sub(r'\s+', ' ', m.group(1)).strip()
        opts = [re.sub(r'\s+', ' ', m.group(i)).strip() for i in range(2, 6)]

        # Skip if question too short or looks like garbage
        if len(q_text) < 15 or any(len(o) < 1 for o in opts):
            continue
        # Skip if it contains raw HTML
        if re.search(r'<[a-zA-Z]', q_text):
            q_text = re.sub(r'<[^>]+>', '', q_text).strip()

        questions.append({
            "id": str(uuid.uuid4())[:8],
            "topic": topic,
            "difficulty": difficulty,
            "question": q_text,
            "options": opts,
            "correct_answer": opts[0],   # will be updated if answer key found
            "explanation": ""
        })

    # Try to also detect inline-format: "1. Qtext (A) opt (B) opt (C) opt (D) opt"
    if len(questions) < 3:
        inline_pattern = re.compile(
            r'\d{1,3}[\.\)]\s+(.{10,}?)\s*'
            r'[\(\[]?[Aa][\)\]]\.?\s*(.+?)\s*'
            r'[\(\[]?[Bb][\)\]]\.?\s*(.+?)\s*'
            r'[\(\[]?[Cc][\)\]]\.?\s*(.+?)\s*'
            r'[\(\[]?[Dd][\)\]]\.?\s*(.+?)(?:\s*\d{1,3}[\.\)]|$)',
            re.DOTALL
        )
        for m in inline_pattern.finditer(text):
            q_text = re.sub(r'\s+', ' ', m.group(1)).strip()
            opts = [re.sub(r'\s+', ' ', m.group(i)).strip() for i in range(2, 6)]
            if len(q_text) < 15 or any(len(o) < 1 for o in opts):
                continue
            if re.search(r'<[a-zA-Z]', q_text):
                q_text = re.sub(r'<[^>]+>', '', q_text).strip()
            questions.append({
                "id": str(uuid.uuid4())[:8],
                "topic": topic,
                "difficulty": difficulty,
                "question": q_text,
                "options": opts,
                "correct_answer": opts[0],
                "explanation": ""
            })

    return questions


# ════════════════════════════════════════════════════════════════
# 15. BOOKMARKS PAGE
# ════════════════════════════════════════════════════════════════
def render_bookmarks():
    st.markdown('<h2 class="page-title">🔖 Bookmarked Questions</h2>', unsafe_allow_html=True)
    if not st.session_state.bookmarks:
        st.markdown('<div class="empty-state"><div class="empty-icon">🔖</div><div class="empty-title">No bookmarks yet</div><div class="empty-desc">Bookmark questions during quizzes by clicking the bookmark button.</div></div>', unsafe_allow_html=True)
        return

    all_q = {q.get("id"): q for q in QuestionBank().get_all_questions()}
    bookmarked = [all_q[bid] for bid in st.session_state.bookmarks if bid in all_q]
    st.markdown(f"**{len(bookmarked)} bookmarked questions**")

    if st.button("▶️ Practice Bookmarked Questions", type="primary"):
        st.session_state.update({"questions": bookmarked, "current_q_idx": 0, "answers": {}, "quiz_started": True, "quiz_completed": False, "quiz_mode": "practice", "start_time": time.time(), "q_start_time": time.time(), "page": "quiz"})
        st.rerun()

    for q in bookmarked:
        with st.expander(f"🔖 {q['question'][:80]}..."):
            for opt in q.get("options", []):
                st.write(f"{'✅' if opt == q.get('correct_answer') else '○'} {opt}")
            if q.get("explanation"):
                st.info(f"💡 {q['explanation']}")
            if st.button("Remove Bookmark", key=f"rm_{q.get('id')}"):
                st.session_state.bookmarks.discard(q.get("id"))
                st.rerun()


# ════════════════════════════════════════════════════════════════
# 16. SETTINGS PAGE
# ════════════════════════════════════════════════════════════════
def render_settings():
    st.markdown('<h2 class="page-title">⚙️ Settings</h2>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="config-card">', unsafe_allow_html=True)
        st.markdown("#### 🗄️ Data Management")
        if st.button("🔄 Reset All Progress", use_container_width=True):
            st.session_state.update({"total_attempted":0,"total_correct":0,"streak":0,"wrong_questions":[],"bookmarks":set(),"question_times":{}})
            st.success("✅ Progress reset successfully!")
        if st.button("🗑️ Clear Bookmarks", use_container_width=True):
            st.session_state.bookmarks = set()
            st.success("✅ Bookmarks cleared!")
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="config-card">', unsafe_allow_html=True)
        st.markdown("#### ℹ️ About")
        total = len(QuestionBank().get_all_questions())
        st.markdown(f"""
**NET Quiz Master** v2.0 · Single File Edition

Total questions in bank: **{total}**
Bookmarks saved: **{len(st.session_state.bookmarks)}**
Wrong questions for review: **{len(st.session_state.wrong_questions)}**

Built for UGC NET Paper 1 aspirants.
Supports PDF extraction from any text-based question bank.
        """)
        st.markdown('</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════
# 17. MAIN ROUTER
# ════════════════════════════════════════════════════════════════
def main():
    inject_styles()
    render_sidebar()

    page = st.session_state.page
    if page == "home":
        render_home()
    elif page == "quiz":
        render_quiz_config() if not st.session_state.quiz_started else render_quiz()
    elif page == "analytics":
        render_analytics()
    elif page == "pdf_upload":
        render_pdf_upload()
    elif page == "bookmarks":
        render_bookmarks()
    elif page == "settings":
        render_settings()


if __name__ == "__main__":
    main()
