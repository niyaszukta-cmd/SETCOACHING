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
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="collapsed"
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
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,800;0,900;1,700&family=Outfit:wght@300;400;500;600;700&family=Fira+Code:wght@400;500;600&display=swap');

/* ══════════════════════════════════════════════════════
   DESIGN TOKEN SYSTEM — Obsidian & Amber
══════════════════════════════════════════════════════ */
:root {
  /* Surfaces */
  --bg:       #080b12;
  --bg2:      #0d1220;
  --bg3:      #111828;
  --surface:  #141c2e;
  --surface2: #1a2438;
  --surface3: #1f2d45;

  /* Borders */
  --line:     #1e2d45;
  --line2:    #263650;
  --line3:    #2e4268;

  /* Brand palette */
  --amber:    #e8a020;
  --amber2:   #f5bc4a;
  --amber-glow: rgba(232,160,32,0.12);
  --teal:     #0fb8c9;
  --teal2:    #4dd9e8;
  --teal-glow: rgba(15,184,201,0.10);
  --emerald:  #10b981;
  --rose:     #f43f5e;
  --indigo:   #6366f1;
  --indigo2:  #818cf8;
  --indigo-glow: rgba(99,102,241,0.12);

  /* Text */
  --t1: #eef2ff;
  --t2: #8ba0c0;
  --t3: #4e6285;
  --t4: #2e3d55;

  /* Radii */
  --r-sm: 8px;
  --r-md: 14px;
  --r-lg: 20px;
  --r-xl: 28px;

  /* Shadows */
  --shadow-card: 0 2px 24px rgba(0,0,0,0.4), 0 1px 4px rgba(0,0,0,0.3);
  --shadow-glow-amber: 0 0 32px rgba(232,160,32,0.15);
  --shadow-glow-teal:  0 0 32px rgba(15,184,201,0.12);
}

/* ══════════════════════════════════════════════════════
   RESET & BASE
══════════════════════════════════════════════════════ */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

body, .stApp {
  background: var(--bg) !important;
  font-family: 'Outfit', sans-serif !important;
  color: var(--t1) !important;
  -webkit-font-smoothing: antialiased;
}

#MainMenu, footer, header, .stDeployButton, [data-testid="stText"] {
  display: none !important;
}

/* ── Main container ── */
.main .block-container {
  padding: 0 1rem 6rem !important;
  max-width: 100% !important;
}
@media (min-width: 900px) {
  .main .block-container {
    padding: 0 2.5rem 5rem !important;
    max-width: 1360px !important;
    margin: 0 auto !important;
  }
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--line3); border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: var(--indigo); }

/* ══════════════════════════════════════════════════════
   NAVIGATION BAR
══════════════════════════════════════════════════════ */
.topbar {
  position: sticky; top: 0; z-index: 1000;
  background: rgba(8, 11, 18, 0.94);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border-bottom: 1px solid var(--line);
  padding: 0 1.5rem;
  height: 60px;
  display: flex; align-items: center; justify-content: space-between;
  gap: 1rem;
}

.topbar-brand {
  font-family: 'Playfair Display', serif;
  font-size: 1.25rem; font-weight: 800;
  letter-spacing: -0.01em; white-space: nowrap;
  background: linear-gradient(110deg, var(--amber) 0%, var(--amber2) 40%, var(--teal2) 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
}
.topbar-brand span {
  font-style: italic; font-weight: 700;
}

.topbar-nav {
  display: flex; align-items: center; gap: 2px;
  overflow-x: auto; scrollbar-width: none;
}
.topbar-nav::-webkit-scrollbar { display: none; }

.nav-pill {
  padding: 0.4rem 0.85rem;
  border-radius: 50px;
  font-size: 0.79rem; font-weight: 600;
  color: var(--t3); cursor: pointer;
  border: 1px solid transparent;
  transition: all 0.18s ease;
  white-space: nowrap; letter-spacing: 0.01em;
}
.nav-pill:hover {
  color: var(--t1); background: var(--surface);
  border-color: var(--line2);
}
.nav-pill.active {
  color: var(--amber) !important;
  background: var(--amber-glow) !important;
  border-color: rgba(232,160,32,0.3) !important;
}

.user-chip {
  display: flex; align-items: center; gap: 0.5rem;
  background: var(--surface); border: 1px solid var(--line2);
  border-radius: 50px; padding: 0.3rem 0.85rem 0.3rem 0.3rem;
  font-size: 0.79rem; font-weight: 600; color: var(--t1);
  white-space: nowrap; flex-shrink: 0;
  transition: border-color 0.2s;
}
.user-chip:hover { border-color: var(--line3); }

.user-avatar {
  width: 1.6rem; height: 1.6rem; border-radius: 50%;
  background: linear-gradient(135deg, var(--indigo), var(--teal));
  display: flex; align-items: center; justify-content: center;
  font-size: 0.62rem; font-weight: 800; color: #fff; flex-shrink: 0;
  box-shadow: 0 0 0 2px rgba(99,102,241,0.3);
}

/* ══════════════════════════════════════════════════════
   PAGE ANATOMY HELPERS
══════════════════════════════════════════════════════ */
.page-wrap { padding-top: 1.5rem; animation: fadeUp 0.35s ease both; }
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(14px); }
  to   { opacity: 1; transform: translateY(0); }
}

.page-header {
  margin-bottom: 1.75rem;
  padding-bottom: 1.25rem;
  border-bottom: 1px solid var(--line);
}
.page-header h1 {
  font-family: 'Playfair Display', serif;
  font-size: clamp(1.6rem, 3.5vw, 2.2rem);
  font-weight: 800; color: var(--t1);
  letter-spacing: -0.02em; line-height: 1.15;
  margin-bottom: 0.4rem;
}
.page-header p {
  font-size: 0.9rem; color: var(--t2); line-height: 1.6;
  max-width: 680px;
}

.section-label {
  display: flex; align-items: center; gap: 0.75rem;
  font-size: 0.72rem; font-weight: 700; letter-spacing: 0.12em;
  text-transform: uppercase; color: var(--t3);
  margin: 2rem 0 1rem;
}
.section-label::before { content: ''; width: 3px; height: 14px; border-radius: 2px; background: var(--amber); flex-shrink: 0; }
.section-label::after  { content: ''; flex: 1; height: 1px; background: var(--line); }
.section-label .pill {
  background: var(--surface); border: 1px solid var(--line2);
  color: var(--t3); font-size: 0.6rem; padding: 0.15rem 0.5rem;
  border-radius: 20px; font-weight: 600; text-transform: uppercase;
}

/* ══════════════════════════════════════════════════════
   HERO SECTION
══════════════════════════════════════════════════════ */
.hero {
  text-align: center;
  padding: 3.5rem 1.5rem 2.5rem;
  position: relative; overflow: hidden;
}
.hero::before {
  content: '';
  position: absolute; inset: 0;
  background:
    radial-gradient(ellipse 90% 55% at 50% -10%, rgba(99,102,241,0.14), transparent),
    radial-gradient(ellipse 50% 40% at 90% 100%, rgba(15,184,201,0.08), transparent),
    radial-gradient(ellipse 40% 30% at 10% 80%, rgba(232,160,32,0.07), transparent);
  pointer-events: none;
}

.hero-badge {
  display: inline-flex; align-items: center; gap: 0.5rem;
  background: var(--amber-glow);
  border: 1px solid rgba(232,160,32,0.28);
  color: var(--amber); padding: 0.35rem 1.1rem; border-radius: 50px;
  font-size: 0.7rem; font-weight: 700; letter-spacing: 0.14em;
  text-transform: uppercase; margin-bottom: 1.5rem;
  animation: fadeUp 0.4s 0.1s ease both;
}
.hero-badge::before { content: '●'; font-size: 0.45rem; animation: blink 2s infinite; }
@keyframes blink { 0%,100%{opacity:1;} 50%{opacity:0.3;} }

