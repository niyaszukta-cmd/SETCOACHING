"""
╔══════════════════════════════════════════════════════════════════════╗
║    NET QUIZ MASTER v3.0  ·  Complete Platform Redesign              ║
║    NYZTrade Education  ·  UGC NET Paper 1                           ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import html, json, os, re, random, time, uuid, hashlib
from datetime import datetime, timedelta
from itertools import product
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="NET Guru — UGC NET Paper 1",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════
QUESTION_BANK_FILE = "question_bank.json"
USERS_FILE         = "users.json"
SCORES_FILE        = "scores.json"
DEVELOPER_PIN      = "NYZ2025"

TOPICS = [
    "Teaching Aptitude","Research Aptitude","Reading Comprehension",
    "Communication","Reasoning","ICT","Environment & Ecology",
    "Higher Education","Indian Constitution & Governance","Data Interpretation"
]

PYQ_YEARS = list(range(2024, 2015, -1))  # 2024 → 2016
SEASONS   = ["June", "December"]

# ═══════════════════════════════════════════════
# CSS
# ═══════════════════════════════════════════════
def inject_styles():
    # Inject viewport meta for proper mobile scaling
    st.markdown('<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">', unsafe_allow_html=True)
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,800;0,900;1,700&family=DM+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

/* ══════════════════════════════════════════════════════
   DESIGN TOKENS — Dark Academy (DM + Violet)
══════════════════════════════════════════════════════ */
* { box-sizing: border-box; }
:root {
  --bg:        #07090f;
  --bg2:       #0d1117;
  --bg-card:   #131929;
  --surface:   #131929;
  --surface2:  #1a2235;
  --surface3:  #1e2a40;
  --border:    #1e2d45;
  --border2:   #3b4f6e;
  --line:      #1e2d45;
  --line2:     #2d3f5e;
  --line3:     #3b4f6e;
  --violet:    #7c3aed;
  --violet2:   #a855f7;
  --violet-glow: rgba(124,58,237,0.15);
  --cyan:      #22d3ee;
  --cyan2:     #67e8f9;
  --gold:      #fbbf24;
  --gold2:     #fde68a;
  --amber:     #fbbf24;
  --amber2:    #fde68a;
  --green:     #10b981;
  --red:       #f43f5e;
  --rose:      #f43f5e;
  --indigo:    #6366f1;
  --indigo2:   #818cf8;
  --emerald:   #10b981;
  --teal:      #22d3ee;
  --teal2:     #67e8f9;
  --t1: #ffffff;
  --t2: #cbd5e1;
  --t3: #94a3b8;
  --t4: #64748b;
  --text:  #ffffff;
  --text2: #cbd5e1;
  --text3: #94a3b8;
  --r:    14px; --rl:   20px;
  --r-sm:  8px; --r-md: 14px; --r-lg: 20px; --r-xl: 28px;
  --shadow-card: 0 2px 24px rgba(0,0,0,0.5), 0 1px 4px rgba(0,0,0,0.3);
}

/* ══ APP BASE ══ */
.stApp { background: var(--bg) !important; font-family: 'DM Sans', sans-serif !important; color: var(--t1) !important; -webkit-font-smoothing: antialiased; }
#MainMenu, footer, header { visibility: hidden !important; }
.stDeployButton { display: none !important; }
[data-testid="stText"] { display: none !important; }

/* ══ MAIN CONTAINER ══ */
.main .block-container { padding: 0.75rem 0.75rem 4rem !important; max-width: 100% !important; }
@media (min-width: 768px) { .main .block-container { padding: 1.5rem 2rem 3rem !important; max-width: 1280px !important; } }

/* ══ SCROLLBAR ══ */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--violet); }

/* ══════════════════════════════════════════════════════
   SIDEBAR
══════════════════════════════════════════════════════ */
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #0d1117, #0a0e1a) !important;
  border-right: 1px solid var(--border) !important;
  min-width: 240px !important;
}
.sidebar-brand {
  display: flex; align-items: center; gap: 0.7rem; padding: 1rem;
  background: linear-gradient(135deg, rgba(124,58,237,0.25), rgba(168,85,247,0.1));
  border-radius: var(--r); border: 1px solid rgba(124,58,237,0.5);
  margin-bottom: 0.5rem;
}
.brand-title { font-family: 'Playfair Display', serif; font-size: 1rem; font-weight: 700; color: #fff; }
.brand-subtitle { font-size: 0.68rem; color: #a855f7; letter-spacing: 0.1em; text-transform: uppercase; font-weight: 600; }

[data-testid="stSidebar"] .stButton button {
  background: transparent !important; border: 1px solid transparent !important;
  color: var(--t3) !important; text-align: left !important; font-size: 0.9rem !important;
  padding: 0.6rem 0.8rem !important; border-radius: 10px !important;
  width: 100% !important; font-weight: 500 !important; font-family: 'DM Sans', sans-serif !important;
}
[data-testid="stSidebar"] .stButton button * { color: inherit !important; }
[data-testid="stSidebar"] .stButton button:hover {
  background: rgba(124,58,237,0.18) !important; color: #fff !important;
  border-color: rgba(124,58,237,0.5) !important;
}
[data-testid="stSidebar"] .stButton button[kind="primary"] {
  background: linear-gradient(135deg, rgba(124,58,237,0.35), rgba(168,85,247,0.2)) !important;
  border-color: var(--violet) !important; color: #fff !important;
}
[data-testid="stSidebar"] .stButton button[kind="primary"] * { color: #fff !important; }

.sidebar-stats {
  display: flex; justify-content: space-around; padding: 0.8rem;
  background: linear-gradient(135deg, rgba(124,58,237,0.1), rgba(34,211,238,0.05));
  border-radius: var(--r); border: 1px solid rgba(124,58,237,0.3);
}
.stat-mini { text-align: center; }
.stat-mini-val {
  display: block; font-size: 1.2rem; font-weight: 800;
  font-family: 'JetBrains Mono', monospace;
  background: linear-gradient(135deg, #a855f7, #22d3ee);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.stat-mini-lbl { font-size: 0.6rem; color: var(--t4); text-transform: uppercase; letter-spacing: 0.06em; }

/* ══════════════════════════════════════════════════════
   PAGE ANATOMY
══════════════════════════════════════════════════════ */
.page-wrap { padding-top: 0.5rem; }
.page-header { margin-bottom: 1.75rem; padding-bottom: 1.25rem; border-bottom: 1px solid var(--border); }
.page-header h1 {
  font-family: 'Playfair Display', serif;
  font-size: clamp(1.5rem, 3vw, 2.2rem); font-weight: 800; color: var(--t1);
  letter-spacing: -0.02em; line-height: 1.15; margin-bottom: 0.4rem;
  border-left: 5px solid var(--violet); padding-left: 0.9rem;
}
.page-header p { font-size: 0.9rem; color: var(--t2); line-height: 1.65; max-width: 680px; padding-left: 1rem; }

.page-title {
  font-family: 'Playfair Display', serif !important; font-size: 1.6rem !important;
  font-weight: 800 !important; color: #fff !important; margin-bottom: 1rem !important;
  border-left: 5px solid var(--violet); padding-left: 0.9rem;
}

.section-label {
  display: flex; align-items: center; gap: 0.75rem;
  font-size: 0.72rem; font-weight: 700; letter-spacing: 0.12em;
  text-transform: uppercase; color: var(--t3); margin: 1.75rem 0 1rem;
}
.section-label::before { content: ''; width: 3px; height: 14px; border-radius: 2px; background: var(--violet2); flex-shrink: 0; }
.section-label::after  { content: ''; flex: 1; height: 1px; background: var(--border); }
.section-label .pill {
  background: var(--surface2); border: 1px solid var(--border2);
  color: var(--t3); font-size: 0.6rem; padding: 0.15rem 0.5rem;
  border-radius: 20px; font-weight: 600; text-transform: uppercase;
}

/* ══════════════════════════════════════════════════════
   HERO SECTION
══════════════════════════════════════════════════════ */
.hero, .hero-section {
  text-align: center;
  padding: 3.5rem 1rem 2rem;
  position: relative;
  overflow: hidden;
  display: flex; flex-direction: column; align-items: center; justify-content: center;
}
@media (min-width: 768px) { .hero, .hero-section { padding: 5rem 2rem 3rem; } }

/* multi-layer ambient glow background */
.hero::before {
  content: '';
  position: absolute; inset: 0;
  background:
    radial-gradient(ellipse 80% 60% at 50% 0%, rgba(124,58,237,0.18), transparent 70%),
    radial-gradient(ellipse 50% 40% at 20% 80%, rgba(168,85,247,0.10), transparent 70%),
    radial-gradient(ellipse 50% 40% at 80% 80%, rgba(34,211,238,0.08), transparent 70%);
  pointer-events: none;
  z-index: 0;
}
/* animated top glow line */
.hero::after {
  content: '';
  position: absolute; top: 0; left: 10%; right: 10%; height: 2px;
  background: linear-gradient(90deg, transparent, rgba(124,58,237,0.8), rgba(34,211,238,0.8), transparent);
  border-radius: 50%;
  animation: heroLine 3s ease-in-out infinite alternate;
  z-index: 0;
}
@keyframes heroLine { from{opacity:0.4;left:20%;right:20%;} to{opacity:1;left:5%;right:5%;} }

.hero > * { position: relative; z-index: 1; }

.hero-badge {
  display: inline-flex; align-items: center; gap: 0.5rem;
  background: linear-gradient(135deg, rgba(124,58,237,0.25), rgba(168,85,247,0.12));
  border: 1px solid rgba(168,85,247,0.55); color: #c084fc;
  padding: 0.4rem 1.2rem; border-radius: 50px;
  font-size: 0.75rem; font-weight: 700; letter-spacing: 0.12em;
  text-transform: uppercase; margin-bottom: 1.5rem;
  box-shadow: 0 0 20px rgba(124,58,237,0.15);
  animation: badgePulse 3s ease-in-out infinite;
}
.hero-badge::before { content: '●'; font-size: 0.4rem; color: #a855f7; animation: blink 1.5s infinite; }
@keyframes blink { 0%,100%{opacity:1;} 50%{opacity:0.2;} }
@keyframes badgePulse { 0%,100%{box-shadow:0 0 20px rgba(124,58,237,0.15);} 50%{box-shadow:0 0 35px rgba(124,58,237,0.35);} }

.hero-title {
  font-family: 'Playfair Display', serif !important;
  font-size: clamp(2.4rem, 7vw, 4.8rem) !important;
  font-weight: 900 !important; color: #fff !important;
  line-height: 1.08 !important; margin-bottom: 1rem !important;
  letter-spacing: -0.03em;
  text-align: center;
  text-shadow: 0 2px 40px rgba(124,58,237,0.25);
}
.hero-title em, .gradient-text {
  font-style: italic;
  background: linear-gradient(135deg, #a855f7, #7c3aed, #22d3ee);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
  filter: drop-shadow(0 0 20px rgba(124,58,237,0.4));
}

/* Feature pills row */
.hero-features {
  display: flex; flex-wrap: wrap; gap: 0.6rem;
  justify-content: center; align-items: center;
  margin: 0 auto 1rem; max-width: 680px;
}
.hero-pill {
  display: inline-flex; align-items: center; gap: 0.4rem;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 50px; padding: 0.35rem 0.85rem;
  font-size: 0.78rem; color: var(--t2); font-weight: 500;
  transition: all 0.2s;
}
.hero-pill:hover { background: rgba(124,58,237,0.12); border-color: rgba(124,58,237,0.4); color: #e2e8f0; }
.hero-pill .pill-icon { font-size: 0.9rem; }

.hero-sub, .hero-subtitle { font-size: 1rem; color: var(--t2); line-height: 1.75; max-width: 560px; margin: 0 auto 2rem; text-align:center; }

/* ══ STAT STRIP ══ */
.stat-strip {
  display: grid; grid-template-columns: repeat(6, 1fr);
  background: linear-gradient(135deg, rgba(124,58,237,0.06), rgba(13,17,23,0.95));
  border: 1px solid rgba(124,58,237,0.2);
  border-radius: var(--rl); overflow: hidden; margin: 1.75rem auto;
  max-width: 900px;
  box-shadow: 0 4px 30px rgba(124,58,237,0.1), inset 0 1px 0 rgba(255,255,255,0.04);
}
@media (max-width: 700px) { .stat-strip { grid-template-columns: repeat(3, 1fr); } }
.stat-cell {
  padding: 1.4rem 0.5rem; text-align: center;
  border-right: 1px solid rgba(124,58,237,0.12);
  transition: background 0.25s, transform 0.2s;
  display: flex; flex-direction: column; align-items: center; gap: 0.2rem;
}
.stat-cell:last-child { border-right: none; }
.stat-cell:hover { background: rgba(124,58,237,0.1); }
.stat-icon { font-size: 1.2rem; margin-bottom: 0.1rem; display: block; }
.stat-val {
  font-family: 'Playfair Display', serif; font-size: 1.75rem; font-weight: 800;
  display: block; line-height: 1;
  background: linear-gradient(135deg, #a855f7, #22d3ee);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
  margin-bottom: 0.2rem;
}
.stat-lbl { font-size: 0.6rem; color: var(--t4); text-transform: uppercase; letter-spacing: 0.1em; font-weight: 700; }

/* Stats banner (home page) */
.stats-banner {
  display: flex; justify-content: space-around; flex-wrap: wrap; gap: 1rem;
  padding: 1.5rem 1rem;
  background: linear-gradient(135deg, rgba(124,58,237,0.15), rgba(34,211,238,0.06));
  border: 1px solid rgba(124,58,237,0.35); border-radius: var(--rl); margin-top: 1.5rem;
}
.banner-stat { text-align: center; }
.banner-val {
  display: block; font-family: 'Playfair Display', serif; font-size: 2.2rem; font-weight: 800;
  background: linear-gradient(135deg, #a855f7, #22d3ee);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.banner-lbl { font-size: 0.75rem; color: var(--t4); text-transform: uppercase; letter-spacing: 0.1em; }

/* ══ TOPIC GRID ══ */
.section-title { font-size: 1.2rem; font-weight: 800; color: #fff; margin: 1.2rem 0 0.75rem; }
.topic-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 0.75rem; }
@media (min-width: 600px) { .topic-grid { grid-template-columns: repeat(3, 1fr); } }
@media (min-width: 900px) { .topic-grid { grid-template-columns: repeat(5, 1fr); } }
.topic-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--r); padding: 1rem 0.75rem; text-align: center; transition: all 0.2s; }
.topic-card:hover { border-color: var(--violet); transform: translateY(-3px); }
.topic-icon { font-size: 1.6rem; margin-bottom: 0.4rem; display: block; }
.topic-name { font-weight: 700; font-size: 0.82rem; color: #fff; margin-bottom: 0.25rem; }
.topic-desc { font-size: 0.68rem; color: var(--t4); line-height: 1.4; }

/* ══ FEATURE GRID ══ */
.feature-grid { display: grid; grid-template-columns: 1fr; gap: 0.75rem; margin: 1rem 0; }
@media (min-width: 600px) { .feature-grid { grid-template-columns: repeat(3, 1fr); } }
.feature-card { background: linear-gradient(135deg, var(--bg-card), rgba(124,58,237,0.06)); border: 1px solid var(--border2); border-radius: var(--rl); padding: 1.2rem; }
.feature-icon { font-size: 1.8rem; margin-bottom: 0.6rem; display: block; }
.feature-title { font-weight: 800; font-size: 1rem; color: #fff; margin-bottom: 0.4rem; }
.feature-desc { font-size: 0.83rem; color: var(--t3); line-height: 1.6; }

/* ══════════════════════════════════════════════════════
   CARDS
══════════════════════════════════════════════════════ */
.card {
  background: var(--bg-card); border: 1px solid var(--border);
  border-radius: var(--rl); padding: 1.5rem; position: relative; overflow: hidden;
  transition: border-color 0.2s, transform 0.2s, box-shadow 0.2s; box-shadow: var(--shadow-card);
}
.card:hover { border-color: var(--border2); transform: translateY(-3px); box-shadow: 0 8px 40px rgba(0,0,0,0.5); }
.card-accent-top { position: absolute; top: 0; left: 0; right: 0; height: 2px; border-radius: var(--rl) var(--rl) 0 0; }
.card-title { font-family: 'Playfair Display', serif; font-size: 1.05rem; font-weight: 700; color: var(--t1); margin-bottom: 0.5rem; letter-spacing: -0.01em; }
.card-desc { font-size: 0.83rem; color: var(--t2); line-height: 1.65; }
.card-meta { display: flex; gap: 0.4rem; flex-wrap: wrap; margin-top: 0.9rem; }
.config-card { background: var(--bg-card); border: 1px solid var(--border2); border-radius: var(--rl); padding: 1.2rem; margin-bottom: 1rem; }

/* ══ CHIPS ══ */
.chip { font-size: 0.66rem; font-weight: 700; letter-spacing: 0.04em; padding: 0.2rem 0.55rem; border-radius: 4px; background: var(--surface3); color: var(--t3); border: 1px solid var(--border2); }
.chip.amber  { background: rgba(251,191,36,0.12);  color: var(--gold);   border-color: rgba(251,191,36,0.3); }
.chip.teal   { background: rgba(34,211,238,0.1);   color: var(--cyan2);  border-color: rgba(34,211,238,0.25); }
.chip.emerald{ background: rgba(16,185,129,0.1);   color: #34d399;       border-color: rgba(16,185,129,0.25); }
.chip.rose   { background: rgba(244,63,94,0.1);    color: #fb7185;       border-color: rgba(244,63,94,0.25); }
.chip.indigo { background: rgba(99,102,241,0.12);  color: #818cf8;       border-color: rgba(99,102,241,0.25); }
.chip.violet { background: rgba(124,58,237,0.15);  color: #c084fc;       border-color: rgba(124,58,237,0.3); }

/* ══ PYQ YEAR CARDS ══ */
.year-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--r-md); padding: 1rem 0.6rem; text-align: center; cursor: pointer; transition: all 0.2s; position: relative; overflow: hidden; }
.year-card::after { content: ''; position: absolute; bottom: 0; left: 0; right: 0; height: 2px; background: linear-gradient(90deg, var(--violet), var(--cyan)); transform: scaleX(0); transform-origin: left; transition: transform 0.25s ease; }
.year-card:hover { border-color: var(--violet); background: rgba(124,58,237,0.08); }
.year-card:hover::after { transform: scaleX(1); }
.year-num { font-family: 'Playfair Display', serif; font-size: 1.2rem; font-weight: 800; color: var(--violet2); display: block; letter-spacing: -0.02em; }
.year-count { font-size: 0.62rem; color: var(--t3); margin-top: 0.25rem; line-height: 1.6; }

/* ══════════════════════════════════════════════════════
   QUIZ ENGINE
══════════════════════════════════════════════════════ */
.quiz-header { display: flex; align-items: center; gap: 0.5rem; flex-wrap: wrap; margin-bottom: 0.5rem; }
.q-counter { color: var(--t2); font-size: 0.88rem; font-weight: 600; }
.q-topic-badge { background: rgba(124,58,237,0.25); color: #c084fc; border: 1px solid rgba(168,85,247,0.6); padding: 0.2rem 0.65rem; border-radius: 20px; font-size: 0.72rem; font-weight: 700; }
.q-diff-badge { padding: 0.2rem 0.65rem; border-radius: 20px; font-size: 0.72rem; font-weight: 700; }
.diff-easy   { background: rgba(16,185,129,0.2);  color: #34d399; border: 1px solid rgba(16,185,129,0.5); }
.diff-medium { background: rgba(251,191,36,0.2);  color: #fbbf24; border: 1px solid rgba(251,191,36,0.5); }
.diff-hard   { background: rgba(244,63,94,0.2);   color: #fb7185; border: 1px solid rgba(244,63,94,0.5); }

/* Timer */
.timer-box { background: linear-gradient(135deg, rgba(34,211,238,0.15), rgba(124,58,237,0.1)); border: 1px solid rgba(34,211,238,0.4); border-radius: 10px; padding: 0.4rem 0.8rem; font-family: 'JetBrains Mono', monospace; font-size: 1rem; color: #22d3ee; font-weight: 700; }
.timer-display { font-family: 'JetBrains Mono', monospace; font-size: 1.05rem; font-weight: 600; padding: 0.35rem 1rem; border-radius: var(--r-sm); border: 1px solid; min-width: 5.5rem; text-align: center; letter-spacing: 0.05em; }
.timer-ok   { color: var(--cyan);  border-color: rgba(34,211,238,0.3);  background: rgba(34,211,238,0.07); }
.timer-warn { color: var(--gold);  border-color: rgba(251,191,36,0.3);  background: rgba(251,191,36,0.07); }
.timer-crit { color: var(--red);   border-color: rgba(244,63,94,0.35);  background: rgba(244,63,94,0.08); animation: pulse-crit 0.8s ease-in-out infinite; }
@keyframes pulse-crit { 0%,100%{opacity:1;} 50%{opacity:0.65; box-shadow:0 0 12px rgba(244,63,94,0.4);} }

/* Progress */
.progress-track { height: 3px; background: var(--border); border-radius: 10px; margin-bottom: 1.25rem; overflow: hidden; }
.progress-fill { height: 100%; border-radius: 10px; background: linear-gradient(90deg, var(--violet), var(--cyan)); transition: width 0.5s cubic-bezier(0.4,0,0.2,1); }

/* Progress bar */
.stProgress > div > div > div > div { background: linear-gradient(90deg, var(--violet), var(--violet2), var(--cyan)) !important; border-radius: 10px !important; }

/* Question card */
.question-card, .question-wrap {
  background: linear-gradient(135deg, #131929, #0f1724);
  border: 1px solid var(--border2); border-radius: var(--rl);
  padding: 1.4rem 1.2rem; margin: 0.75rem 0 1rem;
  position: relative; overflow: hidden; box-shadow: 0 8px 40px rgba(0,0,0,0.5);
}
@media (min-width: 768px) { .question-card, .question-wrap { padding: 2rem 2.2rem; } }
.question-card::before, .question-wrap::before {
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 4px;
  background: linear-gradient(90deg, var(--violet), var(--violet2), var(--cyan));
}
.question-card::after {
  content: ''; position: absolute; top: 0; left: 0; bottom: 0; width: 4px;
  background: linear-gradient(180deg, var(--violet), var(--cyan));
}
.question-meta { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; }
.q-num-pill { background: linear-gradient(135deg, var(--violet), var(--violet2)); color: #fff; font-size: 0.78rem; font-weight: 800; padding: 0.3rem 0.9rem; border-radius: 20px; font-family: 'JetBrains Mono', monospace; box-shadow: 0 0 12px rgba(124,58,237,0.4); }
.q-num { font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; font-weight: 600; color: var(--violet2); letter-spacing: 0.1em; margin-bottom: 1.1rem; text-transform: uppercase; }
.question-text, .q-text { font-family: 'Playfair Display', serif; font-size: clamp(1rem, 3vw, 1.35rem); font-weight: 700; color: #fff; line-height: 1.75; letter-spacing: -0.01em; }
.bookmark-indicator { color: var(--gold); font-size: 1.1rem; }
.q-tags { display: flex; gap: 0.4rem; flex-wrap: wrap; margin-top: 1rem; }

/* Options */
.opt-selected {
  background: linear-gradient(135deg, rgba(124,58,237,0.3), rgba(168,85,247,0.18));
  border: 2px solid var(--violet2); border-radius: 12px; padding: 0.9rem 1.2rem; margin: 0.4rem 0;
  color: #f0e6ff !important; font-size: 0.97rem; font-weight: 700;
  box-shadow: 0 0 16px rgba(168,85,247,0.25); line-height: 1.5;
}
.opt-dot-sel { color: #c084fc; margin-right: 0.4rem; }

.option-btn { display: block; padding: 0.9rem 1.2rem; border-radius: 12px; margin: 0.4rem 0; font-size: 0.95rem; font-weight: 600; cursor: default; border: 2px solid; line-height: 1.5; }
.correct-opt { background: rgba(16,185,129,0.15); border-color: var(--green); color: #34d399; box-shadow: 0 0 16px rgba(16,185,129,0.2); }
.wrong-opt   { background: rgba(244,63,94,0.12);  border-color: var(--red);   color: #fb7185; }
.neutral-opt { background: rgba(30,45,69,0.6);    border-color: var(--border2); color: var(--t3); }

/* Keep old class aliases */
.opt-correct { background: rgba(16,185,129,0.15) !important; border-color: var(--green) !important; color: #34d399 !important; }
.opt-wrong   { background: rgba(244,63,94,0.12)  !important; border-color: var(--red)   !important; color: #fb7185 !important; }
.opt-neutral { background: rgba(30,45,69,0.6)    !important; border-color: var(--border2) !important; color: var(--t3) !important; }

.opt-btn {
  display: block; width: 100%; text-align: left;
  padding: 0.9rem 1.2rem; background: var(--bg2);
  border: 1.5px solid var(--border); border-radius: 12px;
  color: var(--t1) !important; font-size: 0.93rem; font-weight: 500;
  cursor: pointer; transition: all 0.15s ease; line-height: 1.55; font-family: 'DM Sans', sans-serif;
}
.opt-btn:hover { border-color: var(--violet2); background: rgba(124,58,237,0.07) !important; }
.opt-btn::before { content: ''; position: absolute; left: 0; top: 0; bottom: 0; width: 3px; border-radius: 12px 0 0 12px; background: transparent; transition: background 0.15s; }
.opt-btn:hover::before { background: var(--violet); }

/* Explanation */
.explanation-box, .explanation {
  background: linear-gradient(135deg, rgba(124,58,237,0.12), rgba(34,211,238,0.06));
  border: 1px solid rgba(124,58,237,0.4); border-left: 3px solid var(--violet);
  border-radius: var(--r); padding: 1.1rem; margin-top: 1rem;
}
.exp-title, .exp-head { font-weight: 800; color: #c084fc; margin-bottom: 0.4rem; font-size: 0.9rem; display: flex; align-items: center; gap: 0.5rem; }
.exp-text, .exp-body { color: var(--t2); font-size: 0.9rem; line-height: 1.7; }

/* ══════════════════════════════════════════════════════
   EXAM NAVIGATOR PANEL
══════════════════════════════════════════════════════ */
.exam-panel { background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--r-lg); padding: 1.25rem; position: sticky; top: 4.5rem; box-shadow: var(--shadow-card); }
.exam-panel-title { font-size: 0.68rem; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: var(--t3); margin-bottom: 0.85rem; padding-bottom: 0.6rem; border-bottom: 1px solid var(--border); }
.exam-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(2.3rem, 1fr)); gap: 0.3rem; max-height: 16rem; overflow-y: auto; margin-bottom: 0.75rem; }
.exam-q-btn { aspect-ratio: 1; border-radius: var(--r-sm); border: 1px solid var(--border); background: var(--bg2); color: var(--t3); font-size: 0.68rem; font-weight: 700; display: flex; align-items: center; justify-content: center; cursor: pointer; transition: all 0.12s; font-family: 'JetBrains Mono', monospace; }
.exam-q-btn:hover { border-color: var(--violet2); color: var(--violet2); }
.exam-q-btn.answered { background: rgba(16,185,129,0.12); border-color: rgba(16,185,129,0.4); color: var(--green); }
.exam-q-btn.current  { background: var(--violet); border-color: var(--violet); color: #fff; box-shadow: 0 0 12px rgba(124,58,237,0.4); }
.exam-q-btn.skipped  { background: rgba(251,191,36,0.12); border-color: rgba(251,191,36,0.35); color: var(--gold); }
.exam-legend { display: flex; gap: 0.85rem; flex-wrap: wrap; font-size: 0.64rem; color: var(--t3); margin-top: 0.6rem; }
.legend-dot { display: inline-block; width: 7px; height: 7px; border-radius: 2px; margin-right: 3px; }

/* ══════════════════════════════════════════════════════
   RESULTS PAGE
══════════════════════════════════════════════════════ */
.result-hero, .results-hero {
  text-align: center; padding: 2.5rem 1.5rem 2rem;
  background: linear-gradient(135deg, #131929, rgba(124,58,237,0.08));
  border-radius: var(--rl); border: 1px solid var(--border2); margin-bottom: 1.75rem;
  position: relative; overflow: hidden;
}
.result-hero::before, .results-hero::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px; background: linear-gradient(90deg, var(--violet), var(--cyan), var(--gold)); }
.grade-letter, .results-grade { font-family: 'Playfair Display', serif; font-size: 4rem; font-weight: 900; line-height: 1; display: block; margin-bottom: 0.5rem; filter: drop-shadow(0 0 20px currentColor); }
.result-score, .results-score { font-family: 'JetBrains Mono', monospace; font-size: 2rem; font-weight: 600; color: var(--t1); letter-spacing: -0.02em; }
.result-pct, .results-pct { font-size: 1rem; color: var(--t2); margin: 0.4rem 0; }
.result-msg, .results-msg { font-family: 'Playfair Display', serif; font-size: 1rem; color: var(--gold); font-style: italic; margin-top: 0.5rem; }

.stat-card-mini, .result-stat-card {
  background: var(--bg-card); border: 1px solid var(--border2); border-radius: var(--r-md);
  padding: 1rem 0.75rem; text-align: center; border-top-width: 3px; transition: transform 0.2s;
}
.stat-card-mini:hover, .result-stat-card:hover { transform: translateY(-2px); }
.stat-card-mini .val, .rs-val { font-family: 'JetBrains Mono', monospace; font-size: 1.65rem; font-weight: 700; display: block; line-height: 1.1; margin-bottom: 0.25rem; }
.stat-card-mini .lbl, .rs-lbl { font-size: 0.64rem; color: var(--t3); text-transform: uppercase; letter-spacing: 0.1em; font-weight: 700; }

/* ══════════════════════════════════════════════════════
   LEADERBOARD
══════════════════════════════════════════════════════ */
.lb-row { display: flex; align-items: center; gap: 0.85rem; padding: 0.85rem 1.1rem; background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--r-md); margin-bottom: 0.4rem; transition: all 0.15s; }
.lb-row:hover { border-color: var(--border2); transform: translateX(3px); }
.lb-row.me { border-color: rgba(251,191,36,0.5) !important; background: linear-gradient(90deg, rgba(251,191,36,0.06), transparent) !important; }
.lb-rank { font-family: 'Playfair Display', serif; font-size: 1.1rem; font-weight: 800; min-width: 2rem; text-align: center; }
.lb-rank.gold   { color: var(--gold); }
.lb-rank.silver { color: #9fb3cc; }
.lb-rank.bronze { color: #b87333; }
.lb-rank.rest   { color: var(--t4); font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; }
.lb-avatar { width: 2.4rem; height: 2.4rem; border-radius: 50%; flex-shrink: 0; background: linear-gradient(135deg, var(--violet), var(--cyan)); display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 0.78rem; color: #fff; box-shadow: 0 0 0 2px rgba(124,58,237,0.2); }
.lb-name { font-weight: 600; font-size: 0.9rem; color: var(--t1); }
.lb-detail { font-size: 0.68rem; color: var(--t3); margin-top: 0.15rem; }
.lb-score { font-family: 'JetBrains Mono', monospace; font-size: 0.9rem; font-weight: 600; color: var(--cyan2); text-align: right; }
.podium-card { background: var(--bg-card); border: 1px solid var(--border2); border-radius: var(--r-lg); padding: 1.5rem 1rem; text-align: center; transition: transform 0.2s; }
.podium-card:hover { transform: translateY(-4px); }
.podium-card.first { border-color: rgba(251,191,36,0.4); background: linear-gradient(180deg, rgba(251,191,36,0.06), transparent); }

/* ══════════════════════════════════════════════════════
   LOGIN PAGE
══════════════════════════════════════════════════════ */
.login-wrap { max-width: 440px; margin: 3rem auto; background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--rl); padding: 3rem 2.5rem; text-align: center; box-shadow: 0 20px 60px rgba(0,0,0,0.5); position: relative; overflow: hidden; }
.login-wrap::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px; background: linear-gradient(90deg, var(--violet), var(--cyan)); }
.login-logo { font-size: 3rem; margin-bottom: 1rem; display: block; filter: drop-shadow(0 4px 12px rgba(124,58,237,0.3)); }
.login-title { font-family: 'Playfair Display', serif; font-size: 1.8rem; font-weight: 800; color: var(--t1); margin-bottom: 0.4rem; letter-spacing: -0.02em; }
.login-sub { font-size: 0.85rem; color: var(--t2); margin-bottom: 2rem; line-height: 1.6; }

/* ══════════════════════════════════════════════════════
   ANALYTICS
══════════════════════════════════════════════════════ */
.analytics-card { background: var(--bg-card); border: 1px solid var(--border2); border-radius: var(--r); padding: 1.1rem 1.3rem; margin-bottom: 1rem; }
.ac-title { font-size: 0.78rem; color: var(--t4); text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.3rem; font-weight: 600; }
.ac-val { font-size: 2rem; font-weight: 800; font-family: 'JetBrains Mono', monospace; display: block; }
.ac-sub { font-size: 0.8rem; color: var(--t3); }

/* ══ PDF UPLOAD ══ */
.pdf-intro { background: linear-gradient(135deg, rgba(34,211,238,0.1), rgba(124,58,237,0.07)); border: 1px solid rgba(34,211,238,0.35); border-radius: var(--r); padding: 1rem 1.3rem; color: var(--t2); font-size: 0.9rem; margin-bottom: 1.2rem; line-height: 1.7; }
.step-list { display: flex; flex-direction: column; gap: 0.7rem; }
.step-item { display: flex; align-items: center; gap: 0.7rem; font-size: 0.85rem; color: var(--t3); }
.step-num { width: 26px; height: 26px; background: linear-gradient(135deg, var(--violet), var(--cyan)); color: #fff; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.72rem; font-weight: 800; flex-shrink: 0; }

/* ══ EMPTY STATE ══ */
.empty-state { text-align: center; padding: 4rem 2rem; color: var(--t3); }
.empty-state .icon, .empty-icon { font-size: 2.5rem; display: block; margin-bottom: 1rem; opacity: 0.5; }
.empty-state h3, .empty-title { font-family: 'Playfair Display', serif; color: var(--t2); margin-bottom: 0.4rem; font-size: 1.2rem; font-weight: 700; }
.empty-desc { color: var(--t4); font-size: 0.88rem; }

/* ══════════════════════════════════════════════════════
   STREAMLIT WIDGET OVERRIDES — MAKE TEXT VISIBLE
══════════════════════════════════════════════════════ */
button { color: #e2e8f0 !important; font-family: 'DM Sans', sans-serif !important; }
button > div { color: inherit !important; }
button > div > p { color: inherit !important; font-size: inherit !important; }
button p, button span { color: inherit !important; }

.stButton > button { border-radius: 10px !important; font-weight: 600 !important; font-size: 0.9rem !important; transition: all 0.2s !important; font-family: 'DM Sans', sans-serif !important; }
.stButton > button[kind="secondary"], [data-testid="baseButton-secondary"] { background: var(--bg-card) !important; color: #e2e8f0 !important; border: 2px solid var(--border2) !important; }
.stButton > button[kind="primary"], [data-testid="baseButton-primary"] { background: linear-gradient(135deg, var(--violet), var(--violet2)) !important; color: #ffffff !important; border: none !important; box-shadow: 0 4px 20px rgba(124,58,237,0.4) !important; }
.stButton > button[kind="primary"] *, [data-testid="baseButton-primary"] * { color: #fff !important; }
.stButton > button[kind="primary"]:hover, [data-testid="baseButton-primary"]:hover { box-shadow: 0 6px 28px rgba(124,58,237,0.55) !important; transform: translateY(-2px) !important; }
.stButton > button[kind="secondary"]:hover, [data-testid="baseButton-secondary"]:hover { background: var(--surface2) !important; border-color: var(--border2) !important; }

div[data-testid="stForm"] { border: none !important; padding: 0 !important; background: transparent !important; margin: 0 !important; }
div[data-testid="stForm"] button { color: #e2e8f0 !important; }
div[data-testid="stForm"] button > div { color: inherit !important; }
div[data-testid="stForm"] button > div > p { color: inherit !important; }
div[data-testid="stForm"] button[kind="primaryFormSubmit"] { background: linear-gradient(135deg, var(--violet), var(--violet2)) !important; color: #fff !important; border: none !important; box-shadow: 0 4px 20px rgba(124,58,237,0.4) !important; }

.stRadio label { color: var(--t2) !important; }
.stRadio label p, .stRadio label span { color: inherit !important; }
.stCheckbox label { color: var(--t2) !important; font-weight: 500 !important; }
.stCheckbox label span { color: #fff !important; }
.stSelectbox label, .stMultiSelect label, .stSlider label, .stRadio label,
.stCheckbox label, .stTextInput label, .stTextArea label,
.stToggle label, .stSelectSlider label, .stNumberInput label { color: var(--t3) !important; font-weight: 600 !important; font-size: 0.82rem !important; }
div[data-baseweb="select"] { background: var(--bg-card) !important; border-color: var(--border2) !important; border-radius: 10px !important; }
div[data-baseweb="select"] * { color: var(--t1) !important; }
.stTextInput input, .stTextArea textarea { background: var(--bg-card) !important; border-color: var(--border2) !important; color: #fff !important; border-radius: 10px !important; font-family: 'DM Sans', sans-serif !important; }
.stTextInput input:focus, .stTextArea textarea:focus { border-color: var(--violet) !important; box-shadow: 0 0 0 3px rgba(124,58,237,0.15) !important; }
.stInfo    { background: rgba(124,58,237,0.12) !important; border-color: rgba(124,58,237,0.5) !important; color: var(--t2) !important; border-radius: 10px !important; }
.stSuccess { background: rgba(16,185,129,0.12) !important; border-color: rgba(16,185,129,0.5) !important; color: #6ee7b7 !important; border-radius: 10px !important; }
.stError   { background: rgba(244,63,94,0.12)  !important; border-color: rgba(244,63,94,0.5)  !important; color: #fda4af !important; border-radius: 10px !important; }
.stWarning { background: rgba(251,191,36,0.12) !important; border-color: rgba(251,191,36,0.5) !important; color: #fde68a !important; border-radius: 10px !important; }
.streamlit-expanderHeader { background: var(--bg-card) !important; border-color: var(--border2) !important; color: #fff !important; border-radius: var(--r) !important; }
[data-testid="stFileUploader"] { background: var(--bg-card) !important; border: 2px dashed var(--border2) !important; border-radius: var(--r) !important; }
.stTabs [data-baseweb="tab-list"] { background: var(--bg-card) !important; border-radius: 10px !important; gap: 0 !important; padding: 3px !important; border: 1px solid var(--border) !important; }
.stTabs [data-baseweb="tab"] { border-radius: 8px !important; color: var(--t2) !important; font-weight: 600 !important; }
.stTabs [aria-selected="true"] { background: var(--bg2) !important; color: #fff !important; box-shadow: 0 1px 4px rgba(0,0,0,0.3) !important; }
.stTabs [data-baseweb="tab-border"] { display: none !important; }
.stRadio [role="radio"] { accent-color: var(--violet) !important; }
.stToggle input:checked + div { background: var(--violet) !important; }
[data-baseweb="tag"] { background: rgba(124,58,237,0.15) !important; border-color: rgba(124,58,237,0.3) !important; }
[data-baseweb="tag"] span { color: #c084fc !important; }
[data-testid="stSidebar"] button { color: var(--t3) !important; }
[data-testid="stSidebar"] button[kind="primary"] { color: #fff !important; }
div[data-testid="metric-container"] { background: var(--bg-card) !important; border: 1px solid var(--border2) !important; border-radius: var(--r) !important; padding: 1rem !important; }
hr { border: none !important; border-top: 1px solid var(--border) !important; margin: 1.5rem 0 !important; }
.divider { height: 1px; background: var(--border); margin: 1.5rem 0; }
.text-muted { color: var(--t2); font-size: 0.85rem; }
.text-tiny  { color: var(--t3); font-size: 0.72rem; }


/* ══════════════════════════════════════════════════════
   MOBILE-NATIVE RESPONSIVE OVERRIDES  (≤ 600px)
══════════════════════════════════════════════════════ */

/* ── Base layout ── */
@media (max-width: 600px) {
  /* Full-bleed content, no wasted margin */
  .main .block-container { padding: 0.5rem 0.5rem 5rem !important; }

  /* Streamlit column stacking */
  [data-testid="column"] { min-width: 100% !important; }

  /* Sidebar: auto-collapse on mobile */
  [data-testid="stSidebar"] { min-width: 200px !important; max-width: 78vw !important; }

  /* ── Hero ── */
  .hero, .hero-section { padding: 2rem 0.75rem 1.5rem !important; }
  .hero-title { font-size: clamp(1.7rem, 8vw, 2.6rem) !important; }
  .hero-badge { font-size: 0.65rem !important; padding: 0.3rem 0.75rem !important; }
  .hero-features { gap: 0.4rem !important; }
  .hero-pill { font-size: 0.7rem !important; padding: 0.28rem 0.65rem !important; }

  /* ── Stat strip: 3 columns, hide last 3 less-critical cells ── */
  .stat-strip { grid-template-columns: repeat(3, 1fr) !important; max-width: 100% !important; }
  .stat-strip .stat-cell:nth-child(n+4) { display: none !important; }
  .stat-val { font-size: 1.4rem !important; }
  .stat-icon { font-size: 1rem !important; }

  /* ── Section labels ── */
  .section-label { font-size: 0.8rem !important; }

  /* ── Cards: single column ── */
  .card { padding: 1rem !important; }
  .card-title { font-size: 0.95rem !important; }
  .card-desc  { font-size: 0.75rem !important; }

  /* ── Year cards ── */
  .year-num { font-size: 1.1rem !important; }
  .year-count { font-size: 0.6rem !important; }

  /* ── Quiz / question card ── */
  .question-wrap, .question-card { padding: 1rem 0.85rem !important; }
  .q-num { font-size: 0.6rem !important; }
  .q-text, .question-text { font-size: clamp(0.9rem, 4vw, 1.1rem) !important; line-height: 1.65 !important; }
  .q-tags { gap: 0.3rem !important; }
  .meta-chip { font-size: 0.6rem !important; padding: 0.15rem 0.5rem !important; }

  /* ── Options ── */
  .opt-selected, .option-btn, .correct-opt, .wrong-opt, .neutral-opt {
    font-size: 0.85rem !important; padding: 0.75rem 0.9rem !important;
    border-radius: 10px !important;
  }

  /* ── Timer ── */
  .timer-display { font-size: 0.9rem !important; padding: 0.3rem 0.7rem !important; min-width: 4rem !important; }

  /* ── Explanation box ── */
  .explanation-box { padding: 0.85rem !important; font-size: 0.8rem !important; }
  .exp-title { font-size: 0.75rem !important; }

  /* ── Page headers ── */
  .page-header h1 { font-size: 1.3rem !important; }
  .page-header p  { font-size: 0.8rem !important; }

  /* ── Leaderboard ── */
  .lb-row { padding: 0.65rem 0.75rem !important; gap: 0.5rem !important; }
  .lb-name { font-size: 0.8rem !important; }
  .lb-detail { font-size: 0.65rem !important; }
  .lb-score { font-size: 0.95rem !important; }
  .lb-avatar { width: 1.8rem !important; height: 1.8rem !important; font-size: 0.65rem !important; }

  /* ── Login card ── */
  .login-wrap { margin: 1rem auto !important; padding: 1.5rem 1.25rem !important; }

  /* ── Results card ── */
  .result-hero, .results-hero { padding: 1.5rem 1rem !important; }
  .result-score { font-size: clamp(2rem, 12vw, 3.5rem) !important; }

  /* ── PYQ year row buttons (3-col → flex wrap) ── */
  .pyq-launch-row { flex-direction: column !important; gap: 0.35rem !important; }

  /* ── Exam navigator panel: hide on very small screens ── */
  .exam-panel { display: none !important; }

  /* ── Buttons: better tap targets ── */
  .stButton button { min-height: 44px !important; font-size: 0.88rem !important; }

  /* ── Bottom nav spacing for thumb reachability ── */
  .stButton:last-child { margin-bottom: 1rem !important; }

  /* ── Scrollable tab overflow ── */
  .stTabs [data-baseweb="tab-list"] { overflow-x: auto !important; flex-wrap: nowrap !important; }
}

/* ── Tablet tweaks (601px – 900px) ── */
@media (min-width: 601px) and (max-width: 900px) {
  .main .block-container { padding: 1rem 1.25rem 3rem !important; }
  .hero-title { font-size: clamp(2rem, 5vw, 3rem) !important; }
  .stat-strip { grid-template-columns: repeat(4, 1fr) !important; }
  .stat-strip .stat-cell:nth-child(n+5) { display: none !important; }
  .card-title { font-size: 1rem !important; }
  .stButton button { min-height: 42px !important; }
}

</style>

<script>
(function forceButtonColors(){
    function fix(){
        document.querySelectorAll('button').forEach(function(b){
            b.querySelectorAll('p,span,div').forEach(function(el){
                el.style.setProperty('color','inherit','important');
            });
        });
    }
    fix();
    new MutationObserver(fix).observe(document.body,{childList:true,subtree:true});
})();
</script>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════
# QUESTION BANK
# ═══════════════════════════════════════════════
# ╔══════════════════════════════════════════════════════════════════════╗
# ║              UGC NET PAPER 1 — QUESTION BANK                        ║
# ║  Organised by topic. To add questions, paste new dicts into the     ║
# ║  matching Q_<TOPIC> list below, then save. That's it!               ║
# ║                                                                      ║
# ║  TEMPLATE (copy-paste and fill):                                     ║
# ║  {"id":"ta009","topic":"Teaching Aptitude",                          ║
# ║   "difficulty":"Easy|Medium|Hard",                                   ║
# ║   "year":2024,"season":"June|December",                              ║
# ║   "question":"Your question?",                                       ║
# ║   "options":["A","B","C","D"],                                       ║
# ║   "correct_answer":"A",                                              ║
# ║   "explanation":"Why A is correct."},                                ║
# ╚══════════════════════════════════════════════════════════════════════╝

# ── 1. TEACHING APTITUDE ─────────────────────────────────────────────
Q_TEACHING_APTITUDE = [
    {"id":"ta001","topic":"Teaching Aptitude","difficulty":"Medium","year":2023,"season":"June","question":"Which level of teaching focuses on the development of thinking power and reasoning in students?","options":["Memory level","Understanding level","Reflective level","None of these"],"correct_answer":"Reflective level","explanation":"Reflective level teaching by Morrison focuses on critical thinking, problem-solving, and independent reasoning."},
    {"id":"ta002","topic":"Teaching Aptitude","difficulty":"Easy","year":2022,"season":"December","question":"Which of the following is NOT a characteristic of effective teaching?","options":["Clarity of goals","Flexibility","Dogmatic approach","Student-centered learning"],"correct_answer":"Dogmatic approach","explanation":"Effective teaching is flexible and student-centered; a dogmatic approach hinders learning."},
    {"id":"ta003","topic":"Teaching Aptitude","difficulty":"Hard","year":2023,"season":"December","question":"In the context of Bloom's Taxonomy (revised), which cognitive level represents the highest order of thinking?","options":["Evaluation","Synthesis","Creating","Analysis"],"correct_answer":"Creating","explanation":"The revised Bloom's Taxonomy places 'Creating' at the apex — generating new ideas, products, or ways of viewing things."},
    {"id":"ta004","topic":"Teaching Aptitude","difficulty":"Medium","year":2021,"season":"June","question":"Which teaching method is most appropriate for large classrooms with heterogeneous groups?","options":["Project Method","Lecture Method","Inquiry Method","Seminar Method"],"correct_answer":"Lecture Method","explanation":"The lecture method is most practical for large, heterogeneous groups."},
    {"id":"ta005","topic":"Teaching Aptitude","difficulty":"Medium","year":2020,"season":"June","question":"The concept of 'Micro-Teaching' was first developed at:","options":["Harvard University","Stanford University","Yale University","MIT"],"correct_answer":"Stanford University","explanation":"Micro-teaching was developed by Dwight W. Allen at Stanford University in 1963."},
    {"id":"ta006","topic":"Teaching Aptitude","difficulty":"Easy","year":2019,"season":"June","question":"Which of the following best describes 'formative evaluation'?","options":["Evaluation at the end of the course","Evaluation to assign final grades","Ongoing evaluation during instruction","Evaluation before the course begins"],"correct_answer":"Ongoing evaluation during instruction","explanation":"Formative evaluation is continuous assessment conducted during the instructional process."},
    {"id":"ta007","topic":"Teaching Aptitude","difficulty":"Hard","year":2018,"season":"December","question":"Which theory proposes that students have different 'learning styles'?","options":["Constructivism","VAK/VARK Model","Behaviorism","Gestalt Theory"],"correct_answer":"VAK/VARK Model","explanation":"The VARK model categorizes learners by Visual, Auditory, Read/Write, and Kinesthetic modes."},
    {"id":"ta008","topic":"Teaching Aptitude","difficulty":"Medium","year":2022,"season":"June","question":"The 'Socratic Method' of teaching primarily involves:","options":["Lecture and demonstration","Asking probing questions","Group projects","Use of audio-visual aids"],"correct_answer":"Asking probing questions","explanation":"The Socratic method uses disciplined questioning to stimulate critical thinking."},
    # ════════════════════════════════════════════════════════════════════
    # ADD MORE Teaching Aptitude QUESTIONS BELOW ↓  (paste here, save, done)
    # ════════════════════════════════════════════════════════════════════
    # SAMPLE — copy format, fill your own content, delete these when done:
    {"id":"ta009","topic":"Teaching Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"Which of the following is an example of intrinsic motivation in students?",
     "options":["Fear of punishment","Desire for rewards","Curiosity and love of learning","Peer pressure"],
     "correct_answer":"Curiosity and love of learning",
     "explanation":"Intrinsic motivation comes from within — driven by genuine interest, curiosity, or personal satisfaction."},

    {"id":"ta010","topic":"Teaching Aptitude","difficulty":"Hard","year":2024,"season":"December",
     "question":"The concept of 'Zone of Proximal Development' was proposed by:",
     "options":["Jean Piaget","Lev Vygotsky","Jerome Bruner","B.F. Skinner"],
     "correct_answer":"Lev Vygotsky",
     "explanation":"Vygotsky's ZPD is the gap between what a learner can do independently and what they can achieve with guidance."},

    {"id":"ta011","topic":"Teaching Aptitude","difficulty":"Easy","year":2023,"season":"June",
     "question":"Which of the following best defines 'pedagogy'?",
     "options":["Study of child development","Art and science of teaching","School administration","Curriculum design only"],
     "correct_answer":"Art and science of teaching",
     "explanation":"Pedagogy refers to the theory and practice of education — how teachers teach and how learners learn."},

    {"id":"ta012","topic":"Teaching Aptitude","difficulty":"Medium","year":2022,"season":"December",
     "question":"'Summative evaluation' is conducted:",
     "options":["During instruction","Before instruction","At the end of instruction","Only for teachers"],
     "correct_answer":"At the end of instruction",
     "explanation":"Summative evaluation assesses learning at the end of an instructional unit or course."},

    {"id":"ta013","topic":"Teaching Aptitude","difficulty":"Hard","year":2021,"season":"December",
     "question":"Which of the following is NOT a principle of constructivism?",
     "options":["Learning is active","Knowledge is constructed by learners","Teacher is the sole authority","Prior knowledge matters"],
     "correct_answer":"Teacher is the sole authority",
     "explanation":"Constructivism holds that learners build knowledge actively; the teacher is a facilitator, not the sole authority."},
    {"id":"ta014","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"Description of 'actual words, written or spoken, used to tell a story' and images or pictures come under the category of",
     "options":["Discourse", "Event", "Law", "Performance"],
     "correct_answer":"Discourse",
     "explanation":"The correct answer is (A) Discourse. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta015","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"A collection of the student's work in an area, showing growth, self reflection, and achievements is known as:",
     "options":["Modelling", "Portfolio", "Mastery goal", "Problem solving"],
     "correct_answer":"Portfolio",
     "explanation":"The correct answer is (B) Portfolio. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta016","topic":"Teaching Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"If the statement \"Some birds are not mammals\" is given as true, which of the following statements can be immediately inferred to be false?",
     "options":["Some mammals are not birds.", "Some birds are mammals.", "No birds are mammals.", "All birds are mammals."],
     "correct_answer":"All birds are mammals.",
     "explanation":"The correct answer is (D) All birds are mammals.. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta017","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"Working 9 hours a day, 12 persons complete a work in 25 days. Working 6 hours a day, 15 persons can do the same work in",
     "options":["28 days", "29 days", "30 days", "32 days"],
     "correct_answer":"30 days",
     "explanation":"The correct answer is (C) 30 days. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta018","topic":"Teaching Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"Arrange the probabilities corresponding to the standard normal variate 'z' lying in the following intervals, in increasing order. (a) − ∞ ≤ z ≤ + 1 (b) 0 ≤ z ≤ + 3 (c) – 1 ≤ z ≤ + 1 (d) z ≥ + 1",
     "options":["(d), (b), (c), (a)", "(c), (b), (d), (a)", "(a), (c), (b), (d)", "(b), (d), (a), (c)"],
     "correct_answer":"(d), (b), (c), (a)",
     "explanation":"The correct answer is (A) (d), (b), (c), (a). This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta019","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"A British official of the East India company who was interested in higher learning in India was.",
     "options":["Francis Gladwin", "William Ward", "William Adam", "William Jones"],
     "correct_answer":"William Jones",
     "explanation":"The correct answer is (D) William Jones. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta021","topic":"Teaching Aptitude","difficulty":"Hard","year":2024,"season":"June",
     "question":"Which of the following norms are prescribed for foreign universities to set up their campuses in India. (a) Foreign universities must invest in the Indian manufacturing industry. (b) They should have secured a position within the top 500 in global ranking. (c) They should have secured a position within the top 500 in global ranking in the subject-wise category. (d) They should employ only Indians for teaching and non-teaching. (e) They should possess outstanding expertise in a specific area.",
     "options":["(a), (b) only", "(b), (c), (d) only", "(c), (d), (e) only", "(b), (c), (e) only"],
     "correct_answer":"(b), (c), (e) only",
     "explanation":"The correct answer is (D) (b), (c), (e) only. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta022","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which higher-order knowledge can make the difference between how well and quickly one's students learn material?",
     "options":["Declarative", "Rote", "Metacognition", "Procedural"],
     "correct_answer":"Metacognition",
     "explanation":"The correct answer is (C) Metacognition. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta023","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"By selling 35 eggs for Rs 30, a man loses 25%. How many eggs should he sell for Rs 144 to gain 20%?",
     "options":["85", "95", "105", "115"],
     "correct_answer":"105",
     "explanation":"The correct answer is (C) 105. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta024","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"In which type of assessment do students measure their own progress against their previous performance rather than against external criteria or peers?",
     "options":["Peer Assessment", "Ipsative Assessment", "Formative Assessment", "Summative Assessment"],
     "correct_answer":"Ipsative Assessment",
     "explanation":"The correct answer is (B) Ipsative Assessment. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta025","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"What is the original source of cultural life of the Hindus?",
     "options":["Itihāsas", "Purānas", "Manu", "Sacred Vedas"],
     "correct_answer":"Sacred Vedas",
     "explanation":"The correct answer is (D) Sacred Vedas. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta029","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"How many boys are enrolled in Soccer and Tennis together?",
     "options":["610", "640", "720", "710"],
     "correct_answer":"710",
     "explanation":"The correct answer is (D) 710. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta031","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"Who invented the Printing process?",
     "options":["G. Marconi", "Tang Dynasty", "William Caxton", "Johannes Gutenberg"],
     "correct_answer":"Johannes Gutenberg",
     "explanation":"The correct answer is (D) Johannes Gutenberg. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta032","topic":"Teaching Aptitude","difficulty":"Hard","year":2024,"season":"June",
     "question":"Which of following are the parts of AYUSH undergraduate education? (a) Siddha (b) Sowa - Rigpa (c) Yoga - Shastra (d) Homoeopathy (e) Sanjeevani",
     "options":["(a), (b) and (e) Only", "(b), (c) and (d) Only", "(a), (b) and (d) Only", "(a), (c) and (e) Only"],
     "correct_answer":"(a), (b) and (d) Only",
     "explanation":"The correct answer is (C) (a), (b) and (d) Only. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta033","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"“Education is the manifestation of perfection already in man” is a statement by:",
     "options":["Rabindranath Tagore", "M.K. Gandhi", "Sri Aurobindo", "Swami Vivekananda"],
     "correct_answer":"Swami Vivekananda",
     "explanation":"The correct answer is (D) Swami Vivekananda. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta034","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"In the context of learning, which of the following DOES NOT represent the self concept?",
     "options":["It is what an individual feels about others.", "It is what an individual feels how others think/perceive of him/her.", "It is an awareness of the individual about his/her strengths.", "It is an awareness of the individual about his/her weaknesses."],
     "correct_answer":"It is what an individual feels about others.",
     "explanation":"The correct answer is (A) It is what an individual feels about others.. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta035","topic":"Teaching Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"Arrange the following fraction in decreasing order: (a) 12 19 (b) 7 12 (c) 11 17 (d) 17 28",
     "options":["(a), (b), (c), (d)", "(c), (a), (d), (b)", "(b), (c), (d), (a)", "(d), (a), (b), (c)"],
     "correct_answer":"(c), (a), (d), (b)",
     "explanation":"The correct answer is (B) (c), (a), (d), (b). This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta036","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which of the following is not a primary air pollutant?",
     "options":["CO", "NO", "O3", "SO2"],
     "correct_answer":"O3",
     "explanation":"The correct answer is (C) O3. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta037","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"Where did nuns and monks meditate, debate and discuss with learned for their quest for knowledge?",
     "options":["Monasteries", "Basadis", "Churches", "Ghatika"],
     "correct_answer":"Monasteries",
     "explanation":"The correct answer is (A) Monasteries. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta038","topic":"Teaching Aptitude","difficulty":"Hard","year":2024,"season":"June",
     "question":"Which of the following correctly represent characteristics of teaching? (a) To provide guidance and training to students (b) Interaction between authorities (c) To provide formal and informal education (d) An art to import knowledge to students in an effective way (e) To prepare policies for corporate bodies",
     "options":["(a) and (b) Only", "(a), (d) and (e) Only", "(a), (c) and (d) Only", "(c), (d) and (e) Only"],
     "correct_answer":"(a), (c) and (d) Only",
     "explanation":"The correct answer is (C) (a), (c) and (d) Only. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta040","topic":"Teaching Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match List - I with List - II. List -I (Word) List -II (Unique Code) (a) PRIME (I) 69 (b) SIGHT (II) 72 (c) QUITE (III) 63 (d) RHYME (IV) 61",
     "options":["(a)-(I), (b)-(II), (c)-(III), (d)-(IV)", "(a)-(II), (b)-(III), (c)-(IV), (d)-(I)", "(a)-(IV), (b)-(III), (c)-(II), (d)-(I)", "(a)-(III), (b)-(IV), (c)-(I), (d)-(II)"],
     "correct_answer":"(a)-(IV), (b)-(III), (c)-(II), (d)-(I)",
     "explanation":"The correct answer is (C) (a)-(IV), (b)-(III), (c)-(II), (d)-(I). This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta041","topic":"Teaching Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"Consider the following snapshot of MS-EXCEL worksheet: A B C 1 90 70 2 60 170 3 150 20 4 30 110 5 50 40 6 130 30 7 What will be the value of the cell C1 containing the formula = SUMIF (A1:A6,\">100\", B1:B6) in the above worksheet?",
     "options":["90", "390", "50", "420"],
     "correct_answer":"50",
     "explanation":"The correct answer is (C) 50. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta042","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"I never teach my pupils; I only attempt to provide the conditions in which they can learn' is a statement by:",
     "options":["Swami Vivekananda", "Albert Einstein", "Sri Aurbindo", "Aristotle"],
     "correct_answer":"Albert Einstein",
     "explanation":"The correct answer is (B) Albert Einstein. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta043","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which of the following activities is NOT included with state government initiative for enrichment?",
     "options":["Bamboo and woodcraft", "Tribal painting", "Stone carving", "Rock Painting"],
     "correct_answer":"Rock Painting",
     "explanation":"The correct answer is (D) Rock Painting. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta044","topic":"Teaching Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"Arrange the following fractions in decreasing order? (a) 17 21 (b) 15 19 (c) 13 16 45 (d) 14 17",
     "options":["(d), (c), (b), (a)", "(a), (b), (c), (d)", "(c), (d), (b), (a)", "(d), (c), (a), (b)"],
     "correct_answer":"(d), (c), (a), (b)",
     "explanation":"The correct answer is (D) (d), (c), (a), (b). This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta045","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"The Sanskrit Commission (1956-57) was headed by-",
     "options":["Sukumar Sen", "U.N. Dhebar", "Suniti Kumar Chatterji", "V.T. Krishnamachari"],
     "correct_answer":"Suniti Kumar Chatterji",
     "explanation":"The correct answer is (C) Suniti Kumar Chatterji. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta046","topic":"Teaching Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match the List-I with List-II List - I (Word) List - II (Unique Code) (a) PRIME (I) NPGKC (b) SIGHT (II) QGEFR (c) QUITE (III) OSGRC (d) RHYME (IV) PFWKC",
     "options":["(a)-(I), (b)-(II), (c)-(III), (d)-(IV)", "(a)-(II), (b)-(III), (c)-(IV), (d)-(I)", "(a)-(III), (b)-(IV), (c)-(I), (d)-(II)", "(a)-(IV), (b)-(I), (c)-(II), (d)-(III)"],
     "correct_answer":"(a)-(I), (b)-(II), (c)-(III), (d)-(IV)",
     "explanation":"The correct answer is (A) (a)-(I), (b)-(II), (c)-(III), (d)-(IV). This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta048","topic":"Teaching Aptitude","difficulty":"Hard","year":2024,"season":"June",
     "question":"According to NEP-2020, which is/are not under curriculum framework of adult education? (a) Critical Life Skills (b) Vocational Skills Development (c) Continuing Education (d) Art in Education (e) Basic Education",
     "options":["(a) only", "(b) and (c) only", "(d) only", "(a), (d) and (e) only"],
     "correct_answer":"(d) only",
     "explanation":"The correct answer is (C) (d) only. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta049","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"What cannot be held as the correct motive of Question-Answer technique in Teaching?",
     "options":["To test the knowledge", "To locate the difficulty", "To intimidate and hamper self-confidence", "To promote thinking and originality"],
     "correct_answer":"To intimidate and hamper self-confidence",
     "explanation":"The correct answer is (C) To intimidate and hamper self-confidence. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta050","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"How many edicts of Ashoka are preserved on a boulder inside the Junagarh caves?",
     "options":["Ten", "Twelve", "Fourteen", "Thirteen"],
     "correct_answer":"Fourteen",
     "explanation":"The correct answer is (C) Fourteen. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta051","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which style of architecture is seen in the Sun Temple of Modhera?",
     "options":["Maru-Gurjara", "Solanki", "Cholan", "Khamboj"],
     "correct_answer":"Maru-Gurjara",
     "explanation":"The correct answer is (A) Maru-Gurjara. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta052","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"A heritage site, protected by ASI in Gandhinagar district is known as:",
     "options":["Adalaj", "Khumbor", "Dholevira", "Shihor"],
     "correct_answer":"Adalaj",
     "explanation":"The correct answer is (A) Adalaj. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta054","topic":"Teaching Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match List - I with List - II. List - I (Word) List - II (Unique Code) (a) Q U A K E (I) K T F U L (b) O F T E N (II) V H Q D U (c) P E A C H (III) I E Y O U (d) D R I V E (IV) J U Y W R",
     "options":["(a)-(I), (b)-(III), (c)-(II), (d)-(IV)", "(a)-(II), (b)-(IV), (c)-(III), (d)-(I)", "(a)-(III), (b)-(I), (c)-(IV), (d)-(II)", "(a)-(IV), (b)-(II), (c)-(I), (d)-(III)"],
     "correct_answer":"(a)-(III), (b)-(I), (c)-(IV), (d)-(II)",
     "explanation":"The correct answer is (C) (a)-(III), (b)-(I), (c)-(IV), (d)-(II). This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta056","topic":"Teaching Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"Arrange the following fractions in increasing order: (a) 12 17 (b) 13 19 (c) 8 11 (d) 16 23",
     "options":["(b), (d), (a), (c)", "(b), (a), (c), (d)", "(d), (a), (b), (c)", "(d), (b), (c), (a)"],
     "correct_answer":"(b), (d), (a), (c)",
     "explanation":"The correct answer is (A) (b), (d), (a), (c). This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta057","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which of the following is known as \"One Nation One Student ID\" card?",
     "options":["Aadhar card", "Pan card", "APAAR card", "Voter's ID card"],
     "correct_answer":"APAAR card",
     "explanation":"The correct answer is (C) APAAR card. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta058","topic":"Teaching Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match List - I with List - II. List-I (Types of Teaching) List-II (Description) (a) Macro teaching (I) A teaching technique especially used in teacher's pre- service education to train them systematically (b) Micro teaching (II) An approach where the educators divide the content among themselves and students sit with one educator before moving to the other (c) Station teaching (III) A situation in a classroom where two teachers work on a class together (d) Cooperative teaching (IV) When a teacher provides instruction to the entire class at one time for an extended period of time",
     "options":["(a)-(II), (b)-(III), (c)-(I), (d)-(IV)", "(a)-(IV), (b)-(II), (c)-(III), (d)-(I)", "(a)-(IV), (b)-(I), (c)-(II), (d)-(III)", "(a)-(I), (b)-(II), (c)-(III), (d)-(IV)"],
     "correct_answer":"(a)-(IV), (b)-(I), (c)-(II), (d)-(III)",
     "explanation":"The correct answer is (C) (a)-(IV), (b)-(I), (c)-(II), (d)-(III). This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta059","topic":"Teaching Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match List - I with List - II. List - I (Forms of Non-existence) List - II (Representation) (a) Anyonyābhāva (I) Hare's horn 63 (b) Atyantābhāva (II) there is non-existence of the jar now (c) Prāgabhava (III) This is not that (d) Pradhvamsābhava (IV) Temporary absence of a thing",
     "options":["(a)-(II), (b)-(IV), (c)-(I), (d)-(III)", "(a)-(I), (b)-(III), (c)-(II), (d)-(IV)", "(a)-(III), (b)-(I), (c)-(IV), (d)-(II)", "(a)-(IV), (b)-(II), (c)-(I), (d)-(III)"],
     "correct_answer":"(a)-(III), (b)-(I), (c)-(IV), (d)-(II)",
     "explanation":"The correct answer is (C) (a)-(III), (b)-(I), (c)-(IV), (d)-(II). This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta060","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"The sacred journey of Lord Jagannath is traditionally undertaken onward to which divine shrine?",
     "options":["Jagannath Temple", "Subhadra Temple", "Balabhadra Temple", "Gundicha Temple"],
     "correct_answer":"Gundicha Temple",
     "explanation":"The correct answer is (D) Gundicha Temple. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta061","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"Whereas the festival of Lord Jagannath is celebrated in many places in India and abroad, it is primarily associated with which city?",
     "options":["Bhuvaneswar", "Puri", "Cuttack", "Konark"],
     "correct_answer":"Puri",
     "explanation":"The correct answer is (B) Puri. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta062","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"The Car Festival is conducted on a broad road that is called _______.",
     "options":["Darpadalana", "Ashadha", "Badadanda", "Taladhwaja"],
     "correct_answer":"Badadanda",
     "explanation":"The correct answer is (C) Badadanda. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta063","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"What are the names of the deities who accompany Lord Jagannath in the Rath Yatra?",
     "options":["Subhadra and Balabhadra", "Balabhadra and Shiva", "Subhadra and Hidimba", "Balabhadra and Hidimba"],
     "correct_answer":"Subhadra and Balabhadra",
     "explanation":"The correct answer is (A) Subhadra and Balabhadra. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta064","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"What is the name assigned to the journey wherein the deities return to the Jagannath Temple after nine days?",
     "options":["Rath Yatra", "Wapsi Yatra", "Maha Yatra", "Bahuda Jatra"],
     "correct_answer":"Bahuda Jatra",
     "explanation":"The correct answer is (D) Bahuda Jatra. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta066","topic":"Teaching Aptitude","difficulty":"Hard","year":2024,"season":"June",
     "question":"Which of the following teaching techniques do not represent modern and ICT based teaching method. (a) Recitation and Memorization (b) Flipped Classroom (c) Mind maps (d) Chalk and Talk Method (e) Gamification",
     "options":["(b) and (c) Only", "(c) and (d) Only", "(a) and (d) Only", "(d) and (e) Only"],
     "correct_answer":"(a) and (d) Only",
     "explanation":"The correct answer is (C) (a) and (d) Only. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta067","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"First printing press in India was established at:",
     "options":["Goa", "Kerala", "Tamil Nadu", "Bengal"],
     "correct_answer":"Goa",
     "explanation":"The correct answer is (A) Goa. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta069","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"The amount of rainfall required to saturate the soil is known as.",
     "options":["Field Capacity", "Soil Moisture content", "Soil Moisture deficit", "Wilting Coefficient"],
     "correct_answer":"Soil Moisture deficit",
     "explanation":"The correct answer is (C) Soil Moisture deficit. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta071","topic":"Teaching Aptitude","difficulty":"Hard","year":2024,"season":"June",
     "question":"Basic factors of listening are: (a) Self interest (b) Speaker (c) Facts (d) Style of speaking (e) Atmosphere",
     "options":["(a), (b) and (d) Only", "(a), (c) and (e) Only", "(b), (c) and (e) Only", "(b), (d) and (e) Only"],
     "correct_answer":"(a), (b) and (d) Only",
     "explanation":"The correct answer is (A) (a), (b) and (d) Only. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta072","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"Groundwater is specially prone to excessive hardness due to.",
     "options":["Calcium and Sodium ions", "Calcium and Magnesium ions", "Sodium and Magnesium ions", "Potassium and Calcium ions"],
     "correct_answer":"Calcium and Magnesium ions",
     "explanation":"The correct answer is (B) Calcium and Magnesium ions. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta073","topic":"Teaching Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"Arrange the following fractions in increasing order- (a) 7 11 (b) 11 17 (c) 9 13 (d) 13 21",
     "options":["(a), (b), (c), (d)", "(a), (d), (b), (c)", "(d), (a), (b), (c)", "(b), (d), (c), (a)"],
     "correct_answer":"(d), (a), (b), (c)",
     "explanation":"The correct answer is (C) (d), (a), (b), (c). This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta074","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which groups of dialects are spoken in the western regions of Assam?",
     "options":["Goalparia and Dimasa", "Kamrupi and Karbi", "Goalparia and Nalbaria", "Goalparia and Kamrupi"],
     "correct_answer":"Goalparia and Kamrupi",
     "explanation":"The correct answer is (D) Goalparia and Kamrupi. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta075","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which group of dialects is spoken in Sibsagar and adjoining areas?",
     "options":["Southern", "Eastern", "Western", "Northern"],
     "correct_answer":"Eastern",
     "explanation":"The correct answer is (B) Eastern. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta076","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"What is the official language of the areas under the Bodoland Territorial council?",
     "options":["Rava", "Asomiya", "Bo-Ro", "Garo"],
     "correct_answer":"Bo-Ro",
     "explanation":"The correct answer is (C) Bo-Ro. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta077","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"If the year 2024 were to show the same percent revenue growth over the year 2023 as the year 2023 over the year 2022, then the revenue in the year 2024 will be approximately",
     "options":["₹ 194. 063 Lakh", "₹ 187. 075 Lakh", "₹ 172. 083 Lakh", "₹ 177. 095 Lakh"],
     "correct_answer":"₹ 177. 095 Lakh",
     "explanation":"The correct answer is (D) ₹ 177. 095 Lakh. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta078","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"The growth in total revenue in 2023 in comparison to the year 2020 is approximately",
     "options":["21%", "28%", "15%", "11%"],
     "correct_answer":"15%",
     "explanation":"The correct answer is (C) 15%. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta081","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"The principal orientation to the role of theory in relation to research is deductive in which of the following research strategies?",
     "options":["Quantitative", "Qualitative", "Inductive", "Constructive"],
     "correct_answer":"Quantitative",
     "explanation":"The correct answer is (A) Quantitative. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta082","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"5 pumps, working 18 hours a day, can empty a tank in 12 days. How many hours a day must 6 pumps operate to empty a tank in 9 days?",
     "options":["19 hours", "20 hours", "21 hours", "22 hours"],
     "correct_answer":"20 hours",
     "explanation":"The correct answer is (B) 20 hours. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta083","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"Typhoid is a waterborne disease caused by water contaminated by",
     "options":["Virus", "Fungi", "Bacteria", "Protozoan"],
     "correct_answer":"Bacteria",
     "explanation":"The correct answer is (C) Bacteria. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta084","topic":"Teaching Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"Which of the following statements are true regarding sub-contrary propositions? (a) If one is true, the other must be false (b) They cannot both be false (c) If one is false, the other must be true (d) They can both be true",
     "options":["(a) and (c) only", "(b), (c) and (d) only", "(a), (b) and (c) only", "(a) and (d) only"],
     "correct_answer":"(b), (c) and (d) only",
     "explanation":"The correct answer is (B) (b), (c) and (d) only. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta085","topic":"Teaching Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"Which of the following are arranged in the order of decreasing denotation?",
     "options":["Animals, Vertebrates, Birds, Sparrows", "Sparrows, Birds, Vertebrates, Animals", "Animals, Birds, Vertebrates, Sparrows", "Sparrows, Vertebrates, Birds, Animals"],
     "correct_answer":"Animals, Vertebrates, Birds, Sparrows",
     "explanation":"The correct answer is (A) Animals, Vertebrates, Birds, Sparrows. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta087","topic":"Teaching Aptitude","difficulty":"Hard","year":2024,"season":"June",
     "question":"Which of the following are the three meta-cognitive skills used to regulate thinking and learning? (a) Planning (b) Presenting (c) Monitoring (d) Evaluating (e) Sequencing",
     "options":["(a), (c) and (e) only", "(a), (c) and (d) only", "(b), (c) and (e) only", "(b), (d) and (e) only"],
     "correct_answer":"(a), (c) and (d) only",
     "explanation":"The correct answer is (B) (a), (c) and (d) only. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta088","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"Atomism was propounded by which of the following schools of Classical Indian Philosophy?",
     "options":["Advaita", "Vaişesika", "Buddhists", "Sāṁkhya"],
     "correct_answer":"Vaişesika",
     "explanation":"The correct answer is (B) Vaişesika. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta089","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"How do rituals help us when we are confronted with a big goal?",
     "options":["Rituals make us feel more stressed", "Rituals provide clear process and substeps to achieve the goal", "Rituals eliminate the need for goals", "Rituals allows us to ignore the goals"],
     "correct_answer":"Rituals provide clear process and substeps to achieve the goal",
     "explanation":"The correct answer is (B) Rituals provide clear process and substeps to achieve the goal. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta090","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"Main religions in Japan emphasize on",
     "options":["The importance of rituals over absolute rules", "Goal over process", "The irrelevance of rituals in daily life", "Absolute rules over rituals"],
     "correct_answer":"The importance of rituals over absolute rules",
     "explanation":"The correct answer is (A) The importance of rituals over absolute rules. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta092","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"The concept of explanatory journalism attempts to answer more-",
     "options":["'Why' questions", "'Where' questions", "'Which' questions", "'Who' questions"],
     "correct_answer":"'Why' questions",
     "explanation":"The correct answer is (A) 'Why' questions. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta093","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"Use of learning strategies and tactics reflects:",
     "options":["Intellectual Humility", "Overlearning", "Rote learning", "Meta cognitive knowledge"],
     "correct_answer":"Meta cognitive knowledge",
     "explanation":"The correct answer is (D) Meta cognitive knowledge. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta094","topic":"Teaching Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"Two propositions are contradictory if (a) They cannot both be true (b) Of the pair, exactly one is true and exactly one is false (c) They can both be false (d) They cannot both be false",
     "options":["(a) and (c) only", "(a), (b) and (c) only", "(b) only", "(a), (b) and (d) only"],
     "correct_answer":"(a), (b) and (d) only",
     "explanation":"The correct answer is (D) (a), (b) and (d) only. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta095","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"When the characteristic like age, sex or race of the researcher affect the behaviour of a participants in a study, it refers to",
     "options":["Biosocial effect", "Psychological effect", "Hawthorn effect", "Evaluation apprehension"],
     "correct_answer":"Biosocial effect",
     "explanation":"The correct answer is (A) Biosocial effect. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta096","topic":"Teaching Aptitude","difficulty":"Hard","year":2024,"season":"June",
     "question":"Which of the following are the explanations of Pedagogical Teacher's Dilemmas of constructivism in practice? (a) Developing deeper knowledge of subject matter (b) Managing new ideas of discourse and collaborative work in the classroom (c) Honoring students attempt to think for themselves which remaining faithful to the accepted disciplinary ideas (d) Mastering the art of facilitation (e) Confronting issues of accountability with various stakeholders in the school community",
     "options":["(a), (b), (c) and (d) only", "(d), and (e) only", "(a), (b) and (c) only", "(b), (c) and (e) only"],
     "correct_answer":"(a), (b), (c) and (d) only",
     "explanation":"The correct answer is (A) (a), (b), (c) and (d) only. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta097","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which of the following is arranged in the order of decreasing extension?",
     "options":["Mathematics, arithmetic, numbers, prime numbers", "Prime numbers, numbers, arithmetic, Mathematics", "Arithmetic, mathematics, numbers, prime numbers", "Numbers, prime numbers, arithmetic, mathematics"],
     "correct_answer":"Mathematics, arithmetic, numbers, prime numbers",
     "explanation":"The correct answer is (A) Mathematics, arithmetic, numbers, prime numbers. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta098","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which of the following does not help the inhabitants to continue their distinctive identity in Andaman and Nicobar Islands?",
     "options":["Linguistic aspect", "Cultural aspect", "Territorial aspect", "Nutritional aspect"],
     "correct_answer":"Nutritional aspect",
     "explanation":"The correct answer is (D) Nutritional aspect. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta099","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"Port Blair is a part of:",
     "options":["Kerala", "Andhra Pradesh", "Sri Lanka", "Andaman and Nicobar Islands"],
     "correct_answer":"Andaman and Nicobar Islands",
     "explanation":"The correct answer is (D) Andaman and Nicobar Islands. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta100","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which of the following communities has connection with the Andaman and Nicobar Islands?",
     "options":["Khasi", "Santhal", "Bodo", "Jarawa"],
     "correct_answer":"Jarawa",
     "explanation":"The correct answer is (D) Jarawa. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta101","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"Andaman and Nicobar Islands",
     "options":["is a cluster of small beautiful countries", "is a cluster of several beautiful islands", "is a cluster of few villages", "is cluster of deserts"],
     "correct_answer":"is a cluster of several beautiful islands",
     "explanation":"The correct answer is (B) is a cluster of several beautiful islands. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta105","topic":"Teaching Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"As per classical Indian School of Logic (Nyāya), verbal testimony (śabda pramāna) includes: (a) Only injunctive sentences (b) Words of a scripture (c) Words of any teacher (d) Words of a trustworthy person",
     "options":["(a) and (c) only", "(b) and (d) only", "(a) and (b) only", "(a), (b), (c) and (d)"],
     "correct_answer":"(b) and (d) only",
     "explanation":"The correct answer is (B) (b) and (d) only. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta106","topic":"Teaching Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"A man deposited some amount of money in a bank at some simple rate of interest for 3 years. Had he deposited the money at 2% higher rate of interest, he would have fetched ₹360 more. Find the amount deposited in the bank.",
     "options":["₹ 6200", "₹ 7000", "₹ 6500", "₹ 6000"],
     "correct_answer":"₹ 6000",
     "explanation":"The correct answer is (D) ₹ 6000. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta107","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"Find the value of the following expression: (0.22×0.22×0.22)+(0.022×0.022×0.022) (0.66×0.66×0.66)+(0.066×0.066×0.066)",
     "options":["2 27", "1 25", "1 27", "1 23"],
     "correct_answer":"1 27",
     "explanation":"The correct answer is (C) 1 27. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta108","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"The tendency of people being observed to act differently than normal as a result of their awareness of being monitored, refers to:",
     "options":["Subject reactivity", "Observer bias", "Observer drift", "De briefing"],
     "correct_answer":"Subject reactivity",
     "explanation":"The correct answer is (A) Subject reactivity. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta109","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"A man can do a piece of work in 8 days and another man can do the same work in 10 days. How long should it take both A and B working together but independently?",
     "options":["6 days", "4", "4", "5"],
     "correct_answer":"4",
     "explanation":"The correct answer is (B) 4. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta110","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which of the following best exemplifies the zero transfer of learning?",
     "options":["Using knowledge of one programming language to another similar language", "Applying techniques of learning in basketball to improve skills in soccer", "Using skills acquired in carpentary to excel in painting", "Applying a mathematical problem solving method to physics problems"],
     "correct_answer":"Using skills acquired in carpentary to excel in painting",
     "explanation":"The correct answer is (C) Using skills acquired in carpentary to excel in painting. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta111","topic":"Teaching Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"A teacher wants to integrate SWAYAM into the curriculum to enhance learning. Which of the following benefits of SWAYAM should the teacher highlight to the students? (a) Free access to quality educational resources (b) Opportunity for live interactions with instructions (c) Peer-reviewed assignments (d) Self-paced learning.",
     "options":["(b), (c) and (d) only", "(a) and (d) only", "(d) only", "(a) and (b) only"],
     "correct_answer":"(a) and (d) only",
     "explanation":"The correct answer is (B) (a) and (d) only. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta112","topic":"Teaching Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"If the statement-\"No squares are circles\" is given as true, which of the following statements can be immediately inferred to be false. (a) Some circles are not squares (b) All squares are circles (c) Some squares are circles (d) Some squares are not circles",
     "options":["(a) and (b) only", "(b) and (c) only", "(a) and (c) only", "(a), (b) and (d) only"],
     "correct_answer":"(b) and (c) only",
     "explanation":"The correct answer is (B) (b) and (c) only. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta113","topic":"Teaching Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"Which of the following two propositions can neither be both true together nor can they be false together? (a) All squares are rectangles (b) Some squares are rectangles (c) No squares are rectangles (d) Some square are not rectangles 107",
     "options":["(a) and (d) only", "(b) and (d) only", "(c) and (d) only", "(a) and (c) only"],
     "correct_answer":"(a) and (d) only",
     "explanation":"The correct answer is (A) (a) and (d) only. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta114","topic":"Teaching Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match List I with List II. List - I (Water treatment) List - II (Process) (a) Primary (I) Removal of wastes with the help of activated charcoal etc. (b) Secondary (II) Ozonization and disinfection by ultraviolet rays. (c) Terliary (III) Removal of large pieces such as stick, stone, rags, plastic etc. (d) Advanced (IV) Removal after flocculation and coagulation of wastes",
     "options":["(a)-(III), (b)-(IV), (c)-(II), (d)-(I)", "(a)-(III), (b)-(IV), (c)-(I), (d)-(II)", "(a)-(II), (b)-(III), (c)-(I), (d)-(IV)", "(a)-(II), (b)-(III), (c)-(IV), (d)-(I)"],
     "correct_answer":"(a)-(III), (b)-(IV), (c)-(I), (d)-(II)",
     "explanation":"The correct answer is (B) (a)-(III), (b)-(IV), (c)-(I), (d)-(II). This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta115","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"Kapilendra Dev's devotion to which deity contributed to the creative atmosphere in Orissa?",
     "options":["Shiva", "Vishnu", "Jagannath", "Lakshmi"],
     "correct_answer":"Jagannath",
     "explanation":"The correct answer is (C) Jagannath. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta116","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which monarch is credited with opening a new horizon for Oriya poets at the beginning of the 15th century?",
     "options":["Kapilendra Dev", "Sarala Das", "Tulsidas", "Kalidasa"],
     "correct_answer":"Kapilendra Dev",
     "explanation":"The correct answer is (A) Kapilendra Dev. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta117","topic":"Teaching Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"If the statement \"All Plants are Carnivorous\", is given as false which of the following statements can be inferred to be true: (a) Some non-plants are non- carnivorous (b) No Plants are carnivorous (c) Some plants are carnivorous (d) Some plants are not carnivorous",
     "options":["(c) only", "(b) and (d) only", "(d) only", "(a), (b), (c), (d) only"],
     "correct_answer":"(d) only",
     "explanation":"The correct answer is (C) (d) only. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta118","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"A certain amount of money deposited in a bank becomes ₹ 1008 in 2 years and ₹ 1164 in 3 1 2 years. Find the amount deposited in the bank and the rate of interest per annum.",
     "options":["₹700, 12%", "₹800, 13%", "₹750, 13%", "₹850, 13.5%"],
     "correct_answer":"₹800, 13%",
     "explanation":"The correct answer is (B) ₹800, 13%. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta119","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"The professional organisation that opposed the inclusion of its educational discipline under NCHER was.",
     "options":["Education Council of India", "Dental Council of India", "Architectural Council of India", "Bar Council of India"],
     "correct_answer":"Bar Council of India",
     "explanation":"The correct answer is (D) Bar Council of India. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta120","topic":"Teaching Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match the List-I with List-II List - I (Proponent) List - II (Initiative) (a) Lord Dalhousie (I) Support to oriental education (b) Annie Besant (II) Technical education (c) Lord Curzan (III) Moral education (d) Lord Auckland (IV) Reform and control of higher education",
     "options":["(a)-(I), (b)-(II), (c)-(III), (d)-(IV)", "(a)-(II), (b)-(III), (c)-(IV), (d)-(I)", "(a)-(ІІІ), (b)-(IV), (c)-(I), (d)-(II)", "(a)-(IV), (b)-(I), (c)-(II), (d)-(III)"],
     "correct_answer":"(a)-(II), (b)-(III), (c)-(IV), (d)-(I)",
     "explanation":"The correct answer is (B) (a)-(II), (b)-(III), (c)-(IV), (d)-(I). This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta121","topic":"Teaching Aptitude","difficulty":"Hard","year":2024,"season":"June",
     "question":"Which of the following cause indirect Green House Warming? (a) CH4 (b) NO (c) NO2 (d) N2O (e) CO",
     "options":["(a), (b) and (c) only", "(a) and (d) only", "(b), (d) and (e) only", "(b), (c) and (e) only"],
     "correct_answer":"(b), (c) and (e) only",
     "explanation":"The correct answer is (D) (b), (c) and (e) only. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta122","topic":"Teaching Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"Which of the following propositions are Contrary? (a) All cows are herbivores (b) No cows are herbivores (c) Some cows are herbivores (d) Some cows are not herbivores",
     "options":["(a) and (c) only", "(a) and (b) only", "(c) and (d) only", "(a) and (d) only"],
     "correct_answer":"(a) and (b) only",
     "explanation":"The correct answer is (B) (a) and (b) only. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta123","topic":"Teaching Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match the List-I with List-II List - I (Unit of Data Capacity) List - II (Approximate Size) (a) Kilobyte (I) 8 billion bits (b) Gigabyte (II) 8 million bits (c) Terabyte (III) 8 thousands bits 118 (d) Megabyte (IV) 8 trillion bits",
     "options":["(a)-(III), (b)-(I), (c)-(IV), (d)-(II)", "(a)-(IV), (b)-(II), (c)-(I), (d)-(III)", "(a)-(ІII), (b)-(IV), (c)-(I), (d)-(II)", "(a)-(I), (b)-(III), (c)-(II), (d)-(IV)"],
     "correct_answer":"(a)-(III), (b)-(I), (c)-(IV), (d)-(II)",
     "explanation":"The correct answer is (A) (a)-(III), (b)-(I), (c)-(IV), (d)-(II). This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta124","topic":"Teaching Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match List I with List II. List - I (Expression) List - II (Value) (a) 0.1x5.5x55.5x0.5 (Ι) 0.00152625 (b) 0.01x0.55x5.55x0.05 (ΙΙ) 0.0152625 (c) 0.1x0.55x55.5x0.005 (III) 0.152625 (d) 0.01x5.5x5.55x0.5 (IV) 15.2625",
     "options":["(a)-(I), (b)-(II), (c)-(III), (d)-(IV)", "(a)-(II), (b)-(III), (c)-(IV), (d)-(I)", "(a)-(ІV), (b)-(I), (c)-(II), (d)-(III)", "(a)-(IV), (b)-(II), (c)-(III), (d)-(I)"],
     "correct_answer":"(a)-(ІV), (b)-(I), (c)-(II), (d)-(III)",
     "explanation":"The correct answer is (C) (a)-(ІV), (b)-(I), (c)-(II), (d)-(III). This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta125","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"What do some anthropologists think and hope about war?",
     "options":["War will continue forever", "War will keep on evolvig taking a new form", "War can be eradicated by wise collective decision making", "War will happen more frequently"],
     "correct_answer":"War can be eradicated by wise collective decision making",
     "explanation":"The correct answer is (C) War can be eradicated by wise collective decision making. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta126","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"What all economic motives have historically driven war?",
     "options":["Only gold and treasure", "Only salt and metals", "Only trade routes", "Various resources including salt, metals, gold, treasure enslaved labour, trade routs and oil"],
     "correct_answer":"Various resources including salt, metals, gold, treasure enslaved labour, trade routs and oil",
     "explanation":"The correct answer is (D) Various resources including salt, metals, gold, treasure enslaved labour, trade routs and oil. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta127","topic":"Teaching Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"A man invests ₹1550 in two parts, one part at the rate of 8% interest and another part at the rate of 6%. If the total interest earned in one year is ₹106, find the amount invested at each rate of interest, respectively.",
     "options":["₹ 650 and ₹ 900", "₹ 700 and ₹ 850", "₹ 750 and ₹ 800", "₹ 800 and ₹ 750"],
     "correct_answer":"₹ 650 and ₹ 900",
     "explanation":"The correct answer is (A) ₹ 650 and ₹ 900. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta128","topic":"Teaching Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"To teach a particular topic a teacher first gives the students to watch the pre-recorded video of the lecture at home and then engages the students in discussions and problem solving activities in the class. This is an example of:",
     "options":["Lecture-demonstration", "Flipped classroom", "Asynchronous learning", "Synchronous learning"],
     "correct_answer":"Flipped classroom",
     "explanation":"The correct answer is (B) Flipped classroom. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta129","topic":"Teaching Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"If the statement \"Some rectangles are squares\" is given as true then which of the following statements can be inferred to be false. (a) All rectangles are squares (b) Some rectangles are not squares (c) Some squares are not rectangles (d) No rectangles are squares",
     "options":["(b), (c) and (d) only", "(d) only", "(b) and (c) only", "(a), (b), (c) and (d)"],
     "correct_answer":"(d) only",
     "explanation":"The correct answer is (B) (d) only. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta130","topic":"Teaching Aptitude","difficulty":"Hard","year":2024,"season":"June",
     "question":"Which of the following were measures initiated by Lord Auckland? (a) Guaranteed the maintenance of oriental colleges (b) Publication of useful works for instruction in oriental languages (c) Selection of certain places for establishing central colleges for highest instruction (d) Closure of college libraries (e) Abolition of student scholarships",
     "options":["(a), (b), (c) only", "(b), (c), (d) only", "(c), (d), (e) only", "(a), (d), (e) only"],
     "correct_answer":"(a), (b), (c) only",
     "explanation":"The correct answer is (A) (a), (b), (c) only. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta131","topic":"Teaching Aptitude","difficulty":"Hard","year":2024,"season":"June",
     "question":"Which of the following are routes for exposure to pollutants in humans? (a) Inhalation (b) Consumption (c) Ingestion (d) Dermal (e) Digestion",
     "options":["(a), (b) and (c) only", "(a), (c) and (d) only", "(b), (d) and (e) only", "(a), (c) and (e) only"],
     "correct_answer":"(a), (c) and (d) only",
     "explanation":"The correct answer is (B) (a), (c) and (d) only. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta132","topic":"Teaching Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"Which of the following propositions are contradictory? (a) All squares are rectangles 132 (b) No squares are rectangles (c) Some squares are rectangles (d) Some squares are not rectangles",
     "options":["(c) and (d) only", "(a) and (d) only", "(b) and (d) only", "(a) and (b) only"],
     "correct_answer":"(a) and (d) only",
     "explanation":"The correct answer is (B) (a) and (d) only. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta133","topic":"Teaching Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"An instructor uses portfolio assessments in an art class. What key components should be included in the students' portfolios? (a) Collection of completed art works (b) Reflective essays on their creative process (c) Standardized test scores (d) Peer feedback and critiques",
     "options":["(b) and (c) only", "(a), (b) and (d) only", "(a) and (c) only", "(c) and (d) only"],
     "correct_answer":"(a), (b) and (d) only",
     "explanation":"The correct answer is (B) (a), (b) and (d) only. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta135","topic":"Teaching Aptitude","difficulty":"Hard","year":2024,"season":"June",
     "question":"Presence of Lead in drinking water can adversely affect the human health. The three vital systems in the human body that are most sensitive to Lead are: (a) Nervous system (b) Cardio-vascular system (c) Renal system (d) Respiratory system (e) Blood forming system",
     "options":["(a), (c) and (e) only", "(b), (c) and (d) only", "(b), (d) and (e) only", "(a), (c) and (d) only"],
     "correct_answer":"(a), (c) and (e) only",
     "explanation":"The correct answer is (A) (a), (c) and (e) only. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta136","topic":"Teaching Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match List - I with List - II. List -I (Expression) List -II (Value) (a) 0.5 × 0.05 × 0.005 × 50 (I) 154.15125 (b) 5.55 × 55.5 × 55 (II) 16941.375 (c) 5.05 × 5.55 × 5.5 (III) 1678.875 (d) 5.5 × 5.5 × 55.5 (IV) 0.00625",
     "options":["(a)-(IV), (b)-(III), (c)-(I), (d)-(II)", "(a)-(II), (b)-(III), (c)-(IV), (d)-(I)", "(a)-(IV), (b)-(II), (c)-(I), (d)-(III)", "(a)-(IV), (b)-(III), (c)-(II), (d)-(I)"],
     "correct_answer":"(a)-(IV), (b)-(II), (c)-(I), (d)-(III)",
     "explanation":"The correct answer is (C) (a)-(IV), (b)-(II), (c)-(I), (d)-(III). This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta137","topic":"Teaching Aptitude","difficulty":"Hard","year":2024,"season":"June",
     "question":"Which of the following are true about sound? (a) 10 decibel (dB) increase in sound is equal to 10 fold increase in sound intensity (b) 20 dB increase in sound is equal to 20 fold increase in sound intensity (c) Loudness is the human perception of sound intensity (d) The audible sound range is between 20 Hz to 20 kHz (e) Sound below 20 Hz is called ultrasound while above 20 kHz is called infrasound",
     "options":["(a), (b) and (d) only", "(b), (c) and (d) only", "(c), (d) and (e) only", "(a), (c) and (d) only"],
     "correct_answer":"(a), (c) and (d) only",
     "explanation":"The correct answer is (D) (a), (c) and (d) only. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta138","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"According to the New Education Policy, 2020, who among the following must be at the centre of fundamental reforms in the education system?",
     "options":["Policy makers", "Teachers", "Industry leaders", "Administrators"],
     "correct_answer":"Teachers",
     "explanation":"The correct answer is (B) Teachers. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta141","topic":"Teaching Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"Arrange the following in order of decreasing extension. (a) Sonnet (b) Poem (c) Verse (d) Literature",
     "options":["(a), (b), (c), (d)", "(d), (c), (b), (a)", "(d), (b), (a), (c)", "(a), (b), (d), (c)"],
     "correct_answer":"(d), (b), (a), (c)",
     "explanation":"The correct answer is (C) (d), (b), (a), (c). This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta142","topic":"Teaching Aptitude","difficulty":"Hard","year":2024,"season":"June",
     "question":"In an online course, a teacher wants to organize weekly readings, quizzes and discussion forums for students. Which of the following platforms would be most suitable for managing these activities? (a) Schoology (b) Blackboard learn (c) Zoom (d) Canvas (e) Moodle",
     "options":["(c), (d) and (e) only", "(a), (b) and (c) only", "(a), (b), (d) and (e) only", "(c) and (d) only"],
     "correct_answer":"(a), (b), (d) and (e) only",
     "explanation":"The correct answer is (C) (a), (b), (d) and (e) only. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta143","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"Pure rain water is naturally:",
     "options":["Mild Acidic", "Mild Basic", "Neutral", "Strong Acidic"],
     "correct_answer":"Mild Acidic",
     "explanation":"The correct answer is (A) Mild Acidic. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta144","topic":"Teaching Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match List - I with List - II. List - I (Author) List - II (Ancient Text) (a) Gotama (I) Vaiśeşika sutras (b) Patanjali (II) Nyāya sutra (c) Kautilya (III) Yoga sutra (d) Kaņād (IV) Arthaśāstra",
     "options":["(a)-(III), (b)-(II), (c)-(IV), (d)-(I)", "(a)-(II), (b)-(III), (c)-(IV), (d)-(I)", "(a)-(III), (b)-(II), (c)-(I), (d)-(IV)", "(a)-(II), (b)-(IV), (c)-(III), (d)-(I)"],
     "correct_answer":"(a)-(II), (b)-(III), (c)-(IV), (d)-(I)",
     "explanation":"The correct answer is (B) (a)-(II), (b)-(III), (c)-(IV), (d)-(I). This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta145","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"The interactive technologies are responsible for the appearance of:",
     "options":["Traditional media age", "Broadcast media age", "Market media age", "Second media age"],
     "correct_answer":"Second media age",
     "explanation":"The correct answer is (D) Second media age. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta146","topic":"Teaching Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"Which of the following are not the examples of Positive - Transfer of Learning? (a) Learning of Piano makes it more difficult to learn the violin (b) Mastering Algebra helps in understanding Calculus (c) Knowing how to drive a car makes it harder to learn how to ride a bicycle (d) Learning to speak French hinders learning Spanish",
     "options":["(b) and (d) only", "(a), (c) and (d) only", "(b), (c) and (d) only", "(a) and (c) only"],
     "correct_answer":"(a), (c) and (d) only",
     "explanation":"The correct answer is (B) (a), (c) and (d) only. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta147","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"Poets have compared adolescence to the following phase of life:",
     "options":["Summer", "Winter", "Spring", "Fall"],
     "correct_answer":"Spring",
     "explanation":"The correct answer is (C) Spring. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta149","topic":"Teaching Aptitude","difficulty":"Hard","year":2024,"season":"June",
     "question":"The major recommendations of the Radhakrishnan Commission are: (a) Transfer of urban universities to rural areas (b) Setting up of rural universities (c) Development of research in agriculture, commerce, law, science and technology (d) Making English language as the medium of instruction at all levels of teaching (e) Focus on student's Welfare",
     "options":["(a), (b) only", "(b), (c), (d) only", "(c), (d), (e) only", "(b), (c), (e) only"],
     "correct_answer":"(b), (c), (e) only",
     "explanation":"The correct answer is (D) (b), (c), (e) only. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta150","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"The Kanya Mahavidyalaya, an Arya Samaji School, was established in 1896 by:",
     "options":["Bhai Veer Singh", "Agya Kaur", "Bhai Takht Singh", "Lala Devraj"],
     "correct_answer":"Lala Devraj",
     "explanation":"The correct answer is (D) Lala Devraj. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta151","topic":"Teaching Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"Arrange the following in order of decreasing denotation. (a) Physics (b) Natural Sciences (c) Sciences (d) Nuclear Physics",
     "options":["(c), (b), (a), (d)", "(b), (c), (a), (d)", "(d), (a), (b), (c)", "(b), (c), (d), (a)"],
     "correct_answer":"(c), (b), (a), (d)",
     "explanation":"The correct answer is (A) (c), (b), (a), (d). This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta152","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"In the post-information age, information is highly.",
     "options":["Homogeneous", "Communitarian", "Personalised", "Impersonal"],
     "correct_answer":"Personalised",
     "explanation":"The correct answer is (C) Personalised. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta153","topic":"Teaching Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match the List-I with List-II List - I (Authors) List - II (Works) (a) Pingal (I) Lilāvati (b) Pāņini (II) Chhandasāstra (c) Āryabhatta (III) Astādhyāyi (d) Bhāskarācharya (IV) Āryabhatiya",
     "options":["(a)-(II), (b)-(IV), (c)-(III), (d)-(I)", "(a)-(III), (b)-(II), (c)-(IV), (d)-(I)", "(a)-(II), (b)-(III), (c)-(IV), (d)-(I)", "(a)-(I), (b)-(III), (c)-(IV), (d)-(II)"],
     "correct_answer":"(a)-(II), (b)-(III), (c)-(IV), (d)-(I)",
     "explanation":"The correct answer is (C) (a)-(II), (b)-(III), (c)-(IV), (d)-(I). This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta154","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"What of the following aspects does not pertain to delibrate practice of learners?",
     "options":["The task is too easy or too hard", "The learner is given informative feed back about his/her performance", "The learner has adequate chances to repeat the task", "The learner has the opportunity to correct his/her errors"],
     "correct_answer":"The task is too easy or too hard",
     "explanation":"The correct answer is (A) The task is too easy or too hard. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta155","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"The New Education Policy, 2020 envisages making all learners:",
     "options":["Social volunteers", "Efficient administrators", "True global citizens", "Spiritual persons"],
     "correct_answer":"True global citizens",
     "explanation":"The correct answer is (C) True global citizens. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta156","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"Match the List-I with List-II",
     "options":["(a)-(I), (b)-(II), (c)-(III), (d)-(IV)", "(a)-(II), (b)-(III), (c)-(IV), (d)-(I)", "(a)-(III), (b)-(IV), (c)-(I), (d)-(II)", "(a)-(IV), (b)-(I), (c)-(II), (d)-(III)"],
     "correct_answer":"(a)-(II), (b)-(III), (c)-(IV), (d)-(I)",
     "explanation":"The correct answer is (B) (a)-(II), (b)-(III), (c)-(IV), (d)-(I). This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta157","topic":"Teaching Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"At the Sikh Kanya Mahvidyalaya, books written by which of the following Singh Sabha stalwarts were taught? (a) Bhai Veer Singh (b) Lala Devraj (c) Harnam Kaur (d) Bhai Mohan Singh Vaid",
     "options":["(a), (b), (c), (d)", "(a) and (d) only", "(a) and (c) only", "(b) and (c) only"],
     "correct_answer":"(a) and (d) only",
     "explanation":"The correct answer is (B) (a) and (d) only. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta158","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"The motivated forgetting of traumatic or other very threatening events is known as-",
     "options":["Repression", "Proactive interference", "Retroactive interference", "Consolidation"],
     "correct_answer":"Repression",
     "explanation":"The correct answer is (A) Repression. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta159","topic":"Teaching Aptitude","difficulty":"Hard","year":2024,"season":"June",
     "question":"Which of the following tools would be most effective for a teacher wanting to poll students in real-time during an online lecture? (a) Poll everywhere (b) Labster (c) Strawpoll (d) Mentimeter (e) Survey monkey",
     "options":["(b), (c) and (e) only", "(b) and (c) only", "(a), (c), (d) and (e) only", "(c) (d) and (e) only"],
     "correct_answer":"(a), (c), (d) and (e) only",
     "explanation":"The correct answer is (C) (a), (c), (d) and (e) only. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta160","topic":"Teaching Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"Arrange the following in the order of decreasing connotation. (a) Polygon (b) Rectangle (c) Geometry (d) Square",
     "options":["(d), (b), (c), (a)", "(c), (a), (b), (d)", "(a), (c), (b), (d)", "(d), (b), (a), (c)"],
     "correct_answer":"(d), (b), (a), (c)",
     "explanation":"The correct answer is (D) (d), (b), (a), (c). This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta161","topic":"Teaching Aptitude","difficulty":"Hard","year":2024,"season":"June",
     "question":"In self-directed learning which of the following are the key features of self- directed students? (a) They have Intrinsic motivation. (b) They have the capacity to choose personal goals. (c) They have self- discipline. (d) They have self- assessment ability. (e) They have metacognitive skills.",
     "options":["(a) and (d) only", "(b) and (e) only", "(c), (d) and (e) only", "(a), (b), (c), (d) and (e)"],
     "correct_answer":"(a), (b), (c), (d) and (e)",
     "explanation":"The correct answer is (D) (a), (b), (c), (d) and (e). This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta162","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"Therapeutic applications of Nicotine - containing products can be stated as follows:",
     "options":["They are used to increase physical strength", "They are used to improve cognitive function.", "They are used to reduce anxiety, stress and depression", "They are mostly used as antibiotics"],
     "correct_answer":"They are used to reduce anxiety, stress and depression",
     "explanation":"The correct answer is (C) They are used to reduce anxiety, stress and depression. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta163","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"What feelings does nicotine cause upon reaching the brain?",
     "options":["Sleepiness", "Depression", "Hunger", "Euphoria"],
     "correct_answer":"Euphoria",
     "explanation":"The correct answer is (D) Euphoria. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta164","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"A child of first class is trying to learn how to draw a circle on his own but is able to do with the help of his/her teacher. In the light of Vygotsky's theory, it highlights?",
     "options":["Assimilation", "Adoption", "Zone of proximal development", "Maturation"],
     "correct_answer":"Zone of proximal development",
     "explanation":"The correct answer is (C) Zone of proximal development. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta165","topic":"Teaching Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"Which of the following are the characteristics of learner centered Approach? (a) It lays emphasis on skills (b) It is centered on learner's needs (c) It is centered on cooperative determination of subject matter (d) Lays emphasis on variability of exposure 175",
     "options":["(c) and (d) only", "(a), (b) and (c) only", "(a), (b), (c) and (d)", "(b) and (d) only"],
     "correct_answer":"(a), (b), (c) and (d)",
     "explanation":"The correct answer is (C) (a), (b), (c) and (d). This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta166","topic":"Teaching Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"Which of the following statements are subalternate as per traditional square of opposition? (a) All plants are green organisms (b) No plants are green organisms (c) Some plants are not green organisms (d) Some plants are green organisms",
     "options":["(a) and (d) only", "(b) and (d) only", "(a) and (c) only", "(a) and (b) only"],
     "correct_answer":"(a) and (d) only",
     "explanation":"The correct answer is (A) (a) and (d) only. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta167","topic":"Teaching Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"If the statement \"all lions are carnivorous animals\" is given as true which of the following statements can be immediately inferred to be false? (a) No lions are carnivorous animals (b) Some lions are carnivorous animals 177 (c) Some lions are not carnivorous animals (d) Some carnivorous animals are lions",
     "options":["(c) and (d) only", "(a) and (c) only", "(a) and (b) only", "(b) and (c) only"],
     "correct_answer":"(a) and (c) only",
     "explanation":"The correct answer is (B) (a) and (c) only. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta168","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"Toxic substances that damage kidneys are called as.",
     "options":["Hematotoxic", "Neurotoxic", "Cytotoxic", "Nephrotoxic"],
     "correct_answer":"Nephrotoxic",
     "explanation":"The correct answer is (D) Nephrotoxic. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta169","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"Project method of teaching was first propounded by.",
     "options":["Crow and Crow", "John Dewey", "Robert Miller", "Robert Mager"],
     "correct_answer":"John Dewey",
     "explanation":"The correct answer is (B) John Dewey. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta170","topic":"Teaching Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"Consider the following snapshot of MS-Excel worksheet: A B C D 17 Day Quantity Sales Amount (₹) 18 Monday 1 234 19 Tuesday 3 144 20 Wednesday 6 367 21 Thursday 5 674 22 Friday 8 1099 23 Saturday 3 233 In cell D18, the value returned by the function. =SUMIFS (C18: C23, B18: B23, \">3\", C18: C23, \">500\") is __________.",
     "options":["1466", "2140", "1773", "26"],
     "correct_answer":"1773",
     "explanation":"The correct answer is (C) 1773. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta171","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"A sum of money becomes ₹ 34800 in 2 years and ₹ 42,000 in 5 years at simple interest per annum. Find the rate of interest and the sum of money respectively",
     "options":["6%, ₹ 40,000", "7%, ₹ 30,000", "8%, ₹ 30,000", "5%, ₹ 35,000"],
     "correct_answer":"8%, ₹ 30,000",
     "explanation":"The correct answer is (C) 8%, ₹ 30,000. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta172","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"In the Buddhist system of education higher education was placed at.",
     "options":["The first level", "The second level", "The third level", "The forth level"],
     "correct_answer":"The second level",
     "explanation":"The correct answer is (B) The second level. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta173","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"Communities have been involved in the protection of plants and animals for the last.",
     "options":["Several thousand years", "200 years only", "60 years only", "only recently"],
     "correct_answer":"Several thousand years",
     "explanation":"The correct answer is (A) Several thousand years. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta174","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"Utilatitarian ideas started dominating attitudes towards nature about.",
     "options":["2000 years ago", "60 years ago", "100 years ago", "200 years ago"],
     "correct_answer":"200 years ago",
     "explanation":"The correct answer is (D) 200 years ago. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta175","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"A certain sum of money becomes ₹28800 in 2 years at 20% per annum of compound interest (Compounded annually). The sum of money is:",
     "options":["₹24000", "₹22000", "₹21000", "₹20000"],
     "correct_answer":"₹20000",
     "explanation":"The correct answer is (D) ₹20000. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta176","topic":"Teaching Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"A teacher assigns a video lecture for students to watch at home before coming to class. Next day in the class she engages sttudents in 'hands-on' experimental activities. Which approach she used in this situation?",
     "options":["Problem solving", "Collaborative learning", "Flipped classroom", "Personalized learning"],
     "correct_answer":"Flipped classroom",
     "explanation":"The correct answer is (C) Flipped classroom. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta178","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"The period between 1200 and 1764 AD was remarkable in India for the highest distinction attained by:",
     "options":["Popular literature", "Vernacular literature", "English literature", "French literature"],
     "correct_answer":"Vernacular literature",
     "explanation":"The correct answer is (B) Vernacular literature. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta179","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"The belief that one can master a situation and produce positive outcomes is known as-",
     "options":["self-efficacy", "self-esteem", "self-actualization", "self-regulation"],
     "correct_answer":"self-efficacy",
     "explanation":"The correct answer is (A) self-efficacy. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta180","topic":"Teaching Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"Which of the following facts regarding synaptic connections are correct? (a) Connections that are used are weakened. (b) Twice as many connections are made than ever will be used. (c) Unused connections either disappear or are replaced by other pathways. (d) Connections that are used perish. 193",
     "options":["(a), (b) and (d) only", "(b) and (c) only", "(a) and (d) only", "(b), (c) and (d) only"],
     "correct_answer":"(b) and (c) only",
     "explanation":"The correct answer is (B) (b) and (c) only. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta182","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"As children grow their attention span focus",
     "options":["Remains static", "Improves", "Declines insignificantly", "Declines significantly"],
     "correct_answer":"Improves",
     "explanation":"The correct answer is (B) Improves. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta185","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"The National Knowledge Commission suggested that the proposed national universities should not have",
     "options":["Affiliated colleges", "Public funding", "Linkage with industries", "Teaching departments"],
     "correct_answer":"Affiliated colleges",
     "explanation":"The correct answer is (A) Affiliated colleges. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta186","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"The style that involves a student's tendency to take more time to respond on the accuracy of answers is known as:",
     "options":["Impulsive style", "Surface style", "Reflective style", "Manipulative style"],
     "correct_answer":"Reflective style",
     "explanation":"The correct answer is (C) Reflective style. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta187","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which of the following is an example of positive-transfer of learning?",
     "options":["Mastering algebra helps in understanding calculus.", "Learning to play piano makes it more difficult to learn the violin.", "Knowing how to drive a car makes it harder to learn how to ride a bicycle.", "Learning to speak French hinders learning Spanish."],
     "correct_answer":"Mastering algebra helps in understanding calculus.",
     "explanation":"The correct answer is (A) Mastering algebra helps in understanding calculus.. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta188","topic":"Teaching Aptitude","difficulty":"Hard","year":2024,"season":"June",
     "question":"Identify the virtuous character traits which help an individual to flourish in life. (a) Integrity (b) Psychophancy (c) Honesty (d) Compassion (e) Faithfulness",
     "options":["(a), (b), (c) and (d) only", "(a), (c) and (d) only", "(a), (b), (c), (d) and (e)", "(a), (c), (d) and (e) only"],
     "correct_answer":"(a), (c), (d) and (e) only",
     "explanation":"The correct answer is (D) (a), (c), (d) and (e) only. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta189","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"Quality of our interactions in human relationships is gauged by",
     "options":["economic status", "social status", "interpersonal behaviour", "educational background"],
     "correct_answer":"interpersonal behaviour",
     "explanation":"The correct answer is (C) interpersonal behaviour. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta190","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"For a good leader it is imperative to have",
     "options":["resources", "daily reflections on his conduct", "higher educational background", "belief in spirituality"],
     "correct_answer":"daily reflections on his conduct",
     "explanation":"The correct answer is (B) daily reflections on his conduct. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta191","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"The N.N. Kunzru committee was formed to look into the issue of _________ at the university level.",
     "options":["Administrative reforms", "Selection of vice-chancellors", "Sports education", "Medium of instruction"],
     "correct_answer":"Medium of instruction",
     "explanation":"The correct answer is (D) Medium of instruction. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta192","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"When we describe how a media system should function in conformity with ideal values, it is labelled as?",
     "options":["Social theory", "Normative theory", "Comparative theory", "Analytical theory"],
     "correct_answer":"Normative theory",
     "explanation":"The correct answer is (B) Normative theory. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta193","topic":"Teaching Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"A science teacher assign students a project where they design and conduct on experiment to investigate the effects of environmental factors on plant growth in real time. This assessment is an example of?",
     "options":["Summative Assessment", "Authentic Assessment", "Ipsative Assessment", "Peer Assessment"],
     "correct_answer":"Authentic Assessment",
     "explanation":"The correct answer is (B) Authentic Assessment. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta194","topic":"Teaching Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match List - I with List - II. List - I (Authors) List - II (Books) (a) Brahma Gupta (I) Lilāvati (b) Varāhamihira (II) Brahma Sphota Siddhanta (c) Bhaskarācharya (III) Nātyashāstra (d) Bharatmuni (IV) Brihat Samhitā",
     "options":["(a)-(II), (b)-(I), (c)-(IV), (d)-(III)", "(a)-(II), (b)-(IV), (c)-(I), (d)-(III)", "(a)-(IV), (b)-(II), (c)-(I), (d)-(III)", "(a)-(II), (b)-(IV), (c)-(III), (d)-(I)"],
     "correct_answer":"(a)-(II), (b)-(IV), (c)-(I), (d)-(III)",
     "explanation":"The correct answer is (B) (a)-(II), (b)-(IV), (c)-(I), (d)-(III). This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta195","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which of the following propositions is contradictory to the proposition \"All cats are Carnivores\"?",
     "options":["Some Cats are not Carnivores", "Some Cats are Carnivores", "No Cats are Carnivores", "No Carnivores are Cats"],
     "correct_answer":"Some Cats are not Carnivores",
     "explanation":"The correct answer is (A) Some Cats are not Carnivores. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta196","topic":"Teaching Aptitude","difficulty":"Hard","year":2024,"season":"June",
     "question":"Which of the following are the characteristics of mental development of Adolescents? (a) Increased ability to deal with abstraction 210 (b) Reviewing of hopes and aspirations (c) Increased ability to understand (d) Increased ability to generalize the facts (e) Ability of problem solving",
     "options":["(b), (d) and (e) only", "(a), (b) and (d) only", "(a), (c), (d) and (e) only", "(c) and (e) only"],
     "correct_answer":"(a), (c), (d) and (e) only",
     "explanation":"The correct answer is (C) (a), (c), (d) and (e) only. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta197","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"Dysentery is a waterborne disease caused by water contaminated by:",
     "options":["Virus", "Bacteria", "Fungi", "Protozoan"],
     "correct_answer":"Bacteria",
     "explanation":"The correct answer is (B) Bacteria. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta198","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which one of the following is not an air pollutant?",
     "options":["NO", "NO2", "NOx", "N2O"],
     "correct_answer":"N2O",
     "explanation":"The correct answer is (D) N2O. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta199","topic":"Teaching Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"Which of the following are arranged in the order of increasing connotation?",
     "options":["Vertebrates, mammals, canine, labradors", "Mammals, vertebrates, canine, labradors", "Canine, labradors, mammals, vertebrates", "Labradors, canine, mammals, vertebrates"],
     "correct_answer":"Vertebrates, mammals, canine, labradors",
     "explanation":"The correct answer is (A) Vertebrates, mammals, canine, labradors. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta200","topic":"Teaching Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"Which of the following statements are true regarding contrary propositions? (a) They cannot both be true (b) They cannot both be false (c) They can both be false (d) If one is true the other must be false",
     "options":["(b) and (c) Only", "(a), (b) and (c) Only", "(a), (c) and (d) Only", "(d) Only"],
     "correct_answer":"(a), (c) and (d) Only",
     "explanation":"The correct answer is (C) (a), (c) and (d) Only. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta201","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"The contents of swayamprabha channel - 15 with the theme of 'Capacity Building and Teacher Education' is provided by:",
     "options":["CEC, New Delhi", "IIT Delhi", "IGNOU, New Delhi", "IIT Kanpur"],
     "correct_answer":"IGNOU, New Delhi",
     "explanation":"The correct answer is (C) IGNOU, New Delhi. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta203","topic":"Teaching Aptitude","difficulty":"Hard","year":2024,"season":"June",
     "question":"The union government of India had in 2011 decided to establish a National Institute of Design in the states of: (a) Andhra Pradesh (b) Kerala (c) Assam (d) Goa (e) Haryana",
     "options":["(a), (b) and (c) Only", "(b), (c) and (d) Only", "(a), (c) and (e) Only", "(d) and (e) Only"],
     "correct_answer":"(a), (c) and (e) Only",
     "explanation":"The correct answer is (C) (a), (c) and (e) Only. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta204","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"An IT giant company has its Global Education Centre at:",
     "options":["Medak", "Ratnagiri", "Mysore", "Agartala"],
     "correct_answer":"Mysore",
     "explanation":"The correct answer is (C) Mysore. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta205","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"7 pumps, working 10 hours a day, can empty a tank in 20 days. How many hours a day must 5 pumps operate to empty the tank in 14 days?",
     "options":["20 hours", "18 hours", "16 hours", "14 hours"],
     "correct_answer":"20 hours",
     "explanation":"The correct answer is (A) 20 hours. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta206","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"Amount of destruction caused by an earthquake is measured by:",
     "options":["Richter Scale", "Intensity Scale", "Magnitude Scale", "Mercalli Scale"],
     "correct_answer":"Mercalli Scale",
     "explanation":"The correct answer is (D) Mercalli Scale. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta207","topic":"Teaching Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"An English teacher asks students to create a multimedia presentation analysing a novel's themes, characters, and literacy devices. Which assessment method is most suitable to check the real time progress of students?",
     "options":["Authentic Assessment", "Summative Assessment", "Norm-referenced Assessment", "Ipsative Assessment"],
     "correct_answer":"Authentic Assessment",
     "explanation":"The correct answer is (A) Authentic Assessment. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta208","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"Role of folklore in the society is:",
     "options":["To provide entertainment only", "To generate and observe broader social value", "To restrict public discourse", "To resist social change"],
     "correct_answer":"To generate and observe broader social value",
     "explanation":"The correct answer is (B) To generate and observe broader social value. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta209","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"What influences the tranformations that can be observed in public sphere?",
     "options":["Multi-level interests of performers and patrons", "A static set of rules", "The absence of economic and philosophical ideas", "Simple pleasure orientation"],
     "correct_answer":"Multi-level interests of performers and patrons",
     "explanation":"The correct answer is (A) Multi-level interests of performers and patrons. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta210","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"What is the difference between the sales of Amul and Warna in 2020? (in ₹ crore)",
     "options":["1804", "2380", "1870", "1760"],
     "correct_answer":"1870",
     "explanation":"The correct answer is (C) 1870. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta211","topic":"Teaching Aptitude","difficulty":"Hard","year":2024,"season":"June",
     "question":"Which of the following come under the category of stand-alone professional universities? (a) Universities of Journalism (b) Law Universities (c) Health Science Universities (d) Technical Universities (e) Homeopathy Universities",
     "options":["(a), (b), (c) Only", "(a), (b), (d) Only", "(c), (d), (e) Only", "(b), (c), (d) Only"],
     "correct_answer":"(b), (c), (d) Only",
     "explanation":"The correct answer is (D) (b), (c), (d) Only. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta212","topic":"Teaching Aptitude","difficulty":"Hard","year":2024,"season":"June",
     "question":"In a biology class, a teacher wants to conduct a formative assessment to gauge students understanding of cell structure and function. Which of the following tools would be most effective for creating interactive quizzes with immediate feedback? (a) Google forms (b) Adobe Illustrator (c) Kahoot (d) Audacity (e) Camtasia",
     "options":["(b), (c) and (e) Only", "(a), (c), (d) and (e) Only", "(a) and (c) Only", "(b), (d) and (e) Only"],
     "correct_answer":"(a) and (c) Only",
     "explanation":"The correct answer is (C) (a) and (c) Only. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta213","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"Many websites require the following to be completed: This is an example of which data issue?",
     "options":["Accuracy", "Matching", "Quality", "Security"],
     "correct_answer":"Security",
     "explanation":"The correct answer is (D) Security. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta214","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which one of the following is an example of natural climate forcing?",
     "options":["Green House Gases", "Volcanic erruptions", "Land use changes", "Tropospheric aerosols"],
     "correct_answer":"Volcanic erruptions",
     "explanation":"The correct answer is (B) Volcanic erruptions. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta216","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"When the content that we have previously learned interferes with the recall of something newly learned then the interference is:",
     "options":["Retroactive Inhibition", "Proactive Inhibition", "Attention Inhibition", "Response Inhibition"],
     "correct_answer":"Proactive Inhibition",
     "explanation":"The correct answer is (B) Proactive Inhibition. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta217","topic":"Teaching Aptitude","difficulty":"Hard","year":2024,"season":"June",
     "question":"Which of the following are biogas? (a) Marsh Gas (b) Swamp Gas (c) Producer Gas (d) Compost Gas (e) Flue Gas",
     "options":["(a), (b) and (d) Only", "(b), (c) and (e) Only", "(a), (c) and (e) Only", "(c), (d) and (e) Only"],
     "correct_answer":"(a), (b) and (d) Only",
     "explanation":"The correct answer is (A) (a), (b) and (d) Only. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta218","topic":"Teaching Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"Which of the following propositions cannot both be false, though they can both be true? (a) All cows are herbivores. (b) No cows are herbivores. (c) Some cows are herbivores. (d) Some cows are not herbivores.",
     "options":["(a) and (d) Only", "(c) and (d) Only", "(b) and (c) Only", "(a) and (c) Only"],
     "correct_answer":"(c) and (d) Only",
     "explanation":"The correct answer is (B) (c) and (d) Only. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta219","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which of the following propositions is contrary to the proposition. \"All cows are herbivores\"?",
     "options":["All herbivores are cows.", "Some cows are herbivores.", "Some cows are not herbivores.", "No cows are herbivores."],
     "correct_answer":"No cows are herbivores.",
     "explanation":"The correct answer is (D) No cows are herbivores.. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta220","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"Aim of Ashram-Sammilani was:",
     "options":["To function as a typical student union", "To talk about the student's rights", "To look after the functioning of the school with a body of elected students and teachers in", "To manage the financial situation of the institution"],
     "correct_answer":"To look after the functioning of the school with a body of elected students and teachers in",
     "explanation":"The correct answer is (C) To look after the functioning of the school with a body of elected students and teachers in. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta221","topic":"Teaching Aptitude","difficulty":"Hard","year":2024,"season":"June",
     "question":"Identify the correct statements related to factor analysis: (a) Factor analysis may be R-type factor analysis. (b) Factor analysis may be Q-type factor analysis. (c) Factor analysis is not useful when we want to condense and simplify the multivariate data. (d) Factor analysis is not useful in the context of empirical clustering of products, media or people. (e) Factor analysis can reveal the latent factors.",
     "options":["(a), (b) and (c) only", "(c), (d) and (e) only", "(b), (c) and (d) only", "(a), (b) and (e) only"],
     "correct_answer":"(a), (b) and (e) only",
     "explanation":"The correct answer is (D) (a), (b) and (e) only. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta222","topic":"Teaching Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match List - I with List - II. List - I List - II (a) Vyapti (I) Observation of agreement in absence (b) Anvaya (II) The minor term found to be characterised by the middle (c) Vyatireka (III) Method of agreement in presence (d) Paksa dharmata-jñāna (IV) Universal concomitance",
     "options":["(a)-(IV), (b)-(I), (c)-(II), (d)-(III)", "(a)-(I), (b)-(II), (c)-(IV), (d)-(III)", "(a)-(II), (b)-(I), (c)-(III), (d)-(IV)", "(a)-(IV), (b)-(III), (c)-(I), (d)-(II)"],
     "correct_answer":"(a)-(IV), (b)-(III), (c)-(I), (d)-(II)",
     "explanation":"The correct answer is (D) (a)-(IV), (b)-(III), (c)-(I), (d)-(II). This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta223","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"The personal intention to improve abilities and learn, no matter how performance suffers, is known as:",
     "options":["Perception", "Mastery Goal", "Meta cognition", "Moratorium"],
     "correct_answer":"Mastery Goal",
     "explanation":"The correct answer is (B) Mastery Goal. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta224","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"The example - 'Have you given up your evil ways' represents which of the following forms of informal fallacies?",
     "options":["Irrelevant conclusion", "Complex question", "False cause", "Petitito Principii"],
     "correct_answer":"Complex question",
     "explanation":"The correct answer is (B) Complex question. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta225","topic":"Teaching Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match List - I with List - II. List - I List - II (a) Pratijña (I) Statement of the reason (b) Hetu (II) Statement of the proposition to be proved (c) Upanaya (III) Conclusion proved (d) Nigamana (IV) Statement of the presence of the mark in the case in question",
     "options":["(a)-(I), (b)-(II), (c)-(III), (d)-(IV)", "(a)-(II), (b)-(I), (c)-(IV), (d)-(III)", "(a)-(III), (b)-(IV), (c)-(I), (d)-(II)", "(a)-(IV), (b)-(III), (c)-(II), (d)-(I)"],
     "correct_answer":"(a)-(II), (b)-(I), (c)-(IV), (d)-(III)",
     "explanation":"The correct answer is (B) (a)-(II), (b)-(I), (c)-(IV), (d)-(III). This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta226","topic":"Teaching Aptitude","difficulty":"Hard","year":2024,"season":"June",
     "question":"What are the characteristics of substances to be categorized as hazardous substances? (a) Ignitability (b) Malleability (c) Reactivity (d) Corrosivity (e) Toxicity",
     "options":["(a), (b), (c) and (d) only", "(b), (c), (d) and (e) only", "(a), (c), (d) and (e) only", "(a), (b), (d) and (e) only"],
     "correct_answer":"(a), (c), (d) and (e) only",
     "explanation":"The correct answer is (C) (a), (c), (d) and (e) only. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta227","topic":"Teaching Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match List - I with List - II. List - I List - II (a) Jean Piaget (I) Zone of proximal development (b) Lev Vygotsky (II) Eight stages of Psychological development (c) Erik Erikson (III) Theory of multiple intelligences (d) Howard Gardner (IV) Theory of cognitive development 244",
     "options":["(a)-(II), (b)-(III), (c)-(IV), (d)-(I)", "(a)-(III), (b)-(IV), (c)-(I), (d)-(II)", "(a)-(IV), (b)-(I), (c)-(II), (d)-(III)", "(a)-(I), (b)-(II), (c)-(III), (d)-(IV)"],
     "correct_answer":"(a)-(IV), (b)-(I), (c)-(II), (d)-(III)",
     "explanation":"The correct answer is (C) (a)-(IV), (b)-(I), (c)-(II), (d)-(III). This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta228","topic":"Teaching Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"The most important element for effective listening in the classroom is:",
     "options":["Advocacy", "Taking sides", "Empathy", "Ignoring the speakers appearance"],
     "correct_answer":"Empathy",
     "explanation":"The correct answer is (C) Empathy. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ta229","topic":"Teaching Aptitude","difficulty":"Hard","year":2024,"season":"June",
     "question":"Which of the following format contains exclusively the sound file format appropriate for web distribution? (a) AVI (b) AIF (c) MIDI (d) MP4 (e) MP3",
     "options":["(a), (c) and (e) only", "(b), (c) and (d) only", "(c), (d) and (e) only", "(b), (c) and (e) only"],
     "correct_answer":"(b), (c) and (e) only",
     "explanation":"The correct answer is (D) (b), (c) and (e) only. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ict1056","topic":"Teaching Aptitude","difficulty":"Hard","year":2024,"season":"June",
     "question":"What can be correctly inferred about the Traditional Teaching Method and Support System? (a) Teacher is responsible to control the class and teach with the usage of blackboard (b) It is also known as 'Back-to Basics' System. (c) The student carries the responsibilities to use self-learning tools. (d) Virtual labs are used as one of the Teaching tools. (e) Charts, Maps and Textbooks are the prime resources and handouts are used by the teacher",
     "options":["(b) and (c) only", "(a), (b) and (d) only", "(d) and (e) only", "(a), (b), and (e) only"],
     "correct_answer":"(a), (b), and (e) only",
     "explanation":"The correct answer is (D) (a), (b), and (e) only. This is a standard UGC NET 2024 June question on Teaching Aptitude."},


    # ↑↑↑ PASTE YOUR NEW Teaching Aptitude QUESTIONS ABOVE THIS LINE ↑↑↑
]

# ── 2. RESEARCH APTITUDE ─────────────────────────────────────────────
Q_RESEARCH_APTITUDE = [
    {"id":"ra001","topic":"Research Aptitude","difficulty":"Medium","year":2023,"season":"June","question":"Which type of research aims to solve immediate practical problems?","options":["Fundamental research","Applied research","Action research","Historical research"],"correct_answer":"Action research","explanation":"Action research is conducted by practitioners to solve specific, immediate problems."},
    {"id":"ra002","topic":"Research Aptitude","difficulty":"Easy","year":2021,"season":"December","question":"A hypothesis is best described as:","options":["A proven fact","A tentative statement to be tested","A summary of findings","A literature review"],"correct_answer":"A tentative statement to be tested","explanation":"A hypothesis is a tentative, testable proposition about the relationship between variables."},
    {"id":"ra003","topic":"Research Aptitude","difficulty":"Hard","year":2020,"season":"December","question":"Which sampling method ensures every member has an equal chance of being selected?","options":["Purposive sampling","Snowball sampling","Simple Random Sampling","Quota sampling"],"correct_answer":"Simple Random Sampling","explanation":"Simple Random Sampling gives every individual an equal probability of selection."},
    {"id":"ra004","topic":"Research Aptitude","difficulty":"Medium","year":2019,"season":"June","question":"The term 'triangulation' in research refers to:","options":["Geometric analysis","Using multiple methods to validate findings","A statistical test","Sampling technique"],"correct_answer":"Using multiple methods to validate findings","explanation":"Triangulation uses multiple data sources to cross-check and validate research findings."},
    {"id":"ra005","topic":"Research Aptitude","difficulty":"Medium","year":2018,"season":"June","question":"Which research design determines cause-and-effect relationships?","options":["Descriptive","Correlational","Experimental","Ethnographic"],"correct_answer":"Experimental","explanation":"Experimental research establishes causality by manipulating an independent variable."},
    {"id":"ra006","topic":"Research Aptitude","difficulty":"Hard","year":2017,"season":"December","question":"A Type I error in research refers to:","options":["Accepting a false null hypothesis","Rejecting a true null hypothesis","Failing to collect data","Using the wrong test"],"correct_answer":"Rejecting a true null hypothesis","explanation":"A Type I error occurs when the null hypothesis is true but incorrectly rejected."},
    # ════════════════════════════════════════════════════════════════════
    # ADD MORE Research Aptitude QUESTIONS BELOW ↓
    # ════════════════════════════════════════════════════════════════════
    {"id":"ra007","topic":"Research Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"Which of the following is a non-parametric test?",
     "options":["t-test","ANOVA","Chi-square test","Pearson correlation"],
     "correct_answer":"Chi-square test",
     "explanation":"Chi-square is a non-parametric test used for categorical data and does not assume normal distribution."},

    {"id":"ra008","topic":"Research Aptitude","difficulty":"Easy","year":2024,"season":"December",
     "question":"A review of literature in research primarily helps to:",
     "options":["Collect primary data","Understand existing knowledge on the topic","Select the sample","Analyse data"],
     "correct_answer":"Understand existing knowledge on the topic",
     "explanation":"Literature review helps researchers understand what is already known and identify gaps in existing knowledge."},

    {"id":"ra009","topic":"Research Aptitude","difficulty":"Hard","year":2023,"season":"December",
     "question":"Ethnographic research is primarily associated with:",
     "options":["Quantitative paradigm","Experimental design","Qualitative paradigm","Survey method"],
     "correct_answer":"Qualitative paradigm",
     "explanation":"Ethnography involves in-depth, qualitative study of people in their natural settings."},

    {"id":"ra010","topic":"Research Aptitude","difficulty":"Medium","year":2022,"season":"June",
     "question":"The 'Hawthorne Effect' refers to:",
     "options":["Bias due to researcher's expectations","Change in behaviour when subjects know they are being observed","Sampling error","Validity threat"],
     "correct_answer":"Change in behaviour when subjects know they are being observed",
     "explanation":"The Hawthorne Effect occurs when research subjects alter their behaviour because they are aware of being studied."},

    {"id":"ra011","topic":"Research Aptitude","difficulty":"Hard","year":2021,"season":"June",
     "question":"Which measure indicates the consistency of a research instrument?",
     "options":["Validity","Reliability","Objectivity","Standardisation"],
     "correct_answer":"Reliability",
     "explanation":"Reliability is the degree to which a research instrument yields consistent results over repeated measurements."},
        {"id":"ra012","topic":"Research Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"If you want to understand the theoretical reasons that led researchers to conduct a study that appeared as a research article in a journal, you would read which of the following sections of the research article?",
     "options":["discussion", "abstract", "introduction", "results"],
     "correct_answer":"introduction",
     "explanation":"The correct answer is (C) introduction. This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra013","topic":"Research Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"When the sample has been randomly selected, which among the following may be expected in cross-sectional research designs? (a) strong external validity (b) weak external validity (c) weak internal validity (d) strong internal validity",
     "options":["Only (a) and (c)", "Only (a) and (d)", "Only (b) and (c)", "Only (b) and (d)"],
     "correct_answer":"Only (a) and (c)",
     "explanation":"The correct answer is (A) Only (a) and (c). This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra014","topic":"Research Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"Identify the probability sampling techniques? (a) simple random sampling (b) snowball sampling (c) stratified random sampling (d) convenience sampling",
     "options":["Only (a) and (b)", "Only (b) and (c)", "Only (a) and (c)", "Only (b) and (d)"],
     "correct_answer":"Only (a) and (c)",
     "explanation":"The correct answer is (C) Only (a) and (c). This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra015","topic":"Research Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which of the following research approaches suggests that theory is an outcome of research?",
     "options":["deductive approach", "inductive approach", "quantitative approach", "cross-sectional approach"],
     "correct_answer":"inductive approach",
     "explanation":"The correct answer is (B) inductive approach. This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra016","topic":"Research Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"The students' t-test would be useful for? (a) comparing two groups to see whether their means differ. (b) comparing multiple groups (more than two) to see whether their means differ. (c) testing the significance of correlation coefficient. (d) testing the significance of regression coefficient.",
     "options":["Only (a), (b) and (c)", "Only (b) and (d)", "Only (a), (c) and (d)", "Only (a), (b), (c) and (d)"],
     "correct_answer":"Only (a), (c) and (d)",
     "explanation":"The correct answer is (C) Only (a), (c) and (d). This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra017","topic":"Research Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"A measure of the consistency of observations of a single situation made by different people refers to.",
     "options":["Construct validity", "Internal validity", "Split-Half reliability", "Interrator reliability"],
     "correct_answer":"Interrator reliability",
     "explanation":"The correct answer is (D) Interrator reliability. This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra018","topic":"Research Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which of the following represents the epistemological orientation of quantitative research?",
     "options":["Interpretivism", "Constructionism", "Positivism", "Inductivism"],
     "correct_answer":"Positivism",
     "explanation":"The correct answer is (C) Positivism. This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra019","topic":"Research Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"The approach in which researchers use the existing data to create groups for comparison is called",
     "options":["Operational", "Ex post facto", "Experimental", "Quasi-experimental"],
     "correct_answer":"Ex post facto",
     "explanation":"The correct answer is (B) Ex post facto. This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra020","topic":"Research Aptitude","difficulty":"Hard","year":2024,"season":"June",
     "question":"Identify the nominal variables. (a) Gender (b) Annoyance level (c) Caste (d) Temperature in Kelvin (e) Economic status",
     "options":["(a), (b), (c) and (d) only", "(a) and (c) only", "(b) and (e) only", "(a), (b), (c) and (e) only"],
     "correct_answer":"(a) and (c) only",
     "explanation":"The correct answer is (B) (a) and (c) only. This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra021","topic":"Research Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match List I with List II. List -I (Initiatives in Higher Education) List -II (Description) (a) GIAN (I) Translation of research knowledge into viable technology (products and processes) (b) IMPRINT-2 (II) Achieve three Cardinal principles of Education policy namely, access, equity and quality (c) DIGILOCKER (III) Tap the talent pool of scientists and entrepreneurs internationally (d) SWAYAM (IV) Issuance and verification of documents and certificates in a digital way",
     "options":["(a)-(III), (b)-(I), (c)-(II), (d)-(IV)", "(a)-(II), (b)-(I), (c)-(IV), (d)-(III)", "(a)-(I), (b)-(III), (c)-(II), (d)-(IV)", "(a)-(III), (b)-(I), (c)-(IV), (d)-(II)"],
     "correct_answer":"(a)-(III), (b)-(I), (c)-(IV), (d)-(II)",
     "explanation":"The correct answer is (D) (a)-(III), (b)-(I), (c)-(IV), (d)-(II). This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra022","topic":"Research Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match List I with List - II. List -I (Term/concept) List -II (Description) (a) Upanaya (I) The knowledge of Pakşadharmatā as qualified by Vyāpti (b) Parāmarśa (II) The invariable relation or association of the Middle term in the minor term (c) Vyāpti (III) The application of the universal concomitance to the present case (d) Pakşadharmatā (IV) The invariable association of the middle term with the major term",
     "options":["(a)-(II), (b)-(I), (c)-(III), (d)-(IV)", "(a)-(III), (b)-(II), (c)-(IV), (d)-(I)", "(a)-(IV), (b)-(III), (c)-(I), (d)-(II)", "(a)-(III), (b)-(I), (c)-(IV), (d)-(II)"],
     "correct_answer":"(a)-(III), (b)-(I), (c)-(IV), (d)-(II)",
     "explanation":"The correct answer is (D) (a)-(III), (b)-(I), (c)-(IV), (d)-(II). This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra023","topic":"Research Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"Survey research on a single, case with a view to revealing important features about its nature, corresponds to which of the following research designs?",
     "options":["Cross - sectional", "Longitudinal", "Case study", "Comparative"],
     "correct_answer":"Case study",
     "explanation":"The correct answer is (C) Case study. This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra024","topic":"Research Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which of the following is concerned with the question whether the measure of a concept truly represents that concept?",
     "options":["internal validity", "external validity", "construct validity", "transferability"],
     "correct_answer":"construct validity",
     "explanation":"The correct answer is (C) construct validity. This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra025","topic":"Research Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match List I with List - II. List -I (Learning style) List -II (Characteristic) (a) Converger (I) They are best at concrete experience and reflective observation. Their strength is their imaginative ability They tend to be interested in people and emotional elements. (b) Diverger (II) They are good at Abstract Conceptualization and Active Experimentation like solving problems; practical application of ideas (c) Assimilator (III) They enjoy and seek new experiences and adopt to new situations; and are intuitive, risk-takers open minded. (d) Accomodator (IV) Ability to create theoretical models; possess sound logic, inductive reasoning, Analytic less interested in people 40",
     "options":["(a)-(IV), (b)-(III), (c)-(II), (d)-(I)", "(a)-(III), (b)-(II), (c)-(I), (d)-(IV)", "(a)-(II), (b)-(I), (c)-(IV), (d)-(III)", "(a)-(I), (b)-(II), (c)-(III), (d)-(IV)"],
     "correct_answer":"(a)-(II), (b)-(I), (c)-(IV), (d)-(III)",
     "explanation":"The correct answer is (C) (a)-(II), (b)-(I), (c)-(IV), (d)-(III). This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra026","topic":"Research Aptitude","difficulty":"Hard","year":2024,"season":"June",
     "question":"According to UGC Regulations 2018 on Plagiarism, a student will have to submit a revised thesis for which of the following similarities of thesis? (a) 12% (b) 27% (c) 46% (d) 66% (e) 70%",
     "options":["(a), (b) and (c) only", "(b), (c), and (d) only", "(c), (d) and (e) only", "(a) and (b) only"],
     "correct_answer":"(a), (b) and (c) only",
     "explanation":"The correct answer is (A) (a), (b) and (c) only. This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra027","topic":"Research Aptitude","difficulty":"Hard","year":2024,"season":"June",
     "question":"Arrange the following institutions according to their year of establishment (from earliest to the most recent) (a) National Council of Rural Institutes (NCRI) (b) Indian Council of Social Science Research (ICSSR) (c) Indian Institute of Advanced Study (IIAS) (d) Indian Council of Historical Research (ICHR) (e) Indian Council of Philosophical Research (ICPR)",
     "options":["(a), (b), (c), (d), (e)", "(c), (d), (b), (e), (a)", "(b), (e), (a), (c), (d)", "(c), (b), (d), (e), (a)"],
     "correct_answer":"(c), (b), (d), (e), (a)",
     "explanation":"The correct answer is (D) (c), (b), (d), (e), (a). This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra028","topic":"Research Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"Qualitative content analysis of documents relating to different time periods corresponds to which of the following research designs?",
     "options":["Cross-sectional", "Longitudinal", "Case study", "Comparative"],
     "correct_answer":"Longitudinal",
     "explanation":"The correct answer is (B) Longitudinal. This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra029","topic":"Research Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"Qualitative research is generally associated with-",
     "options":["Inductive approach", "Deductive approach", "Positivism", "Objectivism"],
     "correct_answer":"Inductive approach",
     "explanation":"The correct answer is (A) Inductive approach. This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra030","topic":"Research Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match the List-I with List-II List - I (Type of Variables) List - II (Example) (a) Nominal (I) Anger level (b) Ordinal (II) Crop yield (c) Interval (III) Type of forest (d) Ratio (IV) Temperature in Fahrenheit",
     "options":["(a)-(I), (b)-(II), (c)-(IV), (d)-(III)", "(a)-(I), (b)-(II), (c)-(III), (d)-(IV)", "(a)-(III), (b)-(I), (c)-(IV), (d)-(II)", "(a)-(III), (b)-(IV), (c)-(I), (d)-(II)"],
     "correct_answer":"(a)-(III), (b)-(I), (c)-(IV), (d)-(II)",
     "explanation":"The correct answer is (C) (a)-(III), (b)-(I), (c)-(IV), (d)-(II). This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra031","topic":"Research Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match List - I with List - II. List - I (Type of variable) List - II (Example) (a) Nominal (I) Satisfaction level (b) Ordinal (II) Weight (c) Interval (III) Ethnicity (d) Ratio (IV) Year of death",
     "options":["(a)-(I), (b)-(II), (c)-(III), (d)-(IV)", "(a)-(I), (b)-(III), (c)-(II), (d)-(IV)", "(a)-(III), (b)-(IV), (c)-(II), (d)-(I)", "(a)-(III), (b)-(I), (c)-(IV), (d)-(II)"],
     "correct_answer":"(a)-(III), (b)-(I), (c)-(IV), (d)-(II)",
     "explanation":"The correct answer is (D) (a)-(III), (b)-(I), (c)-(IV), (d)-(II). This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra032","topic":"Research Aptitude","difficulty":"Hard","year":2024,"season":"June",
     "question":"According to UGC regulations 2018 on plagiarism, which of the following similarities constitute Level-1 plagiarism? (a) 12% (b) 42% (c) 28% (d) 56% (e) 37%",
     "options":["(a), (b) and (c) only", "(b), (c) and (d) only", "(a), (c) and (e) only", "(b), (c) and (e) only"],
     "correct_answer":"(a), (c) and (e) only",
     "explanation":"The correct answer is (C) (a), (c) and (e) only. This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra033","topic":"Research Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which of the following criteria in research relates mainly to the issue of causality?",
     "options":["Transferability", "Measurement validity", "External validity", "Internal validity"],
     "correct_answer":"Internal validity",
     "explanation":"The correct answer is (D) Internal validity. This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra034","topic":"Research Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"A researcher decides to tell participants something false about a research session in order to mislead them. The researcher is using:",
     "options":["Naturalistic observation", "Role playing", "Active deception", "Dehoaxing"],
     "correct_answer":"Active deception",
     "explanation":"The correct answer is (C) Active deception. This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra035","topic":"Research Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"In qualitative research, which of the following criteria is concerned with the question _____ do the findings apply to other contexts?",
     "options":["Transferability", "Credibility", "Internal validity", "Confirmability"],
     "correct_answer":"Transferability",
     "explanation":"The correct answer is (A) Transferability. This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra036","topic":"Research Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"The process of telling research participants of any deception or ruses used in a study, is known as",
     "options":["Active deception", "Passive deception", "Dehoaxing", "Desensitization"],
     "correct_answer":"Dehoaxing",
     "explanation":"The correct answer is (C) Dehoaxing. This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra037","topic":"Research Aptitude","difficulty":"Hard","year":2024,"season":"June",
     "question":"According to UGC regulations 2018 on plagiarism a faculty will be denied two successive annual increments for which of the following similarities in research publications? (a) 42% (b) 58% (c) 76% (d) 62% (e) 52% 75",
     "options":["(a), (b) and (e) Only", "(b), (c) and (d) Only", "(a), (b), (d) and (e) Only", "(c) and (d) Only"],
     "correct_answer":"(c) and (d) Only",
     "explanation":"The correct answer is (D) (c) and (d) Only. This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra038","topic":"Research Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match the List-I with List-II List-I (Type of variable) List-II (Example) (a) Nominal (I) Happiness level (b) Ordinal (II) Height (c) Interval (III) Blood group (d) Ratio (IV) Year of birth",
     "options":["(a)-(I), (b)-(II), (c)-(III), (d)-(IV)", "(a)-(II), (b)-(III), (c)-(IV), (d)-(I)", "(a)-(III), (b)-(I), (c)-(IV), (d)-(II)", "(a)-(IV), (b)-(III), (c)-(I), (d)-(II)"],
     "correct_answer":"(a)-(III), (b)-(I), (c)-(IV), (d)-(II)",
     "explanation":"The correct answer is (C) (a)-(III), (b)-(I), (c)-(IV), (d)-(II). This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra039","topic":"Research Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"The numerator and denominator degrees of freedom are used in the computation of which of the following test statistics?",
     "options":["Z", "Chi-Square", "t", "F"],
     "correct_answer":"F",
     "explanation":"The correct answer is (D) F. This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra040","topic":"Research Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which of the following types of validity is mainly concerned with the issue of causality?",
     "options":["Measurement Validity", "External Validity", "Internal Validity", "Ecological Validity"],
     "correct_answer":"Internal Validity",
     "explanation":"The correct answer is (C) Internal Validity. This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra041","topic":"Research Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"In the context of medical research, a comparison group that receives what appears to be a treatment, but which actually has no effect, is called the",
     "options":["experimental group", "control group", "placebo group", "independent group"],
     "correct_answer":"placebo group",
     "explanation":"The correct answer is (C) placebo group. This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra042","topic":"Research Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"In the APA style of writing journal article references, identify the correct order of the following information about the research article: (a) Title of the article (b) Last name of the author (c) Page numbers (d) Name of journal",
     "options":["(a), (b), (c), (d)", "(a), (b), (d), (c)", "(b), (a), (d), (c)", "(b), (d), (a), (c)"],
     "correct_answer":"(b), (a), (d), (c)",
     "explanation":"The correct answer is (C) (b), (a), (d), (c). This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra043","topic":"Research Aptitude","difficulty":"Hard","year":2024,"season":"June",
     "question":"Which of the following are public sector funding agencies for research in India? (a) ΤΑΤΑ Τrust (b) ICAR (c) ICHR (d) ICMR (e) Population Foundation of India (PFI)",
     "options":["(a), (b), (c) only", "(b), (c), (d) only", "(d), (e) only", "(a), (c), (e) only"],
     "correct_answer":"(b), (c), (d) only",
     "explanation":"The correct answer is (B) (b), (c), (d) only. This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra044","topic":"Research Aptitude","difficulty":"Hard","year":2024,"season":"June",
     "question":"Identify the ordinal variables. (a) Rank of army personnel (b) Religion (c) Caste (d) Annoyance level (e) Temperature in Celsius",
     "options":["(a), (b), (c) and (d) only", "(b) and (c) only", "(a) and (d) only", "(d) and (e) only"],
     "correct_answer":"(a) and (d) only",
     "explanation":"The correct answer is (C) (a) and (d) only. This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra045","topic":"Research Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"Which among the following research designs are likely to suffer from the problem of sample attrition? (a) Cross-sectional studies (b) Longitudinal studies (c) Panel studies (d) Cohort studies",
     "options":["(a) and (b) only", "(a), (b) and (d) only", "(a), (c) and (d) only", "(b), (c) and (d) only"],
     "correct_answer":"(b), (c) and (d) only",
     "explanation":"The correct answer is (D) (b), (c) and (d) only. This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra046","topic":"Research Aptitude","difficulty":"Hard","year":2024,"season":"June",
     "question":"The major initiatives of the union government during the XI plan in the higher education sector were: (a) Establishment of 14 world class universities (b) Diversion of funds to private universities better performance (c) Strengthening of science based higher education and research in universities (d) Restructuring of different councils (e) Financially supporting uncovered state universities and colleges",
     "options":["(a), (b), (c) only", "(a), (c), (e) only", "(b), (c), (d) only", "(d), (e) only"],
     "correct_answer":"(a), (c), (e) only",
     "explanation":"The correct answer is (B) (a), (c), (e) only. This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra047","topic":"Research Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which of the following research designs would allow systematic elimination of extraneous variables other than those you are interested in?",
     "options":["Longitudinal research", "Qualitative research", "Correlational research", "Experimental research"],
     "correct_answer":"Experimental research",
     "explanation":"The correct answer is (D) Experimental research. This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra048","topic":"Research Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"The semiotic study of Charles Pierce is __________ in its approach:",
     "options":["Experimental", "Historical", "Quasi legal", "Quasi- scientific"],
     "correct_answer":"Quasi- scientific",
     "explanation":"The correct answer is (D) Quasi- scientific. This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra049","topic":"Research Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"Identify the main pre-occupations of quantitative researchers (a) Measurement (b) Causality (c) Description (d) Generalization",
     "options":["(a), (b) and (c) only", "(b), (c) and (d) only", "(a), (b) and (d) only", "(a), (c) and (d) only"],
     "correct_answer":"(a), (b) and (d) only",
     "explanation":"The correct answer is (C) (a), (b) and (d) only. This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra050","topic":"Research Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match List I with List - II. List - I (Total sum of squares (TSS) and Residual sum of squares) List - II (R2 of Regression Model) (a) RSS = 5, TSS = 20 (I) 0.62 (b) RSS = 5, TSS = 25 (II) 0.75 (c) RSS = 10, TSS = 25 (III) 0.8 (d) RSS = 12, TSS = 32 (IV) 0.6",
     "options":["(a)-(I), (b)-(II), (c)-(III), (d)-(IV)", "(a)-(II), (b)-(III), (c)-(IV), (d)-(I)", "(a)-(III), (b)-(IV), (c)-(I), (d)-(II)", "(a)-(IV), (b)-(I), (c)-(II), (d)-(III)"],
     "correct_answer":"(a)-(II), (b)-(III), (c)-(IV), (d)-(I)",
     "explanation":"The correct answer is (B) (a)-(II), (b)-(III), (c)-(IV), (d)-(I). This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra051","topic":"Research Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match List I with List II. List - I (Total Sum Squares (TSS) and Residual Sum of Sequences (RSS) List - II (R2 of Regression Model) (a) RSS = 25, TSS = 60 (I) 0.46 (b) RSS = 35, TSS = 75 (II) 0.57 (c) RSS = 30, TSS = 70 (III) 0.53 (d) RSS = 40, TSS = 75 (IV) 0.58",
     "options":["(a)-(I), (b)-(II), (c)-(III), (d)-(IV)", "(a)-(II), (b)-(III), (c)-(IV), (d)-(I)", "(a)-(ІІІ), (b)-(IV), (c)-(I), (d)-(II)", "(a)-(IV), (b)-(III), (c)-(II), (d)-(I)"],
     "correct_answer":"(a)-(IV), (b)-(III), (c)-(II), (d)-(I)",
     "explanation":"The correct answer is (D) (a)-(IV), (b)-(III), (c)-(II), (d)-(I). This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra052","topic":"Research Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"Identify the main preoccupations of qualitative researches. (a) Generalization (b) Description (c) Emphasis on context (d) Flexibility",
     "options":["(a), (b) and (c) only", "(b), (c) and (d) only", "(a), (b) and (d) only", "(a), (c) and (d) only"],
     "correct_answer":"(b), (c) and (d) only",
     "explanation":"The correct answer is (B) (b), (c) and (d) only. This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra053","topic":"Research Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"Identify the threats to internal validity. (a) Selection threat (b) Maturation threat (c) Attrition threat (d) Testing threat",
     "options":["(a), (b) and (c) only", "(b), (c) and (d) only", "(a), (c) and (d) only", "(a), (b), (c) and (d)"],
     "correct_answer":"(a), (b), (c) and (d)",
     "explanation":"The correct answer is (D) (a), (b), (c) and (d). This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra054","topic":"Research Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"According to UGC Regulations 2018 on Plagiarism, which of the following percentages of similarity in a research article would result in debarring a university teacher from supervising a PhD. Student for a period of two years?",
     "options":["27 %", "38 %", "44 %", "65 %"],
     "correct_answer":"44 %",
     "explanation":"The correct answer is (C) 44 %. This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra055","topic":"Research Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"Important key message the above text conveys about holiday eating can be stated as follows:",
     "options":["It is important to completely avoid indulgence", "Occasional indulgence is unlikely to cause lasting damage", "Diet has no significant impact on the immune system", "Holidays are an ideal time to experiment with extreme diets"],
     "correct_answer":"Occasional indulgence is unlikely to cause lasting damage",
     "explanation":"The correct answer is (B) Occasional indulgence is unlikely to cause lasting damage. This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra056","topic":"Research Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which of the following types of sampling is likely to have maximum bias?",
     "options":["Simple random sampling", "Stratified random sampling", "Snowball sampling", "Cluster random sampling"],
     "correct_answer":"Snowball sampling",
     "explanation":"The correct answer is (C) Snowball sampling. This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra057","topic":"Research Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"Identify the threats to internal validity associated with participants in a study. (a) Testing threat (b) Selection threat (c) History threat (d) Attrition threat 145",
     "options":["(a), (b) and (c) only", "(b), (c) and (d) only", "(a), (b) and (d) only", "(a), (c) and (d) only"],
     "correct_answer":"(b), (c) and (d) only",
     "explanation":"The correct answer is (B) (b), (c) and (d) only. This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra058","topic":"Research Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match List - I with List - II. List - I (Variable) List - II (Description) (a) Dichotomous variable (I) Is causally influenced by another variable (b) Independent variable (II) Where distances between categories are identical across its range of categories (c) Dependent variable (III) Has just two categories (d) Interval variable (IV) Has a causal impact on another variable 146",
     "options":["(a)-(I), (b)-(II), (c)-(III), (d)-(IV)", "(a)-(III), (b)-(I), (c)-(IV), (d)-(II)", "(a)-(III), (b)-(IV), (c)-(I), (d)-(II)", "(a)-(I), (b)-(III), (c)-(IV), (d)-(II)"],
     "correct_answer":"(a)-(III), (b)-(IV), (c)-(I), (d)-(II)",
     "explanation":"The correct answer is (C) (a)-(III), (b)-(IV), (c)-(I), (d)-(II). This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra059","topic":"Research Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which of the following types of sampling is likely to have least bias?",
     "options":["Snowball sampling", "Simple random sampling", "Convenience sampling", "Purposive sampling"],
     "correct_answer":"Simple random sampling",
     "explanation":"The correct answer is (B) Simple random sampling. This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra060","topic":"Research Aptitude","difficulty":"Hard","year":2024,"season":"June",
     "question":"Identify the correct statements regarding survey research. (a) A closed ended question contains a set of answers that a respondent chooses (b) Self-Deception Positivity is a from of social desirability bias (c) Impression Management is a form of social desirability bias (d) In key informant sampling, a researcher uses a member of the population of interest to actively recruit others",
     "options":["(a), (b) and (c) only", "(b), (c) and (d) only", "(a), (b) and (d) only", "(a), (c) and (d) only"],
     "correct_answer":"(a), (b) and (c) only",
     "explanation":"The correct answer is (A) (a), (b) and (c) only. This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra061","topic":"Research Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"Identify the correct statements regarding web-based study of human subjects (a) It requires considerably more time per person than laboratory based study. (b) Data collection occurs at the convenience of the participant. (c) Data collection is automatic. (d) It can be conducted on participants who would have been out of reach of the researcher in physical mode.",
     "options":["(a), (b) and (c) only", "(b), (c) and (d) only", "(a), (c) and (d) only", "(a), (b) and (d) only"],
     "correct_answer":"(b), (c) and (d) only",
     "explanation":"The correct answer is (B) (b), (c) and (d) only. This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra062","topic":"Research Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match the List-I with List-II List - I (Thinkers) List - II (Text/Subject) (a) Bharatmuni (I) Astāngasamgrah (b) Patanjali (II) Mahabhāsya (c) Vāgbhata (III) Brahmsphutasiddhānta (d) Brahmagupta (IV) Natyasāstra List - I (Scale of measurement List - II (Example of variable) (a) Nominal (I) Weight of students (b) Ordinal (II) Ethnicity (c) Interval (III) Degree of annoyance (d) Ratio (IV) Date of birth 165",
     "options":["(a)-(IV), (b)-(II), (c)-(I), (d)-(III)", "(a)-(IV), (b)-(I), (c)-(II), (d)-(III)", "(a)-(III), (b)-(I), (c)-(II), (d)-(IV)", "(a)-(III), (b)-(II), (c)-(I), (d)-(IV)"],
     "correct_answer":"(a)-(IV), (b)-(II), (c)-(I), (d)-(III)",
     "explanation":"The correct answer is (A) (a)-(IV), (b)-(II), (c)-(I), (d)-(III). This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra063","topic":"Research Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"A researcher conducts a study on a population and obtains some results. He now wants to generalize these results to a different population, For this, his measurements should show",
     "options":["External Validity", "Internal Validity", "Convergent Validity", "Divergent Validity"],
     "correct_answer":"External Validity",
     "explanation":"The correct answer is (A) External Validity. This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra064","topic":"Research Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"If a conclusion incorporates a casual relationship between two or more variables it has measured.",
     "options":["External validity", "Internal validity", "Replicability", "Conceptualisation"],
     "correct_answer":"Internal validity",
     "explanation":"The correct answer is (B) Internal validity. This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra065","topic":"Research Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"Qualitative research makes use of.",
     "options":["Scaling", "Factoring", "Representative quotations", "SPSS"],
     "correct_answer":"Representative quotations",
     "explanation":"The correct answer is (C) Representative quotations. This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra066","topic":"Research Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"Arrange the following terms in order of increading abstractness: (a) Alloy (b) Metal (c) Steel (d) Mineral",
     "options":["(c), (b), (d), (a)", "(c), (a), (b), (d)", "(c), (a), (d), (b)", "(d), (b), (a), (c)"],
     "correct_answer":"(c), (a), (b), (d)",
     "explanation":"The correct answer is (B) (c), (a), (b), (d). This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra067","topic":"Research Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"Identify the correct statement about the quantitative content analysis:",
     "options":["It can allow a certain amount of longitudinal analysis", "It is an obtrusive method", "It is a very rigid method", "It is a reactive method"],
     "correct_answer":"It can allow a certain amount of longitudinal analysis",
     "explanation":"The correct answer is (A) It can allow a certain amount of longitudinal analysis. This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra068","topic":"Research Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"Suppose H0 = Null Hypothesis, Ha = Alternate Hypothesis, µ = population mean. µHo = hypothesized mean. A researcher sets up H0: µ = µHo and Ha: µ < µHo. In this situation, the researcher would apply",
     "options":["right-tailed test", "left-tailed test", "two-tailed test", "half-tailed test"],
     "correct_answer":"left-tailed test",
     "explanation":"The correct answer is (B) left-tailed test. This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra069","topic":"Research Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"The criterion of dependendability' in qualitative research parallels which of the following criteria in quantitative research?",
     "options":["Objectivity", "internal validity", "external validity", "reliability"],
     "correct_answer":"reliability",
     "explanation":"The correct answer is (D) reliability. This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra070","topic":"Research Aptitude","difficulty":"Hard","year":2024,"season":"June",
     "question":"Which of the following are the functions of Indian Council of Social Science Research? (a) Encourage delinking of social sciences from natural sciences (b) Provide scholarship for research in social sciences. 188 (c) Give financial support to institutional journals of research. (d) Promote social science research. (e) Blacklist non-performing social science institutions from time to time.",
     "options":["(a), (b) and (c) only", "(b), (c) and (d) only", "(c), (d) and (e) only", "(a), (d) and (e) only"],
     "correct_answer":"(b), (c) and (d) only",
     "explanation":"The correct answer is (B) (b), (c) and (d) only. This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra071","topic":"Research Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"A quantitative research would be mainly concerned with (a) measurement (b) causality (c) context (d) replication",
     "options":["(a), (b) and (c) only", "(a), (b) and (d) only", "(b), (c) and (d) only", "(a), (c) and (d) only"],
     "correct_answer":"(a), (b) and (d) only",
     "explanation":"The correct answer is (B) (a), (b) and (d) only. This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra072","topic":"Research Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"The criterion of ‘credibility’ in qualitative research is equivalent to which of the following criteria in quantitative research?",
     "options":["external validity", "internal validity", "objectivity", "reliability"],
     "correct_answer":"internal validity",
     "explanation":"The correct answer is (B) internal validity. This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra073","topic":"Research Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"The numerator and denominator degrees of freedom are used in which of the following test- statistic in hypothesis testing?",
     "options":["t", "F", "Ƶ", "𝜒𝜒2 (chi square)"],
     "correct_answer":"F",
     "explanation":"The correct answer is (B) F. This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra074","topic":"Research Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"A sampling technique that relies on getting information from people who know about a population of interest rather than from members of that population themselves, refers to?",
     "options":["Probability sampling", "Key informant sampling", "Snowball sampling", "Quota sampling"],
     "correct_answer":"Key informant sampling",
     "explanation":"The correct answer is (B) Key informant sampling. This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra075","topic":"Research Aptitude","difficulty":"Hard","year":2024,"season":"June",
     "question":"A sociology professor wants to gather student's opinions on controversial social issue discussed in class which tools allow the professor to create polls and analyze responses in real-time? (a) Poll everywhere (b) Camtasia (c) Strawpoll (d) Survey Monkey (e) Mentimeter",
     "options":["(a), (b) and (d) only", "(a), (c), (d) and (e) only", "(b) and (e) only", "(b), (c) and (d) only"],
     "correct_answer":"(a), (c), (d) and (e) only",
     "explanation":"The correct answer is (B) (a), (c), (d) and (e) only. This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra076","topic":"Research Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"Your measurements should show which of the following validities if you want to generalize the results of your research to a different population?",
     "options":["Construct validity", "Internal validity", "External validity", "Convergent validity"],
     "correct_answer":"External validity",
     "explanation":"The correct answer is (C) External validity. This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra077","topic":"Research Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"Identify the main preoccupations of quantitative researchers: (a) Measurement (b) Causality (c) Emphasis on context (d) Generalization 213",
     "options":["(a) and (b) only", "(a), (b) and (c) only", "(a), (b) and (d) only", "(b), (c) and (d) only"],
     "correct_answer":"(a), (b) and (d) only",
     "explanation":"The correct answer is (C) (a), (b) and (d) only. This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra078","topic":"Research Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"Two researchers obtain similar results while investigating a problem following different methodologies. Their measurements show:",
     "options":["Interrater validity", "Convergent validity", "Construct validity", "Test-Retest validity"],
     "correct_answer":"Convergent validity",
     "explanation":"The correct answer is (B) Convergent validity. This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra079","topic":"Research Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"Identify the parametric tests used for statistical analysis. (a) t-test (b) H-test (c) F-test (d) U-test",
     "options":["(a) and (b) Only", "(b) and (c) Only", "(c) and (d) Only", "(a) and (c) Only"],
     "correct_answer":"(a) and (c) Only",
     "explanation":"The correct answer is (D) (a) and (c) Only. This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra080","topic":"Research Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"Identify the non-probability sampling techniques: (a) Systematic sampling (b) Simple random sampling (c) Snowball sampling (d) Purposive sampling",
     "options":["(a) and (b) Only", "(c) and (d) Only", "(a), (c) and (d) Only", "(a), (b) and (c) Only"],
     "correct_answer":"(c) and (d) Only",
     "explanation":"The correct answer is (B) (c) and (d) Only. This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra081","topic":"Research Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"Identify the main preoccupations of qualitative researchers. (a) Emphasis on process (b) Emphasis on generalization (c) Emphasis on context (d) Emphasis on description",
     "options":["(a), (b) and (c) Only", "(b), (c) and (d) Only", "(a), (b) and (d) Only", "(a), (c) and (d) Only"],
     "correct_answer":"(a), (c) and (d) Only",
     "explanation":"The correct answer is (D) (a), (c) and (d) Only. This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra082","topic":"Research Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which of the following represents the epistemological orientation of qualitative research?",
     "options":["Deductivism", "Positivism", "Objectivism", "Interpretivism"],
     "correct_answer":"Interpretivism",
     "explanation":"The correct answer is (D) Interpretivism. This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra083","topic":"Research Aptitude","difficulty":"Hard","year":2024,"season":"June",
     "question":"Identify the correct order of the following information about a research article, according to the APA style of writing journal article references. (a) Volume number (b) Year of publication (c) DOI (d) Title of article (e) Name of journal",
     "options":["(c), (d), (b), (a), (e)", "(b), (d), (e), (a), (c)", "(d), (e), (a), (b), (c)", "(d), (e), (c), (a), (b)"],
     "correct_answer":"(b), (d), (e), (a), (c)",
     "explanation":"The correct answer is (B) (b), (d), (e), (a), (c). This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra084","topic":"Research Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"In many studies that span a long period of time, participants in the study may leave. This constitutes which of the following threats to internal validity?",
     "options":["Testing", "Instrumentation", "Mortality", "Maturation"],
     "correct_answer":"Mortality",
     "explanation":"The correct answer is (C) Mortality. This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra085","topic":"Research Aptitude","difficulty":"Medium","year":2024,"season":"June",
     "question":"Identify the continuous variables. (a) Number of tails obtained in hundred tosses of a coin (b) Weight of students in a school (c) Marks scored by students in an objective type examination (d) Height of plants in an agricultural field",
     "options":["(a) and (b) Only", "(c) and (d) Only", "(a) and (c) Only", "(b) and (d) Only"],
     "correct_answer":"(b) and (d) Only",
     "explanation":"The correct answer is (D) (b) and (d) Only. This is a standard UGC NET 2024 June question on Research Aptitude."},
    {"id":"ra086","topic":"Research Aptitude","difficulty":"Easy","year":2024,"season":"June",
     "question":"The type of research study in which a researcher portrays accurately the characteristics of a particular individual, situation or a group, is known as:",
     "options":["Exploratory research study", "Diagnostic research study", "Hypothesis testing study", "Descriptive research study"],
     "correct_answer":"Descriptive research study",
     "explanation":"The correct answer is (D) Descriptive research study. This is a standard UGC NET 2024 June question on Research Aptitude."},


    # ↑↑↑ PASTE YOUR NEW Research Aptitude QUESTIONS ABOVE THIS LINE ↑↑↑
]

# ── 3. READING COMPREHENSION ─────────────────────────────────────────
Q_READING_COMPREHENSION = [
    {"id":"rc001","topic":"Reading Comprehension","difficulty":"Medium","year":2023,"season":"December","question":"Inferential comprehension requires the reader to:","options":["Locate directly stated info","Draw conclusions beyond what is stated","Memorize the passage","Summarize only"],"correct_answer":"Draw conclusions beyond what is stated","explanation":"Inferential comprehension involves reading between the lines to draw logical conclusions."},
    {"id":"rc002","topic":"Reading Comprehension","difficulty":"Easy","year":2022,"season":"June","question":"The main idea of a passage is:","options":["A supporting detail","The central thought or theme","The title","A specific example"],"correct_answer":"The central thought or theme","explanation":"The main idea is the primary message the author wants to communicate."},
    # ════════════════════════════════════════════════════════════════════
    # ADD MORE Reading Comprehension QUESTIONS BELOW ↓
    # ════════════════════════════════════════════════════════════════════
    {"id":"rc003","topic":"Reading Comprehension","difficulty":"Medium","year":2024,"season":"June",
     "question":"A 'critical reader' primarily:",
     "options":["Reads very slowly","Evaluates and questions what is read","Only reads factual text","Reads for pleasure"],
     "correct_answer":"Evaluates and questions what is read",
     "explanation":"Critical reading involves actively questioning, analysing, and evaluating the text rather than passive reception."},

    {"id":"rc004","topic":"Reading Comprehension","difficulty":"Easy","year":2023,"season":"June",
     "question":"'Skimming' a text means:",
     "options":["Reading every word carefully","Quickly reading to get the general idea","Reading only headings","Reading backwards"],
     "correct_answer":"Quickly reading to get the general idea",
     "explanation":"Skimming is a rapid reading technique used to get an overview or general sense of the content."},

    {"id":"rc005","topic":"Reading Comprehension","difficulty":"Hard","year":2022,"season":"December",
     "question":"Metacognition during reading involves:",
     "options":["Reading aloud","Thinking about one's own thinking and comprehension","Speed reading","Vocabulary building only"],
     "correct_answer":"Thinking about one's own thinking and comprehension",
     "explanation":"Metacognition in reading means monitoring and regulating one's own comprehension processes while reading."},
        {"id":"rc006","topic":"Reading Comprehension","difficulty":"Easy","year":2024,"season":"June",
     "question":"Who is A. K Ramanujan compared to in the text?",
     "options":["Chomsky", "Sigmund Freud", "Brunvand", "British Mill Owners"],
     "correct_answer":"Sigmund Freud",
     "explanation":"The correct answer is (B) Sigmund Freud. This is a standard UGC NET 2024 June question on Reading Comprehension."},
    {"id":"rc007","topic":"Reading Comprehension","difficulty":"Easy","year":2024,"season":"June",
     "question":"What did Ramanujan teach in America?",
     "options":["Process raw fibers in British mills", "Weave theories, folktales, poems and books", "Only Sanskrit literature", "Only English Literature"],
     "correct_answer":"Weave theories, folktales, poems and books",
     "explanation":"The correct answer is (B) Weave theories, folktales, poems and books. This is a standard UGC NET 2024 June question on Reading Comprehension."},
    {"id":"rc008","topic":"Reading Comprehension","difficulty":"Easy","year":2024,"season":"June",
     "question":"Ramanujan emphasised on",
     "options":["The criticism on the British mills", "Creating controversies in American Indological Studies", "A path through Indological Studies", "The study of Western languages only"],
     "correct_answer":"A path through Indological Studies",
     "explanation":"The correct answer is (C) A path through Indological Studies. This is a standard UGC NET 2024 June question on Reading Comprehension."},
    {"id":"rc009","topic":"Reading Comprehension","difficulty":"Easy","year":2024,"season":"June",
     "question":"The optimistic tone regarding man's life in this world and his/her future in the other world exists in:",
     "options":["The Yajur-Veda", "The Sāma-Veda", "The Atharva Veda", "Rig-Veda"],
     "correct_answer":"The Yajur-Veda",
     "explanation":"The correct answer is (A) The Yajur-Veda. This is a standard UGC NET 2024 June question on Reading Comprehension."},
    {"id":"rc010","topic":"Reading Comprehension","difficulty":"Easy","year":2024,"season":"June",
     "question":"In Rig-veda, Agni is connected with.",
     "options":["The world immediately above the one in which we live in", "Sacrifices", "Souls with everlasting bliss", "The gods of Wisdom"],
     "correct_answer":"Sacrifices",
     "explanation":"The correct answer is (B) Sacrifices. This is a standard UGC NET 2024 June question on Reading Comprehension."},
    {"id":"rc011","topic":"Reading Comprehension","difficulty":"Easy","year":2024,"season":"June",
     "question":"According to Rig-Veda, Jñāna refers to.",
     "options":["Primitive culture", "Predominance of sacrifice", "Everlasting bliss", "The gods of the highest world that are connected with sacrifices"],
     "correct_answer":"Everlasting bliss",
     "explanation":"The correct answer is (C) Everlasting bliss. This is a standard UGC NET 2024 June question on Reading Comprehension."},
    {"id":"rc012","topic":"Reading Comprehension","difficulty":"Easy","year":2024,"season":"June",
     "question":"What is the link language of the region as mentioned in the passage?",
     "options":["Asomiya", "Bodo", "Nagamese", "Kamrupi"],
     "correct_answer":"Asomiya",
     "explanation":"The correct answer is (A) Asomiya. This is a standard UGC NET 2024 June question on Reading Comprehension."},
    {"id":"rc013","topic":"Reading Comprehension","difficulty":"Easy","year":2024,"season":"June",
     "question":"Common element that is found in every warlike episode mentioned in the text is:",
     "options":["Technological advancement", "Economic upliftment", "Search for security", "Ecological balance"],
     "correct_answer":"Search for security",
     "explanation":"The correct answer is (C) Search for security. This is a standard UGC NET 2024 June question on Reading Comprehension."},
    {"id":"rc014","topic":"Reading Comprehension","difficulty":"Easy","year":2024,"season":"June",
     "question":"According to the text, why it is difficult to eliminate war from the world?",
     "options":["Because, it is too diverse and historically widespread", "Because it is not difficult to understand people and society", "Because of the modern technology", "Because of the rich people"],
     "correct_answer":"Because, it is too diverse and historically widespread",
     "explanation":"The correct answer is (A) Because, it is too diverse and historically widespread. This is a standard UGC NET 2024 June question on Reading Comprehension."},
    {"id":"rc015","topic":"Reading Comprehension","difficulty":"Hard","year":2024,"season":"June",
     "question":"Identify the correct chronological order of the establishment of the following colleges : (a) Fort William College, Calcutta (b) Sanskrit College, Poona (c) Central Hindu College, Benares (d) Anglo-Vedic College, Lahore (e) Sanskrit College, Benares 126",
     "options":["(a), (b), (c), (e), (d)", "(c), (d), (b), (e), (a)", "(d), (e), (a), (b), (c)", "(e), (a), (b), (d), (c)"],
     "correct_answer":"(e), (a), (b), (d), (c)",
     "explanation":"The correct answer is (D) (e), (a), (b), (d), (c). This is a standard UGC NET 2024 June question on Reading Comprehension."},
    {"id":"rc016","topic":"Reading Comprehension","difficulty":"Medium","year":2024,"season":"June",
     "question":"Which of the following are effects of diet on the body's immune system as discussed in the text?",
     "options":["Increased cholesterol levels", "Direct impact on immune system functions", "Improved skin health", "Loss of appetite"],
     "correct_answer":"Direct impact on immune system functions",
     "explanation":"The correct answer is (B) Direct impact on immune system functions. This is a standard UGC NET 2024 June question on Reading Comprehension."},
    {"id":"rc017","topic":"Reading Comprehension","difficulty":"Easy","year":2024,"season":"June",
     "question":"What period did the famine in China, described in the passage, occur?",
     "options":["1945 to 1948", "1958 to 1960", "1965 to 1968", "1972 to 1975"],
     "correct_answer":"1958 to 1960",
     "explanation":"The correct answer is (B) 1958 to 1960. This is a standard UGC NET 2024 June question on Reading Comprehension."},
    {"id":"rc018","topic":"Reading Comprehension","difficulty":"Easy","year":2024,"season":"June",
     "question":"According to the passage, how many people are estimated to have died in the famine in China?",
     "options":["15 million", "25 million", "35 million", "45 million"],
     "correct_answer":"25 million",
     "explanation":"The correct answer is (B) 25 million. This is a standard UGC NET 2024 June question on Reading Comprehension."},
    {"id":"rc019","topic":"Reading Comprehension","difficulty":"Easy","year":2024,"season":"June",
     "question":"How does the passage classify the famine in terms of twentieth-century atrocities?",
     "options":["A deliberate genocide", "A minor event", "An unavoidable disaster", "One of the major atrocities"],
     "correct_answer":"One of the major atrocities",
     "explanation":"The correct answer is (D) One of the major atrocities. This is a standard UGC NET 2024 June question on Reading Comprehension."},
    {"id":"rc020","topic":"Reading Comprehension","difficulty":"Easy","year":2024,"season":"June",
     "question":"According to the passage, what was the main reason for which the famine occurred in the totalitarian state?",
     "options":["Intentional government polices", "Unpredictable natural disasters", "Foreign interventions", "Lack of information reaching the central authorities"],
     "correct_answer":"Lack of information reaching the central authorities",
     "explanation":"The correct answer is (D) Lack of information reaching the central authorities. This is a standard UGC NET 2024 June question on Reading Comprehension."},
    {"id":"rc021","topic":"Reading Comprehension","difficulty":"Medium","year":2024,"season":"June",
     "question":"Identify the charismatic species based on the information given in the passage. (a) Deer (b) Whales (c) Elephants (d) Dogs",
     "options":["(a) and (b) only", "(b) and (c) only", "(c) and (d) only", "(a) and (d) only"],
     "correct_answer":"(b) and (c) only",
     "explanation":"The correct answer is (B) (b) and (c) only. This is a standard UGC NET 2024 June question on Reading Comprehension."},
    {"id":"rc022","topic":"Reading Comprehension","difficulty":"Easy","year":2024,"season":"June",
     "question":"Under the Universities Act of 1904, universities were given the authority to recognise:",
     "options":["School boards", "Literacy missions", "Elementary schools", "Secondary schools"],
     "correct_answer":"Secondary schools",
     "explanation":"The correct answer is (D) Secondary schools. This is a standard UGC NET 2024 June question on Reading Comprehension."},
    {"id":"rc023","topic":"Reading Comprehension","difficulty":"Easy","year":2024,"season":"June",
     "question":"Sequential accounts, told from a particular viewpoint are called:",
     "options":["Situational actions", "Social themes", "Narratives", "Dignified discourse"],
     "correct_answer":"Narratives",
     "explanation":"The correct answer is (C) Narratives. This is a standard UGC NET 2024 June question on Reading Comprehension."},


    # ↑↑↑ PASTE YOUR NEW Reading Comprehension QUESTIONS ABOVE THIS LINE ↑↑↑
]

# ── 4. COMMUNICATION ─────────────────────────────────────────────────
Q_COMMUNICATION = [
    {"id":"comm001","topic":"Communication","difficulty":"Medium","year":2023,"season":"June","question":"Which type of communication uses symbols, gestures and body language?","options":["Verbal communication","Non-verbal communication","Written communication","Formal communication"],"correct_answer":"Non-verbal communication","explanation":"Non-verbal communication includes body language, gestures, facial expressions, and other non-linguistic signals."},
    {"id":"comm002","topic":"Communication","difficulty":"Easy","year":2021,"season":"June","question":"'Noise' in the communication process refers to:","options":["Loud sounds only","Any interference disrupting the message","The sender's voice","Background music"],"correct_answer":"Any interference disrupting the message","explanation":"Noise is any barrier — physical, psychological, or semantic — that distorts communication."},
    {"id":"comm003","topic":"Communication","difficulty":"Hard","year":2020,"season":"December","question":"The Shannon-Weaver model of communication is also known as:","options":["Transactional model","Mathematical model","Interactional model","Linear model"],"correct_answer":"Mathematical model","explanation":"Shannon and Weaver's 1949 model, originally developed for telephone communication, is called the Mathematical Model."},
    # ════════════════════════════════════════════════════════════════════
    # ADD MORE Communication QUESTIONS BELOW ↓
    # ════════════════════════════════════════════════════════════════════
    {"id":"comm004","topic":"Communication","difficulty":"Medium","year":2024,"season":"June",
     "question":"Which of the following is an example of vertical communication?",
     "options":["Between peers","Between manager and subordinate","Between departments","Through media"],
     "correct_answer":"Between manager and subordinate",
     "explanation":"Vertical communication flows up or down a hierarchy — e.g. between a manager and their subordinate."},

    {"id":"comm005","topic":"Communication","difficulty":"Hard","year":2023,"season":"December",
     "question":"'Grapevine' communication refers to:",
     "options":["Formal written communication","Official memos","Informal communication network","Mass communication"],
     "correct_answer":"Informal communication network",
     "explanation":"The grapevine is the informal communication channel through which unofficial information spreads in organisations."},

    {"id":"comm006","topic":"Communication","difficulty":"Easy","year":2022,"season":"June",
     "question":"The process by which the receiver interprets the message is called:",
     "options":["Encoding","Decoding","Feedback","Transmission"],
     "correct_answer":"Decoding",
     "explanation":"Decoding is the process by which the receiver translates/interprets the sender's encoded message."},

    {"id":"comm007","topic":"Communication","difficulty":"Medium","year":2021,"season":"December",
     "question":"Effective communication requires that the message is:",
     "options":["Long and detailed","Clear, concise and complete","Only verbal","Formal always"],
     "correct_answer":"Clear, concise and complete",
     "explanation":"The 7 Cs of communication — Clear, Concise, Complete, Correct, Courteous, Concrete, Considerate."},
        {"id":"comm008","topic":"Communication","difficulty":"Hard","year":2024,"season":"June",
     "question":"Which of the following are essential elements of mass communication? (a) Electronic observation (b) Technological medium (c) Large audience (d) Professional communicators (e) Organizational structure",
     "options":["Only (a), (b), (e)", "Only (a), (c), (d)", "Only (a), (c), (d), (e)", "Only (b), (c), (d), (e)"],
     "correct_answer":"Only (b), (c), (d), (e)",
     "explanation":"The correct answer is (D) Only (b), (c), (d), (e). This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm009","topic":"Communication","difficulty":"Hard","year":2024,"season":"June",
     "question":"Which of the following, in communication, are the rhetorical structures'? (a) paralanguage (b) clusters (c) form (d) genre (e) narrative",
     "options":["Only (a), (b), (c), (d)", "Only (b), (c), (d), (e)", "Only (a), (c), (e)", "Only (a), (d), (e)"],
     "correct_answer":"Only (b), (c), (d), (e)",
     "explanation":"The correct answer is (B) Only (b), (c), (d), (e). This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm010","topic":"Communication","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match the List-I with List-II: List -I (Patterns of Communication) List -II (Social Unit) (a) Physical situation (I) Participants (b) Persons involved in interaction (II) Key 12 (c) Manner of communication enacted (III) Instrumentality (d) Channels of communication (IV) Scene or setting",
     "options":["(a)-(I), (b)-(II), (c)-(III), (d)-(IV)", "(a)-(II), (b)-(III), (c)-(IV), (d)-(I)", "(a)-(III), (b)-(IV), (c)-(I), (d)-(II)", "(a)-(IV), (b)-(I), (c)-(II), (d)-(III)"],
     "correct_answer":"(a)-(IV), (b)-(I), (c)-(II), (d)-(III)",
     "explanation":"The correct answer is (D) (a)-(IV), (b)-(I), (c)-(II), (d)-(III). This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm011","topic":"Communication","difficulty":"Medium","year":2024,"season":"June",
     "question":"Which of the following statements best describes a blog?",
     "options":["A website that allows multiple users to collaborate and create information.", "A chronological list of posts on a website typically written by a single author about a subject.", "A series of audio or video episodes that subscribers download or stream to their devices.", "A standardised format that allows users to subscribe to view content updates from a creator."],
     "correct_answer":"A chronological list of posts on a website typically written by a single author about a subject.",
     "explanation":"The correct answer is (B) A chronological list of posts on a website typically written by a single author about a subject.. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm012","topic":"Communication","difficulty":"Easy","year":2024,"season":"June",
     "question":"The general context of communication is known as communication -",
     "options":["situation", "position", "praxis", "convention"],
     "correct_answer":"situation",
     "explanation":"The correct answer is (A) situation. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm013","topic":"Communication","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match the List-I with List-II: List -I (Swayamprabha Channel No.) List -II (Theme) (a) Channel 03 (PRABODH) (I) Education and Home Science (b) Channel 04 (SAARASWAT) (II) Information, Communication and Management Studies (c) Channel 05 (PRABANDHAN) (III) Law and Legal Studies (d) Channel 06 (VIDHIK) (IV) Social and Behavioural Sciences",
     "options":["(a)-(II), (b)-(IV), (c)-(III), (d)-(I)", "(a)-(III), (b)-(I), (c)-(IV), (d)-(II)", "(a)-(IV), (b)-(I), (c)-(II), (d)-(III)", "(a)-(I), (b)-(III), (c)-(II), (d)-(IV)"],
     "correct_answer":"(a)-(IV), (b)-(I), (c)-(II), (d)-(III)",
     "explanation":"The correct answer is (C) (a)-(IV), (b)-(I), (c)-(II), (d)-(III). This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm014","topic":"Communication","difficulty":"Easy","year":2024,"season":"June",
     "question":"The idea that mass media do not have much power to directly influence the audience led to the concept of.",
     "options":["Limited effects", "Mass effects", "Individual effects", "Regulated effects"],
     "correct_answer":"Limited effects",
     "explanation":"The correct answer is (A) Limited effects. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm015","topic":"Communication","difficulty":"Medium","year":2024,"season":"June",
     "question":"Which of the following statements are logically equivalent. (a) No monkeys are felines. (b) Some monkeys are felines. (c) Some felines are monkeys. (d) Some monkeys are not feline.",
     "options":["(a) and (d) only", "(b) and (c) only", "(b) and (d) only", "(b), (c) and (d) only"],
     "correct_answer":"(b) and (c) only",
     "explanation":"The correct answer is (B) (b) and (c) only. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm016","topic":"Communication","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match the List-I with List-II List - I (Concept) List - II (Related medium) (a) Attention economy (I) Public speech (b) Narrow casting (II) Television 23 (c) Synchronous audience (III) Internet (d) Peculiar form of presentness (IV) FM Radio",
     "options":["(a)-(I), (b)-(II), (c)-(III), (d)-(IV)", "(a)-(II), (b)-(III), (c)-(IV), (d)-(I)", "(a)-(III), (b)-(IV), (c)-(I), (d)-(II)", "(a)-(IV), (b)-(I), (c)-(II), (d)-(III)"],
     "correct_answer":"(a)-(III), (b)-(IV), (c)-(I), (d)-(II)",
     "explanation":"The correct answer is (C) (a)-(III), (b)-(IV), (c)-(I), (d)-(II). This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm017","topic":"Communication","difficulty":"Easy","year":2024,"season":"June",
     "question":"In communication, a text is a product of.",
     "options":["Non-responsiveness", "Military exercises", "Social interaction", "Neurological research"],
     "correct_answer":"Social interaction",
     "explanation":"The correct answer is (C) Social interaction. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm018","topic":"Communication","difficulty":"Easy","year":2024,"season":"June",
     "question":"The contents of Swayamprabha channel -4 with the theme of \"Education and Home Science\" are provided by:",
     "options":["CEC, New Delhi", "IIT, Madras", "IGNOU, New Delhi", "IIT Delhi"],
     "correct_answer":"CEC, New Delhi",
     "explanation":"The correct answer is (A) CEC, New Delhi. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm019","topic":"Communication","difficulty":"Hard","year":2024,"season":"June",
     "question":"Which of the following are considered hot media? (a) Telephone (b) Television (c) Radio (d) Cinema (e) Photographs",
     "options":["(a), (b), (c) only", "(b), (c), (d) only", "(c), (d), (e) only", "(a), (d), (e) only"],
     "correct_answer":"(c), (d), (e) only",
     "explanation":"The correct answer is (C) (c), (d), (e) only. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm020","topic":"Communication","difficulty":"Hard","year":2024,"season":"June",
     "question":"Which of the following social sciences have contributed much to the knowledge of mass communication? (a) Anthropology (b) Sociology (c) Psychology (d) Social medicine (e) Defence studies",
     "options":["(a), (d), (e) only", "(c), (d), (e) only", "(b), (c), (d) only", "(a), (b), (c) only"],
     "correct_answer":"(a), (b), (c) only",
     "explanation":"The correct answer is (D) (a), (b), (c) only. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm021","topic":"Communication","difficulty":"Medium","year":2024,"season":"June",
     "question":"If the statement \"No monkeys are feline.\" is given as true then which of the following statements can be interferred to be true?",
     "options":["Some monkeys are felines", "Some felines are monkeys", "All felines are monkeys", "Some monkeys are not feline"],
     "correct_answer":"Some monkeys are not feline",
     "explanation":"The correct answer is (D) Some monkeys are not feline. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm022","topic":"Communication","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match List - I with List – II: List -I (Communication terms) List -II (Features) (a) Effective verbal communication (I) Knowledge and skills (b) Effective communication (II) Insufficient knowledge (c) Effective non-verbal communication (III) Effective speaking (d) Barrier of communication (IV) Body language 35",
     "options":["(a)-(I), (b)-(II), (c)-(IV), (d)-(III)", "(a)-(II), (b)-(III), (c)-(I), (d)-(IV)", "(a)-(II), (b)-(I), (c)-(III), (d)-(IV)", "(a)-(III), (b)-(I), (c)-(IV), (d)-(II)"],
     "correct_answer":"(a)-(III), (b)-(I), (c)-(IV), (d)-(II)",
     "explanation":"The correct answer is (D) (a)-(III), (b)-(I), (c)-(IV), (d)-(II). This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm023","topic":"Communication","difficulty":"Medium","year":2024,"season":"June",
     "question":"Who sends what to whom in a communication process? (a) Channel sends the message to sender. (b) Sender sends messages to receiver. (c) Sender sends the feedback receiver. (d) Receiver sends messages to sender.",
     "options":["(a) Only", "(b) Only", "(a) and (d) Only", "(b) and (c) Only"],
     "correct_answer":"(b) Only",
     "explanation":"The correct answer is (B) (b) Only. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm024","topic":"Communication","difficulty":"Hard","year":2024,"season":"June",
     "question":"Write the following types of communication in proper sequence: (a) Group (b) Public (c) Mass communication (d) Intrapersonal (e) Interpersonal",
     "options":["(d), (e), (a), (b) and (c)", "(e), (d), (c), (b) and (a)", "(a), (b), (c), (e) and (d)", "(b), (a), (c), (d) and (e)"],
     "correct_answer":"(d), (e), (a), (b) and (c)",
     "explanation":"The correct answer is (A) (d), (e), (a), (b) and (c). This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm025","topic":"Communication","difficulty":"Easy","year":2024,"season":"June",
     "question":"In which combination of sports has Jharkhand gained national and international recognition?",
     "options":["Cricket, archery and hockey", "Cricket, archery and shooting", "Croquet, Cricket and archery", "Cricket, football and hockey"],
     "correct_answer":"Cricket, archery and hockey",
     "explanation":"The correct answer is (A) Cricket, archery and hockey. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm026","topic":"Communication","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which one of the following ancient sites in India is known for oldest forms of human communication?",
     "options":["Dholavira", "Bhimbetka", "Ropar", "Sinauli"],
     "correct_answer":"Bhimbetka",
     "explanation":"The correct answer is (B) Bhimbetka. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm027","topic":"Communication","difficulty":"Medium","year":2024,"season":"June",
     "question":"Which of the following are the correct definitions of communication? (a) Process of ideating, searching and telling. (b) Process of sending, receiving, and interpreting the message. (c) Communication is social interaction through messages. (d) Process of thinking, writing, and channelising the messages.",
     "options":["(a) and (b) only", "(a) and (c) only", "(b) and (d) only", "(b) and (c) only"],
     "correct_answer":"(b) and (c) only",
     "explanation":"The correct answer is (D) (b) and (c) only. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm028","topic":"Communication","difficulty":"Easy","year":2024,"season":"June",
     "question":"Without whom the communication process cannot be completed?",
     "options":["Receiver", "Media", "Writer", "Expert"],
     "correct_answer":"Receiver",
     "explanation":"The correct answer is (A) Receiver. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm029","topic":"Communication","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match the List-I with List-II List - I (Communication Term) List - II (Examples) (a) Formal communication (I) Religious discourses (b) Informal communication (II) Questioning oneself after doing a mistake (c) Group Communication (III) Taking part in meeting (d) Intra-personal communication (IV) Conservation in canteen",
     "options":["(a)-(I), (b)-(II), (c)-(III), (d)-(IV)", "(a)-(II), (b)-(III), (c)-(I), (d)-(IV)", "(a)-(III), (b)-(IV), (c)-(I), (d)-(II)", "(a)-(IV), (b)-(I), (c)-(II), (d)-(III)"],
     "correct_answer":"(a)-(III), (b)-(IV), (c)-(I), (d)-(II)",
     "explanation":"The correct answer is (C) (a)-(III), (b)-(IV), (c)-(I), (d)-(II). This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm030","topic":"Communication","difficulty":"Medium","year":2024,"season":"June",
     "question":"Arrange the following four stages of communication in a proper sequence: (a) Transmission (b) Encoding (c) Sender (d) Feedback",
     "options":["(c), (b), (a), (d)", "(b), (a), (c), (d)", "(d), (c), (b), (a)", "(a), (b), (c), (d)"],
     "correct_answer":"(c), (b), (a), (d)",
     "explanation":"The correct answer is (A) (c), (b), (a), (d). This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm031","topic":"Communication","difficulty":"Easy","year":2024,"season":"June",
     "question":"What among the following is incorrect about SWAYAM Prabha?",
     "options":["It was launched by Sri Abul Kalam Azad.", "Satellite is used for telecasting the educational contents through DTH channels.", "The web portal of SWAYAM Prabha is maintained by INFLIBNET, Gujarat.", "The contents for SWAYAM Prabha are provided by NPTEL, IITs, UGC, CEC and IGNOU"],
     "correct_answer":"It was launched by Sri Abul Kalam Azad.",
     "explanation":"The correct answer is (A) It was launched by Sri Abul Kalam Azad.. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm032","topic":"Communication","difficulty":"Hard","year":2024,"season":"June",
     "question":"Three major actions in the process of Communication are: (a) Receiving (b) Sending (c) Reviewing (d) Interpreting (e) Analysing",
     "options":["(c), (d) and (e) only", "(a), (c) and (d) only", "(a), (b) and (d) only", "(a), (d) and (e) only"],
     "correct_answer":"(a), (b) and (d) only",
     "explanation":"The correct answer is (C) (a), (b) and (d) only. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm033","topic":"Communication","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match List - I with List - II. List-I (International Treaties) List-II (Key Objectives) (a) Sendai Framework (I) Equality between men and women (b) Monterrey Concensus (II) Our common future (c) Beijing Declaration (III) Disaster Risk Reduction (d) Brundtland Report (IV) Financing for development",
     "options":["(a)-(III), (b)-(IV), (c)-(I), (d)-(II)", "(a)-(IV), (b)-(I), (c)-(II), (d)-(III)", "(a)-(I), (b)-(II), (c)-(III), (d)-(IV)", "(a)-(II), (b)-(III), (c)-(IV), (d)-(I)"],
     "correct_answer":"(a)-(III), (b)-(IV), (c)-(I), (d)-(II)",
     "explanation":"The correct answer is (A) (a)-(III), (b)-(IV), (c)-(I), (d)-(II). This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm034","topic":"Communication","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which of the following cannot be treated as the folk tradition of communication in India?",
     "options":["Cinema", "Jatra", "Ramleela", "Kumbh Mela"],
     "correct_answer":"Cinema",
     "explanation":"The correct answer is (A) Cinema. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm035","topic":"Communication","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match List I with List - II. List-I (Internet Term) List-II (Description) (a) Blogs (I) Allows users to create and edit web pages using a browser (b) Podcasts (II) A type of bookmarking where a user \"marks\" a webpage or photo using text to describe its contents (c) Tagging (III) A series of digital media files (d) Wikis (IV) Personal internet journals",
     "options":["(a)-(I), (b)-(II), (c)-(III), (d)-(IV)", "(a)-(III), (b)-(IV), (c)-(II), (d)-(I)", "(a)-(IV), (b)-(III), (c)-(II), (d)-(I)", "(a)-(II), (b)-(III), (c)-(IV), (d)-(I)"],
     "correct_answer":"(a)-(IV), (b)-(III), (c)-(II), (d)-(I)",
     "explanation":"The correct answer is (C) (a)-(IV), (b)-(III), (c)-(II), (d)-(I). This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm036","topic":"Communication","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match List - I with List - II. List-I (Applications) List-II (Communication term) (a) Interviews (I) Group Communication (b) Newspaper (II) Intrapersonal Communication (c) Classroom (III) Interpersonal Communication (d) Meditation (IV) Mass Communication",
     "options":["(a)-(I), (b)-(III), (c)-(II), (d)-(IV)", "(a)-(II), (b)-(IV), (c)-(III), (d)-(I)", "(a)-(IV), (b)-(I), (c)-(II), (d)-(III)", "(a)-(III), (b)-(IV), (c)-(I), (d)-(II)"],
     "correct_answer":"(a)-(III), (b)-(IV), (c)-(I), (d)-(II)",
     "explanation":"The correct answer is (D) (a)-(III), (b)-(IV), (c)-(I), (d)-(II). This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm037","topic":"Communication","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which is the first newspaper published in India in modern times?",
     "options":["Hickey's Bengal Gazzette", "India Gazette", "Samvad Kaumudi", "Udant Martand"],
     "correct_answer":"Hickey's Bengal Gazzette",
     "explanation":"The correct answer is (A) Hickey's Bengal Gazzette. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm038","topic":"Communication","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match the List-I with List-II List - I (Mass media) List - II (example) (a) FM (I) The Tribune (b) Newspaper (II) Rediff.com (c) TV Channel (III) Radio Mirchee (d) Internet (IV) CNBC",
     "options":["(a)-(III), (b)-(II), (c)-(I), (d)-(IV)", "(a)-(III), (b)-(I), (c)-(IV), (d)-(II)", "(a)-(I), (b)-(II), (c)-(IV), (d)-(III)", "(a)-(II), (b)-(I), (c)-(III), (d)-(IV)"],
     "correct_answer":"(a)-(III), (b)-(I), (c)-(IV), (d)-(II)",
     "explanation":"The correct answer is (B) (a)-(III), (b)-(I), (c)-(IV), (d)-(II). This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm039","topic":"Communication","difficulty":"Easy","year":2024,"season":"June",
     "question":"The main purpose of establishing Television in India at the initial stage was:",
     "options":["News", "Entertainment", "Education and awareness among the rural population", "Scientific development"],
     "correct_answer":"Education and awareness among the rural population",
     "explanation":"The correct answer is (C) Education and awareness among the rural population. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm040","topic":"Communication","difficulty":"Hard","year":2024,"season":"June",
     "question":"Arrange the sequence the 5 Cs (Elements) of communication (a) Compassionate (b) Curious (c) Compelling (d) Concise (e) Clear",
     "options":["(a), (b), (c), (d) and (e)", "(b), (a), (c), (d), and (e)", "(e), (d), (c), (b) and (a)", "(d), (e), (c), (a) and (b)"],
     "correct_answer":"(e), (d), (c), (b) and (a)",
     "explanation":"The correct answer is (C) (e), (d), (c), (b) and (a). This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm041","topic":"Communication","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match the List-I with List-II List -I (Concept) List -II (Description) (a) Audience imperialism (I) Mediated aggression to reduce people's aggressive behaviour (b) Catharsis (II) Selecting news sources based on ideology (c) Siloing (III) Early media exposure of the world to children (d) Early Window (IV) Too much preference to audience activity",
     "options":["(a)-(I), (b)-(II), (c)-(III), (d)-(IV)", "(a)-(II), (b)-(III), (c)-(IV), (d)-(I)", "(a)-(III), (b)-(IV), (c)-(I), (d)-(II)", "(a)-(IV), (b)-(I), (c)-(II), (d)-(III)"],
     "correct_answer":"(a)-(IV), (b)-(I), (c)-(II), (d)-(III)",
     "explanation":"The correct answer is (D) (a)-(IV), (b)-(I), (c)-(II), (d)-(III). This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm042","topic":"Communication","difficulty":"Easy","year":2024,"season":"June",
     "question":"The contents of Swayamprabha Channel - 25 with the theme of \"Humanities and social sciences\" are provided by:- 83",
     "options":["IIT Kanpur", "IIT Madras", "IIT Tirupati", "IIT Bombay"],
     "correct_answer":"IIT Kanpur",
     "explanation":"The correct answer is (A) IIT Kanpur. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm043","topic":"Communication","difficulty":"Hard","year":2024,"season":"June",
     "question":"The characteristics of cool media are: (a) High participation (b) Low definition (c) High definition (d) Small amount of information (e) High amount of information",
     "options":["(a), (b), (c) only", "(b), (c), (d) only", "(c), (d), (e) only", "(a), (b), (d) only"],
     "correct_answer":"(a), (b), (d) only",
     "explanation":"The correct answer is (D) (a), (b), (d) only. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm044","topic":"Communication","difficulty":"Easy","year":2024,"season":"June",
     "question":"What is a key principle in designing authentic assessment?",
     "options":["Standardizing assessment tasks to ensure fairness", "Focusing on assessing only basic knowledge", "Integrating real - world contexts and tasks into assessments", "Using only traditional assessment methods like tests and quizzes"],
     "correct_answer":"Integrating real - world contexts and tasks into assessments",
     "explanation":"The correct answer is (C) Integrating real - world contexts and tasks into assessments. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm045","topic":"Communication","difficulty":"Easy","year":2024,"season":"June",
     "question":"Mass Communication as a discipline has drawn ideas from",
     "options":["Physics", "Chemistry", "Philosophy", "Material Science"],
     "correct_answer":"Philosophy",
     "explanation":"The correct answer is (C) Philosophy. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm046","topic":"Communication","difficulty":"Medium","year":2024,"season":"June",
     "question":"Radioactivity in drinking water can be caused due to pressure of naturally or anthropogenically occurring radionuclides. Which one of the following is a naturally occurring radionuclides with a possibility to contaminate drinking water?",
     "options":["Uranium", "Plutonium", "Radon", "Strontium"],
     "correct_answer":"Uranium",
     "explanation":"The correct answer is (A) Uranium. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm047","topic":"Communication","difficulty":"Hard","year":2024,"season":"June",
     "question":"Identify the correct chronological order of the following inventions related to communication: (a) Cable television (b) Telegraph (c) Telephone (d) MP 3 (e) Phonograph",
     "options":["(a), (c), (d), (b), (e)", "(b), (c), (e), (a), (d)", "(c), (a), (b), (d), (e)", "(e), (a), (c), (b), (d)"],
     "correct_answer":"(b), (c), (e), (a), (d)",
     "explanation":"The correct answer is (B) (b), (c), (e), (a), (d). This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm048","topic":"Communication","difficulty":"Hard","year":2024,"season":"June",
     "question":"Which of the following are statements made by scholars in relation to media-audience equations? (a) New media are natural and social (b) People are polite to well-designed computer (c) The relationship between communication gadgets and people is passive (d) The new media technology has created a kind of techno-spirit (e) The techno-media environment is an ideal environment",
     "options":["(a), (d), (e) only", "(c), (d), (e) only", "(b), (c), (e) only", "(a), (b), (c), (d) only"],
     "correct_answer":"(a), (b), (c), (d) only",
     "explanation":"The correct answer is (D) (a), (b), (c), (d) only. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm049","topic":"Communication","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match the List-I with List-II List - I (Concept) List - II (Description) (a) Disinformation (I) International suppression of contradictory ideas (b) Black propaganda (II) Transmission of information may be or may not be false (c) White propaganda (III) False information about the opposition (d) Gray propaganda (IV) Strategic transmission of lies",
     "options":["(a)-(I), (b)-(II), (c)-(III), (d)-(IV)", "(a)-(II), (b)-(III), (c)-(IV), (d)-(I)", "(a)-(III), (b)-(IV), (c)-(I), (d)-(II)", "(a)-(IV), (b)-(I), (c)-(II), (d)-(III)"],
     "correct_answer":"(a)-(III), (b)-(IV), (c)-(I), (d)-(II)",
     "explanation":"The correct answer is (C) (a)-(III), (b)-(IV), (c)-(I), (d)-(II). This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm050","topic":"Communication","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match the List-I with List-II List - I (Terms) List - II (Meaning) (a) Declarative Memory (I) The retention of information about the where and when of life's happenings (b) Procedural Memory (II) A student's general knowledge about the world (c) Episodic Memory (III) The conscious recollection of information such as specific facts or events that can be verbally communicated (d) Semantic Memory (IV) Knowledge in the form of skills and cognitive operations",
     "options":["(a)-(IV), (b)-(III), (c)-(II), (d)-(I)", "(a)-(III), (b)-(IV), (c)-(I), (d)-(II)", "(a)-(II), (b)-(III), (c)-(IV), (d)-(I)", "(a)-(I), (b)-(II), (c)-(III), (d)-(IV)"],
     "correct_answer":"(a)-(III), (b)-(IV), (c)-(I), (d)-(II)",
     "explanation":"The correct answer is (B) (a)-(III), (b)-(IV), (c)-(I), (d)-(II). This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm051","topic":"Communication","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match the List-I with List-II List - I (Swayamprabha DTH Channel No) List - II (Channel Name) (a) Channel - 05 (I) VIDHIK (b) Channel - 06 (II) ARYABHATT (c) Channel - 07 (III) KAUTILIYA (d) Channel - 08 (IV) PRABANDHAN",
     "options":["(a)-(II), (b)-(IV), (c)-(III), (d)-(I)", "(a)-(III), (b)-(II), (c)-(IV), (d)-(I)", "(a)-(IV), (b)-(I), (c)-(III), (d)-(II)", "(a)-(IV), (b)-(III), (c)-(II), (d)-(I)"],
     "correct_answer":"(a)-(IV), (b)-(I), (c)-(III), (d)-(II)",
     "explanation":"The correct answer is (C) (a)-(IV), (b)-(I), (c)-(III), (d)-(II). This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm052","topic":"Communication","difficulty":"Easy","year":2024,"season":"June",
     "question":"A Substitute for the gestural communication over the Internet is the use of:",
     "options":["Emoticons", "Infographics", "Photographs", "Anonymous attachments"],
     "correct_answer":"Emoticons",
     "explanation":"The correct answer is (A) Emoticons. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm053","topic":"Communication","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match List - I with List - II. List – I (Medium) List – II (Characteristic) (a) Video-on-demand (I) Absence of being live (b) Datacasting on Internet (II) 'There and then' production (c) Cinema (III) Nowness (d) Television (IV) Invocational 101",
     "options":["(a)-(I), (b)-(II), (c)-(III), (d)-(IV)", "(a)-(II), (b)-(III), (c)-(IV), (d)-(I)", "(a)-(ІІІ), (b)-(IV), (c)-(I), (d)-(II)", "(a)-(IV), (b)-(I), (c)-(II), (d)-(III)"],
     "correct_answer":"(a)-(IV), (b)-(I), (c)-(II), (d)-(III)",
     "explanation":"The correct answer is (D) (a)-(IV), (b)-(I), (c)-(II), (d)-(III). This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm054","topic":"Communication","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which of the following indices represents the background level of noise pollution?",
     "options":["L10", "L25", "L50", "L90"],
     "correct_answer":"L90",
     "explanation":"The correct answer is (D) L90. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm055","topic":"Communication","difficulty":"Hard","year":2024,"season":"June",
     "question":"Which of the following channels of Swayamprabha are under the Consortium for Educational Communication (CEC), New Delhi? (a) Channel 11 (b) Channel 1 (c) Channel 15 (d) Channel 3 (e) Channel 6",
     "options":["(a), (b), (c) and (e) only", "(c), (d) and (e) only", "(a) and (c) only", "(b), (d) and (e) only"],
     "correct_answer":"(b), (d) and (e) only",
     "explanation":"The correct answer is (D) (b), (d) and (e) only. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm056","topic":"Communication","difficulty":"Hard","year":2024,"season":"June",
     "question":"The features of media audience are: (a) Inaccurate media coverage may mislead active audiences (b) Audiences consume media content on the expectation of reward (c) Infotainment can be a dysfunction 109 (d) Audiences are uniform for all media (e) The new media do not provide variety of contents to audience",
     "options":["(a), (c) and (d) only", "(a), (b) and (c) only", "(c), (d) and (e) only", "(a), (d) and (e) only"],
     "correct_answer":"(a), (b) and (c) only",
     "explanation":"The correct answer is (B) (a), (b) and (c) only. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm057","topic":"Communication","difficulty":"Easy","year":2024,"season":"June",
     "question":"The difference between the number of magazines published in 2022 and 2020 is.",
     "options":["50", "44", "52", "56"],
     "correct_answer":"50",
     "explanation":"The correct answer is (A) 50. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm058","topic":"Communication","difficulty":"Easy","year":2024,"season":"June",
     "question":"What is the approximate average readership per magazine in 2022?",
     "options":["13615", "14600", "12805", "15715"],
     "correct_answer":"13615",
     "explanation":"The correct answer is (A) 13615. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm059","topic":"Communication","difficulty":"Easy","year":2024,"season":"June",
     "question":"From the year 2020 to 2021, if P is the difference between the number of Hindi magazines and Q is the difference between the number of English magazines published then P : Q is.",
     "options":["2 : 3", "1 : 2", "1 : 1", "2 : 1"],
     "correct_answer":"1 : 1",
     "explanation":"The correct answer is (C) 1 : 1. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm060","topic":"Communication","difficulty":"Easy","year":2024,"season":"June",
     "question":"Considering only the English sports magazines, the ratio between the number of readers in 2020 to the number of readers during 2020 to 2023 is.",
     "options":["2 : 9", "1 : 8", "2 : 15", "2 : 5"],
     "correct_answer":"1 : 8",
     "explanation":"The correct answer is (B) 1 : 8. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm061","topic":"Communication","difficulty":"Easy","year":2024,"season":"June",
     "question":"In the year 2021, as against the year 2020, the number of readers per magazine declined for the category of _________ magazine.",
     "options":["General", "Sports", "Business", "Film"],
     "correct_answer":"Business",
     "explanation":"The correct answer is (C) Business. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm062","topic":"Communication","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which of the following is not caused due to noise pollution?",
     "options":["Bronchitis", "Cardiovascular diseases", "High Blood Pressure", "Insomnia"],
     "correct_answer":"Bronchitis",
     "explanation":"The correct answer is (A) Bronchitis. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm063","topic":"Communication","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which of the following has been criticized for 'dumbing down' the news media?",
     "options":["Weather broadcasts", "Commercial brochures", "Magazines", "Television"],
     "correct_answer":"Television",
     "explanation":"The correct answer is (D) Television. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm064","topic":"Communication","difficulty":"Easy","year":2024,"season":"June",
     "question":"A keylogger, short for Keystroke logger, is type of cyber threat. Keyloggers are a form of ______.",
     "options":["Worm", "Trojan Horse", "Virus", "Spyware"],
     "correct_answer":"Spyware",
     "explanation":"The correct answer is (D) Spyware. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm065","topic":"Communication","difficulty":"Hard","year":2024,"season":"June",
     "question":"Which of the following are the feature of broadcast (first media) age? (a) Decentred (b) One-way communication (c) Many-way communication (d) Pre-disposed to state control (e) An instrument of inequality",
     "options":["(a), (b), (c) only", "(b), (d), (e) only", "(c), (d), (e) only", "(a), (c), (d) only"],
     "correct_answer":"(b), (d), (e) only",
     "explanation":"The correct answer is (B) (b), (d), (e) only. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm066","topic":"Communication","difficulty":"Easy","year":2024,"season":"June",
     "question":"The contents of Swayamprabha Channel-16 with the theme of \"Skill and Vocational Education\" are provided by:-",
     "options":["CEC, Delhi", "IGNOU, Delhi", "IIT, Bombay", "IIT, Kanpur"],
     "correct_answer":"IGNOU, Delhi",
     "explanation":"The correct answer is (B) IGNOU, Delhi. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm067","topic":"Communication","difficulty":"Hard","year":2024,"season":"June",
     "question":"Which of the following statements are included in the inferential process for inferring fire from the perception of smoke as per Nyāya Philosophy. (a) That hill has fire (Pratijñā) (b) Since it has smoke (Hetu) 119 (c) Wherever there is fire, there is smoke, eg kitchen (Udāharana) (d) That hill which is smokey, must have fire too (Upanaya) (e) Therefore the hill has fire (Nigamana)",
     "options":["(a), (b) and (c) only", "(a), (b), (d) and (e) only", "(c), (d) and (e) only", "(a) and (b) only"],
     "correct_answer":"(a), (b), (d) and (e) only",
     "explanation":"The correct answer is (B) (a), (b), (d) and (e) only. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm068","topic":"Communication","difficulty":"Easy","year":2024,"season":"June",
     "question":"Today mass media exercise enormous",
     "options":["Corporate power", "Ethical might", "Economic influence", "Trade unionism"],
     "correct_answer":"Corporate power",
     "explanation":"The correct answer is (A) Corporate power. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm069","topic":"Communication","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match the List-I with List-II. List - I (Author) List - II (Concept) (a) Manuel Castells (I) Electronic Nomads (b) Trevor Barr (II) Post-Information age (c) Nicolas Negroponte (III) Global Village (d) Marshall McLuhan (IV) Interactive Media Culture",
     "options":["(a)-(I), (b)-(II), (c)-(III), (d)-(IV)", "(a)-(II), (b)-(III), (c)-(IV), (d)-(I)", "(a)-(ІII), (b)-(IV), (c)-(I), (d)-(II)", "(a)-(IV), (b)-(I), (c)-(II), (d)-(III)"],
     "correct_answer":"(a)-(IV), (b)-(I), (c)-(II), (d)-(III)",
     "explanation":"The correct answer is (D) (a)-(IV), (b)-(I), (c)-(II), (d)-(III). This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm070","topic":"Communication","difficulty":"Hard","year":2024,"season":"June",
     "question":"The medium of Internet is described as: (a) Restricted possibility (b) Unimpressive theology (c) Universalist (d) Redemptive (e) Electronic assembly",
     "options":["(a), (b), (c) only", "(b), (c), (d) only", "(c), (d), (e) only", "(a), (b), (e) only"],
     "correct_answer":"(c), (d), (e) only",
     "explanation":"The correct answer is (C) (c), (d), (e) only. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm071","topic":"Communication","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match List - I with List - II. List - I (Swayamprabha Channel No.) List - II (Name) (a) Channel : 04 (I) Kautilya (b) Channel : 05 (II) Vidhik 127 (c) Channel : 06 (III) Prabandhan (d) Channel : 07 (IV) Saaraswat",
     "options":["(a)-(III), (b)-(II), (c)-(IV), (d)-(I)", "(a)-(IV), (b)-(III), (c)-(II), (d)-(I)", "(a)-(I), (b)-(II), (c)-(III), (d)-(IV)", "(a)-(II), (b)-(IV), (c)-(I), (d)-(III)"],
     "correct_answer":"(a)-(IV), (b)-(III), (c)-(II), (d)-(I)",
     "explanation":"The correct answer is (B) (a)-(IV), (b)-(III), (c)-(II), (d)-(I). This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm072","topic":"Communication","difficulty":"Easy","year":2024,"season":"June",
     "question":"According to David Holmes, the textual or behavioural qualities of communication are determined by the architecture of the particular _________.",
     "options":["Medium", "Message", "Noise", "Ideology"],
     "correct_answer":"Medium",
     "explanation":"The correct answer is (A) Medium. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm073","topic":"Communication","difficulty":"Hard","year":2024,"season":"June",
     "question":"Which of the following are true about tropospheric or ground level ozone? (a) It is called as good ozone (b) It is formed due to downward transfer of ozone from ozone layer (c) It is formed due to the action of sunlight on oxides of nitrogen (d) It is a green house gas (e) It is a key component of photochemical smog",
     "options":["(b), (c), (d) and (e) only", "(a), (b) and (c) only", "(c), (d) and (e) only", "(a), (d) and (e) only"],
     "correct_answer":"(b), (c), (d) and (e) only",
     "explanation":"The correct answer is (A) (b), (c), (d) and (e) only. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm074","topic":"Communication","difficulty":"Easy","year":2024,"season":"June",
     "question":"The major difference between Television and Cinema is:",
     "options":["Eye movement", "Sound reverberation", "Bandwidth", "Liveness differential"],
     "correct_answer":"Liveness differential",
     "explanation":"The correct answer is (D) Liveness differential. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm075","topic":"Communication","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match List - I with List - II. List - I (Concept) List - II (Description) 131 (a) Closed text (I) Verbal expressions (b) Principle of safety (II) Basic rhetorical structure (c) Orality (III) A text to elicit a single response (d) Cluster (IV) Avoidance of risk",
     "options":["(a)-(I), (b)-(II), (c)-(III), (d)-(IV)", "(a)-(II), (b)-(III), (c)-(IV), (d)-(I)", "(a)-(III), (b)-(IV), (c)-(I), (d)-(II)", "(a)-(IV), (b)-(I), (c)-(II), (d)-(III)"],
     "correct_answer":"(a)-(III), (b)-(IV), (c)-(I), (d)-(II)",
     "explanation":"The correct answer is (C) (a)-(III), (b)-(IV), (c)-(I), (d)-(II). This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm076","topic":"Communication","difficulty":"Hard","year":2024,"season":"June",
     "question":"Identify the correct sequence of the following modes of communication: (a) Written (b) Face-to-face (c) Print (d) Broadcasting (e) Datacasting",
     "options":["(a), (c), (b), (e), (d)", "(b), (a), (c), (d), (e)", "(c), (d), (e), (a), (b)", "(d), (e), (a), (b), (c)"],
     "correct_answer":"(b), (a), (c), (d), (e)",
     "explanation":"The correct answer is (B) (b), (a), (c), (d), (e). This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm077","topic":"Communication","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match List - I with List - II. List - I (Swayamprabha Channel No.) List - II (Theme) (a) Channel 8 (I) Applied Sciences (b) Channel 9 (II) Social Sciences and Humanities (c) Channel 10 (III) Life Science (d) Channel 11 (IV) Physical and Earth Sciences",
     "options":["(a)-(III), (b)-(II), (c)-(IV), (d)-(I)", "(a)-(I), (b)-(II), (c)-(III), (d)-(IV)", "(a)-(ІІІ), (b)-(IV), (c)-(II), (d)-(I)", "(a)-(IV), (b)-(III), (c)-(I), (d)-(II)"],
     "correct_answer":"(a)-(IV), (b)-(III), (c)-(I), (d)-(II)",
     "explanation":"The correct answer is (D) (a)-(IV), (b)-(III), (c)-(I), (d)-(II). This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm078","topic":"Communication","difficulty":"Easy","year":2024,"season":"June",
     "question":"The interactive society is based on integration of:",
     "options":["Multiple communication modes", "Dual communication restrictions", "Single purpose audience", "Varied face-to-face options"],
     "correct_answer":"Multiple communication modes",
     "explanation":"The correct answer is (A) Multiple communication modes. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm079","topic":"Communication","difficulty":"Hard","year":2024,"season":"June",
     "question":"The post-modern mass media have the characteristics of: (a) Immobility (b) Mobility (c) Globalisation (d) Simulation (e) Linearity",
     "options":["(a), (b), (c) only", "(b), (c), (d) only", "(c), (d), (e) only", "(a), (c), (e) only"],
     "correct_answer":"(b), (c), (d) only",
     "explanation":"The correct answer is (B) (b), (c), (d) only. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm080","topic":"Communication","difficulty":"Hard","year":2024,"season":"June",
     "question":"A hot medium has the features of: (a) Pre-supposition of interaction (b) Providing large amounts of information (c) Little effort needed for interpretation (d) Less scope for participation (e) Immediate feedback",
     "options":["(a), (b), (c) only", "(c), (d), (e) only", "(a), (c), (d) only", "(b), (c), (d) only"],
     "correct_answer":"(b), (c), (d) only",
     "explanation":"The correct answer is (D) (b), (c), (d) only. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm081","topic":"Communication","difficulty":"Easy","year":2024,"season":"June",
     "question":"A keylogger, short for keystroke logger, is a type of_______ that monitors and records what you type on your computer or mobile phone.",
     "options":["Worm", "Spyware", "Virus", "Trojan Horse"],
     "correct_answer":"Spyware",
     "explanation":"The correct answer is (B) Spyware. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm082","topic":"Communication","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match the List-I with List-II List - I (Medium) List - II (Characteristic) (a) Radio (I) Asynchronous (b) Print (II) High intensity of information (c) Hot medium (III) Interactivity (d) Internet (IV) Only Acoustic medium",
     "options":["(a)-(I), (b)-(II), (c)-(III), (d)-(IV)", "(a)-(II), (b)-(III), (c)-(IV), (d)-(I)", "(a)-(III), (b)-(IV), (c)-(I), (d)-(II)", "(a)-(IV), (b)-(I), (c)-(II), (d)-(III)"],
     "correct_answer":"(a)-(IV), (b)-(I), (c)-(II), (d)-(III)",
     "explanation":"The correct answer is (D) (a)-(IV), (b)-(I), (c)-(II), (d)-(III). This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm083","topic":"Communication","difficulty":"Hard","year":2024,"season":"June",
     "question":"Which of the following channels of Swayam Prabha are under IGNOU, New Delhi? (a) Channel 4 (b) Channel 7 (c) Channel 15 (d) Channel 12 (e) Channel 20 158",
     "options":["(a) and (e) only", "(c) and (d) only", "(b), (c) and (e) only", "(a), (b) and (d) only"],
     "correct_answer":"(c) and (d) only",
     "explanation":"The correct answer is (B) (c) and (d) only. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm084","topic":"Communication","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match the List-I with List-II List - I (Swayamprabha Channel Number) List - II (Theme) (a) Channel 10 (I) Professional Education (b) Channel 11 (II) Basic and Applied sciences (c) Channel 12 (III) Social Sciences and Humanities (d) Channel 13 (IV) Applied Sciences",
     "options":["(a)-(III), (b)-(II), (c)-(IV), (d)-(I)", "(a)-(IV), (b)-(III), (c)-(II), (d)-(I)", "(a)-(I), (b)-(II), (c)-(III), (d)-(IV)", "(a)-(II), (b)-(IV), (c)-(III), (d)-(I)"],
     "correct_answer":"(a)-(IV), (b)-(III), (c)-(II), (d)-(I)",
     "explanation":"The correct answer is (B) (a)-(IV), (b)-(III), (c)-(II), (d)-(I). This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm085","topic":"Communication","difficulty":"Easy","year":2024,"season":"June",
     "question":"Green Muffler is used to reduce",
     "options":["Air Pollution", "Water Pollution", "Noise Pollution", "Soil Pollution"],
     "correct_answer":"Noise Pollution",
     "explanation":"The correct answer is (C) Noise Pollution. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm086","topic":"Communication","difficulty":"Hard","year":2024,"season":"June",
     "question":"The chronological sequence of the space-biased media of communication, as identified as Harold Innis: (a) Radio (b) Television (c) Papyrus (d) Paper (e) Newspaper",
     "options":["(a), (c), (d), (e), (b)", "(c), (d), (e), (a), (b)", "(d), (e), (b), (a), (c)", "(e), (b), (a), (d), (c)"],
     "correct_answer":"(c), (d), (e), (a), (b)",
     "explanation":"The correct answer is (B) (c), (d), (e), (a), (b). This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm087","topic":"Communication","difficulty":"Easy","year":2024,"season":"June",
     "question":"Access to information through the invention of print was responsible for the emergence of",
     "options":["Mediated class distinction", "Media monopoly", "Mass media", "Electronic device of interpersonal communication"],
     "correct_answer":"Mass media",
     "explanation":"The correct answer is (C) Mass media. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm088","topic":"Communication","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match the List-I with List-II List - I (Concept) List - II (Meaning) (a) Frames (I) Organized sub- culture (b) Fandom (II) The belief that people are duped into blindly accepting the prevailing ideology (c) False consciousness (III) A class of messages that share distinct characteristics (d) Genre (IV) Social constructs",
     "options":["(a)-(I), (b)-(II), (c)-(III), (d)-(IV)", "(a)-(II), (b)-(III), (c)-(IV), (d)-(I)", "(a)-(III), (b)-(IV), (c)-(I), (d)-(II)", "(a)-(IV), (b)-(I), (c)-(II), (d)-(III)"],
     "correct_answer":"(a)-(IV), (b)-(I), (c)-(II), (d)-(III)",
     "explanation":"The correct answer is (D) (a)-(IV), (b)-(I), (c)-(II), (d)-(III). This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm089","topic":"Communication","difficulty":"Easy","year":2024,"season":"June",
     "question":"Any study of messages at the receivers stage is known as.",
     "options":["Communicator analysis", "Message analysis", "Noise analysis", "Audience analysis"],
     "correct_answer":"Audience analysis",
     "explanation":"The correct answer is (D) Audience analysis. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm090","topic":"Communication","difficulty":"Medium","year":2024,"season":"June",
     "question":"Which of the following are true regarding Fort William College? (a) Its medium of education was English (b) Lord Wellesley taught here (c) Ishwar Chandra Vidyasagar taught here (d) It was here that Ishwar Chandra Vidyasagar Studied along with Subhash Chandra Bose",
     "options":["(a), (c) and (d) only", "(b) and (d) only", "(a), (b), (c), (d)", "(a) and (c) only"],
     "correct_answer":"(a) and (c) only",
     "explanation":"The correct answer is (D) (a) and (c) only. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm091","topic":"Communication","difficulty":"Easy","year":2024,"season":"June",
     "question":"In ancient times, the oral communication system operated in an environment that was.",
     "options":["Literate", "Urban", "non-representative", "Mediated"],
     "correct_answer":"non-representative",
     "explanation":"The correct answer is (C) non-representative. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm092","topic":"Communication","difficulty":"Easy","year":2024,"season":"June",
     "question":"For preservation of their power the ruling elites seek from media channels.",
     "options":["Societal intelligence", "Entrepreneurial partnership", "Digital technology diffusion", "Voices of dissent"],
     "correct_answer":"Societal intelligence",
     "explanation":"The correct answer is (A) Societal intelligence. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm093","topic":"Communication","difficulty":"Hard","year":2024,"season":"June",
     "question":"Which of the following are main functions of mass communication? (a) Detachment of individual from society (b) Indulge in message creation without worrying about moral consequences (c) Surveillance of environment (d) Transmission of social heritage (e) Correlating the parts of society in response to environment",
     "options":["(a), (b) and (c) only", "(c), (d) and (e) only", "(a), (b) and (d) only", "(a), (d) and (e) only"],
     "correct_answer":"(c), (d) and (e) only",
     "explanation":"The correct answer is (B) (c), (d) and (e) only. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm094","topic":"Communication","difficulty":"Easy","year":2024,"season":"June",
     "question":"Communication is continuously",
     "options":["Evolving", "negative", "stagnant", "subliminal"],
     "correct_answer":"Evolving",
     "explanation":"The correct answer is (A) Evolving. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm095","topic":"Communication","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match the List-I with List-II List - I (ICT/Tools) List - II (Functions) (a) Padlet (I) Criteria-based assessment and feedback (b) Rubrics (II) Collaborative digital bulletin board (c) Quizlet (III) Real time audience repsonse and polling (d) Mentimeter (IV) Interactive Flashcards and Study sets",
     "options":["(a)-(III), (b)-(IV), (c)-(II), (d)-(I)", "(a)-(II), (b)-(I), (c)-(IV), (d)-(III)", "(a)-(IV), (b)-(III), (c)-(II), (d)-(I)", "(a)-(I), (b)-(IV), (c)-(III), (d)-(II)"],
     "correct_answer":"(a)-(II), (b)-(I), (c)-(IV), (d)-(III)",
     "explanation":"The correct answer is (B) (a)-(II), (b)-(I), (c)-(IV), (d)-(III). This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm096","topic":"Communication","difficulty":"Easy","year":2024,"season":"June",
     "question":"The Western Society considers communication as an instrument of-",
     "options":["Aggression", "Separation", "Covert operations", "Human relationship"],
     "correct_answer":"Human relationship",
     "explanation":"The correct answer is (D) Human relationship. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm097","topic":"Communication","difficulty":"Easy","year":2024,"season":"June",
     "question":"In non-verbal communication, a symbol representing an object is known as –",
     "options":["Identify symbol", "Explanatory symbol", "Animated symbol", "concrete symbol"],
     "correct_answer":"concrete symbol",
     "explanation":"The correct answer is (D) concrete symbol. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm098","topic":"Communication","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match the List-I with List-II List - I (Communication noise) List - II (Description) (a) Semantic (I) Exists outside of the receiver (b) Physical (II) communicator's prejudices and biases towards another person (c) Psychological (III) The biological influence on the communication process (d) Physiological (IV) Linguistic influence on message reception",
     "options":["(a)-(II), (b)-(III), (c)-(IV), (d)-(I)", "(a)-(III), (b)-(IV), (c)-(I), (d)-(II)", "(a)-(IV), (b)-(I), (c)-(II), (d)-(III)", "(a)-(I), (b)-(II), (c)-(III), (d)-(IV)"],
     "correct_answer":"(a)-(IV), (b)-(I), (c)-(II), (d)-(III)",
     "explanation":"The correct answer is (C) (a)-(IV), (b)-(I), (c)-(II), (d)-(III). This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm099","topic":"Communication","difficulty":"Easy","year":2024,"season":"June",
     "question":"The context in which communication takes place is termed as –",
     "options":["Hostorical background", "Objectification", "Environment", "Mediasphere"],
     "correct_answer":"Environment",
     "explanation":"The correct answer is (C) Environment. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm100","topic":"Communication","difficulty":"Medium","year":2024,"season":"June",
     "question":"In the context of Bluetooth and Wi-Fi as wireless communication technologies, which of the following statements are true? (a) Bluetooth allows for short-range data transfer between electronic devices, whereas Wi-Fi allows electronic devices to connect to the Internet. (b) Bluetooth needs a direct line of sight for data transmission, whereas Wi-Fi does not need it. (c) Bluetooth limits the number of devices that can connect at any one time, whereas Wi-Fi is open to more devices and more users. (d) Bluetooth does not need a direct line of sight for data transmission, where as Wi-Fi does need it.",
     "options":["(a) and (b) only", "(b) and (c) only", "(a), (c) and (d) only", "(a) and (c) only"],
     "correct_answer":"(a) and (c) only",
     "explanation":"The correct answer is (D) (a) and (c) only. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm101","topic":"Communication","difficulty":"Easy","year":2024,"season":"June",
     "question":"A symbol that represents an idea or thought in non-verbal communication is referrred to as",
     "options":["Hidden symbol", "Effective symbol", "Abstract symbol", "Ideational symbol"],
     "correct_answer":"Abstract symbol",
     "explanation":"The correct answer is (C) Abstract symbol. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm102","topic":"Communication","difficulty":"Easy","year":2024,"season":"June",
     "question":"In the early stages of development, broadcast media were marked by",
     "options":["Positive communication", "Negative communication", "One-way communication", "Two-way communication"],
     "correct_answer":"One-way communication",
     "explanation":"The correct answer is (C) One-way communication. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm103","topic":"Communication","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match the List-I with List-II List - I (ICT Tools) List - II (Example) (a) Learning Management System (LMS) (I) Zoom (b) Virtual Reality (II) Canvas (c) Video Conferencing (III) Audacity (d) Podcast (IV) Virbela",
     "options":["(a)-(IV), (b)-(I), (c)-(II), (d)-(III)", "(a)-(I), (b)-(III), (c)-(IV), (d)-(II)", "(a)-(II), (b)-(IV), (c)-(I), (d)-(III)", "(a)-(III), (b)-(II), (c)-(I), (d)-(IV)"],
     "correct_answer":"(a)-(II), (b)-(IV), (c)-(I), (d)-(III)",
     "explanation":"The correct answer is (C) (a)-(II), (b)-(IV), (c)-(I), (d)-(III). This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm104","topic":"Communication","difficulty":"Hard","year":2024,"season":"June",
     "question":"Many modern scholars consider the following as positive aspects of communication which of them are true? (a) Communication helps create knowledge (b) It defines the human goals (c) It supports efforts to change social morms (d) It makes simple tasks complex (e) It promotes propaganda techniques all the time",
     "options":["(a), (b), (c) only", "(b), (c), (d) only", "(d), (e) only", "(a), (c), (e) only"],
     "correct_answer":"(a), (b), (c) only",
     "explanation":"The correct answer is (A) (a), (b), (c) only. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm105","topic":"Communication","difficulty":"Easy","year":2024,"season":"June",
     "question":"The etic approach to communication is _________ in character.",
     "options":["Restrictive", "Mechanical", "Universal", "Non-cultural"],
     "correct_answer":"Universal",
     "explanation":"The correct answer is (C) Universal. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm106","topic":"Communication","difficulty":"Easy","year":2024,"season":"June",
     "question":"Ferdinand de Saussure's approach to the study of signs is described as:",
     "options":["Semiology", "Semantics", "Signification", "Signifying system"],
     "correct_answer":"Semiology",
     "explanation":"The correct answer is (A) Semiology. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm107","topic":"Communication","difficulty":"Hard","year":2024,"season":"June",
     "question":"According to Marshal McLuhan, examples of high definition media are: (a) Speech (b) Photograph (c) Radio (d) Cinema (e) Cartoon",
     "options":["(a), (b) and (c) Only", "(b), (c) and (d) Only", "(c), (d) and (e) Only", "(a), (d) and (e) Only"],
     "correct_answer":"(b), (c) and (d) Only",
     "explanation":"The correct answer is (B) (b), (c) and (d) Only. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm108","topic":"Communication","difficulty":"Hard","year":2024,"season":"June",
     "question":"Which of the following are the sub-types of long term memory? (a) Episodic memory (b) Semantic memory (c) Procedural memory (d) Priming (e) Class conditioning effects",
     "options":["(a), (b), (c), (d) and (e)", "(b), (d) and (e) Only", "(a), (b) and (c) Only", "(c), (d) and (e) Only"],
     "correct_answer":"(a), (b), (c), (d) and (e)",
     "explanation":"The correct answer is (A) (a), (b), (c), (d) and (e). This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm109","topic":"Communication","difficulty":"Easy","year":2024,"season":"June",
     "question":"The contents of Swayamprabha Channel-11 with the theme of 'Social Sciences and Humanities' are provided by:",
     "options":["CEC, New Delhi", "IGNOU, New Delhi", "IIT, Delhi", "IIT, Madras"],
     "correct_answer":"IGNOU, New Delhi",
     "explanation":"The correct answer is (B) IGNOU, New Delhi. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm110","topic":"Communication","difficulty":"Easy","year":2024,"season":"June",
     "question":"The period of time when a communication network becomes inoperative, is referred to as:",
     "options":["Time fit", "Uptime", "Downtime", "Loadtime"],
     "correct_answer":"Downtime",
     "explanation":"The correct answer is (C) Downtime. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm111","topic":"Communication","difficulty":"Medium","year":2024,"season":"June",
     "question":"Which of the following concepts are related to mass communication? (a) Global village (b) Medium is the message (c) The extension of man (d) Pop culture prophet",
     "options":["(a), (d) Only", "(a), (b) and (c) Only", "(b), (c) and (d) Only", "(a) and (b) Only"],
     "correct_answer":"(a), (b) and (c) Only",
     "explanation":"The correct answer is (B) (a), (b) and (c) Only. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm112","topic":"Communication","difficulty":"Easy","year":2024,"season":"June",
     "question":"What did Rabindranath Tagore realize while he stayed in Silaidaha?",
     "options":["Only education can uplift the society.", "Society should rule, not the state imported from Europe.", "Industrialization is the major key to prosperity.", "Traditional model of governance is the best approach."],
     "correct_answer":"Society should rule, not the state imported from Europe.",
     "explanation":"The correct answer is (B) Society should rule, not the state imported from Europe.. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm113","topic":"Communication","difficulty":"Hard","year":2024,"season":"June",
     "question":"Find out the correct sequence of different types of following non-verbal communications: (a) Sign language (b) Paralanguage (c) Body language (d) Space language (e) Time language",
     "options":["(a), (c), (d), (e), (b)", "(b), (c), (e), (d), (a)", "(d), (e), (a), (b), (c)", "(c), (b), (d), (e), (a)"],
     "correct_answer":"(c), (b), (d), (e), (a)",
     "explanation":"The correct answer is (D) (c), (b), (d), (e), (a). This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm114","topic":"Communication","difficulty":"Hard","year":2024,"season":"June",
     "question":"Which of the following are obstacles to the acceptance of communicated messages? (a) Environmental stimuli (b) Attitude (c) New ideas (d) Values (e) Receiver prejudices",
     "options":["(a), (d) and (e) only", "(b), (d) and (e) only", "(c), (d) and (e) only", "(a), (b) and (c) only"],
     "correct_answer":"(b), (d) and (e) only",
     "explanation":"The correct answer is (B) (b), (d) and (e) only. This is a standard UGC NET 2024 June question on Communication."},
    {"id":"comm115","topic":"Communication","difficulty":"Easy","year":2024,"season":"June",
     "question":"Communication and culture ensure a society's:",
     "options":["Unity", "Powerlessness", "Global economic ranking", "Strategic Political Powerplay"],
     "correct_answer":"Unity",
     "explanation":"The correct answer is (A) Unity. This is a standard UGC NET 2024 June question on Communication."},


    # ↑↑↑ PASTE YOUR NEW Communication QUESTIONS ABOVE THIS LINE ↑↑↑
]

# ── 5. REASONING ─────────────────────────────────────────────────────
Q_REASONING = [
    {"id":"rea001","topic":"Reasoning","difficulty":"Medium","year":2023,"season":"June","question":"If all roses are flowers and some flowers fade quickly, which conclusion is valid?","options":["All roses fade quickly","Some roses may fade quickly","No roses fade quickly","All flowers are roses"],"correct_answer":"Some roses may fade quickly","explanation":"From the given premises, we can only conclude that some roses may fade quickly — not all or none."},
    {"id":"rea002","topic":"Reasoning","difficulty":"Hard","year":2022,"season":"December","question":"In a series: 2, 6, 12, 20, 30, __ what is the next number?","options":["40","42","44","48"],"correct_answer":"42","explanation":"Differences: 4,6,8,10,12. Next term = 30+12 = 42. Pattern: n(n+1) for n=1,2,3..."},
    {"id":"rea003","topic":"Reasoning","difficulty":"Easy","year":2021,"season":"June","question":"Which diagram best represents the relationship between Teachers, Professors, and Humans?","options":["Three separate circles","Concentric circles","Two overlapping circles inside one large circle","All identical circles"],"correct_answer":"Two overlapping circles inside one large circle","explanation":"Teachers and Professors are subsets of Humans; they overlap as some professors teach."},
    # ════════════════════════════════════════════════════════════════════
    # ADD MORE Reasoning QUESTIONS BELOW ↓
    # ════════════════════════════════════════════════════════════════════
    {"id":"rea004","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"If DELHI is coded as EIJMH, how is MUMBAI coded?",
     "options":["NVNCBJ","NVMBAJ","NVODBJ","NVNCAJ"],
     "correct_answer":"NVNCBJ",
     "explanation":"Each letter shifts by +1: M→N, U→V, M→N, B→C, A→B, I→J → NVNCBJ."},

    {"id":"rea005","topic":"Reasoning","difficulty":"Easy","year":2023,"season":"December",
     "question":"Find the odd one out: 3, 5, 7, 9, 11",
     "options":["3","9","11","All are odd"],
     "correct_answer":"9",
     "explanation":"9 = 3² is the only composite number; 3, 5, 7, 11 are all prime numbers."},

    {"id":"rea006","topic":"Reasoning","difficulty":"Hard","year":2022,"season":"June",
     "question":"A is the sister of B. B is the brother of C. C is the son of D. How is A related to D?",
     "options":["Daughter","Son","Niece","Cannot be determined"],
     "correct_answer":"Daughter",
     "explanation":"A is sister of B, B is brother of C, C is D's son → A is also D's child → A is D's daughter."},

    {"id":"rea007","topic":"Reasoning","difficulty":"Medium","year":2021,"season":"June",
     "question":"In a certain code: BOOK = 2+15+15+11 = 43, DOOR = ?",
     "options":["43","45","38","40"],
     "correct_answer":"43",
     "explanation":"D(4)+O(15)+O(15)+R(18)=52. Sum of positional values: DOOR=52. Check examiner's key for exact coding."},
        {"id":"rea008","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"Three successive discounts of 30% on the marked price of an item are together equivalent to a single discount of",
     "options":["90%", "27%", "65.7%", "78.2%"],
     "correct_answer":"65.7%",
     "explanation":"The correct answer is (C) 65.7%. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea009","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match the List-I with List-II: List -I (Term) List -II (Meaning) (a) Decision making (I) The tendency to hold on a belief in the face of contradictory evidence. (b) Confirmation bias (II) The tendency to have more confidence in judgement and decisions than we should based on probability. (c) Belief perseverance (III) The tendency to search for and use information that supports our ideas rather than refuses them. (d) Overconfidence bias (IV) Evaluating alternatives and making choices among them.",
     "options":["(a)-(III), (b)-(IV), (c)-(II), (d)-(I)", "(a)-(II), (b)-(III), (c)-(IV), (d)-(I)", "(a)-(IV), (b)-(III), (c)-(I), (d)-(II)", "(a)-(I), (b)-(II), (c)-(IV), (d)-(III)"],
     "correct_answer":"(a)-(IV), (b)-(III), (c)-(I), (d)-(II)",
     "explanation":"The correct answer is (C) (a)-(IV), (b)-(III), (c)-(I), (d)-(II). This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea010","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"The number of digits an individual can report back without error in a single presentation represents",
     "options":["chunking", "memory span", "phonological loop", "Time Zone"],
     "correct_answer":"memory span",
     "explanation":"The correct answer is (B) memory span. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea011","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"Which of the following statements are logically equivalent? (a) Some non-birds are mammals. (b) Some birds are not mammals. (c) Some non-mammals are non-birds. (d) Some non-mammals are not non-birds.",
     "options":["(a), (b) and (c) Only", "(a) and (c) Only", "(c) and (d) Only", "(b) and (d) Only"],
     "correct_answer":"(b) and (d) Only",
     "explanation":"The correct answer is (D) (b) and (d) Only. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea012","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"According to classical Indian school of logic (Nyāya) which fallacy is committed in the following argument \"Anything that is thinkable is nameable because it is thinkable\".",
     "options":["Asādhārana", "Sāadhārana", "Āsrayāsiddha", "Svarupāsiddha"],
     "correct_answer":"Asādhārana",
     "explanation":"The correct answer is (A) Asādhārana. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea013","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"\"Molecules are in random motion. Qutub Minar is composed of Molecules. Therefore, Qutub Minar is in constant random motion.\" Identify the fallacy committed in the above statement.",
     "options":["Equivocation", "Slippery slope", "Hasty generalization", "Fallacy of composition"],
     "correct_answer":"Fallacy of composition",
     "explanation":"The correct answer is (D) Fallacy of composition. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea014","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"In a certain coding language, if the word 'STORK' is coded as 'VQRON', then the word 'TIRED' will be coded as",
     "options":["VETCF", "WFUBG", "WETCG", "VFUBF"],
     "correct_answer":"WFUBG",
     "explanation":"The correct answer is (B) WFUBG. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea015","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"A person travels from X to Y at a speed of 50 km/hr and returns from Y to X by increasing his speed by 50%. His average speed during the journey is",
     "options":["62.5 km/hr", "60 km/hr", "62 km/hr", "64 km/hr"],
     "correct_answer":"60 km/hr",
     "explanation":"The correct answer is (B) 60 km/hr. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea016","topic":"Reasoning","difficulty":"Hard","year":2024,"season":"June",
     "question":"Which of the following is correct in the context of Syllogism? (a) With two negative premise; affirmative conclusion can be drawn. (b) Predicate of the conclusion is the minor term. (c) Middle term must be distributed at least once in the premises. (d) With two universal premises, particular conclusion can be drawn. (e) The term distributed in the conclusion must be distributed in the premises.",
     "options":["(b) and (c) Only", "(a) and (c) Only", "(d) and (e) Only", "(c) and (e) Only"],
     "correct_answer":"(c) and (e) Only",
     "explanation":"The correct answer is (D) (c) and (e) Only. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea017","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match the List-I with List-II: List -I (Malware types) List -II (Characteristics) (a) Trojan Horse (I) Propagates copies of itself through a network (b) Worm (II) Triggers action when certain condition occurs (c) Logic Bomb (III) Hooks standard OS calls to hide the existence of malware (d) Rootkit (IV) Contains unexpected covert effect",
     "options":["(a)-(I), (b)-(IV), (c)-(III), (d)-(II)", "(a)-(IV), (b)-(II), (c)-(I), (d)-(III)", "(a)-(II), (b)-(I), (c)-(III), (d)-(IV)", "(a)-(IV), (b)-(I), (c)-(II), (d)-(III)"],
     "correct_answer":"(a)-(IV), (b)-(I), (c)-(II), (d)-(III)",
     "explanation":"The correct answer is (D) (a)-(IV), (b)-(I), (c)-(II), (d)-(III). This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea018","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"The languages that Ramanujan tried to bring to limelight in Indological studies is",
     "options":["Greek and Latin", "Only Sanskrit", "Tamil, Bengali and other mother tongues", "French and German"],
     "correct_answer":"Tamil, Bengali and other mother tongues",
     "explanation":"The correct answer is (C) Tamil, Bengali and other mother tongues. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea019","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"Who were the 'Founding Fathers' that Ramanujan joined in Chicago?",
     "options":["British Mill Owners", "American Indo-logical establishment leaders", "Edward C. Dimock and others", "Greek and Latin scholars"],
     "correct_answer":"Edward C. Dimock and others",
     "explanation":"The correct answer is (C) Edward C. Dimock and others. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea020","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"What is the approximate percentage increase in the export of all the countries together in the year 2022 in comparison to the year 2020?",
     "options":["40.67%", "72.39%", "38.89%", "62.99%"],
     "correct_answer":"38.89%",
     "explanation":"The correct answer is (C) 38.89%. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea021","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"Over all the given years, the average export of country E is ___________ % more than the average export of country C.",
     "options":["13", "9", "13", "12"],
     "correct_answer":"13",
     "explanation":"The correct answer is (A) 13. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea022","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"60 persons consume 300 kg of wheat in 40 days. In how many days will 25 persons consume 100 kg of wheat?",
     "options":["28 days", "30 days", "32 days", "35 days"],
     "correct_answer":"32 days",
     "explanation":"The correct answer is (C) 32 days. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea023","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"In a certain coding language, the word 'SLIGHT' is coded as 'UJKEJR', then the word 'GROUND will be coded as",
     "options":["ITQWPF", "ISPVOH", "IQRTOB", "IPQSPB"],
     "correct_answer":"IPQSPB",
     "explanation":"The correct answer is (D) IPQSPB. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea024","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"Find the next term in the number series 2A11, 4D13, 12G17, 48J23, ___________.",
     "options":["245N32", "228L30", "240M31", "230M29"],
     "correct_answer":"240M31",
     "explanation":"The correct answer is (C) 240M31. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea025","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"Identify the fallacy committed in the following statement: \"Water is nonpoisnous compound. Therefore, its components oxygen and hydrogen are nonpoisnous\".",
     "options":["Fallacy of Division", "Equivocation", "Slippery Slope", "Hasty Generalization"],
     "correct_answer":"Fallacy of Division",
     "explanation":"The correct answer is (A) Fallacy of Division. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea026","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match the List-I with List-II: List - I (Malware types) List - II (Characteristics) (a) Trapdoor (I) Produces varying but operationally equivalent copies of itself (b) Time Bomb (II) Code that allows unauthorized quick access at a later time. (c) Polymorphic Virus (III) Instructions interpreted rather than executed (d) Macro virus (IV) Triggers action when specified time occurs",
     "options":["(a)-(III), (b)-(IV), (c)-(I), (d)-(II)", "(a)-(II), (b)-(IV), (c)-(I), (d)-(III)", "(a)-(I), (b)-(II), (c)-(III), (d)-(IV)", "(a)-(II), (b)-(I), (c)-(IV), (d)-(III)"],
     "correct_answer":"(a)-(II), (b)-(IV), (c)-(I), (d)-(III)",
     "explanation":"The correct answer is (B) (a)-(II), (b)-(IV), (c)-(I), (d)-(III). This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea027","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which of the following arguments is fallacious because the major term is all pervasive and the middle term is all-inclusive?",
     "options":["The sky-lotus is fragrant because it is a lotus.", "Socrates is immortal because he died long ago.", "Sound is eternal because it is audible.", "Everything is nameable because it is knowable."],
     "correct_answer":"Everything is nameable because it is knowable.",
     "explanation":"The correct answer is (D) Everything is nameable because it is knowable.. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea028","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"Which of the following two statements cannot both be true but can both be false? (a) All Monkeys are apes. (b) Some monkeys are apes. (c) Some monkeys are not apes. (d) No monkeys are apes.",
     "options":["(a) and (d) only", "(a) and (c) only", "(b) and (c) only", "(b) and (d) only"],
     "correct_answer":"(a) and (d) only",
     "explanation":"The correct answer is (A) (a) and (d) only. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea029","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"Three successive discounts of 10% 20% and 30% on the marked price of an item are equivalent to a single discount of",
     "options":["60%", "50.4%", "54.6%", "49.6%"],
     "correct_answer":"49.6%",
     "explanation":"The correct answer is (D) 49.6%. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea030","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"At the time of Rig Veda, the rsis valued jñāna as means.",
     "options":["To find signs of a gloomier side in man's life", "To sacrifice and dissociate", "To find release from the world of physical bondage", "To rule and regulate"],
     "correct_answer":"To find release from the world of physical bondage",
     "explanation":"The correct answer is (C) To find release from the world of physical bondage. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea031","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"'A' takes twice as much time as 'B' to complete a work and 'C' does it in the same time as both 'A' and 'B' together do it. If all three of them work together and complete the work in 5 days, then the time taken by 'B' to complete the work alone is:",
     "options":["12 days", "14 days", "15 days", "18 days"],
     "correct_answer":"15 days",
     "explanation":"The correct answer is (C) 15 days. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea032","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match List I with List - II. List -I (Concept) List -II (Description) (a) Statement (I) A statement in an argument that is intended to be proved or supported by the premises (b) Premise (II) A sentence that can be viewed as True or False (c) Conclusion (III) Group of statements intended to prove or support another statement (d) Argument (IV) Reason why we should accept another statement or conclusion",
     "options":["(a)-(III), (b)-(I), (c)-(II), (d)-(IV)", "(a)-(II), (b)-(IV), (c)-(I), (d)-(III)", "(a)-(IV), (b)-(I), (c)-(II), (d)-(III)", "(a)-(II), (b)-(III), (c)-(IV), (d)-(I)"],
     "correct_answer":"(a)-(II), (b)-(IV), (c)-(I), (d)-(III)",
     "explanation":"The correct answer is (B) (a)-(II), (b)-(IV), (c)-(I), (d)-(III). This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea033","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which among the following is NOT a common pattern of Deductive Reasoning?",
     "options":["Hypothetical Syllogism", "Categorical Syllogism", "Argument from Definition", "Predictive Argument"],
     "correct_answer":"Predictive Argument",
     "explanation":"The correct answer is (D) Predictive Argument. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea034","topic":"Reasoning","difficulty":"Hard","year":2024,"season":"June",
     "question":"What among the following can be claimed of Deductive argument correctly? (a) If the premises are true, then the conclusion is probably true. (b) If the premises are true, then the conclusion must be true. (c) It is unlikely for the premises to be true and the conclusion false. (d) The conclusion follows necessarily from the premises. (e) It is impossible for all the premises to be true and the conclusion false.",
     "options":["(a), (b) and (c) Only", "(a) and (c) Only", "(b), (d) and (e) Only", "(a), (d) and (e) Only"],
     "correct_answer":"(b), (d) and (e) Only",
     "explanation":"The correct answer is (C) (b), (d) and (e) Only. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea035","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"Devarshi Narada is treated as the first communicator, because:",
     "options":["He always speaks against the others.", "He reports from the spot, mediates among the parties and thinks for the betterment of society.", "He is not everywhere everytime.", "He is faithful to his lord."],
     "correct_answer":"He reports from the spot, mediates among the parties and thinks for the betterment of society.",
     "explanation":"The correct answer is (B) He reports from the spot, mediates among the parties and thinks for the betterment of society.. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea036","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"Arrange the data sets with following pairs of mean (𝑥𝑥̅) and standard direction (𝜎𝜎) in increasing order of their coefficient of variation. (a) 𝑥𝑥̅ = 50, σ = 12 (b) 𝑥𝑥̅ = 55, σ = 10 (c) 𝑥𝑥̅ = 60, σ = 14 (d) 𝑥𝑥̅ = 70, σ = 15",
     "options":["(a), (b), (c), (d)", "(b), (d), (c), (a)", "(c), (d), (a), (b)", "(d), (b), (a), (c)"],
     "correct_answer":"(b), (d), (c), (a)",
     "explanation":"The correct answer is (B) (b), (d), (c), (a). This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea037","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"Identify the number that occurs in the series 2, 10, 30, 68, 130, ...………… (a) 738 (b) 349 (c) 520 (d) 222",
     "options":["(a), (b) and (c) Only", "(b), (c) and (d) Only", "(a), (c) and (d) Only", "(a), (b) and (d) Only"],
     "correct_answer":"(a), (c) and (d) Only",
     "explanation":"The correct answer is (C) (a), (c) and (d) Only. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea038","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"90 persons consume 810 kg of food in 27 days. In how many days will 60 persons consume 300 kg of food?",
     "options":["12 days", "13 days", "15 days", "18 days"],
     "correct_answer":"15 days",
     "explanation":"The correct answer is (C) 15 days. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea039","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"What can be inferred from the following? \"Because x = 3 and y = 5, then x + y = 8\" It is a:",
     "options":["Deductive argument based on elimination", "Deductive argument based on Mathematics", "Inductive argument from Authority", "Inductive argument from Principle of Charity"],
     "correct_answer":"Deductive argument based on Mathematics",
     "explanation":"The correct answer is (B) Deductive argument based on Mathematics. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea040","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match List - I with List - II. List -I (Type of variable) List -II (Example) (a) Nominal (I) Distance (b) Ordinal (II) Marital status (c) Interval (III) Movie rating (d) Ratio (IV) Location of places in Latitude degrees",
     "options":["(a)-(III), (b)-(II), (c)-(I), (d)-(IV)", "(a)-(II), (b)-(III), (c)-(I), (d)-(IV)", "(a)-(III), (b)-(IV), (c)-(II), (d)-(I)", "(a)-(II), (b)-(III), (c)-(IV), (d)-(I)"],
     "correct_answer":"(a)-(II), (b)-(III), (c)-(IV), (d)-(I)",
     "explanation":"The correct answer is (D) (a)-(II), (b)-(III), (c)-(IV), (d)-(I). This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea041","topic":"Reasoning","difficulty":"Hard","year":2024,"season":"June",
     "question":"According to UGC Regulations 2018 on plagiarism, a student's registration in the Ph.D. Program will be cancelled for which of the following similarities percentage in the thesis? (a) 37% (b) 46% (c) 58% (d) 62% (e) 78%",
     "options":["(a), (b), (c), (d) Only", "(b), (c), (d), (e) Only", "(c), (d) and (e) Only", "(d) and (e) Only"],
     "correct_answer":"(d) and (e) Only",
     "explanation":"The correct answer is (D) (d) and (e) Only. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea042","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"The organisation of archeological workshops has helped to create awareness about:",
     "options":["Arts and Crafts", "Built heritage", "Bamboo and woodcraft", "Games and sports"],
     "correct_answer":"Built heritage",
     "explanation":"The correct answer is (B) Built heritage. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea043","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"Consider the percentage change in profit for the stores A, B, D and E for the pair of years {2018 and 2019}, {2018 and 2019}, {2018 and 2022} and {2018 and 2022}, respectively. Which store has maximum percentage change in profits for the pair of years mentioned?",
     "options":["A", "B", "D", "E"],
     "correct_answer":"B",
     "explanation":"The correct answer is (B) B. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea044","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"What should be the income of store D in 2020, so that its profit percent is 30%",
     "options":["₹ 33 lakh", "₹ 42 lakh", "₹ 60 lakh", "₹ 78 lakh"],
     "correct_answer":"₹ 78 lakh",
     "explanation":"The correct answer is (D) ₹ 78 lakh. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea045","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"The profit earned by Store A in 2023 is approximately ________ % more than that in 2019.",
     "options":["40", "66.67", "266", "33.33"],
     "correct_answer":"66.67",
     "explanation":"The correct answer is (B) 66.67. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea046","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"Cloudless night with low wind speed indicates:",
     "options":["Turbulent Atmosphere", "Unstable Atmosphere", "Neutral Atmosphere", "Stable Atmosphere"],
     "correct_answer":"Stable Atmosphere",
     "explanation":"The correct answer is (D) Stable Atmosphere. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea047","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"A shopkeeper first increased the price of an item by 12% and then announces a discount of 20%. The actual discount on the original price is:",
     "options":["12.6%", "10.4%", "14.2%", "12%"],
     "correct_answer":"10.4%",
     "explanation":"The correct answer is (B) 10.4%. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea048","topic":"Reasoning","difficulty":"Hard","year":2024,"season":"June",
     "question":"In the light of Nyaya's Syllogism, which of the following are correct? (a) 'Sādhya' is the major term (b) 'Linga' is the minor term (c) 'Hetu is the middle term (d) 'Paksa' is the minor term (e) 'Anumāna' is the inferential knowledge",
     "options":["(a), (b) and (c) only", "(a), (c), (d) and (e) only", "(b) and (d) only", "(b), (d) and (e) only"],
     "correct_answer":"(a), (c), (d) and (e) only",
     "explanation":"The correct answer is (B) (a), (c), (d) and (e) only. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea049","topic":"Reasoning","difficulty":"Hard","year":2024,"season":"June",
     "question":"Which of the following can be considered as the component of development of ability of critical and logical thinking? (a) To identify the problems (b) To analyse the problems (c) To establish subjective truths (d) To select relevant facts and principles (e) To draw inferences and conclusions",
     "options":["(a) and (c) only", "(a), (b) and (c) only", "(a), (b) and (d) only", "(a), (b), (d) and (e) only"],
     "correct_answer":"(a), (b), (d) and (e) only",
     "explanation":"The correct answer is (D) (a), (b), (d) and (e) only. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea050","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"Identify the numbers that occur in the series 0, 7, 26, 63, 124……………… (a) 344 (b) 511 (c) 215 (d) 730",
     "options":["(a) and (b) only", "(b) and (c) only", "(c) and (d) only", "(a) and (d) only"],
     "correct_answer":"(b) and (c) only",
     "explanation":"The correct answer is (B) (b) and (c) only. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea051","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which of the following is NOT a fallacy of Relevance?",
     "options":["Ad Hominem (Personal Attack)", "Attacking the Motive", "Tu Quoque (Look who's talking)", "False Alternatives"],
     "correct_answer":"False Alternatives",
     "explanation":"The correct answer is (D) False Alternatives. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea052","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"A 200 m long train is travelling at a constant speed of 20 m/s. How long will it take to completely cross a 1000 m long railway platform?",
     "options":["1 minute", "1.5 minute", "2 minutes", "2.5 minutes"],
     "correct_answer":"1 minute",
     "explanation":"The correct answer is (A) 1 minute. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea053","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"Identify the correct logical sequence of the following four randomly-ordered sentences A-D about the discovery of Computer Mouse? (a) We use the mouse today because it is the pointing device that is easiest to use compared to others such as joysticks, trackballs etc. (b) Doug Engelbart was bored at a conference and started thinking about tracking movement of a plane using two sets of wheels moving in orthogonal directions. (c) Doug Engelbart remembered these notes when he was trying to come up with a device to select objects on a computer screen. (d) Doug Engelbart tells the story of how he invented the mouse.",
     "options":["(d), (c), (b), (a)", "(a), (b), (c), (d)", "(b), (c), (d), (a)", "(d), (b), (c), (a)"],
     "correct_answer":"(d), (b), (c), (a)",
     "explanation":"The correct answer is (D) (d), (b), (c), (a). This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea054","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match the List-I with List-II List - I (Fallacy) List - II (Description) (a) Strawman (I) When an arguer tries to side track his audience by raising an irrelevant issue and the claims that the original issue is settled. (b) Red Herring (II) When an arguer states or assumes as a premise the very thing he/she is trying to prove as a conclusion. (c) Equivocation (III) When arguer distorts an opponents claim to make it easier to attack (d) Begging the Question (IV) When a key word is used in two or more senses in the same argument.",
     "options":["(a)-(IV), (b)-(I), (c)-(III), (d)-(II)", "(a)-(II), (b)-(III), (c)-(IV), (d)-(I)", "(a)-(I), (b)-(II), (c)-(IV), (d)-(III)", "(a)-(III), (b)-(I), (c)-(IV), (d)-(II)"],
     "correct_answer":"(a)-(III), (b)-(I), (c)-(IV), (d)-(II)",
     "explanation":"The correct answer is (D) (a)-(III), (b)-(I), (c)-(IV), (d)-(II). This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea055","topic":"Reasoning","difficulty":"Hard","year":2024,"season":"June",
     "question":"What can be inferred correctly from the following? \"Science is based on experiment, on a willingness to challenge old dogma, on an openness to see 51 the universe as it really is. Accordingly, science sometimes requires courage at the very least the courage to question the conventional wisdom.\" (a) Premise: Science sometimes requires courage. (b) Premise: Science is based on experiment, as a willingness to see the universe as it really is. (c) It is merely an Illustration. (d) Conclusion: Science sometimes requires courage. (e) Conclusion: Science is based on experiment, on a willingness to see the universe as it really is.",
     "options":["(a), (c) and (d) only", "(a) and (d) only", "(b) and (d) only", "(b), (c) and (e) only"],
     "correct_answer":"(b) and (d) only",
     "explanation":"The correct answer is (C) (b) and (d) only. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea056","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"Observe the following argument and find the correct form: \"'A' has characteristics of 'X' and 'Y'. 'B' has characteristics of 'X' and 'Y'. 'A' has a characteristics of 'Z'. Therefore 'B' has a characteristics of 'Z'. 52",
     "options":["Statistical Argument", "An argument from Authority", "Mathematical Argument", "Argument from Analogy"],
     "correct_answer":"Argument from Analogy",
     "explanation":"The correct answer is (D) Argument from Analogy. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea057","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"A person sold an item at a loss of 7%. Had he sold the item at a gain of 7.5%, he would have received Rs. 87 more than his selling price. The cost price of the item is:",
     "options":["Rs. 500", "Rs. 550", "Rs. 600", "Rs. 650"],
     "correct_answer":"Rs. 600",
     "explanation":"The correct answer is (C) Rs. 600. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea058","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"In a race of 500 m run, A beats B by 20 m and C by 80 m. If B and C are running another race of 100 m with exactly same speed as before, then by how many meters will B beat C? 58",
     "options":["10.0 m", "8.5 m", "15.0 m", "12.5 m"],
     "correct_answer":"12.5 m",
     "explanation":"The correct answer is (D) 12.5 m. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea059","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"Identify the pattern of the Argument in the following \"Habits are like a cable. We weave a strand of it everyday and soon it cannot be broken.\"",
     "options":["Causal Argument", "Argument from Analogy", "Argument from Authority", "Argument from Definition"],
     "correct_answer":"Argument from Analogy",
     "explanation":"The correct answer is (B) Argument from Analogy. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea060","topic":"Reasoning","difficulty":"Hard","year":2024,"season":"June",
     "question":"What in the following can be correctly inferred? \"You know how I know animals have souls? Because on an average, the lowest animal is a lot nicer and kinder than most of the human beings that inhabit this Earth\". (a) Premise: The lowest animal is a lot nicer and kinder than most human beings that inhabit this Earth. (b) Premise: Animals have soul (c) It is not an argument (d) Conclusion: The lowest animal is a lot nicer and kinder than most human beings that inhabit this Earth (e) Conclusion: Animals have soul",
     "options":["(b), (c) and (d) only", "(a), (c) and (e) only", "(a) and (e) only", "(a), (d) and (e) only"],
     "correct_answer":"(a) and (e) only",
     "explanation":"The correct answer is (C) (a) and (e) only. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea061","topic":"Reasoning","difficulty":"Hard","year":2024,"season":"June",
     "question":"What can be inferred correctly from the following? \"No musicians are Greeks. All traders are Musicians. Therefore, no traders are Greeks\" (a) It represents figure II of the syllogistic argument (b) It is an EAE mood (c) The term 'Greeks' is the major term (d) The minor term of the conclusion is distributed (e) The middle term is undistributed",
     "options":["(a), (b) and (c) only", "(b), (c) and (d) only", "(d) and (e) only", "(a), (c) and (e) only"],
     "correct_answer":"(b), (c) and (d) only",
     "explanation":"The correct answer is (B) (b), (c) and (d) only. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea062","topic":"Reasoning","difficulty":"Hard","year":2024,"season":"June",
     "question":"Identify the numbers that occur in the series 1, 7, 17, 31, 49, …… (a) 74 (b) 95 (c) 97 (d) 127 (e) 161",
     "options":["(a), (b), (c) only", "(c), (d), (e) only", "(e), (b), (a) only", "(c), (d), (b) only"],
     "correct_answer":"(c), (d), (e) only",
     "explanation":"The correct answer is (B) (c), (d), (e) only. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea063","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"The amount of biomass produced by the plants through photosynthesis minus respiration losses in a given time period is known as:",
     "options":["Gross Primary Productivity", "Net Primary Productivity", "Gross Ecological Productivity", "Net Secondary Productivity"],
     "correct_answer":"Net Primary Productivity",
     "explanation":"The correct answer is (B) Net Primary Productivity. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea065","topic":"Reasoning","difficulty":"Hard","year":2024,"season":"June",
     "question":"Identify the numbers that occur in the given series:- 0,3,10,21,36,…….. (a) 55 (b) 78 (c) 99 (d) 105 68 (e) 136",
     "options":["(a), (b), (c) and (d) Only", "(b), (c) and (e) Only", "(c) (d), (e) and (a) Only", "(d), (e), (a) and (b) Only"],
     "correct_answer":"(d), (e), (a) and (b) Only",
     "explanation":"The correct answer is (D) (d), (e), (a) and (b) Only. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea066","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"A ship is approaching towards a shore, when it is 32 miles from the shore, a plane having speed 15 times that of the ship is sent to deliver supplies. How far from sea shore does the sea plane catches up with the ship?",
     "options":["30 miles", "25 miles", "15 miles", "10 miles"],
     "correct_answer":"30 miles",
     "explanation":"The correct answer is (A) 30 miles. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea067","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"A major defect of the sargeant plan was",
     "options":["Integration of education with economic institutions", "Emphasis on social sector", "Too much importance to technical education", "Highly selective admission to colleges"],
     "correct_answer":"Highly selective admission to colleges",
     "explanation":"The correct answer is (D) Highly selective admission to colleges. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea068","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"What can be correctly claimed about the following? \"I ate because I was hungry\"",
     "options":["Its an argument.", "Its a Non-argument", "Its a non-argument, it's an Explanation", "Its a non-argument, it's an Illustration"],
     "correct_answer":"Its a non-argument, it's an Explanation",
     "explanation":"The correct answer is (C) Its a non-argument, it's an Explanation. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea069","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"Identify the fallacy committed in the following: \"Ford cars are lemons, I have owned two and they gave me nothing but trouble\".",
     "options":["Inappropriate appeal to authority", "False alternative", "No fallacy", "Hasty Generalization"],
     "correct_answer":"Hasty Generalization",
     "explanation":"The correct answer is (D) Hasty Generalization. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea070","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match the List-I with List-II List - I List - II 73 (Jackson's learning style) (Description) (a) High sensation seeker (I) Responsible, rational learners, endowed with an urge to explore the world so that positive goals can be achieved (b) Goal oriented achievers (II) Learns from their mistakes, possess a scientific, detached and autonomous learning style, processes information in an emotionally intelligent-manner (c) Emotionally Intelligent Achiever (III) Gets involved in new challenging activities (d) Conscientious Achiever (IV) One who sets learning goal which are generally hard and specific and has confidence to achieve the goals.",
     "options":["(a)-(II), (b)-(III), (c)-(I), (d)-(IV)", "(a)-(III), (b)-(IV), (c)-(II), (d)-(I)", "(a)-(IV), (b)-(I), (c)-(III), (d)-(II)", "(a)-(I), (b)-(III), (c)-(IV), (d)-(II)"],
     "correct_answer":"(a)-(III), (b)-(IV), (c)-(II), (d)-(I)",
     "explanation":"The correct answer is (B) (a)-(III), (b)-(IV), (c)-(II), (d)-(I). This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea071","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"Name the fallacy committed in the following: \"All the textbooks are books intended for careful study. Some reference books are books intended for careful study. Therefore, some reference books are textbooks\"",
     "options":["Fallacy of Illicit Minor", "Fallacy of Illicit Major", "Undistributed Middle", "Fallacy of four terms"],
     "correct_answer":"Undistributed Middle",
     "explanation":"The correct answer is (C) Undistributed Middle. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea072","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which of the following is incorrect claim in the context of Vyapti?",
     "options":["For Cārvākās, it is possible to ascertain that smoke is invariably and universally attended", "For Buddhists, the universal relation between smoke and fire can be ascertained even without", "For Vedāntins, Vyāpti between smoke and fire is known to co-exist and at the same time it is", "For Naiyayikas, it is neither easy nor necessary for the formation of a universal proposition"],
     "correct_answer":"For Cārvākās, it is possible to ascertain that smoke is invariably and universally attended",
     "explanation":"The correct answer is (A) For Cārvākās, it is possible to ascertain that smoke is invariably and universally attended. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea073","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"Microsoft PowerPoint comes with several categories of built-in transition effects. Which of the following is not a type of transition effect supported by Microsoft PowerPoint?",
     "options":["Subtle", "Speed", "Exciting", "Dynamic Content"],
     "correct_answer":"Speed",
     "explanation":"The correct answer is (B) Speed. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea074","topic":"Reasoning","difficulty":"Hard","year":2024,"season":"June",
     "question":"Identify the correct chronological order of the following institutions of higher learning? (a) Rajkot College, Rajkot (b) Civil Engineering College, Roorkee 79 (c) Sanskrit College, Calcutta (d) Sanskrit College, Benaras (e) Fort Williams College, Calcutta",
     "options":["(a), (b), (e), (d), (c)", "(c), (a), (b), (e), (d)", "(d), (e), (c), (b), (a)", "(b), (c), (a), (d), (e)"],
     "correct_answer":"(d), (e), (c), (b), (a)",
     "explanation":"The correct answer is (C) (d), (e), (c), (b), (a). This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea075","topic":"Reasoning","difficulty":"Hard","year":2024,"season":"June",
     "question":"According to Department of Higher Education, Ministry of Education (GoI), which of the following are considered as the Institutions of higher learning? (a) The National Institute of Fashion Technology, New Delhi (b) National Institute of Design (c) Indian Institute of Advanced Study, Shimla (d) National University of Education Planning and Administration (Neupa), Delhi (e) Rashtriya Sanskrit Vidhyapeetha, Tirupati",
     "options":["(a), (b), (c) only", "(b), (c), (d) only", "(a), (b), (d) only", "(c), (d), (e) only"],
     "correct_answer":"(c), (d), (e) only",
     "explanation":"The correct answer is (D) (c), (d), (e) only. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea076","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"Interpretation of a media text, which is in variance with the original creator's intention is described as",
     "options":["Impersonal decoding", "Aberrant decoding", "Above-the-line decoding", "Unequal decoding"],
     "correct_answer":"Aberrant decoding",
     "explanation":"The correct answer is (B) Aberrant decoding. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea077","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which of the following arguments is fallacious because the middle term is non - exclusive?",
     "options":["All things are non-eternal, because they are knowable.", "The hill has fire because it is knowable.", "Fire is cold because it is a substance.", "Sound is eternal because it is produced."],
     "correct_answer":"All things are non-eternal, because they are knowable.",
     "explanation":"The correct answer is (A) All things are non-eternal, because they are knowable.. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea078","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"Which of the following statements are logically equivalent? (a) All non-trees are non-animals (b) No animals are trees (c) Some animals are not trees (d) No trees are animals",
     "options":["(a) and (d) only", "(a) and (b) Only", "(b) and (d) only", "(b) and (c) only"],
     "correct_answer":"(b) and (d) only",
     "explanation":"The correct answer is (C) (b) and (d) only. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea079","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"In a certain coding language if the word 'SOUND' is coded as 'VLXKG', then the word 'TRAIN' will be coded as",
     "options":["VQWPF", "WQDGQ", "WODFQ", "VODGQ"],
     "correct_answer":"WODFQ",
     "explanation":"The correct answer is (C) WODFQ. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea080","topic":"Reasoning","difficulty":"Hard","year":2024,"season":"June",
     "question":"With reference to the computers, which of the following statements are correct? (a) CPU follows fetch-decode-execute-store cycle to run instructions. (b) Intel and AMD are two manufactures of CPUs (c) The clock speed of a CPU is usually measured in Megabytes (d) Fans are required to cool down most CPUs so that they do not overheat (e) CPU is the brain of the computers and modern CPUs cannot have multiple processing cores.",
     "options":["(a), (b), (c) and (d) only", "(a) and (b) Only", "(c) and (d) only", "(a), (b) and (d) only"],
     "correct_answer":"(a), (b) and (d) only",
     "explanation":"The correct answer is (D) (a), (b) and (d) only. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea081","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"Which of the following statements is true about the proposition - \"A ship has mass. Therefore, all the parts of the ship have mass\".\"?",
     "options":["It commits the fallacy of division", "It commits the fallacy of equivocation", "It commits the fallacy of hasty generalisation", "It is a non-fallacious statement"],
     "correct_answer":"It is a non-fallacious statement",
     "explanation":"The correct answer is (D) It is a non-fallacious statement. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea082","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which one of the following rotors is commonly used for electricity generation?",
     "options":["Savonious rotor", "Darrious rotor", "Propeller rotor", "Multiblade rotor"],
     "correct_answer":"Propeller rotor",
     "explanation":"The correct answer is (C) Propeller rotor. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea083","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"If the selling price of Rs.36 results in a discount of 25% on the marked price of an item, at what price should the item be sold to offer a discount of 20%?",
     "options":["Rs. 37.8", "Rs. 38.0", "Rs. 38.4", "Rs. 39.4"],
     "correct_answer":"Rs. 38.4",
     "explanation":"The correct answer is (C) Rs. 38.4. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea084","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"What is easier to achieve in a ritualistic workplace compared to a goal - driven one?",
     "options":["Financial success", "State of flow", "Stress and anxiety", "Unclear goal"],
     "correct_answer":"State of flow",
     "explanation":"The correct answer is (B) State of flow. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea085","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"The average number of male viewers of SONY TV from all the six cities together is approximately _______ % of the six cities of viewers of JIO TV from city D.",
     "options":["30", "40", "50", "60"],
     "correct_answer":"50",
     "explanation":"The correct answer is (C) 50. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea086","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"What is the average number of female viewers of Zee TV taking all six cities together?",
     "options":["1242", "1262", "1282", "1302"],
     "correct_answer":"1282",
     "explanation":"The correct answer is (C) 1282. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea087","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"One term in the number series is wrong. Find out the wrong term? 325, 259, 202, 160, 127, 105, 94",
     "options":["94", "127", "202", "259"],
     "correct_answer":"202",
     "explanation":"The correct answer is (C) 202. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea088","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"In a certain coding language, if the word 'FLOUT' is coded as 'IIRRW', then the word 'CLING' will be coded as:",
     "options":["ΕΝΚΡΙ", "EHLJK", "FLILK", "FILKJ"],
     "correct_answer":"FILKJ",
     "explanation":"The correct answer is (D) FILKJ. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea089","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"“No one has ever been able to prove that psychic powers do not exists. Therefore it is proved that psychic powers do exist. Identify the fallacy in the above arguments.",
     "options":["Appeal to ignorance", "Hasty generalization", "Slippery slope", "Equivocation"],
     "correct_answer":"Appeal to ignorance",
     "explanation":"The correct answer is (A) Appeal to ignorance. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea090","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"If the selling price of Rs 235 results in a discount of 6% on the marked price of an item, at what price should the item be sold to offer a discount of 15%?",
     "options":["Rs 199.5", "Rs 206.5", "Rs 212.5", "Rs 215"],
     "correct_answer":"Rs 212.5",
     "explanation":"The correct answer is (C) Rs 212.5. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea091","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"Which of the following statements are logically equivalent? (a) Some non-intelligent animals are non-apes (b) Some apes are not intelligent animals (c) Some apes are non - intelligent animals (d) Some non - intelligent animals are not non-apes",
     "options":["(a), (b) and (c) only", "(a) and (c) only", "(a) and (d) only", "(b), (c) and (d) only"],
     "correct_answer":"(b), (c) and (d) only",
     "explanation":"The correct answer is (D) (b), (c) and (d) only. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea092","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which of the arguments is fallacious because the middle term is pervaded by the absence of the major term instead of its presence:",
     "options":["The hill has fire because it is knowable", "Sound is eternal because it is produced", "Sound is eternal because it is audible", "Sound is quality because it is visible"],
     "correct_answer":"Sound is eternal because it is produced",
     "explanation":"The correct answer is (B) Sound is eternal because it is produced. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea093","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"What is the ratio of percentage decline in votes of B in May in comparison to January to the percentage decline in votes of C in November in comparison to January?",
     "options":["6:7", "7:6", "6:5", "4:3"],
     "correct_answer":"6:5",
     "explanation":"The correct answer is (C) 6:5. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea094","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"As per table, in the month of July, the votes of D and C are in the ratio 9:5. If the votes of D remain same, then the votes of C should increase by _________% to make the ratio 5:9 (in the month of July).",
     "options":["80", "124", "144", "224"],
     "correct_answer":"224",
     "explanation":"The correct answer is (D) 224. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea095","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match List I with List II. List - I (App) List - II (Use) (a) Labster (I) Real-time polling (b) Google Earth (II) Virtual labs and simulations (c) Kahoot (III) Virtual field trips and geographic exploration (d) Poll Everywhere (IV) Online quizzes and assessments",
     "options":["(a)-(IV), (b)-(III), (c)-(II), (d)-(I)", "(a)-(I), (b)-(II), (c)-(III), (d)-(IV)", "(a)-(II), (b)-(III), (c)-(IV), (d)-(I)", "(a)-(III), (b)-(I), (c)-(II), (d)-(IV)"],
     "correct_answer":"(a)-(II), (b)-(III), (c)-(IV), (d)-(I)",
     "explanation":"The correct answer is (C) (a)-(II), (b)-(III), (c)-(IV), (d)-(I). This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea096","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"Find the next term in the series given below: 2, 10, 30, 68, 130, ?",
     "options":["200", "222", "100", "175"],
     "correct_answer":"222",
     "explanation":"The correct answer is (B) 222. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea097","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"The reduced ability to remember information acquired after the onset of Amnesia is known as:",
     "options":["Working memory", "Retrograde amnesia", "Phonological loop", "Anterograde amnesia"],
     "correct_answer":"Anterograde amnesia",
     "explanation":"The correct answer is (D) Anterograde amnesia. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea098","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"From the following identify the propositions that are logically equivalent. (a) No plants are animals. (b) No animals are plants. (c) All plants are non-animals. (d) All non-animals are plants.",
     "options":["(a) and (d) only", "(b) and (c) only", "(a), (b) and (c) only", "(a) and (c) only"],
     "correct_answer":"(a), (b) and (c) only",
     "explanation":"The correct answer is (C) (a), (b) and (c) only. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea099","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"\"If Anup is a member of Animal Rights Society, then he opposes horse racing. Anup opposes horse racing, therefore, he is a member of Animal Rights Society\". Which fallacy is committed in the above argument?",
     "options":["Hasty generalisation", "Inappropriate authority", "Affirming the consequent", "Denying the antecedent"],
     "correct_answer":"Affirming the consequent",
     "explanation":"The correct answer is (C) Affirming the consequent. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea100","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"In computing, which of the following is a program downloaded and installed on a computer that appears harmless, but is in fact, malicious.",
     "options":["Trojan Horse", "Time Bomb", "Worm", "Logic Bomb"],
     "correct_answer":"Trojan Horse",
     "explanation":"The correct answer is (A) Trojan Horse. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea101","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"If 'CONSTABLE' is coded as 91 and 'STABLE' is coded as 59, then how 'PORTABLE' shall be coded?",
     "options":["89", "109", "111", "110"],
     "correct_answer":"89",
     "explanation":"The correct answer is (A) 89. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea102","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"Forty-five (45) men can do a job in 16 days. Six days after they started working, 30 more men joined them. How many days will they now take to complete the remaining work?",
     "options":["5", "7 days", "5 days", "6 days"],
     "correct_answer":"6 days",
     "explanation":"The correct answer is (D) 6 days. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea103","topic":"Reasoning","difficulty":"Hard","year":2024,"season":"June",
     "question":"Which of the following are true about Waste-to-Energy incinerations? (a) It serves dual purpose of disposing municipal solid waste and producing energy (b) It produces fly ash (c) It produces bottom ash (d) It generates a high level toxic air pollutant-dioxin (e) It produces toxic metals such as Lead and Mercury",
     "options":["(a), (c), (d) and (e) only", "(a), (b), (d) and (e) only", "(b) and (c) only", "(a), (b), (c), (d) and (e) only"],
     "correct_answer":"(a), (b), (c), (d) and (e) only",
     "explanation":"The correct answer is (D) (a), (b), (c), (d) and (e) only. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea104","topic":"Reasoning","difficulty":"Hard","year":2024,"season":"June",
     "question":"In cyber world, Black Hat Hackers are individuals with extra-ordinary computing skills who use these skills with malicious intent. In this context, identify the correct order for a successful black hat operation. (a) Scanning (b) Reconnaissance (c) Gaining Access (d) Covering Tracks (e) Maintaining Access 116",
     "options":["(a), (b), (c), (e), (d)", "(b), (a), (c), (e), (d)", "(c), (d), (b), (a), (e)", "(d), (c), (a), (e), (b)"],
     "correct_answer":"(b), (a), (c), (e), (d)",
     "explanation":"The correct answer is (B) (b), (a), (c), (e), (d). This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea105","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"If 'CAKE' is coded as 20 and 'FAIL' is coded as 28 then how 'FIRST' shall be coded?",
     "options":["35", "72", "64", "40"],
     "correct_answer":"72",
     "explanation":"The correct answer is (B) 72. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea106","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which of the following is the most appropriate for measuring the strength and direction of association between two interval/ratio variables?",
     "options":["Spearman's rho", "Pearson's r", "Phi", "Eta"],
     "correct_answer":"Pearson's r",
     "explanation":"The correct answer is (B) Pearson's r. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea107","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which component of Baddeley's basic working memory model is involved in the task of pressing keys on a keypad in a clockwise pattern?",
     "options":["Visuospatial sketchpad", "Bounded rationality", "Phonological loop", "Metacognition"],
     "correct_answer":"Visuospatial sketchpad",
     "explanation":"The correct answer is (A) Visuospatial sketchpad. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea108","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"So far, which of the following countries has not ratified the Convention on Biological Diversity?",
     "options":["India", "China", "Russia", "United States of America"],
     "correct_answer":"United States of America",
     "explanation":"The correct answer is (D) United States of America. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea109","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"Find the missing term in the series given below. 2, 12, 36, ?, 150",
     "options":["80", "72", "100", "86"],
     "correct_answer":"80",
     "explanation":"The correct answer is (A) 80. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea110","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"From the following identify the statements that are logically equivalent. (a) No squares are circles (b) Some squares are not circles 120 (c) Some non-circles are not non-squares (d) No circles are squares",
     "options":["(b) and (d) only", "(b) and (c) only", "(a), (b) and (c) only", "(a), (c) and (d) only"],
     "correct_answer":"(b) and (c) only",
     "explanation":"The correct answer is (B) (b) and (c) only. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea111","topic":"Reasoning","difficulty":"Hard","year":2024,"season":"June",
     "question":"Identify the correct sequence of the emergence of the following concepts. (a) Virtual Communities (b) Cyber Culture (c) Being Digital (d) Tele Computer (e) Interactive Media Culture",
     "options":["(a), (b), (c), (d), (e)", "(b), (c), (d), (a), (e)", "(d), (a), (c), (e), (b)", "(c), (d), (e), (a), (b)"],
     "correct_answer":"(d), (a), (c), (e), (b)",
     "explanation":"The correct answer is (C) (d), (a), (c), (e), (b). This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea112","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"What is the percentage rise in the sale of sports shoes by company F from the year 2022 to 2023?",
     "options":["12%", "25%", "15%", "20%"],
     "correct_answer":"20%",
     "explanation":"The correct answer is (D) 20%. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea113","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"\"Somdutta who is never seen eating during the day time is constantly gaining weight. Therefore, she must be eating during the night time\". As per classical Indian philosophy which instrument of knowledge is used in the above statement?",
     "options":["Perception", "Analogy", "Verbal authority", "Postulation"],
     "correct_answer":"Postulation",
     "explanation":"The correct answer is (D) Postulation. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea114","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"In a certain code language: \"Bitter patience sweet fruit\" is coded as: \"Bo Po So To\" \"Art is sweet happiness\" is coded as: \"Ao Io So Ho\" \"Hoping is concealing bitter\" is coded as: \"Hp Io Co Bo\" \"Patience is art of hoping\" is coded as: \"Po Io Ao Fo Hp\" How \"Patience is happiness\" will be coded in this language?",
     "options":["Ho Io Po", "Hp Ao Po", "Po Ao Hp", "Po Io Ho"],
     "correct_answer":"Po Io Ho",
     "explanation":"The correct answer is (D) Po Io Ho. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea115","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"Which of the following is/are true? (a) If the selling price (SP) of an article is ₹ 40 and the gain is 15%, the cost price (CP) of the article is ₹ 32 (b) A man bought a toy for ₹ 150 and sold it at a profit of 8%. He sold the toy for ₹ 162 (c) A man buys a cycle for ₹ 500, but due to some problem, he sells it for ₹ 400. He thus incurs a loss of 22% (d) Cost price of an article, if its SP is ₹ 210 and the loss is 30%, is ₹ 300.",
     "options":["(a) only", "(a) and (d) only", "(b) and (d) only", "(b) and (c) only"],
     "correct_answer":"(b) and (d) only",
     "explanation":"The correct answer is (C) (b) and (d) only. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea116","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which component of Baddeley's basic working memory model is involved in the task of Rapid repetition of the word like \"See-Saw\"?",
     "options":["Visuospatial sketchpad", "Bounded rationality", "Phonological loop", "Meta-cognition"],
     "correct_answer":"Phonological loop",
     "explanation":"The correct answer is (C) Phonological loop. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea117","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"Consider the series given below. Find the number which can be inserted at the place of question mark (?). 5, 14, 39, 88, 209, ? , 667 129",
     "options":["378", "297", "299", "375"],
     "correct_answer":"378",
     "explanation":"The correct answer is (A) 378. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea118","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match List I with List - II. List -I (Commission) List -II (Recommendation) (a) Hunter Commission (I) University technological departments providing for research and teaching (b) Sadler Commission (II) Withdrawal of government support to collegiate education (c) Hartog Committee (III) Development of mofussil colleges into future university centres (d) Sargent plan (IV) Enrichment of college libraries and concentration on Honours courses in select centres",
     "options":["(a)-(I), (b)-(II), (c)-(III), (d)-(IV)", "(a)-(II), (b)-(III), (c)-(IV), (d)-(I)", "(a)-(III), (b)-(IV), (c)-(I), (d)-(II)", "(a)-(IV), (b)-(I), (c)-(II), (d)-(III)"],
     "correct_answer":"(a)-(II), (b)-(III), (c)-(IV), (d)-(I)",
     "explanation":"The correct answer is (B) (a)-(II), (b)-(III), (c)-(IV), (d)-(I). This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea119","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"\"If one eats mushrooms after a long gap of time, one falls ill. I have been having some digestive issues since morning today, therefore there must have been mushroom in that mixed vegetable soup we had last night\" which fallacy, if any, committed in the above argument?",
     "options":["It is a valid argument", "Affirming the consequent", "Hasty Generalization", "Begging the question"],
     "correct_answer":"Affirming the consequent",
     "explanation":"The correct answer is (B) Affirming the consequent. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea120","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"From the following identify the propositions that are logically equivalent. (a) Some books are novels (b) Some books are not non-novels (c) Some novels are not non-books (d) Some novels are books",
     "options":["(c) and (d) only", "(a) and (d) only", "(a) and (c) only", "(a), (b), (c) and (d)"],
     "correct_answer":"(a), (b), (c) and (d)",
     "explanation":"The correct answer is (D) (a), (b), (c) and (d). This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea121","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match List - I with List - II. List - I (Scale of Measurement) List - II (Example of Variable) (a) Nominal (I) Height of students (b) Ordinal (II) Time of Day (c) Interval (III) Caste (d) Ratio (IV) Rank of Army personnel",
     "options":["(a)-(I), (b)-(II), (c)-(III), (d)-(IV)", "(a)-(II), (b)-(III), (c)-(IV), (d)-(I)", "(a)-(III), (b)-(IV), (c)-(II), (d)-(I)", "(a)-(IV), (b)-(I), (c)-(II), (d)-(III)"],
     "correct_answer":"(a)-(III), (b)-(IV), (c)-(II), (d)-(I)",
     "explanation":"The correct answer is (C) (a)-(III), (b)-(IV), (c)-(II), (d)-(I). This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea122","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"What is the ratio of the number of female participants from US in the event E2 to the number of female participants from China in the event E3?",
     "options":["60:31", "29:31", "27:31", "58:31"],
     "correct_answer":"60:31",
     "explanation":"The correct answer is (A) 60:31. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea123","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"In a certain coded language: \"Indian cuisines are good\" is coded as: \"MI CI FI GI\" \"They like Indian cuisines\" is coded as: \"AI LI MI CI\" \"People like Indian Chinese\" is coded as: \"PI LI MI HI\" \"They and people are best\" is coded as: \"AI DI PI FI BI\" How the words 'good' Chinese' and 'cuisines' are coded in this language?",
     "options":["GI, HI and CI", "AI, LI and FI", "MI, DI and BI", "HI, Cl and LI"],
     "correct_answer":"GI, HI and CI",
     "explanation":"The correct answer is (A) GI, HI and CI. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea124","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"The average age of a group of workers is 42 yrs. If eight (8) new workers of average age of 36 yrs. join the group, the average age of the group becomes 40 yrs. Find the number of workers initially present in the group:",
     "options":["17", "16", "18", "20"],
     "correct_answer":"16",
     "explanation":"The correct answer is (B) 16. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea125","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match List - I with List - II. List - I (Concept of profit) List - II (Description) (a) Synergy (I) Strong incentive to replicate a successful format 139 (b) Planned obsolescence (II) Media obsession with sensationalism (c) Logic of safety (III) Horizontal integration of subsidiary media companies (d) Spectacle (IV) Planned Phasing out of product",
     "options":["(a)-(I), (b)-(II), (c)-(III), (d)-(IV)", "(a)-(II), (b)-(III), (c)-(IV), (d)-(I)", "(a)-(III), (b)-(IV), (c)-(I), (d)-(II)", "(a)-(IV), (b)-(I), (c)-(II), (d)-(III)"],
     "correct_answer":"(a)-(III), (b)-(IV), (c)-(I), (d)-(II)",
     "explanation":"The correct answer is (C) (a)-(III), (b)-(IV), (c)-(I), (d)-(II). This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea126","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"Which of the following statements are true? (a) An argument is sound when it is valid and has only true premises (b) In an argument truth of its conclusion determines its validity by itself. (c) Some valid arguments have false premises and a true conclusion (d) Some invalid arguments have false premises and a true conclusion",
     "options":["(a), (c) and (d) only", "(a), (b) and (c) only", "(b) and (c) only", "(a), (b) and (d) only"],
     "correct_answer":"(a), (c) and (d) only",
     "explanation":"The correct answer is (A) (a), (c) and (d) only. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea127","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"\"According to some newspapers today the Crime rate in New York has slightly increased in the recent past. New Yorkers are nothing but a bunch of criminals\". Which fallacy is committed in the above statement?",
     "options":["Slippery slope", "Appeal to Inappropriate Authority", "Hasty Generalization", "Strawman"],
     "correct_answer":"Hasty Generalization",
     "explanation":"The correct answer is (C) Hasty Generalization. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea128","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"Which of the following statements are true? (a) A single discount, equivalent to a series of discounts of 20%, 10% and 5%, is 35%. (b) If after two successive discounts of 12% and 5%, an article was sold for ₹209, then the original price of the article is ₹250. (c) If a shopkeeper allows two successive discounts of 5% each on the marked price of ₹80, the selling price of the article is ₹75. (d) If the difference between a single discount of 35% and two successive discounts of 20% on a certain bill is ₹22, then the total amount of the bill is ₹2200.",
     "options":["(a), (b) and (c) only", "(a) and (c) only", "(b) and (d) only", "(c) and (d) only"],
     "correct_answer":"(b) and (d) only",
     "explanation":"The correct answer is (C) (b) and (d) only. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea129","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"According to Nyāya logic, which of the following statements is fallacious because it involves a non- inferentially contradicted middle term?",
     "options":["The hill has fire because it is knowable", "Fire is cold because it is a substance", "All things are non-eternal because they are knowable", "Sound is eternal because it is audible"],
     "correct_answer":"Fire is cold because it is a substance",
     "explanation":"The correct answer is (B) Fire is cold because it is a substance. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea130","topic":"Reasoning","difficulty":"Hard","year":2024,"season":"June",
     "question":"Identify the chronological sequence of the following communication devices: (a) Audio cassettes (b) Long playing record (c) Magnetic tape (d) Compact discs (e) MP3",
     "options":["(a), (b), (c), (e), (d)", "(b), (d), (e), (a), (c)", "(c), (b), (a), (d), (e)", "(d), (e), (b), (c), (a)"],
     "correct_answer":"(c), (b), (a), (d), (e)",
     "explanation":"The correct answer is (C) (c), (b), (a), (d), (e). This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea131","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match List - I with List - II. List - I (Informal fallacy) List - II (Reason) (a) Argument from Ignorance (I) Presumption (b) Appeal to Emotion (II) Ambiguity (c) Fallacy of Division (III) Relevance (d) Begging the Question (IV) Defective Induction",
     "options":["(a)-(IV), (b)-(II), (c)-(III), (d)-(I)", "(a)-(IV), (b)-(I), (c)-(III), (d)-(II)", "(a)-(I), (b)-(III), (c)-(II), (d)-(IV)", "(a)-(IV), (b)-(III), (c)-(II), (d)-(I)"],
     "correct_answer":"(a)-(IV), (b)-(III), (c)-(II), (d)-(I)",
     "explanation":"The correct answer is (D) (a)-(IV), (b)-(III), (c)-(II), (d)-(I). This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea132","topic":"Reasoning","difficulty":"Hard","year":2024,"season":"June",
     "question":"Find out the chronological order of the following agencies of educational administration in British India. (a) University Board (b) Board of Governors (c) Committee of Native Education (d) Council of Education (e) Department of Public Instruction",
     "options":["(a), (c), (d), (e), (b)", "(b), (e), (c), (a), (d)", "(c), (a), (d), (b), (e)", "(d), (e), (b), (c), (a)"],
     "correct_answer":"(c), (a), (d), (b), (e)",
     "explanation":"The correct answer is (C) (c), (a), (d), (b), (e). This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea133","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"Which of the following statements about adolescence is true?",
     "options":["Adolescence is a period in between the years from 12 to the early 20's.", "No one can predict exactly when adolescence commences.", "Adolescents are incompetent in tackling science and mathematics puzzles.", "Adolescence does not include any physical and psychological change"],
     "correct_answer":"Adolescence is a period in between the years from 12 to the early 20's.",
     "explanation":"The correct answer is (A) Adolescence is a period in between the years from 12 to the early 20's.. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea134","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"A.T. Jersild's definition regarding adolescence highlights the following:",
     "options":["A child moves from childhood to adulthood, mentally, emotionally, socially and physically.", "Adolescents spend less time in front of the television than other age groups.", "Adolescents reject their parents as companions and as a source of advice.", "Only a minority of adolescents experience some serious psychological issues."],
     "correct_answer":"A child moves from childhood to adulthood, mentally, emotionally, socially and physically.",
     "explanation":"The correct answer is (A) A child moves from childhood to adulthood, mentally, emotionally, socially and physically.. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea135","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"If the number of male unsubscribed viewers in Town-D is 200 3 % more than that of female unsubscribed viewers, then what is the ratio of number of male unsubscribed viewers in Town-D to the number of unsubscribed viewers in Town-A and Town-C together?",
     "options":["25:53", "25:54", "7:9", "2:3"],
     "correct_answer":"25:54",
     "explanation":"The correct answer is (B) 25:54. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea136","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"What is the correct sequence of following drinking water treatment processes from initial to final? (a) Filtration (b) Disinfection (c) Gravity settlement of large particles (d) Flocculation",
     "options":["(a), (b), (c), (d)", "(a), (b), (d), (c)", "(c), (d), (a), (b)", "(c), (d), (b), (a)"],
     "correct_answer":"(c), (d), (a), (b)",
     "explanation":"The correct answer is (C) (c), (d), (a), (b). This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea137","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match List I with List II. List - I (n=number of trials p=probability of success) List - II (Variance of Binomial Distribution) (a) n = 7, p = 0.3 (I) 1.44 (b) n = 5, p = 0.4 (II) 2.00 (c) n = 8, p = 0.5 (III) 1.20 (d) n = 6, p = 0.6 (IV) 1.47",
     "options":["(a)-(I), (b)-(II), (c)-(III), (d)-(IV)", "(a)-(II), (b)-(III), (c)-(IV), (d)-(I)", "(a)-(III), (b)-(IV), (c)-(I), (d)-(II)", "(a)-(IV), (b)-(III), (c)-(II), (d)-(I)"],
     "correct_answer":"(a)-(IV), (b)-(III), (c)-(II), (d)-(I)",
     "explanation":"The correct answer is (D) (a)-(IV), (b)-(III), (c)-(II), (d)-(I). This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea138","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"The impaired memory for events occuring before the onset of amnesia is called as:-",
     "options":["Phonological loop", "Retrograde amnesia", "Anterograde amnesia", "Visuospatial sketchpad"],
     "correct_answer":"Retrograde amnesia",
     "explanation":"The correct answer is (B) Retrograde amnesia. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea139","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"Identify the sequence of ICT terms A-D that correctly fills the blanks in the following paragraph: __________is permanent memory that is used to store instructions that are needed to start the computer. _________ is fast temporary memory that is used to store data and applications that are currently in use. _________ carries out processing and turns data into information. The ________is used to plug all other components into the computer system. (a) Motherboard (b) RAM (c) CPU (d) ROM",
     "options":["(d), (b), (a), (c)", "(a), (d), (c), (b)", "(c), (a), (b), (d)", "(d), (b), (c), (a)"],
     "correct_answer":"(d), (b), (c), (a)",
     "explanation":"The correct answer is (D) (d), (b), (c), (a). This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea140","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"Which of the following statements are true? (a) A valid argument may have false premises and a true conclusion (b) An invalid argument may have false premises and a true conclusion (c) An invalid argument may have true premises and a false conclusion (d) A valid argument may have true premises and a false conclusion",
     "options":["(a), (b), (c), (d)", "(b) and (c) only", "(a) and (d) only", "(a), (b) and (c) only"],
     "correct_answer":"(a), (b) and (c) only",
     "explanation":"The correct answer is (D) (a), (b) and (c) only. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea141","topic":"Reasoning","difficulty":"Hard","year":2024,"season":"June",
     "question":"Identify the correct chronological sequence of the following communication devices: (a) Blu-ray Disc (b) Universal media Disc (c) Digital Compact Disc (d) Hi 8 (e) Digital Audio Tape",
     "options":["(e), (d), (c), (b), (a)", "(d), (c), (b), (a), (e)", "(c), (b), (a), (e), (d)", "(b), (a), (e), (d), (c)"],
     "correct_answer":"(e), (d), (c), (b), (a)",
     "explanation":"The correct answer is (A) (e), (d), (c), (b), (a). This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea142","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"In a certain code language: \"Kashmiri Cuisines are good\" is coded as: \"KI CI FI GI\" \"You like Kashmiri Cuisines\" is coded as: \"AI LI KI CI\" \"Indians like Punjabi Cuisines\" is coded as: \"MI LI BI CI\" \"Punjabi Cuisines are best\" is coded as: \"BI CI FI TI\" How the words 'you', 'Indians' and' best' are coded in this language.",
     "options":["LI, KI and AI", "KI, MI and CI", "AI, MI and TI", "AI, MI and CI"],
     "correct_answer":"AI, MI and TI",
     "explanation":"The correct answer is (C) AI, MI and TI. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea143","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"Arrange the following Ancient Texts in chronological order. (a) Rig Veda (b) Lilāvati (c) Āryabhatiya (d) Arthasāstra",
     "options":["(a), (c), (d), (b)", "(a), (d), (c), (b)", "(b), (c), (d), (a)", "(a), (b), (d), (c)"],
     "correct_answer":"(a), (d), (c), (b)",
     "explanation":"The correct answer is (B) (a), (d), (c), (b). This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea144","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match the List-I with List-II List - I (Type of informal Fallacy) List - II (Reason) (a) False cause (I) Relevance (b) Appeal to Emotion (II) Ambiguity (c) Complex Question (III) Defective Induction (d) Fallacy of Composition (IV) Presumption",
     "options":["(a)-(IV), (b)-(II), (c)-(III), (d)-(I)", "(a)-(III), (b)-(I), (c)-(IV), (d)-(II)", "(a)-(III), (b)-(IV), (c)-(I), (d)-(II)", "(a)-(II), (b)-(I), (c)-(IV), (d)-(III)"],
     "correct_answer":"(a)-(III), (b)-(I), (c)-(IV), (d)-(II)",
     "explanation":"The correct answer is (B) (a)-(III), (b)-(I), (c)-(IV), (d)-(II). This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea145","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"\"This piece of Chalk has mass, therefore, the atoms that compose this piece of chalk have mass.\" Which of the following options is true of the above argument?",
     "options":["Fallacy of composition is committed here", "Slippery slope is involved here", "Hasty Generalization is committed here", "It is a non-fallacious argument"],
     "correct_answer":"It is a non-fallacious argument",
     "explanation":"The correct answer is (D) It is a non-fallacious argument. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea146","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"In an information society, even nuclear families have the characteristic of technological",
     "options":["Separation", "Mediation", "Constriction", "Passivity"],
     "correct_answer":"Mediation",
     "explanation":"The correct answer is (B) Mediation. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea147","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match the List-I with List-II List - I (Statement) List - II (Result) (a) Average of the squares of first 10 natural numbers (I) 13 (b) Average of first 5 multiplies of 5 (II) 45 (c) Average of first 25 natural numbers (III) 38.5 (d) Average of cubes of first 5 natural numbers (IV) 15",
     "options":["(a)-(I), (b)-(II), (c)-(III), (d)-(IV)", "(a)-(II), (b)-(III), (c)-(IV), (d)-(I)", "(a)-(IV), (b)-(I), (c)-(II), (d)-(III)", "(a)-(III), (b)-(IV), (c)-(I), (d)-(II)"],
     "correct_answer":"(a)-(III), (b)-(IV), (c)-(I), (d)-(II)",
     "explanation":"The correct answer is (D) (a)-(III), (b)-(IV), (c)-(I), (d)-(II). This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea148","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"According to UGC Regulations 2018 on Plagiarism, which of the following percentage of similarity in the thesis would result in the cancellation of a student's registration in the programme he/she is registered in?",
     "options":["42%", "53%", "58%", "61%"],
     "correct_answer":"61%",
     "explanation":"The correct answer is (D) 61%. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea149","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"According to Nyāya logic which of the following statements is fallacious because the middle term instead of proving the existence of the major term in the minor term, it proves its non- existence therein.",
     "options":["Sound is eternal because it is produced", "The hill has fire because it is knowable", "Sound is eternal because it is audible", "All things are non-eternal because they are knowable"],
     "correct_answer":"Sound is eternal because it is produced",
     "explanation":"The correct answer is (A) Sound is eternal because it is produced. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea150","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"Find the number that can be inserted at the place of questions mark (?) in the series given below. 4, 10, 20, 34, 52, 74, ?",
     "options":["98", "102", "97", "100"],
     "correct_answer":"100",
     "explanation":"The correct answer is (D) 100. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea151","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"who discussed the famine in detail and considered it an ideological crime?",
     "options":["Karl Marx", "Amartya Sen", "Noam Chomsky", "T. S Eliot"],
     "correct_answer":"Amartya Sen",
     "explanation":"The correct answer is (B) Amartya Sen. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea152","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"For all the six given years, the difference between the average number of employees working in office-D and office-E is",
     "options":["74", "66", "72", "70"],
     "correct_answer":"74",
     "explanation":"The correct answer is (A) 74. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea153","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"In office-F, the percentage increase in the number of employees in comparison to previous year is more than 6% for exactly _________ years(s)",
     "options":["1", "2", "3", "4"],
     "correct_answer":"2",
     "explanation":"The correct answer is (B) 2. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea154","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"In the years 2018 and 2019, the ratio between the number of employees working in all the six offices together is",
     "options":["13:11", "13:14", "37:36", "4:3"],
     "correct_answer":"37:36",
     "explanation":"The correct answer is (C) 37:36. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea155","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"For all the six given years, what is the ratio of total number of employees working in Office-A to that in office-B?",
     "options":["2:1", "41:26", "19:11", "11:19"],
     "correct_answer":"41:26",
     "explanation":"The correct answer is (B) 41:26. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea156","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"Find the missing term in the series given below: 1, 7, 25, 61, 121, ?, 337",
     "options":["205", "211", "209", "208"],
     "correct_answer":"211",
     "explanation":"The correct answer is (B) 211. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea157","topic":"Reasoning","difficulty":"Hard","year":2024,"season":"June",
     "question":"What is the correct sequence of Risk assessment for environment contaminants? (a) Exposure Assessment 163 (b) Dose Response Assessment (c) Risk Assessment (d) Hazard Identification (e) Risk Characterization",
     "options":["(d), (a), (b), (e), (c)", "(d), (a), (b), (c), (e)", "(c), (e), (d), (b), (a)", "(e), (c), (b), (a), (d)"],
     "correct_answer":"(d), (a), (b), (e), (c)",
     "explanation":"The correct answer is (A) (d), (a), (b), (e), (c). This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea158","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which of the following is a software that locks data files and demands a monetary payment in exchange for unlocking?",
     "options":["Ransomware", "Spyware", "Logic Bomb", "Trojan Horse"],
     "correct_answer":"Ransomware",
     "explanation":"The correct answer is (A) Ransomware. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea159","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"\"Either we forcibly sterilize the third world people or the world population will explode and all of us will die. We certainly don't want to die, therefore we must forcibly sterilize the third world people.\" Which informal fallacy is committed in the above argument?",
     "options":["Hasty generalization", "Slippery slope", "False Dichotomy", "Ad hominem"],
     "correct_answer":"False Dichotomy",
     "explanation":"The correct answer is (C) False Dichotomy. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea160","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match the List-I with List-II List - I (Member as per Nyāya syllogism) List - II (Statement) (a) Upanaya (I) Whoever is man is a mortal just like Pythagoras (b) Nigamana (II) Socrates is mortal (c) Udāharana (III) Socrates is a man who is invariably a mortal (d) Pratijnā (IV) Therefore Socrates is mortal",
     "options":["(a)-(II), (b)-(IV), (c)-(I), (d)-(III)", "(a)-(III), (b)-(IV), (c)-(I), (d)-(II)", "(a)-(III), (b)-(I), (c)-(IV), (d)-(II)", "(a)-(III), (b)-(II), (c)-(IV), (d)-(I)"],
     "correct_answer":"(a)-(III), (b)-(IV), (c)-(I), (d)-(II)",
     "explanation":"The correct answer is (B) (a)-(III), (b)-(IV), (c)-(I), (d)-(II). This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea161","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which of the following has the highest Biological Oxygen Demand (BOD)",
     "options":["Potable water", "Unpolluted surface water", "Contaminated surface water", "Municipal Sewage Effluent"],
     "correct_answer":"Municipal Sewage Effluent",
     "explanation":"The correct answer is (D) Municipal Sewage Effluent. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea162","topic":"Reasoning","difficulty":"Hard","year":2024,"season":"June",
     "question":"Which of the following statements are true? (a) Propositions or statements can be true or false. (b) Propositions can be valid or invalid. (c) A valid argument must contain only true premises. (d) A valid argument must have a true conclusion. (e) In a valid argument, if its premises are true, the conclusion cannot be false.",
     "options":["(a) and (e) only", "(c), (d) and (e) only", "(d) and (e) only", "(a), (b), (c) and (d) only"],
     "correct_answer":"(a) and (e) only",
     "explanation":"The correct answer is (A) (a) and (e) only. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea163","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"Find out the chronological order of the following British Authorities/Persons who took interest in higher education in India. (a) Lord Curzon (b) Lord Ripon (c) Lord Canning (d) Lord Dalhousis",
     "options":["(a), (b), (c), (d)", "(b), (d), (a), (c)", "(d), (c), (b), (a)", "(c), (d), (a), (b)"],
     "correct_answer":"(d), (c), (b), (a)",
     "explanation":"The correct answer is (C) (d), (c), (b), (a). This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea164","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"Which of the following is/are true? (a) The average of given data is less than the greatest observation and greater than the smallest observation of the given data. (b) If the observations of a given data are equal, then the average of the data may or may not be same as the observations. (c) If all the observations of a given data get increased by x, then their average is also increased by x. (d) If all the observations of a given data are divided by x, then their average may or may not 169 change.",
     "options":["(a), (b), (c) only", "(b), (c), (d) only", "(a), (c) only", "(d) only"],
     "correct_answer":"(a), (c) only",
     "explanation":"The correct answer is (C) (a), (c) only. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea165","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which of the following fallacious arguments involves unproved middle term as per Nyāya logic?",
     "options":["Sound is eternal because it is produced.", "Fire is cold because it is a substance.", "The sky- lotus is fragrant, because it is a lotus, like the lotus of a lake.", "The hill has fire because it is knowable."],
     "correct_answer":"The sky- lotus is fragrant, because it is a lotus, like the lotus of a lake.",
     "explanation":"The correct answer is (C) The sky- lotus is fragrant, because it is a lotus, like the lotus of a lake.. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea166","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"In a certain languages: \"Sun rises in the East\" is coded as \"ST SR SI SH SS\" \"Sun sets in the West\" is coded as \"ST SE SI SH SU\" \"Your house faces East\" is coded as: \"SN SM SA SS\" 170 \"His house faces West\" is coded as: \"SC SM SA SU\" How the words \"East\", and \"West\" are coded in this languages respectively?",
     "options":["SR, SE", "SS, SN", "SS, SU", "SN, SC"],
     "correct_answer":"SS, SU",
     "explanation":"The correct answer is (C) SS, SU. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea167","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"What is the percentage of male in tier I cities who consume tobacco according to the 'Human – Centric Approach to Tobacco Control' report?",
     "options":["62%", "40%", "50%", "80%"],
     "correct_answer":"62%",
     "explanation":"The correct answer is (A) 62%. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea168","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"What is the ratio of the number of visitors to Manali on Wednesday to the number of visitors to Kullu on Thursday?",
     "options":["9:2", "4:3", "2:9", "3:4"],
     "correct_answer":"9:2",
     "explanation":"The correct answer is (A) 9:2. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea169","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"What is the average number of visitors to Manali on all the days except Monday?",
     "options":["560", "520", "490", "450"],
     "correct_answer":"450",
     "explanation":"The correct answer is (D) 450. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea170","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"The average number of visitors to Kullu on Monday and Thursday is _________ % less than the number of visitors to Manali on Wednesday.",
     "options":["53.29", "63.89", "67.44", "50.28"],
     "correct_answer":"63.89",
     "explanation":"The correct answer is (B) 63.89. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea171","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"An instrument used in structured observation that mentions the categories of behaviour to be observed is known as.",
     "options":["Category schedule", "Observation device", "Observation schedule", "Ontological tool"],
     "correct_answer":"Observation schedule",
     "explanation":"The correct answer is (C) Observation schedule. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea172","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"Which of the following statements are logically equivalent? (a) All cats are carnivorous animals (b) All non-carnivorous animals are non-cats (c) No cats are non-carnivorous animals (d) Some carnivorous animals are cats",
     "options":["(a), (b) and (c) only", "(b), (c) and (d) only", "(a), (c) and (d) only", "(c) and (d) only"],
     "correct_answer":"(a), (b) and (c) only",
     "explanation":"The correct answer is (A) (a), (b) and (c) only. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea173","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"What number would replace question mark (?) in the series given below? 1, 7, 16, 28, 43, 61, 82, ?",
     "options":["102", "143", "106", "110"],
     "correct_answer":"106",
     "explanation":"The correct answer is (C) 106. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea174","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"As per classical Indian school of logic (Nyāya) which of the following fallacy is committed when the middle term is too wide?",
     "options":["Anupasamhāri", "Bādhita", "Sādhārana", "Asādhārana"],
     "correct_answer":"Sādhārana",
     "explanation":"The correct answer is (C) Sādhārana. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea175","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"Two persons X and Y invested ₹ 15,000 and ₹ 20,000, respectively, in a business. At the end of the year, they share the profit in the ratio of 3:1. If X has invested his money for the whole year, for how many months Y has invested his money?",
     "options":["3", "6", "5", "4"],
     "correct_answer":"3",
     "explanation":"The correct answer is (A) 3. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea176","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"In a certain code language A is coded as Z, B is coded as Y, C is coded as X, and so on. How 'PERFECT’ will be coded in that language?",
     "options":["KVIUVXG", "KVIVUXG", "KVIUVGX", "KVUIVXG"],
     "correct_answer":"KVIUVXG",
     "explanation":"The correct answer is (A) KVIUVXG. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea177","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"In an examination, average marks of six students is 50. However, during cross checking of the papers, it is found that the marks of one student has been misread as 48 instead of 84. Find the correct average marks of the students.",
     "options":["52", "54", "56", "58"],
     "correct_answer":"56",
     "explanation":"The correct answer is (C) 56. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea178","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"Which informal fallacy is committed in the following statement \"Famous actor Jimmy Pecker has said in an interview that astrology is a real science, therefore scientists now must acknowledge that astrology is actually a science.\"?",
     "options":["Appeal to Inappropriate authority", "Red herring", "Strawman", "Appeal to Ignorance"],
     "correct_answer":"Appeal to Inappropriate authority",
     "explanation":"The correct answer is (A) Appeal to Inappropriate authority. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea179","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"If the ratio of the number of items sold by B and C together on Thursday to the number of items sold by C and E together on the same day is 2:1, then the number of items sold by C on Thursday is:",
     "options":["300", "420", "380", "340"],
     "correct_answer":"380",
     "explanation":"The correct answer is (C) 380. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea180","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"If the average number of items sold by D on Monday and Tuesday is 490, then the number of items sold by E on Friday is _________% more than the number of items sold by D on Monday.",
     "options":["39.76", "42.86", "48.23", "45"],
     "correct_answer":"42.86",
     "explanation":"The correct answer is (B) 42.86. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea181","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"\"A line is composed of points. Points have no length. Therefore a line has no length.\" Which informal fallacy is committed in this statement?",
     "options":["Fallacy of composition", "Equivocation", "Hasty generalisation", "Slippery slope"],
     "correct_answer":"Fallacy of composition",
     "explanation":"The correct answer is (A) Fallacy of composition. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea182","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"What was National Knowledge Commission's recommendations for minimum gross enrollment ratio to be achieved in higher education by 2015?",
     "options":["5 percent", "10 percent", "15 percent", "20 percent"],
     "correct_answer":"15 percent",
     "explanation":"The correct answer is (C) 15 percent. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea183","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"There are three positive numbers. One third of the average of all the three numbers is 8 less than the value of the highest number. If the average of the lowest and the second lowest number is 8, then what is the highest number?",
     "options":["9", "10", "11", "12"],
     "correct_answer":"11",
     "explanation":"The correct answer is (C) 11. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea184","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"What will be the value of P in the following number series? 0, 3, 26, 255, P, . . . . . . . .",
     "options":["624", "511", "1023", "3124"],
     "correct_answer":"3124",
     "explanation":"The correct answer is (D) 3124. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea185","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"A school boy, travelling at 3 km/hr, reaches his school 28 minutes late but when he travels at 5 km/hr, he reachers his school 28 minutes early. What distance does he travel every day to reach the school?",
     "options":["6 km", "8 km", "7 km", "9 km"],
     "correct_answer":"7 km",
     "explanation":"The correct answer is (C) 7 km. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea186","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"‘Code numbers given to the religion of persons’ is an example of data on which of the following scales of measurement?",
     "options":["nominal", "ordinal", "interval", "ratio"],
     "correct_answer":"nominal",
     "explanation":"The correct answer is (A) nominal. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea187","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which of the following statement is logically equivalent to the statement - \"No liquids are beverages.\"?",
     "options":["All non-bevarages are non-liquids", "All liquids are non-beverages.", "Some beverages are not liquids", "No beverages are liquids"],
     "correct_answer":"All liquids are non-beverages.",
     "explanation":"The correct answer is (B) All liquids are non-beverages.. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea188","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"In a school, there were 1582 students and the ratio of the number of the boys and girls was 4:3. After few days, 30 girls joined the school but few boys left the school and as a result, the ratio of the boys and girls became 7:6. The number of boys who left the school is?",
     "options":["84", "74", "86", "78"],
     "correct_answer":"78",
     "explanation":"The correct answer is (D) 78. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea189","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"According to Classical Indian School of Logic (Nyaതya) the argument - \"Sound is eternal because it is produced\" is fallacious because:",
     "options":["The middle term instead of being pervaded by the presence of major term is pervaded by its", "The locus of the middle term is impossible.", "The middle term instead of being pervaded by the absence of major term is pervaded by its", "It lacks any major term."],
     "correct_answer":"The middle term instead of being pervaded by the presence of major term is pervaded by its",
     "explanation":"The correct answer is (A) The middle term instead of being pervaded by the presence of major term is pervaded by its. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea190","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"Which of the following facts about Myclination are correct? (a) It increases the speed at which information trevels through the nervous system. (b) It is responsible for increase in size of the brain. (c) It is completed in all areas of the brain by age four. (d) Knowledge about it dies not benefit us in any way.",
     "options":["(c) and (d) only", "(b), (c) and (d) only", "(a) and (b) only", "(a), (c) and (d) only"],
     "correct_answer":"(a) and (b) only",
     "explanation":"The correct answer is (C) (a) and (b) only. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea193","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"\"If a student gets a part time job in an architect's office and applies what was learnt in geometry class to help the architect analyze a spatial problem that is quite different from any problem the student encountered in geometry class\" is an example of ________learning?",
     "options":["Near transfer", "Forward-reaching transfer", "Low-road transfer", "Far transfer"],
     "correct_answer":"Far transfer",
     "explanation":"The correct answer is (D) Far transfer. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea194","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"'Abhay's mind is a cave, deep, dark and full of bats.\" Which of the following is correct about the above statement?",
     "options":["It contains analogical argument.", "It is a valid and sound argument.", "It contains analogy.", "It is a valid but not a sound argument."],
     "correct_answer":"It contains analogy.",
     "explanation":"The correct answer is (C) It contains analogy.. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea195","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"Three positive numbers are in the ratio 2: 3: 4. If the sum of their squares is 2349, then the numbers respectively are 197",
     "options":["14, 21 and 28", "18, 27 and 36", "16, 24 and 32", "12, 18 and 24"],
     "correct_answer":"18, 27 and 36",
     "explanation":"The correct answer is (B) 18, 27 and 36. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea196","topic":"Reasoning","difficulty":"Hard","year":2024,"season":"June",
     "question":"Softening of hard water is done by (a) Aeration (b) Boiling (c) Lime soda (d) Ozonation (e) Ion exchange",
     "options":["(a), (b) and (c) only", "(b), (c) and (e) only", "(b), (c) and (d) only", "(c), (d) and (e) only"],
     "correct_answer":"(b), (c) and (e) only",
     "explanation":"The correct answer is (B) (b), (c) and (e) only. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea197","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"Let L and M be the sum and average of four consecutive odd numbers (a, b, c and d) respectively, and, P and Q be the sum and average of three consecutive even numbers (x, y and z) respectively. If M = Q – 6 and P = L – 16, then M =",
     "options":["32", "34", "36", "30"],
     "correct_answer":"34",
     "explanation":"The correct answer is (B) 34. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea198","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"Identify correct statements about content analysis. (a) The main use of content analysis has been in the examination of printed texts and documents. (b) Content analysis lacks transparency. (c) Coding is crucial in content analysis. (d) It is almost impossible to devise coding manuals that do not entail some interpretation on the part of coders.",
     "options":["(a), (b) and (c) only", "(b), (c) and (d) only", "(a), (c) and (d) only", "(a), (b) and (d) Only"],
     "correct_answer":"(a), (c) and (d) only",
     "explanation":"The correct answer is (C) (a), (c) and (d) only. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea199","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"According to classical Indian School of Logic (Nyāya) the statement \"fire is cold because it is a substance\" is fallacious because:",
     "options":["It has a non-inferentially contradicted middle term.", "The middle term has an impossible locus.", "The middle term instead of proving its presence in major term proves its absence.", "The major term proves its presence"],
     "correct_answer":"It has a non-inferentially contradicted middle term.",
     "explanation":"The correct answer is (A) It has a non-inferentially contradicted middle term.. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea200","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"In a certain coding scheme the word 'SCHOLAR' is coded as 'TEKSQGY'. In the same coding scheme, the word 'GREEN' will be coded as",
     "options":["ITGGP", "HTHIS", "EPCGP", "JUHHQ"],
     "correct_answer":"HTHIS",
     "explanation":"The correct answer is (B) HTHIS. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea201","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which of the following tool is used to create pre and post-session polls to gauge students learning from each session?",
     "options":["Mentimeter", "Github", "Plotagon", "Labster"],
     "correct_answer":"Mentimeter",
     "explanation":"The correct answer is (A) Mentimeter. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea202","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"In any conventional media, the point of content production and the point of consumption involve",
     "options":["Temporal separation", "Imaginary hurdles", "Free marketing", "Technological over-dependence"],
     "correct_answer":"Temporal separation",
     "explanation":"The correct answer is (A) Temporal separation. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea203","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"Which of the following statements are logically equivalent? (a) Some beverages are not liquids. (b) Some beverages are liquids. (c) Some non-liquids are not non-beverages. (d) Some beverages are non-liquids.",
     "options":["(a) and (b) only", "(b), (c) and (d) only", "(b) and (c) only", "(a), (c) and (d) only"],
     "correct_answer":"(a), (c) and (d) only",
     "explanation":"The correct answer is (D) (a), (c) and (d) only. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea204","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"In what time will a sum of money double itself at the rate of 12.5% per annum simple interest?",
     "options":["10 years", "8 years", "6 years", "12 years"],
     "correct_answer":"8 years",
     "explanation":"The correct answer is (B) 8 years. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea205","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"If a person travels in a car at a speed of 36 km/hour, then he will reach his destination on time. He covers half the journey in (4/5)th time. What should be his speed for the remaining part of the journey so that he reaches his destination on time?",
     "options":["80 km/hour", "75 km/hour", "90 km/hour", "85 km/hour"],
     "correct_answer":"90 km/hour",
     "explanation":"The correct answer is (C) 90 km/hour. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea206","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"I have read that one aspirin taken everyday reduces the risk of heart attack. Why not take two a day and double the protection.\" Which informal fallacy is committed in the above statement?",
     "options":["Fallacy of composition", "Begging the question", "Hasty generalisation", "Slippery slope"],
     "correct_answer":"Fallacy of composition",
     "explanation":"The correct answer is (A) Fallacy of composition. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea207","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which of the following statement is incorrect?",
     "options":["Culture is static", "All cultures have developed their ethical norms and principles over time", "Rational people of goodwill exist in all cultures", "Culture is dynamic"],
     "correct_answer":"Culture is static",
     "explanation":"The correct answer is (A) Culture is static. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea208","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"In 2021-2022, if the income of PSU Banks is twice the expenditure of Foreign Banks, then in 2022- 2023, what will be the ratio of income of PSU Banks to the expenditure of Foreign Banks?",
     "options":["1:2", "78:37", "75:29", "2:1"],
     "correct_answer":"78:37",
     "explanation":"The correct answer is (B) 78:37. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea209","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"In 2021-2022, if the income of Foreign Banks is four times its expenditure, then what will be the approximate ratio of income to the expenditure of foreign Banks in 2022-2023?",
     "options":["1:4", "4:1", "5:1", "1:5"],
     "correct_answer":"4:1",
     "explanation":"The correct answer is (B) 4:1. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea210","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"40 people consume 320 kg of rice in 50 days. In how many days will 30 people consume 80 kg of rice?",
     "options":["18", "16", "17", "16"],
     "correct_answer":"16",
     "explanation":"The correct answer is (B) 16. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea211","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"In a certain coding language, the word 'GREAT' is coded as 'ETCCR', then the word 'FROWN' will be coded as:",
     "options":["DTMYL", "ETNWL", "HTQYP", "DSOXL"],
     "correct_answer":"DTMYL",
     "explanation":"The correct answer is (A) DTMYL. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea212","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"If the selling price of Rs. 623 results in a discount of 11% on the market price of an item, at what price should the item be sold to offer a discount of 19%?",
     "options":["Rs. 557", "Rs. 567", "Rs. 577", "Rs. 587"],
     "correct_answer":"Rs. 567",
     "explanation":"The correct answer is (B) Rs. 567. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea213","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"According to Nyāya (Classical school of logic) which of the following step of inference corresponds to Upanaya?",
     "options":["The hill has fire", "Because it has smoke", "What ever has smoke has fire, e.g. an oven", "The hill has smoke which is invariably associated with fire"],
     "correct_answer":"The hill has smoke which is invariably associated with fire",
     "explanation":"The correct answer is (D) The hill has smoke which is invariably associated with fire. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea214","topic":"Reasoning","difficulty":"Hard","year":2024,"season":"June",
     "question":"Identify the sequence of words A-E that correctly fills the blanks in the following paragraph: _________ is used to connect the smartwatch and wireless headphone to the phone and is a ________ range wireless technology. ________ is used to connect the phone and the laptop to the outside world called the \"Internet\" and it uses radio waves to allow high-speed data transfer over short distances. ________ is used to connect the phone to countless services via the \"Internet\" and is a _________ range wireless technology. (a) Short (b) Long (c) Wifi (d) 3G/4G/5G (e) Bluetooth",
     "options":["(e), (a), (c), (d), (b)", "(b), (a), (c), (d), (e)", "(a), (e), (b), (c), (d)", "(e), (c), (a), (b), (d)"],
     "correct_answer":"(e), (a), (c), (d), (b)",
     "explanation":"The correct answer is (A) (e), (a), (c), (d), (b). This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea215","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"\"Of course, abortion has to be legal. After all, a woman must have freedom to do whatever she wants with her own body\". Identify the fallacy committed in this statement:",
     "options":["Fallacy of composition", "Complex question", "Begging the question", "Hasty generalization"],
     "correct_answer":"Begging the question",
     "explanation":"The correct answer is (C) Begging the question. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea216","topic":"Reasoning","difficulty":"Hard","year":2024,"season":"June",
     "question":"Which of the following are part of narration? (a) A sequence of a beginning, middle and end (b) Causal development between sequences and the conclusion (c) Memorable phrases indicating what happened (d) Absence of spatial context (e) Exclusion of temporal factor",
     "options":["(a), (b), (c) only", "(b), (c), (d) only", "(d), (e) only", "(a), (c), (e) only"],
     "correct_answer":"(a), (b), (c) only",
     "explanation":"The correct answer is (A) (a), (b), (c) only. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea217","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"Which of the following statements is true?",
     "options":["In a valid argument all of its premises have to be true", "Validity can be attributed to any single proposition by itself", "Truth and falsehood are attributes of single propositions", "Truth and falsehood can be attributed to arguments"],
     "correct_answer":"Truth and falsehood are attributes of single propositions",
     "explanation":"The correct answer is (C) Truth and falsehood are attributes of single propositions. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea218","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"Which of the following statements are logically equivalent? (a) No Carnivores are Cats. (b) Some Carnivores are not Cats. (c) All Cats are Carnivores (d) All non-carnivores are non-cats",
     "options":["(c) and (d) only", "(a) and (d) only", "(a) and (b) only", "(b) and (d) only"],
     "correct_answer":"(c) and (d) only",
     "explanation":"The correct answer is (A) (c) and (d) only. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea219","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"Find the next number in the number series: 48, 24, 72, 36, 108,?",
     "options":["115", "121", "110", "54"],
     "correct_answer":"54",
     "explanation":"The correct answer is (D) 54. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea220","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"Travelling in a train, a man notices 13 telephone poles in two minutes. If the two successive telephone poles are known to be 125 m a part, then the train is travelling at a speed of:",
     "options":["40 km/hr", "42 km/hr", "45 km/hr", "48 km/hr"],
     "correct_answer":"45 km/hr",
     "explanation":"The correct answer is (C) 45 km/hr. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea221","topic":"Reasoning","difficulty":"Hard","year":2024,"season":"June",
     "question":"List the following developments in a chronological sequence: (a) Invention of television remote controls (b) Publication of diurnals (c) Invention of camera (d) Arrival of mass market paperbacks (e) Origin of hieroglyptic writing system",
     "options":["(a), (c), (e), (d), (b)", "(b), (d), (c), (e), (a)", "(c), (e), (d), (a), (b)", "(e), (b), (c), (d), (a)"],
     "correct_answer":"(e), (b), (c), (d), (a)",
     "explanation":"The correct answer is (D) (e), (b), (c), (d), (a). This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea222","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"How do human activities like paving the roads and parking lots influence floods?",
     "options":["They reduce the severity of floods", "They speed up the rate of run off into streams and lakes", "They decrease the volume of water discharge after a storm", "They have no influence on floods"],
     "correct_answer":"They speed up the rate of run off into streams and lakes",
     "explanation":"The correct answer is (B) They speed up the rate of run off into streams and lakes. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea223","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"Which of the following statements are logically equivalent? (a) Some non-dogs are non-friendly animals (b) Some dogs are friendly animals (c) Some friendly animals are dogs (d) All dogs are friendly animals 217",
     "options":["(b) and (c) Only", "(b) and (d) Only", "(a), (b) and (c) Only", "(a) and (d) Only"],
     "correct_answer":"(b) and (c) Only",
     "explanation":"The correct answer is (A) (b) and (c) Only. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea224","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which of the following arguments is fallacious because of the middle term being too narrow?",
     "options":["All things are non-eternal because they are knowable", "Sound is eternal, because it is audible", "Fire is cold because it is substance", "Wherever there is fire, there is smoke"],
     "correct_answer":"Sound is eternal, because it is audible",
     "explanation":"The correct answer is (B) Sound is eternal, because it is audible. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea225","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"If the selling price of ₹ 276 results in a discount of 8% on the marked price of an item, at what price should the item be sold to offer a discount of 13%?",
     "options":["₹ 265", "₹ 251", "₹ 257", "₹ 261"],
     "correct_answer":"₹ 261",
     "explanation":"The correct answer is (D) ₹ 261. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea226","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"Find out the wrong term from the given series: 125, 126, 124, 127, 123, 129",
     "options":["126", "124", "123", "129"],
     "correct_answer":"129",
     "explanation":"The correct answer is (D) 129. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea227","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"In a certain coding language, the word 'TRAIN' is coded as 'VPCGP', then the word 'PROUD' will be coded as:",
     "options":["QSPVE", "RPQSF", "RQPTF", "RQQSE"],
     "correct_answer":"RPQSF",
     "explanation":"The correct answer is (B) RPQSF. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea228","topic":"Reasoning","difficulty":"Hard","year":2024,"season":"June",
     "question":"Which of the following are consequences of Global Warming? (a) Change in Hydrological Cycle (b) Species Migration (c) Change in Ocean Circulation (d) Ocean Acidification (e) Sea level rise",
     "options":["(a), (b) and (e) Only", "(a), (c) and (d) Only", "(b), (c) and (d) Only", "(a), (b), (c), (d) and (e)"],
     "correct_answer":"(a), (b), (c), (d) and (e)",
     "explanation":"The correct answer is (D) (a), (b), (c), (d) and (e). This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea229","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which fallacy is committed in the following argument-\"Ambassador cars have almost disappeared. This is an ambassador car. Therefore, this car has almost disappeared\":",
     "options":["Equivocation", "Fallacy of Division", "Hasty Generalization", "Slippery Slope"],
     "correct_answer":"Fallacy of Division",
     "explanation":"The correct answer is (B) Fallacy of Division. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea230","topic":"Reasoning","difficulty":"Hard","year":2024,"season":"June",
     "question":"Which of the following are advantages of e-commerce for consumers? (a) They save time by visiting websites instead of stores. (b) They have little risk of having their credit card number intercepted. (c) They can choose goods from any vendor in the world. (d) They can shop no matter their location, time, or conditions.",
     "options":["(a) and (d) Only", "(b) and (c) Only", "(a), (c) and (d) Only", "(a), (b), (c) and (d)"],
     "correct_answer":"(a), (c) and (d) Only",
     "explanation":"The correct answer is (C) (a), (c) and (d) Only. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea231","topic":"Reasoning","difficulty":"Hard","year":2024,"season":"June",
     "question":"The New Education Policy of 2020, suggested degree courses in: (a) Development Communication (b) Logic (c) Art and Museum Administration (d) Graphic Design (e) Web Design",
     "options":["(a), (b) and (c) Only", "(b), (c) and (d) Only", "(c), (d) and (e) Only", "(b), (d) and (e) Only"],
     "correct_answer":"(c), (d) and (e) Only",
     "explanation":"The correct answer is (C) (c), (d) and (e) Only. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea232","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"The market share of companies in 2023 is same as in 2020. In 2024, the ice-cream sale increases by 10% but the market share of Amul falls to 23%. What is the percentage change in the turnover of Amul from 2023 to 2024?",
     "options":["9.64% increase", "9.64% decrease", "17.86% increase", "17.86% decrease"],
     "correct_answer":"9.64% decrease",
     "explanation":"The correct answer is (B) 9.64% decrease. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea233","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"If the percentage market share of companies remains the same in 2021 as that in 2020, then what is the increase/decrease in the turnover of Amul from 2020 to 2021?",
     "options":["₹ 175 crore increase", "₹ 140 crore decrease", "₹ 175 crore decrease", "₹ 140 crore increase"],
     "correct_answer":"₹ 140 crore decrease",
     "explanation":"The correct answer is (B) ₹ 140 crore decrease. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea234","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"What is the average annual rate of increase in the Ice-Cream sale in 2023 in comparison to the year 2018?",
     "options":["5.33%", "26.67%", "6.67%", "10%"],
     "correct_answer":"5.33%",
     "explanation":"The correct answer is (A) 5.33%. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea235","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"A person travels from X to Y at a speed of 30 km/hr and returns from Y to X by increasing his speed by 50%. His average speed during the journey is:",
     "options":["37.5 km/hr", "37 km/hr", "36 km/hr", "38 km/hr"],
     "correct_answer":"36 km/hr",
     "explanation":"The correct answer is (C) 36 km/hr. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea236","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"Which of the following statements are logically equivalent? (a) All cows are herbivores. (b) All herbivores are cows. (c) Some herbivores are cows. (d) No cows are non-herbivores.",
     "options":["(a) and (b) Only", "(b) and (d) Only", "(b) and (c) Only", "(a) and (d) Only"],
     "correct_answer":"(a) and (d) Only",
     "explanation":"The correct answer is (D) (a) and (d) Only. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea237","topic":"Reasoning","difficulty":"Hard","year":2024,"season":"June",
     "question":"Which of the following are true about Pyrolysis? (a) It produces less air pollution than complete incineration. (b) It is done in the presence of oxygen. (c) Instead of oxidation a complex series of decomposition and other chemical reactions take place. (d) Pyrolysis many times generates useful materials. (e) Pyrolysis is a high temperature thermal process, an alternative to incineration.",
     "options":["(a), (b), (c) and (d) Only", "(a), (c), (d) and (e) Only", "(b), (c), (d) and (e) Only", "(a), (b) and (e) Only"],
     "correct_answer":"(a), (c), (d) and (e) Only",
     "explanation":"The correct answer is (B) (a), (c), (d) and (e) Only. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea238","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"Find the next term in the series..... 2Z5, 7Y7, 14X9, 23W11, 34V13, (?) 229",
     "options":["27U24", "45U15", "47U15", "47U14"],
     "correct_answer":"47U15",
     "explanation":"The correct answer is (C) 47U15. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea239","topic":"Reasoning","difficulty":"Hard","year":2024,"season":"June",
     "question":"Identify the correct chronological sequence of the following: (a) Launch of Twitter (b) Launch of Facebook (c) Appearance of social network sites (d) Launch of Sputnik (e) 'War of the worlds' broadcast",
     "options":["(a), (c), (b), (e), (d)", "(e), (d), (c), (b), (a)", "(b), (e), (d), (a), (c)", "(c), (b), (a), (d), (e)"],
     "correct_answer":"(e), (d), (c), (b), (a)",
     "explanation":"The correct answer is (B) (e), (d), (c), (b), (a). This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea240","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"Identify the fallacy committed in the statement given below: \"People who lack arrogance are intelligent because intelligent people do not have arrogance\"",
     "options":["Equivocation", "Fallacy of division", "Begging the question", "Fallacy of composition"],
     "correct_answer":"Begging the question",
     "explanation":"The correct answer is (C) Begging the question. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea241","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"Three successive discounts of 15%, 20% and 40% on the marked price of an item are equivalent to a single discount of:",
     "options":["75%", "40.8%", "59.2%", "67.5%"],
     "correct_answer":"59.2%",
     "explanation":"The correct answer is (C) 59.2%. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea242","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"In Kyoto protocol, how much target was fixed for the reduction of concentration of Green House Gases (GHGs) below 1990 level, during first commitment period 2008-12 by state parties?",
     "options":["1.0%", "5.2%", "10.4%", "20.0%"],
     "correct_answer":"5.2%",
     "explanation":"The correct answer is (B) 5.2%. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea243","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"In a certain coding language, if the word 'TREND' is coded as 'QUBQA', then the word 'STRAY' will be coded as.",
     "options":["PVPDV", "PWPDW", "PWODV", "QWPEW"],
     "correct_answer":"PWODV",
     "explanation":"The correct answer is (C) PWODV. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea244","topic":"Reasoning","difficulty":"Hard","year":2024,"season":"June",
     "question":"Identify the public sector universities from the following that have the highest number of collaboration with foreign universities. (a) Indian Institute of Technology, Kanpur (b) Indian Institute of Science, Bengaluru (c) Pondicherry University, Pondicherry (d) North-Eastern Hill University, Shillong (e) Gujarat Vidyapeeth, Gujarat",
     "options":["(a), (b), (c) Only", "(b), (c), (d) Only", "(c), (d), (e) Only", "(a), (d), (e) Only"],
     "correct_answer":"(a), (b), (c) Only",
     "explanation":"The correct answer is (A) (a), (b), (c) Only. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea245","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match List - I with List - II. List - I (Computer Terms) List - II (Purpose) (a) Motherboard (I) Stores the date, time and system configuration for BIOS (b) BIOS (II) Allows processor and other hardware to function and communicate with each other (c) CMOS (III) Transfer the contents of web pages into a web browser for viewing (d) HTTP (IV) Initializes and tests the system hardware components and loads an OS when a computer is turned on",
     "options":["(a)-(II), (b)-(I), (c)-(IV), (d)-(III)", "(a)-(III), (b)-(IV), (c)-(I), (d)-(II)", "(a)-(II), (b)-(IV), (c)-(I), (d)-(III)", "(a)-(IV), (b)-(III), (c)-(II), (d)-(I)"],
     "correct_answer":"(a)-(II), (b)-(IV), (c)-(I), (d)-(III)",
     "explanation":"The correct answer is (C) (a)-(II), (b)-(IV), (c)-(I), (d)-(III). This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea246","topic":"Reasoning","difficulty":"Hard","year":2024,"season":"June",
     "question":"Arrange the steps of the cycle of self regulated learning in logical order? (a) Setting goals (b) Regulating learning (c) Enacting Tactics and Strategies (d) Analysing the task (e) Devising plans",
     "options":["(e), (d), (b), (a), (c)", "(b), (c), (e), (d), (a)", "(d), (a), (e), (c), (b)", "(a), (e), (c), (b), (d)"],
     "correct_answer":"(d), (a), (e), (c), (b)",
     "explanation":"The correct answer is (C) (d), (a), (e), (c), (b). This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea247","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"What is the respective ratio between Amit's average monthly income in the year 2016, Anil's average monthly income in the year 2017 and Ajay's average monthly income in the year 2015?",
     "options":["6 : 3 : 5", "5 : 6 : 4", "5 : 4 : 7", "6 : 5 : 3"],
     "correct_answer":"6 : 5 : 3",
     "explanation":"The correct answer is (D) 6 : 5 : 3. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea248","topic":"Reasoning","difficulty":"Hard","year":2024,"season":"June",
     "question":"According to Piaget, our thinking process changes radically, though slowly, from birth to maturity because we constantly strive to make sense of the world. Identify the factors which Piaget indicated that influence changes in thinking. (a) Equilibration (b) Impulsivity (c) Social experiences (d) Activity (e) Biological maturation",
     "options":["(a), (b), (c) and (d) only", "(a), (b), (d) and (e) only", "(a), (c), (d) and (e) only", "(b), (c), (d) and (e) only"],
     "correct_answer":"(a), (c), (d) and (e) only",
     "explanation":"The correct answer is (C) (a), (c), (d) and (e) only. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea249","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"Shiv is 27 times as old as his grand daughter. However, three years later, he will be 14 times as old as his grand daughter. What is the present age of his grand daughter?",
     "options":["7 years", "4 years", "21 years", "3 years"],
     "correct_answer":"3 years",
     "explanation":"The correct answer is (D) 3 years. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea250","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"Solar chimneys can be used for:",
     "options":["Space heating", "Desalination of water", "Generation of electricity", "Refrigeration"],
     "correct_answer":"Generation of electricity",
     "explanation":"The correct answer is (C) Generation of electricity. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea251","topic":"Reasoning","difficulty":"Hard","year":2024,"season":"June",
     "question":"Thermal pollution in river water: (a) Increases the solubility of Oxygen (b) Promotes the growth of certain fish (c) Increases the metabolism of fish (d) May cause elimination of most sponges and mollusks (e) Does not change the ecological balance of river",
     "options":["(a), (b) and (c) only", "(b), (c) and (d) only", "(c), (d) and (e) only", "(a), (b) and (d) only"],
     "correct_answer":"(b), (c) and (d) only",
     "explanation":"The correct answer is (B) (b), (c) and (d) only. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea252","topic":"Reasoning","difficulty":"Medium","year":2024,"season":"June",
     "question":"Which of the following codes correctly represents the figure and mood of the argument? \"Some conservatives are not advocates of high tariff rates, because all advocates of high tariff rates are republicans and some republicans are not conservatives.\"",
     "options":["AOO-IV", "OAO-III", "OOA-II", "OOA-I"],
     "correct_answer":"AOO-IV",
     "explanation":"The correct answer is (A) AOO-IV. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"rea253","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"What number comes next in the following sequences? 3, 3.5, 4.5, 6, ?",
     "options":["8.5", "7", "8", "7.5"],
     "correct_answer":"8",
     "explanation":"The correct answer is (C) 8. This is a standard UGC NET 2024 June question on Reasoning."},
    {"id":"ict1055","topic":"Reasoning","difficulty":"Easy","year":2024,"season":"June",
     "question":"Junagarh is known for beautiful shrines of which of the following combination of religions?",
     "options":["Hinduism, Buddhism, Christianity", "Christianity, Hinduism, Jainism", "Hinduism, Buddhism, Islam", "Islam, Hinduism, Jainism"],
     "correct_answer":"Islam, Hinduism, Jainism",
     "explanation":"The correct answer is (D) Islam, Hinduism, Jainism. This is a standard UGC NET 2024 June question on Teaching Aptitude."},


    # ↑↑↑ PASTE YOUR NEW Reasoning QUESTIONS ABOVE THIS LINE ↑↑↑
]

# ── 6. ICT ───────────────────────────────────────────────────────────
Q_ICT = [
    {"id":"ict001","topic":"ICT","difficulty":"Easy","year":2023,"season":"December","question":"What does 'www' stand for in a web address?","options":["World Wide Web","World Web Works","Wide World Web","Web World Wire"],"correct_answer":"World Wide Web","explanation":"WWW stands for World Wide Web — the information system accessed via the Internet using URLs."},
    {"id":"ict002","topic":"ICT","difficulty":"Medium","year":2022,"season":"June","question":"Which protocol is used to transfer files over the internet?","options":["HTTP","FTP","SMTP","TCP"],"correct_answer":"FTP","explanation":"FTP (File Transfer Protocol) is specifically designed for transferring files between client and server."},
    {"id":"ict003","topic":"ICT","difficulty":"Hard","year":2019,"season":"December","question":"Which generation of computers used transistors?","options":["First generation","Second generation","Third generation","Fourth generation"],"correct_answer":"Second generation","explanation":"Second-generation computers (1956-1963) used transistors, replacing vacuum tubes."},
    {"id":"ict004","topic":"ICT","difficulty":"Hard","year":2018,"season":"June","question":"Moore's Law states transistor count doubles approximately every:","options":["6 months","1 year","2 years","5 years"],"correct_answer":"2 years","explanation":"Gordon Moore observed in 1965 that transistor count doubles roughly every two years."},
    # ════════════════════════════════════════════════════════════════════
    # ADD MORE ICT QUESTIONS BELOW ↓
    # ════════════════════════════════════════════════════════════════════
    {"id":"ict005","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which of the following is an example of open-source software?",
     "options":["Microsoft Word","Adobe Photoshop","Linux","Windows 11"],
     "correct_answer":"Linux",
     "explanation":"Linux is a free, open-source operating system where the source code is publicly available."},

    {"id":"ict006","topic":"ICT","difficulty":"Medium","year":2024,"season":"December",
     "question":"What is the full form of URL?",
     "options":["Universal Resource Locator","Uniform Resource Locator","Unified Record Link","Universal Record Link"],
     "correct_answer":"Uniform Resource Locator",
     "explanation":"URL stands for Uniform Resource Locator — the address used to access resources on the internet."},

    {"id":"ict007","topic":"ICT","difficulty":"Hard","year":2023,"season":"June",
     "question":"Which technology enables multiple operating systems to run on a single physical machine?",
     "options":["Cloud computing","Virtualisation","Distributed computing","Grid computing"],
     "correct_answer":"Virtualisation",
     "explanation":"Virtualisation allows multiple virtual machines, each running its own OS, to run on one physical host."},

    {"id":"ict008","topic":"ICT","difficulty":"Medium","year":2022,"season":"December",
     "question":"DIKSHA platform in India is primarily used for:",
     "options":["Financial transactions","Digital educational content for teachers and students","E-governance","Defence communication"],
     "correct_answer":"Digital educational content for teachers and students",
     "explanation":"DIKSHA (Digital Infrastructure for Knowledge Sharing) is India's national platform for school education."},

    {"id":"ict009","topic":"ICT","difficulty":"Easy","year":2021,"season":"June",
     "question":"RAM stands for:",
     "options":["Read Access Memory","Random Access Memory","Rapid Application Memory","Read Application Memory"],
     "correct_answer":"Random Access Memory",
     "explanation":"RAM (Random Access Memory) is the primary volatile memory used by computers for active processes."},
    
{"id":"ict010","topic":"ICT","difficulty":"Medium","year":2024,"season":"June",
     "question":"If (L)M represents a number L in base-M number system, then which of the following equalities are true? (a) (127.125)10 = (1111111.001)2 (b) (127.125)10 = (1333.02)4 (c) (127.125)10 = (177.1)8 (d) (127.125)10 = (7F.2)16",
     "options":["(a) only", "(a) and (b) only", "(a), (b) and (c) only", "(a), (b), (c) and (d)"],
     "correct_answer":"(a), (b), (c) and (d)",
     "explanation":"The correct answer is (D) (a), (b), (c) and (d). This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict011","topic":"ICT","difficulty":"Medium","year":2024,"season":"June",
     "question":"A history teacher wants to create an interactive timeline showcasing the evolution of different art movements over centuries? Which tool would best support the creation of this multimedia presentation?",
     "options":["Prezi", "Adobe Illustrator", "Flipgrid", "Google forms"],
     "correct_answer":"Prezi",
     "explanation":"The correct answer is (A) Prezi. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict012","topic":"ICT","difficulty":"Hard","year":2024,"season":"June",
     "question":"Identify the sequence of words A-E that correctly fills the blanks in the following paragraph: The __________ is the 'brain' of the computer and the __________ processor made by Intel is an example of this. The speed of the processor is measured in __________. _________ is a volatile memory whereas ___________ is used in most computers to hold a small special piece of software known as the 'boot up' program. (a) ROM (b) CPU (c) RAM (d) Pentium (e) Hertz",
     "options":["(b), (d), (e), (c), (a)", "(d), (b), (c), (e), (a)", "(c), (d), (e), (a), (b)", "(b), (e), (d), (a), (c)"],
     "correct_answer":"(b), (d), (e), (c), (a)",
     "explanation":"The correct answer is (A) (b), (d), (e), (c), (a). This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict013","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which of the following electronic technologies is the key technology for making the first generation electronic computer?",
     "options":["Transistor based", "Integrated Circuit based", "Vacuum Tube based", "Dual Core CPU based"],
     "correct_answer":"Vacuum Tube based",
     "explanation":"The correct answer is (C) Vacuum Tube based. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict014","topic":"ICT","difficulty":"Medium","year":2024,"season":"June",
     "question":"With reference to the open source software, which of the following statements are correct? (a) It is a software that is distributed with its source code. (b) It allows anyone to modify the software to best fit their needs. (c) It is a software that anyone can use on a trial basis before paying for it. (d) Linux is a example of open source software.",
     "options":["(a), (b), and (d) only", "(a), (b), (c) and (d) only", "(a), (c) and (d) only", "(b) and (c) only"],
     "correct_answer":"(a), (b), and (d) only",
     "explanation":"The correct answer is (A) (a), (b), and (d) only. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict015","topic":"ICT","difficulty":"Medium","year":2024,"season":"June",
     "question":"Reena wanted to eat an ice-cream. She took out a phone number online. She repeated the number over and over again while dialing. After order was delivered she forgot the number. This is an example of the use of which memory process?",
     "options":["Short-term memory", "Automatic Processing", "Echoic Memory", "Iconic Memory"],
     "correct_answer":"Short-term memory",
     "explanation":"The correct answer is (A) Short-term memory. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict016","topic":"ICT","difficulty":"Hard","year":2024,"season":"June",
     "question":"Which of the following are the interactive whiteboard softwares that allow teachers to create digital lessons, annotate documents and collaborate with students in real time? (a) Jamboard (b) Camtasia (c) Stormboard (d) Concept board (e) Plotagon",
     "options":["(b) and (c) only", "(a), (c) and (d) only", "(c), (d) and (e) only", "(a), (b) and (e) only"],
     "correct_answer":"(a), (c) and (d) only",
     "explanation":"The correct answer is (B) (a), (c) and (d) only. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict017","topic":"ICT","difficulty":"Hard","year":2024,"season":"June",
     "question":"Identify the sequence of words A-E that correctly fills the blanks in the following paragraph: In the context of human-computer interaction, a _________ is an interface built around visual things and Windows-11 is an example of an __________ with these visual things. _________ is region of the screen used to display information. ___________ is a small picture that is used to represent folders, software etc., whereas __________ is a list of options that the user can select from. (a) OS (b) Menu (c) Window (d) Icon (e) GUI",
     "options":["(e), (a), (c), (b), (d)", "(a), (e), (d), (c), (b)", "(e), (a), (c), (d), (b)", "(b), (c), (a), (e), (d)"],
     "correct_answer":"(e), (a), (c), (d), (b)",
     "explanation":"The correct answer is (C) (e), (a), (c), (d), (b). This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict018","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which of the following would create the most stable computer network with the fastest data transmission?",
     "options":["Use a wireless access point to connect devices", "Connect devices wirelessly using mobile phone", "Use coaxial cables to connect devices in sequence", "Connect devices to a switch using optic fibre cables"],
     "correct_answer":"Connect devices to a switch using optic fibre cables",
     "explanation":"The correct answer is (D) Connect devices to a switch using optic fibre cables. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict019","topic":"ICT","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match the List-I with List-II: List - I (Particulate Matter Terms) List - II (Explanation) (a) Aerosol (I) Particles formed by incomplete combination with mixture of carbon volatiles (b) Nano Particles (II) Particles with size less then 2.5 micro meter (c) Smoke (III) Particles with size less than 0.2 micrometer (d) Fine particles (IV) Any solid or liquid particle suspended in air",
     "options":["(a)-(IV), (b)-(III), (c)-(II), (d)-(I)", "(a)-(IV), (b)-(III), (c)-(I), (d)-(II)", "(a)-(I), (b)-(II), (c)-(IV), (d)-(III)", "(a)-(I), (b)-(II), (c)-(III), (d)-(IV)"],
     "correct_answer":"(a)-(IV), (b)-(III), (c)-(I), (d)-(II)",
     "explanation":"The correct answer is (B) (a)-(IV), (b)-(III), (c)-(I), (d)-(II). This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict020","topic":"ICT","difficulty":"Medium","year":2024,"season":"June",
     "question":"If (L)M represents a number L in base - M number system, then identify the correct descending order of the following number A-D, when converted to base-10 number system. (a) (9C)16 (b) (233)8 (c) (313)7 (d) (10011110)2",
     "options":["(c), (d), (b), (a)", "(d), (c), (a), (b)", "(b), (c), (a), (d)", "(d), (c), (b), (a)"],
     "correct_answer":"(d), (c), (a), (b)",
     "explanation":"The correct answer is (B) (d), (c), (a), (b). This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict021","topic":"ICT","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match List - I with List - II. List -I (MOOCs Quadrant) List -II (Component) (a) Quadrant I (I) e-Tutorial (b) Quadrant II (II) e-Content (c) Quadrant III (III) Web Resources (d) Quadrant IV (IV) Self Assessment",
     "options":["(a)-(I), (b)-(II), (c)-(III), (d)-(IV)", "(a)-(I), (b)-(III), (c)-(II), (d)-(IV)", "(a)-(II), (b)-(IV), (c)-(I), (d)-(III)", "(a)-(IV), (b)-(I), (c)-(III), (d)-(II)"],
     "correct_answer":"(a)-(I), (b)-(II), (c)-(III), (d)-(IV)",
     "explanation":"The correct answer is (A) (a)-(I), (b)-(II), (c)-(III), (d)-(IV). This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict022","topic":"ICT","difficulty":"Medium","year":2024,"season":"June",
     "question":"What are the advantages of using Cloud Computing word processing software? (a) The user does not have to install word processing software on the computer. (b) The user does not have to allocate space to install software in the hard disk. (c) Storage space to save the document is provided by the cloud provider. The user can open or edit the document from any computer which has Internet facility. (d) If the user has slow Internet connection, then he/she would not face any problems accessing or downloading his/her documents.",
     "options":["(a) and (b) Only", "(a) and (c) Only", "(b), (c) and (d) Only", "(a), (b) and (c) Only"],
     "correct_answer":"(a), (b) and (c) Only",
     "explanation":"The correct answer is (D) (a), (b) and (c) Only. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict023","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"Jharkhand has become a favourite destination for visitors from India and abroad because of its:",
     "options":["Stone carving activities", "Mineral wealth", "Natural attractions", "Central location"],
     "correct_answer":"Natural attractions",
     "explanation":"The correct answer is (C) Natural attractions. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict024","topic":"ICT","difficulty":"Medium","year":2024,"season":"June",
     "question":"If (L)M represents a number L in base -M number system, then which of the following equalities are true? (a) (512.125)10 = (1000000000.001)2 (b) (512.125)10 = (1000.1)8 (c) (512.125)10 = (200.2)16 (d) (512.125)10 = (2000.02)4",
     "options":["(a) and (b) only", "(a) and (c) only", "(b), (c) and (d) only", "(a), (b) and (c) only"],
     "correct_answer":"(a), (b) and (c) only",
     "explanation":"The correct answer is (D) (a), (b) and (c) only. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict025","topic":"ICT","difficulty":"Hard","year":2024,"season":"June",
     "question":"Arrange the following Indian States in descending order according to their climate vulnerability (Starting from most vulnerable to least vulnerable) (a) Uttar Pradesh (b) Jharkhand (c) Maharashtra (d) Manipur (e) Punjab",
     "options":["(d), (b), (c), (a), (e)", "(c), (e), (a), (d), (b)", "(b), (a), (d), (e), (c)", "(a), (e), (b), (c), (d)"],
     "correct_answer":"(b), (a), (d), (e), (c)",
     "explanation":"The correct answer is (C) (b), (a), (d), (e), (c). This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict026","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"The Acronym 'SWAYAM' represents-",
     "options":["Scopus Web of Attentive learning for Youth and Apt Minds", "Social Web of Agent learning for Youth and Adult Minds", "Study Webs of Active learning for Young Aspiring Minds", "Science Web of Aspirants and Young Active Minds"],
     "correct_answer":"Study Webs of Active learning for Young Aspiring Minds",
     "explanation":"The correct answer is (C) Study Webs of Active learning for Young Aspiring Minds. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict027","topic":"ICT","difficulty":"Hard","year":2024,"season":"June",
     "question":"Match the List-I with List-II List - I (Myers Briggs Type Learner) List - II (Indicator) (a) Judging learners (I) Depend on outside simulation and interaction for engaging in learning (b) Extrovert learners (II) They choose to decide things impersonally based on analysis, self discipline, logic, prefer clear course and outcomes (c) The intuitors (III) Concerned with knowing the essentials and take actions quickly, intolerant to ambiguity (d) The thinkers (IV) Seek out patterns and relationships among the facts they gather inferences, guesses from context",
     "options":["(a)-(II), (b)-(III), (c)-(I), (d)-(IV)", "(a)-(IV), (b)-(I), (c)-(III), (d)-(II)", "(a)-(III), (b)-(I), (c)-(IV), (d)-(II)", "(a)-(I), (b)-(II), (c)-(III), (d)-(IV)"],
     "correct_answer":"(a)-(III), (b)-(I), (c)-(IV), (d)-(II)",
     "explanation":"The correct answer is (C) (a)-(III), (b)-(I), (c)-(IV), (d)-(II). This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict028","topic":"ICT","difficulty":"Medium","year":2024,"season":"June",
     "question":"A webpage displays the following information, in which underlined word is a link to another webpage. For digital devices, the bandwidth is usually expressed in bits per second (bps). For analog devices, the bandwidth is expressed in Hertz (Hz) Which method of data organisation is being used?",
     "options":["HTML", "Hypertext", "Storyboard", "Data Scheme"],
     "correct_answer":"Hypertext",
     "explanation":"The correct answer is (B) Hypertext. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict029","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which of the following agencies launched the \"International Environmental Education Programme\"?",
     "options":["UNESCO", "UNEP", "IUCN", "GEF"],
     "correct_answer":"UNESCO",
     "explanation":"The correct answer is (A) UNESCO. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict030","topic":"ICT","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match the List-I with List-II List - I (ICT Term) List - II (Description) (a) Authentication (I) Identifies which device is connected at a given IP address (b) Biometrics (II) Relies on certain unique characteristics of human beings such as retina scans (c) IP Address (III) Verifies that data comes from a secure and trusted source and works with encryption to strengthen internet security (d) MAC Address (IV) Identifies where on the network a device is located.",
     "options":["(a)-(I), (b)-(II), (c)-(IV), (d)-(III)", "(a)-(III), (b)-(II), (c)-(IV), (d)-(I)", "(a)-(II), (b)-(III), (c)-(I), (d)-(IV)", "(a)-(IV), (b)-(III), (c)-(II), (d)-(I)"],
     "correct_answer":"(a)-(III), (b)-(II), (c)-(IV), (d)-(I)",
     "explanation":"The correct answer is (B) (a)-(III), (b)-(II), (c)-(IV), (d)-(I). This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict032","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"The number of males who passed in Commerce from City-F is approximately _______ % more than the number of females who passed in Commerce from City-F.",
     "options":["31.25", "47.47", "45.45", "42.67"],
     "correct_answer":"45.45",
     "explanation":"The correct answer is (C) 45.45. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict033","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"If the number of males who passed in Commerce from City-G is 2544, then what is the number of students who passed in Arts from City-G?",
     "options":["3600", "4200", "4800", "3400"],
     "correct_answer":"3600",
     "explanation":"The correct answer is (A) 3600. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict034","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"If the number of students who passed in Commerce from City-F is 3240, then the number of students who passed from City-F is ______ % of the number of Science students who passed from City-F.",
     "options":["75", "150", "180", "225"],
     "correct_answer":"225",
     "explanation":"The correct answer is (D) 225. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict035","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"In computer networking, an IP version-6 is _______ times larger than an IP version-4 address.",
     "options":["2", "4", "6", "8"],
     "correct_answer":"4",
     "explanation":"The correct answer is (B) 4. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict036","topic":"ICT","difficulty":"Hard","year":2024,"season":"June",
     "question":"To record voice narration for your Microsoft PowerPoint presentation, your computer must have: (a) Sound card (b) An internet connection (c) Speakers (d) An external video port (e) Microphone",
     "options":["(a), (c) and (e) only", "(b) and (d) only", "(a) and (e) only", "(b), (c) and (d) only"],
     "correct_answer":"(a) and (e) only",
     "explanation":"The correct answer is (C) (a) and (e) only. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict037","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"If (L)M represents a number L in base-M number system, then what will be the value of (107)16 + (257)16?",
     "options":["(762)10", "(862)10", "(962)10", "(662)10"],
     "correct_answer":"(862)10",
     "explanation":"The correct answer is (B) (862)10. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict038","topic":"ICT","difficulty":"Medium","year":2024,"season":"June",
     "question":"Identify the correct order of the following major technological changes A-D in the development of computers based on first to fourth generation of computers: (a) Transistors (b) Microprocessor (c) Vacuum tubes 60 (d) Integrated circuits",
     "options":["(a), (c), (d), (b)", "(b), (a), (c), (d)", "(d), (a), (c), (b)", "(c), (a), (d), (b)"],
     "correct_answer":"(c), (a), (d), (b)",
     "explanation":"The correct answer is (D) (c), (a), (d), (b). This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict039","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"According to National Credit Framework (NCrF) the credit level earned after Doctoral degree (Ph.D.) will be:",
     "options":["7", "8", "9", "10"],
     "correct_answer":"8",
     "explanation":"The correct answer is (B) 8. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict040","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"Among the following which is correct in the context of Śabda Pramāņa?",
     "options":["For Sāmkhya, a word signifies universal", "For, Jainas, a word signifies a particular", "For old Nyāya, a word symbolizes universal only", "For Vedantins, a word primarily means the class character of individuals"],
     "correct_answer":"For Vedantins, a word primarily means the class character of individuals",
     "explanation":"The correct answer is (D) For Vedantins, a word primarily means the class character of individuals. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict041","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"According to National Credit Framework (NCrF), the credit level earned after obtaining Bachelor's degree (three years of undergraduate programme) will be",
     "options":["7", "5.5", "6.5", "5"],
     "correct_answer":"5.5",
     "explanation":"The correct answer is (B) 5.5. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict042","topic":"ICT","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match the List-I with List-II List - I (Digital India Theme) List - II (Purpose) (a) e-ShodhSindhu (I) Subscription-based scholarly information (e-books and e-journals) at lower rates (b) e-Yantra (II) Robotics outreach project run by IIT, Mumbai (c) e-Vidwan (III) Expert database and National Researcher's Network (d) e-Kalpa (IV) Digital-learning environment for design",
     "options":["(a)-(IV), (b)-(II), (c)-(III), (d)-(I)", "(a)-(III), (b)-(II), (c)-(I), (d)-(IV)", "(a)-(I), (b)-(II), (c)-(III), (d)-(IV)", "(a)-(II), (b)-(IV), (c)-(III), (d)-(I)"],
     "correct_answer":"(a)-(I), (b)-(II), (c)-(III), (d)-(IV)",
     "explanation":"The correct answer is (C) (a)-(I), (b)-(II), (c)-(III), (d)-(IV). This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict043","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"If (L)16 represents a number L in base - 16 number system, then (4AC)16 + (9BF)16 =",
     "options":["(E6B)16", "(A7BF)16", "(CFC)16", "(D68)16"],
     "correct_answer":"(E6B)16",
     "explanation":"The correct answer is (A) (E6B)16. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict044","topic":"ICT","difficulty":"Hard","year":2024,"season":"June",
     "question":"Arrange the following events in the order of their occurrence starting from oldest to the recent. (a) Bhopal gas tragedy (b) Fukushima disaster (c) Chernobil disaster (d) California Smog (e) London Smog",
     "options":["(d), (e), (b), (a), (c)", "(e), (c), (a), (b), (d)", "(d), (e), (a), (c), (b)", "(e), (d), (a), (b), (c)"],
     "correct_answer":"(d), (e), (a), (c), (b)",
     "explanation":"The correct answer is (C) (d), (e), (a), (c), (b). This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict045","topic":"ICT","difficulty":"Hard","year":2024,"season":"June",
     "question":"Identify the correct order of the following computer storage capacities A-E from largest to smallest capaity (1 K = 1024) (a) 1000000 K Bytes (b) 100000 M Bytes (c) 1 T Bytes (d) 10000000000 Bytes (e) 100 G Bytes",
     "options":["(e), (c), (b), (d), (a)", "(a), (e), (b), (d), (c)", "(d), (c), (e), (b), (a)", "(c), (e), (b), (d), (a)"],
     "correct_answer":"(c), (e), (b), (d), (a)",
     "explanation":"The correct answer is (D) (c), (e), (b), (d), (a). This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict046","topic":"ICT","difficulty":"Medium","year":2024,"season":"June",
     "question":"In cloud computing, which of the following are the advantages of using cloud storage? (a) Data files of customers stores on the cloud can be accessed at any time from any device anywhere in the world provided internet access is available. (b) There is no need for customers to carry an external storage device with them or use same computer to store and retrieve information (c) If the computers have slow internet connection, then they would not face any problems accessing or downloading their data files (d) Cloud storage is typically delivered by a cloud service provider",
     "options":["(a) (b) and (c) Only", "(a), (b) and (d) Only", "(a) and (c) Only", "(b) and (c) Only"],
     "correct_answer":"(a), (b) and (d) Only",
     "explanation":"The correct answer is (B) (a), (b) and (d) Only. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict047","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"From which language is Asomiya considered to have evolved?",
     "options":["Tibetan", "Magadhi", "Angika", "Thai"],
     "correct_answer":"Magadhi",
     "explanation":"The correct answer is (B) Magadhi. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict048","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"There was an increase in revenue from atleast two types of publications in comparison to previous year for exactly _________ year(s)",
     "options":["1", "2", "3", "0"],
     "correct_answer":"2",
     "explanation":"The correct answer is (B) 2. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict049","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"In 2023, approximately what percent of the total revenue came from books?",
     "options":["46%", "55%", "35%", "25%"],
     "correct_answer":"46%",
     "explanation":"The correct answer is (A) 46%. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict050","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which year shows the highest change in revenue obtained from journals over the previous year?",
     "options":["2020", "2021", "2022", "2023"],
     "correct_answer":"2022",
     "explanation":"The correct answer is (C) 2022. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict051","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"What is the contribution of Douglas Engelbart in the evolution of computer?",
     "options":["Developed the first mouse", "Developed the first Operating System (OS)", "Developed the first Vacuum Tube", "Developed the World Wide Web (WWW)"],
     "correct_answer":"Developed the first mouse",
     "explanation":"The correct answer is (A) Developed the first mouse. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict052","topic":"ICT","difficulty":"Hard","year":2024,"season":"June",
     "question":"Identify the sequence of words A-E that correctly fills the blanks in the following paragraph on computer networking:? IPv4 addresses are ___________ long, and IPv6 addresses are __________ long. The MAC address on the other hand, is __________ long. A MAC address is oriented – towards ___________, whereas IP address is oriented towards ____________ (a) 128-bit (b) 32-bit (c) software (d) hardware (e) 48-bit",
     "options":["(b), (e), (a), (d), (c)", "(b), (a), (e), (d), (c)", "(e), (b), (a), (c), (d)", "(a), (b), (e), (d), (c)"],
     "correct_answer":"(b), (a), (e), (d), (c)",
     "explanation":"The correct answer is (B) (b), (a), (e), (d), (c). This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict053","topic":"ICT","difficulty":"Hard","year":2024,"season":"June",
     "question":"Which of the following are associated with heavy use of Internet? (a) Internet addiction (b) Depression (c) Distraction (d) Atomization (e) Media Literacy",
     "options":["(a), (b), (c), (d) only", "(b), (c), (d), (e) only", "(a), (b), (e) only", "(a), (b), (c), (e) only"],
     "correct_answer":"(a), (b), (c), (d) only",
     "explanation":"The correct answer is (A) (a), (b), (c), (d) only. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict054","topic":"ICT","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match the List-I with List-II List - I (Description) List - II (Appropriate) (a) A storage medium that stores data on the Internet (I) RAM (b) Internal storage where the current instructions are stored (II) Cloud Storage (c) A solid - state storage that is used in digital cameras (III) Blu-ray Disc (d) An optical storage medium that stores high - definition (HD) movies (IV) Flash Memory",
     "options":["(a)-(II), (b)-(IV), (c)-(I), (d)-(III)", "(a)-(III), (b)-(IV), (c)-(I), (d)-(II)", "(a)-(II), (b)-(I), (c)-(IV), (d)-(III)", "(a)-(I), (b)-(II), (c)-(III), (d)-(IV)"],
     "correct_answer":"(a)-(II), (b)-(I), (c)-(IV), (d)-(III)",
     "explanation":"The correct answer is (C) (a)-(II), (b)-(I), (c)-(IV), (d)-(III). This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict055","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"In the context of computer networking, which of the following best describes the transmission of a message using packet switching?",
     "options":["Data packets may follow different routes and may arrive at different times in different order.", "Data packets will always follow the same route and arrive at the same time in the same order.", "Data packets will always follow the same route but could arrive at different times in different", "Data packets may follow different routes but will always arrive at the same time in the same"],
     "correct_answer":"Data packets may follow different routes and may arrive at different times in different order.",
     "explanation":"The correct answer is (A) Data packets may follow different routes and may arrive at different times in different order.. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict056","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"Role of rituals in human life",
     "options":["is to distract us from our goals", "is to keep us busy and structure our daily activities", "is very important during the religious practices only", "is irrelevant in contemporary life"],
     "correct_answer":"is to keep us busy and structure our daily activities",
     "explanation":"The correct answer is (B) is to keep us busy and structure our daily activities. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict057","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"The number of male viewers of ZEE TV from city C is approximately _________ % more than the number of female viewers of SONY TV from city F?",
     "options":["12.4", "15.2", "17.3", "18.6"],
     "correct_answer":"18.6",
     "explanation":"The correct answer is (D) 18.6. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict058","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"The total number of female viewers of COLORS TV from city C is approximately _______ % of the total number of female viewers of JIO from city A.",
     "options":["82", "88", "96", "108"],
     "correct_answer":"88",
     "explanation":"The correct answer is (B) 88. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict059","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"What is the difference between the total number of male viewers and female viewers of ZEE TV from all six cities?",
     "options":["710", "704", "706", "708"],
     "correct_answer":"710",
     "explanation":"The correct answer is (A) 710. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict060","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"‘Web 2.0’, a second generation of the Internet, can best be described as:",
     "options":["A software package developed by Microsoft and available at a discount to teachers", "An approach to the Internet in which users can share thoughts, opinions and ideas in a free", "An approach to the Internet in which websites and apps can process information in a smart", "Faster Internet for big business"],
     "correct_answer":"An approach to the Internet in which users can share thoughts, opinions and ideas in a free",
     "explanation":"The correct answer is (B) An approach to the Internet in which users can share thoughts, opinions and ideas in a free. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict061","topic":"ICT","difficulty":"Medium","year":2024,"season":"June",
     "question":"Which of the following statements are true with reference to cybersecurity? (a) Incident response in cyber security involves identifying vulnerabilities and patching them before an attack occurs (b) CERT-In acts as an early warning system for cyber threats and attacks in India (c) ‘Tor’ is an acronym for 'The Onion Router', which is a web browser that enables people to communicate anonymously online to prevent bad actors from tracking their Internet activity (d) Using a Virtual Personal Network can help secure a network by encrypting the data transmitted over it",
     "options":["(a) and (d) only", "(a) and (c) only", "(b) and (d) only", "(b) and (c) only"],
     "correct_answer":"(b) and (c) only",
     "explanation":"The correct answer is (D) (b) and (c) only. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict062","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"Each webpage is assigned a (n) ________, an address that identifies the location of the page on the Internet.",
     "options":["Internet Protocol (IP)", "Uniform Resource Locator (URL)", "Top-Level Domain (TLD)", "Hyper Text Transfer Protocol (HTTP)"],
     "correct_answer":"Uniform Resource Locator (URL)",
     "explanation":"The correct answer is (B) Uniform Resource Locator (URL). This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict063","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"A physics instructor needs to create international videos demonstrating Newton's law of motion. Which tool should the instructor use to record, edit and share these videos with students.",
     "options":["Flipgrid", "Camtasia", "Padlet", "Google forms"],
     "correct_answer":"Camtasia",
     "explanation":"The correct answer is (B) Camtasia. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict064","topic":"ICT","difficulty":"Medium","year":2024,"season":"June",
     "question":"If (L)M represents a number L in base-M number system then identify the correct ascending order of the following numbers A-D when converted to decimal number system (a) (203)4 (b) (100001)2 (c) (114)5 (d) (1012)3",
     "options":["(d), (b), (c), (a)", "(b), (d), (c), (a)", "(a), (b), (c), (d)", "(d), (b), (a), (c)"],
     "correct_answer":"(d), (b), (c), (a)",
     "explanation":"The correct answer is (A) (d), (b), (c), (a). This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict065","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which of the following groups of people of Andaman and Nicobar islands have migrated from Indian mainland, Myanmar and Sri Lanka?",
     "options":["Indians", "Natives", "Nagas", "Marwaris"],
     "correct_answer":"Indians",
     "explanation":"The correct answer is (A) Indians. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict066","topic":"ICT","difficulty":"Medium","year":2024,"season":"June",
     "question":"Identify the correct order of the following storage devices A-D as per their increasing data storage capacity: (a) DVD (b) Hard Disk (c) CDROM (d) Blu-Ray Disk",
     "options":["(c), (a), (d), (b)", "(a), (c), (d), (b)", "(b), (d), (c), (a)", "(c), (a), (b), (d)"],
     "correct_answer":"(c), (a), (d), (b)",
     "explanation":"The correct answer is (A) (c), (a), (d), (b). This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict067","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"A 'SWAYAM' course is classified based on the engagement of number of __________ and number of video hours.",
     "options":["semesters", "months", "weeks", "years"],
     "correct_answer":"weeks",
     "explanation":"The correct answer is (C) weeks. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict068","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which of the following pair of acronyms and their expansion is incorrectly matched?",
     "options":["SIM - Subscriber Identity Module", "SMTP - Simple Mail Transfer Plan", "SQL - Structured Query Language", "URL - Uniform Resource Locator"],
     "correct_answer":"SMTP - Simple Mail Transfer Plan",
     "explanation":"The correct answer is (B) SMTP - Simple Mail Transfer Plan. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict069","topic":"ICT","difficulty":"Hard","year":2024,"season":"June",
     "question":"Value based education shall include universal human values such as: (a) Isolation (b) Non-violence (c) Peace (d) Righteous conduct (e) Punishment to crime",
     "options":["(a), (b) only", "(b), (c) and (d) only", "(c), (d) and (e) only", "(a), (c) and (e) only"],
     "correct_answer":"(b), (c) and (d) only",
     "explanation":"The correct answer is (B) (b), (c) and (d) only. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict070","topic":"ICT","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match List I with List - II. List - I (ICT Term) List - II (Meaning) (a) Software (I) The software that accesses and displays pages on the web. (b) Web Browser (II) A mechanism that isolates a network from the rest of the Internet, permitting only specific traffic to pass in and out. (c) PDA (III) A set of computer programs that enables hardware to perform different tasks. (d) Firewall (IV) A small mobile computing device.",
     "options":["(a)-(I), (b)-(III), (c)-(IV), (d)-(II)", "(a)-(II), (b)-(I), (c)-(IV), (d)-(III)", "(a)-(III), (b)-(I), (c)-(IV), (d)-(II)", "(a)-(I), (b)-(III), (c)-(II), (d)-(IV)"],
     "correct_answer":"(a)-(III), (b)-(I), (c)-(IV), (d)-(II)",
     "explanation":"The correct answer is (C) (a)-(III), (b)-(I), (c)-(IV), (d)-(II). This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict071","topic":"ICT","difficulty":"Medium","year":2024,"season":"June",
     "question":"Which of the following statements are true in the context of Web Conferencing? (a) It uses the Internet to permit conferencing to take place. (b) Multiple computers are used with this system, all connected over the Internet. (c) Delegates cannot leave the conference once they join. (d) It is carried out in real-time.",
     "options":["(a) and (b) only", "(a), (b) and (c) only", "(c) and (d) only", "(a), (b) and (d)"],
     "correct_answer":"(a), (b) and (d)",
     "explanation":"The correct answer is (D) (a), (b) and (d). This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict072","topic":"ICT","difficulty":"Hard","year":2024,"season":"June",
     "question":"The important characteristics of Internet communication are: (a) Absence of sub-media (b) Multi-data networking (c) High fidelity realism (d) Sophisticated reciprocity (e) Non-interactive",
     "options":["(a), (b) and (c) only", "(b), (c) and (d) only", "(c), (d) and (e) only", "(a), (d) and (e) only"],
     "correct_answer":"(b), (c) and (d) only",
     "explanation":"The correct answer is (B) (b), (c) and (d) only. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict073","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"In Parashurama Vyayoga, how did Kapilendra Dev show his support for the Oriya language?",
     "options":["By writing the entire work in Oriya", "By including an Oriya poem", "By translating it into multiple languages", "By prohibiting Sanskrit and Tamil languages"],
     "correct_answer":"By including an Oriya poem",
     "explanation":"The correct answer is (B) By including an Oriya poem. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict074","topic":"ICT","difficulty":"Hard","year":2024,"season":"June",
     "question":"Which of the following software titles are examples of system software? (a) Ubuntu (b) Google Docs (c) MS-Office 365 (d) Android (e) Chrome OS",
     "options":["(a), (b), (d) and (e) only", "(b) and (c) only", "(a), (d) and (e) only", "(c), (d) and (e) only"],
     "correct_answer":"(a), (d) and (e) only",
     "explanation":"The correct answer is (C) (a), (d) and (e) only. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict075","topic":"ICT","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match the List-I with List-II List - I (Tool/ Softwares) List - II (Applications) (a) Plotagon (I) To create Pre-and-post-session polls to gauge student learning from each session (b) Mindmeister (II) To create instant animated videos (c) Github (III) To understand and make connections between concepts, ideas and information (d) Mentimeter (IV) To store, share, and work together with others to write code",
     "options":["(a)-(IV), (b)-(II), (c)-(I), (d)-(III)", "(a)-(III), (b)-(II), (c)-(IV), (d)-(I)", "(a)-(ІI), (b)-(III), (c)-(IV), (d)-(I)", "(a)-(I), (b)-(IV), (c)-(III), (d)-(II)"],
     "correct_answer":"(a)-(ІI), (b)-(III), (c)-(IV), (d)-(I)",
     "explanation":"The correct answer is (C) (a)-(ІI), (b)-(III), (c)-(IV), (d)-(I). This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict076","topic":"ICT","difficulty":"Hard","year":2024,"season":"June",
     "question":"The recommendations of the National Council of Teachers Education (1976) were: (a) Limiting the number of teacher education colleges (b) Universities should recognise short term courses for in-service education for teachers (c) Avoidance of correspondence courses for in-service teachers (d) Use of technological aids like television, films and others (e) Formulation of a network of extension services for in-service teachers",
     "options":["(a), (b), (c) only", "(b), (c), (d) only", "(c), (d), (e) only", "(b), (d), (e) only"],
     "correct_answer":"(b), (d), (e) only",
     "explanation":"The correct answer is (D) (b), (d), (e) only. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict077","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"What is the total number of rejected sports shoes from all the companies together in year 2022?",
     "options":["835000", "835020", "835040", "835080"],
     "correct_answer":"835000",
     "explanation":"The correct answer is (A) 835000. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict078","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"Microsoft Access is an example of a(n) ___________.",
     "options":["Operational resource toolkit system", "ERP system", "Database management system", "Knowledge management system"],
     "correct_answer":"Database management system",
     "explanation":"The correct answer is (C) Database management system. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict079","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which of the following is a software that displays unwanted or sometimes irritating pop-up advertisements which can appear on your computer or mobile phone?",
     "options":["Spyware", "Adware", "Worm", "Trojan Horse"],
     "correct_answer":"Adware",
     "explanation":"The correct answer is (B) Adware. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict080","topic":"ICT","difficulty":"Hard","year":2024,"season":"June",
     "question":"Which of the following devices are computer output devices only? (a) Scanner (b) Plotter (c) Light pen (d) Projector (e) Speaker",
     "options":["(a), (b), (d) and (e) only", "(d) and (e) only", "(a), (b) and (c) only", "(b), (d) and (e) only"],
     "correct_answer":"(b), (d) and (e) only",
     "explanation":"The correct answer is (D) (b), (d) and (e) only. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict081","topic":"ICT","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match List - I with List - II. List - I (ICT Term) List - II (Definition) (a) VoIP (I) A tool for real-time communication between two or more people sending text messages to their devices (b) Instant Messaging (IM) (II) A system of interlinked hypertext documents accessed via the Internet (c) VPN (III) A technology that allows you to talk with other people using the internet (d) WWW (IV) A network that protects data by encrypting network traffic 133",
     "options":["(a)-(II), (b)-(I), (c)-(IV), (d)-(III)", "(a)-(IV), (b)-(II), (c)-(III), (d)-(I)", "(a)-(III), (b)-(I), (c)-(II), (d)-(IV)", "(a)-(III), (b)-(I), (c)-(IV), (d)-(II)"],
     "correct_answer":"(a)-(III), (b)-(I), (c)-(IV), (d)-(II)",
     "explanation":"The correct answer is (D) (a)-(III), (b)-(I), (c)-(IV), (d)-(II). This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict082","topic":"ICT","difficulty":"Medium","year":2024,"season":"June",
     "question":"On the basis of the coverage area, identify the correct ascending order of the following four types of computer networks A-D: (a) WAN (b) LAN (c) MAN (d) PAN",
     "options":["(d), (b), (c), (a)", "(b), (c), (a), (d)", "(d), (c), (b), (a)", "(a), (b), (d), (c)"],
     "correct_answer":"(d), (b), (c), (a)",
     "explanation":"The correct answer is (A) (d), (b), (c), (a). This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict083","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which one of the following is considered as a prominent indoor air pollutant?",
     "options":["Mercury", "Radon", "Helium", "Argon"],
     "correct_answer":"Radon",
     "explanation":"The correct answer is (B) Radon. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict084","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"The number of participants from China in event E2 is _______% more than the number of female participants from US in event E3.",
     "options":["120", "124", "128", "132"],
     "correct_answer":"132",
     "explanation":"The correct answer is (D) 132. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict085","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"What is the difference between the number of male participants and the number of female participants in the event E2 from all the six countries together?",
     "options":["1724", "1728", "1732", "1734"],
     "correct_answer":"1732",
     "explanation":"The correct answer is (C) 1732. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict086","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"The number of female participants from India in event E1 is _________ % less than the number of female participants from Germany in event E3.",
     "options":["40", "36", "28", "22"],
     "correct_answer":"36",
     "explanation":"The correct answer is (B) 36. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict087","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"A web-based e-learning application allowing users to select a video and customize it by editing, cropping, recording their own audio and adding quiz questions directly to the video stream is known as:",
     "options":["ED puzzle", "Mindmeister", "Miro", "Labster"],
     "correct_answer":"ED puzzle",
     "explanation":"The correct answer is (A) ED puzzle. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict088","topic":"ICT","difficulty":"Medium","year":2024,"season":"June",
     "question":"With reference to computer networking, which of the following statements is true of an Intranet.",
     "options":["It is a network within an organization that uses Internet protocols and technologies.", "It is a network that covers a wide area with the help of rented telecommunication lines.", "It is a network where a computer is connected to the Internet and acts as a gateway for other", "It is a widely available public network of interconnected computer networks."],
     "correct_answer":"It is a network within an organization that uses Internet protocols and technologies.",
     "explanation":"The correct answer is (A) It is a network within an organization that uses Internet protocols and technologies.. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict089","topic":"ICT","difficulty":"Hard","year":2024,"season":"June",
     "question":"Identify the sequence of words A-E that correctly fills the blanks in the following paragraph: An operating system that uses windows, icons, menus and pointers for human - computer interaction, is known as ________. Post-WIMP inter-faces found on devices like iPads, iPods and mobile phone make use of _________ technology that allows us to use our fingers to select icons and menus. Post- WIMP interfaces allow us to use __________, rotating and swiping techniques. The technology that allows users to store documents, programs and data on Internet is known as ___________. Documents created using Google Docs are stored _________ on the Internet and can be accessed anywhere and at any time. (a) Touch Screen (b) Cloud Computing (c) GUI (d) Remotely (e) Pinching",
     "options":["(c), (a), (e), (d), (b)", "(a), (c), (d), (b), (e)", "(b), (d), (c), (e), (a)", "(c), (a), (e), (b), (d)"],
     "correct_answer":"(c), (a), (e), (b), (d)",
     "explanation":"The correct answer is (D) (c), (a), (e), (b), (d). This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict090","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which of the following pair of acronym and its expansion is incorrectly matched?",
     "options":["CDROM - Computer Disk Read Only Memory", "CRT - Cathode Ray Tube", "MICR - Magnetic Ink Character Recognition", "AVI - Audio Video Interleave"],
     "correct_answer":"CDROM - Computer Disk Read Only Memory",
     "explanation":"The correct answer is (A) CDROM - Computer Disk Read Only Memory. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict091","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"The process mostly completed within several hours, but which can last for years, which fixes information in long-term memory is known as:",
     "options":["Repression", "Episodic memory", "Consolidation", "Retroactive interference"],
     "correct_answer":"Consolidation",
     "explanation":"The correct answer is (C) Consolidation. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict092","topic":"ICT","difficulty":"Hard","year":2024,"season":"June",
     "question":"Which of the following devices are computer input devices only? (a) DVD - R (b) Joystick (c) Plotter (d) Touch Pad (e) Microphone",
     "options":["(a), (d) and (e) only", "(b), (d) and (e) only", "(a), (b) and (c) only", "(b), (c), (d) and (e) only"],
     "correct_answer":"(b), (d) and (e) only",
     "explanation":"The correct answer is (B) (b), (d) and (e) only. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict093","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"The origin of the world 'adolescence' has come from the following language:",
     "options":["Latin", "Greek", "Sanskrit", "German"],
     "correct_answer":"Greek",
     "explanation":"The correct answer is (B) Greek. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict094","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"The term 'adolescence' means:",
     "options":["A state of bliss", "Innocence of childhood", "Moving towards maturity", "Detachment from materialistic world"],
     "correct_answer":"Moving towards maturity",
     "explanation":"The correct answer is (C) Moving towards maturity. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict095","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"If out of the number of viewers from Town-C, 325 7 % are female and 7 13 of the number of female viewers are unsubscribed viewers, then the number of unsubscribed male viewers from Town-C is.",
     "options":["340", "360", "380", "420"],
     "correct_answer":"380",
     "explanation":"The correct answer is (C) 380. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict096","topic":"ICT","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match the List-I with List-II List -I (Online Softwares/Tools) List -II (Application) (a) Trello (I) Managing and analyzing social media campaigns (b) Hootsuite (II) Managing and recording, fun built-in camera recording add effects and share in the groups (c) GitHub Classroom (III) Managing group projects and tasks (d) Flipgrid (IV) Managing and writing coding assignments",
     "options":["(a)-(IV), (b)-(III), (c)-(II), (d)-(I)", "(a)-(III), (b)-(IV), (c)-(II), (d)-(I)", "(a)-(III), (b)-(I), (c)-(IV), (d)-(II)", "(a)-(I), (b)-(II), (c)-(III), (d)-(IV)"],
     "correct_answer":"(a)-(III), (b)-(I), (c)-(IV), (d)-(II)",
     "explanation":"The correct answer is (C) (a)-(III), (b)-(I), (c)-(IV), (d)-(II). This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict097","topic":"ICT","difficulty":"Hard","year":2024,"season":"June",
     "question":"Which of the following software titles are examples of operating system? (a) MS-Word (b) Linux (c) MS-PowerPoint (d) Adobe Photoshop (e) Android",
     "options":["(a), (c) and (d) only", "(a), (b), (c) and (d) only", "(b) and (e) only", "(b), (d) and (e) only"],
     "correct_answer":"(b) and (e) only",
     "explanation":"The correct answer is (C) (b) and (e) only. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict098","topic":"ICT","difficulty":"Hard","year":2024,"season":"June",
     "question":"Which of the following can be used as LMS to create and manage course content? (a) Moodle (b) Zoom (c) Edmodo (d) Canvas (e) Strawpoll",
     "options":["(b), (d) and (e) only", "(a), (c) and (d) only", "(b), (c) and (e) only", "(a), (b) and (d) only"],
     "correct_answer":"(a), (c) and (d) only",
     "explanation":"The correct answer is (B) (a), (c) and (d) only. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict099","topic":"ICT","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match the List-I with List-II List - I (Computer Network) List - II (Description) (a) Flat Network (I) Describes today's worldwide connection of networks (b) Extranet (II) Describes a network that lies completely inside a trusted area of a network and is under the security control of system and network administrators (c) Intranet (III) Describes a network that avoids packet-looping issues, through an architecture that does not have layers (d) Internet (IV) Describes a network that is an extension of a selected portion of a company's Intranet to external partners",
     "options":["(a)-(IV), (b)-(III), (c)-(I), (d)-(II)", "(a)-(III), (b)-(IV), (c)-(II), (d)-(I)", "(a)-(II), (b)-(I), (c)-(III), (d)-(IV)", "(a)-(III), (b)-(IV), (c)-(I), (d)-(II)"],
     "correct_answer":"(a)-(III), (b)-(IV), (c)-(II), (d)-(I)",
     "explanation":"The correct answer is (B) (a)-(III), (b)-(IV), (c)-(II), (d)-(I). This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict100","topic":"ICT","difficulty":"Medium","year":2024,"season":"June",
     "question":"If (L)M represents a number L in base- M number system, then identify the correct descending order of the following numbers A-D when converted to decimal number system. (a) (123)7 (b) (1211)3 (c) (212)6 (d) (201)5",
     "options":["(a), (c), (b), (d)", "(b), (d), (a), (c)", "(d), (b), (c), (a)", "(c), (a), (d), (b)"],
     "correct_answer":"(c), (a), (d), (b)",
     "explanation":"The correct answer is (D) (c), (a), (d), (b). This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict101","topic":"ICT","difficulty":"Hard","year":2024,"season":"June",
     "question":"The internet portals function like (a) Folk entertainers (b) Mass circulation magazines (c) T.V. networks (d) Sites of meta-aggregate contents (e) The home page of users",
     "options":["(a), (b), (c) only", "(a), (b), (c), (d) only", "(a), (c), (d) only", "(b), (c), (d), (e) only"],
     "correct_answer":"(b), (c), (d), (e) only",
     "explanation":"The correct answer is (D) (b), (c), (d), (e) only. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict102","topic":"ICT","difficulty":"Hard","year":2024,"season":"June",
     "question":"Arrange the phases of Inquiry-based learning approach in a sequence from Phase I to Phase V (a) Discussion (b) Orientation (c) Conceptualization (d) Conclusion (e) Investigation",
     "options":["(a), (b), (c), (d), (e)", "(e), (a), (d), (b), (c)", "(b), (c), (e), (d), (a)", "(b), (e), (a), (c), (d)"],
     "correct_answer":"(b), (c), (e), (d), (a)",
     "explanation":"The correct answer is (C) (b), (c), (e), (d), (a). This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict103","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which one of the following personalities advocated western education for Indians in the early nineteenth century?",
     "options":["Rajaram Mohan Roy", "Lord Hardinge", "Mahatma Gandhi", "Rabindranath Tagore"],
     "correct_answer":"Rajaram Mohan Roy",
     "explanation":"The correct answer is (A) Rajaram Mohan Roy. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict104","topic":"ICT","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match the List-I with List-II List - I (ICT Terms) List - II (Meaning) (a) Printer (I) Volatile memory (b) Scanner (II) Processor (c) RAM (III) Output device (d) CPU (IV) Input device",
     "options":["(a)-(II), (b)-(III), (c)-(IV), (d)-(I)", "(a)-(III), (b)-(IV), (c)-(I), (d)-(II)", "(a)-(I), (b)-(II), (c)-(IV), (d)-(III)", "(a)-(III), (b)-(IV), (c)-(II), (d)-(I)"],
     "correct_answer":"(a)-(III), (b)-(IV), (c)-(I), (d)-(II)",
     "explanation":"The correct answer is (B) (a)-(III), (b)-(IV), (c)-(I), (d)-(II). This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict105","topic":"ICT","difficulty":"Hard","year":2024,"season":"June",
     "question":"Which of the following countries were asked to reduce their green house emission by 5% below the level of 1990 by 2012 in Kyoto protocol? (a) United States (b) India (c) Russia (d) Canada (e) China",
     "options":["(a), (c) and (d) only", "(c), (d) and (e) only", "(b), (c) and (e) only", "(b) and (e) only"],
     "correct_answer":"(a), (c) and (d) only",
     "explanation":"The correct answer is (A) (a), (c) and (d) only. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict106","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"The development of vitascope led to:",
     "options":["The silent film era", "Video advertisements", "The television network system", "The arrival of computers"],
     "correct_answer":"The silent film era",
     "explanation":"The correct answer is (A) The silent film era. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict107","topic":"ICT","difficulty":"Hard","year":2024,"season":"June",
     "question":"Which of the following software titles are examples of application software only? (a) MS-Excel (b) Android 168 (c) Adobe Photoshop (d) iOS (e) Windows- 11",
     "options":["(a), (b) and (c) only", "(b) and (d) only", "(a) and (c) only", "(a) and (e) only"],
     "correct_answer":"(a) and (c) only",
     "explanation":"The correct answer is (C) (a) and (c) only. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict108","topic":"ICT","difficulty":"Medium","year":2024,"season":"June",
     "question":"Which of the following statements about Read Only Memory (ROM) are correct? (a) The contents of the memory remain intact even when the power to the ROM is turned off (b) ROM is often used to store the start-up instructions when the computer is first switched on (c) As the ROM becomes full, the processor has to continually access the hard disk (d) ROM is a volatile memory",
     "options":["(a) and (b) only", "(b) and (c) only", "(a) and (c) only", "(a), (b), (c) and (d)"],
     "correct_answer":"(a) and (b) only",
     "explanation":"The correct answer is (A) (a) and (b) only. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict109","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"In the context of Computer Networks, which of the following best describes the transmission of a message using packet switching?",
     "options":["Data packets may follow different routes and may arrive at different times in different order.", "Data packets will always follow the same route and arrive at the same time in the same order", "Data packets will always follow the same route but could arrive at different times in different", "Data packets may follow different routes but will always arrive at the same time in the same"],
     "correct_answer":"Data packets may follow different routes and may arrive at different times in different order.",
     "explanation":"The correct answer is (A) Data packets may follow different routes and may arrive at different times in different order.. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict110","topic":"ICT","difficulty":"Medium","year":2024,"season":"June",
     "question":"Which of the following statements is true about computers?",
     "options":["The quality of the pictures taken by a digital camera depends on its resolution, which is", "USB stands for Universal Secure Bus", "Microsoft Excel is an example of system software", "The size of a computer monitor is measured diagonally across the screen"],
     "correct_answer":"The size of a computer monitor is measured diagonally across the screen",
     "explanation":"The correct answer is (D) The size of a computer monitor is measured diagonally across the screen. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict111","topic":"ICT","difficulty":"Medium","year":2024,"season":"June",
     "question":"Which of the following statements is true about Number system?",
     "options":["The binary equivalent of the decimal number 57.625 is 111000.101", "(145)6 = (75)10", "(1011)2 + (1001)2 = (20)10", "(65)10 = (220)5"],
     "correct_answer":"(1011)2 + (1001)2 = (20)10",
     "explanation":"The correct answer is (C) (1011)2 + (1001)2 = (20)10. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict112","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"SWAYAM is a programme initiated by.",
     "options":["Government of India", "National Council of Education Research and Training", "University Grants commission", "Indira Gandhi National Open University"],
     "correct_answer":"Government of India",
     "explanation":"The correct answer is (A) Government of India. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict113","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which of the following is a free and Open-source content collaboration framework based on Javascript that enables existing CMSs and LMSs to create richer content?",
     "options":["H5P", "Plotagon", "Mindmeister", "Labster"],
     "correct_answer":"H5P",
     "explanation":"The correct answer is (A) H5P. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict114","topic":"ICT","difficulty":"Hard","year":2024,"season":"June",
     "question":"Which of the following are examples of organic pollutants in water. (a) Salts (b) Pesticides (c) Dioxins (d) Bases (e) Pigments",
     "options":["(a), (b) and (c) only", "(b), (c) and (d) only", "(c), (d) and (e) only", "(b), (c) and (e) only"],
     "correct_answer":"(b), (c) and (e) only",
     "explanation":"The correct answer is (D) (b), (c) and (e) only. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict115","topic":"ICT","difficulty":"Medium","year":2024,"season":"June",
     "question":"In computers, which of the following statements is true?",
     "options":["Data matrix printer is a type of non-impact printer", "laser printer is a type of impact printer", "The resolution of a laser printer is measured in Megabits per second (Mbps)", "Data matrix printers are noisy, low quality and slow in comparison to laser printers"],
     "correct_answer":"Data matrix printers are noisy, low quality and slow in comparison to laser printers",
     "explanation":"The correct answer is (D) Data matrix printers are noisy, low quality and slow in comparison to laser printers. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict116","topic":"ICT","difficulty":"Medium","year":2024,"season":"June",
     "question":"Which of the following statements about spreadsheet software (MS-EXCEL) are true? (a) Data in spreadsheets are always correct. 189 (b) Spreadsheet software cannot draw bar graphs. (c) Spread sheet software automatically recalculates. (d) Some cells in a spreadsheet can be locked to prevent a user changing its contents.",
     "options":["(a) and (b) only", "(c) and (d) only", "(a) and (c) only", "(b) and (d) only"],
     "correct_answer":"(c) and (d) only",
     "explanation":"The correct answer is (B) (c) and (d) only. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict117","topic":"ICT","difficulty":"Medium","year":2024,"season":"June",
     "question":"With reference to different number systems, which of the following statements is true?",
     "options":["(109)10 = (1101001)2", "(123)5 = (212)4", "(101)16 + (110)8 = (429)10", "(241)6 = (131)8"],
     "correct_answer":"(123)5 = (212)4",
     "explanation":"The correct answer is (B) (123)5 = (212)4. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict118","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"The transfer of learning from one situation to another situation that is conscious and effortful is known as –",
     "options":["Near transfer", "High-road transfer", "Low-road transfer", "Far transfer"],
     "correct_answer":"High-road transfer",
     "explanation":"The correct answer is (B) High-road transfer. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict119","topic":"ICT","difficulty":"Medium","year":2024,"season":"June",
     "question":"With reference to ICT, which of the following statements is true?",
     "options":["Global Positioning Systems (GPSs) in cars send signals to satellite which then work out", "HTTP stands for HyperText Transfer policy.", "RAM stands for Rapid Access Memory.", "Geographic Information System (GIS) is a computer based tool for mapping and analysing"],
     "correct_answer":"Geographic Information System (GIS) is a computer based tool for mapping and analysing",
     "explanation":"The correct answer is (D) Geographic Information System (GIS) is a computer based tool for mapping and analysing. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict120","topic":"ICT","difficulty":"Medium","year":2024,"season":"June",
     "question":"Based on the following, which of the following statements is true. A CD contains 12 music tracks which are of lengths (in minute): 3, 7, 4, 3, 5, 6, 4, 5, 4, 7, 8, 8 and each minute of music requires 12 MB of storage.",
     "options":["512 MB of memory is used for the 12 music tracks.", "1 GB of memory is used for the 12 music tracks.", "768 MB of memory is used for the 12 music tracks.", "If the tracks are to be stored in MP3 format, then each music track will be reduced in size by"],
     "correct_answer":"768 MB of memory is used for the 12 music tracks.",
     "explanation":"The correct answer is (C) 768 MB of memory is used for the 12 music tracks.. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict121","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which of the following \"Digital India\" themes is incorrectly matched with its purpose?",
     "options":["Spoken Tutorial- Learn various free and open-source software all by oneself", "FOSSEE- Reduce dependency on proprietary software in Educational Institutions", "e-Kalpa- Create Digital-learning environment for design", "e-ShodhSindhi- Spread education in Embedded systems and Robotics"],
     "correct_answer":"e-ShodhSindhi- Spread education in Embedded systems and Robotics",
     "explanation":"The correct answer is (D) e-ShodhSindhi- Spread education in Embedded systems and Robotics. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict122","topic":"ICT","difficulty":"Hard","year":2024,"season":"June",
     "question":"Biomass (a) is a carbon cycle neutral fuel (b) has significantly higher calorific value then coal (c) can be converted in solid, liquid and gaseous fuels (d) can be converted into Producer Gas (e) cannot be obtained from energy crops",
     "options":["(a), (b) and (c) only", "(a), (c) and (d) only", "(b), (d) and (e) only", "(a), (b) and (e) only"],
     "correct_answer":"(a), (c) and (d) only",
     "explanation":"The correct answer is (B) (a), (c) and (d) only. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict123","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"In computer Networking, MAC addresses are unique to each device. Which of the following is the meaning of the term MAC?",
     "options":["Medium Access Card", "Media Address Command", "Modem Addressing Card", "Media Access Control"],
     "correct_answer":"Media Access Control",
     "explanation":"The correct answer is (D) Media Access Control. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict124","topic":"ICT","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match the List-I with List-II List - I (Computer Components) List - II (Description) (a) ALU (I) Immediate access storage (b) Control Unit (II) Carries out arithmetical and logical calculations (c) Pen Drive (III) Directs the input and output flow in the CPU (d) Main Memory (IV) Secondary/ offline storage",
     "options":["(a)-(II), (b)-(III), (c)-(IV), (d)-(I)", "(a)-(II), (b)-(I), (c)-(IV), (d)-(III)", "(a)-(I), (b)-(III), (c)-(IV), (d)-(II)", "(a)-(IV), (b)-(III), (c)-(II), (d)-(I)"],
     "correct_answer":"(a)-(II), (b)-(III), (c)-(IV), (d)-(I)",
     "explanation":"The correct answer is (A) (a)-(II), (b)-(III), (c)-(IV), (d)-(I). This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict125","topic":"ICT","difficulty":"Medium","year":2024,"season":"June",
     "question":"Arrange the following terms in order of decreasing in intension? (a) Baseball player (b) Athlete (c) Fielder 201 (d) Ball player",
     "options":["(c), (d), (a), (b)", "(b), (a), (d), (c)", "(c), (a), (d), (b)", "(b), (d), (a), (c)"],
     "correct_answer":"(c), (a), (d), (b)",
     "explanation":"The correct answer is (C) (c), (a), (d), (b). This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict126","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"What do people basically want to extract from the communicated message?",
     "options":["Compulsions", "Meaning", "Synergy", "Behavioural pattern"],
     "correct_answer":"Meaning",
     "explanation":"The correct answer is (B) Meaning. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict127","topic":"ICT","difficulty":"Medium","year":2024,"season":"June",
     "question":"Ethical living is based on (a) our own virtuous attributes (b) our behaviour towards other species (c) our behaviour towards environment (d) material satisfaction",
     "options":["(b) and (c) only", "(a) and (b) only", "(a), (b) and (c) only", "(a) (b), (c) and (d)"],
     "correct_answer":"(a), (b) and (c) only",
     "explanation":"The correct answer is (C) (a), (b) and (c) only. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict128","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"Computer security breaches can be minimized by incorporating which feature into a computer system's operation?",
     "options":["Installation of software of user's choice", "The ability to log into multiple nodes, using only one account", "Forced log off from the system if no activity has been detected", "Allowing the uploading and downloading of files to the system"],
     "correct_answer":"Forced log off from the system if no activity has been detected",
     "explanation":"The correct answer is (C) Forced log off from the system if no activity has been detected. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict129","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"Priya knows she did something embarrassing at her best friend's birthday party many years ago, but she cannot remember what it was. This is an example of:",
     "options":["Repression", "Amnesia", "Implicit memory", "Interferences"],
     "correct_answer":"Repression",
     "explanation":"The correct answer is (A) Repression. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict130","topic":"ICT","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match List - I with List - II. List -I (Computer Components) List -II (Meaning) (a) RAM (I) Brain of the computer (b) ROM (II) Stores the date, time and system configuration for BIOS (c) CMOS (III) Memory that can be written to and read from (d) CPU (IV) Stores 'boot up' program",
     "options":["(a)-(III), (b)-(II), (c)-(IV), (d)-(I)", "(a)-(ІІІ), (b)-(IV), (c)-(II), (d)-(I)", "(a)-(ІІІ), (b)-(I), (c)-(IV), (d)-(II)", "(a)-(IV), (b)-(III), (c)-(II), (d)-(I)"],
     "correct_answer":"(a)-(ІІІ), (b)-(IV), (c)-(II), (d)-(I)",
     "explanation":"The correct answer is (B) (a)-(ІІІ), (b)-(IV), (c)-(II), (d)-(I). This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict131","topic":"ICT","difficulty":"Medium","year":2024,"season":"June",
     "question":"Knowing the importance of metacognition, Richa decided she would try to focus her young students' attention on their own thinking skills. Richa knew by having her students \"think\" about their thinking they would eventually increase their metacognitive skills. Which one of the strategy should Richa employ?",
     "options":["Overlearning", "A KWL Chart", "Rote learning", "An algorithm"],
     "correct_answer":"A KWL Chart",
     "explanation":"The correct answer is (B) A KWL Chart. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict132","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which of the following electronic technologies is the key technology for making the Personal Computer (PC) in the 1970s?",
     "options":["Transistor based", "Integrated components (ICs) based", "Microprocessor based", "Vacumm tube based"],
     "correct_answer":"Microprocessor based",
     "explanation":"The correct answer is (C) Microprocessor based. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict133","topic":"ICT","difficulty":"Hard","year":2024,"season":"June",
     "question":"With reference to computer components, which of the following statements are correct? (a) A hard drive has no moving parts. (b) Fan is required to cool down CPUs so that these do not overheat. (c) Accessing information in a hard drive is faster than accessing information stored in RAM. (d) When power is switched off, any information stored in a hard drive is lost. (e) For a given amount of memory, RAM is more expensive than a hard drive.",
     "options":["(a), (b) and (e) only", "(c) and (d) only", "(c), (d) and (e) only", "(b) and (e) only"],
     "correct_answer":"(b) and (e) only",
     "explanation":"The correct answer is (D) (b) and (e) only. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict134","topic":"ICT","difficulty":"Medium","year":2024,"season":"June",
     "question":"If (L)M represents a number L in base-M number system, then identify the correct ascending order of the following numbers A-D when converted to decimal number system. (a) (102)4 (b) (10001)2 (c) (103)6 (d) (201)3",
     "options":["(b), (a), (c), (d)", "(a), (c), (d), (b)", "(a), (b), (d), (c)", "(b), (a), (d), (c)"],
     "correct_answer":"(b), (a), (d), (c)",
     "explanation":"The correct answer is (D) (b), (a), (d), (c). This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict135","topic":"ICT","difficulty":"Hard","year":2024,"season":"June",
     "question":"A marketing instructor wants to engage students by conducting live polls during an online lecture to gather instant feedback on marketing strategies. Which of the following tools should the instructor use for creating and displaying polls? (a) Adobe Illustrator (b) Slido (c) Straw Poll (d) Camtasia (e) Flipgrid",
     "options":["(a), (b) and (e) Only", "(a) and (d) Only", "(b) and (c) Only", "(c), (d) and (e) Only"],
     "correct_answer":"(b) and (c) Only",
     "explanation":"The correct answer is (C) (b) and (c) Only. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict136","topic":"ICT","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match List - I with List - II. List - I (Malware) List - II (Definition) (a) Ransomware (I) Software that monitors and/or records the actions of targeted users. (b) Spyware (II) A small piece of code that misleads users of its true intent by disguising itself as a legitimate program and infects your computer when you run it. (c) Worm (III) Software that locks data files and demands a monetary payment in exchange for unlocking. (d) Trojan Horses (IV) A piece of code that replicates itself to other devices without user interaction",
     "options":["(a)-(II), (b)-(I), (c)-(IV), (d)-(III)", "(a)-(III), (b)-(IV), (c)-(I), (d)-(II)", "(a)-(I), (b)-(III), (c)-(II), (d)-(IV)", "(a)-(III), (b)-(I), (c)-(IV), (d)-(II)"],
     "correct_answer":"(a)-(III), (b)-(I), (c)-(IV), (d)-(II)",
     "explanation":"The correct answer is (D) (a)-(III), (b)-(I), (c)-(IV), (d)-(II). This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict137","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"Who among the following ancient scholars was a proponent of grammarian tradition?",
     "options":["Ishwarkrishna", "Bhaṛtṛhari", "Gautama", "Kaṇada"],
     "correct_answer":"Bhaṛtṛhari",
     "explanation":"The correct answer is (B) Bhaṛtṛhari. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict138","topic":"ICT","difficulty":"Hard","year":2024,"season":"June",
     "question":"Find out the correct chronological order of the following: (a) First binary computer by Britishers (b) Printing press (c) Plan for mechanical computer (d) Single-screen motion picture exhibition (e) First public broadcast of television",
     "options":["(a), (c), (e), (d), (b)", "(b), (c), (d), (e), (a)", "(c), (e), (a), (b), (d)", "(d), (a), (b), (c), (e)"],
     "correct_answer":"(b), (c), (d), (e), (a)",
     "explanation":"The correct answer is (B) (b), (c), (d), (e), (a). This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict139","topic":"ICT","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match List - I with List - II. List - I (Authors) List - II (Concepts) (a) Roland Barthes (I) Doxa (b) Pierre Bourdieu (II) Hegemony (c) Antonio Gramsci (III) Simulation (d) Jean Baudrillard (IV) Myth",
     "options":["(a)-(I), (b)-(II), (c)-(III), (d)-(IV)", "(a)-(II), (b)-(III), (c)-(IV), (d)-(I)", "(a)-(III), (b)-(IV), (c)-(I), (d)-(II)", "(a)-(IV), (b)-(I), (c)-(II), (d)-(III)"],
     "correct_answer":"(a)-(IV), (b)-(I), (c)-(II), (d)-(III)",
     "explanation":"The correct answer is (D) (a)-(IV), (b)-(I), (c)-(II), (d)-(III). This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict140","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"A relationship in which a less-experienced learner acquires knowledge and skills under the guidance of an expert is known as:",
     "options":["Cloud computing", "Cognitive load", "Cognitive apprenticeship", "Collective monologue"],
     "correct_answer":"Cognitive apprenticeship",
     "explanation":"The correct answer is (C) Cognitive apprenticeship. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict141","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"An Internet standard that allows for adding media attachments to an email is called:",
     "options":["MIME", "DHCP", "HDMI", "FTP"],
     "correct_answer":"MIME",
     "explanation":"The correct answer is (A) MIME. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict142","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"Mobile games were the first to popularize_________ which uses an image of an actual place or thing and adds digital information to it.",
     "options":["Virtual Reality", "Augmented Reality", "Mixed Reality", "Computer-Aided Design (CAD)"],
     "correct_answer":"Augmented Reality",
     "explanation":"The correct answer is (B) Augmented Reality. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict143","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"What does folklore contribute to public discourse?",
     "options":["It creates a public space for stress-free interaction", "It restricts the expression of ideas and values", "It promotes only traditional values", "It eliminates modern influences"],
     "correct_answer":"It creates a public space for stress-free interaction",
     "explanation":"The correct answer is (A) It creates a public space for stress-free interaction. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict144","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"If the sale of Wadilal increases by 38% from 2020 to 2023, and the percent sale of other companies accordingly stands reduced then what would be the market share of Wadilal in 2023?",
     "options":["17.5%", "18%", "16.94%", "16.05%"],
     "correct_answer":"16.05%",
     "explanation":"The correct answer is (D) 16.05%. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict145","topic":"ICT","difficulty":"Hard","year":2024,"season":"June",
     "question":"If (L)M represents a number L in base-M number system, then which of the following numbers are equivalent to (19)16? (a) (11001)2 (b) (201)3 (c) (121)4 (d) (101)5 (e) (25)10",
     "options":["(a), (c) and (e) Only", "(b) and (d) Only", "(a), (b) and (d) Only", "(a), (b), (c), (d) and (e)"],
     "correct_answer":"(a), (c) and (e) Only",
     "explanation":"The correct answer is (A) (a), (c) and (e) Only. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict146","topic":"ICT","difficulty":"Hard","year":2024,"season":"June",
     "question":"As a mode of communication, drama has four forms from the western perspective. They are: (a) Tragedy (b) Comedy (c) Serious drama (d) Melodrama (e) Character drama 230",
     "options":["(a), (b), (c), (d) Only", "(b), (c), (e) Only", "(a), (c), (d), (e) Only", "(a), (b), (d), (e) Only"],
     "correct_answer":"(a), (b), (c), (d) Only",
     "explanation":"The correct answer is (A) (a), (b), (c), (d) Only. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict147","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which of the following electronic technologies is the key technology for making the fourth generation electronic computer?",
     "options":["Transistor based", "Integrated Circuit (IC) based", "Vacuum Tube based", "Microprocessor based"],
     "correct_answer":"Microprocessor based",
     "explanation":"The correct answer is (D) Microprocessor based. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict148","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"Anna sits at her kitchen table and is able to think about what she needs to buy from the grocery stores. She is using her ability to:",
     "options":["Recognise", "Recite", "Recall", "Memorize"],
     "correct_answer":"Recall",
     "explanation":"The correct answer is (C) Recall. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict149","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"According to classical Indian Philosophy the source of knowledge based on cognition of an object, similar to another one which is already known to the cognizer is known as:",
     "options":["Śabda", "Pratyaksa", "Anumāna", "Upamāna"],
     "correct_answer":"Upamāna",
     "explanation":"The correct answer is (D) Upamāna. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict150","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"How often did the Ashram-Sammilani meet?",
     "options":["Once a year", "Twice a month", "Weekly", "Monthly"],
     "correct_answer":"Twice a month",
     "explanation":"The correct answer is (B) Twice a month. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict151","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"What principles did Rabindranath Tagore apply to Sriniketan's rural development program?",
     "options":["Centralized governance", "Industrial growth", "Equal respect, participation and distribution of wealth", "Personal growth over community welfare"],
     "correct_answer":"Equal respect, participation and distribution of wealth",
     "explanation":"The correct answer is (C) Equal respect, participation and distribution of wealth. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict152","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which among the following is a MOOC platform?",
     "options":["Diksha", "NROER", "EdX", "GoogleMeet"],
     "correct_answer":"EdX",
     "explanation":"The correct answer is (C) EdX. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict153","topic":"ICT","difficulty":"Medium","year":2024,"season":"June",
     "question":"In square of opposition, if the statement - 'No reptiles are warm blooded animals' is given as false, which of the following could be validly inferred from it? (a) 'All reptiles are warm blooded animals' is undetermined. (b) 'Some reptiles are warm blooded animals' is true. (c) 'Some reptiles are not warm blooded animals' is undetermined. (d) 'All reptiles are warm blooded animals' is true.",
     "options":["(a), (b) and (c) only", "(b) and (c) only", "(c) and (d) only", "(a) and (c) only"],
     "correct_answer":"(a), (b) and (c) only",
     "explanation":"The correct answer is (A) (a), (b) and (c) only. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict154","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which software among the following is used as a reference management tool?",
     "options":["Zotero", "Google Jamboard", "AUTOCAD", "Microsoft teams"],
     "correct_answer":"Zotero",
     "explanation":"The correct answer is (A) Zotero. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict155","topic":"ICT","difficulty":"Medium","year":2024,"season":"June",
     "question":"Identify the correct order of the following data transfer rates measured in bits per second (bps) ranked from smallest to largest: (a) 1500 Kbps (b) 1500 Mbps (c) 1 Mbps (d) 1 Gbps",
     "options":["(c), (a), (b), (d)", "(a), (c), (d), (b)", "(c), (d), (a), (b)", "(c), (a), (d), (b)"],
     "correct_answer":"(c), (a), (d), (b)",
     "explanation":"The correct answer is (D) (c), (a), (d), (b). This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict156","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"Suman uses her computer to edit a photograph. Which one of these is a peripheral device that could be used to edit a photograph?",
     "options":["Memory card", "Mouse", "Printer", "USB port"],
     "correct_answer":"Mouse",
     "explanation":"The correct answer is (B) Mouse. This is a standard UGC NET 2024 June question on ICT."},
    {"id":"ict1048","topic":"ICT","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match the List-I with List-II List -I (Nature of substances) List - II (Effect) (a) Allergens (I) Substances that cause cancer (b) Carcinogens (II) Substances that can hamper embryonic growth (c) Mutagens (III) Substances that activate the immune system (d) Teratogens (IV) Substances that can damage or alter genetic material",
     "options":["(a)-(IV), (b)-(I), (c)-(II), (d)-(III)", "(a)-(IV), (b)-(II), (c)-(I), (d)-(III)", "(a)-(III), (b)-(I), (c)-(II), (d)-(IV)", "(a)-(III), (b)-(I), (c)-(IV), (d)-(II)"],
     "correct_answer":"(a)-(III), (b)-(I), (c)-(IV), (d)-(II)",
     "explanation":"The correct answer is (D) (a)-(III), (b)-(I), (c)-(IV), (d)-(II). This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ict1053","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"ChatGPT is an AI chatbot developed by OpenAI and was launched in November 2022. What does ChatGPT stand for?",
     "options":["Chat Generative Pre-trained Transmission", "Chat General Pre-trained Technology", "Chat Generalized Pre-trained Technique", "Chat Generative Pre-trained Transformer"],
     "correct_answer":"Chat Generative Pre-trained Transformer",
     "explanation":"The correct answer is (D) Chat Generative Pre-trained Transformer. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ict1054","topic":"ICT","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match the List-I with List-II List - I (Kinds of classroom Resources) List - II (Description) (a) Simple Resources (I) Resources which are not easily bought, measured or adjusted, e.g. instructional approaches and teaching philosophies (b) Compound Resources (II) Resources difficult discern and measure and often embedded via web of relationship practices, decision making, teacher accountability etc. (c) Complex Resources (III) Physical object and can be directly bought, adjusted and measured e.g. textbooks, blackboards and chalks etc. (d) Abstract Resources (IV) Use of two or more than two resources such as class, size reduction and use of technology.",
     "options":["(a)-(I), (b)-(II), (c)-(III), (d)-(IV)", "(a)-(IV), (b)-(III), (c)-(II), (d)-(I)", "(a)-(IV), (b)-(III), (c)-(I), (d)-(II)", "(a)-(III), (b)-(IV), (c)-(II), (d)-(I)"],
     "correct_answer":"(a)-(III), (b)-(IV), (c)-(II), (d)-(I)",
     "explanation":"The correct answer is (D) (a)-(III), (b)-(IV), (c)-(II), (d)-(I). This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ict1058","topic":"ICT","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match the List-I with List-II List - I (Word) List - II (Unique code) (a) QUAKE (I) QDBBI (b) OFTEN (II) EQJUF (c) PEACH (III) RTBJF (d) DRIVE (IV) PEUDO",
     "options":["(a)-(I), (b)-(II), (c)-(III), (d)-(IV)", "(a)-(II), (b)-(III), (c)-(IV), (d)-(I)", "(a)-(IV), (b)-(I), (c)-(II), (d)-(III)", "(a)-(III), (b)-(IV), (c)-(I), (d)-(II)"],
     "correct_answer":"(a)-(III), (b)-(IV), (c)-(I), (d)-(II)",
     "explanation":"The correct answer is (D) (a)-(III), (b)-(IV), (c)-(I), (d)-(II). This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ict1059","topic":"ICT","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match the List-I with List-II List -I (Concept) List - II (Description) (a) Academic year (I) A unit by which the course work is measured. It defines the number of hours of instruction required per week (b) Credit Point (II) Papers taught under the programme duly defining the learning objectives and outcomes (c) Credit (III) Two consecutive (one odd and one even) semesters (d) Course (IV) The product of grade point and number of credits for a course",
     "options":["(a)-(III), (b)-(II), (c)-(IV), (d)-(I)", "(a)-(IV), (b)-(I), (c)-(III), (d)-(II)", "(a)-(III), (b)-(IV), (c)-(I), (d)-(II)", "(a)-(II), (b)-(III), (c)-(IV), (d)-(I)"],
     "correct_answer":"(a)-(III), (b)-(IV), (c)-(I), (d)-(II)",
     "explanation":"The correct answer is (C) (a)-(III), (b)-(IV), (c)-(I), (d)-(II). This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ict1060","topic":"ICT","difficulty":"Hard","year":2024,"season":"June",
     "question":"A language teacher wants to create visually appealing presentations / lessons with embedded videos and interactive slides to enhance online lessons. Which of the following tools are most suitable for this purpose? (a) Canva (b) Quizlet (c) Book Creator (d) Flipgrid (e) Adobe Illustrator",
     "options":["(b), (c) and (d) only", "(a), (c) and (e) only", "(b), (d) and (e) only", "(a) and (c) only"],
     "correct_answer":"(a) and (c) only",
     "explanation":"The correct answer is (D) (a) and (c) only. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ict1061","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"In the period of subject English, in a class, Ram is able to recall the author of the book ‘The diary of a young girl’. This type of memory is called _________",
     "options":["Procedural", "Semantic", "Episodic", "Constructive"],
     "correct_answer":"Semantic",
     "explanation":"The correct answer is (B) Semantic. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ict1062","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"The total value of a collection of coins of denomination Rs.20, Rs.10, Rs.5, Rs.2 and Rs. 1 is Rs.570. If the number of coins of each denomination is same, then the number of 1 Rs Coin is?",
     "options":["10", "12", "15", "18"],
     "correct_answer":"15",
     "explanation":"The correct answer is (C) 15. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ict1063","topic":"ICT","difficulty":"Medium","year":2024,"season":"June",
     "question":"In an examination a student scores 4 marks for every correct answer and loses 1 mark for every wrong answer. A student attempted all the 200 questions and scores 400 marks. The number of questions he answered correctly was:",
     "options":["60", "100", "120", "150"],
     "correct_answer":"120",
     "explanation":"The correct answer is (C) 120. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ict1064","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"In the month of September, the additional number of votes needed by A and B together to get 7% more votes than D is __________.",
     "options":["91300", "81500", "14400", "71200"],
     "correct_answer":"81500",
     "explanation":"The correct answer is (B) 81500. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ict1065","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"In all the six months combined _________% more votes are required by company A to equal the total votes polled by company D.",
     "options":["150", "145", "133", "88"],
     "correct_answer":"145",
     "explanation":"The correct answer is (B) 145. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ict1066","topic":"ICT","difficulty":"Medium","year":2024,"season":"June",
     "question":"The number of votes polled in favour of A and C, taken together in January, May and September is approximately _________% less than the number of votes polled in favour of B and D, taken together in March, July and November.",
     "options":["27", "37", "44", "18"],
     "correct_answer":"27",
     "explanation":"The correct answer is (A) 27. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ict1067","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"A teacher wants his students to watch pre-recorded videos and answer questions embedded in the videos. Which tool would be most suitable for this purpose?",
     "options":["Edpuzzle", "Evernote", "Google Docs", "Strawpoll"],
     "correct_answer":"Edpuzzle",
     "explanation":"The correct answer is (A) Edpuzzle. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ict1068","topic":"ICT","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match List I with List - II. List -I (Error Message in MS-EXCEL) List -II (Error Description) (a) # # # # # (I) When the formula contains a cell reference that is 141 pointing to an invalid cell (b) #VALUE! (II) When you divide a number by a cell that points to an empty cell (c) #REF! (III) When the arithmetic formula contains text instead of a number (d) #DIV/O (IV) When the cell contains a number that is too wide for the result to be displayed",
     "options":["(a)-(III), (b)-(IV), (c)-(II), (d)-(I)", "(a)-(IV), (b)-(III), (c)-(I), (d)-(II)", "(a)-(I), (b)-(IV), (c)-(II), (d)-(III)", "(a)-(IV), (b)-(I), (c)-(III), (d)-(II)"],
     "correct_answer":"(a)-(IV), (b)-(III), (c)-(I), (d)-(II)",
     "explanation":"The correct answer is (B) (a)-(IV), (b)-(III), (c)-(I), (d)-(II). This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ict1069","topic":"ICT","difficulty":"Medium","year":2024,"season":"June",
     "question":"Which of the following Anglican Missionary Societies were most involved in teaching in high schools and colleges across North India in later part of Ninetieth country? (a) The Church Missionary Society (b) The London Missionary Society (c) Society for the propagation of the Gospel (d) The Cambridge Mission to Delhi 142",
     "options":["(a) and (b) only", "(a), (b), (c), (d)", "(c) and (d) only", "(a), (c) and (d) only"],
     "correct_answer":"(a), (b), (c), (d)",
     "explanation":"The correct answer is (B) (a), (b), (c), (d). This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ict1070","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"What is the difference between the number of unsubscribed viewers and subscribed viewers, taking all the towns together?",
     "options":["320", "240", "340", "300"],
     "correct_answer":"240",
     "explanation":"The correct answer is (B) 240. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ict1071","topic":"ICT","difficulty":"Medium","year":2024,"season":"June",
     "question":"A security system used a camera to capture images of each person entering a gift shop. Each image taken requires 1 MB of storage. If the camera captures an image every 5 seconds over a 24-hour of period, how much storage is required?",
     "options":["16.875 GB", "15.250 GB", "12.525 GB", "19.625 GB"],
     "correct_answer":"16.875 GB",
     "explanation":"The correct answer is (A) 16.875 GB. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ict1072","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"The number and size of the brain's nerve endings continue to grow till:",
     "options":["Elementaty school years", "Early childhood", "Adulthood", "Adolescence"],
     "correct_answer":"Adolescence",
     "explanation":"The correct answer is (D) Adolescence. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ict1073","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"Number of people in age group III of city D is ________% more than that of age group II of city B.",
     "options":["7%", "6", "6", "6%"],
     "correct_answer":"6",
     "explanation":"The correct answer is (C) 6. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ict1074","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"Number of people of age group I is more than 4 lakhs in exactly _______city/cities.",
     "options":["one", "two", "three", "four"],
     "correct_answer":"two",
     "explanation":"The correct answer is (B) two. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ict1075","topic":"ICT","difficulty":"Medium","year":2024,"season":"June",
     "question":"A sum of money is equally divided among a number of children. Had there been 10 children less, each would have received ₹ 5 more, and had there been 10 children more each would have received ₹ 3 less. What is the sum of money that is distributed?",
     "options":["300", "600", "750", "900"],
     "correct_answer":"600",
     "explanation":"The correct answer is (B) 600. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ict1076","topic":"ICT","difficulty":"Easy","year":2024,"season":"June",
     "question":"15 men working 8 hours per day complete a piece of work in 18 days. To complete the same work in 6 days, working 12 hours a day, the number of men required will be:",
     "options":["24 men", "26 men", "28 men", "30 men"],
     "correct_answer":"30 men",
     "explanation":"The correct answer is (D) 30 men. This is a standard UGC NET 2024 June question on Teaching Aptitude."},


    # ↑↑↑ PASTE YOUR NEW ICT QUESTIONS ABOVE THIS LINE ↑↑↑
]

# ── 7. ENVIRONMENT & ECOLOGY ─────────────────────────────────────────
Q_ENVIRONMENT = [
    {"id":"env001","topic":"Environment & Ecology","difficulty":"Medium","year":2023,"season":"June","question":"The 'Paris Agreement' primarily addresses:","options":["Nuclear non-proliferation","Climate change and global warming","Trade barriers","Ozone depletion"],"correct_answer":"Climate change and global warming","explanation":"The Paris Agreement (2015) limits global warming to well below 2 degrees Celsius."},
    {"id":"env002","topic":"Environment & Ecology","difficulty":"Easy","year":2022,"season":"December","question":"Which gas is primarily responsible for the greenhouse effect?","options":["Oxygen","Nitrogen","Carbon Dioxide","Hydrogen"],"correct_answer":"Carbon Dioxide","explanation":"CO2 is the primary anthropogenic greenhouse gas."},
    {"id":"env003","topic":"Environment & Ecology","difficulty":"Hard","year":2021,"season":"June","question":"The 'Chipko Movement' in India was primarily associated with:","options":["Water conservation","Forest and tree conservation","Wildlife protection","Soil conservation"],"correct_answer":"Forest and tree conservation","explanation":"The Chipko Movement (1973) was a protest where villagers embraced trees to prevent their felling."},
    # ════════════════════════════════════════════════════════════════════
    # ADD MORE Environment & Ecology QUESTIONS BELOW ↓
    # ════════════════════════════════════════════════════════════════════
    {"id":"env004","topic":"Environment & Ecology","difficulty":"Medium","year":2024,"season":"June",
     "question":"The 'Montreal Protocol' was signed to protect:",
     "options":["Biodiversity","The ozone layer","Ocean ecosystems","Freshwater resources"],
     "correct_answer":"The ozone layer",
     "explanation":"The Montreal Protocol (1987) is an international treaty to phase out ozone-depleting substances like CFCs."},

    {"id":"env005","topic":"Environment & Ecology","difficulty":"Easy","year":2024,"season":"December",
     "question":"Which of the following is a renewable source of energy?",
     "options":["Coal","Natural gas","Solar energy","Nuclear energy"],
     "correct_answer":"Solar energy",
     "explanation":"Solar energy is a renewable resource — it is naturally replenished and will not deplete."},

    {"id":"env006","topic":"Environment & Ecology","difficulty":"Hard","year":2023,"season":"December",
     "question":"'Biomagnification' refers to:",
     "options":["Growth of microorganisms","Increase in pollutant concentration up the food chain","Expansion of forest cover","Population explosion"],
     "correct_answer":"Increase in pollutant concentration up the food chain",
     "explanation":"Biomagnification is the progressive increase in concentration of a substance (e.g. DDT) in organisms at successively higher trophic levels."},

    {"id":"env007","topic":"Environment & Ecology","difficulty":"Medium","year":2022,"season":"June",
     "question":"World Environment Day is celebrated on:",
     "options":["April 22","June 5","March 21","December 11"],
     "correct_answer":"June 5",
     "explanation":"World Environment Day is observed on June 5 every year, established by the UN in 1972."},

    {"id":"env008","topic":"Environment & Ecology","difficulty":"Hard","year":2021,"season":"December",
     "question":"Which Indian state has the highest forest cover percentage?",
     "options":["Kerala","Arunachal Pradesh","Madhya Pradesh","Mizoram"],
     "correct_answer":"Mizoram",
     "explanation":"Mizoram has the highest percentage of forest cover relative to its total geographical area (~85%)."},
        {"id":"env009","topic":"Environment & Ecology","difficulty":"Medium","year":2024,"season":"June",
     "question":"To understand the Global Climate Change, GCM model are widely used. GCM stands for (a) Global Circulation Model (b) General Circulation Model (c) Global Climate Model (d) General Climate Model",
     "options":["Only (a) and (b)", "Only (b) and (c)", "Only (c) and (d)", "Only (a) and (d)"],
     "correct_answer":"Only (b) and (c)",
     "explanation":"The correct answer is (B) Only (b) and (c). This is a standard UGC NET 2024 June question on Environment & Ecology."},
    {"id":"env010","topic":"Environment & Ecology","difficulty":"Easy","year":2024,"season":"June",
     "question":"When a water body becomes extremely low in nutrient content, then it is called as",
     "options":["Dystrophic", "Oligotrophic", "Mesotrophic", "Eutrophic"],
     "correct_answer":"Oligotrophic",
     "explanation":"The correct answer is (B) Oligotrophic. This is a standard UGC NET 2024 June question on Environment & Ecology."},
    {"id":"env011","topic":"Environment & Ecology","difficulty":"Easy","year":2024,"season":"June",
     "question":"In a breeder reactor",
     "options":["More fissile materials are produced than it is consumed", "Less fissile materials are produced than it is consumed", "Neutrons are slowed down by moderator", "U-238 a fissile material is produced from Pu-239 a fertile material."],
     "correct_answer":"More fissile materials are produced than it is consumed",
     "explanation":"The correct answer is (A) More fissile materials are produced than it is consumed. This is a standard UGC NET 2024 June question on Environment & Ecology."},
    {"id":"env012","topic":"Environment & Ecology","difficulty":"Hard","year":2024,"season":"June",
     "question":"Dissolved Oxygen (DO), a water quality parameter, is essential in which of the following water bodies/sources? (a) River Water (b) Lake Water (c) Tap Water (d) Underground Water (e) Pond Water",
     "options":["(a), (b) and (e) Only", "(c) and (d) Only", "(b), (d) and (e) Only", "(a), (c), (d) and (e) Only"],
     "correct_answer":"(a), (b) and (e) Only",
     "explanation":"The correct answer is (A) (a), (b) and (e) Only. This is a standard UGC NET 2024 June question on Environment & Ecology."},
    {"id":"env013","topic":"Environment & Ecology","difficulty":"Easy","year":2024,"season":"June",
     "question":"The convention of Biological Diversity (CBD) was first opened for signature during",
     "options":["Conference on human environment", "Earth Summit", "Montreal Protocol", "COP1"],
     "correct_answer":"Earth Summit",
     "explanation":"The correct answer is (B) Earth Summit. This is a standard UGC NET 2024 June question on Environment & Ecology."},
    {"id":"env014","topic":"Environment & Ecology","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which of the following Green House Gases (GHGs) was considered during the second compliance period of Kyoto protocol at Doha?",
     "options":["Sulphur Hexafluoride (SF6)", "Hydrofluoro Carbons (HFCs)", "Nitrogen Trifluoride (NF3)", "Perfluorocarbons (PFCs)"],
     "correct_answer":"Nitrogen Trifluoride (NF3)",
     "explanation":"The correct answer is (C) Nitrogen Trifluoride (NF3). This is a standard UGC NET 2024 June question on Environment & Ecology."},
    {"id":"env015","topic":"Environment & Ecology","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which of the following is an example of negative feedback in the context of climate change?",
     "options":["Oceans remove carbon dioxide from the air", "Warming increases water vapour in air", "Snow cover loss and iceshelf melt reduce sun's reflection", "Global temperature increases due to global warming"],
     "correct_answer":"Oceans remove carbon dioxide from the air",
     "explanation":"The correct answer is (A) Oceans remove carbon dioxide from the air. This is a standard UGC NET 2024 June question on Environment & Ecology."},
    {"id":"env016","topic":"Environment & Ecology","difficulty":"Hard","year":2024,"season":"June",
     "question":"Burning of solid waste, such as cans, batteries, plastic etc. generate (a) Microplastics (b) Chlorofluorocarbons (CFCs) (c) Dioxins (d) Polychlorinated biphenyls (PCBs) (e) Halons 24",
     "options":["(a), (b), (c) and (d) only", "(a), (c) and (d) only", "(b), (d) and (e) only", "(b), (c) and (e) only"],
     "correct_answer":"(a), (c) and (d) only",
     "explanation":"The correct answer is (B) (a), (c) and (d) only. This is a standard UGC NET 2024 June question on Environment & Ecology."},
    {"id":"env017","topic":"Environment & Ecology","difficulty":"Hard","year":2024,"season":"June",
     "question":"Which among the followings are global scale Phenomenon? (a) Ozone layer depletion (b) Global warming (c) Forest Fire (d) Sea level rise (e) Air pollution",
     "options":["(a), (c) and (d) Only", "(a), (b), (c) and (d) Only", "(b), (c) and (e) Only", "(a), (b) and (d) Only"],
     "correct_answer":"(a), (b) and (d) Only",
     "explanation":"The correct answer is (D) (a), (b) and (d) Only. This is a standard UGC NET 2024 June question on Environment & Ecology."},
    {"id":"env018","topic":"Environment & Ecology","difficulty":"Hard","year":2024,"season":"June",
     "question":"Arrange the following themes of Sustainable Development Goals according to their goal number in increasing order. (a) Gender Equality (b) Zero Hunger (c) Peace and Justice (d) Climate Action (e) Quality Education",
     "options":["(b), (e), (a), (d), (c)", "(a), (b), (d), (c), (e)", "(c), (d), (a), (e), (b)", "(b), (a), (e), (d), (c)"],
     "correct_answer":"(b), (e), (a), (d), (c)",
     "explanation":"The correct answer is (A) (b), (e), (a), (d), (c). This is a standard UGC NET 2024 June question on Environment & Ecology."},
    {"id":"env019","topic":"Environment & Ecology","difficulty":"Hard","year":2024,"season":"June",
     "question":"Arrange the following gases in ascending order of their global warming potential (GWD). (a) CO2 (b) CH4 (c) SF6 33 (d) CFC-11 (e) N₂O",
     "options":["(a), (b), (c), (e), (d)", "(a), (b), (e), (d), (c)", "(b), (c), (a), (e), (d)", "(a), (e), (b), (d), (c)"],
     "correct_answer":"(a), (b), (e), (d), (c)",
     "explanation":"The correct answer is (B) (a), (b), (e), (d), (c). This is a standard UGC NET 2024 June question on Environment & Ecology."},
    {"id":"env020","topic":"Environment & Ecology","difficulty":"Easy","year":2024,"season":"June",
     "question":"Based on the source of their food, organisms occupy a specific place in the food chain, known as:",
     "options":["Trophic level", "Standing crop", "Top level organism", "Species level"],
     "correct_answer":"Trophic level",
     "explanation":"The correct answer is (A) Trophic level. This is a standard UGC NET 2024 June question on Environment & Ecology."},
    {"id":"env021","topic":"Environment & Ecology","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match List - I with List II. List -I (International Meetings) List -II (Key objectives) (a) Kyoto protocol (I) Global warming (b) Montreal protocol (II) Biodiversity conservation (c) Rio Summit (III) Ozone depletion (d) Paris Agreement (IV) Solar Alliance",
     "options":["(a)-(I), (b)-(III), (c)-(II), (d)-(IV)", "(a)-(II), (b)-(III), (c)-(I), (d)-(IV)", "(a)-(III), (b)-(I), (c)-(IV), (d)-(II)", "(a)-(IV), (b)-(II), (c)-(I), (d)-(III)"],
     "correct_answer":"(a)-(I), (b)-(III), (c)-(II), (d)-(IV)",
     "explanation":"The correct answer is (A) (a)-(I), (b)-(III), (c)-(II), (d)-(IV). This is a standard UGC NET 2024 June question on Environment & Ecology."},
    {"id":"env022","topic":"Environment & Ecology","difficulty":"Easy","year":2024,"season":"June",
     "question":"In MS-EXCEL, a formula =B$1 + C$3 + 5 in cell D9 when copied to cell F12 will become:",
     "options":["= D1 + E3 = 5", "= B$2 + C$4 + 5", "= C$1 + D$3 + 5", "= D$1 + E$3 + 5"],
     "correct_answer":"= D$1 + E$3 + 5",
     "explanation":"The correct answer is (D) = D$1 + E$3 + 5. This is a standard UGC NET 2024 June question on Environment & Ecology."},
    {"id":"env023","topic":"Environment & Ecology","difficulty":"Hard","year":2024,"season":"June",
     "question":"Which among the followings are the renewable energy resources? (a) Biodiesel (b) Nuclear Energy (c) Solar Energy (d) Hydroelectric Energy (e) Wind Energy",
     "options":["(a), (b), (c), (d) only", "(b), (c), (d), (e) only", "(c), (d), (e), (a) only", "(e), (a), (b) only"],
     "correct_answer":"(c), (d), (e), (a) only",
     "explanation":"The correct answer is (C) (c), (d), (e), (a) only. This is a standard UGC NET 2024 June question on Environment & Ecology."},
    {"id":"env024","topic":"Environment & Ecology","difficulty":"Easy","year":2024,"season":"June",
     "question":"Indigenous Knowledge and Resource Management System is at best can be considered as-",
     "options":["Mitigation Response", "Adaptation Response", "Decarbonization Response", "Ethical Response"],
     "correct_answer":"Adaptation Response",
     "explanation":"The correct answer is (B) Adaptation Response. This is a standard UGC NET 2024 June question on Environment & Ecology."},
    {"id":"env025","topic":"Environment & Ecology","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match the List-I with List-II List - I (Sustainable Development Goals - SDG) List - II (Goal Number) (a) Zero Hunger (I) SDG-13 (b) Sustainable Cities and Communities (II) SDG-7 (c) Affordable and clean Energy (III) SDG-2 (d) Climate Action (IV) SDG-11",
     "options":["(a)-(III), (b)-(IV), (c)-(II), (d)-(I)", "(a)-(I), (b)-(II), (c)-(IV), (d)-(III)", "(a)-(II), (b)-(III), (c)-(I), (d)-(IV)", "(a)-(IV), (b)-(I), (c)-(III), (d)-(II)"],
     "correct_answer":"(a)-(III), (b)-(IV), (c)-(II), (d)-(I)",
     "explanation":"The correct answer is (A) (a)-(III), (b)-(IV), (c)-(II), (d)-(I). This is a standard UGC NET 2024 June question on Environment & Ecology."},
    {"id":"env026","topic":"Environment & Ecology","difficulty":"Medium","year":2024,"season":"June",
     "question":"What among the following can be ascribed to learning styles? (a) It is a way 'how' the student learns (b) They are strengths and preferences of the learners for responding to the stimuli in the 56 environment (c) It is 'Whať the learner learns (d) It is a behavioural pattern developed for any new learning",
     "options":["(a) and (b) only", "(a) and (c) only", "(a), (b), and (d) only", "(b), (c), and (d) only"],
     "correct_answer":"(a), (b), and (d) only",
     "explanation":"The correct answer is (C) (a), (b), and (d) only. This is a standard UGC NET 2024 June question on Environment & Ecology."},
    {"id":"env027","topic":"Environment & Ecology","difficulty":"Medium","year":2024,"season":"June",
     "question":"Eye irritation is the common phenomenon during smog. It is mostly caused by: (a) Formaldehyde (b) Per-oxy acetyl Nitrate (c) Ozone (d) Acrolin",
     "options":["(a), (b) and (c) only", "(a), (b) and (d) only", "(c), (d) and (a) only", "(b), (c) and (d) only"],
     "correct_answer":"(a), (b) and (d) only",
     "explanation":"The correct answer is (B) (a), (b) and (d) only. This is a standard UGC NET 2024 June question on Environment & Ecology."},
    {"id":"env028","topic":"Environment & Ecology","difficulty":"Hard","year":2024,"season":"June",
     "question":"Arrange the following states in ascending order according to their area under forest cover: (a) Arunachal Pradesh (b) Chhattisgarh (c) Maharastra (d) Odisha (e) Madhya Pradesh",
     "options":["(a), (c), (d), (b), (e)", "(c), (d), (b), (a), (e)", "(b), (a), (c), (e), (d)", "(d), (b), (a), (e), (c)"],
     "correct_answer":"(c), (d), (b), (a), (e)",
     "explanation":"The correct answer is (B) (c), (d), (b), (a), (e). This is a standard UGC NET 2024 June question on Environment & Ecology."},
    {"id":"env029","topic":"Environment & Ecology","difficulty":"Hard","year":2024,"season":"June",
     "question":"Which of the following National missions come under the National Action Plan for climate change? (a) National Solar mission (b) National Water mission 71 (c) National Green Hydrogen mission (d) National Mission for Sustainable Agriculture (e) National Mission on Sustainable Habitat",
     "options":["(a), (b), (c) and (d) Only", "(b), (c) and (e) Only", "(c), (d), (e) and (a) Only", "(d), (e), (a) and (b) Only"],
     "correct_answer":"(d), (e), (a) and (b) Only",
     "explanation":"The correct answer is (D) (d), (e), (a) and (b) Only. This is a standard UGC NET 2024 June question on Environment & Ecology."},
    {"id":"env030","topic":"Environment & Ecology","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match the List-I with List-II List - I (Organism) List - II (Trophic Level) (a) Lion (I) First Trophic level (b) Trees (II) Second Trophic level (c) Fish (III) Third Trophic level (d) Grasshopper (IV) Fourth Trophic level",
     "options":["(a)-(I), (b)-(IV), (c)-(II), (d)-(III)", "(a)-(IV), (b)-(I), (c)-(III), (d)-(II)", "(a)-(II), (b)-(III), (c)-(I), (d)-(IV)", "(a)-(III), (b)-(II), (c)-(IV), (d)-(I)"],
     "correct_answer":"(a)-(IV), (b)-(I), (c)-(III), (d)-(II)",
     "explanation":"The correct answer is (B) (a)-(IV), (b)-(I), (c)-(III), (d)-(II). This is a standard UGC NET 2024 June question on Environment & Ecology."},
    {"id":"env031","topic":"Environment & Ecology","difficulty":"Easy","year":2024,"season":"June",
     "question":"UNFCCC (United Nations Framework Connection on Climate Change) was outcome of which of the following meetings? 81",
     "options":["Montreal Protocol", "Stockholm Conference", "Rio Summit", "Kyoto Protocol"],
     "correct_answer":"Rio Summit",
     "explanation":"The correct answer is (C) Rio Summit. This is a standard UGC NET 2024 June question on Environment & Ecology."},
    {"id":"env032","topic":"Environment & Ecology","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which one of the following is not among \"three Rs\" a slogan: for solid waste management",
     "options":["Reduce", "Recover", "Recycle", "Reuse"],
     "correct_answer":"Recover",
     "explanation":"The correct answer is (B) Recover. This is a standard UGC NET 2024 June question on Environment & Ecology."},
    {"id":"env033","topic":"Environment & Ecology","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which one of the following is an example of positive feedback in the context of climate change?",
     "options":["Warmed earth radiates more infrared energy (heat) into space", "Plants remove carbon dioxide from the air", "Oceans remove carbon dioxide from the air", "Snow cover and ice shelf melting reduce reflection of sunlight"],
     "correct_answer":"Snow cover and ice shelf melting reduce reflection of sunlight",
     "explanation":"The correct answer is (D) Snow cover and ice shelf melting reduce reflection of sunlight. This is a standard UGC NET 2024 June question on Environment & Ecology."},
    {"id":"env034","topic":"Environment & Ecology","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which of the following is used to measure and monitor air pollution?",
     "options":["RADAR", "SONAR", "LIDAR", "SODAR"],
     "correct_answer":"LIDAR",
     "explanation":"The correct answer is (C) LIDAR. This is a standard UGC NET 2024 June question on Environment & Ecology."},
    {"id":"env035","topic":"Environment & Ecology","difficulty":"Easy","year":2024,"season":"June",
     "question":"What was the level Carbon dioxide (CO2) during pre-industrial era?",
     "options":["200 ppm", "280 ppm", "350 ppm", "420 ppm"],
     "correct_answer":"280 ppm",
     "explanation":"The correct answer is (B) 280 ppm. This is a standard UGC NET 2024 June question on Environment & Ecology."},
    {"id":"env036","topic":"Environment & Ecology","difficulty":"Easy","year":2024,"season":"June",
     "question":"Excess presence of which one of the following in drinking water can elevate the blood pressure of humans?",
     "options":["Sulphate", "Zinc", "Lead", "Copper"],
     "correct_answer":"Lead",
     "explanation":"The correct answer is (C) Lead. This is a standard UGC NET 2024 June question on Environment & Ecology."},
    {"id":"env037","topic":"Environment & Ecology","difficulty":"Medium","year":2024,"season":"June",
     "question":"Which of the following is/are Environmental Hazard(s) due to Geothermal Power Plants? (a) Noise pollution (b) Production of SO2 and NOX (c) Production of H₂S (toxic gas) (d) Production of CO2",
     "options":["(a) only", "(b) and (d) only", "(c) only", "(a), (b), (c) and (d)"],
     "correct_answer":"(a), (b), (c) and (d)",
     "explanation":"The correct answer is (D) (a), (b), (c) and (d). This is a standard UGC NET 2024 June question on Environment & Ecology."},
    {"id":"env038","topic":"Environment & Ecology","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match the List-I with List-II List - I (Fuel Type) List - II (Example) (a) Non fuel (I) Biodiesel (b) Alternative fuel (II) Hydrogen fuel cell (c) Non traditional fossil fuel (III) Wind power (d) Emerging fuel (IV) Compressed Natural Gas (CNG)",
     "options":["(a)-(II), (b)-(IV), (c)-(I), (d)-(III)", "(a)-(IV), (b)-(II), (c)-(III), (d)-(I)", "(a)-(І), (b)-(III), (c)-(IV), (d)-(II)", "(a)-(III), (b)-(I), (c)-(IV), (d)-(II)"],
     "correct_answer":"(a)-(III), (b)-(I), (c)-(IV), (d)-(II)",
     "explanation":"The correct answer is (D) (a)-(III), (b)-(I), (c)-(IV), (d)-(II). This is a standard UGC NET 2024 June question on Environment & Ecology."},
    {"id":"env039","topic":"Environment & Ecology","difficulty":"Hard","year":2024,"season":"June",
     "question":"Which of the following are true about International Solar Alliance (ISA)? (a) There are over 100 member countries in this alliance (b) Its head quarter is in Geneva, Switzerland (c) Most of its member countries lie between equator and tropic of cancer (d) Primary objective of alliance is to efficiently use solar energy (e) It is a collaborative initiative of India and France",
     "options":["(a), (b) and (d) only", "(a), (d) and (e) only", "(b), (c) and (e) only", "(c), (d) and (e) only"],
     "correct_answer":"(a), (d) and (e) only",
     "explanation":"The correct answer is (B) (a), (d) and (e) only. This is a standard UGC NET 2024 June question on Environment & Ecology."},
    {"id":"env040","topic":"Environment & Ecology","difficulty":"Hard","year":2024,"season":"June",
     "question":"Which of the following represent the nutrient contents of a water body at different levels? (a) Phototropic (b) Eutrophic (c) Mesotrophic (d) Chemotrophic (e) Oligotrophic",
     "options":["(a), (c) and (e) only", "(b), (c) and (d) only", "(a), (b) and (d) only", "(b), (c) and (e) only"],
     "correct_answer":"(b), (c) and (e) only",
     "explanation":"The correct answer is (D) (b), (c) and (e) only. This is a standard UGC NET 2024 June question on Environment & Ecology."},
    {"id":"env041","topic":"Environment & Ecology","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which of the following green house gases trapped in large quantity in permafrost and hydrates will likely be released in atmosphere due to global warming?",
     "options":["Nitrous Oxide (N2O)", "Methane (CH4)", "Chlorofluorocarbons (CFCs)", "Hydrofluorocarbons (HFCs)"],
     "correct_answer":"Methane (CH4)",
     "explanation":"The correct answer is (B) Methane (CH4). This is a standard UGC NET 2024 June question on Environment & Ecology."},
    {"id":"env042","topic":"Environment & Ecology","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match the List-I with List-II List - I (Sustainable Development Goal (SDG) List - II (SDG No) (a) Climate action (I) SDG 12 (b) Life on Land (II) SDG 13 (c) Responsible consumption and production (III) SDG 14 (d) Life below water (IV) SDG 15",
     "options":["(a)-(I), (b)-(III), (c)-(II), (d)-(IV)", "(a)-(III), (b)-(I), (c)-(IV), (d)-(II)", "(a)-(II), (b)-(IV), (c)-(III), (d)-(I)", "(a)-(II), (b)-(IV), (c)-(I), (d)-(III)"],
     "correct_answer":"(a)-(II), (b)-(IV), (c)-(I), (d)-(III)",
     "explanation":"The correct answer is (D) (a)-(II), (b)-(IV), (c)-(I), (d)-(III). This is a standard UGC NET 2024 June question on Environment & Ecology."},
    {"id":"env043","topic":"Environment & Ecology","difficulty":"Easy","year":2024,"season":"June",
     "question":"Doha amendment is an amendment to.",
     "options":["Montreal Protocol", "Kyoto Protocol", "Stockholm Convention", "Rio Summit"],
     "correct_answer":"Kyoto Protocol",
     "explanation":"The correct answer is (B) Kyoto Protocol. This is a standard UGC NET 2024 June question on Environment & Ecology."},
    {"id":"env044","topic":"Environment & Ecology","difficulty":"Hard","year":2024,"season":"June",
     "question":"Which of the following are true about class I and class II ozone depleting substances? (a) Ozone depleting potential of class-I substances are far more than class II (b) Ozone depleting potential of class II substances are far more than class I (c) All chlorofluoro carbons belong to class II ozone depleting substances (d) HCFC-21 belongs to class II ozone depleting substance (e) Class-I contains fully halogenated gases",
     "options":["(a), (d) and (e) only", "(b), (c) and (e) only", "(a), (c) and (d) only", "(c), (d) and (e) only"],
     "correct_answer":"(a), (d) and (e) only",
     "explanation":"The correct answer is (A) (a), (d) and (e) only. This is a standard UGC NET 2024 June question on Environment & Ecology."},
    {"id":"env045","topic":"Environment & Ecology","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which of the following harmful substances are produced upon combustion of tobacco?",
     "options":["Hydrogen cyanide and methane", "Carbon monoxide and carbon dioxide", "Nicotine and ammonia", "Hydrogen cyanide, carbon monoxide and ammonia"],
     "correct_answer":"Hydrogen cyanide, carbon monoxide and ammonia",
     "explanation":"The correct answer is (D) Hydrogen cyanide, carbon monoxide and ammonia. This is a standard UGC NET 2024 June question on Environment & Ecology."},
    {"id":"env046","topic":"Environment & Ecology","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which one of the following is used as a reference to measure the Global Warning Potential (GWP) of a green house gas?",
     "options":["Carbon dioxide (CO2)", "Methane (CH4)", "Chlorofluorocarbon (CFC)", "Hydrofluorocarbon (HFC)"],
     "correct_answer":"Carbon dioxide (CO2)",
     "explanation":"The correct answer is (A) Carbon dioxide (CO2). This is a standard UGC NET 2024 June question on Environment & Ecology."},
    {"id":"env047","topic":"Environment & Ecology","difficulty":"Easy","year":2024,"season":"June",
     "question":"Montreal Protocol is related to protection of.",
     "options":["Biodiversity", "Glaciers", "Oceans", "Stratospheric ozone layer"],
     "correct_answer":"Stratospheric ozone layer",
     "explanation":"The correct answer is (D) Stratospheric ozone layer. This is a standard UGC NET 2024 June question on Environment & Ecology."},
    {"id":"env048","topic":"Environment & Ecology","difficulty":"Easy","year":2024,"season":"June",
     "question":"Sustainable Development Goal 7 is related to.",
     "options":["Gender Equality", "Climate Action", "Affordable and Clean energy", "Quality Education"],
     "correct_answer":"Affordable and Clean energy",
     "explanation":"The correct answer is (C) Affordable and Clean energy. This is a standard UGC NET 2024 June question on Environment & Ecology."},
    {"id":"env049","topic":"Environment & Ecology","difficulty":"Medium","year":2024,"season":"June",
     "question":"Identify the correct statements. (a) Conservations is all about caring for the species we love and admire (b) Communities have been living in ecological harmony for the last two centuries (c) Field ecologists have contributed to our understanding about the value of different species in our lives (d) Salim Ali is considered as pioneer in India in the field of mainstream ecology",
     "options":["(a) and (b) only", "(b) and (c) only", "(c) and (d) only", "(a) and (d) only"],
     "correct_answer":"(c) and (d) only",
     "explanation":"The correct answer is (C) (c) and (d) only. This is a standard UGC NET 2024 June question on Environment & Ecology."},
    {"id":"env050","topic":"Environment & Ecology","difficulty":"Easy","year":2024,"season":"June",
     "question":"Modern environment consciousness is.",
     "options":["~ 20 years old", "~ 40 years old", "~ 60 years old", "~ 100 years old"],
     "correct_answer":"~ 60 years old",
     "explanation":"The correct answer is (C) ~ 60 years old. This is a standard UGC NET 2024 June question on Environment & Ecology."},
    {"id":"env051","topic":"Environment & Ecology","difficulty":"Hard","year":2024,"season":"June",
     "question":"Benefits of biodiesel over petrodiesel are: (a) Biodiesel contains virtually no sulfur (b) Biodiesel emits substantially lower carbon monoxide (CO) (c) Biodiesel is a better lubricant than petrodiesel. (d) Biodiesel emits significantly lower Oxides of Nitrogen Oxides (NOx) than petrodiesel. (e) Particulate emission by biodiesel is much lower that that of petrodiesel.",
     "options":["(a), (b), (c), (d) only", "(b), (c), (d), (e) only", "(a), (b), (c), (e) only", "(a), (b), (d), (e) only"],
     "correct_answer":"(a), (b), (c), (e) only",
     "explanation":"The correct answer is (C) (a), (b), (c), (e) only. This is a standard UGC NET 2024 June question on Environment & Ecology."},
    {"id":"env052","topic":"Environment & Ecology","difficulty":"Easy","year":2024,"season":"June",
     "question":"Temporary hardness in water is also known as:",
     "options":["Sulphate hardness", "Nitrate hardness", "Chloride hardness", "Carbonate hardness"],
     "correct_answer":"Carbonate hardness",
     "explanation":"The correct answer is (D) Carbonate hardness. This is a standard UGC NET 2024 June question on Environment & Ecology."},
    {"id":"env053","topic":"Environment & Ecology","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which of the following is correct chronological order of earliest to latest of different acts according to their year of enactment in India?",
     "options":["The Environment Protection Act, Air (Prevention and Control of Pollution) Act, Water", "Air (Prevention and Control of Pollution) Act, The Environment Protection Act, Water", "Water (Prevention and Control of Pollution) Act, The Environment Protection Act, Air", "Water (Prevention and Control of Pollution) Act, Air (Prevention and Control of Pollution) Act,"],
     "correct_answer":"Water (Prevention and Control of Pollution) Act, Air (Prevention and Control of Pollution) Act,",
     "explanation":"The correct answer is (D) Water (Prevention and Control of Pollution) Act, Air (Prevention and Control of Pollution) Act,. This is a standard UGC NET 2024 June question on Environment & Ecology."},
    {"id":"env054","topic":"Environment & Ecology","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which of the following is true about over fertile lake?",
     "options":["Nitrate level decreases", "Depletion in algal productivity", "Oxygen level increases", "Quality of fishes produced is impaired"],
     "correct_answer":"Quality of fishes produced is impaired",
     "explanation":"The correct answer is (D) Quality of fishes produced is impaired. This is a standard UGC NET 2024 June question on Environment & Ecology."},
    {"id":"env055","topic":"Environment & Ecology","difficulty":"Medium","year":2024,"season":"June",
     "question":"Which of the following came as alternatives to chlorofluorocarbons (CFCs) as refrigerants? (a) Hydrofluorocarbons (b) Perfluorocarbons 191 (c) Hydrochlorofluorocarbons (d) Halons",
     "options":["(a), (b) and (c) only", "(b), (c) and (d) only", "(b) and (d) only", "(a) and (c) only"],
     "correct_answer":"(a) and (c) only",
     "explanation":"The correct answer is (D) (a) and (c) only. This is a standard UGC NET 2024 June question on Environment & Ecology."},
    {"id":"env056","topic":"Environment & Ecology","difficulty":"Easy","year":2024,"season":"June",
     "question":"International Solar Alliance (ISA) is the alliance of countries, most of which lie.",
     "options":["Between North Pole and Tropic of cancer", "Between Tropic of Capricorn and South Pole", "At equator", "Between Tropic of cancer and Tropic of Capricorn"],
     "correct_answer":"Between Tropic of cancer and Tropic of Capricorn",
     "explanation":"The correct answer is (D) Between Tropic of cancer and Tropic of Capricorn. This is a standard UGC NET 2024 June question on Environment & Ecology."},
    {"id":"env057","topic":"Environment & Ecology","difficulty":"Easy","year":2024,"season":"June",
     "question":"Hydrochlorofluorocarbons (HCFCs), replacement for chlorofluorocarbons (CFCs), have to be phased out completely by the year",
     "options":["2025", "2030", "2035", "2040"],
     "correct_answer":"2030",
     "explanation":"The correct answer is (B) 2030. This is a standard UGC NET 2024 June question on Environment & Ecology."},
    {"id":"env058","topic":"Environment & Ecology","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which one of the following is a chemical parameter to measure the water quality?",
     "options":["Turbidity", "Temperature", "Hardness", "Color"],
     "correct_answer":"Hardness",
     "explanation":"The correct answer is (C) Hardness. This is a standard UGC NET 2024 June question on Environment & Ecology."},
    {"id":"env059","topic":"Environment & Ecology","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which one of the following agreements/protocols mainly focuses on the curbing of global temperature rise?",
     "options":["Montreal Protocol", "Kigali Agreement", "Kyoto Protocol", "Paris Agreement"],
     "correct_answer":"Paris Agreement",
     "explanation":"The correct answer is (D) Paris Agreement. This is a standard UGC NET 2024 June question on Environment & Ecology."},
    {"id":"env060","topic":"Environment & Ecology","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which of the following is not a disease caused due to exposure of Ultra Violet (UV)-rays, one of the Environmental hazards due to ozone layer depletion?",
     "options":["Melanoma", "Erythema", "Teratoma", "Carcinoma"],
     "correct_answer":"Teratoma",
     "explanation":"The correct answer is (C) Teratoma. This is a standard UGC NET 2024 June question on Environment & Ecology."},
    {"id":"env061","topic":"Environment & Ecology","difficulty":"Easy","year":2024,"season":"June",
     "question":"Because of Biochemical Oxygen Demand (BOD), Dissolved Oxygen (DO) of a water body:",
     "options":["Increases", "Decreases", "Remains unchanged", "Initially increases and then decreases"],
     "correct_answer":"Decreases",
     "explanation":"The correct answer is (B) Decreases. This is a standard UGC NET 2024 June question on Environment & Ecology."},
    {"id":"env062","topic":"Environment & Ecology","difficulty":"Easy","year":2024,"season":"June",
     "question":"What is the mission of International Solar Alliance?",
     "options":["Every home no matter how far will have electricity", "Every home will harvest solar energy", "Every home no matter how far away will have light at home", "Every home has to be carbon neutral"],
     "correct_answer":"Every home no matter how far away will have light at home",
     "explanation":"The correct answer is (C) Every home no matter how far away will have light at home. This is a standard UGC NET 2024 June question on Environment & Ecology."},
    {"id":"env063","topic":"Environment & Ecology","difficulty":"Medium","year":2024,"season":"June",
     "question":"Which of the following statements about email are true? (a) You can add signatures to your emails to give personal contact details (b) email stands for electrical mail (c) BCC stands for Blind Carbon Copy (d) Using the CC (Carbon Copy) feature of email will hide all other recipients from each other",
     "options":["(a) and (d) only", "(a) and (b) only", "(a) and (c) only", "(c) and (d) only"],
     "correct_answer":"(a) and (c) only",
     "explanation":"The correct answer is (C) (a) and (c) only. This is a standard UGC NET 2024 June question on Environment & Ecology."},
    {"id":"env064","topic":"Environment & Ecology","difficulty":"Medium","year":2024,"season":"June",
     "question":"Chlorofluoro Carbons (CFCs): (a) destroy ozone molecules (b) increase the atmospheric temperature (c) produce secondary aerosols (d) decrease the atmospheric temperature",
     "options":["(a), (b), (c) and (d)", "(b), (c) and (d) only", "(a), (c) and (d) only", "(a) and (b) only"],
     "correct_answer":"(a) and (b) only",
     "explanation":"The correct answer is (D) (a) and (b) only. This is a standard UGC NET 2024 June question on Environment & Ecology."},
    {"id":"env065","topic":"Environment & Ecology","difficulty":"Easy","year":2024,"season":"June",
     "question":"The Air (Prevention and control of pollution) Act was legislated in:",
     "options":["1981", "1986", "1989", "1991"],
     "correct_answer":"1981",
     "explanation":"The correct answer is (A) 1981. This is a standard UGC NET 2024 June question on Environment & Ecology."},
    {"id":"env958","topic":"Environment & Ecology","difficulty":"Easy","year":2024,"season":"June",
     "question":"Due to over fertilization of lakes, quality of fish produced",
     "options":["does not change", "impaires", "improves", "first improves then impaires"],
     "correct_answer":"impaires",
     "explanation":"The correct answer is (B) impaires. This is a standard UGC NET 2024 June question on Indian Constitution & Governance."},


    # ↑↑↑ PASTE YOUR NEW Environment & Ecology QUESTIONS ABOVE THIS LINE ↑↑↑
]

# ── 8. HIGHER EDUCATION ──────────────────────────────────────────────
Q_HIGHER_EDUCATION = [
    {"id":"he001","topic":"Higher Education","difficulty":"Medium","year":2023,"season":"December","question":"The NEP 2020 recommends the school curriculum to be restructured as:","options":["10+2","5+3+3+4","8+4","6+3+2+1"],"correct_answer":"5+3+3+4","explanation":"NEP 2020 proposes a 5+3+3+4 curricular structure."},
    {"id":"he002","topic":"Higher Education","difficulty":"Easy","year":2022,"season":"June","question":"UGC stands for:","options":["University Grants Commission","United Graduates Council","Universal Government College","University General Council"],"correct_answer":"University Grants Commission","explanation":"UGC is the statutory body for coordination and maintenance of standards in higher education."},
    {"id":"he003","topic":"Higher Education","difficulty":"Hard","year":2020,"season":"December","question":"'Autonomous Institutions' in Indian higher education means:","options":["Complete independence","Freedom to design curriculum and conduct exams","Government-funded colleges","Deemed universities"],"correct_answer":"Freedom to design curriculum and conduct exams","explanation":"Autonomous institutions have freedom to design curriculum, conduct exams, and declare results."},
    # ════════════════════════════════════════════════════════════════════
    # ADD MORE Higher Education QUESTIONS BELOW ↓
    # ════════════════════════════════════════════════════════════════════
    {"id":"he004","topic":"Higher Education","difficulty":"Medium","year":2024,"season":"June",
     "question":"NAAC accreditation in India is given on a scale of:",
     "options":["1 to 5","A++ to C","A++ to D","Pass/Fail"],
     "correct_answer":"A++ to C",
     "explanation":"NAAC grades institutions on a seven-point scale: A++, A+, A, B++, B+, B, and C."},

    {"id":"he005","topic":"Higher Education","difficulty":"Easy","year":2024,"season":"December",
     "question":"The full form of SWAYAM is:",
     "options":["Study Webs of Active Learning for Young Aspiring Minds","Smart Web Access for Youth and Management","Students Web for Active Youth Academic Module","None of these"],
     "correct_answer":"Study Webs of Active Learning for Young Aspiring Minds",
     "explanation":"SWAYAM is India's MOOCs platform launched in 2017 offering free online courses from school to PG level."},

    {"id":"he006","topic":"Higher Education","difficulty":"Hard","year":2023,"season":"June",
     "question":"Under NEP 2020, the multidisciplinary education and research universities (MERUs) are modelled on:",
     "options":["IITs","IIMs","Ivy League universities","Global research universities like MIT"],
     "correct_answer":"Global research universities like MIT",
     "explanation":"NEP 2020 envisions MERUs as world-class, multidisciplinary institutions comparable to global leaders like MIT and Stanford."},

    {"id":"he007","topic":"Higher Education","difficulty":"Medium","year":2022,"season":"December",
     "question":"The 'Open Book Examination' system primarily aims to test:",
     "options":["Memorisation ability","Higher-order thinking and application","Speed of writing","Knowledge of textbook content"],
     "correct_answer":"Higher-order thinking and application",
     "explanation":"Open book exams shift focus from rote memorisation to application, analysis, and synthesis of knowledge."},
        {"id":"he008","topic":"Higher Education","difficulty":"Hard","year":2024,"season":"June",
     "question":"Which of the following universities were multi-disciplinary in ancient India? (a) Banaras Hindu University (b) Takshashila (c) Nalanda (d) Vallabhi (e) Vikramshila",
     "options":["Only (a), (b), (c)", "Only (a), (c), (e)", "Only (a), (d), (e)", "Only (b), (c), (d), (e)"],
     "correct_answer":"Only (b), (c), (d), (e)",
     "explanation":"The correct answer is (D) Only (b), (c), (d), (e). This is a standard UGC NET 2024 June question on Higher Education."},
    {"id":"he009","topic":"Higher Education","difficulty":"Hard","year":2024,"season":"June",
     "question":"The National Education Policy, 2020 recommended the integration of humanities at the undergraduate level with subjects of (a) Science (b) Technology (c) Engineering (d) Mathematics (e) Propaganda techniques",
     "options":["Only (a), (b), (c), (d)", "Only (b), (c), (e)", "Only (a), (c), (d), (e)", "Only (a), (b), (d), (e)"],
     "correct_answer":"Only (a), (b), (c), (d)",
     "explanation":"The correct answer is (A) Only (a), (b), (c), (d). This is a standard UGC NET 2024 June question on Higher Education."},
    {"id":"he010","topic":"Higher Education","difficulty":"Easy","year":2024,"season":"June",
     "question":"The National Education Policy, 2020 aims to create",
     "options":["fragmented universities", "online universities", "knowledge hubs", "corporate clusters of education"],
     "correct_answer":"knowledge hubs",
     "explanation":"The correct answer is (C) knowledge hubs. This is a standard UGC NET 2024 June question on Higher Education."},
    {"id":"he011","topic":"Higher Education","difficulty":"Hard","year":2024,"season":"June",
     "question":"Dr. Baba Saheb Ambedkar was associated with: (a) Presidency College, Kolkata (b) Khalsa College, Mumbai (c) Siddharth College, Mumbai (d) Milind College, Aurangabad (e) National College, Bengaluru",
     "options":["Only (a), (b), (c)", "Only (b), (c), (d)", "Only (c), (d), (e)", "Only (a), (d), (e)"],
     "correct_answer":"Only (b), (c), (d)",
     "explanation":"The correct answer is (B) Only (b), (c), (d). This is a standard UGC NET 2024 June question on Higher Education."},
    {"id":"he012","topic":"Higher Education","difficulty":"Easy","year":2024,"season":"June",
     "question":"An important feature of the third five year plan was",
     "options":["Abolition of Education Commission.", "Reduction in the number of colleges", "Setting up examination research units in some universities", "More emphasis on open book examination."],
     "correct_answer":"Setting up examination research units in some universities",
     "explanation":"The correct answer is (C) Setting up examination research units in some universities. This is a standard UGC NET 2024 June question on Higher Education."},
    {"id":"he013","topic":"Higher Education","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match the List-I with List-II: List - I (Five year plan) List - II (Agency set up) (a) First five year plan (I) Autonomous colleges (b) Second five year plan (II) University Grants Commission (c) Third five year plan (III) Specialized departments of scientific study (d) Fifth five year plan (IV) Two rural institutes in Wardha and Mysore",
     "options":["(a)-(I), (b)-(II), (c)-(III), (d)-(IV)", "(a)-(II), (b)-(III), (c)-(IV), (d)-(I)", "(a)-(III), (b)-(IV), (c)-(I), (d)-(II)", "(a)-(IV), (b)-(I), (c)-(II), (d)-(III)"],
     "correct_answer":"(a)-(II), (b)-(III), (c)-(IV), (d)-(I)",
     "explanation":"The correct answer is (B) (a)-(II), (b)-(III), (c)-(IV), (d)-(I). This is a standard UGC NET 2024 June question on Higher Education."},
    {"id":"he014","topic":"Higher Education","difficulty":"Hard","year":2024,"season":"June",
     "question":"The components of quality education identified in the national education policy of 2020 are: (a) Political affiliation (b) Curriculum (c) Pedagogy (d) Continuous assessment (e) Higher fee",
     "options":["(a), (b) only", "(b), (c), (d) only", "(c), (d), (e) only", "(a), (c), (e) only"],
     "correct_answer":"(b), (c), (d) only",
     "explanation":"The correct answer is (B) (b), (c), (d) only. This is a standard UGC NET 2024 June question on Higher Education."},
    {"id":"he015","topic":"Higher Education","difficulty":"Easy","year":2024,"season":"June",
     "question":"The National Education policy, 2020 supported the idea of:",
     "options":["Science only education", "Fragmented research", "Rigorous specialization", "Segregating humanities and science"],
     "correct_answer":"Rigorous specialization",
     "explanation":"The correct answer is (C) Rigorous specialization. This is a standard UGC NET 2024 June question on Higher Education."},
    {"id":"he016","topic":"Higher Education","difficulty":"Hard","year":2024,"season":"June",
     "question":"Arrange the following open Universities according to their year of establishment in Chronological order (Older - New): (a) Yashwant Rao Chavan Maharashtra Open University (b) Karnataka State Open University (c) U.P. Rajarshi Tandon Open University (d) Kota Open University (e) Madhya Pradesh Bhoj Open University",
     "options":["(a), (b), (c), (d), (e)", "(d), (a), (e), (b), (c)", "(b), (c), (e), (a), (d)", "(d), (a), (b), (c), (e)"],
     "correct_answer":"(d), (a), (e), (b), (c)",
     "explanation":"The correct answer is (B) (d), (a), (e), (b), (c). This is a standard UGC NET 2024 June question on Higher Education."},
    {"id":"he017","topic":"Higher Education","difficulty":"Easy","year":2024,"season":"June",
     "question":"In ancient India, Ujjain was famous for the study of:",
     "options":["Anthropology", "Astronomy", "Archaeology", "Geology"],
     "correct_answer":"Astronomy",
     "explanation":"The correct answer is (B) Astronomy. This is a standard UGC NET 2024 June question on Higher Education."},
    {"id":"he018","topic":"Higher Education","difficulty":"Hard","year":2024,"season":"June",
     "question":"Which of the following universities were set up in 1916? (a) Osmania University (b) S.N.D.T Women's University (c) Mysore University (d) Patna University (e) Benaras Hindu University",
     "options":["(a), (b) and (c) only", "(b), (c) and (e) only", "(b), (c) and (d) only", "(a), (d) and (e) only"],
     "correct_answer":"(b), (c) and (e) only",
     "explanation":"The correct answer is (B) (b), (c) and (e) only. This is a standard UGC NET 2024 June question on Higher Education."},
    {"id":"he019","topic":"Higher Education","difficulty":"Medium","year":2024,"season":"June",
     "question":"Arrange the following ancient Indian Institutes from East to West direction. (a) Takshashila (b) Nalanda (c) Vikramshila (d) Shardapeeth",
     "options":["(a), (d), (c), (b)", "(b), (c), (a), (d)", "(d), (a), (b), (c)", "(c), (b), (d), (a)"],
     "correct_answer":"(c), (b), (d), (a)",
     "explanation":"The correct answer is (D) (c), (b), (d), (a). This is a standard UGC NET 2024 June question on Higher Education."},
    {"id":"he020","topic":"Higher Education","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which of the following recommended the linkages of Universities with outside autonomous research organisations?",
     "options":["Indian Council of Medical Research", "Education Commission (1964-66)", "Indian Council of Agricultural Research", "Calcutta university Commission"],
     "correct_answer":"Education Commission (1964-66)",
     "explanation":"The correct answer is (B) Education Commission (1964-66). This is a standard UGC NET 2024 June question on Higher Education."},
    {"id":"he021","topic":"Higher Education","difficulty":"Easy","year":2024,"season":"June",
     "question":"The National Education Policy, 2020, emphasised the need to standardise:",
     "options":["The Indian tribal dialects", "The vanishing languages", "The Indian Sign Languages (ISL)", "The classical languages"],
     "correct_answer":"The Indian Sign Languages (ISL)",
     "explanation":"The correct answer is (C) The Indian Sign Languages (ISL). This is a standard UGC NET 2024 June question on Higher Education."},
    {"id":"he022","topic":"Higher Education","difficulty":"Easy","year":2024,"season":"June",
     "question":"The Mashelkar Committee recommended upgradation of Regional Engineering Colleges into:",
     "options":["National Institutes of Technology", "National Technical Institute", "National Engineering Colleges", "National Technical Colleges"],
     "correct_answer":"National Institutes of Technology",
     "explanation":"The correct answer is (A) National Institutes of Technology. This is a standard UGC NET 2024 June question on Higher Education."},
    {"id":"he023","topic":"Higher Education","difficulty":"Easy","year":2024,"season":"June",
     "question":"The ancient grammarian Panini was a student at which of the following ancient places of learning?",
     "options":["Takshashila", "Nalanda", "Sridhanya Katak", "Odantapuri"],
     "correct_answer":"Takshashila",
     "explanation":"The correct answer is (A) Takshashila. This is a standard UGC NET 2024 June question on Higher Education."},
    {"id":"he024","topic":"Higher Education","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match the List-I with List-II. List - I List - II 93 (Forerunner college) (University) (a) Muir Central College (I) Lucknow University (b) Oriental College (II) Allahabad University (c) University College (III) Aligarh University (d) Canning College (IV) Punjab University",
     "options":["(a)-(I), (b)-(II), (c)-(III), (d)-(IV)", "(a)-(II), (b)-(III), (c)-(IV), (d)-(I)", "(a)-(III), (b)-(IV), (c)-(I), (d)-(II)", "(a)-(IV), (b)-(I), (c)-(II), (d)-(III)"],
     "correct_answer":"(a)-(II), (b)-(III), (c)-(IV), (d)-(I)",
     "explanation":"The correct answer is (B) (a)-(II), (b)-(III), (c)-(IV), (d)-(I). This is a standard UGC NET 2024 June question on Higher Education."},
    {"id":"he025","topic":"Higher Education","difficulty":"Easy","year":2024,"season":"June",
     "question":"One of the major recommendations of the National Education Policy, 2020, is the establishment of _________ for restructuring higher education in India.",
     "options":["Science universities", "Autonomous colleges", "Technology clubs", "Higher Education Institutions clusters"],
     "correct_answer":"Autonomous colleges",
     "explanation":"The correct answer is (B) Autonomous colleges. This is a standard UGC NET 2024 June question on Higher Education."},
    {"id":"he026","topic":"Higher Education","difficulty":"Easy","year":2024,"season":"June",
     "question":"The ancient buildings named Ratnasagara, Ratnadadhi and Ratnaranjaka were part of which of the following university of ancient India?",
     "options":["Takshashila", "Odantapuri", "Nalanda", "Sridhanya Katak"],
     "correct_answer":"Nalanda",
     "explanation":"The correct answer is (C) Nalanda. This is a standard UGC NET 2024 June question on Higher Education."},
    {"id":"he027","topic":"Higher Education","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match List - I with List - II. List – I (Commissions) List – II (Major Recommendation) (a) Knowledge Commission (I) Grants for collegiate education (b) Council of Education (Pre-Independence) (II) Improvement of teaching at the university level (c) Hunter Commission (III) Establishment of 50 National Universities (d) Kothari Commission (IV) Setting up a university in Bengal",
     "options":["(a)-(I), (b)-(II), (c)-(III), (d)-(IV)", "(a)-(II), (b)-(III), (c)-(IV), (d)-(I)", "(a)-(ІII), (b)-(IV), (c)-(I), (d)-(II)", "(a)-(IV), (b)-(I), (c)-(II), (d)-(III)"],
     "correct_answer":"(a)-(ІII), (b)-(IV), (c)-(I), (d)-(II)",
     "explanation":"The correct answer is (C) (a)-(ІII), (b)-(IV), (c)-(I), (d)-(II). This is a standard UGC NET 2024 June question on Higher Education."},
    {"id":"he028","topic":"Higher Education","difficulty":"Easy","year":2024,"season":"June",
     "question":"The names of great scholars like Raghunath, Raghunandan and Sri Chaitanya were associated with which of the following ancient university?",
     "options":["Sridhanya Katak", "Vikramshila", "Sakya", "Odantapuri"],
     "correct_answer":"Vikramshila",
     "explanation":"The correct answer is (B) Vikramshila. This is a standard UGC NET 2024 June question on Higher Education."},
    {"id":"he029","topic":"Higher Education","difficulty":"Hard","year":2024,"season":"June",
     "question":"The National Education Policy, 2020, recommended certain verticals Under Higher Education Commission of India. They are (a) NHERC (National Higher Education Regulatory Council) (b) NAC (National Accreditation Council) (c) HEGC (Higher Education Grants Council) (d) GEC (General Education Council) (e) OLC (Open Learning Council)",
     "options":["(a), (d), (e) only", "(a), (b), (c), (d) only", "(b), (c), (d), (e) only", "(a), (b), (c), (e) only"],
     "correct_answer":"(a), (b), (c), (d) only",
     "explanation":"The correct answer is (B) (a), (b), (c), (d) only. This is a standard UGC NET 2024 June question on Higher Education."},
    {"id":"he030","topic":"Higher Education","difficulty":"Easy","year":2024,"season":"June",
     "question":"The University Education Commission (1948-49) suggested a bachelor degree of:",
     "options":["Five years", "Four years", "Three years", "Two years"],
     "correct_answer":"Three years",
     "explanation":"The correct answer is (C) Three years. This is a standard UGC NET 2024 June question on Higher Education."},
    {"id":"he031","topic":"Higher Education","difficulty":"Easy","year":2024,"season":"June",
     "question":"The Kothari Commission (1963-64) suggested spending _________ of national income on education.",
     "options":["3 percent", "6 percent", "7 percent", "9 percent"],
     "correct_answer":"6 percent",
     "explanation":"The correct answer is (B) 6 percent. This is a standard UGC NET 2024 June question on Higher Education."},
    {"id":"he032","topic":"Higher Education","difficulty":"Easy","year":2024,"season":"June",
     "question":"The Council of Education (in India) sought the establishment of a university in:",
     "options":["Bengal Presidency", "Bombay Presidency", "Madras Presidency", "North-Western provinces"],
     "correct_answer":"Bengal Presidency",
     "explanation":"The correct answer is (A) Bengal Presidency. This is a standard UGC NET 2024 June question on Higher Education."},
    {"id":"he033","topic":"Higher Education","difficulty":"Easy","year":2024,"season":"June",
     "question":"The Anglo- Indian Vidyalaya (college) was founded in Calcutta in 1816 by",
     "options":["The Christian missionaries", "The local government", "The East India company", "The people of Calcutta"],
     "correct_answer":"The people of Calcutta",
     "explanation":"The correct answer is (D) The people of Calcutta. This is a standard UGC NET 2024 June question on Higher Education."},
    {"id":"he034","topic":"Higher Education","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which one of the following is a deemed to be university?",
     "options":["Periyar University, Salem", "Nagaland University, Kohima", "Guru Ghasidas Vishwavidyalaya, Bilaspur", "Gandhigram Rural University, Madurai"],
     "correct_answer":"Gandhigram Rural University, Madurai",
     "explanation":"The correct answer is (D) Gandhigram Rural University, Madurai. This is a standard UGC NET 2024 June question on Higher Education."},
    {"id":"he035","topic":"Higher Education","difficulty":"Hard","year":2024,"season":"June",
     "question":"According to National Education Policy 2020, which of the following universal human values will be considered as an integral part of holistic education? (a) Truth (b) Sympathy (c) Righteous conduct 178 (d) Nonviolence (e) Scientific temper",
     "options":["(c) and (e) only", "(b), (d) and (e) only", "(a), (c), (d) and (e) only", "(a), (b), (c) and (d) only"],
     "correct_answer":"(a), (c), (d) and (e) only",
     "explanation":"The correct answer is (C) (a), (c), (d) and (e) only. This is a standard UGC NET 2024 June question on Higher Education."},
    {"id":"he036","topic":"Higher Education","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which of the following is included among the core values promoted by NAAC (National Assessment and Accreditation Council) among the institutions of higher learning",
     "options":["Framing National Education Protocols", "Promoting religious education", "Total Privatisation of education", "Fostering global competencies among students and teachers"],
     "correct_answer":"Fostering global competencies among students and teachers",
     "explanation":"The correct answer is (D) Fostering global competencies among students and teachers. This is a standard UGC NET 2024 June question on Higher Education."},
    {"id":"he037","topic":"Higher Education","difficulty":"Easy","year":2024,"season":"June",
     "question":"Who among the following was the principal of Bengal National College, established in 1906?",
     "options":["Motilal Ghosh", "Aurobindo Ghosh", "Satish Chandra Mukharjee", "Bipin Chandra Paul"],
     "correct_answer":"Aurobindo Ghosh",
     "explanation":"The correct answer is (B) Aurobindo Ghosh. This is a standard UGC NET 2024 June question on Higher Education."},
    {"id":"he038","topic":"Higher Education","difficulty":"Easy","year":2024,"season":"June",
     "question":"The education imparted at Nalanda University was both religious and",
     "options":["Irreligious", "Entertaining", "Secular", "Business-oriented"],
     "correct_answer":"Secular",
     "explanation":"The correct answer is (C) Secular. This is a standard UGC NET 2024 June question on Higher Education."},
    {"id":"he039","topic":"Higher Education","difficulty":"Hard","year":2024,"season":"June",
     "question":"Which of the following institutions were to play a role in shaping the National System of Education at higher level under the National Education Policy (1986)? (a) UNESCO (b) UNDP (c) UGC (d) AICTE (e) ICAR",
     "options":["(a), (b) and (c) only", "(b), (c) and (d) only", "(a), (c) and (d) only", "(c), (d) and (e) only"],
     "correct_answer":"(c), (d) and (e) only",
     "explanation":"The correct answer is (D) (c), (d) and (e) only. This is a standard UGC NET 2024 June question on Higher Education."},
    {"id":"he040","topic":"Higher Education","difficulty":"Easy","year":2024,"season":"June",
     "question":"Most recommendations of the Calcutta University Commission were influenced by",
     "options":["The Hunter Commission", "Wood's Dispatch", "The Haldane Commission", "The Indian Universities Commission"],
     "correct_answer":"The Haldane Commission",
     "explanation":"The correct answer is (C) The Haldane Commission. This is a standard UGC NET 2024 June question on Higher Education."},
    {"id":"he041","topic":"Higher Education","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which of the following ancient universities was visited by the Chinese traveller Hiuen Tsang?",
     "options":["Indraprastha", "Takshashila", "Nalanda", "Odantapuri"],
     "correct_answer":"Nalanda",
     "explanation":"The correct answer is (C) Nalanda. This is a standard UGC NET 2024 June question on Higher Education."},
    {"id":"he042","topic":"Higher Education","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which was the first commission to touch upon the issues of higher education in India indirectly?",
     "options":["The Indian Education Commission (1882-83)", "The Indian Universities Commission (1902)", "The Calcutta University Commission (1917-1919)", "The Hartog Committee (1929)"],
     "correct_answer":"The Indian Education Commission (1882-83)",
     "explanation":"The correct answer is (A) The Indian Education Commission (1882-83). This is a standard UGC NET 2024 June question on Higher Education."},
    {"id":"he043","topic":"Higher Education","difficulty":"Easy","year":2024,"season":"June",
     "question":"The Indian Institute of management, Indore, was set up during:",
     "options":["Eighth five year plan", "Ninth five year plan", "Tenth five year plan", "Eleventh five year plan"],
     "correct_answer":"Ninth five year plan",
     "explanation":"The correct answer is (B) Ninth five year plan. This is a standard UGC NET 2024 June question on Higher Education."},
    {"id":"he044","topic":"Higher Education","difficulty":"Easy","year":2024,"season":"June",
     "question":"The National Education Policy 2020 recommended moving towards.",
     "options":["Suburban Universities", "Single discipline Universities", "Multi-disciplinary Universities", "Specialised Universities"],
     "correct_answer":"Multi-disciplinary Universities",
     "explanation":"The correct answer is (C) Multi-disciplinary Universities. This is a standard UGC NET 2024 June question on Higher Education."},
    {"id":"he045","topic":"Higher Education","difficulty":"Easy","year":2024,"season":"June",
     "question":"The first foreign university to set up its campus at GIFT City, Gujarat, is:",
     "options":["London University, Britain", "Queen's University, Ireland", "Deak in University, Australia", "Moscow University, Russia"],
     "correct_answer":"Deak in University, Australia",
     "explanation":"The correct answer is (C) Deak in University, Australia. This is a standard UGC NET 2024 June question on Higher Education."},
    {"id":"he046","topic":"Higher Education","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match List - I with List - II. List – I (Commission/Committee) List - II (Chairperson) (a) University Education Commission (1948-49) (I) D. S. Kothari (b) Sanskrit Commission (II) K. L. Shirmali (c) Education Commission (1964-66) (III) S. Radhakrishna (d) Committee on Higher Education for Rural Areas (1954) (IV) Suniti Kumar Chatterji",
     "options":["(a)-(I), (b)-(II), (c)-(III), (d)-(IV)", "(a)-(II), (b)-(III), (c)-(IV), (d)-(I)", "(a)-(III), (b)-(IV), (c)-(I), (d)-(II)", "(a)-(IV), (b)-(I), (c)-(II), (d)-(III)"],
     "correct_answer":"(a)-(III), (b)-(IV), (c)-(I), (d)-(II)",
     "explanation":"The correct answer is (C) (a)-(III), (b)-(IV), (c)-(I), (d)-(II). This is a standard UGC NET 2024 June question on Higher Education."},
    {"id":"he047","topic":"Higher Education","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which one of the following was described as the Magna Carta of Indian education by J.A. Richter?",
     "options":["Hunter Commission report", "Hartog Committee report", "Kothari Commission report", "The Education Dispatch of 1854"],
     "correct_answer":"The Education Dispatch of 1854",
     "explanation":"The correct answer is (D) The Education Dispatch of 1854. This is a standard UGC NET 2024 June question on Higher Education."},
    {"id":"he048","topic":"Higher Education","difficulty":"Easy","year":2024,"season":"June",
     "question":"The fifth university to be established during the pre-indepence period in India was:",
     "options":["Punjab University", "Allahabad University", "Patna University", "Andhra University"],
     "correct_answer":"Allahabad University",
     "explanation":"The correct answer is (B) Allahabad University. This is a standard UGC NET 2024 June question on Higher Education."},
    {"id":"he049","topic":"Higher Education","difficulty":"Easy","year":2024,"season":"June",
     "question":"According to National Education Policy, 2020 all Ph.D. entrants are required to take credit based courses in disciplines like:",
     "options":["Education", "Clinical Psychology", "Tribal Studies", "Cultural Studies"],
     "correct_answer":"Education",
     "explanation":"The correct answer is (A) Education. This is a standard UGC NET 2024 June question on Higher Education."},
    {"id":"he050","topic":"Higher Education","difficulty":"Hard","year":2024,"season":"June",
     "question":"The vision of National Education Policy 2020 includes: (a) Moving towards a more multidisciplinary undergraduate education (b) Expansion of professional education institutions (c) Revamping curriculum, pedagogy, assessment and student support for enhanced student experiences (d) Strengthening the regulatory mechanism of AICTE (e) 'light but tighť regulation by a single regulator for higher education",
     "options":["(a), (b), (c) and (d) only", "(a), (c) and (e) only", "(b), (c) and (e) only", "(a), (b) and (e) only"],
     "correct_answer":"(a), (c) and (e) only",
     "explanation":"The correct answer is (B) (a), (c) and (e) only. This is a standard UGC NET 2024 June question on Higher Education."},


    # ↑↑↑ PASTE YOUR NEW Higher Education QUESTIONS ABOVE THIS LINE ↑↑↑
]

# ── 9. INDIAN CONSTITUTION & GOVERNANCE ─────────────────────────────
Q_GOVERNANCE = [
    {"id":"gov001","topic":"Indian Constitution & Governance","difficulty":"Easy","year":2023,"season":"June","question":"The Preamble describes India as:","options":["Federal, Democratic Republic","Sovereign, Socialist, Secular, Democratic Republic","Federal, Socialist State","Secular Parliamentary Democracy"],"correct_answer":"Sovereign, Socialist, Secular, Democratic Republic","explanation":"The Preamble declares India to be a Sovereign, Socialist, Secular, Democratic Republic."},
    {"id":"gov002","topic":"Indian Constitution & Governance","difficulty":"Medium","year":2022,"season":"December","question":"Which Article guarantees Right to Education?","options":["Article 19","Article 21A","Article 25","Article 32"],"correct_answer":"Article 21A","explanation":"Article 21A provides free and compulsory education to children aged 6-14."},
    {"id":"gov003","topic":"Indian Constitution & Governance","difficulty":"Hard","year":2021,"season":"June","question":"The 'Basic Structure' doctrine was established by:","options":["Golaknath case (1967)","Kesavananda Bharati case (1973)","Minerva Mills case (1980)","Maneka Gandhi case (1978)"],"correct_answer":"Kesavananda Bharati case (1973)","explanation":"The Basic Structure Doctrine established that Parliament cannot alter the basic structure of the Constitution."},
    # ════════════════════════════════════════════════════════════════════
    # ADD MORE Indian Constitution & Governance QUESTIONS BELOW ↓
    # ════════════════════════════════════════════════════════════════════
    {"id":"gov004","topic":"Indian Constitution & Governance","difficulty":"Easy","year":2024,"season":"June",
     "question":"The Right to Information Act was passed in India in:",
     "options":["2001","2003","2005","2007"],
     "correct_answer":"2005",
     "explanation":"The RTI Act, 2005 empowers citizens to request information from public authorities."},

    {"id":"gov005","topic":"Indian Constitution & Governance","difficulty":"Medium","year":2024,"season":"December",
     "question":"Which schedule of the Indian Constitution lists the 22 official languages?",
     "options":["Sixth Schedule","Seventh Schedule","Eighth Schedule","Ninth Schedule"],
     "correct_answer":"Eighth Schedule",
     "explanation":"The Eighth Schedule of the Indian Constitution lists 22 officially recognised languages."},

    {"id":"gov006","topic":"Indian Constitution & Governance","difficulty":"Hard","year":2023,"season":"December",
     "question":"The 73rd Constitutional Amendment relates to:",
     "options":["Urban local bodies","Panchayati Raj institutions","Fundamental Rights","Directive Principles"],
     "correct_answer":"Panchayati Raj institutions",
     "explanation":"The 73rd Amendment (1992) gave constitutional status to Panchayati Raj institutions for rural local self-governance."},

    {"id":"gov007","topic":"Indian Constitution & Governance","difficulty":"Medium","year":2022,"season":"June",
     "question":"The concept of 'Judicial Review' in India means:",
     "options":["Judges reviewing their own judgements","Courts reviewing administrative decisions","Power of courts to examine constitutionality of laws","Re-examining pending cases"],
     "correct_answer":"Power of courts to examine constitutionality of laws",
     "explanation":"Judicial review allows courts to invalidate laws and executive actions that violate the Constitution."},

    {"id":"gov008","topic":"Indian Constitution & Governance","difficulty":"Easy","year":2021,"season":"December",
     "question":"Which Article of the Constitution abolishes untouchability?",
     "options":["Article 14","Article 15","Article 17","Article 19"],
     "correct_answer":"Article 17",
     "explanation":"Article 17 abolishes untouchability and forbids its practice in any form."},
        {"id":"gov009","topic":"Indian Constitution & Governance","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which among the following fuels produces least amount of soot particles during combustion?",
     "options":["Petrol", "Kerosene", "Diesel", "Compressed Natural Gas (CNG)"],
     "correct_answer":"Compressed Natural Gas (CNG)",
     "explanation":"The correct answer is (D) Compressed Natural Gas (CNG). This is a standard UGC NET 2024 June question on Indian Constitution & Governance."},
    {"id":"gov010","topic":"Indian Constitution & Governance","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match List - I with List - II. List - I (Constitutional Provision of Education) List - II (Article) (a) Women's Education (I) 28 (b) Education of Minorities (II) 21-A (c) Secular Education (III) 15 (Part-II) (d) Right to Education (IV) 29 (Part-III) 57",
     "options":["(a)-(III), (b)-(I), (c)-(IV), (d)-(II)", "(a)-(I), (b)-(II), (c)-(IV), (d)-(III)", "(a)-(III), (b)-(IV), (c)-(I), (d)-(II)", "(a)-(I), (b)-(IV), (c)-(II), (d)-(III)"],
     "correct_answer":"(a)-(III), (b)-(IV), (c)-(I), (d)-(II)",
     "explanation":"The correct answer is (C) (a)-(III), (b)-(IV), (c)-(I), (d)-(II). This is a standard UGC NET 2024 June question on Indian Constitution & Governance."},
    {"id":"gov011","topic":"Indian Constitution & Governance","difficulty":"Medium","year":2024,"season":"June",
     "question":"The cost price of two articles is same, one of them is sold at a profit of 13% while the other one is sold at a profit of 19%. If the difference between their selling price is Rs. 126, the cost of price of each article is",
     "options":["Rs. 1800", "Rs. 1900", "Rs. 2000", "Rs. 2100"],
     "correct_answer":"Rs. 2100",
     "explanation":"The correct answer is (D) Rs. 2100. This is a standard UGC NET 2024 June question on Indian Constitution & Governance."},
    {"id":"gov012","topic":"Indian Constitution & Governance","difficulty":"Medium","year":2024,"season":"June",
     "question":"Arrange the following statistical measures in increasing order. (a) Sixth decile (b) Median (c) Third quartile (d) 67th percentile",
     "options":["(a), (d), (b), (c)", "(b), (c), (a), (d)", "(b), (a), (d), (c)", "(a), (c), (d), (b)"],
     "correct_answer":"(b), (a), (d), (c)",
     "explanation":"The correct answer is (C) (b), (a), (d), (c). This is a standard UGC NET 2024 June question on Indian Constitution & Governance."},
    {"id":"gov013","topic":"Indian Constitution & Governance","difficulty":"Easy","year":2024,"season":"June",
     "question":"What is the total number of female participants in sports events El and E3 together?",
     "options":["4274", "4308", "4326", "4334"],
     "correct_answer":"4334",
     "explanation":"The correct answer is (D) 4334. This is a standard UGC NET 2024 June question on Indian Constitution & Governance."},
    {"id":"gov014","topic":"Indian Constitution & Governance","difficulty":"Medium","year":2024,"season":"June",
     "question":"Arrange the following statistical measures in increasing order (a) 37th percentile (b) first quartile (c) median (d) third decile",
     "options":["(a), (b), (c), (d)", "(b), (d), (a), (c)", "(b), (c), (a), (d)", "(c), (b), (d), (a)"],
     "correct_answer":"(b), (d), (a), (c)",
     "explanation":"The correct answer is (B) (b), (d), (a), (c). This is a standard UGC NET 2024 June question on Indian Constitution & Governance."},
    {"id":"gov015","topic":"Indian Constitution & Governance","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which one of the following is known as the heart of sewage treatment?",
     "options":["Primary treatment", "Secondary treatment", "Tertiary treatment", "Advanced treatment"],
     "correct_answer":"Secondary treatment",
     "explanation":"The correct answer is (B) Secondary treatment. This is a standard UGC NET 2024 June question on Indian Constitution & Governance."},
    {"id":"gov016","topic":"Indian Constitution & Governance","difficulty":"Easy","year":2024,"season":"June",
     "question":"Response of participants who are well aware of the fact that they are being studied is considered as.",
     "options":["Directed response", "Intentional response", "Desire effect", "Reactive effect"],
     "correct_answer":"Reactive effect",
     "explanation":"The correct answer is (D) Reactive effect. This is a standard UGC NET 2024 June question on Indian Constitution & Governance."},
    {"id":"gov017","topic":"Indian Constitution & Governance","difficulty":"Easy","year":2024,"season":"June",
     "question":"Individual who live in a particular community develop distinctively patterned systems of",
     "options":["Information distribution", "Media ownership", "Media marketing", "Information imperialism"],
     "correct_answer":"Information distribution",
     "explanation":"The correct answer is (A) Information distribution. This is a standard UGC NET 2024 June question on Indian Constitution & Governance."},
    {"id":"gov018","topic":"Indian Constitution & Governance","difficulty":"Easy","year":2024,"season":"June",
     "question":"A way of dealing with conflict in which people express their feelings, ask for what they want, say 'no' to things they don't want, and act in their own best interests, is known as-",
     "options":["Aggressive style", "Passive style", "Assertive style", "Manipulative style"],
     "correct_answer":"Assertive style",
     "explanation":"The correct answer is (C) Assertive style. This is a standard UGC NET 2024 June question on Indian Constitution & Governance."},
    {"id":"gov019","topic":"Indian Constitution & Governance","difficulty":"Easy","year":2024,"season":"June",
     "question":"Synapses are considered as:",
     "options":["Timely gaps between neurons where connections between neurons are made.", "An element responsible for blood circulation in the brain", "Large gaps between neurons where connections between neurons are made", "One and only particle of the brain related to hand-eye-coordination."],
     "correct_answer":"Timely gaps between neurons where connections between neurons are made.",
     "explanation":"The correct answer is (A) Timely gaps between neurons where connections between neurons are made.. This is a standard UGC NET 2024 June question on Indian Constitution & Governance."},
    {"id":"gov021","topic":"Indian Constitution & Governance","difficulty":"Easy","year":2024,"season":"June",
     "question":"Making way for technologies of automation is ________transformation of modern society",
     "options":["Cyber-nation", "Mechanical", "Political", "Artificial"],
     "correct_answer":"Cyber-nation",
     "explanation":"The correct answer is (A) Cyber-nation. This is a standard UGC NET 2024 June question on Indian Constitution & Governance."},
    {"id":"gov022","topic":"Indian Constitution & Governance","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which one of the following is considered to be the finest particulate matter?",
     "options":["Fine mode particles", "Neucleation mode particles", "Aitken mode particles", "Accumulation mode particles"],
     "correct_answer":"Neucleation mode particles",
     "explanation":"The correct answer is (B) Neucleation mode particles. This is a standard UGC NET 2024 June question on Indian Constitution & Governance."},
    {"id":"gov023","topic":"Indian Constitution & Governance","difficulty":"Easy","year":2024,"season":"June",
     "question":"The cost price of 35 articles is the same as the selling price of N articles. If the profit earned is 40%, the value of N is:",
     "options":["15", "20", "25", "30"],
     "correct_answer":"25",
     "explanation":"The correct answer is (C) 25. This is a standard UGC NET 2024 June question on Indian Constitution & Governance."},



    # ↑↑↑ PASTE YOUR NEW Indian Constitution & Governance QUESTIONS ABOVE THIS LINE ↑↑↑
]

# ── 10. DATA INTERPRETATION ──────────────────────────────────────────
Q_DATA_INTERPRETATION = [
    {"id":"di001","topic":"Data Interpretation","difficulty":"Medium","year":2023,"season":"June","question":"If the mean of 5 numbers is 30 and mean of 3 of them is 20, what is mean of remaining 2?","options":["35","45","40","50"],"correct_answer":"45","explanation":"Total=150, Sum of 3=60, Remaining=90, Mean=45."},
    {"id":"di002","topic":"Data Interpretation","difficulty":"Easy","year":2022,"season":"June","question":"Which measure of central tendency is most affected by extreme values?","options":["Mode","Median","Mean","None"],"correct_answer":"Mean","explanation":"The arithmetic mean is significantly affected by extreme values."},
    {"id":"di003","topic":"Data Interpretation","difficulty":"Hard","year":2021,"season":"December","question":"The coefficient of variation (CV) is calculated as:","options":["(Mean/SD)x100","(SD/Mean)x100","SD x Mean","Mean/Variance"],"correct_answer":"(SD/Mean)x100","explanation":"CV = (SD/Mean) x 100, expressing variability as a percentage of mean."},
    # ════════════════════════════════════════════════════════════════════
    # ADD MORE Data Interpretation QUESTIONS BELOW ↓
    # ════════════════════════════════════════════════════════════════════
    {"id":"di004","topic":"Data Interpretation","difficulty":"Medium","year":2024,"season":"June",
     "question":"In a pie chart, if a sector represents 25% of the total, its central angle is:",
     "options":["45°","60°","90°","120°"],
     "correct_answer":"90°",
     "explanation":"Central angle = (25/100) × 360° = 90°."},

    {"id":"di005","topic":"Data Interpretation","difficulty":"Easy","year":2024,"season":"December",
     "question":"The difference between the highest and lowest values in a dataset is called:",
     "options":["Variance","Standard deviation","Range","Mean deviation"],
     "correct_answer":"Range",
     "explanation":"Range = Maximum value − Minimum value; it is the simplest measure of dispersion."},

    {"id":"di006","topic":"Data Interpretation","difficulty":"Hard","year":2023,"season":"June",
     "question":"If two events A and B are mutually exclusive, then P(A or B) =",
     "options":["P(A) × P(B)","P(A) + P(B) − P(A∩B)","P(A) + P(B)","P(A) / P(B)"],
     "correct_answer":"P(A) + P(B)",
     "explanation":"For mutually exclusive events, P(A∩B) = 0, so P(A∪B) = P(A) + P(B)."},

    {"id":"di007","topic":"Data Interpretation","difficulty":"Medium","year":2022,"season":"December",
     "question":"Which graphical representation is best suited for showing trends over time?",
     "options":["Pie chart","Bar graph","Line graph","Histogram"],
     "correct_answer":"Line graph",
     "explanation":"Line graphs are ideal for displaying continuous data trends over time."},

    {"id":"di008","topic":"Data Interpretation","difficulty":"Easy","year":2021,"season":"June",
     "question":"The median of 3, 7, 9, 11, 15 is:",
     "options":["7","9","11","15"],
     "correct_answer":"9",
     "explanation":"Arranged in order: 3,7,9,11,15 — median is the middle value = 9."},
        {"id":"di009","topic":"Data Interpretation","difficulty":"Medium","year":2024,"season":"June",
     "question":"If the export of country A in the year 2024 is 20% more than the combined export of country B in 2022 and the export of country E in 2021 together, then what is the income of country A (in ₹ crore) in the year 2024, if its import is ₹ 184 crore for that year?",
     "options":["106", "44", "92", "68"],
     "correct_answer":"68",
     "explanation":"The correct answer is (D) 68. This is a standard UGC NET 2024 June question on Data Interpretation."},
    {"id":"di010","topic":"Data Interpretation","difficulty":"Easy","year":2024,"season":"June",
     "question":"Owner of store C invests ₹ 9 lakh in 2021. What should be the investment of D in the same year to get an income which is double than that of store C?",
     "options":["₹ 51 lakh", "₹ 6 lakh", "₹ 50000", "₹ 33 lakh"],
     "correct_answer":"₹ 51 lakh",
     "explanation":"The correct answer is (A) ₹ 51 lakh. This is a standard UGC NET 2024 June question on Data Interpretation."},
    {"id":"di011","topic":"Data Interpretation","difficulty":"Medium","year":2024,"season":"June",
     "question":"Arrange the datasets with following pairs of mean (𝑥𝑥̅) and standard deviation (𝜎𝜎) in increasing order of their coefficient of variation: (a) 𝑥𝑥̅ = 25, σ = 9 (b) 𝑥𝑥̅ = 40, σ = 12 (c) 𝑥𝑥̅ = 30, σ = 10 (d) 𝑥𝑥̅ = 35, σ = 11",
     "options":["(a), (b), (c), (d)", "(b), (c), (d), (a)", "(a), (c), (d), (b)", "(b), (d), (c), (a)"],
     "correct_answer":"(b), (d), (c), (a)",
     "explanation":"The correct answer is (D) (b), (d), (c), (a). This is a standard UGC NET 2024 June question on Data Interpretation."},
    {"id":"di012","topic":"Data Interpretation","difficulty":"Easy","year":2024,"season":"June",
     "question":"For City-A, if the total number of males who passed in Arts is 2480, then what is the difference between the number of students who passed in Commerce and that in Science?",
     "options":["600", "1000", "1400", "1800"],
     "correct_answer":"1800",
     "explanation":"The correct answer is (D) 1800. This is a standard UGC NET 2024 June question on Data Interpretation."},
    {"id":"di013","topic":"Data Interpretation","difficulty":"Hard","year":2024,"season":"June",
     "question":"What among the following can be correctly claimed in the light of 'Assessment Rubrics'? (a) A tool used to interpret and grade students on the basis of some criterion. (b) A means to increase subjective evaluation by the evaluator. 61 (c) It ensures transparency and fairness in the marking process. (d) It provides an opportunity to set orbitrary standards and guidelines for moderation. (e) It is an innovative evaluation system.",
     "options":["(a), (c), and (d) only", "(a), (b) and (c) only", "(c), (d), and (e) only", "(a), (c), and (e) only"],
     "correct_answer":"(a), (c), and (e) only",
     "explanation":"The correct answer is (D) (a), (c), and (e) only. This is a standard UGC NET 2024 June question on Data Interpretation."},
    {"id":"di014","topic":"Data Interpretation","difficulty":"Medium","year":2024,"season":"June",
     "question":"Arrange the data sets with following pairs of mean (𝑥𝑥̅) and standard derivation (σ) in increasing order of their coefficient of variation. (a) 𝑥𝑥̅ = 8, σ = 1.7 (b) 𝑥𝑥̅ = 11, σ = 2.2 (c) 𝑥𝑥̅ = 15, σ = 3.6 (d) 𝑥𝑥̅ = 16, σ = 3",
     "options":["(a), (b), (d), (c)", "(b), (d), (c), (a)", "(c), (b), (d), (a)", "(d), (b), (a), (c)"],
     "correct_answer":"(d), (b), (a), (c)",
     "explanation":"The correct answer is (D) (d), (b), (a), (c). This is a standard UGC NET 2024 June question on Data Interpretation."},
    {"id":"di018","topic":"Data Interpretation","difficulty":"Easy","year":2024,"season":"June",
     "question":"In the context of sentence meaning relationship which of the following refers to 'Expectancy'",
     "options":["Āsatti", "Ākaṁkşā", "Yogyatā", "Tātparya Jñāna"],
     "correct_answer":"Ākaṁkşā",
     "explanation":"The correct answer is (B) Ākaṁkşā. This is a standard UGC NET 2024 June question on Data Interpretation."},
    {"id":"di019","topic":"Data Interpretation","difficulty":"Medium","year":2024,"season":"June",
     "question":"Arrange the datasets with following pairs of mean (𝑥𝑥̅) and standard deviation (σ) in increasing order of their coefficient of variation. (a) 𝑥𝑥̅ = 14, σ = 2.8 (b) 𝑥𝑥̅ = 9, σ = 1.5 (c) 𝑥𝑥̅ =12, σ = 2.1 (d) 𝑥𝑥̅ = 8, σ = 1.2",
     "options":["(a), (b), (c), (d)", "(b), (c), (d), (a)", "(d), (b), (c), (a)", "(c), (d), (a), (b)"],
     "correct_answer":"(d), (b), (c), (a)",
     "explanation":"The correct answer is (C) (d), (b), (c), (a). This is a standard UGC NET 2024 June question on Data Interpretation."},
    {"id":"di020","topic":"Data Interpretation","difficulty":"Easy","year":2024,"season":"June",
     "question":"How do rituals influence business practices in modern Japan?",
     "options":["Results are prioritized over the process", "Manners and processes are more important than the final outcome", "Rituals are not significant in Japanese culture", "Business processes are goal oriented"],
     "correct_answer":"Manners and processes are more important than the final outcome",
     "explanation":"The correct answer is (B) Manners and processes are more important than the final outcome. This is a standard UGC NET 2024 June question on Data Interpretation."},
    {"id":"di021","topic":"Data Interpretation","difficulty":"Easy","year":2024,"season":"June",
     "question":"In a situation where a researcher wants to test whether the population mean is lower than some hypothesized value, the researcher would employ-",
     "options":["Z-tailed test", "Left tailed test", "Right tailed test", "F- test"],
     "correct_answer":"Left tailed test",
     "explanation":"The correct answer is (B) Left tailed test. This is a standard UGC NET 2024 June question on Data Interpretation."},
    {"id":"di022","topic":"Data Interpretation","difficulty":"Hard","year":2024,"season":"June",
     "question":"In nuclear reactors, 'moderators' are substances. (a) That slows down neutron (b) That limits the chain reaction (c) That helps to sustain the chain reaction (d) Without which chain reaction in most nuclear reactors would stop (e) Such as heavy water or D₂O",
     "options":["(a), (b), (c) and (d) only", "(a), (c), (d) and (e) only", "(b), (c) and (d) only", "(a), (b) and (e) only"],
     "correct_answer":"(a), (c), (d) and (e) only",
     "explanation":"The correct answer is (B) (a), (c), (d) and (e) only. This is a standard UGC NET 2024 June question on Data Interpretation."},
    {"id":"di023","topic":"Data Interpretation","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which of the following methods of graphical representation of data would be useful for depicting proportions?",
     "options":["Line charts", "Histograms", "Pie charts", "Scatter plots"],
     "correct_answer":"Pie charts",
     "explanation":"The correct answer is (C) Pie charts. This is a standard UGC NET 2024 June question on Data Interpretation."},
    {"id":"di024","topic":"Data Interpretation","difficulty":"Easy","year":2024,"season":"June",
     "question":"The production and distribution of news by ordinary people is referred to as:",
     "options":["Popular journalism", "Common journalism", "Citizen journalism", "New journalism"],
     "correct_answer":"Citizen journalism",
     "explanation":"The correct answer is (C) Citizen journalism. This is a standard UGC NET 2024 June question on Data Interpretation."},
    {"id":"di025","topic":"Data Interpretation","difficulty":"Medium","year":2024,"season":"June",
     "question":"Covariance i.e Cov (X,Y) and standard deviations of different datasets are given. Estimate the correlation coefficients and arrange in increasing order (a) Cov (X,Y) = 32, σx = 8, σy = 7 (b) Cov (X,Y) = 36, σx = 12, σy = 5 (c) Cov (X,Y) = 35, σx = 7, σy = 8 (d) Cov (X,Y) = 39, σx = 6, σy = 13 117",
     "options":["(a), (b), (c), (d)", "(b), (c), (d), (a)", "(c), (d), (a), (b)", "(d), (a), (b), (c)"],
     "correct_answer":"(d), (a), (b), (c)",
     "explanation":"The correct answer is (D) (d), (a), (b), (c). This is a standard UGC NET 2024 June question on Data Interpretation."},
    {"id":"di026","topic":"Data Interpretation","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which of the following methods of graphical representation of data would be useful for showing trends?",
     "options":["Bar charts", "Line charts", "Box plants", "Pie charts"],
     "correct_answer":"Line charts",
     "explanation":"The correct answer is (B) Line charts. This is a standard UGC NET 2024 June question on Data Interpretation."},
    {"id":"di027","topic":"Data Interpretation","difficulty":"Hard","year":2024,"season":"June",
     "question":"Which of the following are the primary goals of PM e-Vidya? (a) To provide free text-books to all students (b) To facilitate multi mode access to digital/online teaching-learning content (c) To offer scholarships to topper students (d) To facilitate the uniqueness with its comprehensive accessibility for all (e) To benefit learners in remote areas where stable internet is not available",
     "options":["(a), (c) and (e) only", "(a), (d) and (e) only", "(b), (d) and (e) only", "(c) and (d) only"],
     "correct_answer":"(b), (d) and (e) only",
     "explanation":"The correct answer is (C) (b), (d) and (e) only. This is a standard UGC NET 2024 June question on Data Interpretation."},
    {"id":"di028","topic":"Data Interpretation","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which of the following terms has been used to describe wars meant to establish dominion by leaders like Alexander Napoleon and Hitler?",
     "options":["Resource Wars", "Defensive Wars", "Hubristic Warfare", "Revolutionary Wars"],
     "correct_answer":"Hubristic Warfare",
     "explanation":"The correct answer is (C) Hubristic Warfare. This is a standard UGC NET 2024 June question on Data Interpretation."},
    {"id":"di029","topic":"Data Interpretation","difficulty":"Easy","year":2024,"season":"June",
     "question":"Total number of sports shoes sold by all companies in year 2023 is approximately _________% of the total number of sports shoes produced by all the companies in that year.",
     "options":["84", "79", "72", "75"],
     "correct_answer":"79",
     "explanation":"The correct answer is (B) 79. This is a standard UGC NET 2024 June question on Data Interpretation."},
    {"id":"di030","topic":"Data Interpretation","difficulty":"Easy","year":2024,"season":"June",
     "question":"What is the percentage rise in the production of sports shoes by company C from the year 2022 to 2023?",
     "options":["15.375%", "20.625%", "15.625%", "10.625%"],
     "correct_answer":"15.625%",
     "explanation":"The correct answer is (C) 15.625%. This is a standard UGC NET 2024 June question on Data Interpretation."},
    {"id":"di031","topic":"Data Interpretation","difficulty":"Easy","year":2024,"season":"June",
     "question":"Percentage rise in the production of sports shoes from the year 2022 to 2023 is more than 25 % for exactly __________ companies.",
     "options":["2", "3", "4", "5"],
     "correct_answer":"3",
     "explanation":"The correct answer is (B) 3. This is a standard UGC NET 2024 June question on Data Interpretation."},
    {"id":"di032","topic":"Data Interpretation","difficulty":"Easy","year":2024,"season":"June",
     "question":"Which of the following methods of graphical representation of data would be useful in showing association between two variables?",
     "options":["Ogive", "Pie charts", "Histogram", "Scatter plots"],
     "correct_answer":"Scatter plots",
     "explanation":"The correct answer is (D) Scatter plots. This is a standard UGC NET 2024 June question on Data Interpretation."},
    {"id":"di033","topic":"Data Interpretation","difficulty":"Medium","year":2024,"season":"June",
     "question":"Arrange the datasets with the following means ( 𝑋𝑋ത ) and standard deviations(σ) in decreasing order of their coefficients of variation. (a) σ = 4.3, 𝑋𝑋ത = 13.8 (b) σ = 3.8, 𝑋𝑋ത = 12.7 (c) σ = 5.7, 𝑋𝑋ത = 14.9 (d) σ = 4.7, 𝑋𝑋ത = 14.1",
     "options":["(a), (b), (c), (d)", "(b), (c), (d), (a)", "(c), (d), (a), (b)", "(d), (a), (b), (c)"],
     "correct_answer":"(c), (d), (a), (b)",
     "explanation":"The correct answer is (C) (c), (d), (a), (b). This is a standard UGC NET 2024 June question on Data Interpretation."},
    {"id":"di034","topic":"Data Interpretation","difficulty":"Medium","year":2024,"season":"June",
     "question":"Arrange the data sets with following means (𝑥𝑥̅) and standard deviations (σ) in increasing order of their coefficients of variation: (a) σ = 3.7, 𝑥𝑥̅ = 20 (b) σ = 4.3, 𝑥𝑥̅ = 25 (c) σ = 5.2, 𝑥𝑥̅ = 35 (d) σ = 6.1, 𝑥𝑥̅ = 40",
     "options":["(a), (b), (c), (d)", "(b), (c), (d), (a)", "(c), (d), (b), (a)", "(d), (c), (a), (b)"],
     "correct_answer":"(c), (d), (b), (a)",
     "explanation":"The correct answer is (C) (c), (d), (b), (a). This is a standard UGC NET 2024 June question on Data Interpretation."},
    {"id":"di035","topic":"Data Interpretation","difficulty":"Easy","year":2024,"season":"June",
     "question":"If P is the total number of unsubscribed viewers in Town-B and Town-C together, and Q is the number of subscribed viewers in Town-E, then Q is ________ % less than P.",
     "options":["65", "80", "60", "70"],
     "correct_answer":"70",
     "explanation":"The correct answer is (D) 70. This is a standard UGC NET 2024 June question on Data Interpretation."},
    {"id":"di036","topic":"Data Interpretation","difficulty":"Easy","year":2024,"season":"June",
     "question":"If P is the total number of unsubscribed viewers in Town- B and Town-C together, and Q is the number of unsubscribed viewers in town-E, then Q is __________ % of P.",
     "options":["60", "70", "80", "75"],
     "correct_answer":"70",
     "explanation":"The correct answer is (B) 70. This is a standard UGC NET 2024 June question on Data Interpretation."},
    {"id":"di037","topic":"Data Interpretation","difficulty":"Medium","year":2024,"season":"June",
     "question":"There are some Cows and Ducks in a park. The total number of heads of Cows and Ducks together is 60. However, the total number legs of the cows and ducks together is 180. Find the number of cows and ducks in the park, respectively.",
     "options":["30, 30", "32,28", "28, 32", "24, 36"],
     "correct_answer":"30, 30",
     "explanation":"The correct answer is (A) 30, 30. This is a standard UGC NET 2024 June question on Data Interpretation."},
    {"id":"di038","topic":"Data Interpretation","difficulty":"Medium","year":2024,"season":"June",
     "question":"Arrange the correlation coefficients computed from the following information on covariance i.e. cov (x,y) and standard deviation 𝜎𝜎𝑥𝑥 and 𝜎𝜎𝑦𝑦, in increasing order. (a) cov(x, y) = 18, 𝜎𝜎𝑥𝑥 = 4, 𝜎𝜎𝑦𝑦= 9 (b) cov(x,y) = 15, 𝜎𝜎𝑥𝑥 = 8 𝜎𝜎𝑦𝑦 = 3 (c) cov(x,y) = 16, 𝜎𝜎𝑥𝑥 = 7, 𝜎𝜎𝑦𝑦 = 4 (d) cov(x,y) = 21 , 𝜎𝜎𝑥𝑥 = 6, 𝜎𝜎𝑦𝑦= 5",
     "options":["(a), (c), (b), (d)", "(b), (c), (d), (a)", "(c), (b), (a), (d)", "(d), (b), (a), (c)"],
     "correct_answer":"(a), (c), (b), (d)",
     "explanation":"The correct answer is (A) (a), (c), (b), (d). This is a standard UGC NET 2024 June question on Data Interpretation."},
    {"id":"di039","topic":"Data Interpretation","difficulty":"Medium","year":2024,"season":"June",
     "question":"Which of the following statements accuracy describe the presence of nicotine in plants?",
     "options":["Nicotine is found in several plants, including some vegetables, in trace amounts", "Nicotine is exclusively found in tobacco and not in any other plants", "Nicotine is synthesized only in laboratories and not naturally found in plants", "Nicotine is a by product of industrial processes and not naturally found"],
     "correct_answer":"Nicotine is found in several plants, including some vegetables, in trace amounts",
     "explanation":"The correct answer is (A) Nicotine is found in several plants, including some vegetables, in trace amounts. This is a standard UGC NET 2024 June question on Data Interpretation."},
    {"id":"di040","topic":"Data Interpretation","difficulty":"Easy","year":2024,"season":"June",
     "question":"The total number of visitors to Manali on Monday and Wednesday is________ % of the number of visitors to Kullu on Wednesday.",
     "options":["200", "150", "125", "50"],
     "correct_answer":"200",
     "explanation":"The correct answer is (A) 200. This is a standard UGC NET 2024 June question on Data Interpretation."},
    {"id":"di041","topic":"Data Interpretation","difficulty":"Medium","year":2024,"season":"June",
     "question":"If 20% of the visitors to Kullu on Tuesday are foreigners and 40% of the visitors to Manali on Friday are foreigners, then what is the total number of visitors to Kullu on Tuesday who are not 174 foreigners and to Manali on Friday who are foreigners?",
     "options":["920", "776", "984", "844"],
     "correct_answer":"776",
     "explanation":"The correct answer is (B) 776. This is a standard UGC NET 2024 June question on Data Interpretation."},
    {"id":"di042","topic":"Data Interpretation","difficulty":"Easy","year":2024,"season":"June",
     "question":"If the total number of items sold by A on all the five days is 3600, then the difference between the number of items sold by A on Monday and Friday is:",
     "options":["640", "450", "420", "440"],
     "correct_answer":"440",
     "explanation":"The correct answer is (D) 440. This is a standard UGC NET 2024 June question on Data Interpretation."},
    {"id":"di043","topic":"Data Interpretation","difficulty":"Easy","year":2024,"season":"June",
     "question":"If the number of items sold by C on Thursday is the average of the number of items sold by C on Wednesday and Friday, then the total number of items sold by C on all the five days is:",
     "options":["3500", "3800", "3400", "3700"],
     "correct_answer":"3800",
     "explanation":"The correct answer is (B) 3800. This is a standard UGC NET 2024 June question on Data Interpretation."},
    {"id":"di044","topic":"Data Interpretation","difficulty":"Medium","year":2024,"season":"June",
     "question":"If the total numbers of items sold by A and B on all the five days is 4000, and 4400, respectively, then the number of items sold by B on Tuesday is _______% more than the number of items sold by A on Friday.",
     "options":["37.5", "23.5", "32.25", "42.5"],
     "correct_answer":"37.5",
     "explanation":"The correct answer is (A) 37.5. This is a standard UGC NET 2024 June question on Data Interpretation."},
    {"id":"di045","topic":"Data Interpretation","difficulty":"Medium","year":2024,"season":"June",
     "question":"Which of the following statements are true regarding the word 'God'? (a) It is meaningless (b) it is meaningful (c) The word God has no intension that could be its meaning. (d) In case of word 'God', there is an intension that is its meaning.",
     "options":["(b) and (d) only", "(a) and (c) only", "(a) only", "(b) only"],
     "correct_answer":"(b) and (d) only",
     "explanation":"The correct answer is (A) (b) and (d) only. This is a standard UGC NET 2024 June question on Data Interpretation."},
    {"id":"di046","topic":"Data Interpretation","difficulty":"Easy","year":2024,"season":"June",
     "question":"The geometric mean of the number 9, 12 and 16 is:",
     "options":["12.33", "11.66", "12", "12.66"],
     "correct_answer":"12",
     "explanation":"The correct answer is (C) 12. This is a standard UGC NET 2024 June question on Data Interpretation."},
    {"id":"di048","topic":"Data Interpretation","difficulty":"Easy","year":2024,"season":"June",
     "question":"Sharpness of the peak of a statistical distribution is represented by",
     "options":["Kurtosis", "Skewness", "Mean", "Median"],
     "correct_answer":"Kurtosis",
     "explanation":"The correct answer is (A) Kurtosis. This is a standard UGC NET 2024 June question on Data Interpretation."},
    {"id":"di049","topic":"Data Interpretation","difficulty":"Medium","year":2024,"season":"June",
     "question":"Consider the income of new Private Banks in 2021-2022 as ₹8000 Crore. If the expenditure of new Private Banks in 2021-2022 is same as their income, then the difference in income of new Private Banks in 2021-2022 and 2022-2023 will be approximately______% of the difference in expenditure of new private banks in 2021-2022 and 2022-2023.",
     "options":["52", "76", "84", "118"],
     "correct_answer":"84",
     "explanation":"The correct answer is (C) 84. This is a standard UGC NET 2024 June question on Data Interpretation."},
    {"id":"di050","topic":"Data Interpretation","difficulty":"Medium","year":2024,"season":"June",
     "question":"If the expenditure of foreign Banks in 2020-2021 is equal to their income in that year and is equal to ₹ 60,000 crore, then in 2022-2023, what is the difference in income and expenditure of Foreign Banks?",
     "options":["₹ 3984 crore", "₹ 4000 crore", "₹ 5462 crore", "₹ 3460 crore"],
     "correct_answer":"₹ 3984 crore",
     "explanation":"The correct answer is (A) ₹ 3984 crore. This is a standard UGC NET 2024 June question on Data Interpretation."},
    {"id":"di051","topic":"Data Interpretation","difficulty":"Medium","year":2024,"season":"June",
     "question":"Consider the income of PSU Banks in 2020-2021 as ₹ 10,00,000 crore. If the expenditure of PSU Banks in 2022-2023 is equal to the income of PSU Banks in 2020-2021, then the income of PSU Banks in 2022-23 will be approximately________% more than the expenditure of PSU Banks in 2021-2022.",
     "options":["62", "44", "56", "64"],
     "correct_answer":"64",
     "explanation":"The correct answer is (D) 64. This is a standard UGC NET 2024 June question on Data Interpretation."},
    {"id":"di052","topic":"Data Interpretation","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match List - I with List - II. List -I (Abbreviations) List -II (Meaning) (a) id., (I) refer to (b) post: (II) the same (c) vid (III) namely (d) viz., (IV) after",
     "options":["(a)-(I), (b)-(II), (c)-(III), (d)-(IV)", "(a)-(II), (b)-(IV), (c)-(I), (d)-(III)", "(a)-(II), (b)-(I), (c)-(III), (d)-(IV)", "(a)-(III), (b)-(II), (c)-(IV), (d)-(I)"],
     "correct_answer":"(a)-(II), (b)-(IV), (c)-(I), (d)-(III)",
     "explanation":"The correct answer is (B) (a)-(II), (b)-(IV), (c)-(I), (d)-(III). This is a standard UGC NET 2024 June question on Data Interpretation."},
    {"id":"di053","topic":"Data Interpretation","difficulty":"Hard","year":2024,"season":"June",
     "question":"Identify the measures of dispersion: (a) Mean deviation (b) Median (c) Standard deviation (d) Range (e) Quartile",
     "options":["(a), (b) and (c) only", "(a) and (e) only", "(a), (c) and (d) only", "(c), (d) and (e) only"],
     "correct_answer":"(a), (c) and (d) only",
     "explanation":"The correct answer is (C) (a), (c) and (d) only. This is a standard UGC NET 2024 June question on Data Interpretation."},
    {"id":"di054","topic":"Data Interpretation","difficulty":"Easy","year":2024,"season":"June",
     "question":"If the amount of money spent on food by C and D is ₹144000 and ₹172800, respectively, then the annual income of C is ________ % of the annual income of D.",
     "options":["47.5", "60", "62.5", "120"],
     "correct_answer":"62.5",
     "explanation":"The correct answer is (C) 62.5. This is a standard UGC NET 2024 June question on Data Interpretation."},
    {"id":"di055","topic":"Data Interpretation","difficulty":"Easy","year":2024,"season":"June",
     "question":"If the annual income of each of C and D is ₹ 840000, then what is the sum of the amount spent by C on Rent and that by D on Miscellaneous items?",
     "options":["₹ 288820", "₹ 290520", "₹ 293160", "₹ 295700"],
     "correct_answer":"₹ 293160",
     "explanation":"The correct answer is (C) ₹ 293160. This is a standard UGC NET 2024 June question on Data Interpretation."},
    {"id":"di056","topic":"Data Interpretation","difficulty":"Easy","year":2024,"season":"June",
     "question":"If the annual income of each of the six persons is ₹ 3 lakh, then the amount of money spent on clothes is more than ₹ 41800 by exactly_______ persons.",
     "options":["2", "3", "4", "5"],
     "correct_answer":"2",
     "explanation":"The correct answer is (A) 2. This is a standard UGC NET 2024 June question on Data Interpretation."},
    {"id":"di057","topic":"Data Interpretation","difficulty":"Easy","year":2024,"season":"June",
     "question":"If the annual incomes of B and C are ₹ 432000 and ₹ 528000, respectively, then what is the difference between the amount spent by them on Transport?",
     "options":["₹ 18496", "₹ 18828", "₹ 19216", "₹ 19488"],
     "correct_answer":"₹ 19488",
     "explanation":"The correct answer is (D) ₹ 19488. This is a standard UGC NET 2024 June question on Data Interpretation."},
    {"id":"di058","topic":"Data Interpretation","difficulty":"Easy","year":2024,"season":"June",
     "question":"If the monthly income of A and D are ₹ 80000 and ₹ 72000, respectively, then the amount of money spent by A on Rent is ________ % more than the amount spent by D on clothes.",
     "options":["32.62", "38.89", "36.54", "34.24"],
     "correct_answer":"38.89",
     "explanation":"The correct answer is (B) 38.89. This is a standard UGC NET 2024 June question on Data Interpretation."},
    {"id":"di059","topic":"Data Interpretation","difficulty":"Medium","year":2024,"season":"June",
     "question":"Match List - I with List - II. List -I (Abbreviations) List -II (Meaning) (a) ante., (I) here and there (b) cf. (II) and others (c) et.al., (III) compare (d) passim: (IV) before",
     "options":["(a)-(IV), (b)-(III), (c)-(II), (d)-(I)", "(a)-(III), (b)-(IV), (c)-(I), (d)-(II)", "(a)-(II), (b)-(III), (c)-(IV), (d)-(I)", "(a)-(I), (b)-(II), (c)-(III), (d)-(IV)"],
     "correct_answer":"(a)-(IV), (b)-(III), (c)-(II), (d)-(I)",
     "explanation":"The correct answer is (A) (a)-(IV), (b)-(III), (c)-(II), (d)-(I). This is a standard UGC NET 2024 June question on Data Interpretation."},
    {"id":"di060","topic":"Data Interpretation","difficulty":"Easy","year":2024,"season":"June",
     "question":"What is the influence of modernity on folk traditions and public space according to the text?",
     "options":["Folk traditions are disappearing.", "It has no effect on ancient tradition.", "It only leads to conflicts without resolution.", "It makes social changes more acceptable."],
     "correct_answer":"It makes social changes more acceptable.",
     "explanation":"The correct answer is (D) It makes social changes more acceptable.. This is a standard UGC NET 2024 June question on Data Interpretation."},
    {"id":"di061","topic":"Data Interpretation","difficulty":"Easy","year":2024,"season":"June",
     "question":"Main aim of Santiniketan can be stated as:",
     "options":["To spread the culture of Kolkata", "To completely ignore the western influences", "To emphasize on a culture that was Bengali/Indian yet significant to the modern world", "To focus only on the traditional folk culture"],
     "correct_answer":"To emphasize on a culture that was Bengali/Indian yet significant to the modern world",
     "explanation":"The correct answer is (C) To emphasize on a culture that was Bengali/Indian yet significant to the modern world. This is a standard UGC NET 2024 June question on Data Interpretation."},
    {"id":"di062","topic":"Data Interpretation","difficulty":"Easy","year":2024,"season":"June",
     "question":"In which year was the difference between Ajay's average monthly income and Amit's average monthly income second highest?",
     "options":["2015", "2016", "2017", "2019"],
     "correct_answer":"2016",
     "explanation":"The correct answer is (B) 2016. This is a standard UGC NET 2024 June question on Data Interpretation."},
    {"id":"di063","topic":"Data Interpretation","difficulty":"Easy","year":2024,"season":"June",
     "question":"What was the difference between the total of the average monthly income of Amit in all the years together and Anil's average monthly income in the year 2017?",
     "options":["₹ 2.48 lakhs", "₹ 2.26 lakhs", "₹ 24.8 lakhs", "₹ 22.6 lakhs"],
     "correct_answer":"₹ 2.26 lakhs",
     "explanation":"The correct answer is (B) ₹ 2.26 lakhs. This is a standard UGC NET 2024 June question on Data Interpretation."},
    {"id":"di064","topic":"Data Interpretation","difficulty":"Easy","year":2024,"season":"June",
     "question":"What was the percentage (%) increase in the average monthly income of Ajay in the year 2018 as compared to the previous year?",
     "options":["50", "150", "160", "60"],
     "correct_answer":"50",
     "explanation":"The correct answer is (A) 50. This is a standard UGC NET 2024 June question on Data Interpretation."},
    {"id":"di065","topic":"Data Interpretation","difficulty":"Medium","year":2024,"season":"June",
     "question":"Identify the correct sequence of steps used for Sandler's A-test: (a) Subtract the hypothesised mean of the population (µH) from each individual score (Xi) (b) Find ∑Di (c) Square each Di (d) Obtain the sum of each squares",
     "options":["(b), (d), (c), (a)", "(c), (d), (b), (a)", "(a), (b), (c), (d)", "(a), (c), (b), (d)"],
     "correct_answer":"(a), (b), (c), (d)",
     "explanation":"The correct answer is (C) (a), (b), (c), (d). This is a standard UGC NET 2024 June question on Data Interpretation."},
    {"id":"ict1049","topic":"Data Interpretation","difficulty":"Easy","year":2024,"season":"June",
     "question":"Number of boys who are enrolled in Soccer is _______ % of the number of boys who are enrolled in all the five sports games.",
     "options":["10.2", "11.2", "12.2", "13.2"],
     "correct_answer":"11.2",
     "explanation":"The correct answer is (B) 11.2. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ict1050","topic":"Data Interpretation","difficulty":"Easy","year":2024,"season":"June",
     "question":"What is the number of boys who are enrolled in the game Basketball?",
     "options":["805", "430", "840", "470"],
     "correct_answer":"470",
     "explanation":"The correct answer is (D) 470. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ict1051","topic":"Data Interpretation","difficulty":"Easy","year":2024,"season":"June",
     "question":"What is the difference between the number of girls and the number of boys who are enrolled in the game of Tennis?",
     "options":["340", "370", "390", "320"],
     "correct_answer":"340",
     "explanation":"The correct answer is (A) 340. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ict1052","topic":"Data Interpretation","difficulty":"Easy","year":2024,"season":"June",
     "question":"Number of boys who are enrolled in Cricket is approximately _______ % more than the number of students who are enrolled in Badminton.",
     "options":["21.79", "22.71", "23.81", "25.91"],
     "correct_answer":"23.81",
     "explanation":"The correct answer is (C) 23.81. This is a standard UGC NET 2024 June question on Teaching Aptitude."},
    {"id":"ict1057","topic":"Data Interpretation","difficulty":"Easy","year":2024,"season":"June",
     "question":"If the number of people in city-A belonging to the age group of (19-35] years is 31680, then how many people are there in the age group of more than 60 years?",
     "options":["21120", "24280", "23680", "19350"],
     "correct_answer":"21120",
     "explanation":"The correct answer is (A) 21120. This is a standard UGC NET 2024 June question on Teaching Aptitude."},


    # ↑↑↑ PASTE YOUR NEW Data Interpretation QUESTIONS ABOVE THIS LINE ↑↑↑
]

# ── AI PREDICTED (upcoming exam focus) ───────────────────────────────
Q_AI_PREDICTED = [
    {"id":"ai001","topic":"Teaching Aptitude","difficulty":"Hard","year":2025,"season":"June","predicted":True,"question":"Based on NEP 2020 implementation trends, which pedagogical shift is most likely to be tested?","options":["Shift from rote learning to competency-based education","Increased emphasis on standardized testing","Reduction in teacher training programs","Focus on single-language instruction"],"correct_answer":"Shift from rote learning to competency-based education","explanation":"NEP 2020 emphasizes competency-based education as a core reform — highly likely to appear in upcoming exams."},
    {"id":"ai002","topic":"Research Aptitude","difficulty":"Medium","year":2025,"season":"June","predicted":True,"question":"With increasing use of AI in research, which ethical concern is most prominent?","options":["Data fabrication","Algorithmic bias and transparency","Plagiarism only","Sample size issues"],"correct_answer":"Algorithmic bias and transparency","explanation":"AI-driven research raises significant concerns about algorithmic bias, reproducibility, and transparency — a trending exam topic."},
    {"id":"ai003","topic":"ICT","difficulty":"Medium","year":2025,"season":"June","predicted":True,"question":"Which technology is central to India's Digital India initiative for education?","options":["Blockchain","Cloud computing and mobile internet","Quantum computing","5G only"],"correct_answer":"Cloud computing and mobile internet","explanation":"Digital India's education thrust relies on cloud-based platforms and mobile internet access for DIKSHA, SWAYAM, etc."},
    {"id":"ai004","topic":"Environment & Ecology","difficulty":"Hard","year":2025,"season":"June","predicted":True,"question":"India's National Action Plan on Climate Change (NAPCC) includes how many missions?","options":["6","8","10","12"],"correct_answer":"8","explanation":"NAPCC has 8 national missions covering solar energy, water, forests, sustainable agriculture, etc. — frequently tested."},
    {"id":"ai005","topic":"Higher Education","difficulty":"Medium","year":2025,"season":"December","predicted":True,"question":"The Academic Bank of Credits (ABC) under NEP 2020 primarily facilitates:","options":["Financial aid to students","Multiple entry/exit and credit transfer","Faculty recruitment","Research funding"],"correct_answer":"Multiple entry/exit and credit transfer","explanation":"ABC enables credit accumulation and transfer, supporting flexible degree completion pathways under NEP 2020."},
    # ════════════════════════════════════════════════════════════════════
    # ADD MORE AI Predicted QUESTIONS BELOW ↓
    # ════════════════════════════════════════════════════════════════════
    # Remember: add  "predicted": True  to every question here

    # ↑↑↑ PASTE YOUR NEW AI Predicted QUESTIONS ABOVE THIS LINE ↑↑↑
]

# ── Master list: all topics combined ─────────────────────────────────
BUILTIN_QUESTIONS = (
    Q_TEACHING_APTITUDE +
    Q_RESEARCH_APTITUDE +
    Q_READING_COMPREHENSION +
    Q_COMMUNICATION +
    Q_REASONING +
    Q_ICT +
    Q_ENVIRONMENT +
    Q_HIGHER_EDUCATION +
    Q_GOVERNANCE +
    Q_DATA_INTERPRETATION
)
AI_PREDICTED_QUESTIONS = Q_AI_PREDICTED


class QuestionBank:
    def __init__(self, filepath=QUESTION_BANK_FILE):
        self.filepath = filepath
        self._ensure_file()

    def _ensure_file(self):
        all_builtin = BUILTIN_QUESTIONS + AI_PREDICTED_QUESTIONS
        if not os.path.exists(self.filepath):
            self._save(all_builtin)
        else:
            existing = self._load()
            existing_ids = {q.get("id") for q in existing}
            new_ones = [q for q in all_builtin if q.get("id") not in existing_ids]
            if new_ones:
                existing.extend(new_ones)
                self._save(existing)

    def _load(self):
        try:
            with open(self.filepath) as f:
                return json.load(f)
        except:
            return list(BUILTIN_QUESTIONS)

    def _save(self, questions):
        with open(self.filepath, "w") as f:
            json.dump(questions, f, indent=2)

    def get_all(self): return self._load()

    def get_topics(self):
        return sorted(set(q.get("topic","General") for q in self._load()))

    def get_years(self):
        return sorted(set(int(q["year"]) for q in self._load() if q.get("year")), reverse=True)

    def get_seasons(self):
        return sorted(set(q["season"] for q in self._load() if q.get("season")))

    def get_filtered(self, topics=None, difficulty="Mixed", years=None,
                     seasons=None, n=50, predicted_only=False, shuffle=True):
        qs = self._load()
        if predicted_only:
            qs = [q for q in qs if q.get("predicted")]
        if topics:
            qs = [q for q in qs if q.get("topic") in topics]
        if difficulty != "Mixed":
            f = [q for q in qs if q.get("difficulty") == difficulty]
            if f: qs = f
        if years:
            f = [q for q in qs if str(q.get("year","")) in [str(y) for y in years]]
            if f: qs = f
        if seasons:
            f = [q for q in qs if q.get("season","") in seasons]
            if f: qs = f
        if shuffle:
            random.shuffle(qs)
        return qs[:n]

    def add(self, new_qs):
        existing = self._load()
        ids = {q.get("id") for q in existing}
        for q in new_qs:
            if not q.get("id"): q["id"] = str(uuid.uuid4())[:8]
            if q["id"] not in ids:
                existing.append(q)
                ids.add(q["id"])
        self._save(existing)


# ═══════════════════════════════════════════════
# USER AUTH  (flat-file, bcrypt-free simple hash)
# ═══════════════════════════════════════════════
def _hash(pw): return hashlib.sha256(pw.encode()).hexdigest()

def load_users():
    if not os.path.exists(USERS_FILE): return {}
    try:
        with open(USERS_FILE) as f: return json.load(f)
    except: return {}

def save_users(users):
    with open(USERS_FILE, "w") as f: json.dump(users, f, indent=2)

def register_user(username, password, name):
    users = load_users()
    if username in users: return False, "Username already exists"
    users[username] = {"name": name, "pw_hash": _hash(password),
                       "joined": datetime.now().isoformat()[:10], "attempts": 0}
    save_users(users)
    return True, "ok"

def verify_user(username, password):
    users = load_users()
    if username not in users: return False, None
    if users[username]["pw_hash"] == _hash(password): return True, users[username]
    return False, None

# ═══════════════════════════════════════════════
# SCORES / LEADERBOARD
# ═══════════════════════════════════════════════
def load_scores():
    if not os.path.exists(SCORES_FILE): return []
    try:
        with open(SCORES_FILE) as f: return json.load(f)
    except: return []

def save_score(username, name, score, total, pct, mode, duration_secs):
    scores = load_scores()
    scores.append({
        "username": username, "name": name, "score": score,
        "total": total, "pct": pct, "mode": mode,
        "duration": duration_secs,
        "ts": datetime.now().isoformat()
    })
    with open(SCORES_FILE, "w") as f: json.dump(scores, f, indent=2)

def get_leaderboard(mode=None, limit=20):
    scores = load_scores()
    if mode: scores = [s for s in scores if s.get("mode") == mode]
    # Best score per user
    best = {}
    for s in scores:
        u = s["username"]
        if u not in best or s["pct"] > best[u]["pct"]:
            best[u] = s
    ranked = sorted(best.values(), key=lambda x: (-x["pct"], x["duration"]))
    return ranked[:limit]


# ═══════════════════════════════════════════════
# SESSION STATE
# ═══════════════════════════════════════════════
def init_state():
    defs = {
        "page": "home", "user": None, "username": None,
        "questions": [], "q_idx": 0, "answers": {},
        "quiz_active": False, "quiz_done": False,
        "quiz_mode": "practice",
        "quiz_label": "",
        "start_time": None, "q_start": None,
        "total_time": 0,
        "streak": 0, "total_attempted": 0, "total_correct": 0,
        "bookmarks": set(), "wrong_questions": [],
        "q_times": {},
        "fb_done": set(), "fb_session": 0,
        "dev_mode": False,
    }
    for k, v in defs.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()


# ═══════════════════════════════════════════════
# NAV BAR (always visible, replaces sidebar)
# ═══════════════════════════════════════════════
def render_sidebar():
    """Sidebar navigation — replaces the old topbar."""
    # Always-visible floating hamburger toggle
    st.markdown("""
    <style>
    [data-testid="stSidebarCollapseButton"] { display: none !important; }
    #custom-sidebar-toggle {
        position: fixed; z-index: 99999;
        /* Desktop: top-left */
        top: 0.7rem; left: 0.7rem;
        width: 2.5rem; height: 2.5rem;
        background: linear-gradient(135deg, #7c3aed, #a855f7);
        border: none; border-radius: 50%; cursor: pointer;
        display: flex; align-items: center; justify-content: center;
        box-shadow: 0 4px 18px rgba(124,58,237,0.55);
        transition: box-shadow 0.2s, transform 0.15s; outline: none;
        -webkit-tap-highlight-color: transparent;
        touch-action: manipulation;
    }
    #custom-sidebar-toggle:hover { box-shadow: 0 6px 24px rgba(124,58,237,0.75); transform: scale(1.08); }
    #custom-sidebar-toggle:active { transform: scale(0.94); }
    #custom-sidebar-toggle svg { width: 1.1rem; height: 1.1rem; fill: #ffffff; pointer-events: none; }
    .main .block-container { padding-top: 3.5rem !important; }
    @media (min-width: 768px) { .main .block-container { padding-top: 1.5rem !important; } }

    /* Mobile: move button to bottom-right for thumb reach */
    @media (max-width: 600px) {
        #custom-sidebar-toggle {
            top: auto !important;
            left: auto !important;
            bottom: 1.2rem !important;
            right: 1.2rem !important;
            width: 3rem !important;
            height: 3rem !important;
            box-shadow: 0 6px 24px rgba(124,58,237,0.7) !important;
        }
        #custom-sidebar-toggle svg { width: 1.3rem !important; height: 1.3rem !important; }
        .main .block-container { padding-top: 0.75rem !important; padding-bottom: 5.5rem !important; }
    }
    </style>
    <button id="custom-sidebar-toggle" aria-label="Toggle sidebar">
        <svg viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="2" rx="1"/><rect x="3" y="11" width="18" height="2" rx="1"/><rect x="3" y="17" width="18" height="2" rx="1"/></svg>
    </button>
    <script>
    (function(){
        var btn = document.getElementById('custom-sidebar-toggle');
        if (!btn) return;
        function clickNativeToggle() {
            var collapsed = document.querySelector('[data-testid="collapsedControl"]');
            if (collapsed) { collapsed.click(); return; }
            var closeBtn = document.querySelector('[data-testid="stSidebarCollapseButton"] button');
            if (closeBtn) { closeBtn.click(); return; }
        }
        btn.addEventListener('click', function(e){ e.stopPropagation(); clickNativeToggle(); });
        function ensureButton(){ if (!document.getElementById('custom-sidebar-toggle')) document.body.appendChild(btn); }
        new MutationObserver(ensureButton).observe(document.body, {childList:true, subtree:false});
    })();
    </script>
    """, unsafe_allow_html=True)

    user = st.session_state.get("user")
    with st.sidebar:
        # Brand
        initials = ""
        if user:
            initials = "".join(w[0].upper() for w in user.get("name","U").split()[:2])
        st.markdown(f"""
        <div class="sidebar-brand">
            <div style="font-size:1.8rem;">🎓</div>
            <div>
                <div class="brand-title">NET Guru</div>
                <div class="brand-subtitle">UGC NET · Paper 1</div>
            </div>
        </div>""", unsafe_allow_html=True)

        st.markdown("---")

        # Main nav
        pages_public = [("🏛️","Home","home"),("📅","PYQ Yearwise","pyq"),("📝","Practice","quiz"),("🧪","Mock Tests","mock"),("🏆","Leaderboard","leaderboard")]
        pages_private = [("🤖","AI Predict","ai"),("📊","Analytics","analytics"),("🔖","Bookmarks","bookmarks")]

        all_pages = pages_public + (pages_private if user else [])
        for icon, label, key in all_pages:
            active = st.session_state.page == key
            if st.button(f"{icon}  {label}", key=f"nav_{key}",
                         use_container_width=True,
                         type="primary" if active else "secondary"):
                st.session_state.page = key
                st.session_state.quiz_active = False
                st.rerun()

        st.markdown("---")

        # Login / Profile
        if user:
            if st.button(f"👤  {user.get('name','').split()[0]} (Profile)", key="nav_profile",
                         use_container_width=True, type="primary" if st.session_state.page == "login" else "secondary"):
                st.session_state.page = "login"
                st.rerun()
            if st.button("🚪  Logout", key="nav_logout", use_container_width=True):
                st.session_state.user = None
                st.session_state.username = None
                st.session_state.page = "home"
                st.rerun()
        else:
            if st.button("👤  Login / Register", key="nav_login",
                         use_container_width=True,
                         type="primary" if st.session_state.page == "login" else "secondary"):
                st.session_state.page = "login"
                st.rerun()

        st.markdown("---")

        # Developer mode
        if st.session_state.get("dev_mode"):
            st.markdown(
                '<div style="background:rgba(251,191,36,0.12);border:1px solid rgba(251,191,36,0.4);'
                'border-radius:10px;padding:0.5rem 0.75rem;margin-bottom:0.6rem;font-size:0.78rem;'
                'color:#fbbf24;font-weight:700;text-align:center;">🔧 DEVELOPER MODE</div>',
                unsafe_allow_html=True
            )
            if st.button("📄  PDF Upload", key="nav_pdf", use_container_width=True,
                         type="primary" if st.session_state.page == "pdf_upload" else "secondary"):
                st.session_state.page = "pdf_upload"
                st.rerun()
            if st.button("🔒  Exit Dev Mode", key="nav_exitdev", use_container_width=True):
                st.session_state.dev_mode = False
                if st.session_state.page == "pdf_upload":
                    st.session_state.page = "home"
                st.rerun()
        else:
            with st.expander("🔧 Developer", expanded=False):
                pin = st.text_input("PIN", type="password", key="dev_pin_input", placeholder="Enter PIN")
                if st.button("Unlock", key="dev_unlock", use_container_width=True, type="primary"):
                    if pin == DEVELOPER_PIN:
                        st.session_state.dev_mode = True
                        st.rerun()
                    else:
                        st.error("❌ Incorrect PIN")

        st.markdown("---")

        # Stats strip
        attempted = st.session_state.total_attempted
        accuracy  = round(st.session_state.total_correct / attempted * 100) if attempted > 0 else 0
        streak    = st.session_state.streak
        st.markdown(f"""
        <div class="sidebar-stats">
            <div class="stat-mini"><span class="stat-mini-val">{attempted}</span><span class="stat-mini-lbl">Done</span></div>
            <div class="stat-mini"><span class="stat-mini-val">{accuracy}%</span><span class="stat-mini-lbl">Accuracy</span></div>
            <div class="stat-mini"><span class="stat-mini-val">{streak}🔥</span><span class="stat-mini-lbl">Streak</span></div>
        </div>""", unsafe_allow_html=True)

        st.markdown(
            '<div style="text-align:center;opacity:0.4;font-size:0.72rem;padding:0.75rem 0.5rem 0;">'
            'NYZTrade Education<br><span style="color:#a855f7;">Built for NET Aspirants</span></div>',
            unsafe_allow_html=True
        )


# Keep topbar as alias for backwards compat with any old callers
def topbar():
    render_sidebar()


def page_home():
    qb = QuestionBank()
    total = len(qb.get_all())
    years = qb.get_years()
    user  = st.session_state.user

    # ── Hero ──────────────────────────────────────
    st.markdown(f"""
    <div class="hero">
      <div class="hero-badge">🏛️ UGC NET &nbsp;·&nbsp; Paper 1 &nbsp;·&nbsp; NYZTrade Education</div>
      <h1 class="hero-title">Master NET with<br><em>Intelligent Practice</em></h1>
      <div class="hero-features">
        <span class="hero-pill"><span class="pill-icon">📅</span> PYQ Year-wise Tests</span>
        <span class="hero-pill"><span class="pill-icon">🧪</span> Mock &amp; Exam Simulation</span>
        <span class="hero-pill"><span class="pill-icon">🏆</span> Live Leaderboard</span>
        <span class="hero-pill"><span class="pill-icon">📊</span> Analytics Dashboard</span>
        <span class="hero-pill"><span class="pill-icon">🔖</span> Bookmarks &amp; Review</span>
        <span class="hero-pill"><span class="pill-icon">⚡</span> Instant Feedback</span>
      </div>
    </div>""", unsafe_allow_html=True)

    # ── Stat strip ────────────────────────────────
    user_attempts = st.session_state.total_attempted
    user_accuracy = round(st.session_state.total_correct / user_attempts * 100) if user_attempts else 0
    streak = st.session_state.get("streak", 0)
    st.markdown(f"""
    <div class="stat-strip">
      <div class="stat-cell">
        <span class="stat-icon">📚</span>
        <span class="stat-val">{total}+</span>
        <span class="stat-lbl">Questions</span>
      </div>
      <div class="stat-cell">
        <span class="stat-icon">📅</span>
        <span class="stat-val">{len(years)}</span>
        <span class="stat-lbl">PYQ Years</span>
      </div>
      <div class="stat-cell">
        <span class="stat-icon">🎯</span>
        <span class="stat-val">10</span>
        <span class="stat-lbl">Topics</span>
      </div>
      <div class="stat-cell">
        <span class="stat-icon">✏️</span>
        <span class="stat-val">{user_attempts}</span>
        <span class="stat-lbl">Attempted</span>
      </div>
      <div class="stat-cell">
        <span class="stat-icon">🎯</span>
        <span class="stat-val">{user_accuracy}%</span>
        <span class="stat-lbl">Accuracy</span>
      </div>
      <div class="stat-cell">
        <span class="stat-icon">🔥</span>
        <span class="stat-val">{streak}</span>
        <span class="stat-lbl">Streak</span>
      </div>
    </div>""", unsafe_allow_html=True)

    # ── Quick-start cards ─────────────────────────
    st.markdown('<div class="section-label">Quick Start <span class="pill">choose a mode</span></div>', unsafe_allow_html=True)

    cards = [
        ("📅", "PYQ Yearwise",   "15-Q tests by year, season & topic",  "pyq",   "var(--amber)",   "amber",   "2023 · 2022 · 15 Qs each"),
        ("🧪", "Mock Tests",     "15-Q sprints, full mocks & exam sim", "mock",  "var(--indigo)",  "indigo",  "⚡ 15-Q · 🎓 Exam Sim"),
        ("🤖", "AI Predicted",   "Smart questions for upcoming exams",  "ai",    "var(--teal)",    "teal",    "June 2025 focus"),
        ("⚡", "Quick Drill",    "15 questions, 15 min sprint",         "quick", "var(--emerald)", "emerald", "All topics mixed"),
    ]
    # On mobile Streamlit columns stack naturally — use 2 cols for better mobile layout
    import streamlit as _st
    _is_mobile_hint = False  # Streamlit doesn't expose screen width; CSS handles stacking
    c1, c2 = st.columns(2)
    c3, c4 = st.columns(2)
    for col, (icon, title, desc, dest, accent, chip_cls, meta) in zip([c1,c2,c3,c4], cards):
        with col:
            st.markdown(f"""<div class="card">
              <div class="card-accent-top" style="background:{accent};"></div>
              <div class="card-glow" style="background:{accent};"></div>
              <span class="card-icon">{icon}</span>
              <div class="card-title">{title}</div>
              <div class="card-desc">{desc}</div>
              <div class="card-meta"><span class="chip {chip_cls}">{meta}</span></div>
            </div>""", unsafe_allow_html=True)
            if st.button("Start →", key=f"home_{dest}", use_container_width=True, type="primary"):
                if dest == "quick":
                    _start_quiz(QuestionBank().get_filtered(n=15, shuffle=True), "practice", "Quick Drill (15 Qs)", 15*60)
                else:
                    st.session_state.page = dest
                st.rerun()

    # ── PYQ Year Grid ─────────────────────────────
    st.markdown('<div class="section-label">PYQ Years <span class="pill">click to practice</span></div>', unsafe_allow_html=True)
    all_q = qb.get_all()
    n_years = min(len(years), 9)
    if n_years:
        year_cols = st.columns(n_years)
        for i, yr in enumerate(years[:n_years]):
            cnt = len([q for q in all_q if str(q.get("year","")) == str(yr)])
            with year_cols[i]:
                st.markdown(f"""<div class="year-card">
                  <span class="year-num">{yr}</span>
                  <div class="year-count">{cnt} Qs</div>
                </div>""", unsafe_allow_html=True)
                if st.button(str(yr), key=f"home_yr_{yr}", use_container_width=True):
                    qs = qb.get_filtered(years=[yr], n=50)
                    _start_quiz(qs, "practice", f"PYQ {yr}", 60*60)
                    st.rerun()

    # ── Leaderboard preview ───────────────────────
    st.markdown('<div class="section-label">Top Rankers <span class="pill">leaderboard</span></div>', unsafe_allow_html=True)
    lb = get_leaderboard(limit=5)
    if lb:
        for i, row in enumerate(lb):
            rank_cls = ["gold","silver","bronze","rest","rest"][i]
            medal    = ["🥇","🥈","🥉","4","5"][i]
            initials = "".join(w[0].upper() for w in row["name"].split()[:2])
            is_me    = row["username"] == st.session_state.username
            me_cls   = "lb-row me" if is_me else "lb-row"
            ts_str   = datetime.fromisoformat(row["ts"]).strftime("%d %b") if row.get("ts") else ""
            st.markdown(f"""<div class="{me_cls}">
              <div class="lb-rank {rank_cls}">{medal}</div>
              <div class="lb-avatar">{initials}</div>
              <div style="flex:1">
                <div class="lb-name">{row["name"]} {"⭐" if is_me else ""}</div>
                <div class="lb-detail">{row.get("mode","—")} · {ts_str}</div>
              </div>
              <div class="lb-score">{row["pct"]}%
                <div style="color:var(--t3);font-size:0.68rem;">{row["score"]}/{row["total"]}</div>
              </div>
            </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""<div class="empty-state">
          <span class="icon">🏆</span>
          <h3>No scores yet</h3>
          <p>Complete a quiz to appear on the leaderboard!</p>
        </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════
# PYQ PAGE
# ═══════════════════════════════════════════════
def _pyq_card_btn(label, key, count, on_click_fn, tag_color="#e8a020"):
    """Helper to render a mini PYQ launch card."""
    disabled = count == 0
    badge = f'<span style="font-size:0.65rem;background:{"rgba(16,185,129,0.15)" if count>0 else "rgba(78,98,133,0.2)"};color:{"var(--emerald)" if count>0 else "var(--t3)"};padding:0.1rem 0.5rem;border-radius:20px;font-family:Fira Code,monospace;">{count}q</span>'
    st.markdown(f'<div style="display:flex;align-items:center;gap:0.4rem;margin-bottom:0.25rem;">{badge}</div>', unsafe_allow_html=True)
    if st.button(label, key=key, use_container_width=True,
                 type="primary" if count > 0 else "secondary", disabled=disabled):
        on_click_fn()

def page_pyq():
    qb = QuestionBank()
    all_q = qb.get_all()

    st.markdown("""<div class="page-header">
      <h1>📅 PYQ Yearwise Tests</h1>
      <p>Previous Year Questions organized by year — <strong>15 questions per session</strong> · 30 minutes · Auto-scored · Ranked on leaderboard.</p>
    </div>""", unsafe_allow_html=True)

    available_years = qb.get_years()

    # ── Hero: Yearwise Test Grid ─────────────────
    st.markdown('<div class="section-label">📅 Pick a Year <span class="pill">15 Qs · 30 min · click to launch</span></div>', unsafe_allow_html=True)

    if not available_years:
        st.markdown("""<div class="card" style="text-align:center;padding:3rem;border-color:rgba(232,160,32,0.25);">
          <div style="font-size:3rem;margin-bottom:1rem;">📂</div>
          <div style="font-family:'Playfair Display',serif;font-weight:800;font-size:1.1rem;color:var(--t2);">No PYQ data yet</div>
          <div style="color:var(--t3);font-size:0.85rem;margin-top:0.5rem;max-width:320px;margin-left:auto;margin-right:auto;">Upload PDF question papers via Developer mode to populate year-wise questions. Questions will auto-appear here.</div>
        </div>""", unsafe_allow_html=True)
    else:
        # ── Year cards — 3 per row, rich design ──
        yr_rows = [available_years[i:i+3] for i in range(0, len(available_years), 3)]
        for row in yr_rows:
            yr_cols = st.columns(len(row))
            for col_i, yr in enumerate(row):
                yr_q      = [q for q in all_q if str(q.get("year",""))==str(yr)]
                june_cnt  = len([q for q in yr_q if q.get("season")=="June"])
                dec_cnt   = len([q for q in yr_q if q.get("season")=="December"])
                total_cnt = len(yr_q)
                easy_c  = len([q for q in yr_q if q.get("difficulty")=="Easy"])
                med_c   = len([q for q in yr_q if q.get("difficulty")=="Medium"])
                hard_c  = len([q for q in yr_q if q.get("difficulty")=="Hard"])
                avail_15 = total_cnt >= 15

                with yr_cols[col_i]:
                    st.markdown(f"""<div class="card" style="border-color:rgba(232,160,32,{'0.4' if avail_15 else '0.15'});margin-bottom:0.25rem;position:relative;overflow:hidden;">
                      <div style="position:absolute;top:0;right:0;width:60px;height:60px;
                        background:radial-gradient(circle at top right,rgba(232,160,32,0.12),transparent 70%);"></div>
                      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:0.6rem;">
                        <span style="font-family:'Playfair Display',serif;font-weight:900;font-size:1.6rem;
                          color:{'var(--amber)' if avail_15 else 'var(--t3)'};">{yr}</span>
                        <span style="font-size:0.65rem;background:{'rgba(232,160,32,0.15)' if avail_15 else 'rgba(78,98,133,0.15)'};
                          color:{'var(--amber2)' if avail_15 else 'var(--t3)'};padding:0.2rem 0.5rem;border-radius:20px;
                          font-family:'Fira Code',monospace;">{total_cnt}q total</span>
                      </div>
                      <div style="display:flex;gap:0.5rem;margin-bottom:0.6rem;flex-wrap:wrap;">
                        <span style="font-size:0.65rem;color:var(--t3);">☀️ {june_cnt}</span>
                        <span style="font-size:0.65rem;color:var(--t3);">❄️ {dec_cnt}</span>
                        <span style="font-size:0.65rem;color:var(--emerald);">E:{easy_c}</span>
                        <span style="font-size:0.65rem;color:var(--amber);">M:{med_c}</span>
                        <span style="font-size:0.65rem;color:var(--rose);">H:{hard_c}</span>
                      </div>
                    </div>""", unsafe_allow_html=True)

                    # 3 launch buttons per year
                    b1, b2, b3 = st.columns(3)
                    with b1:
                        if st.button(f"☀️ Jun", key=f"pyq_j_{yr}", use_container_width=True,
                                     type="primary" if june_cnt>=15 else "secondary", disabled=june_cnt==0):
                            qs = qb.get_filtered(years=[yr], seasons=["June"], n=15)
                            _start_quiz(qs, "practice", f"PYQ {yr} ☀️ June", 30*60); st.rerun()
                    with b2:
                        if st.button(f"❄️ Dec", key=f"pyq_d_{yr}", use_container_width=True,
                                     type="primary" if dec_cnt>=15 else "secondary", disabled=dec_cnt==0):
                            qs = qb.get_filtered(years=[yr], seasons=["December"], n=15)
                            _start_quiz(qs, "practice", f"PYQ {yr} ❄️ Dec", 30*60); st.rerun()
                    with b3:
                        if st.button(f"🎯 All", key=f"pyq_a_{yr}", use_container_width=True,
                                     type="primary" if avail_15 else "secondary", disabled=total_cnt==0):
                            qs = qb.get_filtered(years=[yr], n=15)
                            _start_quiz(qs, "practice", f"PYQ {yr} (All)", 30*60); st.rerun()

                    st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Season Series ──────────────────────────────────
    st.markdown('<div class="section-label">📆 Season Series <span class="pill">15 Qs across all years</span></div>', unsafe_allow_html=True)
    june_total = len([q for q in all_q if q.get("season")=="June"])
    dec_total  = len([q for q in all_q if q.get("season")=="December"])

    sc1, sc2 = st.columns(2)
    with sc1:
        st.markdown(f"""<div class="card" style="border-color:rgba(232,160,32,0.35);">
          <div class="card-accent-top" style="background:var(--amber);"></div>
          <div style="display:flex;align-items:center;gap:1rem;">
            <span style="font-size:2.2rem;">☀️</span>
            <div>
              <div class="card-title">June Series</div>
              <div class="card-desc">All June-session PYQs · {june_total} questions available</div>
              <div class="card-meta" style="margin-top:0.4rem;"><span class="chip">15 Qs</span><span class="chip amber">18 min</span><span class="chip">Mixed</span></div>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)
        if st.button("☀️ Start June Series →", key="pyq_june_all", use_container_width=True, type="primary", disabled=june_total==0):
            qs = qb.get_filtered(seasons=["June"], n=15)
            _start_quiz(qs, "practice", "June PYQ Series", 30*60); st.rerun()

    with sc2:
        st.markdown(f"""<div class="card" style="border-color:rgba(15,184,201,0.35);">
          <div class="card-accent-top" style="background:var(--teal);"></div>
          <div style="display:flex;align-items:center;gap:1rem;">
            <span style="font-size:2.2rem;">❄️</span>
            <div>
              <div class="card-title">December Series</div>
              <div class="card-desc">All December-session PYQs · {dec_total} questions available</div>
              <div class="card-meta" style="margin-top:0.4rem;"><span class="chip">15 Qs</span><span class="chip teal">18 min</span><span class="chip">Mixed</span></div>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)
        if st.button("❄️ Start December Series →", key="pyq_dec_all", use_container_width=True, type="primary", disabled=dec_total==0):
            qs = qb.get_filtered(seasons=["December"], n=15)
            _start_quiz(qs, "practice", "December PYQ Series", 30*60); st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Topic-wise PYQ ─────────────────────────────────
    st.markdown('<div class="section-label">📚 Topic-wise PYQ <span class="pill">15 Qs · filtered by topic</span></div>', unsafe_allow_html=True)
    topic_list = qb.get_topics()
    t_cols = st.columns(2)
    for ti, topic in enumerate(topic_list):
        t_cnt = len([q for q in all_q if q.get("topic")==topic and not q.get("predicted")])
        with t_cols[ti % 2]:
            c1, c2 = st.columns([3, 1])
            with c1:
                st.markdown(f"""<div style="background:var(--surface2);border:1px solid var(--line2);border-radius:var(--r-sm);
                  padding:0.5rem 0.75rem;margin-bottom:0.3rem;display:flex;align-items:center;justify-content:space-between;">
                  <span style="font-size:0.82rem;font-weight:600;color:var(--t1);">{topic}</span>
                  <span style="font-family:'Fira Code',monospace;font-size:0.7rem;color:var(--t3);">{t_cnt}q</span>
                </div>""", unsafe_allow_html=True)
            with c2:
                if st.button("▶", key=f"pyq_t_{ti}", use_container_width=True, disabled=t_cnt==0):
                    qs = qb.get_filtered(topics=[topic], n=15)
                    _start_quiz(qs, "practice", f"PYQ · {topic}", 30*60); st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Custom filter session ─────────────────────
    st.markdown('<div class="section-label">🔎 Custom Filter Session</div>', unsafe_allow_html=True)
    with st.expander("▸ Advanced Filters (year + season + topic + difficulty)", expanded=False):
        fc1, fc2, fc3 = st.columns(3)
        with fc1: sel_years   = st.multiselect("Year",   options=qb.get_years(),   default=[], placeholder="All years",   key="pyq_years")
        with fc2: sel_seasons = st.multiselect("Season", options=qb.get_seasons(), default=[], placeholder="All seasons", key="pyq_seasons")
        with fc3: sel_topics  = st.multiselect("Topics", options=qb.get_topics(),  default=[], placeholder="All topics",  key="pyq_topics")
        fc4, fc5 = st.columns(2)
        with fc4: sel_diff = st.selectbox("Difficulty", ["Mixed","Easy","Medium","Hard"], key="pyq_diff")
        with fc5: sel_n    = st.select_slider("Questions", [10,15,20,25,30], value=15, key="pyq_n")

        preview = qb.get_filtered(topics=sel_topics or None, difficulty=sel_diff,
                                   years=sel_years or None, seasons=sel_seasons or None, n=9999, shuffle=False)
        st.markdown(f'<div style="color:var(--indigo2);font-weight:700;font-size:0.84rem;margin-bottom:0.75rem;">✅ {len(preview)} match · {min(sel_n,len(preview))} will be used · {sel_n * 2} min timed</div>', unsafe_allow_html=True)

        if st.button("🚀 Start Filtered PYQ Session", use_container_width=True, type="primary", key="pyq_start"):
            qs = qb.get_filtered(topics=sel_topics or None, difficulty=sel_diff,
                                 years=sel_years or None, seasons=sel_seasons or None, n=sel_n)
            if not qs: st.error("No questions match your filters. Try broadening the selection.")
            else: _start_quiz(qs, "practice", f"PYQ Custom ({sel_diff})", sel_n * 120); st.rerun()


# ═══════════════════════════════════════════════
# MOCK TESTS PAGE
# ═══════════════════════════════════════════════
MOCK_BLUEPRINTS = [
    # 15-Q Sprints (primary category — shown first)
    {"id":"m_15_mix","name":"15-Q Sprint — Mixed","icon":"⚡","tag":"15-Q Mock","tag_c":"gold","total":15,"mins":30,"diff":"Mixed","topics":None,"seasons":None,"desc":"15 mixed questions · 18 min · All topics · Perfect revision session","exam_sim":False},
    {"id":"m_15_b","name":"15-Q Sprint — Set B","icon":"⚡","tag":"15-Q Mock","tag_c":"gold","total":15,"mins":30,"diff":"Mixed","topics":None,"seasons":None,"desc":"Fresh shuffle · same 30-min format · compare with Set A"},
    {"id":"m_15_hard","name":"15-Q Hard Challenge","icon":"🔥","tag":"15-Q Mock","tag_c":"red","total":15,"mins":30,"diff":"Hard","topics":None,"seasons":None,"desc":"Hard questions only · 18 min · Tests your exam readiness"},
    {"id":"m_15_easy","name":"15-Q Warm-Up","icon":"🌱","tag":"15-Q Mock","tag_c":"green","total":15,"mins":30,"diff":"Easy","topics":None,"seasons":None,"desc":"Easy questions · great for beginners · confidence builder"},
    {"id":"m_15_teach","name":"15-Q Teaching Focus","icon":"🧠","tag":"15-Q Mock","tag_c":"cyan","total":15,"mins":30,"diff":"Mixed","topics":["Teaching Aptitude"],"seasons":None,"desc":"Teaching Aptitude only · 15 Qs · 30 min targeted sprint"},
    {"id":"m_15_res","name":"15-Q Research Focus","icon":"🔬","tag":"15-Q Mock","tag_c":"cyan","total":15,"mins":30,"diff":"Mixed","topics":["Research Aptitude"],"seasons":None,"desc":"Research Aptitude only · 15 Qs · 30 min targeted sprint"},
    # Full Mock Tests
    {"id":"m_full1","name":"Full Mock — Set 1","icon":"🎯","tag":"Full Mock","tag_c":"indigo","total":50,"mins":100,"diff":"Mixed","topics":None,"seasons":None,"desc":"50 questions · 100 min · All topics · Full bank shuffle","exam_sim":False},
    {"id":"m_full2","name":"Full Mock — Set 2","icon":"🎯","tag":"Full Mock","tag_c":"indigo","total":50,"mins":100,"diff":"Mixed","topics":None,"seasons":None,"desc":"Fresh shuffle · same pattern · compare your score"},
    # Exam Simulation
    {"id":"m_exam1","name":"Exam Simulation — Set 1","icon":"🎓","tag":"Exam Simulation","tag_c":"violet","total":50,"mins":100,"diff":"Mixed","topics":None,"seasons":None,"desc":"Full UGC NET pattern · 50 Qs · 100 min · Live countdown · Auto-submit","exam_sim":True},
    {"id":"m_exam2","name":"Exam Simulation — Set 2","icon":"🎓","tag":"Exam Simulation","tag_c":"violet","total":50,"mins":100,"diff":"Mixed","topics":None,"seasons":None,"desc":"New shuffle · 100-min exam conditions · ranked on leaderboard","exam_sim":True},
    # Season PYQ Mocks
    {"id":"m_june","name":"June PYQ Mock","icon":"☀️","tag":"Season Mock","tag_c":"gold","total":15,"mins":30,"diff":"Mixed","topics":None,"seasons":["June"],"desc":"15 June-session PYQs · 18 min · real exam questions"},
    {"id":"m_dec","name":"December PYQ Mock","icon":"❄️","tag":"Season Mock","tag_c":"gold","total":15,"mins":30,"diff":"Mixed","topics":None,"seasons":["December"],"desc":"15 December-session PYQs · 18 min · real exam questions"},
]

def page_mock():
    qb = QuestionBank()

    st.markdown("""<div class="page-header">
      <h1>🧪 Mock Tests</h1>
      <p>Structured tests for every level — <strong>15-Q Sprints</strong> · Full Mocks · Exam Simulation · Season PYQs. All auto-scored and ranked.</p>
    </div>""", unsafe_allow_html=True)

    # ── 15-Q Sprints — PRIMARY section ────────────
    st.markdown('<div class="section-label">⚡ 15-Question Mock Tests <span class="pill">30 min · quick & targeted · most popular</span></div>', unsafe_allow_html=True)
    sprint_mocks = [m for m in MOCK_BLUEPRINTS if m["tag"] == "15-Q Mock"]
    s_cols = st.columns(3)
    for si, m in enumerate(sprint_mocks):
        avail = qb.get_filtered(topics=m.get("topics"), difficulty=m["diff"], seasons=m.get("seasons"), n=9999, shuffle=False)
        cnt = len(avail); used = min(m["total"], cnt); can = cnt >= 10
        diff_color = {"Mixed":"var(--indigo2)","Easy":"var(--emerald)","Medium":"var(--amber)","Hard":"var(--rose)"}.get(m["diff"],"var(--t2)")
        avail_color = "var(--emerald)" if can else "var(--rose)"
        with s_cols[si % 3]:
            st.markdown(f"""<div class="card" style="border-color:{'rgba(232,160,32,0.4)' if m['diff']=='Mixed' else ('rgba(16,185,129,0.3)' if m['diff']=='Easy' else 'rgba(244,63,94,0.3)')};">
              <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:0.5rem;">
                <span style="font-size:1.8rem;">{m['icon']}</span>
                <span style="font-size:0.63rem;color:{avail_color};font-weight:700;">{'✓ ' + str(cnt) + ' avail' if can else '⚠ Upload more'}</span>
              </div>
              <div class="card-title" style="font-size:0.88rem;">{m['name']}</div>
              <div class="card-desc" style="font-size:0.76rem;">{m['desc']}</div>
              <div class="card-meta" style="margin-top:0.5rem;">
                <span class="chip" style="color:{diff_color};">⚡ {used} Qs</span>
                <span class="chip amber">⏱ 18 min</span>
              </div>
            </div>""", unsafe_allow_html=True)
            if st.button(f"▶ Start", key=f"mock_{m['id']}", use_container_width=True,
                         type="primary" if can else "secondary", disabled=not can):
                qs = qb.get_filtered(topics=m.get("topics"), difficulty=m["diff"], seasons=m.get("seasons"), n=m["total"])
                _start_quiz(qs, "exam", m["name"], m["mins"]*60); st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Exam Simulation ─────────────────────────────
    st.markdown('<div class="section-label">🎓 Exam Simulation <span class="pill">UGC NET real conditions · 50 Qs · 100 min · auto-submit · ranked</span></div>', unsafe_allow_html=True)
    sim_mocks = [m for m in MOCK_BLUEPRINTS if m.get("exam_sim")]
    sim_cols = st.columns(2)
    for i, m in enumerate(sim_mocks):
        avail = qb.get_filtered(difficulty=m["diff"], n=9999, shuffle=False)
        cnt = len(avail); can = cnt > 0; used = min(m["total"], cnt)
        with sim_cols[i]:
            st.markdown(f"""<div class="card" style="border-color:rgba(99,102,241,0.5);background:linear-gradient(135deg,rgba(99,102,241,0.07),rgba(15,184,201,0.04));">
              <div class="card-accent-top" style="background:linear-gradient(90deg,var(--indigo),var(--teal));"></div>
              <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:0.5rem;">
                <span style="font-size:1.8rem;">{m['icon']}</span>
                <span style="font-size:0.65rem;color:var(--indigo2);font-weight:700;">🔒 Exam Mode</span>
              </div>
              <div class="card-title" style="color:var(--indigo2);">{m['name']}</div>
              <div class="card-desc">{m['desc']}</div>
              <div class="card-meta">
                <span class="chip" style="color:var(--indigo2);">📝 {used} Qs</span>
                <span class="chip amber">⏱ 180 min</span>
                <span class="chip" style="color:var(--rose);">🏆 Ranked</span>
              </div>
            </div>""", unsafe_allow_html=True)
            if st.button(f"🎓 Launch Exam Simulation", key=f"mock_{m['id']}", use_container_width=True,
                         type="primary" if can else "secondary", disabled=not can):
                qs = qb.get_filtered(n=m["total"])
                _start_quiz(qs, "exam_sim", m["name"], m["mins"]*60); st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Full Mocks + Season Mocks ──────────────────
    st.markdown('<div class="section-label">🎯 Full Mock Tests <span class="pill">50 Qs · 90 min</span></div>', unsafe_allow_html=True)
    full_mocks  = [m for m in MOCK_BLUEPRINTS if m["tag"] == "Full Mock"]
    f_cols = st.columns(2)
    for fi, m in enumerate(full_mocks):
        avail = qb.get_filtered(n=9999, shuffle=False)
        cnt = len(avail); used = min(m["total"], cnt); can = cnt > 0
        with f_cols[fi]:
            st.markdown(f"""<div class="card" style="border-color:rgba(99,102,241,0.3);">
              <div class="card-accent-top" style="background:var(--indigo);"></div>
              <div style="font-size:1.6rem;margin-bottom:0.4rem;">{m['icon']}</div>
              <div class="card-title">{m['name']}</div>
              <div class="card-desc">{m['desc']}</div>
              <div class="card-meta"><span class="chip">📝 {used} Qs</span><span class="chip">⏱ 90 min</span></div>
            </div>""", unsafe_allow_html=True)
            if st.button(f"▶ Start {m['name']}", key=f"mock_{m['id']}", use_container_width=True,
                         type="primary" if can else "secondary", disabled=not can):
                qs = qb.get_filtered(n=m["total"])
                _start_quiz(qs, "exam", m["name"], m["mins"]*60); st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Season Mocks ─────────────────────────────────
    st.markdown('<div class="section-label">📅 Season PYQ Mocks <span class="pill">15 Qs from real exams</span></div>', unsafe_allow_html=True)
    sea_mocks = [m for m in MOCK_BLUEPRINTS if m["tag"] == "Season Mock"]
    sm_cols = st.columns(2)
    for si2, m in enumerate(sea_mocks):
        avail = qb.get_filtered(seasons=m.get("seasons"), n=9999, shuffle=False)
        cnt = len(avail); used = min(m["total"], cnt); can = cnt > 0
        border_c = "rgba(232,160,32,0.4)" if "June" in m["name"] else "rgba(15,184,201,0.4)"
        with sm_cols[si2]:
            st.markdown(f"""<div class="card" style="border-color:{border_c};">
              <div style="font-size:1.6rem;margin-bottom:0.4rem;">{m['icon']}</div>
              <div class="card-title">{m['name']}</div>
              <div class="card-desc">{m['desc']} · {cnt} questions available</div>
              <div class="card-meta"><span class="chip">📝 {used} Qs</span><span class="chip amber">⏱ 18 min</span></div>
            </div>""", unsafe_allow_html=True)
            if st.button(f"▶ Start {m['name']}", key=f"mock_{m['id']}", use_container_width=True,
                         type="primary" if can else "secondary", disabled=not can):
                qs = qb.get_filtered(seasons=m.get("seasons"), n=m["total"])
                _start_quiz(qs, "exam", m["name"], m["mins"]*60); st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Custom Mock Builder ────────────────────────
    st.markdown('<div class="section-label">🔧 Custom Mock Builder <span class="pill">design your own test</span></div>', unsafe_allow_html=True)
    with st.expander("▸ Configure Custom Mock", expanded=False):
        r1c1, r1c2, r1c3 = st.columns(3)
        with r1c1: cy = st.multiselect("Year(s)",   qb.get_years(),   default=[], key="cb_years",   placeholder="All")
        with r1c2: cs = st.multiselect("Season(s)", qb.get_seasons(), default=[], key="cb_seasons", placeholder="All")
        with r1c3: ct = st.multiselect("Topic(s)",  qb.get_topics(),  default=[], key="cb_topics",  placeholder="All")
        r2c1, r2c2, r2c3 = st.columns(3)
        with r2c1: cn  = st.select_slider("Questions", [10,15,20,25,30,50], value=15, key="cb_n")
        with r2c2: cd  = st.selectbox("Difficulty", ["Mixed","Easy","Medium","Hard"], key="cb_diff")
        with r2c3: ct2 = st.select_slider("Time (min)", [10,15,18,20,30,45,60,90,120,180], value=18, key="cb_time")

        prev = qb.get_filtered(topics=ct or None, difficulty=cd, years=cy or None, seasons=cs or None, n=9999, shuffle=False)
        st.markdown(f'<div style="color:var(--indigo2);font-weight:700;font-size:0.84rem;margin-bottom:0.75rem;">✅ {len(prev)} match · {min(cn,len(prev))} will be used</div>', unsafe_allow_html=True)
        if st.button("🚀 Launch Custom Mock", key="cb_start", use_container_width=True, type="primary"):
            qs = qb.get_filtered(topics=ct or None, difficulty=cd, years=cy or None, seasons=cs or None, n=cn)
            if not qs: st.error("No questions found. Adjust filters.")
            else:
                _start_quiz(qs, "exam", f"Custom Mock ({cd})", ct2*60); st.rerun()


# ═══════════════════════════════════════════════
# AI PREDICTED QUESTIONS
# ═══════════════════════════════════════════════
def page_ai():
    qb = QuestionBank()

    st.markdown("""<div class="page-header">
      <h1>🤖 AI Predicted Questions</h1>
      <p>Curated by AI analysis of exam trends, NEP 2020 reforms, and topic frequency — targeted at upcoming UGC NET exams.</p>
    </div>""", unsafe_allow_html=True)

    ai_qs = [q for q in qb.get_all() if q.get("predicted")]
    reg_qs_total = len([q for q in qb.get_all() if not q.get("predicted")])

    # ── Stats banner ────────────────────────────────
    s1, s2, s3 = st.columns(3)
    with s1:
        st.markdown(f"""<div class="card" style="text-align:center;padding:1.1rem;border-color:rgba(15,184,201,0.35);border-top:3px solid var(--teal);">
          <div style="font-family:'Fira Code',monospace;font-size:1.8rem;font-weight:800;color:var(--teal2);">{len(ai_qs)}</div>
          <div style="font-size:0.68rem;color:var(--t3);text-transform:uppercase;margin-top:0.2rem;">AI Predictions</div>
        </div>""", unsafe_allow_html=True)
    with s2:
        st.markdown("""<div class="card" style="text-align:center;padding:1.1rem;border-color:rgba(232,160,32,0.35);border-top:3px solid var(--amber);">
          <div style="font-family:'Fira Code',monospace;font-size:1.8rem;font-weight:800;color:var(--amber2);">June 2025</div>
          <div style="font-size:0.68rem;color:var(--t3);text-transform:uppercase;margin-top:0.2rem;">Target Exam</div>
        </div>""", unsafe_allow_html=True)
    with s3:
        st.markdown("""<div class="card" style="text-align:center;padding:1.1rem;border-color:rgba(99,102,241,0.35);border-top:3px solid var(--indigo);">
          <div style="font-family:'Fira Code',monospace;font-size:1.8rem;font-weight:800;color:var(--indigo2);">NEP 2020</div>
          <div style="font-size:0.68rem;color:var(--t3);text-transform:uppercase;margin-top:0.2rem;">Aligned Reforms</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Action buttons ──────────────────────────────
    st.markdown('<div class="section-label">🚀 Practice Modes</div>', unsafe_allow_html=True)
    ac1, ac2, ac3 = st.columns(3)
    with ac1:
        st.markdown("""<div class="card" style="border-color:rgba(15,184,201,0.4);text-align:center;padding:1.2rem;">
          <div style="font-size:2rem;margin-bottom:0.5rem;">🤖</div>
          <div style="font-weight:700;color:var(--teal2);font-size:0.9rem;margin-bottom:0.3rem;">AI Questions Only</div>
          <div style="font-size:0.75rem;color:var(--t3);">Practice all AI-predicted questions · 18 min</div>
        </div>""", unsafe_allow_html=True)
        if st.button("▶ Start AI Practice", key="ai_all", use_container_width=True, type="primary"):
            if ai_qs: _start_quiz(ai_qs, "practice", "AI Predicted Questions", len(ai_qs)*90)
            else: st.error("No AI questions in bank yet.")
            st.rerun()
    with ac2:
        st.markdown("""<div class="card" style="border-color:rgba(99,102,241,0.4);text-align:center;padding:1.2rem;">
          <div style="font-size:2rem;margin-bottom:0.5rem;">🔀</div>
          <div style="font-weight:700;color:var(--indigo2);font-size:0.9rem;margin-bottom:0.3rem;">AI + PYQ Mix</div>
          <div style="font-size:0.75rem;color:var(--t3);">AI picks blended with real PYQs · 20 Qs</div>
        </div>""", unsafe_allow_html=True)
        if st.button("▶ Start Mix Mock", key="ai_mock", use_container_width=True):
            reg = qb.get_filtered(n=15, shuffle=True)
            mixed = (ai_qs + reg)[:20]; random.shuffle(mixed)
            _start_quiz(mixed, "exam", "AI + PYQ Mix Mock", 20*90); st.rerun()
    with ac3:
        st.markdown("""<div class="card" style="border-color:rgba(232,160,32,0.4);text-align:center;padding:1.2rem;">
          <div style="font-size:2rem;margin-bottom:0.5rem;">🎯</div>
          <div style="font-weight:700;color:var(--amber2);font-size:0.9rem;margin-bottom:0.3rem;">15-Q AI Mock</div>
          <div style="font-size:0.75rem;color:var(--t3);">AI picks · 15 Qs · 30 min timed sprint</div>
        </div>""", unsafe_allow_html=True)
        if st.button("▶ Start 15-Q AI Mock", key="ai_15", use_container_width=True):
            qs15 = ai_qs[:] ; random.shuffle(qs15)
            if not qs15: qs15 = qb.get_filtered(n=15)
            _start_quiz(qs15[:15], "exam", "AI 15-Q Mock", 30*60); st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── AI questions preview list ────────────────────
    st.markdown('<div class="section-label">🔍 AI-Predicted Questions Preview</div>', unsafe_allow_html=True)
    diff_colors = {"Easy":"var(--emerald)","Medium":"var(--amber)","Hard":"var(--rose)"}
    topic_icons = {"Teaching Aptitude":"🧠","Research Aptitude":"🔬","ICT":"💻","Environment & Ecology":"🌿",
                   "Higher Education":"🎓","Communication":"📡","Reasoning":"🧩","Data Interpretation":"📊",
                   "Indian Constitution & Governance":"⚖️","Reading Comprehension":"📖"}
    for qi, q in enumerate(ai_qs):
        dc = diff_colors.get(q.get("difficulty",""), "var(--t2)")
        icon = topic_icons.get(q.get("topic",""), "📌")
        st.markdown(f"""<div class="card" style="margin-bottom:0.5rem;border-color:rgba(15,184,201,0.2);">
          <div class="card-meta" style="margin-bottom:0.5rem;">
            <span class="chip teal">{icon} {q.get('topic','—')}</span>
            <span class="chip" style="color:{dc};">{q.get('difficulty','—')}</span>
            
            <span style="font-size:0.65rem;color:var(--t3);margin-left:auto;">Target: {q.get('year','')} {q.get('season','')}</span>
          </div>
          <div style="font-family:'Playfair Display',serif;font-weight:700;color:var(--t1);font-size:0.93rem;line-height:1.7;">{q['question']}</div>
        </div>""", unsafe_allow_html=True)



# ═══════════════════════════════════════════════
# QUIZ ENGINE (shared by all modes)
# ═══════════════════════════════════════════════
def _start_quiz(questions, mode, label, total_time_secs):
    random.shuffle(questions)
    st.session_state.update({
        "questions": questions, "q_idx": 0, "answers": {},
        "quiz_active": True, "quiz_done": False,
        "quiz_mode": mode, "quiz_label": label,
        "start_time": time.time(), "q_start": time.time(),
        "total_time": total_time_secs,
        "q_times": {},
        "page": "quiz",
    })

# ── Timer fragment: reruns every 1s independently, never blocks buttons ──
@st.fragment(run_every=1)
def _timer_fragment(remaining, tl, label, idx, total):
    """Isolated fragment that only updates the header/timer row."""
    if remaining is None:
        st.markdown(
            f'<div style="display:flex;align-items:center;justify-content:space-between;'
            f'flex-wrap:wrap;gap:0.5rem;margin-bottom:0.5rem;">'
            f'<div style="font-size:0.8rem;color:var(--t2);font-weight:600;">📝 {label}</div>'
            f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:1rem;font-weight:700;'
            f'color:var(--cyan);background:rgba(34,211,238,0.1);border:1px solid rgba(34,211,238,0.35);'
            f'border-radius:8px;padding:0.35rem 0.85rem;">⏱ Free</div>'
            f'<div style="font-size:0.8rem;color:var(--t2);font-family:\'JetBrains Mono\',monospace;">'
            f'{idx+1}/{total}</div></div>',
            unsafe_allow_html=True
        )
        return

    # Recalculate from session state so it's always accurate
    elapsed   = int(time.time() - st.session_state.start_time)
    remaining = max(0, tl - elapsed)
    rm, rs    = divmod(remaining, 60)
    pct       = remaining / tl if tl > 0 else 1.0

    if pct > 0.4:    cls, color = "timer-ok",   "var(--cyan)"
    elif pct > 0.15: cls, color = "timer-warn",  "var(--gold)"
    else:            cls, color = "timer-crit",  "var(--red)"

    progress_pct = (st.session_state.q_idx / total * 100) if total > 0 else 0

    st.markdown(
        f'<div class="progress-track">'
        f'<div class="progress-fill" style="width:{progress_pct:.1f}%"></div></div>'
        f'<div style="display:flex;align-items:center;justify-content:space-between;'
        f'flex-wrap:wrap;gap:0.5rem;margin-bottom:0.75rem;">'
        f'<div style="font-size:0.8rem;color:var(--t2);font-weight:600;">📝 {label}</div>'
        f'<div class="timer-display {cls}">⏱ {rm:02d}:{rs:02d}</div>'
        f'<div style="font-size:0.8rem;color:var(--t2);font-family:\'JetBrains Mono\',monospace;">'
        f'{idx+1}/{total}</div></div>',
        unsafe_allow_html=True
    )

    # Auto-submit when time is up
    if remaining == 0:
        st.session_state.quiz_done = True
        st.session_state.score = sum(
            1 for a in st.session_state.answers.values() if a.get("correct")
        )
        st.rerun()


def page_quiz():
    if st.session_state.quiz_done:
        page_results()
        return
    if not st.session_state.quiz_active:
        page_quiz_config()
        return

    questions = st.session_state.questions
    idx       = st.session_state.q_idx
    total     = len(questions)
    mode      = st.session_state.quiz_mode
    label     = st.session_state.quiz_label

    if idx >= total:
        st.session_state.quiz_done = True
        st.session_state.score = sum(1 for a in st.session_state.answers.values() if a.get("correct"))
        st.rerun()
        return

    q      = questions[idx]
    tl     = st.session_state.total_time
    elapsed = int(time.time() - st.session_state.start_time)
    remaining = max(0, tl - elapsed) if tl > 0 else None

    # Auto-submit on expiry
    if remaining == 0 and tl > 0:
        st.session_state.quiz_done = True
        st.session_state.score = sum(1 for a in st.session_state.answers.values() if a.get("correct"))
        st.rerun()
        return

    # For exam_sim we compute rm/rs for the big header
    rm, rs = divmod(remaining or 0, 60)
    diff_color = {"Easy":"var(--green)","Medium":"var(--gold)","Hard":"var(--red)"}.get(q.get("difficulty",""),"var(--text2)")
    yr_tag = f'· {q.get("year","")} {q.get("season","")}' if q.get("year") else ""
    ai_tag = ""  # AI tag removed from display
    is_exam_sim = (mode == "exam_sim")

    # Layout
    if mode in ("exam", "exam_sim"):
        col_q, col_nav = st.columns([3, 1])
    else:
        col_q = col_nav = None

    def _render_body():
        # ── Header / Timer ──
        if is_exam_sim:
            # Big exam-sim header with static timer (fragment handles tick separately)
            timer_color = "var(--red)" if (remaining is not None and remaining < 600) else \
                          ("var(--gold)" if (remaining is not None and remaining < 1800) else "var(--cyan)")
            st.markdown(f"""<div style="background:rgba(10,14,22,0.95);border:1px solid rgba(124,58,237,0.4);
                border-radius:12px;padding:0.75rem 1.25rem;display:flex;align-items:center;
                justify-content:space-between;margin-bottom:1rem;gap:1rem;flex-wrap:wrap;">
              <div style="display:flex;align-items:center;gap:0.5rem;">
                <span style="font-size:1.1rem;">🎓</span>
                <span style="font-weight:700;font-size:0.88rem;color:var(--violet2);">{label}</span>
              </div>
              <div style="font-family:'JetBrains Mono',monospace;font-size:1.6rem;font-weight:700;
                  color:{timer_color};letter-spacing:0.05em;">
                ⏱ {rm:02d}:{rs:02d}
              </div>
              <div style="font-size:0.82rem;color:var(--t2);">Q {idx+1} / {total}</div>
            </div>""", unsafe_allow_html=True)
            # Fragment handles live tick for exam_sim too
            _timer_fragment(remaining, tl, label, idx, total)
        else:
            # Live-ticking timer fragment (1s updates, non-blocking)
            _timer_fragment(remaining, tl, label, idx, total)

        # ── Question card ──
        clean_q = html.unescape(re.sub(r'<[^>]+>', '', q["question"])).strip()
        st.markdown(f"""<div class="question-wrap">
          <div class="q-num">QUESTION {idx+1} OF {total}</div>
          <div class="q-text">{clean_q}</div>
          <div class="q-tags">
            <span class="meta-chip" style="color:{diff_color}">{q.get("difficulty","")}</span>
            <span class="meta-chip violet">{q.get("topic","")}</span>
            <span class="meta-chip">{yr_tag}</span>
          </div>
        </div>""", unsafe_allow_html=True)

        # ── Options ──
        options = q.get("options", [])
        correct = q.get("correct_answer", "")
        already = idx in st.session_state.answers
        sel_key = f"sel_{idx}"
        if sel_key not in st.session_state:
            st.session_state[sel_key] = options[0] if options else ""

        if already:
            user_ans = st.session_state.answers[idx].get("answer")
            for opt in options:
                clean = html.unescape(re.sub(r'<[^>]+>', '', opt)).strip()
                if opt == correct:
                    st.markdown(f'<div class="option-btn correct-opt">✅ {clean}</div>', unsafe_allow_html=True)
                elif opt == user_ans and opt != correct:
                    st.markdown(f'<div class="option-btn wrong-opt">❌ {clean}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="option-btn neutral-opt">{clean}</div>', unsafe_allow_html=True)

            # ── Answer feedback effects ──────────────────────────────
            if st.session_state.pop("_show_correct_fx", None) == idx:
                st.balloons()
                st.markdown("""
                <div style="text-align:center;padding:0.75rem 0;animation:popIn 0.4s ease;">
                  <span style="font-size:3.5rem;filter:drop-shadow(0 0 12px #22c55e);">🎉</span>
                  <div style="font-family:'DM Sans',sans-serif;font-size:1.1rem;font-weight:700;
                    color:#22c55e;margin-top:0.25rem;letter-spacing:0.03em;">Brilliant! Correct Answer!</div>
                  <div style="font-size:0.8rem;color:var(--t2);margin-top:0.2rem;">Keep going! 🚀</div>
                </div>
                <style>@keyframes popIn{from{transform:scale(0.5);opacity:0}to{transform:scale(1);opacity:1}}</style>
                """, unsafe_allow_html=True)
            elif st.session_state.pop("_show_wrong_fx", None) == idx:
                st.markdown("""
                <div style="text-align:center;padding:0.75rem 0;animation:shakeIt 0.5s ease;">
                  <span style="font-size:3.5rem;filter:drop-shadow(0 0 12px #f43f5e);">😢</span>
                  <div style="font-family:'DM Sans',sans-serif;font-size:1.1rem;font-weight:700;
                    color:#f43f5e;margin-top:0.25rem;">Oops! That was wrong</div>
                  <div style="font-size:0.8rem;color:var(--t2);margin-top:0.2rem;">Check the explanation below 👇</div>
                </div>
                <style>
                  @keyframes shakeIt{0%,100%{transform:translateX(0)}20%{transform:translateX(-8px)}
                  40%{transform:translateX(8px)}60%{transform:translateX(-5px)}80%{transform:translateX(5px)}}
                </style>
                """, unsafe_allow_html=True)

            if q.get("explanation") and mode not in ("exam", "exam_sim"):
                clean_exp = html.unescape(re.sub(r'<[^>]+>', '', q["explanation"])).strip()
                st.markdown(
                    f'<div class="explanation-box"><div class="exp-title">💡 Explanation</div>'
                    f'<div class="exp-text">{clean_exp}</div></div>',
                    unsafe_allow_html=True
                )

            nc1, nc2, nc3 = st.columns([1, 1, 1])
            with nc1:
                if idx > 0 and st.button("← Prev", key=f"prev_{idx}", use_container_width=True):
                    st.session_state.q_idx -= 1; st.rerun()
            with nc2:
                bm_id    = q.get("id", idx)
                bm_label = "🔖 Saved" if bm_id in st.session_state.bookmarks else "🔖 Save"
                if st.button(bm_label, key=f"bm_{idx}", use_container_width=True):
                    if bm_id in st.session_state.bookmarks:
                        st.session_state.bookmarks.discard(bm_id)
                    else:
                        st.session_state.bookmarks.add(bm_id)
                    st.rerun()
            with nc3:
                if idx < total - 1:
                    if st.button("Next →", key=f"next_{idx}", use_container_width=True, type="primary"):
                        st.session_state.q_idx += 1
                        st.session_state.q_start = time.time()
                        st.rerun()
                else:
                    if st.button("🏁 Finish", key=f"finish_{idx}", use_container_width=True, type="primary"):
                        st.session_state.quiz_done = True
                        st.session_state.score = sum(1 for a in st.session_state.answers.values() if a.get("correct"))
                        st.rerun()

        else:
            # Pre-answer: pure buttons — no duplicate HTML
            clean_opts = [html.unescape(re.sub(r'<[^>]+>', '', o)).strip() for o in options]
            for i_o, (opt, clean) in enumerate(zip(options, clean_opts)):
                if st.session_state[sel_key] == opt:
                    st.markdown(
                        f'<div class="opt-selected">'
                        f'<span class="opt-dot-sel">●</span>&nbsp;&nbsp;{clean}'
                        f'</div>',
                        unsafe_allow_html=True
                    )
                else:
                    if st.button(f"○  {clean}", key=f"opt_{idx}_{i_o}", use_container_width=True):
                        st.session_state[sel_key] = opt
                        st.rerun()

            st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
            # Submit — full width for easy tapping on mobile
            if st.button("✅  Submit Answer", key=f"sub_{idx}", use_container_width=True, type="primary"):
                choice       = st.session_state[sel_key]
                correct_flag = (choice == correct)
                t_taken      = int(time.time() - (st.session_state.q_start or time.time()))
                st.session_state.answers[idx] = {"answer": choice, "correct": correct_flag, "time": t_taken}
                st.session_state.q_times[idx]  = t_taken
                st.session_state.total_attempted += 1
                if correct_flag:
                    st.session_state.total_correct += 1
                    st.session_state.streak += 1
                    st.session_state["_show_correct_fx"] = idx
                else:
                    st.session_state.streak = 0
                    st.session_state["_show_wrong_fx"] = idx
                    if q not in st.session_state.wrong_questions:
                        st.session_state.wrong_questions.append(q)
                if mode in ("exam", "exam_sim"):
                    st.session_state.q_idx += 1
                    st.session_state.q_start = time.time()
                st.rerun()
            # Skip + Bookmark in 2-col row — large tap targets
            _sb1, _sb2 = st.columns(2)
            with _sb1:
                if st.button("⏭  Skip", key=f"skip_{idx}", use_container_width=True):
                    st.session_state.answers[idx] = {"answer": None, "correct": False, "skipped": True}
                    st.session_state.q_idx += 1
                    st.session_state.q_start = time.time()
                    st.rerun()
            with _sb2:
                bm_id2   = q.get("id", idx)
                bm_lbl2  = "🔖 Saved" if bm_id2 in st.session_state.bookmarks else "🔖 Save"
                if st.button(bm_lbl2, key=f"bm2_{idx}", use_container_width=True):
                    if bm_id2 in st.session_state.bookmarks:
                        st.session_state.bookmarks.discard(bm_id2)
                    else:
                        st.session_state.bookmarks.add(bm_id2)
                    st.rerun()

    # Render in correct container
    if col_q is not None:
        with col_q:
            _render_body()
    else:
        _render_body()

    # ── Exam navigator panel (CLICKABLE) ─────────────────────────────
    if mode in ("exam", "exam_sim") and col_nav is not None:
        with col_nav:
            answered_count = sum(1 for a in st.session_state.answers.values() if not a.get("skipped"))

            st.markdown('<div class="exam-panel-title">QUESTION NAVIGATOR</div>', unsafe_allow_html=True)

            # Navigator button CSS
            st.markdown("""<style>
            .nav-btn-grid {display:grid;grid-template-columns:repeat(7,1fr);gap:3px;margin-bottom:0.5rem;}
            .nav-btn {border:1px solid rgba(255,255,255,0.15);border-radius:6px;text-align:center;
                      padding:5px 2px;font-size:0.72rem;font-weight:600;cursor:pointer;
                      background:rgba(255,255,255,0.05);color:var(--t1);line-height:1;}
            .nav-btn.current  {background:var(--violet)!important;border-color:var(--violet)!important;
                               color:#fff!important;box-shadow:0 0 8px rgba(139,92,246,0.6);}
            .nav-btn.answered {background:var(--green)!important;border-color:var(--green)!important;color:#000!important;}
            .nav-btn.skipped  {background:var(--gold)!important;border-color:var(--gold)!important;color:#000!important;}
            </style>""", unsafe_allow_html=True)

            # Render color indicator row (visual only)
            nav_html = '<div class="nav-btn-grid">'
            for qi in range(total):
                if qi == idx:            cls = "nav-btn current"
                elif qi in st.session_state.answers:
                    cls = "nav-btn answered" if not st.session_state.answers[qi].get("skipped") else "nav-btn skipped"
                else:                    cls = "nav-btn"
                nav_html += f'<div class="{cls}">{qi+1}</div>'
            nav_html += '</div>'
            st.markdown(nav_html, unsafe_allow_html=True)

            # Clickable jump buttons — compact rows of 7
            cols_per_row = 7
            for row_start in range(0, total, cols_per_row):
                row_qs = list(range(row_start, min(row_start + cols_per_row, total)))
                btn_cols = st.columns(len(row_qs))
                for bi, qi in enumerate(row_qs):
                    with btn_cols[bi]:
                        btn_label = str(qi + 1)
                        if st.button(btn_label, key=f"nav_q_{qi}",
                                     use_container_width=True,
                                     help=f"Jump to Question {qi+1}"):
                            st.session_state.quiz_idx = qi
                            st.rerun()

            # Legend + stats
            st.markdown(f"""
            <div style="margin-top:0.5rem;display:flex;gap:0.75rem;flex-wrap:wrap;font-size:0.7rem;color:var(--t2);">
              <span><span style="display:inline-block;width:9px;height:9px;border-radius:50%;
                background:var(--violet);margin-right:3px;vertical-align:middle;"></span>Now</span>
              <span><span style="display:inline-block;width:9px;height:9px;border-radius:50%;
                background:var(--green);margin-right:3px;vertical-align:middle;"></span>Done</span>
              <span><span style="display:inline-block;width:9px;height:9px;border-radius:50%;
                background:var(--gold);margin-right:3px;vertical-align:middle;"></span>Skip</span>
            </div>
            <div style="margin-top:0.35rem;font-size:0.78rem;color:var(--t2);">
              Answered: <b style="color:var(--green);">{answered_count}</b> / {total}
            </div>""", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🏁 Submit Exam", key="exam_submit", use_container_width=True, type="primary"):
                st.session_state.quiz_done = True
                st.session_state.score = sum(1 for a in st.session_state.answers.values() if a.get("correct"))
                st.rerun()


def page_quiz_config():
    qb = QuestionBank()
    st.markdown('<h2 style="font-family:Syne,sans-serif;font-size:1.5rem;font-weight:800;margin-bottom:1rem;">📝 Configure Practice Session</h2>', unsafe_allow_html=True)

    cc1, cc2 = st.columns([2,1])
    with cc1:
        st.markdown("**📚 Select Topics**")
        selected = []
        tc = st.columns(2)
        for i, topic in enumerate(qb.get_topics()):
            with tc[i%2]:
                if st.checkbox(topic, value=True, key=f"cfg_{topic}"): selected.append(topic)

    with cc2:
        diff   = st.radio("Difficulty", ["Mixed","Easy","Medium","Hard"], horizontal=True)
        n      = st.select_slider("Questions", [10,15,20,25,30,50], value=15)
        pm     = st.radio("Mode", ["Practice","Exam"], captions=["Show answers after each Q","Full simulation"])
        timed  = st.toggle("Timer", value=True)
        t_secs = n * 120 if timed else 0
        # Year/season filter
        sy = st.multiselect("Year(s)", qb.get_years(), default=[], placeholder="All", key="cfg_yr")
        ss = st.multiselect("Season(s)", qb.get_seasons(), default=[], placeholder="All", key="cfg_ss")

    prev = qb.get_filtered(topics=selected or None, difficulty=diff, years=sy or None, seasons=ss or None, n=9999, shuffle=False)
    st.markdown(f'<p style="color:var(--violet2);font-weight:700;font-size:0.85rem;">✅ {len(prev)} match · {min(n,len(prev))} will be used</p>', unsafe_allow_html=True)

    if st.button("🚀 Start Session", use_container_width=True, type="primary"):
        if not selected: st.error("Select at least one topic."); return
        qs = qb.get_filtered(topics=selected, difficulty=diff, years=sy or None, seasons=ss or None, n=n)
        _start_quiz(qs, pm.lower(), f"Practice ({diff})", t_secs)
        st.rerun()


# ═══════════════════════════════════════════════
# RESULTS
# ═══════════════════════════════════════════════
def get_grade(pct):
    if pct >= 90: return "A+", "var(--emerald)", "Outstanding! 🏆"
    if pct >= 75: return "A",  "var(--emerald)", "Excellent! 🎉"
    if pct >= 60: return "B+", "var(--teal2)",   "Good work! 👍"
    if pct >= 50: return "B",  "var(--amber)",   "Keep practicing 💪"
    if pct >= 35: return "C",  "var(--amber)",   "Need more revision 📖"
    return "D", "var(--rose)", "Don't give up! 🔥"

def page_results():
    score   = st.session_state.get("score", 0)
    total   = len(st.session_state.questions)
    pct     = round(score/total*100) if total else 0
    elapsed = int(time.time() - (st.session_state.start_time or time.time()))
    em, es  = divmod(elapsed, 60)
    grade, gc, gm = get_grade(pct)
    label   = st.session_state.quiz_label

    user = st.session_state.user
    if user and st.session_state.quiz_mode in ("exam", "exam_sim", "practice"):
        save_score(st.session_state.username, user["name"], score, total, pct,
                   st.session_state.quiz_mode, elapsed)

    wrong   = sum(1 for a in st.session_state.answers.values() if not a.get("correct") and not a.get("skipped"))
    skipped = sum(1 for a in st.session_state.answers.values() if a.get("skipped"))
    avg_t   = round(sum(st.session_state.q_times.values())/len(st.session_state.q_times)) if st.session_state.q_times else 0

    st.markdown(f"""<div class="result-hero">
      <div style="font-size:0.8rem;color:var(--t2);margin-bottom:0.75rem;font-weight:600;letter-spacing:0.05em;text-transform:uppercase;">📝 {label}</div>
      <span class="grade-letter" style="color:{gc};">{grade}</span>
      <div class="result-score">{score} / {total}</div>
      <div class="result-pct">{pct}% Accuracy</div>
      <div class="result-msg">{gm}</div>
    </div>""", unsafe_allow_html=True)

    stat_cols = st.columns(5)
    for col, val, lbl, c in [
        (stat_cols[0], score,         "Correct", "var(--emerald)"),
        (stat_cols[1], wrong,         "Wrong",   "var(--rose)"),
        (stat_cols[2], skipped,       "Skipped", "var(--amber)"),
        (stat_cols[3], f"{em}m{es}s", "Time",    "var(--indigo2)"),
        (stat_cols[4], f"{avg_t}s",   "Avg / Q", "var(--teal2)"),
    ]:
        with col:
            st.markdown(f"""<div class="stat-card-mini" style="border-top-color:{c};">
              <span class="val" style="color:{c};">{val}</span>
              <span class="lbl">{lbl}</span>
            </div>""", unsafe_allow_html=True)

    if user:
        lb = get_leaderboard(mode=st.session_state.quiz_mode)
        my_rank = next((i+1 for i,r in enumerate(lb) if r["username"]==st.session_state.username), None)
        if my_rank:
            st.markdown(f"""<div style="text-align:center;margin:1.5rem 0;padding:1rem;background:var(--amber-glow);border:1px solid rgba(232,160,32,0.3);border-radius:var(--r-md);">
              <span style="font-family:'Playfair Display',serif;font-size:1.1rem;font-weight:800;color:var(--amber);">🏆 Your Rank: #{my_rank} out of {len(lb)}</span>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    rc1, rc2, rc3, rc4 = st.columns(4)
    with rc1:
        if st.button("🔄 Retry",       use_container_width=True, type="primary"):
            st.session_state.quiz_active=False; st.session_state.quiz_done=False; st.rerun()
    with rc2:
        if st.button("📊 Analytics",   use_container_width=True):
            st.session_state.page="analytics"; st.session_state.quiz_active=False; st.session_state.quiz_done=False; st.rerun()
    with rc3:
        if st.button("🏆 Leaderboard", use_container_width=True):
            st.session_state.page="leaderboard"; st.session_state.quiz_active=False; st.session_state.quiz_done=False; st.rerun()
    with rc4:
        if st.button("🏛️ Home",        use_container_width=True):
            st.session_state.page="home"; st.session_state.quiz_active=False; st.session_state.quiz_done=False; st.rerun()


# ═══════════════════════════════════════════════
# LEADERBOARD
# ═══════════════════════════════════════════════
def page_leaderboard():
    st.markdown('<h2 style="font-family:Syne,sans-serif;font-size:1.5rem;font-weight:800;margin-bottom:0.5rem;">🏆 Leaderboard</h2>', unsafe_allow_html=True)

    lc1, lc2, lc3 = st.columns([2,1,1])
    with lc1:
        mode_filter = st.selectbox("Filter by mode", ["All","exam_sim","exam","practice"], key="lb_mode",
                                   format_func=lambda x: {"All":"All Modes","exam_sim":"🎓 Exam Simulation","exam":"🧪 Mock Test","practice":"📝 Practice"}.get(x,x))
    with lc2:
        n_show = st.select_slider("Show", [10,20,50], value=20, key="lb_n")
    with lc3:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()

    lb = get_leaderboard(mode=mode_filter if mode_filter != "All" else None, limit=n_show)

    # Show current user's rank
    if st.session_state.username:
        lb_all = get_leaderboard(mode=mode_filter if mode_filter != "All" else None, limit=200)
        my_rank = next((i+1 for i,r in enumerate(lb_all) if r["username"]==st.session_state.username), None)
        total_students = len(lb_all)
        if my_rank:
            pct_rank = round((total_students - my_rank + 1)/total_students*100) if total_students else 0
            st.markdown(f"""<div style="background:var(--indigo-glow);border:1px solid rgba(99,102,241,0.35);border-radius:var(--r-md);
                padding:0.85rem 1.25rem;margin-bottom:1rem;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:0.5rem;">
              <span style="font-size:0.9rem;color:var(--t2);">📍 Your Standing</span>
              <span style="font-family:'Fira Code',monospace;font-weight:800;font-size:1.05rem;color:var(--indigo2);">
                Rank #{my_rank} of {total_students} students · Top {pct_rank}%
              </span>
            </div>""", unsafe_allow_html=True)

    medals = ["🥇","🥈","🥉"]
    rank_colors = ["gold","silver","bronze"]

    if not lb:
        st.markdown('<div style="text-align:center;padding:3rem;color:var(--text3);">No scores recorded yet. Complete a quiz to appear here!</div>', unsafe_allow_html=True)
        return

    # Top 3 podium
    if len(lb) >= 3:
        p2, p1, p3 = st.columns([1,1.2,1])
        for col, row, i, height in [(p2,lb[1],1,"7rem"),(p1,lb[0],0,"9rem"),(p3,lb[2],2,"6rem")]:
            with col:
                initials = "".join(w[0].upper() for w in row["name"].split()[:2])
                is_me = row["username"] == st.session_state.username
                st.markdown(f"""<div style="text-align:center;background:var(--card);border:1px solid var(--border2);
                  border-radius:var(--rl);padding:1.2rem 0.75rem;margin-bottom:0.5rem;">
                  <div style="font-size:1.6rem;">{medals[i]}</div>
                  <div style="width:2.8rem;height:2.8rem;border-radius:50%;background:linear-gradient(135deg,var(--violet),var(--cyan));
                    display:flex;align-items:center;justify-content:center;font-weight:800;color:#fff;margin:0.4rem auto;">
                    {initials}</div>
                  <div style="font-weight:700;font-size:0.85rem;color:var(--text);">{row["name"]} {"⭐" if is_me else ""}</div>
                  <div style="font-family:JetBrains Mono,monospace;font-weight:800;font-size:1.1rem;color:var(--gold);">{row["pct"]}%</div>
                  <div style="font-size:0.7rem;color:var(--text3);">{row["score"]}/{row["total"]}</div>
                </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    for i, row in enumerate(lb):
        is_me = row["username"] == st.session_state.username
        me_cls = "lb-row me" if is_me else "lb-row"
        rank_cls = rank_colors[i] if i < 3 else "rest"
        medal = medals[i] if i < 3 else str(i+1)
        initials = "".join(w[0].upper() for w in row["name"].split()[:2])
        ts = datetime.fromisoformat(row["ts"]).strftime("%d %b %Y") if row.get("ts") else ""
        st.markdown(f"""<div class="{me_cls}">
          <div class="lb-rank {rank_cls}">{medal}</div>
          <div class="lb-avatar">{initials}</div>
          <div style="flex:1">
            <div class="lb-name">{row["name"]} {"⭐ You" if is_me else ""}</div>
            <div class="lb-detail">{row.get("mode","—")} · {ts}</div>
          </div>
          <div style="text-align:right;">
            <div class="lb-score">{row["pct"]}%</div>
            <div style="font-size:0.7rem;color:var(--text3);">{row["score"]}/{row["total"]}</div>
          </div>
        </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════
# ANALYTICS
# ═══════════════════════════════════════════════
def page_analytics():
    st.markdown('<h2 style="font-family:Syne,sans-serif;font-size:1.5rem;font-weight:800;margin-bottom:1rem;">📊 Your Analytics</h2>', unsafe_allow_html=True)

    attempted = st.session_state.total_attempted
    correct   = st.session_state.total_correct
    accuracy  = round(correct/attempted*100) if attempted else 0
    streak    = st.session_state.streak
    bookmarks = len(st.session_state.bookmarks)
    wrong_cnt = len(st.session_state.wrong_questions)

    c1,c2,c3,c4,c5,c6 = st.columns(6)
    for col,val,lbl,c in [
        (c1,attempted,"Attempted","#7c5cfc"),(c2,correct,"Correct","#00e5a0"),
        (c3,f"{accuracy}%","Accuracy","#00d4ff"),(c4,streak,"Streak 🔥","#f5a623"),
        (c5,bookmarks,"Bookmarks","#a78bfa"),(c6,wrong_cnt,"For Review","#ff4d6d"),
    ]:
        with col:
            st.markdown(f'<div class="card" style="text-align:center;padding:1rem;border-top:3px solid {c}"><div style="font-family:JetBrains Mono,monospace;font-size:1.6rem;font-weight:800;color:{c};">{val}</div><div style="font-size:0.68rem;color:var(--text3);text-transform:uppercase;margin-top:0.2rem;">{lbl}</div></div>', unsafe_allow_html=True)

    # Topic performance
    answers   = st.session_state.answers
    questions = st.session_state.questions
    if answers and questions:
        st.markdown('<div class="section-label">Topic Performance</div>', unsafe_allow_html=True)
        topic_stats = {}
        for qi, ans in answers.items():
            if qi < len(questions):
                t = questions[qi].get("topic","General")
                if t not in topic_stats: topic_stats[t] = {"correct":0,"total":0}
                topic_stats[t]["total"] += 1
                if ans.get("correct"): topic_stats[t]["correct"] += 1
        for topic, stats in sorted(topic_stats.items()):
            pct = round(stats["correct"]/stats["total"]*100) if stats["total"] else 0
            bar_c = "#00e5a0" if pct>=70 else ("#f5a623" if pct>=50 else "#ff4d6d")
            st.markdown(f"""<div style="background:var(--card);border:1px solid var(--border);border-radius:10px;padding:0.75rem 1rem;margin-bottom:0.4rem;">
              <div style="display:flex;justify-content:space-between;margin-bottom:0.4rem;">
                <span style="font-weight:600;font-size:0.85rem;">{topic}</span>
                <span style="font-family:JetBrains Mono,monospace;font-size:0.85rem;color:{bar_c};">{pct}% ({stats["correct"]}/{stats["total"]})</span>
              </div>
              <div style="background:var(--border);height:5px;border-radius:3px;">
                <div style="background:{bar_c};height:100%;width:{pct}%;border-radius:3px;transition:width 0.5s;"></div>
              </div>
            </div>""", unsafe_allow_html=True)

    # Wrong questions for review
    if st.session_state.wrong_questions:
        st.markdown('<div class="section-label">❌ Questions for Review</div>', unsafe_allow_html=True)
        if st.button("🔄 Practice Wrong Questions", use_container_width=True, type="primary"):
            qs = st.session_state.wrong_questions[:20]
            _start_quiz(qs, "practice", "Wrong Q Review", len(qs)*90)
            st.rerun()


# ═══════════════════════════════════════════════
# BOOKMARKS
# ═══════════════════════════════════════════════
def page_bookmarks():
    st.markdown('<h2 style="font-family:Syne,sans-serif;font-size:1.5rem;font-weight:800;margin-bottom:0.5rem;">🔖 Bookmarks</h2>', unsafe_allow_html=True)
    bms = st.session_state.bookmarks
    if not bms:
        st.markdown('<div style="text-align:center;padding:3rem;color:var(--text3);">No bookmarks yet. Click 🔖 during a quiz to save questions.</div>', unsafe_allow_html=True)
        return
    qb = QuestionBank()
    all_q = {q.get("id"): q for q in qb.get_all()}
    bm_questions = [all_q[bid] for bid in bms if bid in all_q]
    st.markdown(f'<p style="color:var(--text2);font-size:0.85rem;margin-bottom:1rem;">{len(bm_questions)} saved questions</p>', unsafe_allow_html=True)
    if bm_questions and st.button("🚀 Practice Bookmarks", use_container_width=True, type="primary"):
        _start_quiz(bm_questions, "practice", "Bookmarked Questions", len(bm_questions)*90)
        st.rerun()
    for q in bm_questions:
        st.markdown(f"""<div class="card" style="margin-bottom:0.5rem;">
          <div class="card-meta"><span class="meta-chip violet">{q.get("topic","")}</span>
          <span class="meta-chip">{q.get("difficulty","")}</span>
          <span class="meta-chip">{q.get("year","")} {q.get("season","")}</span></div>
          <div style="font-weight:600;font-size:0.88rem;margin-top:0.5rem;color:var(--text);line-height:1.6;">{q["question"][:200]}</div>
          <div style="font-size:0.8rem;color:var(--green);margin-top:0.3rem;">✅ {q.get("correct_answer","")}</div>
        </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════
# LOGIN / REGISTER
# ═══════════════════════════════════════════════
def page_login():
    user = st.session_state.user
    uname = st.session_state.username or ""

    # ── If already logged in, show profile card ──
    if user:
        scores = load_scores()
        my_scores = [s for s in scores if s.get("username")==uname]
        attempts  = len(my_scores)
        best_pct  = max((s["pct"] for s in my_scores), default=0)
        avg_pct   = round(sum(s["pct"] for s in my_scores)/attempts) if attempts else 0
        lb_all    = get_leaderboard(limit=200)
        my_rank   = next((i+1 for i,r in enumerate(lb_all) if r["username"]==uname), None)
        initials  = "".join(w[0].upper() for w in user["name"].split()[:2])

        st.markdown(f"""<div class="page-header">
          <h1>👤 My Profile</h1>
        </div>""", unsafe_allow_html=True)

        st.markdown(f"""<div class="card" style="border-color:rgba(99,102,241,0.4);margin-bottom:1.5rem;">
          <div class="card-accent-top" style="background:linear-gradient(90deg,var(--indigo),var(--teal));"></div>
          <div style="display:flex;align-items:center;gap:1.5rem;flex-wrap:wrap;">
            <div style="width:4rem;height:4rem;border-radius:50%;background:linear-gradient(135deg,var(--indigo),var(--teal));
              display:flex;align-items:center;justify-content:center;font-weight:800;font-size:1.4rem;color:#fff;flex-shrink:0;">
              {initials}
            </div>
            <div style="flex:1;">
              <div style="font-family:'Playfair Display',serif;font-weight:800;font-size:1.2rem;color:var(--t1);">{user["name"]}</div>
              <div style="color:var(--t3);font-size:0.8rem;">@{uname} · Joined {user.get("joined","—")}</div>
            </div>
            {f'<div style="font-family:Fira Code,monospace;font-size:1.5rem;font-weight:800;color:var(--amber);">🏆 #{my_rank}</div>' if my_rank else ""}
          </div>
        </div>""", unsafe_allow_html=True)

        sc = st.columns(4)
        for col, val, lbl, c in [
            (sc[0], attempts,  "Attempts",   "var(--indigo2)"),
            (sc[1], f"{best_pct}%", "Best Score", "var(--emerald)"),
            (sc[2], f"{avg_pct}%",  "Avg Score",  "var(--amber)"),
            (sc[3], f"#{my_rank}" if my_rank else "—", "Rank", "var(--teal2)"),
        ]:
            with col:
                st.markdown(f"""<div class="card" style="text-align:center;padding:1rem;border-top:3px solid {c};">
                  <div style="font-family:'Fira Code',monospace;font-size:1.5rem;font-weight:800;color:{c};">{val}</div>
                  <div style="font-size:0.68rem;color:var(--t3);text-transform:uppercase;margin-top:0.2rem;">{lbl}</div>
                </div>""", unsafe_allow_html=True)

        if my_scores:
            st.markdown('<div class="section-label">Recent Attempts</div>', unsafe_allow_html=True)
            for s in sorted(my_scores, key=lambda x: x.get("ts",""), reverse=True)[:5]:
                ts = datetime.fromisoformat(s["ts"]).strftime("%d %b %Y %H:%M") if s.get("ts") else "—"
                mode_badge = {"exam_sim":"🎓 Exam Sim","exam":"🧪 Mock","practice":"📝 Practice"}.get(s.get("mode",""), s.get("mode","—"))
                c = "var(--emerald)" if s["pct"]>=60 else ("var(--amber)" if s["pct"]>=40 else "var(--rose)")
                st.markdown(f"""<div class="card" style="padding:0.75rem 1rem;margin-bottom:0.4rem;display:flex;align-items:center;
                    justify-content:space-between;flex-wrap:wrap;gap:0.5rem;">
                  <span style="font-size:0.82rem;color:var(--t2);">{mode_badge}</span>
                  <span style="font-size:0.75rem;color:var(--t3);">{ts}</span>
                  <span style="font-family:'Fira Code',monospace;font-weight:700;color:{c};">{s["pct"]}% ({s["score"]}/{s["total"]})</span>
                </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🏆 View Leaderboard", use_container_width=True, type="primary"):
                st.session_state.page = "leaderboard"; st.rerun()
        with col2:
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.user = None; st.session_state.username = None
                st.session_state.page = "home"; st.rerun()
        return

    # ── Login / Register form ────────────────────
    st.markdown('<div class="login-wrap">', unsafe_allow_html=True)
    st.markdown('<span class="login-logo">🏛️</span>', unsafe_allow_html=True)
    st.markdown('<div class="login-title">NET Guru</div>', unsafe_allow_html=True)
    st.markdown('<div class="login-sub">Sign in to track progress, earn ranks, and join the student leaderboard</div>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["🔑 Login", "📝 Register"])

    with tab1:
        un = st.text_input("Username", key="login_un", placeholder="your_username")
        pw = st.text_input("Password", type="password", key="login_pw", placeholder="••••••••")
        st.markdown('<div style="font-size:0.75rem;color:var(--t3);margin-top:-0.5rem;margin-bottom:0.5rem;">Default demo: username <b>demo</b> · password <b>demo123</b></div>', unsafe_allow_html=True)
        if st.button("Login →", use_container_width=True, type="primary", key="do_login"):
            ok, user_data = verify_user(un, pw)
            if ok:
                st.session_state.user = user_data
                st.session_state.username = un
                st.session_state.page = "home"
                st.success(f"Welcome back, {user_data['name']}! 🎉")
                st.rerun()
            else:
                st.error("Invalid username or password.")

    with tab2:
        rname = st.text_input("Full Name",   key="reg_name", placeholder="Your Full Name")
        run   = st.text_input("Username",    key="reg_un",   placeholder="choose_a_username")
        rpw   = st.text_input("Password",    type="password", key="reg_pw", placeholder="minimum 6 characters")
        rpw2  = st.text_input("Confirm Password", type="password", key="reg_pw2", placeholder="repeat password")
        if st.button("Create Account →", use_container_width=True, type="primary", key="do_reg"):
            if not rname or not run or not rpw: st.error("Please fill all fields.")
            elif rpw != rpw2: st.error("Passwords don't match.")
            elif len(rpw) < 6: st.error("Password must be at least 6 characters.")
            else:
                ok, msg = register_user(run, rpw, rname)
                if ok:
                    ok2, udata = verify_user(run, rpw)
                    st.session_state.user = udata
                    st.session_state.username = run
                    st.session_state.page = "home"
                    st.success(f"Account created! Welcome, {rname} 🎉")
                    st.rerun()
                else: st.error(msg)

    st.markdown('</div>', unsafe_allow_html=True)

    # Auto-create demo accounts for leaderboard demo
    try:
        users = load_users()
        demo_accounts = [
            ("demo",    "demo123",  "Demo Student"),
            ("arjun",   "test123",  "Arjun Kumar"),
            ("priya",   "test123",  "Priya Nair"),
            ("rahul",   "test123",  "Rahul Sharma"),
            ("anjali",  "test123",  "Anjali Menon"),
        ]
        scores = load_scores()
        existing_score_users = {s.get("username") for s in scores}
        for un_, pw_, nm_ in demo_accounts:
            if un_ not in users:
                register_user(un_, pw_, nm_)
            # Seed demo scores for leaderboard
            if un_ != "demo" and un_ not in existing_score_users:
                import random as _r
                sc_ = _r.randint(8, 14)
                save_score(un_, nm_, sc_, 15,
                           round(sc_/15*100), "exam", 900)
    except: pass


# ═══════════════════════════════════════════════
# PDF UPLOAD (dev only)
# ═══════════════════════════════════════════════
def page_pdf_upload():
    if not st.session_state.dev_mode:
        st.error("Developer access required."); return
    st.markdown('<h2 style="font-family:Syne,sans-serif;font-weight:800;">📄 PDF Upload (Developer)</h2>', unsafe_allow_html=True)
    st.info("Upload PDF question papers. Questions will be extracted and added to the bank with year/season metadata.")
    yr_in = st.selectbox("Year", PYQ_YEARS, key="pdf_yr")
    ss_in = st.selectbox("Season", SEASONS, key="pdf_ss")
    uploaded = st.file_uploader("Upload PDF", type="pdf", key="pdf_file")
    if uploaded:
        st.success(f"Uploaded: {uploaded.name} — {yr_in} {ss_in}")
        st.info("PDF extraction requires PyMuPDF/pdfplumber. Questions auto-tagged with selected year and season.")


# ═══════════════════════════════════════════════
# MAIN ROUTER
# ═══════════════════════════════════════════════
def main():
    inject_styles()
    render_sidebar()

    # Dev mode unlock via URL param
    if not st.session_state.dev_mode:
        params = st.query_params
        if params.get("dev") == DEVELOPER_PIN:
            st.session_state.dev_mode = True

    page = st.session_state.page

    # Guard developer-only pages
    if page == "pdf_upload" and not st.session_state.get("dev_mode", False):
        page = "home"
        st.session_state.page = "home"

    if   page == "home":        page_home()
    elif page == "pyq":         page_pyq()
    elif page == "quiz":
        if st.session_state.quiz_active or st.session_state.quiz_done:
            page_quiz()
        else:
            page_quiz_config()
    elif page == "mock":        page_mock()
    elif page == "ai":          page_ai()
    elif page == "analytics":   page_analytics()
    elif page == "bookmarks":   page_bookmarks()
    elif page == "leaderboard": page_leaderboard()
    elif page == "login":       page_login()
    elif page == "pdf_upload":  page_pdf_upload()
    else:                       page_home()

if __name__ == "__main__":
    main()
