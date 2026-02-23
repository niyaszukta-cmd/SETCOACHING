# ╔══════════════════════════════════════════════════════════════════╗
# ║          NET QUIZ MASTER — UGC NET Paper 1                      ║
# ║          Single-file Streamlit App                               ║
# ║          Includes: Question Bank · AI Generator · PDF Extractor  ║
# ╚══════════════════════════════════════════════════════════════════╝.
#
# USAGE:
#   pip install streamlit pandas PyMuPDF pdfplumber PyPDF2 anthropic
#   streamlit run net_quiz_master.py
#
# FEATURES:
#   • 47+ built-in NET Paper 1 questions across 10 topics
#   • AI question generation via Claude (Anthropic) or Gemini (Google)
#   • PDF upload → auto question extraction
#   • Practice / Exam / Review modes
#   • Bookmarks, streaks, analytics dashboard
#   • Professional dark UI with custom CSS

import streamlit as st

# ── Page config MUST be the very first Streamlit call ──────────────
st.set_page_config(
    page_title="NET Paper 1 · Quiz Master",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Standard library ───────────────────────────────────────────────
import json
import os
import random
import re
import time
import uuid
from itertools import product

# ── Third-party ────────────────────────────────────────────────────
import pandas as pd


# ══════════════════════════════════════════════════════════════════
# SECTION 1 — STYLES (CSS)
# ══════════════════════════════════════════════════════════════════

def inject_styles():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=DM+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

:root {
    --bg-primary: #0a0f1e;
    --bg-secondary: #111827;
    --bg-card: #1a2235;
    --bg-card-hover: #1e2a42;
    --accent-primary: #6366f1;
    --accent-secondary: #8b5cf6;
    --accent-gold: #f59e0b;
    --accent-green: #22c55e;
    --accent-red: #ef4444;
    --accent-cyan: #06b6d4;
    --text-primary: #f1f5f9;
    --text-secondary: #94a3b8;
    --text-muted: #475569;
    --border-color: #1e293b;
    --shadow: 0 4px 24px rgba(0,0,0,0.4);
    --shadow-glow: 0 0 30px rgba(99,102,241,0.15);
    --radius: 12px;
    --radius-lg: 20px;
}

.stApp {
    background: var(--bg-primary) !important;
    font-family: 'DM Sans', sans-serif !important;
    color: var(--text-primary) !important;
}
.stApp::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background:
        radial-gradient(ellipse at 20% 20%, rgba(99,102,241,0.08) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 80%, rgba(139,92,246,0.06) 0%, transparent 50%);
    pointer-events: none;
    z-index: 0;
}
#MainMenu, footer, header { visibility: hidden !important; }
.stDeployButton { display: none !important; }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: var(--bg-secondary) !important;
    border-right: 1px solid var(--border-color) !important;
}
[data-testid="stSidebar"] [data-testid="stVerticalBlock"] { padding: 1rem 0.5rem; }

.sidebar-brand {
    display: flex; align-items: center; gap: 0.75rem;
    padding: 1rem;
    background: linear-gradient(135deg, rgba(99,102,241,0.15), rgba(139,92,246,0.1));
    border-radius: var(--radius);
    border: 1px solid rgba(99,102,241,0.2);
    margin-bottom: 0.5rem;
}
.brand-icon { font-size: 2rem; }
.brand-title { font-family: 'Playfair Display', serif; font-size: 1.1rem; font-weight: 700; color: var(--text-primary); line-height: 1.2; }
.brand-subtitle { font-size: 0.72rem; color: var(--accent-primary); letter-spacing: 0.08em; text-transform: uppercase; }

[data-testid="stSidebar"] .stButton button {
    background: transparent !important;
    border: 1px solid transparent !important;
    color: var(--text-secondary) !important;
    text-align: left !important;
    font-size: 0.9rem !important;
    padding: 0.6rem 0.8rem !important;
    border-radius: 10px !important;
    transition: all 0.2s ease !important;
    font-family: 'DM Sans', sans-serif !important;
    width: 100% !important;
}
[data-testid="stSidebar"] .stButton button:hover {
    background: rgba(99,102,241,0.12) !important;
    color: var(--text-primary) !important;
    border-color: rgba(99,102,241,0.3) !important;
    transform: translateX(3px) !important;
}
[data-testid="stSidebar"] .stButton button[kind="primary"] {
    background: linear-gradient(135deg, rgba(99,102,241,0.25), rgba(139,92,246,0.15)) !important;
    border-color: var(--accent-primary) !important;
    color: var(--text-primary) !important;
}
.sidebar-stats {
    display: flex; justify-content: space-around;
    padding: 0.75rem;
    background: var(--bg-card);
    border-radius: var(--radius);
    border: 1px solid var(--border-color);
}
.stat-mini { text-align: center; }
.stat-mini-val { display: block; font-size: 1.2rem; font-weight: 700; color: var(--accent-primary); font-family: 'JetBrains Mono', monospace; }
.stat-mini-lbl { font-size: 0.65rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; }

/* ── LAYOUT ── */
.main .block-container { padding: 1.5rem 2rem 3rem !important; max-width: 1200px !important; }

/* ── HERO ── */
.hero-section { text-align: center; padding: 3rem 2rem 2rem; }
.hero-badge {
    display: inline-block;
    background: linear-gradient(135deg, rgba(99,102,241,0.2), rgba(139,92,246,0.1));
    border: 1px solid rgba(99,102,241,0.4);
    color: var(--accent-primary);
    padding: 0.4rem 1.2rem;
    border-radius: 50px;
    font-size: 0.8rem; font-weight: 600;
    letter-spacing: 0.1em; text-transform: uppercase;
    margin-bottom: 1.5rem;
}
.hero-title {
    font-family: 'Playfair Display', serif !important;
    font-size: clamp(2.5rem, 5vw, 4rem) !important;
    font-weight: 800 !important;
    color: var(--text-primary) !important;
    line-height: 1.15 !important;
    margin-bottom: 1rem !important;
}
.gradient-text {
    background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary), var(--accent-cyan));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-subtitle { color: var(--text-secondary) !important; font-size: 1.1rem !important; max-width: 600px !important; margin: 0 auto !important; }

/* ── TOPIC CARDS ── */
.section-title { font-size: 1.3rem; font-weight: 700; color: var(--text-primary); margin: 2rem 0 1rem; }
.topic-card {
    background: var(--bg-card); border: 1px solid var(--border-color);
    border-radius: var(--radius); padding: 1.2rem 1rem;
    text-align: center; margin-bottom: 1rem;
    transition: all 0.25s ease; position: relative; overflow: hidden;
}
.topic-card:hover { border-color: var(--accent-primary); transform: translateY(-3px); box-shadow: var(--shadow-glow); }
.topic-icon { font-size: 1.8rem; margin-bottom: 0.5rem; }
.topic-name { font-weight: 600; font-size: 0.85rem; color: var(--text-primary); margin-bottom: 0.3rem; }
.topic-desc { font-size: 0.72rem; color: var(--text-muted); line-height: 1.4; }

/* ── FEATURE CARDS ── */
.feature-card {
    background: var(--bg-card); border: 1px solid var(--border-color);
    border-radius: var(--radius-lg); padding: 1.5rem;
    margin-bottom: 1rem; min-height: 130px;
}
.feature-icon { font-size: 2rem; margin-bottom: 0.75rem; }
.feature-title { font-weight: 700; font-size: 1.05rem; color: var(--text-primary); margin-bottom: 0.5rem; }
.feature-desc { font-size: 0.85rem; color: var(--text-secondary); line-height: 1.6; }