.hero-title {
  font-family: 'Playfair Display', serif;
  font-size: clamp(2.4rem, 7vw, 5rem);
  font-weight: 900; line-height: 1.05;
  color: var(--t1); letter-spacing: -0.03em;
  margin-bottom: 1.1rem;
  animation: fadeUp 0.4s 0.2s ease both;
}
.hero-title em {
  font-style: italic;
  background: linear-gradient(110deg, var(--amber), var(--amber2), var(--teal2));
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-sub {
  font-size: 1.05rem; color: var(--t2); line-height: 1.75;
  max-width: 560px; margin: 0 auto 2rem;
  animation: fadeUp 0.4s 0.3s ease both;
}

/* ══════════════════════════════════════════════════════
   STAT STRIP
══════════════════════════════════════════════════════ */
.stat-strip {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: var(--r-lg);
  overflow: hidden;
  margin: 1.75rem 0;
  box-shadow: var(--shadow-card);
}
@media (max-width: 600px) { .stat-strip { grid-template-columns: repeat(3, 1fr); } }

.stat-cell {
  padding: 1.25rem 0.75rem;
  text-align: center;
  border-right: 1px solid var(--line);
  position: relative;
  transition: background 0.2s;
}
.stat-cell:last-child { border-right: none; }
.stat-cell:hover { background: var(--surface2); }

.stat-val {
  font-family: 'Playfair Display', serif;
  font-size: 1.9rem; font-weight: 800;
  display: block; line-height: 1;
  background: linear-gradient(135deg, var(--amber), var(--teal2));
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 0.3rem;
}
.stat-lbl {
  font-size: 0.62rem; color: var(--t3);
  text-transform: uppercase; letter-spacing: 0.12em; font-weight: 700;
}

/* ══════════════════════════════════════════════════════
   CARDS
══════════════════════════════════════════════════════ */
.card {
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: var(--r-lg);
  padding: 1.5rem;
  position: relative; overflow: hidden;
  transition: border-color 0.2s, transform 0.2s, box-shadow 0.2s;
  box-shadow: var(--shadow-card);
}
.card:hover {
  border-color: var(--line3);
  transform: translateY(-3px);
  box-shadow: 0 8px 40px rgba(0,0,0,0.5);
}

.card-accent-top {
  position: absolute; top: 0; left: 0; right: 0; height: 2px;
  border-radius: var(--r-lg) var(--r-lg) 0 0;
}
.card-glow {
  position: absolute; top: -30px; right: -30px;
  width: 100px; height: 100px; border-radius: 50%;
  opacity: 0.07; pointer-events: none;
  filter: blur(25px);
}

.card-icon {
  font-size: 1.75rem; margin-bottom: 0.85rem; display: block;
  line-height: 1;
}
.card-title {
  font-family: 'Playfair Display', serif;
  font-size: 1.05rem; font-weight: 700;
  color: var(--t1); margin-bottom: 0.5rem;
  letter-spacing: -0.01em;
}
.card-desc {
  font-size: 0.83rem; color: var(--t2); line-height: 1.65;
}
.card-meta { display: flex; gap: 0.4rem; flex-wrap: wrap; margin-top: 0.9rem; }

.chip {
  font-size: 0.66rem; font-weight: 700; letter-spacing: 0.04em;
  padding: 0.2rem 0.55rem; border-radius: 4px;
  background: var(--surface3); color: var(--t3);
  border: 1px solid var(--line2);
}
.chip.amber  { background: rgba(232,160,32,0.1);  color: var(--amber);   border-color: rgba(232,160,32,0.2); }
.chip.teal   { background: rgba(15,184,201,0.1);  color: var(--teal2);   border-color: rgba(15,184,201,0.2); }
.chip.emerald{ background: rgba(16,185,129,0.1);  color: var(--emerald); border-color: rgba(16,185,129,0.2); }
.chip.rose   { background: rgba(244,63,94,0.1);   color: var(--rose);    border-color: rgba(244,63,94,0.2);  }
.chip.indigo { background: rgba(99,102,241,0.12); color: var(--indigo2); border-color: rgba(99,102,241,0.2); }

/* ══════════════════════════════════════════════════════
   PYQ YEAR CARDS
══════════════════════════════════════════════════════ */
.year-card {
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: var(--r-md);
  padding: 1rem 0.6rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s;
  position: relative; overflow: hidden;
}
.year-card::after {
  content: '';
  position: absolute; bottom: 0; left: 0; right: 0; height: 2px;
  background: linear-gradient(90deg, var(--amber), var(--teal));
  transform: scaleX(0); transform-origin: left;
  transition: transform 0.25s ease;
}
.year-card:hover { border-color: var(--amber); background: var(--amber-glow); }
.year-card:hover::after { transform: scaleX(1); }

.year-num {
  font-family: 'Playfair Display', serif;
  font-size: 1.2rem; font-weight: 800;
  color: var(--amber); display: block;
  letter-spacing: -0.02em;
}
.year-count {
  font-size: 0.62rem; color: var(--t3);
  margin-top: 0.25rem; line-height: 1.6;
}

/* ══════════════════════════════════════════════════════
   QUIZ ENGINE
══════════════════════════════════════════════════════ */
/* Progress bar */
.progress-track {
  height: 3px; background: var(--line);
  border-radius: 10px; margin-bottom: 1.25rem;
  overflow: hidden;
}
.progress-fill {
  height: 100%; border-radius: 10px;
  background: linear-gradient(90deg, var(--indigo), var(--teal));
  transition: width 0.5s cubic-bezier(0.4,0,0.2,1);
  position: relative;
}
.progress-fill::after {
  content: '';
  position: absolute; right: 0; top: -1px;
  width: 8px; height: 5px;
  background: var(--teal2);
  border-radius: 50%;
  box-shadow: 0 0 8px var(--teal);
}

/* Timer */
.timer-display {
  font-family: 'Fira Code', monospace;
  font-size: 1.05rem; font-weight: 600;
  padding: 0.35rem 1rem; border-radius: var(--r-sm);
  border: 1px solid; min-width: 5.5rem; text-align: center;
  letter-spacing: 0.05em;
}
.timer-ok   { color: var(--teal2);  border-color: rgba(15,184,201,0.3);  background: rgba(15,184,201,0.07);  }
.timer-warn { color: var(--amber);  border-color: rgba(232,160,32,0.3);  background: rgba(232,160,32,0.07);  }
.timer-crit { color: var(--rose);   border-color: rgba(244,63,94,0.35);  background: rgba(244,63,94,0.08);
              animation: pulse-crit 0.8s ease-in-out infinite; }
@keyframes pulse-crit {
  0%, 100% { opacity: 1; box-shadow: none; }
  50% { opacity: 0.7; box-shadow: 0 0 12px rgba(244,63,94,0.4); }
}

/* Question card */
.question-wrap {
  background: var(--surface);
  border: 1px solid var(--line2);
  border-radius: var(--r-xl);
  padding: 1.75rem 1.5rem;
  margin: 0.75rem 0 1rem;
  position: relative;
  box-shadow: var(--shadow-card);
  animation: fadeUp 0.25s ease both;
}
@media (min-width: 768px) { .question-wrap { padding: 2.75rem 3rem; } }

.question-wrap::before {
  content: '';
  position: absolute; top: 0; left: 0; right: 0; height: 2px;
  border-radius: var(--r-xl) var(--r-xl) 0 0;
  background: linear-gradient(90deg, var(--indigo), var(--teal), var(--amber));
}

.q-num {
  font-family: 'Fira Code', monospace;
  font-size: 0.72rem; font-weight: 600;
  color: var(--indigo2); letter-spacing: 0.1em;
  margin-bottom: 1.1rem; text-transform: uppercase;
}

.q-text {
  font-family: 'Playfair Display', serif;
  font-size: clamp(1rem, 2.4vw, 1.28rem);
  font-weight: 700; color: var(--t1);
  line-height: 1.75; letter-spacing: -0.01em;
}

.q-tags { display: flex; gap: 0.4rem; flex-wrap: wrap; margin-top: 1rem; }

/* Answer options */
.opt-wrap { display: flex; flex-direction: column; gap: 0.5rem; margin-top: 1.25rem; }

.opt-btn {
  display: block; width: 100%; text-align: left;
  padding: 0.9rem 1.2rem 0.9rem 1rem;
  background: var(--bg2);
  border: 1.5px solid var(--line);
  border-radius: var(--r-md);
  color: var(--t1) !important; font-size: 0.93rem; font-weight: 500;
  cursor: pointer; transition: all 0.15s ease; line-height: 1.55;
  font-family: 'Outfit', sans-serif;
  position: relative;
}
.opt-btn::before {
  content: '';
  position: absolute; left: 0; top: 0; bottom: 0;
  width: 3px; border-radius: var(--r-md) 0 0 var(--r-md);
  background: transparent;
  transition: background 0.15s;
}
.opt-btn:hover {
  border-color: var(--indigo2);
  background: rgba(99,102,241,0.07) !important;
}
.opt-btn:hover::before { background: var(--indigo); }

.opt-selected {
  background: rgba(99,102,241,0.1) !important;
  border-color: var(--indigo) !important;
  color: var(--t1) !important; font-weight: 600 !important;
}
.opt-selected::before { background: var(--indigo) !important; }

.opt-correct {
  background: rgba(16,185,129,0.1) !important;
  border-color: var(--emerald) !important;
  color: var(--emerald) !important;
}
.opt-correct::before { background: var(--emerald) !important; }

.opt-wrong {
  background: rgba(244,63,94,0.08) !important;
  border-color: var(--rose) !important;
  color: var(--rose) !important;
}
.opt-wrong::before { background: var(--rose) !important; }

.opt-neutral {
  background: var(--bg2) !important;
  border-color: var(--line) !important;
  color: var(--t3) !important;
}

/* Explanation */
.explanation {
  background: linear-gradient(135deg, rgba(99,102,241,0.07), rgba(15,184,201,0.04));
  border: 1px solid rgba(99,102,241,0.2);
  border-left: 3px solid var(--indigo);
  border-radius: var(--r-md);
  padding: 1.1rem 1.4rem;
  margin-top: 1.25rem;
  animation: fadeUp 0.2s ease both;
}
.exp-head {
  font-weight: 700; color: var(--indigo2);
  font-size: 0.8rem; letter-spacing: 0.06em;
  text-transform: uppercase; margin-bottom: 0.5rem;
  display: flex; align-items: center; gap: 0.5rem;
}
.exp-body { color: var(--t2); font-size: 0.88rem; line-height: 1.75; }

/* ══════════════════════════════════════════════════════
   EXAM NAVIGATOR PANEL
══════════════════════════════════════════════════════ */
.exam-panel {
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: var(--r-lg);
  padding: 1.25rem;
  position: sticky; top: 4.5rem;
  box-shadow: var(--shadow-card);
}
.exam-panel-title {
  font-size: 0.68rem; font-weight: 700; letter-spacing: 0.12em;
  text-transform: uppercase; color: var(--t3);
  margin-bottom: 0.85rem; padding-bottom: 0.6rem;
  border-bottom: 1px solid var(--line);
}

.exam-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(2.3rem, 1fr));
  gap: 0.3rem;
  max-height: 16rem; overflow-y: auto;
  margin-bottom: 0.75rem;
}

.exam-q-btn {
  aspect-ratio: 1; border-radius: var(--r-sm);
  border: 1px solid var(--line);
  background: var(--bg2); color: var(--t3);
  font-size: 0.68rem; font-weight: 700;
  display: flex; align-items: center; justify-content: center;
  cursor: pointer; transition: all 0.12s;
  font-family: 'Fira Code', monospace;
}
.exam-q-btn:hover { border-color: var(--indigo2); color: var(--indigo2); }
.exam-q-btn.answered {
  background: rgba(16,185,129,0.12);
  border-color: rgba(16,185,129,0.4);
  color: var(--emerald);
}
.exam-q-btn.current {
  background: var(--indigo);
  border-color: var(--indigo);
  color: #fff;
  box-shadow: 0 0 12px rgba(99,102,241,0.4);
}
.exam-q-btn.skipped {
  background: rgba(232,160,32,0.12);
  border-color: rgba(232,160,32,0.35);
  color: var(--amber);
}

.exam-legend {
  display: flex; gap: 0.85rem; flex-wrap: wrap;
  font-size: 0.64rem; color: var(--t3); margin-top: 0.6rem;
}
.legend-dot { display: inline-block; width: 7px; height: 7px; border-radius: 2px; margin-right: 3px; }

/* ══════════════════════════════════════════════════════
   RESULTS PAGE
══════════════════════════════════════════════════════ */
.result-hero {
  text-align: center;
  padding: 3rem 1.5rem 2.5rem;
  background:
    radial-gradient(ellipse 60% 50% at 50% 0%, rgba(99,102,241,0.12), transparent);
  border-radius: var(--r-xl);
  border: 1px solid var(--line2);
  margin-bottom: 1.75rem;
  position: relative; overflow: hidden;
  animation: fadeUp 0.3s ease both;
}
.result-hero::before {
  content: '';
  position: absolute; top: 0; left: 0; right: 0; height: 2px;
  background: linear-gradient(90deg, var(--indigo), var(--teal), var(--amber));
}

.grade-letter {
  font-family: 'Playfair Display', serif;
  font-size: 6rem; font-weight: 900;
  line-height: 1; display: block;
  margin-bottom: 0.5rem;
  filter: drop-shadow(0 0 20px currentColor);
}
.result-score {
  font-family: 'Fira Code', monospace;
  font-size: 2.2rem; font-weight: 600;
  color: var(--t1); letter-spacing: -0.02em;
}
.result-pct { font-size: 1rem; color: var(--t2); margin: 0.4rem 0; }
.result-msg {
  font-family: 'Playfair Display', serif;
  font-size: 1rem; color: var(--amber);
  font-style: italic; margin-top: 0.5rem;
}