/* ── STATS BANNER ── */
.stats-banner {
    display: flex; justify-content: center; gap: 3rem;
    padding: 2rem;
    background: linear-gradient(135deg, rgba(99,102,241,0.1), rgba(139,92,246,0.05));
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: var(--radius-lg); margin-top: 2rem;
}
.banner-stat { text-align: center; }
.banner-val {
    display: block; font-family: 'Playfair Display', serif;
    font-size: 2.5rem; font-weight: 800;
    background: linear-gradient(135deg, var(--accent-primary), var(--accent-cyan));
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.banner-lbl { font-size: 0.8rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.08em; }

/* ── PAGE TITLE ── */
.page-title {
    font-family: 'Playfair Display', serif !important;
    font-size: 2rem !important; font-weight: 800 !important;
    color: var(--text-primary) !important; margin-bottom: 1.5rem !important;
    border-left: 4px solid var(--accent-primary); padding-left: 1rem;
}

/* ── QUIZ ── */
.quiz-header { display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.5rem; }
.q-counter { color: var(--text-secondary); font-size: 0.9rem; }
.q-topic-badge {
    background: rgba(99,102,241,0.15); color: var(--accent-primary);
    border: 1px solid rgba(99,102,241,0.3);
    padding: 0.2rem 0.7rem; border-radius: 20px;
    font-size: 0.75rem; font-weight: 600;
}
.q-diff-badge { padding: 0.2rem 0.7rem; border-radius: 20px; font-size: 0.75rem; font-weight: 600; }
.diff-easy { background: rgba(34,197,94,0.15); color: #22c55e; border: 1px solid rgba(34,197,94,0.3); }
.diff-medium { background: rgba(245,158,11,0.15); color: #f59e0b; border: 1px solid rgba(245,158,11,0.3); }
.diff-hard { background: rgba(239,68,68,0.15); color: #ef4444; border: 1px solid rgba(239,68,68,0.3); }

.timer-box {
    background: var(--bg-card); border: 1px solid var(--border-color);
    border-radius: 8px; padding: 0.5rem 0.8rem;
    font-family: 'JetBrains Mono', monospace; font-size: 1rem;
    color: var(--accent-cyan); text-align: center; font-weight: 600;
}
.question-card {
    background: var(--bg-card); border: 1px solid var(--border-color);
    border-radius: var(--radius-lg); padding: 2rem;
    margin: 1rem 0 1.5rem; box-shadow: var(--shadow);
    position: relative; overflow: hidden;
}
.question-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary), var(--accent-cyan));
}
.question-meta { display: flex; justify-content: space-between; margin-bottom: 1rem; font-size: 0.8rem; color: var(--text-muted); }
.bookmark-indicator { color: var(--accent-gold); font-size: 1rem; }
.question-text { font-size: 1.15rem; font-weight: 500; color: var(--text-primary); line-height: 1.7; }

.option-btn { padding: 0.85rem 1.2rem; border-radius: 10px; margin: 0.4rem 0; font-size: 0.95rem; font-weight: 500; border: 2px solid; }
.correct-opt { background: rgba(34,197,94,0.12); border-color: #22c55e; color: #22c55e; }
.wrong-opt { background: rgba(239,68,68,0.1); border-color: #ef4444; color: #ef4444; }
.neutral-opt { background: var(--bg-secondary); border-color: var(--border-color); color: var(--text-secondary); }

.explanation-box {
    background: linear-gradient(135deg, rgba(99,102,241,0.08), rgba(6,182,212,0.05));
    border: 1px solid rgba(99,102,241,0.25);
    border-radius: var(--radius); padding: 1.2rem; margin-top: 1.2rem;
}
.exp-title { font-weight: 700; color: var(--accent-primary); margin-bottom: 0.5rem; font-size: 0.9rem; }
.exp-text { color: var(--text-secondary); font-size: 0.9rem; line-height: 1.7; }

/* ── RESULTS ── */
.results-hero {
    text-align: center; padding: 2.5rem 2rem;
    background: linear-gradient(135deg, var(--bg-card), rgba(99,102,241,0.05));
    border: 1px solid var(--border-color);
    border-radius: var(--radius-lg); margin-bottom: 2rem;
}
.results-grade { font-family: 'Playfair Display', serif; font-size: 4rem; font-weight: 800; line-height: 1; margin-bottom: 0.5rem; }
.results-score { font-size: 2rem; font-weight: 700; color: var(--text-primary); font-family: 'JetBrains Mono', monospace; }
.results-pct { font-size: 1.1rem; color: var(--text-secondary); margin: 0.5rem 0; }
.results-msg { font-size: 1rem; color: var(--accent-gold); font-style: italic; margin-top: 0.5rem; }
.result-stat-card { background: var(--bg-card); border: 1px solid var(--border-color); border-radius: var(--radius); padding: 1.2rem; text-align: center; }
.rs-val { font-size: 1.8rem; font-weight: 700; font-family: 'JetBrains Mono', monospace; display: block; margin-bottom: 0.3rem; }
.rs-lbl { font-size: 0.78rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.08em; }

/* ── ANALYTICS ── */
.analytics-card { background: var(--bg-card); border: 1px solid var(--border-color); border-radius: var(--radius); padding: 1.2rem 1.5rem; margin-bottom: 1rem; }
.ac-title { font-size: 0.8rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.4rem; }
.ac-val { font-size: 2rem; font-weight: 700; font-family: 'JetBrains Mono', monospace; display: block; }
.ac-sub { font-size: 0.8rem; color: var(--text-secondary); margin-top: 0.2rem; }

/* ── AI LAB ── */
.ai-intro-card {
    display: flex; align-items: flex-start; gap: 1.5rem;
    background: linear-gradient(135deg, rgba(99,102,241,0.1), rgba(139,92,246,0.05));
    border: 1px solid rgba(99,102,241,0.25);
    border-radius: var(--radius-lg); padding: 1.5rem; margin-bottom: 2rem;
}
.ai-intro-icon { font-size: 2.5rem; }
.ai-intro-title { font-size: 1.1rem; font-weight: 700; color: var(--text-primary); margin-bottom: 0.5rem; }
.ai-intro-desc { color: var(--text-secondary); font-size: 0.9rem; line-height: 1.6; }
.perm-stats { display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem; margin-bottom: 1.5rem; }
.perm-item { background: var(--bg-secondary); border: 1px solid var(--border-color); border-radius: 10px; padding: 0.75rem; text-align: center; }
.perm-total { grid-column: 1/-1; background: linear-gradient(135deg, rgba(99,102,241,0.15), rgba(139,92,246,0.1)); border-color: rgba(99,102,241,0.3); }
.perm-val { display: block; font-size: 1.5rem; font-weight: 700; color: var(--accent-primary); font-family: 'JetBrains Mono', monospace; }
.perm-lbl { font-size: 0.72rem; color: var(--text-muted); }

/* ── CONFIG / PDF ── */
.config-card { background: var(--bg-card); border: 1px solid var(--border-color); border-radius: var(--radius-lg); padding: 1.5rem; margin-bottom: 1rem; }
.pdf-intro {
    background: linear-gradient(135deg, rgba(6,182,212,0.08), rgba(99,102,241,0.05));
    border: 1px solid rgba(6,182,212,0.2);
    border-radius: var(--radius); padding: 1rem 1.5rem;
    color: var(--text-secondary); font-size: 0.9rem; margin-bottom: 1.5rem; line-height: 1.6;
}
.step-list { display: flex; flex-direction: column; gap: 0.75rem; }
.step-item { display: flex; align-items: center; gap: 0.75rem; font-size: 0.85rem; color: var(--text-secondary); }
.step-num {
    width: 26px; height: 26px;
    background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
    color: white; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.75rem; font-weight: 700; flex-shrink: 0;
}

/* ── EMPTY STATE ── */
.empty-state { text-align: center; padding: 4rem 2rem; color: var(--text-muted); }
.empty-icon { font-size: 3rem; margin-bottom: 1rem; }
.empty-title { font-size: 1.3rem; font-weight: 600; color: var(--text-secondary); margin-bottom: 0.5rem; }
.empty-desc { font-size: 0.9rem; }

/* ── STREAMLIT OVERRIDES ── */
.stProgress > div > div > div > div { background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary)) !important; }
.stButton button { font-family: 'DM Sans', sans-serif !important; font-weight: 600 !important; border-radius: 10px !important; transition: all 0.2s ease !important; border: none !important; }
.stButton button[kind="primary"] { background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary)) !important; color: white !important; box-shadow: 0 4px 15px rgba(99,102,241,0.3) !important; }
.stButton button[kind="primary"]:hover { transform: translateY(-2px) !important; box-shadow: 0 6px 20px rgba(99,102,241,0.4) !important; }
.stButton button[kind="secondary"] { background: var(--bg-card) !important; color: var(--text-primary) !important; border: 1px solid var(--border-color) !important; }
.stRadio label { color: var(--text-secondary) !important; font-size: 0.95rem !important; }
.stSelectbox label { color: var(--text-secondary) !important; }
div[data-baseweb="select"] { background: var(--bg-card) !important; border-color: var(--border-color) !important; }
.stTextInput input, .stTextArea textarea { background: var(--bg-card) !important; border-color: var(--border-color) !important; color: var(--text-primary) !important; font-family: 'DM Sans', sans-serif !important; }
.stCheckbox label { color: var(--text-secondary) !important; }
.streamlit-expanderHeader { background: var(--bg-card) !important; border-color: var(--border-color) !important; color: var(--text-primary) !important; border-radius: var(--radius) !important; }
div[data-baseweb="tag"] { background: rgba(99,102,241,0.2) !important; color: var(--accent-primary) !important; }
.stInfo { background: rgba(99,102,241,0.08) !important; border-color: rgba(99,102,241,0.3) !important; color: var(--text-secondary) !important; }
.stSuccess { background: rgba(34,197,94,0.08) !important; border-color: rgba(34,197,94,0.3) !important; }
.stError { background: rgba(239,68,68,0.08) !important; border-color: rgba(239,68,68,0.3) !important; }
div[data-testid="metric-container"] { background: var(--bg-card) !important; border: 1px solid var(--border-color) !important; border-radius: var(--radius) !important; padding: 1rem !important; }
.stSpinner > div { border-top-color: var(--accent-primary) !important; }
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 { color: var(--text-primary) !important; font-family: 'DM Sans', sans-serif !important; }
hr { border-color: var(--border-color) !important; }
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: var(--border-color); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent-primary); }
[data-testid="stFileUploader"] { background: var(--bg-card) !important; border: 2px dashed var(--border-color) !important; border-radius: var(--radius) !important; }
[data-testid="stFileUploader"]:hover { border-color: var(--accent-primary) !important; }
.stToggle label { color: var(--text-secondary) !important; }
.stCaption { color: var(--text-muted) !important; }
div[data-testid="stSlider"] { padding: 0.5rem 0; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
# SECTION 2 — QUESTION BANK
# ══════════════════════════════════════════════════════════════════

QUESTION_BANK_FILE = "question_bank.json"

BUILTIN_QUESTIONS = [
    # ─── TEACHING APTITUDE ───────────────────────────────────────
    {"id":"ta001","topic":"Teaching Aptitude","difficulty":"Medium",
     "question":"Which level of teaching focuses on the development of thinking power and reasoning in students?",
     "options":["Memory level","Understanding level","Reflective level","None of these"],
     "correct_answer":"Reflective level",
     "explanation":"Reflective level teaching by Morrison focuses on critical thinking, problem-solving, and independent reasoning — the highest cognitive level."},
    {"id":"ta002","topic":"Teaching Aptitude","difficulty":"Easy",
     "question":"Which of the following is NOT a characteristic of effective teaching?",
     "options":["Clarity of goals","Flexibility","Dogmatic approach","Student-centered learning"],
     "correct_answer":"Dogmatic approach",
     "explanation":"Effective teaching is flexible and student-centered; a dogmatic (rigid, doctrine-based) approach hinders learning."},
    {"id":"ta003","topic":"Teaching Aptitude","difficulty":"Hard",
     "question":"In the context of Bloom's Taxonomy (revised), which cognitive level represents the highest order of thinking?",
     "options":["Evaluation","Synthesis","Creating","Analysis"],
     "correct_answer":"Creating",
     "explanation":"The revised Bloom's Taxonomy (Anderson & Krathwohl, 2001) places 'Creating' at the apex — generating new ideas, products, or ways of viewing things."},
    {"id":"ta004","topic":"Teaching Aptitude","difficulty":"Medium",
     "question":"Which teaching method is most appropriate for large classrooms with heterogeneous groups?",
     "options":["Project Method","Lecture Method","Inquiry Method","Seminar Method"],
     "correct_answer":"Lecture Method",
     "explanation":"The lecture method is most practical for large, heterogeneous groups, allowing structured delivery to many students simultaneously."},
    {"id":"ta005","topic":"Teaching Aptitude","difficulty":"Medium",
     "question":"The concept of 'Micro-Teaching' was first developed at:",
     "options":["Harvard University","Stanford University","Yale University","MIT"],
     "correct_answer":"Stanford University",
     "explanation":"Micro-teaching was developed by Dwight W. Allen and his colleagues at Stanford University in 1963."},
    {"id":"ta006","topic":"Teaching Aptitude","difficulty":"Easy",
     "question":"Which of the following best describes 'formative evaluation'?",
     "options":["Evaluation at the end of the course","Evaluation to assign final grades","Ongoing evaluation during instruction","Evaluation before the course begins"],
     "correct_answer":"Ongoing evaluation during instruction",
     "explanation":"Formative evaluation is continuous assessment conducted during the instructional process to improve learning."},
    {"id":"ta007","topic":"Teaching Aptitude","difficulty":"Hard",
     "question":"Which theory proposes that students have different 'learning styles' and teachers should adapt instruction accordingly?",
     "options":["Constructivism","VAK/VARK Model","Behaviorism","Gestalt Theory"],
     "correct_answer":"VAK/VARK Model",
     "explanation":"The VARK model (Visual, Auditory, Read/Write, Kinesthetic) categorizes learners by preferred sensory modes."},
    {"id":"ta008","topic":"Teaching Aptitude","difficulty":"Medium",
     "question":"The 'Socratic Method' of teaching primarily involves:",
     "options":["Lecture and demonstration","Asking probing questions to stimulate thinking","Group projects","Use of audio-visual aids"],
     "correct_answer":"Asking probing questions to stimulate thinking",
     "explanation":"The Socratic method uses disciplined questioning to stimulate critical thinking and illuminate ideas."},
    {"id":"ta009","topic":"Teaching Aptitude","difficulty":"Medium",
     "question":"Which of the following is a characteristic of a 'learner-centered' classroom?",
     "options":["Teacher dominates discussions","Students passively receive information","Students actively construct knowledge","Rote memorization is emphasized"],
     "correct_answer":"Students actively construct knowledge",
     "explanation":"Learner-centered classrooms shift the focus from teacher to student, emphasizing active participation, inquiry, and knowledge construction."},
    {"id":"ta010","topic":"Teaching Aptitude","difficulty":"Easy",
     "question":"The primary purpose of teaching is to:",
     "options":["Complete the syllabus","Facilitate learning","Maintain discipline","Assess students"],
     "correct_answer":"Facilitate learning",
     "explanation":"The fundamental purpose of teaching is to facilitate, guide, and support student learning and overall development."},

    # ─── RESEARCH APTITUDE ───────────────────────────────────────
    {"id":"ra001","topic":"Research Aptitude","difficulty":"Medium",
     "question":"Which type of research aims to solve immediate practical problems?",
     "options":["Fundamental research","Applied research","Action research","Historical research"],
     "correct_answer":"Action research",
     "explanation":"Action research is conducted by practitioners to solve specific, immediate problems in their working environment."},
    {"id":"ra002","topic":"Research Aptitude","difficulty":"Easy",
     "question":"A hypothesis is best described as:",
     "options":["A proven fact","A tentative statement to be tested","A summary of findings","A literature review"],
     "correct_answer":"A tentative statement to be tested",
     "explanation":"A hypothesis is a tentative, testable proposition about the relationship between two or more variables."},
    {"id":"ra003","topic":"Research Aptitude","difficulty":"Hard",
     "question":"Which sampling method ensures every member of the population has an equal chance of being selected?",
     "options":["Purposive sampling","Snowball sampling","Simple Random Sampling","Quota sampling"],
     "correct_answer":"Simple Random Sampling",
     "explanation":"Simple Random Sampling gives every individual in the population an equal and independent probability of selection."},
    {"id":"ra004","topic":"Research Aptitude","difficulty":"Medium",
     "question":"The term 'triangulation' in research refers to:",
     "options":["Geometric analysis of data","Using multiple methods to validate findings","A statistical test","Sampling technique"],
     "correct_answer":"Using multiple methods to validate findings",
     "explanation":"Triangulation uses multiple data sources, methods, or theories to cross-check and validate research findings."},
    {"id":"ra005","topic":"Research Aptitude","difficulty":"Medium",
     "question":"Which research design is used to determine cause-and-effect relationships?",
     "options":["Descriptive","Correlational","Experimental","Ethnographic"],
     "correct_answer":"Experimental",
     "explanation":"Experimental research involves manipulation of an independent variable to determine its effect on a dependent variable, establishing causality."},
    {"id":"ra006","topic":"Research Aptitude","difficulty":"Hard",
     "question":"A Type I error in research refers to:",
     "options":["Accepting a false null hypothesis","Rejecting a true null hypothesis","Failing to collect data","Using the wrong statistical test"],
     "correct_answer":"Rejecting a true null hypothesis",
     "explanation":"A Type I error (false positive) occurs when the null hypothesis is true but is incorrectly rejected. Its probability is denoted by alpha (α)."},
    {"id":"ra007","topic":"Research Aptitude","difficulty":"Easy",
     "question":"Plagiarism in research is considered:",
     "options":["Acceptable if citing the source","An ethical violation","Only applies to published work","Legal but unprofessional"],
     "correct_answer":"An ethical violation",
     "explanation":"Plagiarism — presenting others' work as one's own — is a serious breach of research ethics and academic integrity."},
    {"id":"ra008","topic":"Research Aptitude","difficulty":"Medium",
     "question":"The review of related literature in research helps to:",
     "options":["Define the research problem only","Identify gaps and situate the study","Replace primary data collection","Eliminate the need for methodology"],
     "correct_answer":"Identify gaps and situate the study",
     "explanation":"Literature review helps researchers understand existing knowledge, identify research gaps, and frame their study within the field."},

    # ─── READING COMPREHENSION ───────────────────────────────────
    {"id":"rc001","topic":"Reading Comprehension","difficulty":"Medium",
     "question":"Inferential comprehension requires the reader to:",
     "options":["Locate directly stated information","Draw conclusions beyond what is stated","Memorize the passage","Summarize only"],
     "correct_answer":"Draw conclusions beyond what is stated",
     "explanation":"Inferential comprehension involves reading 'between the lines' — using clues in the text to draw logical conclusions not explicitly stated."},
    {"id":"rc002","topic":"Reading Comprehension","difficulty":"Easy",
     "question":"The main idea of a passage is:",
     "options":["A supporting detail","The central thought or theme","The title of the passage","A specific example"],
     "correct_answer":"The central thought or theme",
     "explanation":"The main idea is the primary message or central argument the author wants to communicate."},
    {"id":"rc003","topic":"Reading Comprehension","difficulty":"Hard",
     "question":"'Critical reading' involves:",
     "options":["Reading rapidly for the gist","Evaluating the author's arguments and evidence","Memorizing key vocabulary","Paraphrasing every sentence"],
     "correct_answer":"Evaluating the author's arguments and evidence",
     "explanation":"Critical reading goes beyond comprehension — it involves analyzing, questioning, and evaluating the quality and validity of the author's arguments."},

    # ─── COMMUNICATION ───────────────────────────────────────────
    {"id":"cm001","topic":"Communication","difficulty":"Easy",
     "question":"Which element is NOT part of the communication process?",
     "options":["Sender","Message","Channel","Profit"],
     "correct_answer":"Profit",
     "explanation":"The communication process involves: Sender, Message, Channel, Receiver, Feedback, and Noise. Profit is not a component."},
    {"id":"cm002","topic":"Communication","difficulty":"Medium",
     "question":"Which of the following is an example of 'noise' in communication?",
     "options":["Clear pronunciation","Use of jargon unfamiliar to the receiver","Well-organized message","Appropriate channel selection"],
     "correct_answer":"Use of jargon unfamiliar to the receiver",
     "explanation":"Noise refers to any barrier that distorts or interferes with message transmission — semantic noise includes jargon or unfamiliar language."},
    {"id":"cm003","topic":"Communication","difficulty":"Medium",
     "question":"Proxemics in non-verbal communication refers to:",
     "options":["Tone of voice","Use of space and distance","Facial expressions","Gestures"],
     "correct_answer":"Use of space and distance",
     "explanation":"Proxemics (coined by Edward Hall) studies how people use physical space and distance in communication."},
    {"id":"cm004","topic":"Communication","difficulty":"Hard",
     "question":"The Berlo's SMCR model of communication stands for:",
     "options":["Source, Message, Channel, Receiver","Signal, Medium, Code, Response","Sender, Meaning, Content, Reaction","None of the above"],
     "correct_answer":"Source, Message, Channel, Receiver",
     "explanation":"David Berlo's SMCR model (1960) includes Source, Message, Channel, and Receiver as the four key elements of communication."},
    {"id":"cm005","topic":"Communication","difficulty":"Easy",
     "question":"Classroom communication is primarily:",
     "options":["Intrapersonal","Interpersonal & Group","Mass communication","Corporate communication"],
     "correct_answer":"Interpersonal & Group",
     "explanation":"Classroom communication involves both interpersonal (teacher-student) and group (teacher + multiple students) communication."},
    {"id":"cm006","topic":"Communication","difficulty":"Medium",
     "question":"'Effective listening' is best characterized by:",
     "options":["Hearing every word spoken","Interpreting the speaker's body language only","Understanding the full meaning including feelings and intent","Replying immediately after the speaker stops"],
     "correct_answer":"Understanding the full meaning including feelings and intent",
     "explanation":"Effective listening (active listening) involves comprehending the message's full meaning — content, emotions, and intent — not merely hearing words."},

    # ─── LOGICAL REASONING ───────────────────────────────────────
    {"id":"lr001","topic":"Logical Reasoning","difficulty":"Medium",
     "question":"If all professors are researchers, and some researchers are administrators, which conclusion is VALID?",
     "options":["All professors are administrators","Some professors may be administrators","No professors are administrators","All administrators are professors"],
     "correct_answer":"Some professors may be administrators",
     "explanation":"From the given premises, we can only conclude that it's possible (not certain) that some professors are administrators."},
    {"id":"lr002","topic":"Logical Reasoning","difficulty":"Easy",
     "question":"What comes next in the series: 2, 6, 12, 20, 30, ?",
     "options":["40","42","44","36"],
     "correct_answer":"42",
     "explanation":"The differences are 4, 6, 8, 10, 12. So next = 30 + 12 = 42."},
    {"id":"lr003","topic":"Logical Reasoning","difficulty":"Hard",
     "question":"Which of the following is an example of 'deductive reasoning'?",
     "options":["All observed swans are white, so the next swan is white","All men are mortal; Socrates is a man; therefore Socrates is mortal","Based on past experience, it will rain today","The sample suggests the whole population believes X"],
     "correct_answer":"All men are mortal; Socrates is a man; therefore Socrates is mortal",
     "explanation":"Deductive reasoning moves from general principles to specific conclusions. This classic syllogism is the textbook example of valid deductive reasoning."},
    {"id":"lr004","topic":"Logical Reasoning","difficulty":"Medium",
     "question":"A statement followed by two conclusions: 'Education is the key to success.' Conclusion I: All educated people are successful. Conclusion II: Success requires effort in education. Which conclusion(s) follow?",
     "options":["Only I","Only II","Both I and II","Neither I nor II"],
     "correct_answer":"Only II",
     "explanation":"Conclusion I is an absolute statement not supported by 'key to success.' Conclusion II reasonably follows from the idea that education (effort) leads to success."},
    {"id":"lr005","topic":"Logical Reasoning","difficulty":"Hard",
     "question":"In a coded language, if ROSE is written as TQUG, how is BISCUIT written?",
     "options":["DKUEWKV","DKUEWKW","CKTEVKW","DKUFVKV"],
     "correct_answer":"DKUEWKV",
     "explanation":"Each letter is shifted forward by 2 positions: B→D, I→K, S→U, C→E, U→W, I→K, T→V. So BISCUIT → DKUEWKV."},

    # ─── ICT ─────────────────────────────────────────────────────
    {"id":"ict001","topic":"ICT","difficulty":"Easy",
     "question":"Which of the following is an example of an input device?",
     "options":["Monitor","Printer","Keyboard","Speaker"],
     "correct_answer":"Keyboard",
     "explanation":"Input devices send data to the computer. Keyboard, mouse, scanner are input devices; monitor, printer, speaker are output devices."},
    {"id":"ict002","topic":"ICT","difficulty":"Medium",
     "question":"What does 'HTML' stand for?",
     "options":["Hyper Text Markup Language","High Tech Modern Language","Hyper Transfer Meta Language","Home Tool Markup Language"],
     "correct_answer":"Hyper Text Markup Language",
     "explanation":"HTML (HyperText Markup Language) is the standard markup language for creating web pages."},
    {"id":"ict003","topic":"ICT","difficulty":"Medium",
     "question":"Which protocol is used for secure web browsing?",
     "options":["HTTP","FTP","HTTPS","SMTP"],
     "correct_answer":"HTTPS",
     "explanation":"HTTPS (HyperText Transfer Protocol Secure) uses SSL/TLS encryption to secure data transmission between browser and server."},
    {"id":"ict004","topic":"ICT","difficulty":"Hard",
     "question":"Moore's Law states that the number of transistors on a microchip doubles approximately every:",
     "options":["6 months","1 year","2 years","5 years"],
     "correct_answer":"2 years",
     "explanation":"Gordon Moore observed in 1965 that transistor count doubles roughly every two years, leading to exponential growth in computing power."},
    {"id":"ict005","topic":"ICT","difficulty":"Easy",
     "question":"What is the full form of 'ICT' in educational context?",
     "options":["Information and Communication Technology","Integrated Computer Training","International Computer Technology","Interactive Communication Tools"],
     "correct_answer":"Information and Communication Technology",
     "explanation":"ICT stands for Information and Communication Technology — encompassing all technologies for handling information and facilitating communication."},
    {"id":"ict006","topic":"ICT","difficulty":"Medium",
     "question":"Which of the following is NOT a search engine?",
     "options":["Google","Bing","WhatsApp","DuckDuckGo"],
     "correct_answer":"WhatsApp",
     "explanation":"WhatsApp is a messaging application, not a search engine. Google, Bing, and DuckDuckGo are all search engines."},

    # ─── ENVIRONMENT & ECOLOGY ───────────────────────────────────
    {"id":"env001","topic":"Environment & Ecology","difficulty":"Medium",
     "question":"The 'Paris Agreement' primarily addresses:",
     "options":["Nuclear non-proliferation","Climate change and global warming","Trade barriers","Ozone layer depletion"],
     "correct_answer":"Climate change and global warming",
     "explanation":"The Paris Agreement (2015) is an international treaty under UNFCCC focused on limiting global warming to well below 2°C above pre-industrial levels."},
    {"id":"env002","topic":"Environment & Ecology","difficulty":"Easy",
     "question":"Which gas is primarily responsible for the greenhouse effect?",
     "options":["Oxygen","Nitrogen","Carbon Dioxide","Hydrogen"],
     "correct_answer":"Carbon Dioxide",
     "explanation":"CO₂ is the primary anthropogenic greenhouse gas, trapping heat in the atmosphere and contributing to global warming."},
    {"id":"env003","topic":"Environment & Ecology","difficulty":"Hard",
     "question":"The 'Chipko Movement' in India was primarily associated with:",
     "options":["Water conservation","Forest and tree conservation","Wildlife protection","Soil conservation"],
     "correct_answer":"Forest and tree conservation",
     "explanation":"The Chipko Movement (1973, Uttarakhand) was a non-violent protest where villagers embraced trees to prevent their felling, pioneering environmental activism in India."},
    {"id":"env004","topic":"Environment & Ecology","difficulty":"Medium",
     "question":"Biodiversity hotspots are areas with:",
     "options":["High temperature and humidity","High species richness and endemism facing threats","Rich mineral resources","Dense human population"],
     "correct_answer":"High species richness and endemism facing threats",
     "explanation":"Biodiversity hotspots have exceptional concentrations of endemic species and have lost significant amounts of their original habitat."},
    {"id":"env005","topic":"Environment & Ecology","difficulty":"Medium",
     "question":"'Sustainable development' was defined in which report?",
     "options":["Brundtland Report","Stockholm Declaration","Rio Declaration","Kyoto Protocol"],
     "correct_answer":"Brundtland Report",
     "explanation":"The Brundtland Report (Our Common Future, 1987) defined sustainable development as 'development that meets the needs of the present without compromising the ability of future generations to meet their own needs.'"},

    # ─── HIGHER EDUCATION ────────────────────────────────────────
    {"id":"he001","topic":"Higher Education","difficulty":"Medium",
     "question":"The National Education Policy (NEP) 2020 recommends the school curriculum to be restructured as:",
     "options":["10+2","5+3+3+4","8+4","6+3+2+1"],
     "correct_answer":"5+3+3+4",
     "explanation":"NEP 2020 proposes a 5+3+3+4 curricular structure: Foundational (5 years), Preparatory (3 years), Middle (3 years), Secondary (4 years)."},
    {"id":"he002","topic":"Higher Education","difficulty":"Easy",
     "question":"UGC stands for:",
     "options":["University Grants Commission","United Graduates Council","Universal Government College","University General Council"],
     "correct_answer":"University Grants Commission",
     "explanation":"The University Grants Commission (UGC) is the statutory body responsible for coordination, determination, and maintenance of standards in higher education in India."},
    {"id":"he003","topic":"Higher Education","difficulty":"Hard",
     "question":"The concept of 'Autonomous Institutions' in Indian higher education means:",
     "options":["Complete independence from any university","Freedom to design curriculum, conduct exams, and declare results","Government-funded colleges","Deemed universities"],
     "correct_answer":"Freedom to design curriculum, conduct exams, and declare results",
     "explanation":"Autonomous institutions have the freedom to design their own curriculum, set syllabus, conduct exams, and declare results under UGC guidelines."},
    {"id":"he004","topic":"Higher Education","difficulty":"Medium",
     "question":"NAAC stands for:",
     "options":["National Assessment and Accreditation Council","National Academic Awards Council","National Association for Academic Curriculum","None of these"],
     "correct_answer":"National Assessment and Accreditation Council",
     "explanation":"NAAC is an autonomous body established by UGC to assess and accredit higher education institutions in India."},
    {"id":"he005","topic":"Higher Education","difficulty":"Medium",
     "question":"Which committee recommended the establishment of UGC?",
     "options":["Kothari Commission","Radhakrishnan Commission","Mudaliar Commission","Sarkar Committee"],
     "correct_answer":"Radhakrishnan Commission",
     "explanation":"The University Education Commission (1948–49) chaired by Dr. S. Radhakrishnan recommended the establishment of the UGC."},

    # ─── GOVERNANCE ──────────────────────────────────────────────
    {"id":"gov001","topic":"Indian Constitution & Governance","difficulty":"Easy",
     "question":"The Preamble of the Indian Constitution describes India as:",
     "options":["Federal, Democratic Republic","Sovereign, Socialist, Secular, Democratic Republic","Federal, Socialist State","Secular, Parliamentary Democracy"],
     "correct_answer":"Sovereign, Socialist, Secular, Democratic Republic",
     "explanation":"The Preamble declares India to be a Sovereign, Socialist, Secular, Democratic Republic committed to Justice, Liberty, Equality, and Fraternity."},
    {"id":"gov002","topic":"Indian Constitution & Governance","difficulty":"Medium",
     "question":"Which Article of the Indian Constitution guarantees Right to Education?",
     "options":["Article 19","Article 21A","Article 25","Article 32"],
     "correct_answer":"Article 21A",
     "explanation":"Article 21A (inserted by 86th Amendment, 2002) provides free and compulsory education to children aged 6-14 as a Fundamental Right."},
    {"id":"gov003","topic":"Indian Constitution & Governance","difficulty":"Hard",
     "question":"The concept of 'Basic Structure' of the Indian Constitution was established by:",
     "options":["Golaknath case (1967)","Kesavananda Bharati case (1973)","Minerva Mills case (1980)","Maneka Gandhi case (1978)"],
     "correct_answer":"Kesavananda Bharati case (1973)",
     "explanation":"The Supreme Court in Kesavananda Bharati v. State of Kerala (1973) established the Basic Structure Doctrine — Parliament cannot alter the basic structure of the Constitution."},
    {"id":"gov004","topic":"Indian Constitution & Governance","difficulty":"Medium",
     "question":"Directive Principles of State Policy in India are:",
     "options":["Justiciable in courts","Non-justiciable but fundamental to governance","Enforceable by the Supreme Court only","Part of the Fundamental Rights"],
     "correct_answer":"Non-justiciable but fundamental to governance",
     "explanation":"Directive Principles (Part IV, Articles 36–51) are non-justiciable (not enforceable by courts) but are fundamental in governance and aim to establish a welfare state."},

    # ─── DATA INTERPRETATION ─────────────────────────────────────
    {"id":"di001","topic":"Data Interpretation","difficulty":"Medium",
     "question":"If the mean of 5 numbers is 30 and the mean of 3 of them is 20, what is the mean of the remaining 2?",
     "options":["35","45","40","50"],
     "correct_answer":"45",
     "explanation":"Total sum = 5×30 = 150. Sum of 3 numbers = 3×20 = 60. Remaining sum = 150-60 = 90. Mean of 2 = 90/2 = 45."},
    {"id":"di002","topic":"Data Interpretation","difficulty":"Easy",
     "question":"Which measure of central tendency is most affected by extreme values (outliers)?",
     "options":["Mode","Median","Mean","None of these"],
     "correct_answer":"Mean",
     "explanation":"The arithmetic mean is significantly affected by extreme values/outliers since all values are summed; median and mode are more resistant."},
    {"id":"di003","topic":"Data Interpretation","difficulty":"Hard",
     "question":"The coefficient of variation (CV) is calculated as:",
     "options":["(Mean/SD) × 100","(SD/Mean) × 100","SD × Mean","Mean/Variance"],
     "correct_answer":"(SD/Mean) × 100",
     "explanation":"CV = (Standard Deviation / Mean) × 100. It expresses variability as a percentage of the mean, allowing comparison across datasets with different units."},
    {"id":"di004","topic":"Data Interpretation","difficulty":"Medium",
     "question":"In a bar chart, the height of each bar represents:",
     "options":["The percentage of data","The frequency or value of the category","The range of data","The median value"],
     "correct_answer":"The frequency or value of the category",
     "explanation":"In a bar chart, the length/height of each bar is proportional to the value or frequency it represents."},
    {"id":"di005","topic":"Data Interpretation","difficulty":"Medium",
     "question":"A pie chart is best used to display:",
     "options":["Trends over time","Parts of a whole as percentages","Correlation between two variables","Frequency distribution"],
     "correct_answer":"Parts of a whole as percentages",
     "explanation":"Pie charts are ideal for showing the proportional composition of a whole — how each category contributes to 100% of the total."},
]


class QuestionBank:
    def __init__(self, filepath=QUESTION_BANK_FILE):
        self.filepath = filepath
        self._ensure_file()

    def _ensure_file(self):
        if not os.path.exists(self.filepath):
            with open(self.filepath, "w") as f:
                json.dump(BUILTIN_QUESTIONS, f, indent=2)
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
        added = 0
        for q in new_questions:
            if not q.get("id"):
                q["id"] = str(uuid.uuid4())[:8]
            if q["id"] not in existing_ids:
                existing.append(q)
                existing_ids.add(q["id"])
                added += 1
        self._save(existing)
        return added


# ══════════════════════════════════════════════════════════════════
# SECTION 3 — AI QUESTION GENERATOR
# ══════════════════════════════════════════════════════════════════

class AIQuestionGenerator:
    """Generate UGC NET Paper 1 MCQs via Claude or Gemini API."""

    def __init__(self, api_key: str, provider: str = "claude"):
        self.api_key = api_key
        self.provider = provider.lower()

    # ── Public ────────────────────────────────────────────────────
    def generate_questions(self, topic, difficulties, styles, n=10, extra_instructions=""):
        combos = list(product(difficulties, styles))
        q_per_combo = max(1, n // len(combos))
        remainder = n - q_per_combo * len(combos)
        all_questions = []
        for i, (difficulty, style) in enumerate(combos):
            count = q_per_combo + (1 if i < remainder else 0)
            prompt = self._build_generation_prompt(topic, difficulty, style, count, extra_instructions)
            raw = self._call_api(prompt)
            parsed = self._parse_questions(raw, topic=topic, difficulty=difficulty)
            all_questions.extend(parsed)
        return all_questions[:n]

    def generate_from_text(self, text, n=5, topic="UGC NET Paper 1"):
        prompt = self._build_text_prompt(text, n, topic)
        raw = self._call_api(prompt)
        return self._parse_questions(raw, topic=topic, difficulty="Medium")

    # ── Prompt builders ───────────────────────────────────────────
    def _build_generation_prompt(self, topic, difficulty, style, n, extra=""):
        style_instructions = {
            "MCQ (4 options)": "Standard 4-option MCQ. One clearly correct answer, three plausible distractors.",
            "True/False": "Convert to 4-option: statement + True / False / Cannot Say / Partially True.",
            "Assertion-Reason": "Format: Assertion (A) and Reason (R). Options: (1) Both A and R true, R explains A; (2) Both true, R does not explain A; (3) A true R false; (4) A false R true.",
            "Match the Following": "Two lists. Options are match combinations (e.g., A-3,B-1,C-4,D-2).",
            "Case-based": "Short paragraph/case followed by one MCQ based on the scenario.",
        }
        style_desc = style_instructions.get(style, "Standard MCQ with 4 options")
        level_desc = {"Easy": "straightforward recall", "Medium": "application and understanding", "Hard": "analysis, evaluation, higher-order thinking"}.get(difficulty, "mixed")
        return f"""You are an expert UGC NET Paper 1 question setter.

Generate EXACTLY {n} {difficulty.upper()} level questions on: "{topic}"
Style: {style} — {style_desc}
Level means: {level_desc}

Rules:
- Strictly UGC NET Paper 1 {topic} syllabus
- Exactly 4 options per question
- One unambiguously correct answer
- 2-3 sentence explanation per question
- No repeated questions
{f'Additional: {extra}' if extra else ''}

Return ONLY a valid JSON array, no other text:
[
  {{
    "question": "...",
    "options": ["A", "B", "C", "D"],
    "correct_answer": "A",
    "explanation": "...",
    "difficulty": "{difficulty}",
    "topic": "{topic}"
  }}
]"""

    def _build_text_prompt(self, text, n, topic):
        return f"""You are an expert UGC NET Paper 1 question setter.

Generate EXACTLY {n} MCQ questions directly based on this study material:

{text[:3000]}

Rules:
- Questions must be based only on the provided text
- Exactly 4 options each
- Mix Easy / Medium / Hard difficulty
- Provide correct answer and brief explanation

Return ONLY valid JSON array:
[
  {{
    "question": "...",
    "options": ["A", "B", "C", "D"],
    "correct_answer": "A",
    "explanation": "...",
    "difficulty": "Medium",
    "topic": "{topic}"
  }}
]"""

    # ── API calls ─────────────────────────────────────────────────
    def _call_api(self, prompt):
        return self._call_claude(prompt) if self.provider == "claude" else self._call_gemini(prompt)

    def _call_claude(self, prompt):
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=self.api_key)
            msg = client.messages.create(
                model="claude-opus-4-6", max_tokens=4096,
                messages=[{"role": "user", "content": prompt}]
            )
            return msg.content[0].text
        except ImportError:
            return self._call_claude_http(prompt)
        except Exception as e:
            st.error(f"Claude API error: {e}")
            return ""

    def _call_claude_http(self, prompt):
        import urllib.request
        try:
            payload = json.dumps({
                "model": "claude-opus-4-6", "max_tokens": 4096,
                "messages": [{"role": "user", "content": prompt}]
            }).encode()
            req = urllib.request.Request(
                "https://api.anthropic.com/v1/messages", data=payload,
                headers={"Content-Type": "application/json",
                         "x-api-key": self.api_key,
                         "anthropic-version": "2023-06-01"}
            )
            with urllib.request.urlopen(req, timeout=60) as resp:
                return json.loads(resp.read())["content"][0]["text"]
        except Exception as e:
            st.error(f"Claude HTTP error: {e}")
            return ""

    def _call_gemini(self, prompt):
        import urllib.request
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.api_key}"
            payload = json.dumps({
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"maxOutputTokens": 4096, "temperature": 0.7}
            }).encode()
            req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=60) as resp:
                return json.loads(resp.read())["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            st.error(f"Gemini API error: {e}")
            return ""

    # ── Parser ────────────────────────────────────────────────────
    def _parse_questions(self, raw, topic="General", difficulty="Medium"):
        if not raw:
            return []
        try:
            match = re.search(r'\[.*\]', raw, re.DOTALL)
            questions = json.loads(match.group() if match else raw)
            valid = []
            for q in questions:
                if (isinstance(q, dict) and q.get("question") and
                        q.get("options") and q.get("correct_answer") and
                        q["correct_answer"] in q["options"] and
                        len(q["options"]) >= 4):
                    q["id"] = str(uuid.uuid4())[:8]
                    q.setdefault("topic", topic)
                    q.setdefault("difficulty", difficulty)
                    q.setdefault("explanation", "")
                    valid.append(q)
            return valid
        except Exception:
            return []


# ══════════════════════════════════════════════════════════════════
# SECTION 4 — PDF EXTRACTOR
# ══════════════════════════════════════════════════════════════════

class PDFExtractor:
    """Extract text from PDF files using multiple fallback methods."""

    def extract_chunks(self, pdf_path, chunk_size=1500):
        text = self._extract_text(pdf_path)
        if not text:
            return []
        text = self._clean_text(text)
        chunks = self._split_into_chunks(text, chunk_size)
        return [c for c in chunks if len(c.strip()) > 200]

    def _extract_text(self, pdf_path):
        for method in [self._extract_with_pymupdf, self._extract_with_pdfplumber, self._extract_with_pypdf2]:
            text = method(pdf_path)
            if text and len(text) > 100:
                return text
        return ""

    def _extract_with_pymupdf(self, pdf_path):
        try:
            import fitz
            doc = fitz.open(pdf_path)
            text = "".join(page.get_text() + "\n\n" for page in doc)
            doc.close()
            return text
        except Exception:
            return ""

    def _extract_with_pdfplumber(self, pdf_path):
        try:
            import pdfplumber
            text = ""
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    t = page.extract_text()
                    if t:
                        text += t + "\n\n"
            return text
        except Exception:
            return ""

    def _extract_with_pypdf2(self, pdf_path):
        try:
            import PyPDF2
            text = ""
            with open(pdf_path, "rb") as f:
                for page in PyPDF2.PdfReader(f).pages:
                    text += page.extract_text() + "\n\n"
            return text
        except Exception:
            return ""

    def _clean_text(self, text):
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = re.sub(r' {2,}', ' ', text)
        text = re.sub(r'\n\s*\d+\s*\n', '\n', text)
        text = re.sub(r'www\.\S+', '', text)
        return text.strip()

    def _split_into_chunks(self, text, chunk_size):
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
        if len(chunks) <= 1 and len(text) > chunk_size:
            chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size-200) if len(text[i:i+chunk_size]) > 200]
        return chunks