.stat-card-mini {
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: var(--r-md);
  padding: 1rem 0.75rem;
  text-align: center;
  border-top-width: 3px;
  transition: transform 0.2s;
}
.stat-card-mini:hover { transform: translateY(-2px); }
.stat-card-mini .val {
  font-family: 'Fira Code', monospace;
  font-size: 1.65rem; font-weight: 700;
  display: block; line-height: 1.1; margin-bottom: 0.25rem;
}
.stat-card-mini .lbl {
  font-size: 0.64rem; color: var(--t3);
  text-transform: uppercase; letter-spacing: 0.1em; font-weight: 700;
}

/* ══════════════════════════════════════════════════════
   LEADERBOARD
══════════════════════════════════════════════════════ */
.lb-row {
  display: flex; align-items: center; gap: 0.85rem;
  padding: 0.85rem 1.1rem;
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: var(--r-md);
  margin-bottom: 0.4rem;
  transition: all 0.15s;
  animation: fadeUp 0.25s ease both;
}
.lb-row:hover { border-color: var(--line3); transform: translateX(3px); }
.lb-row.me {
  border-color: var(--amber) !important;
  background: linear-gradient(90deg, rgba(232,160,32,0.06), transparent) !important;
}

.lb-rank {
  font-family: 'Playfair Display', serif;
  font-size: 1.1rem; font-weight: 800;
  min-width: 2rem; text-align: center;
}
.lb-rank.gold   { color: var(--amber); }
.lb-rank.silver { color: #9fb3cc; }
.lb-rank.bronze { color: #b87333; }
.lb-rank.rest   { color: var(--t4); font-family: 'Fira Code', monospace; font-size: 0.85rem; }

.lb-avatar {
  width: 2.4rem; height: 2.4rem; border-radius: 50%; flex-shrink: 0;
  background: linear-gradient(135deg, var(--indigo), var(--teal));
  display: flex; align-items: center; justify-content: center;
  font-weight: 800; font-size: 0.78rem; color: #fff;
  box-shadow: 0 0 0 2px rgba(99,102,241,0.2);
}
.lb-name   { font-weight: 600; font-size: 0.9rem; color: var(--t1); }
.lb-detail { font-size: 0.68rem; color: var(--t3); margin-top: 0.15rem; }
.lb-score  {
  font-family: 'Fira Code', monospace;
  font-size: 0.9rem; font-weight: 600; color: var(--teal2);
  text-align: right;
}

/* Podium */
.podium-card {
  background: var(--surface);
  border: 1px solid var(--line2);
  border-radius: var(--r-lg);
  padding: 1.5rem 1rem; text-align: center;
  transition: transform 0.2s;
}
.podium-card:hover { transform: translateY(-4px); }
.podium-card.first {
  border-color: rgba(232,160,32,0.4);
  background: linear-gradient(180deg, rgba(232,160,32,0.06), transparent);
}

/* ══════════════════════════════════════════════════════
   LOGIN PAGE
══════════════════════════════════════════════════════ */
.login-wrap {
  max-width: 440px; margin: 3rem auto;
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: var(--r-xl);
  padding: 3rem 2.5rem;
  text-align: center;
  box-shadow: 0 20px 60px rgba(0,0,0,0.5);
  animation: fadeUp 0.3s ease both;
  position: relative; overflow: hidden;
}
.login-wrap::before {
  content: '';
  position: absolute; top: 0; left: 0; right: 0; height: 2px;
  background: linear-gradient(90deg, var(--amber), var(--teal));
}
.login-logo {
  font-size: 3rem; margin-bottom: 1rem; display: block;
  filter: drop-shadow(0 4px 12px rgba(232,160,32,0.3));
}
.login-title {
  font-family: 'Playfair Display', serif;
  font-size: 1.8rem; font-weight: 800; color: var(--t1);
  margin-bottom: 0.4rem; letter-spacing: -0.02em;
}
.login-sub { font-size: 0.85rem; color: var(--t2); margin-bottom: 2rem; line-height: 1.6; }

/* ══════════════════════════════════════════════════════
   STREAMLIT WIDGET OVERRIDES
══════════════════════════════════════════════════════ */
/* All button text color fix */
button, button *, .stButton button, .stButton button * {
  color: var(--t1) !important;
  font-family: 'Outfit', sans-serif !important;
}

.stButton > button {
  border-radius: var(--r-sm) !important;
  font-weight: 600 !important;
  font-size: 0.88rem !important;
  transition: all 0.18s ease !important;
  letter-spacing: 0.01em !important;
}

/* Primary buttons */
.stButton > button[kind="primary"],
[data-testid="baseButton-primary"] {
  background: linear-gradient(135deg, var(--indigo) 0%, #7c8ff0 100%) !important;
  color: #fff !important;
  border: none !important;
  box-shadow: 0 4px 18px rgba(99,102,241,0.3) !important;
}
.stButton > button[kind="primary"] *,
[data-testid="baseButton-primary"] * { color: #fff !important; }
.stButton > button[kind="primary"]:hover,
[data-testid="baseButton-primary"]:hover {
  box-shadow: 0 6px 28px rgba(99,102,241,0.5) !important;
  transform: translateY(-1px) !important;
}

/* Secondary buttons */
.stButton > button[kind="secondary"],
[data-testid="baseButton-secondary"] {
  background: var(--surface) !important;
  border: 1px solid var(--line2) !important;
  color: var(--t1) !important;
}
.stButton > button[kind="secondary"]:hover,
[data-testid="baseButton-secondary"]:hover {
  border-color: var(--line3) !important;
  background: var(--surface2) !important;
}

/* Form containers */
div[data-testid="stForm"] {
  border: none !important; padding: 0 !important; background: transparent !important;
}
div[data-testid="stForm"] button { color: var(--t1) !important; }
div[data-testid="stForm"] button * { color: inherit !important; }

/* Text inputs */
.stTextInput input, .stTextArea textarea {
  background: var(--bg2) !important;
  border: 1px solid var(--line2) !important;
  color: var(--t1) !important;
  border-radius: var(--r-sm) !important;
  font-family: 'Outfit', sans-serif !important;
  font-size: 0.92rem !important;
  padding: 0.6rem 0.85rem !important;
  transition: border-color 0.15s !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
  border-color: var(--indigo) !important;
  box-shadow: 0 0 0 3px rgba(99,102,241,0.15) !important;
  outline: none !important;
}

/* Labels */
.stSelectbox label, .stMultiSelect label, .stSlider label, .stRadio label,
.stCheckbox label, .stTextInput label, .stTextArea label,
.stToggle label, .stSelectSlider label, .stNumberInput label {
  color: var(--t2) !important; font-weight: 600 !important;
  font-size: 0.82rem !important; letter-spacing: 0.02em !important;
  text-transform: uppercase !important;
}

/* Selectboxes */
div[data-baseweb="select"] {
  background: var(--bg2) !important; border-color: var(--line2) !important;
  border-radius: var(--r-sm) !important;
}
div[data-baseweb="select"] * { color: var(--t1) !important; }
div[data-baseweb="select"]:focus-within { border-color: var(--indigo) !important; }

/* Progress */
.stProgress > div > div > div > div {
  background: linear-gradient(90deg, var(--indigo), var(--teal)) !important;
  border-radius: 10px !important;
}

/* Alerts */
.stInfo    { background: rgba(99,102,241,0.08) !important; border-color: rgba(99,102,241,0.3) !important;   color: var(--indigo2) !important; border-radius: var(--r-md) !important; }
.stSuccess { background: rgba(16,185,129,0.08) !important; border-color: rgba(16,185,129,0.3) !important;   color: var(--emerald) !important; border-radius: var(--r-md) !important; }
.stError   { background: rgba(244,63,94,0.08)  !important; border-color: rgba(244,63,94,0.3)  !important;   color: var(--rose) !important;    border-radius: var(--r-md) !important; }
.stWarning { background: rgba(232,160,32,0.08) !important; border-color: rgba(232,160,32,0.3) !important;   color: var(--amber) !important;   border-radius: var(--r-md) !important; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
  background: var(--surface) !important;
  border-radius: var(--r-sm) !important;
  gap: 0 !important; padding: 3px !important;
  border: 1px solid var(--line) !important;
}
.stTabs [data-baseweb="tab"] {
  border-radius: 6px !important; color: var(--t2) !important;
  font-weight: 600 !important; font-size: 0.85rem !important;
  transition: all 0.2s !important;
}
.stTabs [aria-selected="true"] {
  background: var(--bg3) !important; color: var(--t1) !important;
  box-shadow: 0 1px 4px rgba(0,0,0,0.3) !important;
}
.stTabs [data-baseweb="tab-border"] { display: none !important; }

/* Checkboxes & radio */
.stCheckbox > label { gap: 0.5rem !important; }
.stRadio [role="radio"] { accent-color: var(--indigo) !important; }

/* Sidebar */
[data-testid="stSidebar"] {
  background: var(--bg2) !important;
  border-right: 1px solid var(--line) !important;
}

/* HR */
hr { border: none !important; border-top: 1px solid var(--line) !important; margin: 1.5rem 0 !important; }

/* Expander */
.streamlit-expanderHeader {
  background: var(--surface) !important;
  border: 1px solid var(--line) !important;
  border-radius: var(--r-sm) !important;
  color: var(--t1) !important;
}

/* Toggle */
.stToggle input:checked + div { background: var(--indigo) !important; }

/* Multiselect tags */
[data-baseweb="tag"] {
  background: rgba(99,102,241,0.15) !important;
  border-color: rgba(99,102,241,0.3) !important;
}
[data-baseweb="tag"] span { color: var(--indigo2) !important; }

/* ══════════════════════════════════════════════════════
   MISC UTILITIES
══════════════════════════════════════════════════════ */
.divider { height: 1px; background: var(--line); margin: 1.5rem 0; }
.text-muted { color: var(--t2); font-size: 0.85rem; }
.text-tiny  { color: var(--t3); font-size: 0.72rem; }

/* Empty state */
.empty-state {
  text-align: center; padding: 4rem 2rem;
  color: var(--t3);
}
.empty-state .icon { font-size: 2.5rem; display: block; margin-bottom: 1rem; opacity: 0.5; }
.empty-state h3 { font-family: 'Playfair Display', serif; color: var(--t2); margin-bottom: 0.4rem; }

/* Mobile */
@media (max-width: 600px) {
  .topbar { padding: 0 0.75rem; }
  .topbar-nav { display: none; }
  .stat-strip .stat-cell:nth-child(n+4) { display: none; }
  .page-header h1 { font-size: 1.4rem; }
}
</style>

<script>
/* Fix Streamlit button text color inheritance */
(function(){
  function fix() {
    document.querySelectorAll('button').forEach(function(b){
      b.querySelectorAll('p,span,div').forEach(function(el){
        el.style.setProperty('color','inherit','important');
      });
    });
  }
  fix();
  new MutationObserver(fix).observe(document.body, {childList:true, subtree:true});
})();
</script>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════
# QUESTION BANK
# ═══════════════════════════════════════════════
BUILTIN_QUESTIONS = [
    {"id":"ta001","topic":"Teaching Aptitude","difficulty":"Medium","year":2023,"season":"June","question":"Which level of teaching focuses on the development of thinking power and reasoning in students?","options":["Memory level","Understanding level","Reflective level","None of these"],"correct_answer":"Reflective level","explanation":"Reflective level teaching by Morrison focuses on critical thinking, problem-solving, and independent reasoning."},
    {"id":"ta002","topic":"Teaching Aptitude","difficulty":"Easy","year":2022,"season":"December","question":"Which of the following is NOT a characteristic of effective teaching?","options":["Clarity of goals","Flexibility","Dogmatic approach","Student-centered learning"],"correct_answer":"Dogmatic approach","explanation":"Effective teaching is flexible and student-centered; a dogmatic approach hinders learning."},
    {"id":"ta003","topic":"Teaching Aptitude","difficulty":"Hard","year":2023,"season":"December","question":"In the context of Bloom's Taxonomy (revised), which cognitive level represents the highest order of thinking?","options":["Evaluation","Synthesis","Creating","Analysis"],"correct_answer":"Creating","explanation":"The revised Bloom's Taxonomy places 'Creating' at the apex — generating new ideas, products, or ways of viewing things."},
    {"id":"ta004","topic":"Teaching Aptitude","difficulty":"Medium","year":2021,"season":"June","question":"Which teaching method is most appropriate for large classrooms with heterogeneous groups?","options":["Project Method","Lecture Method","Inquiry Method","Seminar Method"],"correct_answer":"Lecture Method","explanation":"The lecture method is most practical for large, heterogeneous groups."},
    {"id":"ta005","topic":"Teaching Aptitude","difficulty":"Medium","year":2020,"season":"June","question":"The concept of 'Micro-Teaching' was first developed at:","options":["Harvard University","Stanford University","Yale University","MIT"],"correct_answer":"Stanford University","explanation":"Micro-teaching was developed by Dwight W. Allen at Stanford University in 1963."},
    {"id":"ta006","topic":"Teaching Aptitude","difficulty":"Easy","year":2019,"season":"June","question":"Which of the following best describes 'formative evaluation'?","options":["Evaluation at the end of the course","Evaluation to assign final grades","Ongoing evaluation during instruction","Evaluation before the course begins"],"correct_answer":"Ongoing evaluation during instruction","explanation":"Formative evaluation is continuous assessment conducted during the instructional process."},
    {"id":"ta007","topic":"Teaching Aptitude","difficulty":"Hard","year":2018,"season":"December","question":"Which theory proposes that students have different 'learning styles'?","options":["Constructivism","VAK/VARK Model","Behaviorism","Gestalt Theory"],"correct_answer":"VAK/VARK Model","explanation":"The VARK model categorizes learners by Visual, Auditory, Read/Write, and Kinesthetic modes."},
    {"id":"ta008","topic":"Teaching Aptitude","difficulty":"Medium","year":2022,"season":"June","question":"The 'Socratic Method' of teaching primarily involves:","options":["Lecture and demonstration","Asking probing questions","Group projects","Use of audio-visual aids"],"correct_answer":"Asking probing questions","explanation":"The Socratic method uses disciplined questioning to stimulate critical thinking."},
    {"id":"ra001","topic":"Research Aptitude","difficulty":"Medium","year":2023,"season":"June","question":"Which type of research aims to solve immediate practical problems?","options":["Fundamental research","Applied research","Action research","Historical research"],"correct_answer":"Action research","explanation":"Action research is conducted by practitioners to solve specific, immediate problems."},
    {"id":"ra002","topic":"Research Aptitude","difficulty":"Easy","year":2021,"season":"December","question":"A hypothesis is best described as:","options":["A proven fact","A tentative statement to be tested","A summary of findings","A literature review"],"correct_answer":"A tentative statement to be tested","explanation":"A hypothesis is a tentative, testable proposition about the relationship between variables."},
    {"id":"ra003","topic":"Research Aptitude","difficulty":"Hard","year":2020,"season":"December","question":"Which sampling method ensures every member has an equal chance of being selected?","options":["Purposive sampling","Snowball sampling","Simple Random Sampling","Quota sampling"],"correct_answer":"Simple Random Sampling","explanation":"Simple Random Sampling gives every individual an equal probability of selection."},
    {"id":"ra004","topic":"Research Aptitude","difficulty":"Medium","year":2019,"season":"June","question":"The term 'triangulation' in research refers to:","options":["Geometric analysis","Using multiple methods to validate findings","A statistical test","Sampling technique"],"correct_answer":"Using multiple methods to validate findings","explanation":"Triangulation uses multiple data sources to cross-check and validate research findings."},
    {"id":"ra005","topic":"Research Aptitude","difficulty":"Medium","year":2018,"season":"June","question":"Which research design determines cause-and-effect relationships?","options":["Descriptive","Correlational","Experimental","Ethnographic"],"correct_answer":"Experimental","explanation":"Experimental research establishes causality by manipulating an independent variable."},
    {"id":"ra006","topic":"Research Aptitude","difficulty":"Hard","year":2017,"season":"December","question":"A Type I error in research refers to:","options":["Accepting a false null hypothesis","Rejecting a true null hypothesis","Failing to collect data","Using the wrong test"],"correct_answer":"Rejecting a true null hypothesis","explanation":"A Type I error occurs when the null hypothesis is true but incorrectly rejected."},
    {"id":"rc001","topic":"Reading Comprehension","difficulty":"Medium","year":2023,"season":"December","question":"Inferential comprehension requires the reader to:","options":["Locate directly stated info","Draw conclusions beyond what is stated","Memorize the passage","Summarize only"],"correct_answer":"Draw conclusions beyond what is stated","explanation":"Inferential comprehension involves reading between the lines to draw logical conclusions."},
    {"id":"rc002","topic":"Reading Comprehension","difficulty":"Easy","year":2022,"season":"June","question":"The main idea of a passage is:","options":["A supporting detail","The central thought or theme","The title","A specific example"],"correct_answer":"The central thought or theme","explanation":"The main idea is the primary message the author wants to communicate."},
    {"id":"comm001","topic":"Communication","difficulty":"Medium","year":2023,"season":"June","question":"Which type of communication uses symbols, gestures and body language?","options":["Verbal communication","Non-verbal communication","Written communication","Formal communication"],"correct_answer":"Non-verbal communication","explanation":"Non-verbal communication includes body language, gestures, facial expressions, and other non-linguistic signals."},
    {"id":"comm002","topic":"Communication","difficulty":"Easy","year":2021,"season":"June","question":"'Noise' in the communication process refers to:","options":["Loud sounds only","Any interference disrupting the message","The sender's voice","Background music"],"correct_answer":"Any interference disrupting the message","explanation":"Noise is any barrier — physical, psychological, or semantic — that distorts communication."},
    {"id":"comm003","topic":"Communication","difficulty":"Hard","year":2020,"season":"December","question":"The Shannon-Weaver model of communication is also known as:","options":["Transactional model","Mathematical model","Interactional model","Linear model"],"correct_answer":"Mathematical model","explanation":"Shannon and Weaver's 1949 model, originally developed for telephone communication, is called the Mathematical Model."},
    {"id":"rea001","topic":"Reasoning","difficulty":"Medium","year":2023,"season":"June","question":"If all roses are flowers and some flowers fade quickly, which conclusion is valid?","options":["All roses fade quickly","Some roses may fade quickly","No roses fade quickly","All flowers are roses"],"correct_answer":"Some roses may fade quickly","explanation":"From the given premises, we can only conclude that some roses may fade quickly — not all or none."},
    {"id":"rea002","topic":"Reasoning","difficulty":"Hard","year":2022,"season":"December","question":"In a series: 2, 6, 12, 20, 30, __ what is the next number?","options":["40","42","44","48"],"correct_answer":"42","explanation":"Differences: 4,6,8,10,12. Next term = 30+12 = 42. Pattern: n(n+1) for n=1,2,3..."},
    {"id":"rea003","topic":"Reasoning","difficulty":"Easy","year":2021,"season":"June","question":"Which diagram best represents the relationship between Teachers, Professors, and Humans?","options":["Three separate circles","Concentric circles","Two overlapping circles inside one large circle","All identical circles"],"correct_answer":"Two overlapping circles inside one large circle","explanation":"Teachers and Professors are subsets of Humans; they overlap as some professors teach."},
    {"id":"ict001","topic":"ICT","difficulty":"Easy","year":2023,"season":"December","question":"What does 'www' stand for in a web address?","options":["World Wide Web","World Web Works","Wide World Web","Web World Wire"],"correct_answer":"World Wide Web","explanation":"WWW stands for World Wide Web — the information system accessed via the Internet using URLs."},
    {"id":"ict002","topic":"ICT","difficulty":"Medium","year":2022,"season":"June","question":"Which protocol is used to transfer files over the internet?","options":["HTTP","FTP","SMTP","TCP"],"correct_answer":"FTP","explanation":"FTP (File Transfer Protocol) is specifically designed for transferring files between client and server."},
    {"id":"ict003","topic":"ICT","difficulty":"Hard","year":2019,"season":"December","question":"Which generation of computers used transistors?","options":["First generation","Second generation","Third generation","Fourth generation"],"correct_answer":"Second generation","explanation":"Second-generation computers (1956-1963) used transistors, replacing vacuum tubes."},
    {"id":"ict004","topic":"ICT","difficulty":"Hard","year":2018,"season":"June","question":"Moore's Law states transistor count doubles approximately every:","options":["6 months","1 year","2 years","5 years"],"correct_answer":"2 years","explanation":"Gordon Moore observed in 1965 that transistor count doubles roughly every two years."},
    {"id":"env001","topic":"Environment & Ecology","difficulty":"Medium","year":2023,"season":"June","question":"The 'Paris Agreement' primarily addresses:","options":["Nuclear non-proliferation","Climate change and global warming","Trade barriers","Ozone depletion"],"correct_answer":"Climate change and global warming","explanation":"The Paris Agreement (2015) limits global warming to well below 2 degrees Celsius."},
    {"id":"env002","topic":"Environment & Ecology","difficulty":"Easy","year":2022,"season":"December","question":"Which gas is primarily responsible for the greenhouse effect?","options":["Oxygen","Nitrogen","Carbon Dioxide","Hydrogen"],"correct_answer":"Carbon Dioxide","explanation":"CO2 is the primary anthropogenic greenhouse gas."},
    {"id":"env003","topic":"Environment & Ecology","difficulty":"Hard","year":2021,"season":"June","question":"The 'Chipko Movement' in India was primarily associated with:","options":["Water conservation","Forest and tree conservation","Wildlife protection","Soil conservation"],"correct_answer":"Forest and tree conservation","explanation":"The Chipko Movement (1973) was a protest where villagers embraced trees to prevent their felling."},
    {"id":"he001","topic":"Higher Education","difficulty":"Medium","year":2023,"season":"December","question":"The NEP 2020 recommends the school curriculum to be restructured as:","options":["10+2","5+3+3+4","8+4","6+3+2+1"],"correct_answer":"5+3+3+4","explanation":"NEP 2020 proposes a 5+3+3+4 curricular structure."},
    {"id":"he002","topic":"Higher Education","difficulty":"Easy","year":2022,"season":"June","question":"UGC stands for:","options":["University Grants Commission","United Graduates Council","Universal Government College","University General Council"],"correct_answer":"University Grants Commission","explanation":"UGC is the statutory body for coordination and maintenance of standards in higher education."},
    {"id":"he003","topic":"Higher Education","difficulty":"Hard","year":2020,"season":"December","question":"'Autonomous Institutions' in Indian higher education means:","options":["Complete independence","Freedom to design curriculum and conduct exams","Government-funded colleges","Deemed universities"],"correct_answer":"Freedom to design curriculum and conduct exams","explanation":"Autonomous institutions have freedom to design curriculum, conduct exams, and declare results."},
    {"id":"gov001","topic":"Indian Constitution & Governance","difficulty":"Easy","year":2023,"season":"June","question":"The Preamble describes India as:","options":["Federal, Democratic Republic","Sovereign, Socialist, Secular, Democratic Republic","Federal, Socialist State","Secular Parliamentary Democracy"],"correct_answer":"Sovereign, Socialist, Secular, Democratic Republic","explanation":"The Preamble declares India to be a Sovereign, Socialist, Secular, Democratic Republic."},
    {"id":"gov002","topic":"Indian Constitution & Governance","difficulty":"Medium","year":2022,"season":"December","question":"Which Article guarantees Right to Education?","options":["Article 19","Article 21A","Article 25","Article 32"],"correct_answer":"Article 21A","explanation":"Article 21A provides free and compulsory education to children aged 6-14."},
    {"id":"gov003","topic":"Indian Constitution & Governance","difficulty":"Hard","year":2021,"season":"June","question":"The 'Basic Structure' doctrine was established by:","options":["Golaknath case (1967)","Kesavananda Bharati case (1973)","Minerva Mills case (1980)","Maneka Gandhi case (1978)"],"correct_answer":"Kesavananda Bharati case (1973)","explanation":"The Basic Structure Doctrine established that Parliament cannot alter the basic structure of the Constitution."},
    {"id":"di001","topic":"Data Interpretation","difficulty":"Medium","year":2023,"season":"June","question":"If the mean of 5 numbers is 30 and mean of 3 of them is 20, what is mean of remaining 2?","options":["35","45","40","50"],"correct_answer":"45","explanation":"Total=150, Sum of 3=60, Remaining=90, Mean=45."},
    {"id":"di002","topic":"Data Interpretation","difficulty":"Easy","year":2022,"season":"June","question":"Which measure of central tendency is most affected by extreme values?","options":["Mode","Median","Mean","None"],"correct_answer":"Mean","explanation":"The arithmetic mean is significantly affected by extreme values."},
    {"id":"di003","topic":"Data Interpretation","difficulty":"Hard","year":2021,"season":"December","question":"The coefficient of variation (CV) is calculated as:","options":["(Mean/SD)x100","(SD/Mean)x100","SD x Mean","Mean/Variance"],"correct_answer":"(SD/Mean)x100","explanation":"CV = (SD/Mean) x 100, expressing variability as a percentage of mean."},
]

# AI Predicted questions (marked with predicted=True)
AI_PREDICTED_QUESTIONS = [
    {"id":"ai001","topic":"Teaching Aptitude","difficulty":"Hard","year":2025,"season":"June","predicted":True,"question":"Based on NEP 2020 implementation trends, which pedagogical shift is most likely to be tested?","options":["Shift from rote learning to competency-based education","Increased emphasis on standardized testing","Reduction in teacher training programs","Focus on single-language instruction"],"correct_answer":"Shift from rote learning to competency-based education","explanation":"NEP 2020 emphasizes competency-based education as a core reform — highly likely to appear in upcoming exams."},
    {"id":"ai002","topic":"Research Aptitude","difficulty":"Medium","year":2025,"season":"June","predicted":True,"question":"With increasing use of AI in research, which ethical concern is most prominent?","options":["Data fabrication","Algorithmic bias and transparency","Plagiarism only","Sample size issues"],"correct_answer":"Algorithmic bias and transparency","explanation":"AI-driven research raises significant concerns about algorithmic bias, reproducibility, and transparency — a trending exam topic."},
    {"id":"ai003","topic":"ICT","difficulty":"Medium","year":2025,"season":"June","predicted":True,"question":"Which technology is central to India's Digital India initiative for education?","options":["Blockchain","Cloud computing and mobile internet","Quantum computing","5G only"],"correct_answer":"Cloud computing and mobile internet","explanation":"Digital India's education thrust relies on cloud-based platforms and mobile internet access for DIKSHA, SWAYAM, etc."},
    {"id":"ai004","topic":"Environment & Ecology","difficulty":"Hard","year":2025,"season":"June","predicted":True,"question":"India's National Action Plan on Climate Change (NAPCC) includes how many missions?","options":["6","8","10","12"],"correct_answer":"8","explanation":"NAPCC has 8 national missions covering solar energy, water, forests, sustainable agriculture, etc. — frequently tested."},
    {"id":"ai005","topic":"Higher Education","difficulty":"Medium","year":2025,"season":"December","predicted":True,"question":"The Academic Bank of Credits (ABC) under NEP 2020 primarily facilitates:","options":["Financial aid to students","Multiple entry/exit and credit transfer","Faculty recruitment","Research funding"],"correct_answer":"Multiple entry/exit and credit transfer","explanation":"ABC enables credit accumulation and transfer, supporting flexible degree completion pathways under NEP 2020."},
]


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
def topbar():
    user = st.session_state.user
    uname = st.session_state.username or ""

    pages_public  = [("🏛️","Home","home"),("📅","PYQ","pyq"),("📝","Practice","quiz"),("🧪","Mocks","mock"),("🏆","Leaderboard","leaderboard")]
    pages_private = [("🤖","AI Predict","ai"),("📊","Analytics","analytics"),("🔖","Bookmarks","bookmarks")]

    nav_html = '<div class="topbar">'
    nav_html += '<div class="topbar-brand">NET Guru</div>'
    nav_html += '<div class="topbar-nav" id="topbar-nav">'

    all_pages = pages_public + (pages_private if user else [])
    for icon, label, key in all_pages:
        active = "active" if st.session_state.page == key else ""
        nav_html += f'<span class="nav-pill {active}" data-page="{key}">{icon} {label}</span>'

    nav_html += "</div>"
    if user:
        initials = "".join(w[0].upper() for w in user.get("name","U").split()[:2])
        nav_html += f'<div class="user-chip"><div class="user-avatar">{initials}</div><span>{user.get("name","").split()[0]}</span></div>'
    else:
        nav_html += '<div class="user-chip" style="color:var(--amber);border-color:rgba(232,160,32,0.35);cursor:pointer;">👤 Login</div>'
    nav_html += "</div>"

    st.markdown(nav_html, unsafe_allow_html=True)

    # Actual nav buttons — one per page (hidden via JS, real Streamlit buttons)
    # We render real buttons in a compact row
    st.markdown("<div style='display:flex;gap:0.4rem;flex-wrap:wrap;padding:0.5rem 0.5rem 0;'>", unsafe_allow_html=True)
    cols = st.columns(len(all_pages) + 2)
    for i, (icon, label, key) in enumerate(all_pages):
        with cols[i]:
            t = "primary" if st.session_state.page == key else "secondary"
            if st.button(f"{icon} {label}", key=f"nav_{key}", type=t, use_container_width=True):
                st.session_state.page = key
                st.session_state.quiz_active = False
                st.rerun()
    with cols[len(all_pages)]:
        if user:
            initials_short = "".join(w[0].upper() for w in user.get("name","U").split()[:2])
            if st.button(f"👤 {initials_short}", key="nav_profile", use_container_width=True, type="primary"):
                st.session_state.page = "login"  # profile page reuses login
                st.rerun()
        else:
            if st.button("👤 Login", key="nav_login", use_container_width=True, type="primary"):
                st.session_state.page = "login"
                st.rerun()
    # Dev mode unlock (hidden in last col)
    with cols[len(all_pages)+1]:
        if st.session_state.dev_mode:
            if st.button("🔧 PDF", key="nav_pdf", use_container_width=True):
                st.session_state.page = "pdf_upload"
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<hr style='margin:0 0 0.75rem;'/>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════
# HOME PAGE
# ═══════════════════════════════════════════════
def page_home():
    qb = QuestionBank()
    total = len(qb.get_all())
    years = qb.get_years()
    user  = st.session_state.user

    # ── Hero ──────────────────────────────────────
    st.markdown("""
    <div class="hero">
      <div class="hero-badge">🏛️ UGC NET · Paper 1 · NYZTrade Education</div>
      <h1 class="hero-title">Master NET with<br><em>Intelligent Practice</em></h1>
      <p class="hero-sub">PYQ year-wise · Full mock tests · AI-predicted questions · Live exam simulation · Student leaderboard</p>
    </div>""", unsafe_allow_html=True)

    # ── Stat strip ────────────────────────────────
    user_attempts = st.session_state.total_attempted
    user_accuracy = round(st.session_state.total_correct / user_attempts * 100) if user_attempts else 0
    st.markdown(f"""
    <div class="stat-strip">
      <div class="stat-cell"><span class="stat-val">{total}+</span><span class="stat-lbl">Questions</span></div>
      <div class="stat-cell"><span class="stat-val">{len(years)}</span><span class="stat-lbl">PYQ Years</span></div>
      <div class="stat-cell"><span class="stat-val">10</span><span class="stat-lbl">Topics</span></div>
      <div class="stat-cell"><span class="stat-val">{user_attempts}</span><span class="stat-lbl">Your Attempts</span></div>
      <div class="stat-cell"><span class="stat-val">{user_accuracy}%</span><span class="stat-lbl">Accuracy</span></div>
    </div>""", unsafe_allow_html=True)

    # ── Quick-start cards ─────────────────────────
    st.markdown('<div class="section-label">Quick Start <span class="pill">choose a mode</span></div>', unsafe_allow_html=True)

    cards = [
        ("📅", "PYQ Practice",   "Year-wise previous year questions",  "pyq",   "var(--amber)",   "amber",   "2023 · 2022 · 2021"),
        ("🧪", "Mock Tests",     "Full-length timed exam simulations",  "mock",  "var(--indigo)",  "indigo",  "50 Qs · 180 min"),
        ("🤖", "AI Predicted",   "Smart questions for upcoming exams",  "ai",    "var(--teal)",    "teal",    "June 2025 focus"),
        ("⚡", "Quick Drill",    "15 questions, 15 min sprint",         "quick", "var(--emerald)", "emerald", "All topics mixed"),
    ]
    c1, c2, c3, c4 = st.columns(4)
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
def page_pyq():
    qb = QuestionBank()
    all_q = qb.get_all()

    st.markdown("""<div class="page-header">
      <h1>📅 Previous Year Questions</h1>
      <p>Practice questions from actual UGC NET exams — organized by year, season, topic, and difficulty. Each session: <strong>15 questions</strong>.</p>
    </div>""", unsafe_allow_html=True)

    # ── Year cards — primary feature ─────────────
    st.markdown('<div class="section-label">📅 Select Year <span class="pill">15 Qs per session · click to launch</span></div>', unsafe_allow_html=True)
    available_years = qb.get_years()

    if not available_years:
        st.markdown("""<div class="card" style="text-align:center;padding:2.5rem;border-color:rgba(232,160,32,0.25);">
          <div style="font-size:2.5rem;margin-bottom:0.75rem;">📂</div>
          <div style="font-family:'Playfair Display',serif;font-weight:700;font-size:1rem;color:var(--t2);">No PYQ data yet</div>
          <div style="color:var(--t3);font-size:0.82rem;margin-top:0.4rem;">Upload PDF question papers via Developer mode to populate year-wise questions.</div>
        </div>""", unsafe_allow_html=True)
    else:
        # Show year grid — up to 8 years, 4 per row
        yr_rows = [available_years[i:i+4] for i in range(0, min(len(available_years), 8), 4)]
        for row in yr_rows:
            yr_cols = st.columns(len(row))
            for i, yr in enumerate(row):
                yr_q    = [q for q in all_q if str(q.get("year",""))==str(yr)]
                june_cnt = len([q for q in yr_q if q.get("season")=="June"])
                dec_cnt  = len([q for q in yr_q if q.get("season")=="December"])
                total_cnt= len(yr_q)
                with yr_cols[i]:
                    st.markdown(f"""<div class="year-card">
                      <span class="year-num">{yr}</span>
                      <div class="year-count">☀️ {june_cnt} &nbsp; ❄️ {dec_cnt}</div>
                      <div style="font-size:0.65rem;color:var(--t3);margin-top:0.2rem;">{total_cnt} questions</div>
                    </div>""", unsafe_allow_html=True)
                    c_june, c_dec = st.columns(2)
                    with c_june:
                        if st.button(f"☀️ Jun", key=f"pyq_june_{yr}", use_container_width=True,
                                     type="primary" if june_cnt>0 else "secondary", disabled=june_cnt==0):
                            qs = qb.get_filtered(years=[yr], seasons=["June"], n=15)
                            _start_quiz(qs, "practice", f"PYQ {yr} June", 15*72); st.rerun()
                    with c_dec:
                        if st.button(f"❄️ Dec", key=f"pyq_dec_{yr}", use_container_width=True,
                                     type="primary" if dec_cnt>0 else "secondary", disabled=dec_cnt==0):
                            qs = qb.get_filtered(years=[yr], seasons=["December"], n=15)
                            _start_quiz(qs, "practice", f"PYQ {yr} Dec", 15*72); st.rerun()
                    if st.button(f"🎯 All {yr}", key=f"pyq_yr_{yr}", use_container_width=True):
                        qs = qb.get_filtered(years=[yr], n=15)
                        _start_quiz(qs, "practice", f"PYQ {yr} (All)", 15*72); st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Season Series cards ────────────────────────────────
    st.markdown('<div class="section-label">📆 Season Series <span class="pill">combined across years</span></div>', unsafe_allow_html=True)
    sc1, sc2 = st.columns(2)
    june_total = len([q for q in all_q if q.get("season")=="June"])
    dec_total  = len([q for q in all_q if q.get("season")=="December"])
    with sc1:
        st.markdown(f"""<div class="card" style="border-color:rgba(232,160,32,0.35);">
          <div class="card-accent-top" style="background:var(--amber);"></div>
          <span style="font-size:1.8rem;">☀️</span>
          <div class="card-title" style="margin-top:0.5rem;">June Series</div>
          <div class="card-desc">All June-session PYQs combined · {june_total} questions</div>
          <div class="card-meta"><span class="chip">15 Qs</span><span class="chip amber">18 min</span></div>
        </div>""", unsafe_allow_html=True)
        if st.button("Start June Series →", key="pyq_june_all", use_container_width=True, type="primary", disabled=june_total==0):
            qs = qb.get_filtered(seasons=["June"], n=15)
            _start_quiz(qs, "practice", "June Series", 15*72); st.rerun()

    with sc2:
        st.markdown(f"""<div class="card" style="border-color:rgba(15,184,201,0.35);">
          <div class="card-accent-top" style="background:var(--teal);"></div>
          <span style="font-size:1.8rem;">❄️</span>
          <div class="card-title" style="margin-top:0.5rem;">December Series</div>
          <div class="card-desc">All December-session PYQs combined · {dec_total} questions</div>
          <div class="card-meta"><span class="chip">15 Qs</span><span class="chip teal">18 min</span></div>
        </div>""", unsafe_allow_html=True)
        if st.button("Start December Series →", key="pyq_dec_all", use_container_width=True, type="primary", disabled=dec_total==0):
            qs = qb.get_filtered(seasons=["December"], n=15)
            _start_quiz(qs, "practice", "December Series", 15*72); st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Custom filter session ─────────────────────
    st.markdown('<div class="section-label">🔎 Custom Filter Session</div>', unsafe_allow_html=True)
    with st.expander("▸ Filters (year, season, topic, difficulty)", expanded=False):
        fc1, fc2, fc3 = st.columns(3)
        with fc1: sel_years   = st.multiselect("Year",     options=qb.get_years(),   default=[], placeholder="All years",   key="pyq_years")
        with fc2: sel_seasons = st.multiselect("Season",   options=qb.get_seasons(), default=[], placeholder="All seasons", key="pyq_seasons")
        with fc3: sel_topics  = st.multiselect("Topics",   options=qb.get_topics(),  default=[], placeholder="All topics",  key="pyq_topics")
        fc4, fc5, fc6 = st.columns(3)
        with fc4: sel_diff = st.selectbox("Difficulty", ["Mixed","Easy","Medium","Hard"], key="pyq_diff")
        with fc5: sel_n    = st.select_slider("Questions", [10,15,20,25,30,50], value=15, key="pyq_n")
        with fc6:
            timed   = st.toggle("⏱ Timed Mode", value=True, key="pyq_timed")
            t_limit = sel_n * 72

        preview = qb.get_filtered(topics=sel_topics or None, difficulty=sel_diff,
                                   years=sel_years or None, seasons=sel_seasons or None, n=9999, shuffle=False)
        st.markdown(f'<div style="color:var(--indigo2);font-weight:700;font-size:0.84rem;margin-bottom:0.5rem;">✅ {len(preview)} questions match · {min(sel_n,len(preview))} will be used</div>', unsafe_allow_html=True)

        if st.button("🚀 Start Filtered Session", use_container_width=True, type="primary", key="pyq_start"):
            qs = qb.get_filtered(topics=sel_topics or None, difficulty=sel_diff,
                                 years=sel_years or None, seasons=sel_seasons or None, n=sel_n)
            if not qs: st.error("No questions match your filters. Try broadening the selection.")
            else:
                _start_quiz(qs, "practice", f"PYQ Custom ({sel_diff})", t_limit if timed else 0); st.rerun()


# ═══════════════════════════════════════════════
# MOCK TESTS PAGE
# ═══════════════════════════════════════════════
MOCK_BLUEPRINTS = [
    # Exam Simulation
    {"id":"m_exam1","name":"Exam Simulation — Set 1","icon":"🎓","tag":"Exam Simulation","tag_c":"violet","total":50,"mins":180,"diff":"Mixed","topics":None,"seasons":None,"desc":"Full UGC NET pattern · 50 Qs · 3 hrs · Live countdown · Auto-submit","exam_sim":True},
    {"id":"m_exam2","name":"Exam Simulation — Set 2","icon":"🎓","tag":"Exam Simulation","tag_c":"violet","total":50,"mins":180,"diff":"Mixed","topics":None,"seasons":None,"desc":"New shuffle · same exam conditions · ranked on leaderboard","exam_sim":True},
    # Full Mock Tests
    {"id":"m_full1","name":"Full Mock — Set 1","icon":"🎯","tag":"Full Mock","tag_c":"indigo","total":50,"mins":90,"diff":"Mixed","topics":None,"seasons":None,"desc":"50 questions · 90 min · All topics · Full bank shuffle","exam_sim":False},
    {"id":"m_full2","name":"Full Mock — Set 2","icon":"🎯","tag":"Full Mock","tag_c":"indigo","total":50,"mins":90,"diff":"Mixed","topics":None,"seasons":None,"desc":"Fresh shuffle · same pattern · compare your score","exam_sim":False},
    # 15-Q Sprints
    {"id":"m_15_1","name":"15-Q Sprint — Set A","icon":"⚡","tag":"15-Q Sprint","tag_c":"gold","total":15,"mins":18,"diff":"Mixed","topics":None,"seasons":None,"desc":"15 questions · 18 min · Perfect for quick revision","exam_sim":False},
    {"id":"m_15_2","name":"15-Q Sprint — Set B","icon":"⚡","tag":"15-Q Sprint","tag_c":"gold","total":15,"mins":18,"diff":"Mixed","topics":None,"seasons":None,"desc":"Second sprint set · different question selection","exam_sim":False},
    {"id":"m_15_3","name":"15-Q Hard Challenge","icon":"🔥","tag":"15-Q Sprint","tag_c":"red","total":15,"mins":18,"diff":"Hard","topics":None,"seasons":None,"desc":"15 hard questions only · tests your limits · 18 min","exam_sim":False},
    {"id":"m_15_easy","name":"15-Q Warm-Up","icon":"🌱","tag":"15-Q Sprint","tag_c":"green","total":15,"mins":18,"diff":"Easy","topics":None,"seasons":None,"desc":"Easy questions · great for beginners and warm-up","exam_sim":False},
    # Topic Sprints
    {"id":"m_teach","name":"Teaching Sprint","icon":"🧠","tag":"Topic Sprint","tag_c":"cyan","total":25,"mins":40,"diff":"Mixed","topics":["Teaching Aptitude"],"seasons":None,"desc":"25 questions · Teaching Aptitude only · 40 min","exam_sim":False},
    {"id":"m_res","name":"Research Sprint","icon":"🔬","tag":"Topic Sprint","tag_c":"cyan","total":25,"mins":40,"diff":"Mixed","topics":["Research Aptitude"],"seasons":None,"desc":"25 questions · Research Aptitude only · 40 min","exam_sim":False},
    {"id":"m_ict","name":"ICT + Reasoning","icon":"💻","tag":"Topic Sprint","tag_c":"cyan","total":20,"mins":30,"diff":"Mixed","topics":["ICT","Reasoning"],"seasons":None,"desc":"ICT and Reasoning combined · 20 Qs · 30 min","exam_sim":False},
    {"id":"m_env","name":"Environment Sprint","icon":"🌿","tag":"Topic Sprint","tag_c":"cyan","total":20,"mins":30,"diff":"Mixed","topics":["Environment & Ecology"],"seasons":None,"desc":"Environment & Ecology only · 20 Qs · 30 min","exam_sim":False},
    # Season PYQ Mocks
    {"id":"m_june","name":"June PYQ Series","icon":"☀️","tag":"Season Mock","tag_c":"gold","total":50,"mins":90,"diff":"Mixed","topics":None,"seasons":["June"],"desc":"All June-session PYQs · 50 Qs · 90 min","exam_sim":False},
    {"id":"m_dec","name":"December PYQ Series","icon":"❄️","tag":"Season Mock","tag_c":"gold","total":50,"mins":90,"diff":"Mixed","topics":None,"seasons":["December"],"desc":"All December-session PYQs · 50 Qs · 90 min","exam_sim":False},
]

def page_mock():
    qb = QuestionBank()

    st.markdown("""<div class="page-header">
      <h1>🧪 Mock Tests</h1>
      <p>Structured tests for every need — Exam Simulation · Full Mocks · 15-Q Sprints · Topic Sprints · Season PYQs. All auto-scored and ranked.</p>
    </div>""", unsafe_allow_html=True)

    # ── Exam Simulation banner ─────────────────────
    sim_mocks = [m for m in MOCK_BLUEPRINTS if m.get("exam_sim")]
    st.markdown('<div class="section-label">🎓 Exam Simulation <span class="pill">UGC NET real conditions · 50 Qs · 3 hrs · auto-submit</span></div>', unsafe_allow_html=True)
    sim_cols = st.columns(len(sim_mocks))
    for i, m in enumerate(sim_mocks):
        avail = qb.get_filtered(topics=m["topics"], difficulty=m["diff"], seasons=m["seasons"], n=9999, shuffle=False)
        cnt = len(avail); can = cnt > 0; used = min(m["total"], cnt)
        avail_color = "var(--emerald)" if can else "var(--rose)"
        with sim_cols[i]:
            st.markdown(f"""<div class="card" style="border-color:rgba(99,102,241,0.5);background:linear-gradient(135deg,rgba(99,102,241,0.07),rgba(15,184,201,0.04));">
              <div class="card-accent-top" style="background:linear-gradient(90deg,var(--indigo),var(--teal));"></div>
              <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:0.5rem;">
                <span style="font-size:2rem;">{m["icon"]}</span>
                <span style="font-size:0.68rem;color:{avail_color};font-weight:700;">✓ {cnt} Qs available</span>
              </div>
              <div class="card-title" style="color:var(--indigo2);">{m["name"]}</div>
              <div class="card-desc">{m["desc"]}</div>
              <div class="card-meta">
                <span class="chip" style="color:var(--indigo2);border-color:rgba(99,102,241,0.3);">📝 {used} Qs</span>
                <span class="chip amber">⏱ 180 min</span>
                <span class="chip" style="color:var(--rose);border-color:rgba(244,63,94,0.3);">🔒 No pause</span>
              </div>
            </div>""", unsafe_allow_html=True)
            if st.button(f"🎓 Start {m['name'][:28]}", key=f"mock_{m['id']}", use_container_width=True,
                         type="primary" if can else "secondary", disabled=not can):
                qs = qb.get_filtered(topics=m["topics"], difficulty=m["diff"], seasons=m["seasons"], n=m["total"])
                _start_quiz(qs, "exam_sim", m["name"], m["mins"]*60); st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── All other mock groups ──────────────────────
    tag_order  = ["Full Mock", "15-Q Sprint", "Topic Sprint", "Season Mock"]
    tag_colors = {"Full Mock":"var(--indigo)","15-Q Sprint":"var(--amber)","Topic Sprint":"var(--teal)","Season Mock":"var(--amber2)"}

    tags = {}
    for m in MOCK_BLUEPRINTS:
        if not m.get("exam_sim"):
            tags.setdefault(m["tag"], []).append(m)

    for tag in tag_order:
        mocks = tags.get(tag, [])
        if not mocks: continue
        chip_color = tag_colors.get(tag, "var(--teal)")
        st.markdown(f'<div class="section-label">{tag} <span class="pill">{len(mocks)} tests</span></div>', unsafe_allow_html=True)

        cols = st.columns(min(len(mocks), 2) if len(mocks) <= 4 else 3)
        for i, m in enumerate(mocks):
            avail = qb.get_filtered(topics=m["topics"], difficulty=m["diff"], seasons=m["seasons"], n=9999, shuffle=False)
            cnt   = len(avail); used = min(m["total"], cnt); can = cnt > 0
            avail_color = "var(--emerald)" if can else "var(--rose)"
            avail_label = f"✓ {cnt} available" if can else "⚠ No questions"
            with cols[i % len(cols)]:
                st.markdown(f"""<div class="card">
                  <div class="card-accent-top" style="background:{chip_color};"></div>
                  <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:0.5rem;">
                    <span style="font-size:1.5rem;">{m["icon"]}</span>
                    <span style="font-size:0.65rem;color:{avail_color};font-weight:700;">{avail_label}</span>
                  </div>
                  <div class="card-title" style="font-size:0.9rem;">{m["name"]}</div>
                  <div class="card-desc" style="font-size:0.77rem;">{m["desc"]}</div>
                  <div class="card-meta">
                    <span class="chip">📝 {used} Qs</span>
                    <span class="chip">⏱ {m["mins"]}m</span>
                    <span class="chip teal">{m["diff"]}</span>
                  </div>
                </div>""", unsafe_allow_html=True)
                if st.button(f"Start →", key=f"mock_{m['id']}", use_container_width=True,
                             type="primary" if can else "secondary", disabled=not can):
                    qs = qb.get_filtered(topics=m["topics"], difficulty=m["diff"], seasons=m["seasons"], n=m["total"])
                    _start_quiz(qs, "exam", m["name"], m["mins"]*60); st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Custom Mock Builder ────────────────────────
    st.markdown('<div class="section-label">🔧 Custom Mock Builder <span class="pill">build your own</span></div>', unsafe_allow_html=True)
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
      <p>Questions curated by AI analysis of exam trends, NEP 2020 reforms, and topic frequency — targeted at upcoming exams.</p>
    </div>""", unsafe_allow_html=True)

    ai_qs = [q for q in qb.get_all() if q.get("predicted")]

    st.markdown(f"""<div class="card" style="border-color:rgba(15,184,201,0.3);margin-bottom:1.5rem;">
      <div class="card-accent-top" style="background:linear-gradient(90deg,var(--teal),var(--indigo));"></div>
      <div style="display:flex;gap:1.5rem;align-items:center;flex-wrap:wrap;">
        <div style="font-size:2.8rem;line-height:1;">🤖</div>
        <div>
          <div style="font-family:'Playfair Display',serif;font-weight:800;font-size:1.15rem;color:var(--teal2);">{len(ai_qs)} AI-Predicted Questions</div>
          <div style="color:var(--t2);font-size:0.85rem;margin-top:0.3rem;">Based on trend analysis · June 2025 focus · NEP 2020 aligned</div>
        </div>
      </div>
    </div>""", unsafe_allow_html=True)

    diff_colors = {"Easy":"var(--emerald)","Medium":"var(--amber)","Hard":"var(--rose)"}
    for q in ai_qs:
        dc = diff_colors.get(q.get("difficulty",""), "var(--t2)")
        st.markdown(f"""<div class="card" style="margin-bottom:0.6rem;">
          <div class="card-meta" style="margin-bottom:0.6rem;">
            <span class="chip teal">{q.get("topic","—")}</span>
            <span class="chip" style="color:{dc};border-color:{dc}20;">{q.get("difficulty","—")}</span>
            <span class="chip amber">🤖 AI Pick</span>
          </div>
          <div style="font-family:'Playfair Display',serif;font-weight:700;color:var(--t1);font-size:0.95rem;line-height:1.65;">{q["question"]}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🚀 Practice All AI Questions", use_container_width=True, type="primary", key="ai_all"):
            if ai_qs: _start_quiz(ai_qs, "practice", "AI Predicted Questions", len(ai_qs)*90); st.rerun()
            else: st.error("No AI predicted questions in bank yet.")
    with c2:
        if st.button("🧪 AI + PYQ Mix Mock", use_container_width=True, key="ai_mock"):
            reg_qs = qb.get_filtered(n=15, shuffle=True)
            mixed  = (ai_qs + reg_qs)[:20]; random.shuffle(mixed)
            _start_quiz(mixed, "exam", "AI Predicted Mix Mock", 20*90); st.rerun()


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

    q = questions[idx]
    elapsed   = int(time.time() - st.session_state.start_time)
    tl        = st.session_state.total_time
    remaining = max(0, tl - elapsed) if tl > 0 else None

    # Auto-submit when time runs out
    if remaining is not None and remaining == 0:
        st.session_state.quiz_done = True
        st.session_state.score = sum(1 for a in st.session_state.answers.values() if a.get("correct"))
        st.rerun()
        return

    # ── LIVE TIMER: working countdown via st.rerun ──
    # Store last rerun time to throttle refreshes to ~5s intervals
    if remaining is not None and remaining > 0:
        last_refresh = st.session_state.get("_timer_refresh", 0)
        now_t = time.time()
        if now_t - last_refresh >= 5:
            st.session_state["_timer_refresh"] = now_t
            import streamlit as _st
            # Auto-rerun to update timer display every 5 seconds
            time.sleep(0.05)
            st.rerun()

    # Timer display
    rm, rs = divmod(remaining or 0, 60)
    pct_left = (remaining / tl) if (remaining is not None and tl > 0) else 1.0
    if pct_left > 0.4:    timer_cls = "timer-ok"
    elif pct_left > 0.15: timer_cls = "timer-warn"
    else:                 timer_cls = "timer-crit"

    timer_html = (
        f'<div class="timer-display {timer_cls}">⏱ {rm:02d}:{rs:02d}</div>'
        if remaining is not None else
        '<div class="timer-display timer-ok">⏱ Free</div>'
    )

    diff_color = {"Easy":"var(--green)","Medium":"var(--gold)","Hard":"var(--red)"}.get(q.get("difficulty",""),"var(--text2)")
    yr_tag = f'· {q.get("year","")} {q.get("season","")}' if q.get("year") else ""
    ai_tag = '<span class="meta-chip cyan" style="font-size:0.65rem;padding:0.15rem 0.4rem;">🤖 AI Pick</span>' if q.get("predicted") else ""

    is_exam_sim = (mode == "exam_sim")

    col_q, col_nav = (st.columns([3, 1]) if mode in ("exam", "exam_sim") else (st.container(), None))

    with (col_q if mode in ("exam", "exam_sim") else col_q):
        # ── Exam Simulation header bar ─────────────
        if is_exam_sim:
            timer_color = "var(--rose)" if (remaining is not None and remaining < 600) else ("var(--amber)" if (remaining is not None and remaining < 1800) else "var(--teal2)")
            st.markdown(f"""<div style="background:rgba(10,14,22,0.95);border:1px solid rgba(99,102,241,0.4);border-radius:12px;
                padding:0.75rem 1.25rem;display:flex;align-items:center;justify-content:space-between;
                margin-bottom:1rem;gap:1rem;flex-wrap:wrap;">
              <div style="display:flex;align-items:center;gap:0.5rem;">
                <span style="font-size:1.1rem;">🎓</span>
                <span style="font-weight:700;font-size:0.88rem;color:var(--indigo2);">{label}</span>
              </div>
              <div style="font-family:'Fira Code',monospace;font-size:1.6rem;font-weight:700;color:{timer_color};
                  letter-spacing:0.05em;text-shadow:0 0 20px {timer_color}40;">
                ⏱ {rm:02d}:{rs:02d}
              </div>
              <div style="font-size:0.82rem;color:var(--t2);">Q {idx+1} / {total}</div>
            </div>""", unsafe_allow_html=True)
        else:
            # Progress bar
            pct_done = idx / total
            st.markdown(f'<div class="progress-track"><div class="progress-fill" style="width:{pct_done*100:.1f}%"></div></div>', unsafe_allow_html=True)

            # Label + timer row
            lc1, lc2, lc3 = st.columns([3, 2, 1])
            with lc1:
                st.markdown(f'<div style="font-size:0.8rem;color:var(--text2);font-weight:600;">📝 {label}</div>', unsafe_allow_html=True)
            with lc2:
                st.markdown(f'<div style="display:flex;justify-content:center;">{timer_html}</div>', unsafe_allow_html=True)
            with lc3:
                st.markdown(f'<div style="text-align:right;font-family:JetBrains Mono,monospace;font-size:0.8rem;color:var(--text2);">{idx+1}/{total}</div>', unsafe_allow_html=True)

        # Question card
        clean_q = html.unescape(re.sub(r'<[^>]+>', '', q["question"])).strip()
        st.markdown(f"""<div class="question-wrap">
          <div class="q-num">QUESTION {idx+1} OF {total}</div>
          <div class="q-text">{clean_q}</div>
          <div class="q-tags">
            <span class="meta-chip" style="color:{diff_color}">{q.get("difficulty","")}</span>
            <span class="meta-chip violet">{q.get("topic","")}</span>
            <span class="meta-chip">{yr_tag}</span>
            {ai_tag}
          </div>
        </div>""", unsafe_allow_html=True)

        # Options
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
                    st.markdown(f'<div class="opt-btn opt-correct">✅ {clean}</div>', unsafe_allow_html=True)
                elif opt == user_ans and opt != correct:
                    st.markdown(f'<div class="opt-btn opt-wrong">❌ {clean}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="opt-btn opt-neutral">{clean}</div>', unsafe_allow_html=True)
            if q.get("explanation") and mode != "exam":
                clean_exp = html.unescape(re.sub(r'<[^>]+>', '', q["explanation"])).strip()
                st.markdown(f'<div class="explanation"><div class="exp-head">💡 Explanation</div><div class="exp-body">{clean_exp}</div></div>', unsafe_allow_html=True)
            nc1, nc2, nc3 = st.columns([1, 1, 1])
            with nc1:
                if idx > 0 and st.button("← Prev", key=f"prev_{idx}", use_container_width=True):
                    st.session_state.q_idx -= 1; st.rerun()
            with nc2:
                bm_id = q.get("id", idx)
                bm_label = "🔖 Saved" if bm_id in st.session_state.bookmarks else "🔖 Save"
                if st.button(bm_label, key=f"bm_{idx}", use_container_width=True):
                    if bm_id in st.session_state.bookmarks: st.session_state.bookmarks.discard(bm_id)
                    else: st.session_state.bookmarks.add(bm_id)
                    st.rerun()
            with nc3:
                if idx < total - 1:
                    if st.button("Next →", key=f"next_{idx}", use_container_width=True, type="primary"):
                        st.session_state.q_idx += 1; st.session_state.q_start = time.time(); st.rerun()
                else:
                    if st.button("🏁 Finish", key=f"finish_{idx}", use_container_width=True, type="primary"):
                        st.session_state.quiz_done = True
                        st.session_state.score = sum(1 for a in st.session_state.answers.values() if a.get("correct"))
                        st.rerun()
        else:
            clean_opts = [html.unescape(re.sub(r'<[^>]+>', '', o)).strip() for o in options]
            for i_o, (opt, clean) in enumerate(zip(options, clean_opts)):
                is_sel = st.session_state[sel_key] == opt
                cls    = "opt-btn opt-selected" if is_sel else "opt-btn"
                prefix = "●" if is_sel else "○"
                st.markdown(f'<div class="{cls}">{prefix} {clean}</div>', unsafe_allow_html=True)
                if not is_sel:
                    if st.button(f"Select {i_o+1}", key=f"opt_{idx}_{i_o}", use_container_width=True):
                        st.session_state[sel_key] = opt; st.rerun()

            st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
            sc1, sc2, sc3 = st.columns([3, 1, 1])
            with sc1:
                if st.button("✅ Submit Answer", key=f"sub_{idx}", use_container_width=True, type="primary"):
                    choice = st.session_state[sel_key]
                    correct_flag = (choice == correct)
                    t_taken = int(time.time() - (st.session_state.q_start or time.time()))
                    st.session_state.answers[idx] = {"answer": choice, "correct": correct_flag, "time": t_taken}
                    st.session_state.q_times[idx]  = t_taken
                    st.session_state.total_attempted += 1
                    if correct_flag:
                        st.session_state.total_correct += 1
                        st.session_state.streak += 1
                    else:
                        st.session_state.streak = 0
                        if q not in st.session_state.wrong_questions:
                            st.session_state.wrong_questions.append(q)
                    if mode == "exam":
                        st.session_state.q_idx += 1
                        st.session_state.q_start = time.time()
                    st.rerun()
            with sc2:
                if st.button("⏭ Skip", key=f"skip_{idx}", use_container_width=True):
                    st.session_state.answers[idx] = {"answer": None, "correct": False, "skipped": True}
                    st.session_state.q_idx += 1; st.session_state.q_start = time.time(); st.rerun()
            with sc3:
                if st.button("🔖", key=f"bm2_{idx}", use_container_width=True):
                    bm_id = q.get("id", idx)
                    if bm_id in st.session_state.bookmarks: st.session_state.bookmarks.discard(bm_id)
                    else: st.session_state.bookmarks.add(bm_id)
                    st.rerun()

        # Auto-advance timer: rerun every 5s while question is live to refresh timer display
        if remaining is not None and remaining > 0 and not already:
            time.sleep(1)
            st.rerun()

    # Exam mode: question navigator panel
    if mode == "exam" and col_nav is not None:
        with col_nav:
            st.markdown('<div class="card" style="position:sticky;top:4rem;">', unsafe_allow_html=True)
            st.markdown('<div style="font-size:0.75rem;font-weight:700;color:var(--text2);margin-bottom:0.5rem;text-transform:uppercase;letter-spacing:0.08em;">Question Navigator</div>', unsafe_allow_html=True)
            # Large live timer in exam panel
            st.markdown(f'<div style="text-align:center;margin-bottom:0.75rem;">{timer_html}</div>', unsafe_allow_html=True)
            st.markdown('<div class="exam-grid">', unsafe_allow_html=True)
            nav_html = ""
            for qi in range(total):
                if qi == idx:
                    cls = "exam-q-btn current"
                elif qi in st.session_state.answers:
                    cls = "exam-q-btn answered" if not st.session_state.answers[qi].get("skipped") else "exam-q-btn skipped"
                else:
                    cls = "exam-q-btn"
                nav_html += f'<div class="{cls}">{qi+1}</div>'
            st.markdown(nav_html + '</div>', unsafe_allow_html=True)
            st.markdown("""<div style="margin-top:0.75rem;font-size:0.68rem;color:var(--text3);">
              <span style="color:var(--green);">■</span> Answered &nbsp;
              <span style="color:var(--gold);">■</span> Skipped &nbsp;
              <span style="color:var(--violet2);">■</span> Current
            </div>""", unsafe_allow_html=True)
            answered_count = sum(1 for a in st.session_state.answers.values() if not a.get("skipped"))
            st.markdown(f'<div style="margin-top:0.5rem;font-size:0.78rem;color:var(--text2);">Answered: <b style="color:var(--green);">{answered_count}</b> / {total}</div>', unsafe_allow_html=True)
            if st.button("🏁 Submit Exam", key="exam_submit", use_container_width=True, type="primary"):
                st.session_state.quiz_done = True
                st.session_state.score = sum(1 for a in st.session_state.answers.values() if a.get("correct"))
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)


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
        t_secs = n * 72 if timed else 0
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

    # Auto-create demo account if it doesn't exist
    try:
        users = load_users()
        if "demo" not in users:
            register_user("demo", "demo123", "Demo Student")
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

    # Dev mode unlock via URL param
    if not st.session_state.dev_mode:
        params = st.query_params
        if params.get("dev") == DEVELOPER_PIN:
            st.session_state.dev_mode = True

    page = st.session_state.page

    # Pages that don't show topbar
    if page == "quiz" and (st.session_state.quiz_active or st.session_state.quiz_done):
        inject_styles()
        page_quiz()
        return

    topbar()

    if   page == "home":        page_home()
    elif page == "pyq":         page_pyq()
    elif page == "quiz":        page_quiz_config()
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