# ══════════════════════════════════════════════════════════════════
# SECTION 5 — SESSION STATE
# ══════════════════════════════════════════════════════════════════

def init_session_state():
    defaults = {
        "questions": [], "current_q_idx": 0, "answers": {},
        "quiz_started": False, "quiz_completed": False,
        "quiz_mode": "practice", "score": 0,
        "start_time": None, "q_start_time": None,
        "num_questions": 20, "difficulty": "Mixed",
        "bookmarks": set(), "streak": 0,
        "total_attempted": 0, "total_correct": 0,
        "question_times": {}, "ai_generated_count": 0,
        "page": "home", "wrong_questions": [],
        "timed": True, "time_per_q": 90,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


# ══════════════════════════════════════════════════════════════════
# SECTION 6 — SIDEBAR
# ══════════════════════════════════════════════════════════════════

def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-brand">
            <div class="brand-icon">🎓</div>
            <div>
                <div class="brand-title">NET Quiz Master</div>
                <div class="brand-subtitle">Paper 1 · UGC NET</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        nav_items = [
            ("🏠", "Home", "home"),
            ("📝", "Practice Quiz", "quiz"),
            ("📊", "Analytics", "analytics"),
            ("🤖", "AI Question Lab", "ai_lab"),
            ("📄", "PDF Upload", "pdf_upload"),
            ("🔖", "Bookmarks", "bookmarks"),
            ("⚙️", "Settings", "settings"),
        ]
        for icon, label, page_key in nav_items:
            is_active = st.session_state.page == page_key
            if st.button(f"{icon}  {label}", key=f"nav_{page_key}",
                         use_container_width=True,
                         type="primary" if is_active else "secondary"):
                st.session_state.page = page_key
                st.session_state.quiz_started = False
                st.rerun()

        st.markdown("---")

        accuracy = (
            round(st.session_state.total_correct / st.session_state.total_attempted * 100)
            if st.session_state.total_attempted > 0 else 0
        )
        st.markdown(f"""
        <div class="sidebar-stats">
            <div class="stat-mini">
                <span class="stat-mini-val">{st.session_state.total_attempted}</span>
                <span class="stat-mini-lbl">Attempted</span>
            </div>
            <div class="stat-mini">
                <span class="stat-mini-val">{accuracy}%</span>
                <span class="stat-mini-lbl">Accuracy</span>
            </div>
            <div class="stat-mini">
                <span class="stat-mini-val">{st.session_state.streak}</span>
                <span class="stat-mini-lbl">Streak 🔥</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("""
        <div style="text-align:center;opacity:0.45;font-size:0.72rem;padding:0.5rem;">
            UGC NET Paper 1 Prep<br>
            <span style="color:#6366f1;">NYZTrade Education</span>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
# SECTION 7 — HOME PAGE
# ══════════════════════════════════════════════════════════════════

def render_home():
    st.markdown("""
    <div class="hero-section">
        <div class="hero-badge">UGC NET · Paper 1</div>
        <h1 class="hero-title">NET Coaching pro by <span class="gradient-text">ZYRO Learning</span></h1>
        <p class="hero-subtitle">AI-powered question generation · 10 core topics · Real exam simulation</p>
    </div>
    """, unsafe_allow_html=True)

    topics = [
        ("🧠","Teaching Aptitude","Pedagogy, Methods, Levels"),
        ("🔬","Research Aptitude","Methods, Ethics, Types"),
        ("📖","Reading Comprehension","Passages, Inference"),
        ("💬","Communication","Verbal, Non-verbal, Barriers"),
        ("🔢","Logical Reasoning","Syllogism, Series, Data"),
        ("💻","ICT","Computers, Internet, Tools"),
        ("🌍","Environment & Ecology","Ecology, Pollution, Policy"),
        ("📐","Higher Education","UGC, NEP, Institutions"),
        ("🏛️","Governance","Polity, Preamble, Rights"),
        ("📊","Data Interpretation","Graphs, Tables, Stats"),
    ]

    st.markdown('<div class="section-title">📚 Core Topics</div>', unsafe_allow_html=True)
    cols = st.columns(5)
    for i, (icon, title, desc) in enumerate(topics):
        with cols[i % 5]:
            st.markdown(f"""
            <div class="topic-card">
                <div class="topic-icon">{icon}</div>
                <div class="topic-name">{title}</div>
                <div class="topic-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""<div class="feature-card"><div class="feature-icon">⚡</div>
        <div class="feature-title">Quick Practice</div>
        <div class="feature-desc">Jump into a 20-question mixed-topic session immediately.</div></div>""",
        unsafe_allow_html=True)
        if st.button("Start Quick Quiz →", use_container_width=True, type="primary"):
            st.session_state.page = "quiz"
            st.session_state.num_questions = 20
            st.rerun()

    with col2:
        st.markdown("""<div class="feature-card"><div class="feature-icon">🤖</div>
        <div class="feature-title">AI Question Generator</div>
        <div class="feature-desc">Use Claude / Gemini to generate hundreds of unique questions on any topic.</div></div>""",
        unsafe_allow_html=True)
        if st.button("Open AI Lab →", use_container_width=True):
            st.session_state.page = "ai_lab"
            st.rerun()

    with col3:
        st.markdown("""<div class="feature-card"><div class="feature-icon">📄</div>
        <div class="feature-title">PDF Quiz Generator</div>
        <div class="feature-desc">Upload any study material PDF and auto-generate quiz questions from it.</div></div>""",
        unsafe_allow_html=True)
        if st.button("Upload PDF →", use_container_width=True):
            st.session_state.page = "pdf_upload"
            st.rerun()

    qb = QuestionBank()
    total_q = len(qb.get_all_questions())
    st.markdown(f"""
    <div class="stats-banner">
        <div class="banner-stat"><span class="banner-val">{total_q}+</span><span class="banner-lbl">Questions</span></div>
        <div class="banner-stat"><span class="banner-val">10</span><span class="banner-lbl">Topics</span></div>
        <div class="banner-stat"><span class="banner-val">3</span><span class="banner-lbl">Difficulty Levels</span></div>
        <div class="banner-stat"><span class="banner-val">AI</span><span class="banner-lbl">Powered</span></div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
# SECTION 8 — QUIZ CONFIG
# ══════════════════════════════════════════════════════════════════

def render_quiz_config():
    st.markdown('<h2 class="page-title">📝 Configure Your Quiz</h2>', unsafe_allow_html=True)
    qb = QuestionBank()
    all_topics = qb.get_topics()

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown('<div class="config-card">', unsafe_allow_html=True)
        st.markdown("#### 🎯 Select Topics")
        selected = []
        topic_cols = st.columns(2)
        for i, topic in enumerate(all_topics):
            with topic_cols[i % 2]:
                if st.checkbox(topic, value=True, key=f"topic_{topic}"):
                    selected.append(topic)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="config-card">', unsafe_allow_html=True)
        st.markdown("#### ⚙️ Settings")
        num_q = st.select_slider("Number of Questions", [10,15,20,25,30,40,50], value=20)
        difficulty = st.radio("Difficulty", ["Easy","Medium","Hard","Mixed"], index=3, horizontal=True)
        quiz_mode = st.radio("Quiz Mode", ["Practice","Exam","Review"],
                             captions=["Show answer after each Q","Full exam simulation","Only wrong questions"], index=0)
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
                "questions": questions,
                "current_q_idx": 0,
                "answers": {},
                "quiz_started": True,
                "quiz_completed": False,
                "quiz_mode": quiz_mode.lower(),
                "start_time": time.time(),
                "q_start_time": time.time(),
                "num_questions": num_q,
                "timed": timed,
                "time_per_q": time_per_q,
            })
            st.rerun()


# ══════════════════════════════════════════════════════════════════
# SECTION 9 — QUIZ INTERFACE
# ══════════════════════════════════════════════════════════════════

def render_quiz():
    if st.session_state.quiz_completed:
        render_results()
        return

    questions = st.session_state.questions
    idx = st.session_state.current_q_idx

    if idx >= len(questions):
        st.session_state.quiz_completed = True
        _calculate_score()
        st.rerun()
        return

    q = questions[idx]
    total = len(questions)
    elapsed = int(time.time() - st.session_state.start_time)
    mins, secs = divmod(elapsed, 60)

    col_prog, col_timer, col_skip = st.columns([4, 1, 1])
    with col_prog:
        st.markdown(f"""
        <div class="quiz-header">
            <span class="q-counter">Question <b>{idx+1}</b> / {total}</span>
            <span class="q-topic-badge">{q.get('topic','General')}</span>
            <span class="q-diff-badge diff-{q.get('difficulty','medium').lower()}">{q.get('difficulty','Medium')}</span>
        </div>
        """, unsafe_allow_html=True)
        st.progress(idx / total)
    with col_timer:
        st.markdown(f'<div class="timer-box">⏱️ {mins:02d}:{secs:02d}</div>', unsafe_allow_html=True)
    with col_skip:
        if st.button("Skip →"):
            st.session_state.answers[idx] = {"answer": None, "correct": False, "skipped": True}
            st.session_state.current_q_idx += 1
            st.session_state.q_start_time = time.time()
            st.rerun()

    q_id = q.get("id", idx)
    bookmarked = q_id in st.session_state.bookmarks
    st.markdown(f"""
    <div class="question-card">
        <div class="question-meta">
            <span>Q{idx+1}</span>
            {'<span class="bookmark-indicator">🔖</span>' if bookmarked else ''}
        </div>
        <div class="question-text">{q['question']}</div>
    </div>
    """, unsafe_allow_html=True)

    already_answered = idx in st.session_state.answers
    options = q.get("options", [])
    correct_ans = q.get("correct_answer", "")

    if already_answered:
        user_ans = st.session_state.answers[idx].get("answer")
        for opt in options:
            if opt == correct_ans:
                st.markdown(f'<div class="option-btn correct-opt">✅ {opt}</div>', unsafe_allow_html=True)
            elif opt == user_ans and opt != correct_ans:
                st.markdown(f'<div class="option-btn wrong-opt">❌ {opt}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="option-btn neutral-opt">{opt}</div>', unsafe_allow_html=True)

        if q.get("explanation"):
            st.markdown(f"""
            <div class="explanation-box">
                <div class="exp-title">💡 Explanation</div>
                <div class="exp-text">{q['explanation']}</div>
            </div>
            """, unsafe_allow_html=True)

        col_prev, col_next = st.columns(2)
        with col_prev:
            if idx > 0:
                if st.button("← Previous", use_container_width=True):
                    st.session_state.current_q_idx -= 1
                    st.rerun()
        with col_next:
            if idx < total - 1:
                if st.button("Next Question →", use_container_width=True, type="primary"):
                    st.session_state.current_q_idx += 1
                    st.session_state.q_start_time = time.time()
                    st.rerun()
            else:
                if st.button("🏁 Finish Quiz", use_container_width=True, type="primary"):
                    st.session_state.quiz_completed = True
                    _calculate_score()
                    st.rerun()
    else:
        choice = st.radio("Select your answer:", options, key=f"q_{idx}", label_visibility="collapsed")
        col_ans, col_bk = st.columns([3, 1])
        with col_ans:
            if st.button("✅ Submit Answer", use_container_width=True, type="primary"):
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
        with col_bk:
            if st.button("🔖 Bookmark", use_container_width=True):
                if q_id in st.session_state.bookmarks:
                    st.session_state.bookmarks.discard(q_id)
                else:
                    st.session_state.bookmarks.add(q_id)
                st.rerun()


def _calculate_score():
    st.session_state.score = sum(1 for a in st.session_state.answers.values() if a.get("correct"))


# ══════════════════════════════════════════════════════════════════
# SECTION 10 — RESULTS
# ══════════════════════════════════════════════════════════════════

def render_results():
    score = st.session_state.score
    total = len(st.session_state.questions)
    pct = round(score / total * 100) if total > 0 else 0
    elapsed = int(time.time() - st.session_state.start_time)
    mins, secs = divmod(elapsed, 60)
    grade, gcolor, gmsg = _get_grade(pct)

    st.markdown(f"""
    <div class="results-hero">
        <div class="results-grade" style="color:{gcolor}">{grade}</div>
        <div class="results-score">{score} / {total}</div>
        <div class="results-pct">{pct}% Accuracy</div>
        <div class="results-msg">{gmsg}</div>
    </div>
    """, unsafe_allow_html=True)

    correct = score
    wrong = sum(1 for a in st.session_state.answers.values() if not a.get("correct") and not a.get("skipped"))
    skipped = sum(1 for a in st.session_state.answers.values() if a.get("skipped"))
    avg_time = (round(sum(st.session_state.question_times.values()) / len(st.session_state.question_times))
                if st.session_state.question_times else 0)

    for col, val, lbl, color in zip(
        st.columns(5),
        [correct, wrong, skipped, f"{mins}m {secs}s", f"{avg_time}s"],
        ["Correct","Wrong","Skipped","Total Time","Avg/Question"],
        ["#22c55e","#ef4444","#f59e0b","#6366f1","#06b6d4"]
    ):
        with col:
            st.markdown(f"""
            <div class="result-stat-card" style="border-top:3px solid {color}">
                <div class="rs-val" style="color:{color}">{val}</div>
                <div class="rs-lbl">{lbl}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🔄 Retake Quiz", use_container_width=True, type="primary"):
            st.session_state.quiz_started = False
            st.session_state.quiz_completed = False
            st.rerun()
    with c2:
        if st.button("📊 View Analytics", use_container_width=True):
            st.session_state.page = "analytics"
            st.rerun()
    with c3:
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


def _get_grade(pct):
    if pct >= 90: return "A+", "#22c55e", "Outstanding! You're ready for the exam! 🏆"
    if pct >= 75: return "A",  "#84cc16", "Excellent work! Keep it up! 🌟"
    if pct >= 60: return "B",  "#f59e0b", "Good performance. A bit more practice needed. 💪"
    if pct >= 45: return "C",  "#f97316", "Average. Focus on weak areas. 📚"
    return "D", "#ef4444", "Keep practicing! Consistency is key. 🎯"


# ══════════════════════════════════════════════════════════════════
# SECTION 11 — ANALYTICS
# ══════════════════════════════════════════════════════════════════

def render_analytics():
    st.markdown('<h2 class="page-title">📊 Performance Analytics</h2>', unsafe_allow_html=True)

    if st.session_state.total_attempted == 0:
        st.markdown("""<div class="empty-state">
            <div class="empty-icon">📊</div>
            <div class="empty-title">No data yet</div>
            <div class="empty-desc">Complete a quiz to see your performance analytics here.</div>
        </div>""", unsafe_allow_html=True)
        return

    accuracy = round(st.session_state.total_correct / st.session_state.total_attempted * 100)
    metrics = [
        ("Total Questions", st.session_state.total_attempted, "answered", "#6366f1"),
        ("Correct Answers", st.session_state.total_correct, "correct", "#22c55e"),
        ("Accuracy Rate", f"{accuracy}%", "overall", "#f59e0b"),
        ("Current Streak", st.session_state.streak, "in a row 🔥", "#ef4444"),
    ]
    for col, (title, val, sub, color) in zip(st.columns(4), metrics):
        with col:
            st.markdown(f"""
            <div class="analytics-card" style="border-left:4px solid {color}">
                <div class="ac-title">{title}</div>
                <div class="ac-val" style="color:{color}">{val}</div>
                <div class="ac-sub">{sub}</div>
            </div>
            """, unsafe_allow_html=True)

    if st.session_state.question_times:
        st.markdown("<br>#### ⏱️ Time per Question (last quiz)")
        df = pd.DataFrame({
            "Question": [f"Q{i+1}" for i in st.session_state.question_times],
            "Seconds": list(st.session_state.question_times.values())
        })
        st.bar_chart(df.set_index("Question"))

    st.markdown(f"#### 🔖 Bookmarked Questions: **{len(st.session_state.bookmarks)}**")
    st.markdown(f"#### ❌ Wrong Questions Bank: **{len(st.session_state.wrong_questions)}** questions saved for review")


# ══════════════════════════════════════════════════════════════════
# SECTION 12 — AI LAB
# ══════════════════════════════════════════════════════════════════

def render_ai_lab():
    st.markdown('<h2 class="page-title">🤖 AI Question Generation Lab</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div class="ai-intro-card">
        <div class="ai-intro-icon">✨</div>
        <div>
            <div class="ai-intro-title">Multiply Your Questions with AI</div>
            <div class="ai-intro-desc">
                Use Claude or Gemini AI to generate hundreds of unique UGC NET Paper 1 questions.
                The AI uses permutations of topics, difficulty levels, and question styles to create
                diverse, exam-relevant questions automatically.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="config-card">', unsafe_allow_html=True)
        st.markdown("#### 🔑 API Configuration")
        ai_provider = st.selectbox("AI Provider", ["Claude (Anthropic)", "Gemini (Google)"])
        api_key = st.text_input("API Key", type="password", placeholder="Enter your API key here...",
                                help="Your key is never stored and only used for this session.")

        st.markdown("#### 🎛️ Generation Settings")
        gen_topic = st.selectbox("Topic", [
            "Teaching Aptitude","Research Aptitude","Reading Comprehension","Communication",
            "Logical Reasoning","ICT","Environment & Ecology","Higher Education",
            "Indian Constitution & Governance","Data Interpretation"
        ])
        gen_difficulty = st.multiselect("Difficulty Levels", ["Easy","Medium","Hard"], default=["Medium","Hard"])
        question_styles = st.multiselect("Question Styles",
            ["MCQ (4 options)","True/False","Assertion-Reason","Match the Following","Case-based"],
            default=["MCQ (4 options)","Assertion-Reason"])
        num_to_generate = st.slider("Questions to generate", 5, 50, 10)
        custom_prompt_extra = st.text_area("Additional Instructions (optional)",
            placeholder="e.g., Focus on recent UGC guidelines...", height=80)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="config-card">', unsafe_allow_html=True)
        st.markdown("#### 🔮 Permutation Preview")
        combos = max(len(gen_difficulty), 1) * max(len(question_styles), 1)
        st.markdown(f"""
        <div class="perm-stats">
            <div class="perm-item"><span class="perm-val">{len(gen_difficulty)}</span><span class="perm-lbl">Difficulty levels</span></div>
            <div class="perm-item"><span class="perm-val">{len(question_styles)}</span><span class="perm-lbl">Question styles</span></div>
            <div class="perm-item"><span class="perm-val">{combos}</span><span class="perm-lbl">Combinations</span></div>
            <div class="perm-item perm-total"><span class="perm-val">~{num_to_generate}</span><span class="perm-lbl">Will be generated</span></div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
#### 📋 How It Works
1. **Topic selection** → AI focuses on NET Paper 1 syllabus
2. **Style permutation** → Different question formats for same concept
3. **Difficulty variation** → Easy / Medium / Hard variants generated
4. **Deduplication** → AI ensures no repeated questions
5. **Quality check** → Questions validated against NET exam pattern
        """)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 Generate Questions with AI", use_container_width=True, type="primary"):
            if not api_key:
                st.error("⚠️ Please enter your API key."); return
            if not gen_difficulty or not question_styles:
                st.error("⚠️ Select at least one difficulty and one question style."); return

            provider = "claude" if "Claude" in ai_provider else "gemini"
            generator = AIQuestionGenerator(api_key=api_key, provider=provider)

            with st.spinner(f"🤖 {ai_provider} is generating {num_to_generate} questions..."):
                generated = generator.generate_questions(
                    topic=gen_topic, difficulties=gen_difficulty,
                    styles=question_styles, n=num_to_generate,
                    extra_instructions=custom_prompt_extra
                )

            if generated:
                st.success(f"✅ Successfully generated {len(generated)} questions!")
                st.session_state.ai_generated_count += len(generated)
                QuestionBank().add_questions(generated)

                st.markdown("#### 📝 Preview (first 3)")
                for i, q in enumerate(generated[:3]):
                    with st.expander(f"Q{i+1}: {q['question'][:60]}..."):
                        for opt in q.get("options", []):
                            st.write(f"{'✅' if opt == q.get('correct_answer') else '○'} {opt}")
                        if q.get("explanation"):
                            st.info(f"💡 {q['explanation']}")

                if st.button("▶️ Start Quiz with Generated Questions", type="primary"):
                    _start_quiz(generated)
            else:
                st.error("❌ Generation failed. Check your API key and try again.")


# ══════════════════════════════════════════════════════════════════
# SECTION 13 — PDF UPLOAD
# ══════════════════════════════════════════════════════════════════

def render_pdf_upload():
    st.markdown('<h2 class="page-title">📄 PDF Quiz Generator</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div class="pdf-intro">
        Upload any NET Paper 1 study material, notes, or question book PDF.
        Our AI will extract content and automatically generate quiz questions from it.
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])
    with col1:
        uploaded_file = st.file_uploader("Upload PDF Study Material", type=["pdf"])
        preloaded = {
            "UGC NET Paper 1 Q-Book 2022": "/mnt/user-data/uploads/UGC_NET_PAPER_1_QBOOK_2022_Edited_compressed.pdf",
            "AIFER Paper 1 Ebook 2023 (December)": "/mnt/user-data/uploads/AIFERPAPER1EBOOK2023DECEMBER.pdf"
        }
        st.markdown("#### 📚 Or Use Pre-loaded Books")
        selected_preload = st.selectbox("Select a pre-loaded book", ["None"] + list(preloaded.keys()))

        pdf_api_key = st.text_input("AI API Key (Claude or Gemini)", type="password", key="pdf_api_key")
        pdf_ai_provider = st.selectbox("AI Provider", ["Claude (Anthropic)", "Gemini (Google)"], key="pdf_provider")
        pdf_num_q = st.slider("Questions to extract", 5, 50, 20, key="pdf_num_q")
        pdf_topic = st.text_input("Topic hint (optional)", placeholder="e.g., Research Aptitude")

        if st.button("🔍 Extract & Generate Questions", use_container_width=True, type="primary"):
            if not pdf_api_key:
                st.error("⚠️ API key required."); return

            pdf_path = None
            if uploaded_file:
                temp_path = f"/tmp/{uploaded_file.name}"
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                pdf_path = temp_path
            elif selected_preload != "None":
                pdf_path = preloaded[selected_preload]

            if not pdf_path:
                st.error("⚠️ Please upload a PDF or select a pre-loaded book."); return

            with st.spinner("📖 Extracting text from PDF..."):
                chunks = PDFExtractor().extract_chunks(pdf_path)

            if not chunks:
                st.error("❌ Could not extract text from PDF."); return

            st.success(f"✅ Extracted {len(chunks)} content sections")
            provider = "claude" if "Claude" in pdf_ai_provider else "gemini"
            generator = AIQuestionGenerator(api_key=pdf_api_key, provider=provider)
            progress_bar = st.progress(0)
            status_text = st.empty()
            generated_all = []
            chunks_to_use = chunks[:min(10, len(chunks))]
            q_per_chunk = max(1, pdf_num_q // len(chunks_to_use))

            for i, chunk in enumerate(chunks_to_use):
                status_text.markdown(f"🤖 Generating from section {i+1}/{len(chunks_to_use)}...")
                progress_bar.progress((i+1)/len(chunks_to_use))
                qs = generator.generate_from_text(chunk, n=q_per_chunk, topic=pdf_topic or "UGC NET Paper 1")
                generated_all.extend(qs)
                if len(generated_all) >= pdf_num_q:
                    break

            generated_all = generated_all[:pdf_num_q]
            status_text.empty()

            if generated_all:
                st.success(f"🎉 Generated {len(generated_all)} questions from PDF!")
                QuestionBank().add_questions(generated_all)
                st.markdown("#### 📝 Sample Questions")
                for i, q in enumerate(generated_all[:3]):
                    with st.expander(f"Q{i+1}: {q['question'][:70]}..."):
                        for opt in q.get("options", []):
                            st.write(f"{'✅' if opt==q.get('correct_answer') else '○'} {opt}")
                        if q.get("explanation"):
                            st.info(f"💡 {q['explanation']}")
                if st.button("▶️ Start Quiz with PDF Questions", type="primary"):
                    _start_quiz(generated_all)
            else:
                st.error("❌ Could not generate questions. Try a different PDF or AI provider.")

    with col2:
        st.markdown("""
        <div class="config-card">
            <div style="font-weight:700;margin-bottom:1rem;">📋 How PDF Extraction Works</div>
            <div class="step-list">
                <div class="step-item"><span class="step-num">1</span><span>PDF text is extracted and chunked into sections</span></div>
                <div class="step-item"><span class="step-num">2</span><span>AI reads each section and identifies key concepts</span></div>
                <div class="step-item"><span class="step-num">3</span><span>MCQ questions are generated with 4 options each</span></div>
                <div class="step-item"><span class="step-num">4</span><span>Correct answers and explanations are added</span></div>
                <div class="step-item"><span class="step-num">5</span><span>Questions are saved to the quiz bank</span></div>
            </div>
        </div>
        <div class="config-card" style="margin-top:1rem;">
            <div style="font-weight:700;margin-bottom:0.5rem;">💡 Tips for Best Results</div>
            <ul style="color:#94a3b8;font-size:0.85rem;line-height:1.8;">
                <li>Use text-based PDFs (not scanned images)</li>
                <li>NET Paper 1 question banks work best</li>
                <li>Clear, structured content gives better questions</li>
                <li>Larger PDFs = more diverse questions</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
# SECTION 14 — BOOKMARKS
# ══════════════════════════════════════════════════════════════════

def render_bookmarks():
    st.markdown('<h2 class="page-title">🔖 Bookmarked Questions</h2>', unsafe_allow_html=True)

    if not st.session_state.bookmarks:
        st.markdown("""<div class="empty-state">
            <div class="empty-icon">🔖</div>
            <div class="empty-title">No bookmarks yet</div>
            <div class="empty-desc">Bookmark questions during quizzes by clicking the bookmark button.</div>
        </div>""", unsafe_allow_html=True)
        return

    qb = QuestionBank()
    all_q = {q.get("id"): q for q in qb.get_all_questions()}
    bookmarked_questions = [all_q[bid] for bid in st.session_state.bookmarks if bid in all_q]
    st.markdown(f"**{len(bookmarked_questions)} bookmarked questions**")

    if bookmarked_questions:
        if st.button("▶️ Practice Bookmarked Questions", type="primary"):
            _start_quiz(bookmarked_questions)

    for q in bookmarked_questions:
        with st.expander(f"🔖 {q['question'][:80]}..."):
            for opt in q.get("options", []):
                st.write(f"{'✅' if opt==q.get('correct_answer') else '○'} {opt}")
            if q.get("explanation"):
                st.info(f"💡 {q['explanation']}")
            if st.button(f"Remove Bookmark", key=f"rm_{q.get('id')}"):
                st.session_state.bookmarks.discard(q.get("id"))
                st.rerun()


# ══════════════════════════════════════════════════════════════════
# SECTION 15 — SETTINGS
# ══════════════════════════════════════════════════════════════════

def render_settings():
    st.markdown('<h2 class="page-title">⚙️ Settings</h2>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="config-card">', unsafe_allow_html=True)
        st.markdown("#### 🗄️ Data Management")
        if st.button("🔄 Reset All Progress", use_container_width=True):
            st.session_state.update({
                "total_attempted": 0, "total_correct": 0,
                "streak": 0, "wrong_questions": [],
                "bookmarks": set(), "question_times": {}
            })
            st.success("✅ Progress reset!")
        if st.button("🗑️ Clear Bookmarks", use_container_width=True):
            st.session_state.bookmarks = set()
            st.success("✅ Bookmarks cleared!")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="config-card">', unsafe_allow_html=True)
        st.markdown("#### ℹ️ About")
        qb = QuestionBank()
        total = len(qb.get_all_questions())
        st.markdown(f"""
**NET Quiz Master** v2.0  
Questions in bank: **{total}**  
AI generated: **{st.session_state.ai_generated_count}**  
Bookmarks: **{len(st.session_state.bookmarks)}**  

Built for UGC NET Paper 1 aspirants.  
Supports Claude & Gemini AI APIs.  
— NYZTrade Education
        """)
        st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
# SECTION 16 — HELPERS
# ══════════════════════════════════════════════════════════════════

def _start_quiz(questions):
    """Helper to start a quiz from any question list."""
    random.shuffle(questions)
    st.session_state.update({
        "questions": questions,
        "current_q_idx": 0,
        "answers": {},
        "quiz_started": True,
        "quiz_completed": False,
        "quiz_mode": "practice",
        "start_time": time.time(),
        "q_start_time": time.time(),
        "page": "quiz",
    })
    st.rerun()


# ══════════════════════════════════════════════════════════════════
# SECTION 17 — MAIN ROUTER
# ══════════════════════════════════════════════════════════════════

def main():
    inject_styles()
    init_session_state()
    render_sidebar()

    page = st.session_state.page

    if page == "home":
        render_home()
    elif page == "quiz":
        if not st.session_state.quiz_started:
            render_quiz_config()
        else:
            render_quiz()
    elif page == "analytics":
        render_analytics()
    elif page == "ai_lab":
        render_ai_lab()
    elif page == "pdf_upload":
        render_pdf_upload()
    elif page == "bookmarks":
        render_bookmarks()
    elif page == "settings":
        render_settings()


if __name__ == "__main__":
    main()
