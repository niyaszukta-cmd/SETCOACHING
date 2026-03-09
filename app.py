# ============================================================================
# NYZTrade UNIFIED GEX/DEX Dashboard - INDEX + STOCK OPTIONS
# Features: Weekly/Monthly Options | VANNA & CHARM | Gamma Flip Zones
#           Smart Caching | Volume Overlay | Volume Spike Detection
#           Significant GEX Classification (Addition vs Unwind)
# Supports: NIFTY, BANKNIFTY, FINNIFTY, MIDCPNIFTY + 30 F&O Stocks
# ============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.stats import norm
from datetime import datetime, timedelta
import pytz
import requests
import time
from dataclasses import dataclass
from typing import Optional, Dict, List, Tuple
import warnings
import hashlib
import json
import os
import pickle
from pathlib import Path
warnings.filterwarnings('ignore')

# ============================================================================
# PAGE CONFIG & STYLING
# ============================================================================

st.set_page_config(
    page_title="NYZTrade Unified - GEX & VANNA Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Space+Grotesk:wght@300;400;500;600;700&display=swap');

    header[data-testid="stHeader"] a[href*="github"] { display: none !important; }
    button[kind="header"][data-testid="baseButton-header"] svg { display: none !important; }
    a[aria-label*="GitHub"], a[aria-label*="github"], a[href*="github.com"] { display: none !important; }

    :root {
        --bg-primary: #0a0e17;
        --bg-secondary: #111827;
        --bg-card: #1a2332;
        --bg-card-hover: #232f42;
        --accent-green: #10b981;
        --accent-red: #ef4444;
        --accent-blue: #3b82f6;
        --accent-purple: #8b5cf6;
        --accent-yellow: #f59e0b;
        --accent-cyan: #06b6d4;
        --text-primary: #f1f5f9;
        --text-secondary: #94a3b8;
        --text-muted: #64748b;
        --border-color: #2d3748;
    }

    .stApp { background: linear-gradient(135deg, var(--bg-primary) 0%, #0f172a 50%, var(--bg-primary) 100%); }

    .main-header {
        background: linear-gradient(135deg, rgba(59,130,246,0.1) 0%, rgba(139,92,246,0.1) 100%);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 24px 32px;
        margin-bottom: 24px;
        backdrop-filter: blur(10px);
    }
    .main-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #3b82f6, #8b5cf6, #06b6d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    .sub-title { font-family: 'JetBrains Mono', monospace; color: var(--text-secondary); font-size: 0.9rem; margin-top: 8px; }

    .metric-card {
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 20px;
        transition: all 0.3s ease;
    }
    .metric-card:hover { background: var(--bg-card-hover); transform: translateY(-2px); box-shadow: 0 8px 25px rgba(0,0,0,0.3); }
    .metric-card.positive { border-left: 4px solid var(--accent-green); }
    .metric-card.negative { border-left: 4px solid var(--accent-red); }
    .metric-card.neutral  { border-left: 4px solid var(--accent-yellow); }

    .metric-label  { font-family: 'JetBrains Mono', monospace; color: var(--text-muted); font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 8px; }
    .metric-value  { font-family: 'Space Grotesk', sans-serif; font-size: 1.75rem; font-weight: 700; color: var(--text-primary); line-height: 1.2; }
    .metric-value.positive { color: var(--accent-green); }
    .metric-value.negative { color: var(--accent-red); }
    .metric-value.neutral  { color: var(--accent-yellow); }
    .metric-delta  { font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; margin-top: 8px; color: var(--text-secondary); }

    .live-indicator {
        display: inline-flex; align-items: center; gap: 8px; padding: 6px 14px;
        background: rgba(239,68,68,0.1); border: 1px solid rgba(239,68,68,0.3);
        border-radius: 20px; animation: pulse 2s ease-in-out infinite;
    }
    .live-dot { width: 8px; height: 8px; background: var(--accent-red); border-radius: 50%; animation: blink 1.5s ease-in-out infinite; }

    .index-badge {
        display: inline-flex; align-items: center; gap: 6px; padding: 4px 12px;
        background: rgba(139,92,246,0.2); border: 1px solid rgba(139,92,246,0.4);
        border-radius: 12px; color: #a78bfa; font-size: 0.75rem; font-weight: 600;
    }
    .stock-badge {
        display: inline-flex; align-items: center; gap: 6px; padding: 4px 12px;
        background: rgba(6,182,212,0.2); border: 1px solid rgba(6,182,212,0.4);
        border-radius: 12px; color: #22d3ee; font-size: 0.75rem; font-weight: 600;
    }
    .spike-legend {
        padding: 10px 16px;
        background: rgba(59,130,246,0.08);
        border: 1px solid rgba(59,130,246,0.25);
        border-radius: 10px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.78rem;
        color: #94a3b8;
        line-height: 1.8;
    }

    @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.7} }
    @keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.3} }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# CONFIGURATION
# ============================================================================

@dataclass
class DhanConfig:
    client_id: str = "1100480354"
    access_token: str = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzczMTIzMzQ3LCJhcHBfaWQiOiJhYjYxZmJmOSIsImlhdCI6MTc3MzAzNjk0NywidG9rZW5Db25zdW1lclR5cGUiOiJBUFAiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwMDQ4MDM1NCJ9.zWyVEoFpOamylRTTd_pXhiTHCcu7LEnQ412tGpoxuUfcsYijGKG-2ZHp4q1jYhZVhNIn17X8CXREmkefeKnBCg"

DHAN_INDEX_SECURITY_IDS = {
    "NIFTY": 13, "BANKNIFTY": 25, "FINNIFTY": 27, "MIDCPNIFTY": 442
}
DHAN_STOCK_SECURITY_IDS = {
    "RELIANCE": 2885, "TCS": 11536, "HDFCBANK": 1333, "INFY": 1594,
    "ICICIBANK": 4963, "SBIN": 3045, "BHARTIARTL": 1195, "ITC": 1660,
    "KOTAKBANK": 1922, "LT": 2980, "AXISBANK": 5900, "HINDUNILVR": 1394,
    "WIPRO": 3787, "MARUTI": 10999, "BAJFINANCE": 317, "HCLTECH": 7229,
    "ASIANPAINT": 157, "TITAN": 3506, "ULTRACEMCO": 11532, "SUNPHARMA": 3351,
    "TATAMOTORS": 3456, "TATASTEEL": 3499, "TECHM": 13538, "POWERGRID": 2752,
    "NTPC": 11630, "ONGC": 2475, "M&M": 2031, "BAJAJFINSV": 16675,
    "ADANIPORTS": 3718, "COALINDIA": 20374,
}

INDEX_CONFIG = {
    "NIFTY":      {"contract_size": 25,  "strike_interval": 50,  "type": "INDEX"},
    "BANKNIFTY":  {"contract_size": 15,  "strike_interval": 100, "type": "INDEX"},
    "FINNIFTY":   {"contract_size": 40,  "strike_interval": 50,  "type": "INDEX"},
    "MIDCPNIFTY": {"contract_size": 75,  "strike_interval": 25,  "type": "INDEX"},
}
STOCK_CONFIG = {
    "RELIANCE":   {"lot_size": 250,  "strike_interval": 10,  "type": "STOCK"},
    "TCS":        {"lot_size": 150,  "strike_interval": 25,  "type": "STOCK"},
    "HDFCBANK":   {"lot_size": 550,  "strike_interval": 10,  "type": "STOCK"},
    "INFY":       {"lot_size": 300,  "strike_interval": 25,  "type": "STOCK"},
    "ICICIBANK":  {"lot_size": 550,  "strike_interval": 10,  "type": "STOCK"},
    "SBIN":       {"lot_size": 1500, "strike_interval": 5,   "type": "STOCK"},
    "BHARTIARTL": {"lot_size": 410,  "strike_interval": 10,  "type": "STOCK"},
    "ITC":        {"lot_size": 1600, "strike_interval": 5,   "type": "STOCK"},
    "KOTAKBANK":  {"lot_size": 400,  "strike_interval": 25,  "type": "STOCK"},
    "LT":         {"lot_size": 300,  "strike_interval": 25,  "type": "STOCK"},
    "AXISBANK":   {"lot_size": 600,  "strike_interval": 10,  "type": "STOCK"},
    "HINDUNILVR": {"lot_size": 300,  "strike_interval": 25,  "type": "STOCK"},
    "WIPRO":      {"lot_size": 1200, "strike_interval": 5,   "type": "STOCK"},
    "MARUTI":     {"lot_size": 75,   "strike_interval": 50,  "type": "STOCK"},
    "BAJFINANCE": {"lot_size": 125,  "strike_interval": 50,  "type": "STOCK"},
    "HCLTECH":    {"lot_size": 350,  "strike_interval": 25,  "type": "STOCK"},
    "ASIANPAINT": {"lot_size": 300,  "strike_interval": 25,  "type": "STOCK"},
    "TITAN":      {"lot_size": 300,  "strike_interval": 25,  "type": "STOCK"},
    "ULTRACEMCO": {"lot_size": 100,  "strike_interval": 50,  "type": "STOCK"},
    "SUNPHARMA":  {"lot_size": 400,  "strike_interval": 25,  "type": "STOCK"},
    "TATAMOTORS": {"lot_size": 1250, "strike_interval": 5,   "type": "STOCK"},
    "TATASTEEL":  {"lot_size": 900,  "strike_interval": 5,   "type": "STOCK"},
    "TECHM":      {"lot_size": 400,  "strike_interval": 25,  "type": "STOCK"},
    "POWERGRID":  {"lot_size": 1800, "strike_interval": 5,   "type": "STOCK"},
    "NTPC":       {"lot_size": 2250, "strike_interval": 5,   "type": "STOCK"},
    "ONGC":       {"lot_size": 2475, "strike_interval": 5,   "type": "STOCK"},
    "M&M":        {"lot_size": 300,  "strike_interval": 25,  "type": "STOCK"},
    "BAJAJFINSV": {"lot_size": 500,  "strike_interval": 10,  "type": "STOCK"},
    "ADANIPORTS": {"lot_size": 250,  "strike_interval": 25,  "type": "STOCK"},
    "COALINDIA":  {"lot_size": 2040, "strike_interval": 5,   "type": "STOCK"},
}
SYMBOL_CONFIG = {**INDEX_CONFIG, **STOCK_CONFIG}
STOCK_CATEGORIES = {
    "Banking & Finance": ["HDFCBANK","ICICIBANK","SBIN","KOTAKBANK","AXISBANK","BAJFINANCE","BAJAJFINSV"],
    "IT & Technology":   ["TCS","INFY","WIPRO","HCLTECH","TECHM"],
    "Energy & Power":    ["RELIANCE","ONGC","POWERGRID","NTPC","COALINDIA"],
    "Auto & Industrial": ["MARUTI","TATAMOTORS","M&M","LT"],
    "FMCG & Consumer":   ["HINDUNILVR","ITC","ASIANPAINT","TITAN"],
    "Others":            ["SUNPHARMA","TATASTEEL","BHARTIARTL","ADANIPORTS","ULTRACEMCO"],
}

IST = pytz.timezone('Asia/Kolkata')
MARKET_OPEN_HOUR, MARKET_OPEN_MINUTE   = 9,  15
MARKET_CLOSE_HOUR, MARKET_CLOSE_MINUTE = 15, 30

# ============================================================================
# CACHE MANAGER
# ============================================================================

class CacheManager:
    def __init__(self):
        self.cache_dir = "/tmp/nyztrade_unified_cache"
        os.makedirs(self.cache_dir, exist_ok=True)

    def _generate_cache_key(self, symbol, date, strikes, interval, expiry_code, expiry_flag, instrument_type):
        key_data = f"{symbol}_{date}_{sorted(strikes)}_{interval}_{expiry_code}_{expiry_flag}_{instrument_type}"
        return hashlib.md5(key_data.encode()).hexdigest()

    def _get_cache_path(self, cache_key): return os.path.join(self.cache_dir, f"{cache_key}.pkl")
    def _get_meta_path(self, cache_key): return os.path.join(self.cache_dir, f"{cache_key}_meta.json")

    def is_current_trading_day(self, target_date):
        return datetime.strptime(target_date, '%Y-%m-%d').date() == datetime.now(IST).date()

    def is_market_hours(self):
        now = datetime.now(IST)
        open_t  = now.replace(hour=MARKET_OPEN_HOUR,  minute=MARKET_OPEN_MINUTE,  second=0, microsecond=0)
        close_t = now.replace(hour=MARKET_CLOSE_HOUR, minute=MARKET_CLOSE_MINUTE, second=0, microsecond=0)
        return open_t <= now <= close_t

    def get_cached_data(self, symbol, date, strikes, interval, expiry_code, expiry_flag, instrument_type):
        cache_key  = self._generate_cache_key(symbol, date, strikes, interval, expiry_code, expiry_flag, instrument_type)
        cache_path = self._get_cache_path(cache_key)
        meta_path  = self._get_meta_path(cache_key)
        if not os.path.exists(cache_path) or not os.path.exists(meta_path):
            return None, None, None
        try:
            df = pd.read_pickle(cache_path)
            with open(meta_path) as f:
                meta = json.load(f)
            last_ts = df['timestamp'].max() if len(df) > 0 and 'timestamp' in df.columns else None
            if isinstance(last_ts, str):
                last_ts = pd.to_datetime(last_ts)
            return df, meta, last_ts
        except Exception as e:
            st.warning(f"Cache read error: {e}")
            return None, None, None

    def save_to_cache(self, df, meta, symbol, date, strikes, interval, expiry_code, expiry_flag, instrument_type):
        cache_key  = self._generate_cache_key(symbol, date, strikes, interval, expiry_code, expiry_flag, instrument_type)
        try:
            df.to_pickle(self._get_cache_path(cache_key))
            with open(self._get_meta_path(cache_key), 'w') as f:
                json.dump(meta, f)
        except Exception as e:
            st.warning(f"Cache write error: {e}")

    def merge_incremental_data(self, cached_df, new_df):
        if cached_df is None or len(cached_df) == 0: return new_df
        if new_df is None or len(new_df) == 0: return cached_df
        combined = pd.concat([cached_df, new_df], ignore_index=True)
        combined = combined.drop_duplicates(subset=['timestamp','strike'], keep='last')
        return combined.sort_values(['timestamp','strike']).reset_index(drop=True)

    def clear_cache(self, symbol=None, date=None):
        try:
            for f in os.listdir(self.cache_dir):
                fp = os.path.join(self.cache_dir, f)
                if symbol is None and date is None:
                    os.remove(fp)
                elif f.startswith(f"{symbol}_{date}"):
                    os.remove(fp)
        except Exception as e:
            st.warning(f"Cache clear error: {e}")

    def get_cache_stats(self):
        try:
            files = [f for f in os.listdir(self.cache_dir) if f.endswith('.pkl')]
            size  = sum(os.path.getsize(os.path.join(self.cache_dir, f)) for f in files)
            return {'num_entries': len(files), 'total_size_mb': size / (1024*1024)}
        except:
            return {'num_entries': 0, 'total_size_mb': 0}

cache_manager = CacheManager()

# ============================================================================
# BLACK-SCHOLES CALCULATOR
# ============================================================================

class BlackScholesCalculator:
    @staticmethod
    def calculate_d1(S, K, T, r, sigma):
        if T <= 0 or sigma <= 0: return 0
        return (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma * np.sqrt(T))

    @staticmethod
    def calculate_d2(S, K, T, r, sigma):
        if T <= 0 or sigma <= 0: return 0
        return BlackScholesCalculator.calculate_d1(S, K, T, r, sigma) - sigma * np.sqrt(T)

    @staticmethod
    def calculate_gamma(S, K, T, r, sigma):
        if T <= 0 or sigma <= 0 or S <= 0 or K <= 0: return 0
        try:
            d1 = BlackScholesCalculator.calculate_d1(S, K, T, r, sigma)
            return norm.pdf(d1) / (S * sigma * np.sqrt(T))
        except: return 0

    @staticmethod
    def calculate_call_delta(S, K, T, r, sigma):
        if T <= 0 or sigma <= 0 or S <= 0 or K <= 0: return 0
        try: return norm.cdf(BlackScholesCalculator.calculate_d1(S, K, T, r, sigma))
        except: return 0

    @staticmethod
    def calculate_put_delta(S, K, T, r, sigma):
        if T <= 0 or sigma <= 0 or S <= 0 or K <= 0: return 0
        try: return norm.cdf(BlackScholesCalculator.calculate_d1(S, K, T, r, sigma)) - 1
        except: return 0

    @staticmethod
    def calculate_vanna(S, K, T, r, sigma):
        if T <= 0 or sigma <= 0 or S <= 0 or K <= 0: return 0
        try:
            d1 = BlackScholesCalculator.calculate_d1(S, K, T, r, sigma)
            d2 = BlackScholesCalculator.calculate_d2(S, K, T, r, sigma)
            return -norm.pdf(d1) * d2 / sigma
        except: return 0

    @staticmethod
    def calculate_charm(S, K, T, r, sigma, option_type='call'):
        if T <= 0 or sigma <= 0 or S <= 0 or K <= 0: return 0
        try:
            d1 = BlackScholesCalculator.calculate_d1(S, K, T, r, sigma)
            d2 = BlackScholesCalculator.calculate_d2(S, K, T, r, sigma)
            return -norm.pdf(d1) * (2*r*T - d2*sigma*np.sqrt(T)) / (2*T*sigma*np.sqrt(T))
        except: return 0

# ============================================================================
# GAMMA FLIP ZONE CALCULATOR
# ============================================================================

def identify_gamma_flip_zones(df: pd.DataFrame, spot_price: float) -> List[Dict]:
    df_sorted = df.sort_values('strike').reset_index(drop=True)
    flip_zones = []
    for i in range(len(df_sorted) - 1):
        cur_gex  = df_sorted.iloc[i]['net_gex']
        nxt_gex  = df_sorted.iloc[i+1]['net_gex']
        cur_str  = df_sorted.iloc[i]['strike']
        nxt_str  = df_sorted.iloc[i+1]['strike']
        if (cur_gex > 0 and nxt_gex < 0) or (cur_gex < 0 and nxt_gex > 0):
            flip_str = cur_str + (nxt_str - cur_str) * (abs(cur_gex) / (abs(cur_gex) + abs(nxt_gex)))
            if spot_price < flip_str:
                direction, arrow, color = ("upward","↑","#ef4444") if cur_gex > 0 else ("downward","↓","#10b981")
            else:
                direction, arrow, color = ("downward","↓","#10b981") if cur_gex < 0 else ("upward","↑","#ef4444")
            flip_zones.append({
                'strike': flip_str, 'lower_strike': cur_str, 'upper_strike': nxt_str,
                'lower_gex': cur_gex, 'upper_gex': nxt_gex,
                'direction': direction, 'arrow': arrow, 'color': color,
                'flip_type': 'Positive→Negative' if cur_gex > 0 else 'Negative→Positive',
            })
    return flip_zones

# ============================================================================
# VOLUME OVERLAY HELPERS
# ============================================================================

def _add_volume_overlay_horizontal(fig, df_sorted: pd.DataFrame):
    if 'call_volume' not in df_sorted.columns or 'put_volume' not in df_sorted.columns:
        return fig
    fig.add_trace(go.Bar(
        y=df_sorted['strike'], x=df_sorted['call_volume'].fillna(0),
        orientation='h', name='Call Volume',
        marker=dict(color='rgba(16,185,129,0.22)', line=dict(width=0)),
        xaxis='x2',
        hovertemplate='Strike: %{y:,.0f}<br>Call Vol: %{x:,.0f}<extra></extra>',
        showlegend=True, legendgroup='volume',
    ))
    fig.add_trace(go.Bar(
        y=df_sorted['strike'], x=df_sorted['put_volume'].fillna(0),
        orientation='h', name='Put Volume',
        marker=dict(color='rgba(239,68,68,0.22)', line=dict(width=0)),
        xaxis='x3',
        hovertemplate='Strike: %{y:,.0f}<br>Put Vol: %{x:,.0f}<extra></extra>',
        showlegend=True, legendgroup='volume',
    ))
    return fig

def _configure_volume_xaxis2(fig, df_sorted: pd.DataFrame):
    PADDING = 4.5
    max_call = max(df_sorted['call_volume'].fillna(0).max() if 'call_volume' in df_sorted.columns else 1, 1)
    max_put  = max(df_sorted['put_volume'].fillna(0).max()  if 'put_volume'  in df_sorted.columns else 1, 1)
    fig.update_layout(
        xaxis2=dict(overlaying='x', side='top', title='Call Vol', range=[0, max_call*PADDING],
                    showgrid=False, showline=False, zeroline=False,
                    tickfont=dict(color='rgba(16,185,129,0.65)',size=9),
                    title_font=dict(color='rgba(16,185,129,0.65)',size=10),
                    color='rgba(16,185,129,0.65)'),
        xaxis3=dict(overlaying='x', side='top', title='Put Vol', range=[0, max_put*PADDING],
                    showgrid=False, showline=False, zeroline=False,
                    tickfont=dict(color='rgba(239,68,68,0.65)',size=9),
                    title_font=dict(color='rgba(239,68,68,0.65)',size=10),
                    color='rgba(239,68,68,0.65)'),
    )
    return fig

# ============================================================================
# VOLUME SPIKE DETECTION
# ============================================================================

def detect_volume_spikes(timeline_df: pd.DataFrame,
                          z_threshold: float = 2.0,
                          rolling_window: int = 5) -> pd.DataFrame:
    """
    Detects volume spikes and GEX shift events on the intraday timeline.
    Uses a hybrid z-score: rolling(15 bars) with global session baseline fallback.

    Added columns:
      vol_spike, call_vol_spike, put_vol_spike  – bool flags
      vol_z_score, call_vol_z, put_vol_z        – standardised z-scores
      gex_change, gex_z_score, gex_shift_spike  – GEX rate-of-change analysis
      spike_type       – CALL_DOMINANT | PUT_DOMINANT | MIXED | ''
      spike_strength   – EXTREME | STRONG | MODERATE | ''
      gex_confirmation – CONFIRMED_BULLISH | CONFIRMED_BEARISH | DIVERGENCE | UNCONFIRMED
      event_label      – short icon + strength label for chart annotation
    """
    df = timeline_df.copy().sort_values('timestamp').reset_index(drop=True)

    def _z_score(series: pd.Series, window: int) -> pd.Series:
        # Trimmed baseline: exclude top 10% so spike rows don't inflate
        # the mean/std and dilute their own z-score
        q90      = series.quantile(0.90)
        baseline = series[series <= q90]
        g_mean   = baseline.mean() if len(baseline) > 0 else series.mean()
        g_std    = baseline.std()  if len(baseline) > 1 else series.std()
        g_std    = g_std if g_std > 0 else 1.0
        r_mean   = series.rolling(window, min_periods=max(3, window // 2)).mean()
        r_std    = series.rolling(window, min_periods=max(3, window // 2)).std()
        # Fill early NaNs and zero-std periods with trimmed global baseline
        r_mean   = r_mean.fillna(g_mean)
        r_std    = r_std.fillna(g_std).replace(0, g_std)
        return (series - r_mean) / r_std

    LONG_WINDOW = max(rolling_window * 3, 15)

    df['vol_z_score'] = _z_score(df['total_volume'], LONG_WINDOW)
    df['call_vol_z']  = _z_score(df['call_volume'],  LONG_WINDOW)
    df['put_vol_z']   = _z_score(df['put_volume'],   LONG_WINDOW)

    df['vol_spike']      = df['vol_z_score']  > z_threshold
    df['call_vol_spike'] = df['call_vol_z']   > z_threshold
    df['put_vol_spike']  = df['put_vol_z']    > z_threshold

    df['gex_change']      = df['net_gex'].diff().fillna(0)
    # Use the same trimmed z-score for GEX changes so that sessions
    # with uniformly tiny GEX moves don't suppress the spike flag
    df['gex_z_score']     = _z_score(df['gex_change'].abs(), LONG_WINDOW)
    df['gex_shift_spike'] = df['gex_z_score'] > z_threshold

    spike_types, spike_strengths, gex_confirmations, event_labels = [], [], [], []

    for _, row in df.iterrows():
        z        = row['vol_z_score']
        czz      = row['call_vol_z']
        pzz      = row['put_vol_z']
        is_spike = bool(row['vol_spike'])

        strength = '' if not is_spike else ('EXTREME' if z > 4.0 else ('STRONG' if z > 3.0 else 'MODERATE'))
        # Use actual call/put volume ratio for dominance — more reliable
        # than comparing z-scores which share a common distorted baseline
        if not is_spike:
            stype = ''
        else:
            cv_raw = row.get('call_volume', 0)
            pv_raw = row.get('put_volume',  0)
            ratio  = cv_raw / (pv_raw + 1)   # +1 avoids division by zero
            if   ratio > 1.5:  stype = 'CALL_DOMINANT'
            elif ratio < 0.67: stype = 'PUT_DOMINANT'
            else:              stype = 'MIXED'

        gex_up      = row['gex_change'] > 0
        gex_down    = row['gex_change'] < 0
        gex_sig     = bool(row['gex_shift_spike'])
        gex_moving  = row['gex_change'] != 0

        if not is_spike:
            gex_conf = 'UNCONFIRMED'
        # Confirmed: volume direction AND GEX direction agree + GEX move is significant
        elif stype == 'CALL_DOMINANT' and gex_up and gex_sig:
            gex_conf = 'CONFIRMED_BULLISH'
        elif stype == 'PUT_DOMINANT' and gex_down and gex_sig:
            gex_conf = 'CONFIRMED_BEARISH'
        # Divergence: volume direction CONFLICTS with GEX direction.
        # Does NOT require gex_sig — direction conflict alone is enough.
        # Also catches MIXED spikes where GEX is repositioning hard.
        elif stype == 'CALL_DOMINANT' and gex_down and gex_moving:
            gex_conf = 'DIVERGENCE'
        elif stype == 'PUT_DOMINANT' and gex_up and gex_moving:
            gex_conf = 'DIVERGENCE'
        elif stype == 'MIXED' and abs(row['gex_z_score']) > z_threshold * 0.75:
            # Both sides spiking + any meaningful GEX repositioning = split market, divergent flow.
            # Use a lower GEX threshold for MIXED (75% of main threshold) because the volume
            # signal itself is already ambiguous — any dealer move is meaningful here.
            gex_conf = 'DIVERGENCE'
        else:
            gex_conf = 'UNCONFIRMED'

        label = '' if not is_spike else (
            {'CONFIRMED_BULLISH':'🚀','CONFIRMED_BEARISH':'💥','DIVERGENCE':'⚠️','UNCONFIRMED':'📊'}.get(gex_conf,'📊')
            + f" {strength[:3]}"
        )

        spike_types.append(stype)
        spike_strengths.append(strength)
        gex_confirmations.append(gex_conf)
        event_labels.append(label)

    df['spike_type']       = spike_types
    df['spike_strength']   = spike_strengths
    df['gex_confirmation'] = gex_confirmations
    df['event_label']      = event_labels

    return df


def _action_hint(row) -> str:
    conf       = row['gex_confirmation']
    stype      = row['spike_type']
    gex_change = row.get('gex_change', 0)
    if conf == 'CONFIRMED_BULLISH':
        return '🟢 Watch for squeeze up'
    if conf == 'CONFIRMED_BEARISH':
        return '🔴 Watch for squeeze down'
    if conf == 'DIVERGENCE':
        # Be explicit about which side is conflicting
        if stype == 'CALL_DOMINANT':
            return '⚠️ Calls bought but GEX falling — dealers fading buyers, watch for failed breakout'
        if stype == 'PUT_DOMINANT':
            return '⚠️ Puts bought but GEX rising — bear trap risk, watch for squeeze up'
        if stype == 'MIXED':
            dir_str = 'rising' if gex_change > 0 else 'falling'
            return f'⚠️ Mixed vol spike + GEX {dir_str} hard — split market, resolution pending'
        return '⚠️ Conflicting signals — wait for clarity'
    if stype == 'CALL_DOMINANT':    return '🟡 Call accumulation (unconfirmed by GEX)'
    if stype == 'PUT_DOMINANT':     return '🟡 Put accumulation (unconfirmed by GEX)'
    return '⬜ Monitor'


def build_spike_summary(df_spikes: pd.DataFrame, unit_label: str = "B") -> pd.DataFrame:
    spikes = df_spikes[df_spikes['vol_spike']].copy()
    if spikes.empty:
        return pd.DataFrame()
    rows = []
    for _, r in spikes.iterrows():
        rows.append({
            'Time'               : r['timestamp'].strftime('%H:%M'),
            'Spike Type'         : r['spike_type'],
            'Strength'           : r['spike_strength'],
            'GEX Signal'         : r['gex_confirmation'],
            'Vol Z-Score'        : f"{r['vol_z_score']:.1f}σ",
            'Call Vol'           : f"{r.get('call_volume',0):,.0f}",
            'Put Vol'            : f"{r.get('put_volume',0):,.0f}",
            'Total Vol'          : f"{r.get('total_volume',0):,.0f}",
            f'GEX Δ ({unit_label})': f"{r['gex_change']:+.4f}",
            'Spot'               : f"₹{r.get('spot_price',0):,.2f}",
            'Action'             : _action_hint(r),
        })
    return pd.DataFrame(rows)

# ============================================================================
# INTRADAY TIMELINE WITH VOLUME SPIKE DETECTION  (replaces old version)
# ============================================================================

def create_vanna_spike_panel(
    df: pd.DataFrame,
    unit_label: str = "B",
    z_threshold: float = 2.0,
) -> Tuple[go.Figure, pd.DataFrame]:
    """
    Compact 2-row spike panel for the VANNA overlay tab.
      Row 1 — Volume Z-Score bars + Net VANNA flow line (secondary y)
      Row 2 — Spike event markers coloured by GEX confirmation type
    """
    agg_cols = {k: v for k, v in {
        'net_gex'    : 'sum', 'net_vanna'   : 'sum',
        'spot_price' : 'first',
        'call_volume': 'sum', 'put_volume'  : 'sum', 'total_volume': 'sum',
    }.items() if k in df.columns}

    timeline_df = (df.groupby('timestamp').agg(agg_cols)
                     .reset_index().sort_values('timestamp'))
    df_spikes   = detect_volume_spikes(timeline_df, z_threshold=z_threshold)
    ts          = df_spikes['timestamp']

    spike_rows = df_spikes[df_spikes['vol_spike']]
    n_spikes   = len(spike_rows)
    n_bull = (spike_rows['gex_confirmation'] == 'CONFIRMED_BULLISH').sum()
    n_bear = (spike_rows['gex_confirmation'] == 'CONFIRMED_BEARISH').sum()
    n_div  = (spike_rows['gex_confirmation'] == 'DIVERGENCE').sum()

    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        subplot_titles=(
            'Volume Z-Score  ·  Net VANNA flow (secondary axis)',
            'Spike Events  (shape & colour = GEX confirmation type)',
        ),
        vertical_spacing=0.08,
        row_heights=[0.52, 0.48],
        specs=[[{"secondary_y": True}],
               [{"secondary_y": False}]],
    )

    # ── Row 1: Z-score bars ───────────────────────────────────────────────
    z_colors = [
        '#dc2626' if z > 4.0 else
        '#ef4444' if z > 3.0 else
        '#f59e0b' if z > z_threshold else
        '#334155'
        for z in df_spikes['vol_z_score']
    ]
    fig.add_trace(go.Bar(
        x=ts, y=df_spikes['vol_z_score'].clip(lower=0),
        marker_color=z_colors, name='Volume Z-Score',
        hovertemplate='%{x|%H:%M}<br>Z-Score: %{y:.2f}σ<extra></extra>',
    ), row=1, col=1, secondary_y=False)

    for level, color, label in [
        (z_threshold, 'rgba(245,158,11,0.75)', f'Threshold ({z_threshold:.1f}σ)'),
        (3.0,         'rgba(239,68,68,0.50)',  'Strong (3σ)'),
        (4.0,         'rgba(220,38,38,0.70)',  'Extreme (4σ)'),
    ]:
        fig.add_hline(y=level, line_dash='dash', line_color=color, line_width=1.5,
                      annotation_text=label, annotation_position='top right',
                      annotation=dict(font=dict(color=color, size=9)), row=1, col=1)

    # Net VANNA on secondary y — spike + VANNA surge = institutional move
    if 'net_vanna' in df_spikes.columns:
        mv_colors = ['rgba(16,185,129,0.8)' if v > 0 else 'rgba(239,68,68,0.8)'
                     for v in df_spikes['net_vanna']]
        fig.add_trace(go.Scatter(
            x=ts, y=df_spikes['net_vanna'],
            mode='lines+markers',
            line=dict(color='rgba(6,182,212,0.7)', width=1.5, dash='dot'),
            marker=dict(size=4, color=mv_colors),
            fill='tozeroy', fillcolor='rgba(6,182,212,0.05)',
            name='Net VANNA flow',
            hovertemplate='%{x|%H:%M}<br>Net VANNA: %{y:.4f}<extra></extra>',
        ), row=1, col=1, secondary_y=True)

    # Coloured spike vlines into row 1
    for _, sr in spike_rows.iterrows():
        vc = {'CONFIRMED_BULLISH':'rgba(16,185,129,0.25)',
              'CONFIRMED_BEARISH':'rgba(239,68,68,0.25)',
              'DIVERGENCE'       :'rgba(245,158,11,0.20)',
              'UNCONFIRMED'      :'rgba(139,92,246,0.15)'}.get(sr['gex_confirmation'],'rgba(255,255,255,0.1)')
        fig.add_vline(x=sr['timestamp'].timestamp()*1000,
                      line_dash='dot', line_color=vc, line_width=1.5, row=1, col=1)

    # ── Row 2: Spike event markers ────────────────────────────────────────
    CONF_STYLE = {
        'CONFIRMED_BULLISH': ('#10b981', 'triangle-up',   18, '🚀 Confirmed Bullish'),
        'CONFIRMED_BEARISH': ('#ef4444', 'triangle-down', 18, '💥 Confirmed Bearish'),
        'DIVERGENCE':        ('#f59e0b', 'diamond',       16, '⚠️ Divergence'),
        'UNCONFIRMED':       ('#8b5cf6', 'circle',        12, '📊 Unconfirmed'),
    }
    for conf_key, (color, symbol, size, legend_name) in CONF_STYLE.items():
        mask = df_spikes['vol_spike'] & (df_spikes['gex_confirmation'] == conf_key)
        sub  = df_spikes[mask]
        if sub.empty: continue
        fig.add_trace(go.Scatter(
            x=sub['timestamp'], y=sub['vol_z_score'].clip(upper=6),
            mode='markers+text',
            marker=dict(symbol=symbol, size=size, color=color,
                        line=dict(color='white', width=1.5)),
            text=sub['event_label'], textposition='top center',
            textfont=dict(color='white', size=9),
            name=legend_name,
            customdata=np.stack([
                sub['spike_type'].values,
                sub['spike_strength'].values,
                sub.get('call_volume', pd.Series([0]*len(sub))).values,
                sub.get('put_volume',  pd.Series([0]*len(sub))).values,
                sub['gex_change'].values,
            ], axis=-1),
            hovertemplate=(
                '%{x|%H:%M}<br>Type: %{customdata[0]}<br>'
                'Strength: %{customdata[1]}<br>'
                'Call Vol: %{customdata[2]:,.0f}<br>'
                'Put Vol: %{customdata[3]:,.0f}<br>'
                f'GEX Δ: %{{customdata[4]:+.4f}}{unit_label}<extra></extra>'
            ),
        ), row=2, col=1)

    fig.add_hline(y=z_threshold, line_dash='dash',
                  line_color='rgba(245,158,11,0.4)', line_width=1, row=2, col=1)

    # ── Layout ────────────────────────────────────────────────────────────
    if n_spikes:
        summary = f"🚀 {n_bull} Bull · 💥 {n_bear} Bear · ⚠️ {n_div} Divergence"
    else:
        summary = "No spikes detected at current threshold"

    fig.update_layout(
        title=dict(
            text=(
                f'<b>⚡ Volume Spike × VANNA Coincidence</b>  '
                f'<span style="font-size:12px;color:#94a3b8;">({n_spikes} spikes — {summary})</span><br>'
                f'<sub>'
                f'🚀 Call spike + GEX ↑ = Bullish confirmed  |  '
                f'💥 Put spike + GEX ↓ = Bearish confirmed  |  '
                f'⚠️ Conflict = Divergence  |  '
                f'Cyan dashed = Net VANNA (spike + VANNA surge = institutional conviction)'
                f'</sub>'
            ),
            font=dict(size=13, color='white'),
        ),
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(26,35,50,0.8)',
        height=430,
        barmode='overlay',
        hovermode='x unified',
        legend=dict(
            orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1,
            font=dict(color='white', size=10),
            bgcolor='rgba(0,0,0,0.7)',
            bordercolor='rgba(255,255,255,0.2)', borderwidth=1,
        ),
        margin=dict(l=60, r=60, t=110, b=40),
        dragmode='drawline',
        newshape=dict(line=dict(color='#f59e0b', width=2)),
    )
    fig.update_layout(
        modebar_add=['drawline','drawopenpath','drawcircle','drawrect','eraseshape'],
        modebar=dict(bgcolor='rgba(0,0,0,0.5)', color='#94a3b8', activecolor='#f59e0b'),
    )
    fig.update_yaxes(title_text='Z-Score (σ)',   row=1, col=1, secondary_y=False,
                     gridcolor='rgba(128,128,128,0.15)', range=[0, None])
    fig.update_yaxes(title_text='Net VANNA',     row=1, col=1, secondary_y=True,
                     showgrid=False, zeroline=True,
                     zerolinecolor='rgba(6,182,212,0.3)', zerolinewidth=1)
    fig.update_yaxes(title_text='Spike Z-Score', row=2, col=1,
                     gridcolor='rgba(128,128,128,0.15)', range=[0, None])
    fig.update_xaxes(title_text='Time (IST)',    row=2, col=1)

    return fig, df_spikes


def create_intraday_timeline_with_spikes(df: pd.DataFrame,
                                          unit_label: str = "B",
                                          z_threshold: float = 2.0) -> Tuple[go.Figure, pd.DataFrame]:
    """
    5-row intraday chart:
      Row 1 – Net GEX bars  +  |GEX Δ| rate line (secondary y)
      Row 2 – Spot price area
      Row 3 – Call / Put volume stacked bars  +  total volume line
      Row 4 – Volume Z-Score with severity bands
      Row 5 – Spike event markers, colour-coded by GEX confirmation
    Returns (fig, df_spikes)
    """
    agg_cols = {k: v for k, v in {
        'net_gex': 'sum', 'net_dex': 'sum', 'spot_price': 'first',
        'call_volume': 'sum', 'put_volume': 'sum', 'total_volume': 'sum',
    }.items() if k in df.columns}

    timeline_df = (df.groupby('timestamp').agg(agg_cols)
                     .reset_index().sort_values('timestamp'))

    df_spikes = detect_volume_spikes(timeline_df, z_threshold=z_threshold)

    fig = make_subplots(
        rows=5, cols=1,
        shared_xaxes=True,
        subplot_titles=(
            f'Net GEX ({unit_label})  +  GEX Δ Rate',
            'Spot Price',
            'Call vs Put Volume',
            'Volume Z-Score  (spike sensitivity threshold shown as dashed line)',
            'Spike Events  (shape & colour = GEX confirmation type)',
        ),
        vertical_spacing=0.04,
        row_heights=[0.26, 0.15, 0.22, 0.18, 0.19],
        specs=[[{"secondary_y": True}],[{"secondary_y": False}],
               [{"secondary_y": False}],[{"secondary_y": False}],
               [{"secondary_y": False}]],
    )

    ts = df_spikes['timestamp']

    # ── Row 1: GEX bars + |GEX Δ| secondary line ────────────────────────────
    gex_colors = ['#10b981' if v > 0 else '#ef4444' for v in df_spikes['net_gex']]
    fig.add_trace(go.Bar(
        x=ts, y=df_spikes['net_gex'], marker_color=gex_colors,
        name='Net GEX', showlegend=True,
        hovertemplate=f'%{{x|%H:%M}}<br>GEX: %{{y:.4f}}{unit_label}<extra></extra>',
    ), row=1, col=1, secondary_y=False)

    fig.add_trace(go.Scatter(
        x=ts, y=df_spikes['gex_change'].abs(),
        mode='lines', line=dict(color='rgba(245,158,11,0.8)', width=1.5, dash='dot'),
        fill='tozeroy', fillcolor='rgba(245,158,11,0.07)',
        name='|GEX Δ| rate', showlegend=True,
        hovertemplate=f'%{{x|%H:%M}}<br>|GEX Δ|: %{{y:.4f}}{unit_label}<extra></extra>',
    ), row=1, col=1, secondary_y=True)

    # ── Row 2: Spot price ────────────────────────────────────────────────────
    fig.add_trace(go.Scatter(
        x=ts, y=df_spikes['spot_price'],
        mode='lines', line=dict(color='#3b82f6', width=2),
        fill='tozeroy', fillcolor='rgba(59,130,246,0.07)',
        name='Spot Price', showlegend=True,
        hovertemplate='%{x|%H:%M}<br>₹%{y:,.2f}<extra></extra>',
    ), row=2, col=1)

    # subtle vertical lines at spike timestamps crossing into spot row
    for _, sr in df_spikes[df_spikes['vol_spike']].iterrows():
        fig.add_vline(x=sr['timestamp'].timestamp()*1000,
                      line_dash='dot', line_color='rgba(255,255,255,0.05)',
                      line_width=1, row=2, col=1)

    # ── Row 3: Call / Put volume stacked + total line ────────────────────────
    fig.add_trace(go.Bar(
        x=ts, y=df_spikes['call_volume'],
        name='Call Volume', marker=dict(color='rgba(16,185,129,0.70)', line=dict(width=0)),
        hovertemplate='%{x|%H:%M}<br>Call Vol: %{y:,.0f}<extra></extra>', showlegend=True,
    ), row=3, col=1)
    fig.add_trace(go.Bar(
        x=ts, y=df_spikes['put_volume'],
        name='Put Volume', marker=dict(color='rgba(239,68,68,0.70)', line=dict(width=0)),
        hovertemplate='%{x|%H:%M}<br>Put Vol: %{y:,.0f}<extra></extra>', showlegend=True,
    ), row=3, col=1)
    fig.add_trace(go.Scatter(
        x=ts, y=df_spikes['total_volume'],
        mode='lines', line=dict(color='rgba(255,255,255,0.45)', width=1.5),
        name='Total Volume', showlegend=True,
        hovertemplate='%{x|%H:%M}<br>Total: %{y:,.0f}<extra></extra>',
    ), row=3, col=1)

    # ── Row 4: Z-score bars ──────────────────────────────────────────────────
    z_colors = ['#dc2626' if z > 4.0 else ('#ef4444' if z > 3.0 else ('#f59e0b' if z > 2.0 else '#64748b'))
                for z in df_spikes['vol_z_score']]
    fig.add_trace(go.Bar(
        x=ts, y=df_spikes['vol_z_score'].clip(lower=0),
        marker_color=z_colors,
        name='Volume Z-Score', showlegend=True,
        hovertemplate='%{x|%H:%M}<br>Z-Score: %{y:.2f}σ<extra></extra>',
    ), row=4, col=1)

    for level, color, label in [
        (z_threshold, 'rgba(245,158,11,0.75)', f'Threshold ({z_threshold}σ)'),
        (3.0,         'rgba(239,68,68,0.50)',  'Strong (3σ)'),
        (4.0,         'rgba(220,38,38,0.70)',  'Extreme (4σ)'),
    ]:
        fig.add_hline(y=level, line_dash='dash', line_color=color, line_width=1.5,
                      annotation_text=label, annotation_position='top right',
                      annotation=dict(font=dict(color=color, size=9)), row=4, col=1)

    # ── Row 5: Spike event markers ───────────────────────────────────────────
    CONF_STYLE = {
        'CONFIRMED_BULLISH': ('#10b981', 'triangle-up',   18, '🚀 Confirmed Bullish'),
        'CONFIRMED_BEARISH': ('#ef4444', 'triangle-down', 18, '💥 Confirmed Bearish'),
        'DIVERGENCE':        ('#f59e0b', 'diamond',       16, '⚠️ Divergence'),
        'UNCONFIRMED':       ('#8b5cf6', 'circle',        12, '📊 Unconfirmed'),
    }
    for conf_key, (color, symbol, size, legend_name) in CONF_STYLE.items():
        mask = df_spikes['vol_spike'] & (df_spikes['gex_confirmation'] == conf_key)
        sub  = df_spikes[mask]
        if sub.empty: continue
        fig.add_trace(go.Scatter(
            x=sub['timestamp'],
            y=sub['vol_z_score'].clip(upper=6),
            mode='markers+text',
            marker=dict(symbol=symbol, size=size, color=color, line=dict(color='white', width=1.5)),
            text=sub['event_label'],
            textposition='top center',
            textfont=dict(color='white', size=9),
            name=legend_name, showlegend=True,
            customdata=np.stack([
                sub['spike_type'].values,
                sub['spike_strength'].values,
                sub.get('call_volume', pd.Series([0]*len(sub))).values,
                sub.get('put_volume',  pd.Series([0]*len(sub))).values,
                sub['gex_change'].values,
            ], axis=-1),
            hovertemplate=(
                '%{x|%H:%M}<br>Type: %{customdata[0]}<br>Strength: %{customdata[1]}<br>'
                'Call Vol: %{customdata[2]:,.0f}<br>Put Vol: %{customdata[3]:,.0f}<br>'
                f'GEX Δ: %{{customdata[4]:+.4f}}{unit_label}<extra></extra>'
            ),
        ), row=5, col=1)

    fig.add_hline(y=z_threshold, line_dash='dash',
                  line_color='rgba(245,158,11,0.4)', line_width=1, row=5, col=1)

    # ── Layout ───────────────────────────────────────────────────────────────
    fig.update_layout(
        title=dict(
            text=(
                "<b>📈 Intraday Timeline — Volume Spike & GEX Overlay</b><br>"
                "<sub>🚀 Confirmed Bullish = Call spike + GEX rising | "
                "💥 Confirmed Bearish = Put spike + GEX falling | "
                "⚠️ Divergence = Volume & GEX conflict | "
                "📊 Unconfirmed = Volume spike, GEX flat | "
                "✏️ Use toolbar to draw</sub>"
            ),
            font=dict(size=15, color='white'),
        ),
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(26,35,50,0.8)',
        height=1180,
        barmode='stack',
        hovermode='x unified',
        legend=dict(
            orientation='h', yanchor='bottom', y=1.01, xanchor='right', x=1,
            font=dict(color='white', size=10),
            bgcolor='rgba(0,0,0,0.8)', bordercolor='rgba(255,255,255,0.2)', borderwidth=1,
        ),
        margin=dict(l=60, r=60, t=140, b=60),
        dragmode='drawline',
        newshape=dict(line=dict(color='#f59e0b', width=2)),
    )
    fig.update_layout(modebar_add=['drawline','drawopenpath','drawclosedpath','drawcircle','drawrect','eraseshape'],
                      modebar=dict(bgcolor='rgba(0,0,0,0.5)', color='#94a3b8', activecolor='#f59e0b'))

    fig.update_yaxes(title_text=f'GEX (₹{unit_label})',      row=1, col=1, secondary_y=False, gridcolor='rgba(128,128,128,0.15)')
    fig.update_yaxes(title_text=f'|GEX Δ| (₹{unit_label})',  row=1, col=1, secondary_y=True,  showgrid=False)
    fig.update_yaxes(title_text='Spot Price (₹)',             row=2, col=1, gridcolor='rgba(128,128,128,0.15)')
    fig.update_yaxes(title_text='Volume (contracts)',         row=3, col=1, gridcolor='rgba(128,128,128,0.15)')
    fig.update_yaxes(title_text='Z-Score (σ)',                row=4, col=1, gridcolor='rgba(128,128,128,0.15)', range=[0,None])
    fig.update_yaxes(title_text='Spike Z-Score',              row=5, col=1, gridcolor='rgba(128,128,128,0.15)', range=[0,None])
    fig.update_xaxes(title_text='Time (IST)',                 row=5, col=1)

    return fig, df_spikes

# ============================================================================
# SIGNIFICANT GEX CLASSIFICATION  (Addition vs Unwind)
# ============================================================================

def classify_gex_significance(df: pd.DataFrame, spot_price: float) -> pd.DataFrame:
    """
    Classifies each strike's GEX into:
      STRONG_ADD | STRONG_UNWIND | WEAK_ADD | WEAK_UNWIND | NOISE

    Significance Score = |ΔOI| × gamma × volume_weight × atm_weight
    """
    df = df.copy()
    OI_CHANGE_THRESHOLD_PCT = 0.02
    VOLUME_CONFIRM_PCT      = 0.15
    ATM_BAND_PCT            = 0.03

    total_call_vol = df['call_volume'].sum() if 'call_volume' in df.columns else 1
    total_put_vol  = df['put_volume'].sum()  if 'put_volume'  in df.columns else 1

    bs_calc = BlackScholesCalculator()
    r, tte  = 0.07, 7/365

    scores, categories = [], []

    for _, row in df.iterrows():
        spot   = row.get('spot_price', spot_price)
        strike = row['strike']
        call_oi_now    = row.get('call_oi', 0)
        put_oi_now     = row.get('put_oi', 0)
        call_oi_change = row.get('call_oi_change', 0)
        put_oi_change  = row.get('put_oi_change', 0)
        call_vol       = row.get('call_volume', 0)
        put_vol        = row.get('put_volume', 0)
        call_iv        = row.get('call_iv', 15)
        put_iv         = row.get('put_iv', 15)

        dist_pct   = abs(strike - spot) / spot
        atm_weight = np.exp(-dist_pct / ATM_BAND_PCT)

        call_vol_share = call_vol / total_call_vol if total_call_vol > 0 else 0
        put_vol_share  = put_vol  / total_put_vol  if total_put_vol  > 0 else 0
        vol_weight = 1 + (call_vol_share + put_vol_share) * 5

        call_iv_d = call_iv / 100 if call_iv > 1 else call_iv
        put_iv_d  = put_iv  / 100 if put_iv  > 1 else put_iv
        gamma = bs_calc.calculate_gamma(spot, strike, tte, r, (call_iv_d + put_iv_d) / 2)

        net_oi_change = call_oi_change - put_oi_change
        score = abs(net_oi_change) * gamma * vol_weight * atm_weight * spot**2
        scores.append(score)

        base_oi        = max(call_oi_now + put_oi_now, 1)
        oi_change_pct  = abs(net_oi_change) / base_oi
        is_meaningful  = oi_change_pct > OI_CHANGE_THRESHOLD_PCT
        is_vol_confirm = (call_vol_share > VOLUME_CONFIRM_PCT or put_vol_share > VOLUME_CONFIRM_PCT)
        is_near_atm    = dist_pct < ATM_BAND_PCT

        if net_oi_change > 0:
            cat = ('STRONG_ADD'   if is_meaningful and (is_vol_confirm or is_near_atm)
                   else 'WEAK_ADD' if is_meaningful else 'NOISE')
        elif net_oi_change < 0:
            cat = ('STRONG_UNWIND'   if is_meaningful and (is_vol_confirm or is_near_atm)
                   else 'WEAK_UNWIND' if is_meaningful else 'NOISE')
        else:
            cat = 'NOISE'
        categories.append(cat)

    df['significance_score'] = scores
    df['gex_category']       = categories
    max_score = max(scores) if max(scores) > 0 else 1
    df['significance_pct'] = df['significance_score'] / max_score * 100
    return df


def create_significant_gex_chart(df: pd.DataFrame, spot_price: float, unit_label: str = "B") -> Tuple[go.Figure, pd.DataFrame]:
    """
    Significant GEX chart that visually separates:
      STRONG_ADD     → Bright Green  (solid border)
      STRONG_UNWIND  → Bright Red    (solid border)
      WEAK_ADD       → Dim Green     (transparent)
      WEAK_UNWIND    → Dim Red       (transparent)
      NOISE          → Gray          (very transparent)
    Secondary axis shows Significance Score as a dotted line.
    Returns (fig, df_classified)
    """
    df_classified = classify_gex_significance(df, spot_price)
    df_sorted     = df_classified.sort_values('strike').reset_index(drop=True)
    flip_zones    = identify_gamma_flip_zones(df_sorted, spot_price)

    COLOR_MAP = {
        'STRONG_ADD'   : ('#10b981', 0.95, 2),
        'STRONG_UNWIND': ('#ef4444', 0.95, 2),
        'WEAK_ADD'     : ('#10b981', 0.30, 0),
        'WEAK_UNWIND'  : ('#ef4444', 0.30, 0),
        'NOISE'        : ('#64748b', 0.18, 0),
    }
    LABEL_MAP = {
        'STRONG_ADD'   : '🟢 Strong Addition  (High Significance)',
        'STRONG_UNWIND': '🔴 Strong Unwind    (High Significance)',
        'WEAK_ADD'     : '🟩 Weak Addition    (Low Significance)',
        'WEAK_UNWIND'  : '🟥 Weak Unwind      (Low Significance)',
        'NOISE'        : '⬜ Noise / Residual OI',
    }

    fig = go.Figure()

    for cat, (color, opacity, bw) in COLOR_MAP.items():
        sub = df_sorted[df_sorted['gex_category'] == cat]
        if sub.empty: continue
        fig.add_trace(go.Bar(
            y=sub['strike'], x=sub['net_gex'], orientation='h',
            name=LABEL_MAP[cat],
            marker=dict(color=color, opacity=opacity, line=dict(color='white', width=bw)),
            customdata=np.stack([
                sub['significance_pct'].values,
                sub.get('call_oi_change', pd.Series([0]*len(sub))).values,
                sub.get('put_oi_change',  pd.Series([0]*len(sub))).values,
                sub.get('total_volume',   pd.Series([0]*len(sub))).values,
            ], axis=-1),
            hovertemplate=(
                f'Strike: %{{y:,.0f}}<br>Net GEX: %{{x:.4f}}{unit_label}<br>'
                'Significance: %{customdata[0]:.1f}%<br>'
                'Call OI Δ: %{customdata[1]:,.0f}<br>'
                'Put OI Δ: %{customdata[2]:,.0f}<br>'
                'Volume: %{customdata[3]:,.0f}<extra></extra>'
            ),
        ))

    # Significance score line (secondary x)
    fig.add_trace(go.Scatter(
        y=df_sorted['strike'], x=df_sorted['significance_pct'],
        mode='lines+markers', name='Significance Score (%)',
        line=dict(color='#f59e0b', width=2, dash='dot'),
        marker=dict(size=5, color='#f59e0b'),
        xaxis='x4',
        hovertemplate='Strike: %{y:,.0f}<br>Score: %{x:.1f}%<extra></extra>',
    ))

    fig = _add_volume_overlay_horizontal(fig, df_sorted)

    fig.add_hline(y=spot_price, line_dash='dash', line_color='white', line_width=3,
                  annotation_text=f'Spot: {spot_price:,.2f}', annotation_position='top right',
                  annotation=dict(font=dict(size=12, color='white', family='Arial Black')))
    fig.add_vline(x=0, line_dash='dot', line_color='gray', line_width=2)

    for zone in flip_zones:
        fig.add_hline(y=zone['strike'], line_dash='dot',
                      line_color=zone['color'], line_width=2,
                      annotation_text=f"🔄 Flip {zone['arrow']} {zone['strike']:,.0f}",
                      annotation_position='left',
                      annotation=dict(font=dict(size=10, color=zone['color']),
                                      bgcolor='rgba(0,0,0,0.7)', bordercolor=zone['color'], borderwidth=1))
        fig.add_hrect(y0=zone['lower_strike'], y1=zone['upper_strike'],
                      fillcolor=zone['color'], opacity=0.05, line_width=0)

    fig.update_layout(
        title=dict(
            text=(
                '<b>🎯 Significant GEX: Addition vs Unwind Classification</b><br>'
                '<sub>🟢 Strong Add = OI↑ + Vol/ATM confirmed | 🔴 Strong Unwind = OI↓ + Vol/ATM confirmed | '
                'Dim = Low significance | ⬜ Noise | 🟡 dotted = Significance Score | ✏️ toolbar to draw</sub>'
            ),
            font=dict(size=15, color='white'),
        ),
        xaxis_title=f'GEX (₹ {unit_label})',
        yaxis_title='Strike Price',
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(26,35,50,0.8)',
        height=760,
        barmode='overlay', bargap=0.15,
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1,
                    font=dict(color='white', size=10), bgcolor='rgba(0,0,0,0.8)',
                    bordercolor='white', borderwidth=1),
        hovermode='closest',
        xaxis=dict(gridcolor='rgba(128,128,128,0.2)', showgrid=True,
                   zeroline=True, zerolinecolor='rgba(255,255,255,0.3)', zerolinewidth=2),
        xaxis4=dict(overlaying='x', side='bottom', title='Significance Score (%)',
                    range=[0, 500], showgrid=False, showline=False, zeroline=False,
                    tickfont=dict(color='rgba(245,158,11,0.7)', size=9),
                    title_font=dict(color='rgba(245,158,11,0.7)', size=10)),
        yaxis=dict(gridcolor='rgba(128,128,128,0.2)', showgrid=True, autorange=True),
        margin=dict(l=80, r=80, t=120, b=80),
        dragmode='drawline',
        newshape=dict(line=dict(color='#f59e0b', width=2)),
    )
    fig = _configure_volume_xaxis2(fig, df_sorted)
    fig.update_layout(modebar_add=['drawline','drawopenpath','drawclosedpath','drawcircle','drawrect','eraseshape'],
                      modebar=dict(bgcolor='rgba(0,0,0,0.5)', color='#94a3b8', activecolor='#f59e0b'))

    return fig, df_classified

# ============================================================================
# STANDARD VISUALIZATION FUNCTIONS (unchanged from original, all with Volume Overlay)
# ============================================================================

def create_separate_gex_chart(df: pd.DataFrame, spot_price: float, unit_label: str = "B") -> go.Figure:
    df_sorted  = df.sort_values('strike').reset_index(drop=True)
    colors     = ['#10b981' if x > 0 else '#ef4444' for x in df_sorted['net_gex']]
    flip_zones = identify_gamma_flip_zones(df_sorted, spot_price)
    fig = go.Figure()
    fig.add_trace(go.Bar(y=df_sorted['strike'], x=df_sorted['net_gex'], orientation='h',
                         marker_color=colors, name='Net GEX', showlegend=True,
                         hovertemplate=f'Strike: %{{y:,.0f}}<br>Net GEX: %{{x:.4f}}{unit_label}<extra></extra>'))
    fig = _add_volume_overlay_horizontal(fig, df_sorted)
    fig.add_hline(y=spot_price, line_dash='dash', line_color='#06b6d4', line_width=3,
                  annotation_text=f'Spot: {spot_price:,.2f}', annotation_position='top right',
                  annotation=dict(font=dict(size=12, color='white')))
    for zone in flip_zones:
        fig.add_hline(y=zone['strike'], line_dash='dot', line_color=zone['color'], line_width=2,
                      annotation_text=f"🔄 Flip {zone['arrow']} {zone['strike']:,.0f}",
                      annotation_position='left',
                      annotation=dict(font=dict(size=10, color=zone['color']),
                                      bgcolor='rgba(0,0,0,0.7)', bordercolor=zone['color'], borderwidth=1))
        fig.add_hrect(y0=zone['lower_strike'], y1=zone['upper_strike'],
                      fillcolor=zone['color'], opacity=0.1, line_width=0,
                      annotation_text=zone['arrow'], annotation_position='right',
                      annotation=dict(font=dict(size=16, color=zone['color'])))
    fig.update_layout(
        title=dict(text='<b>🎯 Gamma Exposure (GEX) with Flip Zones</b><br><sub>Green/Red = Net GEX | 🟩🟥 = Call/Put Volume (top axis) | ✏️ toolbar to draw</sub>',
                   font=dict(size=18, color='white')),
        xaxis_title=f'GEX (₹ {unit_label})', yaxis_title='Strike Price',
        template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(26,35,50,0.8)',
        height=700, barmode='overlay',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1,
                    font=dict(color='white', size=11), bgcolor='rgba(0,0,0,0.8)', bordercolor='white', borderwidth=1),
        hovermode='closest',
        xaxis=dict(gridcolor='rgba(128,128,128,0.2)', showgrid=True),
        yaxis=dict(gridcolor='rgba(128,128,128,0.2)', showgrid=True, autorange=True),
        margin=dict(l=80, r=80, t=80, b=80), dragmode='drawline',
        newshape=dict(line=dict(color='#f59e0b', width=2)),
    )
    fig = _configure_volume_xaxis2(fig, df_sorted)
    fig.update_layout(modebar_add=['drawline','drawopenpath','drawclosedpath','drawcircle','drawrect','eraseshape'],
                      modebar=dict(bgcolor='rgba(0,0,0,0.5)', color='#94a3b8', activecolor='#f59e0b'))
    return fig


def compute_gex_strike_probability(
    df_sorted: pd.DataFrame,
    spot_price: float,
    flip_zones: list,
    unit_label: str = "B",
) -> pd.DataFrame:
    """
    Computes per-strike directional probability (bull% / bear%) for the GEX overlay chart.

    Signals (all per-strike, independent):
      1. GEX sign × magnitude   (40%) — positive GEX = dealer support = bullish
      2. Call/Put volume ratio  (25%) — call-heavy = bullish flow
      3. OI GEX vs Original GEX alignment (20%) — same sign = confirmation, opposite = divergence
      4. Distance from spot     (15%) — ATM strikes dominate

    Overlaid flags:
      • VOLUME_SPIKE   — z-score > 2.5 on total_volume at this strike (relative to cross-strike)
      • DIVERGENCE     — enhanced OI GEX and original GEX have opposite signs (conflicting dealer view)
      • NEAR_FLIP_ZONE — strike within 0.5% of a GEX flip zone (transition zone)

    Returns df_sorted with added columns:
      bull_prob, bear_prob, prob_direction, prob_icon, vol_flag, div_flag, flip_flag, hover_text
    """
    df = df_sorted.copy()

    # ── Signal 1: GEX sign × magnitude (40%) ─────────────────────────────
    max_gex = df['net_gex'].abs().max() or 1.0
    gex_norm = df['net_gex'] / max_gex                  # -1 to +1
    gex_bull = ((gex_norm + 1) / 2 * 100).clip(0, 100)  # 0→100
    gex_bear = (100 - gex_bull)

    # ── Signal 2: Call/Put volume ratio (25%) ─────────────────────────────
    cv = df['call_volume'].fillna(0).clip(lower=0)
    pv = df['put_volume'].fillna(0).clip(lower=0)
    total = (cv + pv).replace(0, 1)
    vol_bull = (cv / total * 100).clip(0, 100)
    vol_bear = (100 - vol_bull)

    # ── Signal 3: Enhanced OI GEX vs Original GEX alignment (20%) ────────
    enh = df.get('enhanced_oi_gex', pd.Series(0.0, index=df.index)).fillna(0)
    orig = df['net_gex'].fillna(0)
    # Same sign = confirmed = neutral (50/50), opposite sign = divergence
    # When aligned: bull if both positive, bear if both negative
    # When diverged: skew toward bear (divergence = uncertainty = discount bull)
    align_bull = []
    for e, o in zip(enh, orig):
        if o > 0 and e > 0:       align_bull.append(65.0)   # confirmed bullish
        elif o < 0 and e < 0:     align_bull.append(35.0)   # confirmed bearish
        elif o > 0 and e < 0:     align_bull.append(42.0)   # divergence → bearish lean
        elif o < 0 and e > 0:     align_bull.append(58.0)   # divergence → bullish lean
        else:                     align_bull.append(50.0)   # one is zero
    align_bull = pd.Series(align_bull, index=df.index)
    align_bear = 100 - align_bull

    # ── Signal 4: Distance weight (15%) ───────────────────────────────────
    dist_pct = ((df['strike'] - spot_price).abs() / spot_price * 100).clip(lower=0)
    # Nearer = higher weight. Exponential decay: weight = e^(-d/2)
    dist_weight = np.exp(-dist_pct / 2.0)          # 0 to 1
    # Distance alone doesn't give direction — it amplifies the other signals
    # We fold it into a weighted composite below

    # ── Weighted composite ────────────────────────────────────────────────
    w1, w2, w3 = 0.40, 0.25, 0.20
    w4 = 0.15  # distance weight modifier (not a separate signal, but a scalar)

    # Distance bonus: if above spot, slightly favour bull (momentum), below = bear
    pos_above = (df['strike'] >= spot_price).astype(float)  # 1 if above
    dist_dir_bonus = (pos_above - 0.5) * dist_weight * 10  # ±0 to ±5 pts

    raw_bull = (w1*gex_bull + w2*vol_bull + w3*align_bull) + dist_dir_bonus * w4 * 10
    raw_bear = (w1*gex_bear + w2*vol_bear + w3*align_bear) - dist_dir_bonus * w4 * 10

    # Normalise so they sum to 100
    total_score = (raw_bull + raw_bear).replace(0, 100)
    df['bull_prob'] = (raw_bull / total_score * 100).clip(0, 100).round(1)
    df['bear_prob'] = (100 - df['bull_prob']).round(1)

    # ── Direction + icon ─────────────────────────────────────────────────
    def _dir(bull):
        if bull >= 60: return 'BULLISH', '🟢'
        if bull <= 40: return 'BEARISH', '🔴'
        return 'NEUTRAL', '⬜'

    dirs, icons = zip(*[_dir(b) for b in df['bull_prob']])
    df['prob_direction'] = list(dirs)
    df['prob_icon']      = list(icons)

    # ── Volume spike flag (per-strike, z-score across strikes) ───────────
    tv = df['total_volume'].fillna(0)
    tv_mean = tv.mean(); tv_std = tv.std() or 1.0
    tv_z = (tv - tv_mean) / tv_std
    df['vol_flag'] = tv_z > 2.5   # True if this strike has anomalous volume vs peers

    # ── GEX divergence flag (enhanced vs original sign conflict) ─────────
    df['div_flag'] = (
        (enh > 0) & (orig < 0) |
        (enh < 0) & (orig > 0)
    )

    # ── Flip zone proximity flag ──────────────────────────────────────────
    flip_strikes = [z['strike'] for z in flip_zones]
    def _near_flip(strike):
        return any(abs(strike - fz) / max(spot_price, 1) * 100 < 0.5 for fz in flip_strikes)
    df['flip_flag'] = df['strike'].apply(_near_flip)

    # ── Composite flag icon for chart annotation ──────────────────────────
    def _composite_icon(row):
        icons = []
        if row['vol_flag']:  icons.append('⚡')
        if row['div_flag']:  icons.append('⚠️')
        if row['flip_flag']: icons.append('🔄')
        return ' '.join(icons)
    df['flag_icons'] = df.apply(_composite_icon, axis=1)

    # ── Rich hover text ───────────────────────────────────────────────────
    def _hover(row):
        flags = []
        if row['vol_flag']:  flags.append('⚡ Vol Spike')
        if row['div_flag']:  flags.append('⚠️ GEX Divergence')
        if row['flip_flag']: flags.append('🔄 Near Flip Zone')
        flag_str = ' | '.join(flags) if flags else '—'
        return (
            f"Strike: ₹{row['strike']:,.0f}<br>"
            f"{row['prob_icon']} Bull: {row['bull_prob']:.0f}% | Bear: {row['bear_prob']:.0f}%<br>"
            f"Direction: {row['prob_direction']}<br>"
            f"Flags: {flag_str}<br>"
            f"GEX: {row['net_gex']:.2f} | Vol: {row.get('total_volume',0):,.0f}"
        )
    df['hover_text'] = df.apply(_hover, axis=1)

    return df


def create_enhanced_gex_overlay_chart(df: pd.DataFrame, spot_price: float, unit_label: str = "B") -> go.Figure:
    df_sorted = df.sort_values('strike').reset_index(drop=True)
    for col in ['net_gex','call_oi_change','put_oi_change','total_volume','call_iv','put_iv']:
        if col not in df_sorted.columns: df_sorted[col] = 0.0
        df_sorted[col] = df_sorted[col].fillna(0)
    df_sorted['enhanced_oi_gex'] = 0.0
    bs_calc = BlackScholesCalculator()
    try:
        total_vol = df_sorted['total_volume'].sum()
        for idx, row in df_sorted.iterrows():
            spot = row.get('spot_price', spot_price); strike = row['strike']
            if spot <= 0 or strike <= 0: continue
            tte = 7/365
            civ = row['call_iv']/100 if row['call_iv'] > 1 else row['call_iv']
            piv = row['put_iv']/100  if row['put_iv']  > 1 else row['put_iv']
            cg = bs_calc.calculate_gamma(spot, strike, tte, 0.07, civ)
            pg = bs_calc.calculate_gamma(spot, strike, tte, 0.07, piv)
            vw = 1 + (row['total_volume'] / total_vol) if total_vol > 0 else 1.0
            iv_adj = 1 + ((civ+piv)/2 * 2)
            dw = 1 / (1 + abs(strike-spot)/spot * 2)
            sc = 1e9 if unit_label == 'B' else 1e7
            cs = 25
            df_sorted.loc[idx, 'enhanced_oi_gex'] = (
                (row['call_oi_change'] * cg * 1.5 * vw * iv_adj * dw * spot**2 * cs) / sc -
                (row['put_oi_change']  * pg * 1.5 * vw * iv_adj * dw * spot**2 * cs) / sc
            )
    except: pass
    max_gex = df_sorted['net_gex'].abs().max()
    max_enh = df_sorted['enhanced_oi_gex'].abs().max()
    flip_zones = identify_gamma_flip_zones(df_sorted, spot_price)

    # ── Per-strike directional probability ───────────────────────────────
    df_prob = compute_gex_strike_probability(df_sorted, spot_price, flip_zones, unit_label)

    fig = go.Figure()

    # ── Original GEX bars ────────────────────────────────────────────────
    orig_colors = ['#10b981' if x > 0 else '#ef4444' for x in df_sorted['net_gex']]
    fig.add_trace(go.Bar(
        y=df_sorted['strike'], x=df_sorted['net_gex'], orientation='h',
        marker=dict(color=orig_colors, opacity=0.6, line=dict(width=0)),
        name=f'Original GEX – Max: {max_gex:.4f}{unit_label}',
        hovertemplate=f'Strike: %{{y:,.0f}}<br>Original GEX: %{{x:.4f}}{unit_label}<extra></extra>',
    ))

    # ── Enhanced OI GEX bars ─────────────────────────────────────────────
    enh_colors = ['#8b5cf6' if x > 0 else '#f59e0b' for x in df_sorted['enhanced_oi_gex']]
    fig.add_trace(go.Bar(
        y=df_sorted['strike'], x=df_sorted['enhanced_oi_gex'], orientation='h',
        marker=dict(color=enh_colors, opacity=0.85, line=dict(color='white', width=1)),
        name=f'Enhanced OI GEX – Max: {max_enh:.4f}{unit_label}',
        hovertemplate=f'Strike: %{{y:,.0f}}<br>Enhanced OI GEX: %{{x:.4f}}{unit_label}<extra></extra>',
    ))

    # ── Volume overlay ───────────────────────────────────────────────────
    fig = _add_volume_overlay_horizontal(fig, df_sorted)

    # ── Probability bars on right-side x-axis (x4) ───────────────────────
    # Bull% bars: green, pointing right from 0 to bull_prob
    # Bear% bars: red, pointing left from 0 (negative)
    bull_colors_prob = [
        'rgba(16,185,129,0.75)' if d == 'BULLISH' else
        'rgba(16,185,129,0.35)' if d == 'NEUTRAL' else
        'rgba(16,185,129,0.20)'
        for d in df_prob['prob_direction']
    ]
    bear_colors_prob = [
        'rgba(239,68,68,0.75)' if d == 'BEARISH' else
        'rgba(239,68,68,0.35)' if d == 'NEUTRAL' else
        'rgba(239,68,68,0.20)'
        for d in df_prob['prob_direction']
    ]
    fig.add_trace(go.Bar(
        y=df_prob['strike'],
        x=df_prob['bull_prob'],
        orientation='h',
        name='🟢 Bull Prob%',
        xaxis='x4',
        marker=dict(color=bull_colors_prob, line=dict(width=0)),
        hovertemplate='%{customdata}<extra></extra>',
        customdata=df_prob['hover_text'],
        legendgroup='prob',
    ))
    fig.add_trace(go.Bar(
        y=df_prob['strike'],
        x=-df_prob['bear_prob'],    # negative = leftward from centre
        orientation='h',
        name='🔴 Bear Prob%',
        xaxis='x4',
        marker=dict(color=bear_colors_prob, line=dict(width=0)),
        hovertemplate='%{customdata}<extra></extra>',
        customdata=df_prob['hover_text'],
        showlegend=True,
        legendgroup='prob',
    ))

    # ── 50% centre line on prob axis ─────────────────────────────────────
    fig.add_shape(
        type='line', xref='x4', yref='paper',
        x0=0, x1=0, y0=0, y1=1,
        line=dict(color='rgba(255,255,255,0.25)', width=1.5, dash='dot'),
    )

    # ── Flag markers: volume spikes, divergences, flip-zone strikes ───────
    flagged = df_prob[df_prob['flag_icons'] != ''].copy()
    if not flagged.empty:
        fig.add_trace(go.Scatter(
            x=[52] * len(flagged),   # just right of centre on x4 scale
            y=flagged['strike'],
            xaxis='x4',
            mode='text',
            text=flagged['flag_icons'],
            textfont=dict(size=11),
            name='⚡⚠️🔄 Flags',
            hovertemplate='%{customdata}<extra></extra>',
            customdata=flagged['hover_text'],
            showlegend=True,
        ))

    # ── Spot line ─────────────────────────────────────────────────────────
    fig.add_hline(
        y=spot_price, line_dash='dash', line_color='white', line_width=3,
        annotation_text=f'Spot: {spot_price:,.2f}', annotation_position='top right',
        annotation=dict(font=dict(size=12, color='white', family='Arial Black')),
    )
    fig.add_vline(x=0, line_dash='dot', line_color='gray', line_width=2)

    # ── GEX flip zone lines ───────────────────────────────────────────────
    for zone in flip_zones:
        fig.add_hline(
            y=zone['strike'], line_dash='dot', line_color=zone['color'], line_width=2,
            annotation_text=f"🔄 {zone['strike']:,.0f}", annotation_position='left',
            annotation=dict(font=dict(size=10, color=zone['color']),
                            bgcolor='rgba(0,0,0,0.7)', bordercolor=zone['color'], borderwidth=1),
        )
        fig.add_hrect(
            y0=zone['lower_strike'], y1=zone['upper_strike'],
            fillcolor=zone['color'], opacity=0.05, line_width=0,
        )

    # ── Probability axis 50% labels ───────────────────────────────────────
    # Annotate the prob axis header
    y_max = df_prob['strike'].max()
    fig.add_annotation(
        x=50, y=y_max, xref='x4', yref='y',
        text='<b>← Bear% | Bull% →</b>',
        showarrow=False,
        font=dict(size=9, color='#94a3b8'),
        xanchor='center', yanchor='bottom',
        bgcolor='rgba(0,0,0,0.6)', borderwidth=0,
    )

    # ── Layout ────────────────────────────────────────────────────────────
    fig.update_layout(
        title=dict(
            text=(
                '<b>🚀 Enhanced GEX Overlay: Original vs Enhanced OI GEX</b><br>'
                '<sub>Green/Red = All effects | Purple/Gold = OI Δ with Greeks+Vol+IV+Distance | '
                '🟩🟥 = Volume | <b>Right panel:</b> 🟢 Bull% / 🔴 Bear% per strike '
                '| ⚡ Vol Spike · ⚠️ GEX Divergence · 🔄 Near Flip | ✏️ toolbar to draw</sub>'
            ),
            font=dict(size=15, color='white'),
        ),
        xaxis_title=f'GEX (₹ {unit_label})',
        yaxis_title='Strike Price',
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(26,35,50,0.8)',
        height=750,
        barmode='overlay',
        bargap=0.15,
        legend=dict(
            orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1,
            font=dict(color='white', size=10),
            bgcolor='rgba(0,0,0,0.8)', bordercolor='white', borderwidth=1,
        ),
        hovermode='closest',
        xaxis=dict(
            gridcolor='rgba(128,128,128,0.2)', showgrid=True,
            zeroline=True, zerolinecolor='rgba(255,255,255,0.3)', zerolinewidth=2,
            domain=[0, 0.68],   # GEX bars use left 68%
        ),
        yaxis=dict(gridcolor='rgba(128,128,128,0.2)', showgrid=True, autorange=True),
        # x4 = probability panel on right
        xaxis4=dict(
            overlaying=None,
            anchor='y',
            side='right',
            position=1.0,
            domain=[0.72, 1.0],  # right 28%
            range=[-100, 100],
            showgrid=False,
            showline=True,
            linecolor='rgba(255,255,255,0.2)',
            zeroline=True,
            zerolinecolor='rgba(255,255,255,0.4)',
            zerolinewidth=1.5,
            tickvals=[-75, -50, -25, 0, 25, 50, 75],
            ticktext=['75%', '50%', '25%', '0', '25%', '50%', '75%'],
            tickfont=dict(size=8, color='#94a3b8'),
            title=dict(text='Bear% ← | → Bull%', font=dict(size=9, color='#94a3b8')),
        ),
        margin=dict(l=80, r=120, t=110, b=80),
        dragmode='drawline',
        newshape=dict(line=dict(color='#f59e0b', width=2)),
    )
    fig = _configure_volume_xaxis2(fig, df_sorted)
    fig.update_layout(
        modebar_add=['drawline','drawopenpath','drawclosedpath','drawcircle','drawrect','eraseshape'],
        modebar=dict(bgcolor='rgba(0,0,0,0.5)', color='#94a3b8', activecolor='#f59e0b'),
    )
    return fig


def create_enhanced_vanna_overlay_chart(
    df: pd.DataFrame,
    spot_price: float,
    unit_label: str = "B",
    df_full: pd.DataFrame = None,
    tte: float = 7/365,
    iv_df_override: pd.DataFrame = None,
) -> Tuple[go.Figure, pd.DataFrame, pd.DataFrame]:
    """
    Enhanced VANNA Overlay — preserves the EXACT original chart appearance:
      • Cyan/teal bars = Original VANNA
      • Pink/magenta bars = Enhanced OI VANNA
      • Green/red volume overlay on left axis (separate x-axis like original)
      • White dashed spot line
      • GEX flip zone dotted lines (original behavior)
    ADDED (as overlays on the same chart, not a separate column):
      • VANNA flip zone dashed lines — colour-coded by role, with icon+label annotations
      • Shaded bands at each flip zone
    Returns (fig, prob_df, iv_df)  — prob_df and iv_df used by the tab for the section below the chart.
    """
    df_sorted = df.sort_values('strike').reset_index(drop=True)
    for col in ['net_vanna','call_oi_change','put_oi_change','total_volume','call_iv','put_iv']:
        if col not in df_sorted.columns: df_sorted[col] = 0.0
        df_sorted[col] = df_sorted[col].fillna(0)

    # ── Enhanced OI VANNA (same formula as original) ──────────────────────
    df_sorted['enhanced_oi_vanna'] = 0.0
    bs_calc   = BlackScholesCalculator()
    total_vol = max(df_sorted['total_volume'].sum(), 1)
    sc = 1e9 if unit_label == 'B' else 1e7
    cs = 25
    try:
        for idx, row in df_sorted.iterrows():
            spot_r = row.get('spot_price', spot_price)
            strike = row['strike']
            if spot_r <= 0 or strike <= 0: continue
            civ = row['call_iv']/100 if row['call_iv'] > 1 else row['call_iv']
            piv = row['put_iv'] /100 if row['put_iv']  > 1 else row['put_iv']
            cv  = bs_calc.calculate_vanna(spot_r, strike, tte, 0.07, civ)
            pv  = bs_calc.calculate_vanna(spot_r, strike, tte, 0.07, piv)
            vw  = 1 + (row['total_volume'] / total_vol)
            iv_adj = 1 + ((civ + piv) / 2 * 3)
            dw  = 1 / (1 + abs(strike - spot_r) / spot_r * 1.5)
            df_sorted.loc[idx, 'enhanced_oi_vanna'] = (
                (row['call_oi_change'] * cv * 2.0 * vw * iv_adj * dw * spot_r * cs) / sc +
                (row['put_oi_change']  * pv * 2.0 * vw * iv_adj * dw * spot_r * cs) / sc
            )
    except: pass

    # ── Flip zones & probability ──────────────────────────────────────────
    gex_flips   = identify_gamma_flip_zones(df_sorted, spot_price)
    vanna_flips = identify_vanna_flip_zones(df_sorted, spot_price)
    # Use caller-supplied iv_df (pre-sliced to selected timestamp) if available
    if iv_df_override is not None and len(iv_df_override) > 0:
        iv_df = iv_df_override
    else:
        iv_df = compute_iv_trend(df_full if df_full is not None else df)
    prob_df     = compute_breakout_probability(vanna_flips, iv_df, spot_price, tte)

    max_vanna   = df_sorted['net_vanna'].abs().max() or 1
    max_enh_van = df_sorted['enhanced_oi_vanna'].abs().max() or 1

    _liv      = iv_df.iloc[-1] if len(iv_df) > 0 else None
    iv_regime = str(_liv['iv_regime'])  if _liv is not None and 'iv_regime' in _liv.index else 'FLAT'
    iv_skew   = float(_liv['iv_skew'])  if _liv is not None and 'iv_skew'   in _liv.index else 0.0

    # ── SINGLE go.Figure — identical to original chart construction ───────
    fig = go.Figure()

    # Original VANNA (cyan/teal)
    orig_col = ['#06b6d4' if x >= 0 else '#0891b2' for x in df_sorted['net_vanna']]
    fig.add_trace(go.Bar(
        y=df_sorted['strike'], x=df_sorted['net_vanna'],
        orientation='h',
        marker=dict(color=orig_col, opacity=0.6, line=dict(width=0)),
        name=f'Original VANNA – Max: {max_vanna:.4f}{unit_label}',
        hovertemplate=f'Strike: %{{y:,.0f}}<br>Original VANNA: %{{x:.4f}}{unit_label}<extra></extra>',
    ))

    # Enhanced OI VANNA (pink/magenta)
    enh_col = ['#ec4899' if x >= 0 else '#be185d' for x in df_sorted['enhanced_oi_vanna']]
    fig.add_trace(go.Bar(
        y=df_sorted['strike'], x=df_sorted['enhanced_oi_vanna'],
        orientation='h',
        marker=dict(color=enh_col, opacity=0.85, line=dict(color='white', width=1)),
        name=f'Enhanced OI VANNA – Max: {max_enh_van:.4f}{unit_label}',
        hovertemplate=f'Strike: %{{y:,.0f}}<br>Enhanced OI VANNA: %{{x:.4f}}{unit_label}<extra></extra>',
    ))

    # Volume overlay (original _add_volume_overlay_horizontal behaviour)
    fig = _add_volume_overlay_horizontal(fig, df_sorted)

    # Spot line (identical to original)
    fig.add_hline(
        y=spot_price, line_dash='dash', line_color='white', line_width=3,
        annotation_text=f'Spot: {spot_price:,.2f}',
        annotation_position='top right',
        annotation=dict(font=dict(size=12, color='white', family='Arial Black')),
    )
    fig.add_vline(x=0, line_dash='dot', line_color='gray', line_width=2)

    # GEX flip zones (identical to original — subtle dotted lines on left)
    for zone in gex_flips:
        fig.add_hline(
            y=zone['strike'], line_dash='dot',
            line_color=zone['color'], line_width=1, opacity=0.3,
            annotation_text=f"🔄 {zone['strike']:,.0f}",
            annotation_position='left',
            annotation=dict(font=dict(size=9, color=zone['color']),
                            bgcolor='rgba(0,0,0,0.5)',
                            bordercolor=zone['color'], borderwidth=1),
        )

    # ── VANNA flip zones — NEW overlays, right-side annotations ──────────
    for z in vanna_flips[:10]:
        # Shaded band between the two bounding strikes
        fig.add_hrect(
            y0=z['lower_strike'], y1=z['upper_strike'],
            fillcolor=z['color'], opacity=0.08, line_width=0,
        )
        # Dashed line at the interpolated flip strike
        fig.add_hline(
            y=z['strike'],
            line_dash='dash', line_color=z['color'], line_width=2.5,
            annotation_text=f"{z['icon']} ₹{z['strike']:,.0f} · {z['role'].replace('_',' ')}",
            annotation_position='right',
            annotation=dict(
                font=dict(color=z['color'], size=10, family='Arial Black'),
                bgcolor='rgba(0,0,0,0.80)',
                bordercolor=z['color'], borderwidth=1.5,
            ),
        )

    # ── Layout — preserved exactly from original ───────────────────────────
    rc = {'EXPANDING':'#ef4444','COMPRESSING':'#10b981','FLAT':'#94a3b8'}.get(iv_regime,'#94a3b8')
    fig.update_layout(
        title=dict(
            text=(
                f'<b>🌊 Enhanced VANNA Overlay: Original vs Enhanced OI VANNA</b><br>'
                f'<sub>Cyan/Teal = All effects | Pink/Magenta = OI Δ with Vol+IV+Distance+VANNA | '
                f'🟩🟥 = Volume | ✏️ toolbar to draw | '
                f'⚡ VANNA Flip: 🔴 Resistance · 🚀 Vacuum · ⚠️ Trap Door · 🛡️ Support | '
                f'IV: <b style="color:{rc}">{iv_regime}</b> | Skew: {iv_skew:+.1f}%</sub>'
            ),
            font=dict(size=15, color='white'),
        ),
        xaxis_title=f'VANNA (dDelta/dVol) [{unit_label}]',
        yaxis_title='Strike Price',
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(26,35,50,0.8)',
        height=780,
        barmode='overlay',
        bargap=0.15,
        legend=dict(
            orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1,
            font=dict(color='white', size=11),
            bgcolor='rgba(0,0,0,0.8)', bordercolor='white', borderwidth=1,
        ),
        hovermode='closest',
        xaxis=dict(
            gridcolor='rgba(128,128,128,0.2)', showgrid=True,
            zeroline=True, zerolinecolor='rgba(255,255,255,0.3)', zerolinewidth=2,
        ),
        yaxis=dict(gridcolor='rgba(128,128,128,0.2)', showgrid=True, autorange=True),
        margin=dict(l=80, r=200, t=110, b=80),  # extra right margin for annotations
        dragmode='drawline',
        newshape=dict(line=dict(color='#f59e0b', width=2)),
    )
    fig = _configure_volume_xaxis2(fig, df_sorted)
    fig.update_layout(
        modebar_add=['drawline','drawopenpath','drawclosedpath','drawcircle','drawrect','eraseshape'],
        modebar=dict(bgcolor='rgba(0,0,0,0.5)', color='#94a3b8', activecolor='#f59e0b'),
    )
    return fig, prob_df, iv_df


def create_standard_vanna_chart(df: pd.DataFrame, spot_price: float, unit_label: str = "B") -> go.Figure:
    df_sorted = df.sort_values('strike').reset_index(drop=True)
    fig = make_subplots(rows=1, cols=2, subplot_titles=('📈 Call VANNA','📉 Put VANNA'), horizontal_spacing=0.12)
    fig.add_trace(go.Bar(y=df_sorted['strike'], x=df_sorted['call_vanna'], orientation='h',
                         marker=dict(color=['#10b981' if x>0 else '#ef4444' for x in df_sorted['call_vanna']]),
                         name='Call VANNA',
                         hovertemplate=f'Strike: %{{y:,.0f}}<br>Call VANNA: %{{x:.4f}}{unit_label}<extra></extra>'), row=1, col=1)
    fig.add_trace(go.Bar(y=df_sorted['strike'], x=df_sorted['put_vanna'], orientation='h',
                         marker=dict(color=['#10b981' if x>0 else '#ef4444' for x in df_sorted['put_vanna']]),
                         name='Put VANNA',
                         hovertemplate=f'Strike: %{{y:,.0f}}<br>Put VANNA: %{{x:.4f}}{unit_label}<extra></extra>'), row=1, col=2)
    for col in [1, 2]:
        fig.add_hline(y=spot_price, line_dash='dash', line_color='#06b6d4', line_width=2,
                      annotation_text=f'Spot: {spot_price:,.2f}', annotation_position='top right',
                      annotation=dict(font=dict(size=10, color='white')), row=1, col=col)
    fig.update_layout(title=dict(text='<b>🌊 VANNA Exposure (dDelta/dVol)</b><br><sub>✏️ toolbar to draw</sub>', font=dict(size=18, color='white')),
                      template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(26,35,50,0.8)',
                      height=600, showlegend=False, hovermode='closest',
                      margin=dict(l=80, r=80, t=100, b=80), dragmode='drawline',
                      newshape=dict(line=dict(color='#f59e0b', width=2)))
    fig.update_layout(modebar_add=['drawline','drawopenpath','drawclosedpath','drawcircle','drawrect','eraseshape'],
                      modebar=dict(bgcolor='rgba(0,0,0,0.5)', color='#94a3b8', activecolor='#f59e0b'))
    fig.update_xaxes(title_text=f'VANNA (₹ {unit_label})', gridcolor='rgba(128,128,128,0.2)', showgrid=True)
    fig.update_yaxes(title_text='Strike Price', gridcolor='rgba(128,128,128,0.2)', showgrid=True)
    return fig



# ============================================================================
# VANNA INSTITUTIONAL SIGNAL ENGINE
# ============================================================================

def compute_vanna_institutional_signals(df: pd.DataFrame,
                                         spot_price: float,
                                         unit_label: str = "B") -> dict:
    """
    Computes three institutional activity scores from VANNA data:

    1. VANNA Acceleration  – rate of change of vanna per strike
       Signal: large players initiating/closing at a specific strike.

    2. VANNA Concentration Score  – top-3 strikes as % of total VANNA
       Signal: >60% = single block position (institutional)
                <40% = distributed/unwinding

    3. Call/Put VANNA Asymmetry – ratio of call_vanna / |put_vanna|
       Signal: >2.0  = dealers net-long vol on calls → upward price pressure
               <0.5  = dealers net-long vol on puts  → downward price pressure
               ~1.0  = balanced / hedged book

    Returns a dict with annotated DataFrames and scalar KPIs.
    """
    df_s = df.sort_values('strike').reset_index(drop=True).copy()

    # ── ensure required columns exist ────────────────────────────────────────
    for col in ['call_vanna','put_vanna','net_vanna','call_volume','put_volume',
                'total_volume','call_iv','put_iv']:
        if col not in df_s.columns:
            df_s[col] = 0.0
        df_s[col] = pd.to_numeric(df_s[col], errors='coerce').fillna(0)

    # ── 1. VANNA ACCELERATION ─────────────────────────────────────────────────
    # Rate of change along the strike axis (spatial derivative).
    # Large acceleration = dealer position wall at that strike.
    df_s['vanna_accel'] = df_s['net_vanna'].diff().fillna(0)
    df_s['vanna_accel_abs'] = df_s['vanna_accel'].abs()
    max_accel = df_s['vanna_accel_abs'].max() or 1
    df_s['vanna_accel_pct'] = df_s['vanna_accel_abs'] / max_accel * 100

    # Z-score of acceleration — marks statistically anomalous strikes
    accel_mean = df_s['vanna_accel_abs'].mean()
    accel_std  = df_s['vanna_accel_abs'].std() or 1
    df_s['vanna_accel_z'] = (df_s['vanna_accel_abs'] - accel_mean) / accel_std

    # Label each strike
    def _accel_label(z):
        if z > 3.0: return '🔴 EXTREME WALL'
        if z > 2.0: return '🟠 STRONG WALL'
        if z > 1.0: return '🟡 MODERATE WALL'
        return ''
    df_s['accel_label'] = df_s['vanna_accel_z'].apply(_accel_label)

    # ── 2. VANNA CONCENTRATION SCORE ─────────────────────────────────────────
    total_vanna_abs = df_s['net_vanna'].abs().sum() or 1
    top3_vanna_abs  = df_s['net_vanna'].abs().nlargest(3).sum()
    concentration   = top3_vanna_abs / total_vanna_abs * 100

    if concentration >= 60:
        conc_label = '🎯 CONCENTRATED — Institutional Block Detected'
        conc_color = '#ef4444'
        conc_signal = 'CONCENTRATED'
    elif concentration >= 45:
        conc_label = '⚠️ SEMI-CONCENTRATED — Watch for Block'
        conc_color = '#f59e0b'
        conc_signal = 'SEMI'
    elif concentration <= 30:
        conc_label = '📤 DISTRIBUTING — Position Unwinding'
        conc_color = '#06b6d4'
        conc_signal = 'DISTRIBUTING'
    else:
        conc_label = '🔵 DISPERSED — Normal Market Making'
        conc_color = '#8b5cf6'
        conc_signal = 'DISPERSED'

    # Mark top-3 strikes
    top3_strikes = df_s.nlargest(3, 'vanna_accel_abs')['strike'].values
    df_s['is_top3'] = df_s['strike'].isin(top3_strikes)

    # ── 3. CALL/PUT VANNA ASYMMETRY ───────────────────────────────────────────
    call_vanna_total = df_s['call_vanna'].sum()
    put_vanna_total  = df_s['put_vanna'].sum()
    asym_ratio = call_vanna_total / (abs(put_vanna_total) + 1e-9)

    # Per-strike asymmetry for bar overlay
    df_s['asym_ratio'] = df_s['call_vanna'] / (df_s['put_vanna'].abs() + 1e-9)
    df_s['asym_ratio'] = df_s['asym_ratio'].clip(-5, 5)   # cap for display

    if asym_ratio > 2.0:
        asym_label  = '📈 CALL-HEAVY: Dealers exposed to upside vol → upward price pressure likely'
        asym_color  = '#10b981'
        asym_signal = 'CALL_HEAVY'
    elif asym_ratio < 0.5:
        asym_label  = '📉 PUT-HEAVY: Dealers exposed to downside vol → downward price pressure likely'
        asym_color  = '#ef4444'
        asym_signal = 'PUT_HEAVY'
    else:
        asym_label  = '⚖️ BALANCED: Hedged book, no directional pressure from VANNA'
        asym_color  = '#8b5cf6'
        asym_signal = 'BALANCED'

    return {
        'df': df_s,
        'concentration': concentration,
        'conc_label': conc_label,
        'conc_color': conc_color,
        'conc_signal': conc_signal,
        'top3_strikes': top3_strikes,
        'call_vanna_total': call_vanna_total,
        'put_vanna_total': put_vanna_total,
        'asym_ratio': asym_ratio,
        'asym_label': asym_label,
        'asym_color': asym_color,
        'asym_signal': asym_signal,
    }


def create_vanna_institutional_chart(df: pd.DataFrame,
                                      spot_price: float,
                                      unit_label: str = "B") -> Tuple[go.Figure, dict]:
    """
    4-panel institutional VANNA chart:
      Row 1 – Net VANNA bars + VANNA Acceleration overlay (secondary x)
      Row 2 – VANNA Acceleration Z-score (strike-axis bar chart)
      Row 3 – Call vs Put VANNA side-by-side with Asymmetry ratio line
      Row 4 – Concentration heatmap: per-strike share of total VANNA
    """
    signals = compute_vanna_institutional_signals(df, spot_price, unit_label)
    df_s    = signals['df']

    fig = make_subplots(
        rows=4, cols=1,
        shared_xaxes=False,   # horizontal bars — strikes on y-axis
        subplot_titles=(
            '🌊 Net VANNA  +  Acceleration Overlay  (dealer position walls)',
            '⚡ VANNA Acceleration Z-Score  (anomalous = institutional wall)',
            '📊 Call vs Put VANNA  +  Asymmetry Ratio  (directional pressure)',
            '🎯 VANNA Concentration  (% of total per strike)',
        ),
        vertical_spacing=0.07,
        row_heights=[0.30, 0.22, 0.26, 0.22],
        specs=[
            [{"secondary_y": True}],
            [{"secondary_y": False}],
            [{"secondary_y": True}],
            [{"secondary_y": False}],
        ],
    )

    strikes = df_s['strike']

    # ── Row 1: Net VANNA bars + acceleration overlay ──────────────────────────
    vanna_colors = ['#06b6d4' if v > 0 else '#ec4899' for v in df_s['net_vanna']]
    fig.add_trace(go.Bar(
        y=strikes, x=df_s['net_vanna'], orientation='h',
        marker=dict(color=vanna_colors, opacity=0.85, line=dict(width=0)),
        name='Net VANNA',
        hovertemplate=f'Strike: %{{y:,.0f}}<br>Net VANNA: %{{x:.4f}}{unit_label}<extra></extra>',
    ), row=1, col=1, secondary_y=False)

    # Acceleration as scatter on secondary x
    fig.add_trace(go.Scatter(
        y=strikes, x=df_s['vanna_accel_abs'],
        mode='lines+markers',
        line=dict(color='rgba(245,158,11,0.9)', width=2),
        marker=dict(size=df_s['vanna_accel_z'].clip(lower=0)*3+4,
                    color='rgba(245,158,11,0.85)',
                    line=dict(color='white', width=1)),
        name='|VANNA Acceleration|',
        hovertemplate=f'Strike: %{{y:,.0f}}<br>|Accel|: %{{x:.4f}}{unit_label}<br>Z: %{{customdata:.1f}}σ<extra></extra>',
        customdata=df_s['vanna_accel_z'],
    ), row=1, col=1, secondary_y=True)

    # Spot line
    fig.add_hline(y=spot_price, line_dash='dash', line_color='white', line_width=2,
                  annotation_text=f'Spot ₹{spot_price:,.0f}',
                  annotation=dict(font=dict(color='white', size=10), bgcolor='rgba(0,0,0,0.6)'),
                  row=1, col=1)

    # Mark top-3 institutional walls
    for s in signals['top3_strikes']:
        fig.add_hline(y=s, line_dash='dot', line_color='#f59e0b', line_width=1.5,
                      annotation_text=f'⚡ Wall ₹{s:,.0f}',
                      annotation_position='right',
                      annotation=dict(font=dict(color='#f59e0b', size=9),
                                      bgcolor='rgba(0,0,0,0.7)', bordercolor='#f59e0b', borderwidth=1),
                      row=1, col=1)

    # ── Row 2: Acceleration Z-score bars ─────────────────────────────────────
    z_colors = ['#dc2626' if z > 3 else ('#f97316' if z > 2 else ('#f59e0b' if z > 1 else '#334155'))
                for z in df_s['vanna_accel_z']]
    fig.add_trace(go.Bar(
        y=strikes, x=df_s['vanna_accel_z'].clip(lower=0),
        orientation='h', marker=dict(color=z_colors, line=dict(width=0)),
        name='Acceleration Z-Score',
        hovertemplate='Strike: %{y:,.0f}<br>Accel Z: %{x:.2f}σ<br>%{customdata}<extra></extra>',
        customdata=df_s['accel_label'],
    ), row=2, col=1)

    # Threshold lines on row 2
    for level, color, label in [(1.0,'rgba(245,158,11,0.6)','1σ moderate'),
                                  (2.0,'rgba(249,115,22,0.7)','2σ strong'),
                                  (3.0,'rgba(220,38,38,0.8)','3σ extreme')]:
        fig.add_vline(x=level, line_dash='dash', line_color=color, line_width=1,
                      annotation_text=label,
                      annotation=dict(font=dict(color=color, size=8)),
                      row=2, col=1)

    fig.add_hline(y=spot_price, line_dash='dash', line_color='rgba(255,255,255,0.3)',
                  line_width=1, row=2, col=1)

    # ── Row 3: Call vs Put VANNA + Asymmetry line ────────────────────────────
    fig.add_trace(go.Bar(
        y=strikes, x=df_s['call_vanna'],
        orientation='h', name='Call VANNA',
        marker=dict(color='rgba(16,185,129,0.75)', line=dict(width=0)),
        hovertemplate=f'Strike: %{{y:,.0f}}<br>Call VANNA: %{{x:.4f}}{unit_label}<extra></extra>',
    ), row=3, col=1, secondary_y=False)

    fig.add_trace(go.Bar(
        y=strikes, x=df_s['put_vanna'],
        orientation='h', name='Put VANNA',
        marker=dict(color='rgba(239,68,68,0.75)', line=dict(width=0)),
        hovertemplate=f'Strike: %{{y:,.0f}}<br>Put VANNA: %{{x:.4f}}{unit_label}<extra></extra>',
    ), row=3, col=1, secondary_y=False)

    # Asymmetry ratio on secondary axis
    asym_color_per_bar = ['#10b981' if r > 2.0 else ('#ef4444' if r < 0.5 else '#8b5cf6')
                          for r in df_s['asym_ratio']]
    fig.add_trace(go.Scatter(
        y=strikes, x=df_s['asym_ratio'],
        mode='lines+markers',
        line=dict(color='rgba(255,255,255,0.7)', width=1.5, dash='dot'),
        marker=dict(size=5, color=asym_color_per_bar, line=dict(color='white', width=1)),
        name='Call/Put VANNA Ratio',
        hovertemplate='Strike: %{y:,.0f}<br>Asymmetry: %{x:.2f}x<extra></extra>',
    ), row=3, col=1, secondary_y=True)

    # Reference lines at 2.0 and 0.5 on secondary axis
    fig.add_hline(y=spot_price, line_dash='dash', line_color='rgba(255,255,255,0.3)',
                  line_width=1, row=3, col=1)

    # ── Row 4: Concentration heatmap (per-strike % of total VANNA) ────────────
    df_s['vanna_share_pct'] = df_s['net_vanna'].abs() / (total_vanna_abs := df_s['net_vanna'].abs().sum() or 1) * 100
    share_colors = ['#dc2626' if p > 20 else ('#f97316' if p > 10 else ('#f59e0b' if p > 5 else '#334155'))
                    for p in df_s['vanna_share_pct']]
    fig.add_trace(go.Bar(
        y=strikes, x=df_s['vanna_share_pct'],
        orientation='h', marker=dict(color=share_colors, line=dict(width=0)),
        name='VANNA Share %',
        hovertemplate='Strike: %{y:,.0f}<br>Share: %{x:.1f}%<extra></extra>',
    ), row=4, col=1)

    # Mark concentration threshold
    fig.add_vline(x=20, line_dash='dash', line_color='rgba(220,38,38,0.7)', line_width=1.5,
                  annotation_text='20% wall threshold',
                  annotation=dict(font=dict(color='rgba(220,38,38,0.8)', size=9)),
                  row=4, col=1)

    fig.add_hline(y=spot_price, line_dash='dash', line_color='rgba(255,255,255,0.3)',
                  line_width=1, row=4, col=1)

    # ── Global layout ─────────────────────────────────────────────────────────
    conc_pct = signals['concentration']
    asym     = signals['asym_ratio']
    fig.update_layout(
        title=dict(
            text=(
                f'<b>🏦 VANNA Institutional Activity Monitor</b><br>'
                f'<sub>'
                f'Concentration: {conc_pct:.1f}% → {signals["conc_label"]}  |  '
                f'Asymmetry: {asym:.2f}x → {signals["asym_label"]}'
                f'</sub>'
            ),
            font=dict(size=14, color='white'),
        ),
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(26,35,50,0.8)',
        height=1200,
        barmode='overlay',
        hovermode='closest',
        legend=dict(
            orientation='h', yanchor='bottom', y=1.01, xanchor='right', x=1,
            font=dict(color='white', size=10),
            bgcolor='rgba(0,0,0,0.8)', bordercolor='rgba(255,255,255,0.2)', borderwidth=1,
        ),
        margin=dict(l=80, r=100, t=130, b=60),
        dragmode='drawline',
        newshape=dict(line=dict(color='#f59e0b', width=2)),
    )
    fig.update_layout(
        modebar_add=['drawline','drawopenpath','drawclosedpath','drawcircle','drawrect','eraseshape'],
        modebar=dict(bgcolor='rgba(0,0,0,0.5)', color='#94a3b8', activecolor='#f59e0b'),
    )

    # Axis labels
    fig.update_xaxes(title_text=f'Net VANNA ({unit_label})', gridcolor='rgba(128,128,128,0.15)', row=1, col=1)
    fig.update_xaxes(title_text='Accel Z-Score (σ)',         gridcolor='rgba(128,128,128,0.15)', row=2, col=1)
    fig.update_xaxes(title_text=f'VANNA ({unit_label})',     gridcolor='rgba(128,128,128,0.15)', row=3, col=1)
    fig.update_xaxes(title_text='VANNA Share (%)',           gridcolor='rgba(128,128,128,0.15)', row=4, col=1)
    for r in range(1, 5):
        fig.update_yaxes(title_text='Strike', gridcolor='rgba(128,128,128,0.15)',
                         autorange=True, row=r, col=1)
    fig.update_yaxes(title_text=f'|Accel| ({unit_label})', secondary_y=True, showgrid=False, row=1, col=1)
    fig.update_yaxes(title_text='Asym Ratio (x)',           secondary_y=True, showgrid=False, row=3, col=1)

    return fig, signals


def create_vanna_intraday_clock(df_full: pd.DataFrame,
                                 spot_price: float,
                                 unit_label: str = "B") -> go.Figure:
    """
    Intraday VANNA drift chart — shows how VANNA migrates across strikes
    through the trading session. This is the 'institutional clock'.

    3-row chart:
      Row 1 – VANNA centre-of-gravity (weighted mean strike) over time
               shows dealers rolling positions up/down
      Row 2 – Concentration score over time (% in top-3 strikes)
               spike = block position being initiated
      Row 3 – Call/Put VANNA asymmetry ratio over time
               >2.0 = upward pressure building, <0.5 = downward
    """
    # Aggregate by timestamp
    agg = {}
    for ts, grp in df_full.groupby('timestamp'):
        cv_sum  = grp['call_vanna'].sum()
        pv_sum  = grp['put_vanna'].sum()
        nv_abs  = grp['net_vanna'].abs()
        tot_abs = nv_abs.sum() or 1

        # centre of gravity: weighted mean strike by |net_vanna|
        cog = (grp['strike'] * nv_abs).sum() / tot_abs

        # concentration: top-3 share
        top3  = nv_abs.nlargest(3).sum()
        conc  = top3 / tot_abs * 100

        # asymmetry ratio
        asym  = cv_sum / (abs(pv_sum) + 1e-9)
        asym  = max(-5, min(5, asym))   # clip for display

        agg[ts] = {'cog': cog, 'concentration': conc, 'asym_ratio': asym,
                   'call_vanna': cv_sum, 'put_vanna': pv_sum,
                   'spot': grp['spot_price'].iloc[0]}

    if not agg:
        return go.Figure()

    clock_df = pd.DataFrame(agg).T.reset_index().rename(columns={'index':'timestamp'})
    clock_df = clock_df.sort_values('timestamp')
    ts = clock_df['timestamp']

    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        subplot_titles=(
            '🧲 VANNA Centre-of-Gravity  (weighted mean strike — shows position rolling)',
            '🎯 Concentration Score Over Time  (spike = block position initiated)',
            '⚖️ Call/Put VANNA Asymmetry Over Time  (>2.0 = upward pressure | <0.5 = downward)',
        ),
        vertical_spacing=0.08,
        row_heights=[0.38, 0.30, 0.32],
        specs=[[{"secondary_y": True}],
               [{"secondary_y": False}],
               [{"secondary_y": False}]],
    )

    # ── Row 1: CoG + spot price ───────────────────────────────────────────────
    fig.add_trace(go.Scatter(
        x=ts, y=clock_df['spot'],
        mode='lines', name='Spot Price',
        line=dict(color='rgba(59,130,246,0.6)', width=1.5),
        fill='tozeroy', fillcolor='rgba(59,130,246,0.05)',
        hovertemplate='%{x|%H:%M}<br>Spot: ₹%{y:,.2f}<extra></extra>',
    ), row=1, col=1, secondary_y=False)

    fig.add_trace(go.Scatter(
        x=ts, y=clock_df['cog'],
        mode='lines+markers', name='VANNA CoG (Gravity Strike)',
        line=dict(color='#f59e0b', width=2.5),
        marker=dict(size=6, color='#f59e0b', line=dict(color='white', width=1)),
        hovertemplate='%{x|%H:%M}<br>CoG Strike: ₹%{y:,.2f}<extra></extra>',
    ), row=1, col=1, secondary_y=True)

    # ── Row 2: Concentration score ────────────────────────────────────────────
    conc_colors = ['#dc2626' if c >= 60 else ('#f97316' if c >= 45 else ('#8b5cf6' if c <= 30 else '#334155'))
                   for c in clock_df['concentration']]
    fig.add_trace(go.Bar(
        x=ts, y=clock_df['concentration'],
        marker_color=conc_colors, name='Concentration %',
        hovertemplate='%{x|%H:%M}<br>Concentration: %{y:.1f}%<extra></extra>',
    ), row=2, col=1)

    for level, color, label in [
        (60, 'rgba(220,38,38,0.8)',  '60% — Institutional Block'),
        (45, 'rgba(249,115,22,0.6)', '45% — Semi-concentrated'),
        (30, 'rgba(6,182,212,0.5)',  '30% — Distributing'),
    ]:
        fig.add_hline(y=level, line_dash='dash', line_color=color, line_width=1.5,
                      annotation_text=label, annotation_position='right',
                      annotation=dict(font=dict(color=color, size=9)), row=2, col=1)

    # ── Row 3: Asymmetry ratio ────────────────────────────────────────────────
    asym_colors = ['#10b981' if r > 2.0 else ('#ef4444' if r < 0.5 else '#8b5cf6')
                   for r in clock_df['asym_ratio']]
    fig.add_trace(go.Scatter(
        x=ts, y=clock_df['asym_ratio'],
        mode='lines+markers', name='Asym Ratio',
        line=dict(color='rgba(255,255,255,0.5)', width=1.5),
        marker=dict(size=8, color=asym_colors, line=dict(color='white', width=1.5)),
        hovertemplate='%{x|%H:%M}<br>Asym: %{y:.2f}x<extra></extra>',
    ), row=3, col=1)

    # Fill zones
    fig.add_hrect(y0=2.0,  y1=5.0,  fillcolor='rgba(16,185,129,0.08)',  line_width=0, row=3, col=1)
    fig.add_hrect(y0=-5.0, y1=0.5,  fillcolor='rgba(239,68,68,0.08)',   line_width=0, row=3, col=1)
    for level, color, label in [
        (2.0,  'rgba(16,185,129,0.7)',  '2.0x — Call Heavy (↑ pressure)'),
        (1.0,  'rgba(139,92,246,0.4)',  '1.0x — Balanced'),
        (0.5,  'rgba(239,68,68,0.7)',   '0.5x — Put Heavy (↓ pressure)'),
    ]:
        fig.add_hline(y=level, line_dash='dash', line_color=color, line_width=1.5,
                      annotation_text=label, annotation_position='right',
                      annotation=dict(font=dict(color=color, size=9)), row=3, col=1)

    # ── Global layout ─────────────────────────────────────────────────────────
    fig.update_layout(
        title=dict(
            text=(
                '<b>🕐 VANNA Institutional Clock — Intraday Position Drift</b><br>'
                '<sub>'
                '🧲 CoG rising with spot = dealers rolling up (trend day) | '
                'CoG flat despite spot move = reversion likely | '
                '🎯 Conc spike = block initiated | '
                '⚖️ Asym >2.0 = upward pressure | <0.5 = downward pressure'
                '</sub>'
            ),
            font=dict(size=14, color='white'),
        ),
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(26,35,50,0.8)',
        height=900,
        hovermode='x unified',
        legend=dict(
            orientation='h', yanchor='bottom', y=1.01, xanchor='right', x=1,
            font=dict(color='white', size=10),
            bgcolor='rgba(0,0,0,0.8)', bordercolor='rgba(255,255,255,0.2)', borderwidth=1,
        ),
        margin=dict(l=70, r=100, t=130, b=60),
        dragmode='drawline',
        newshape=dict(line=dict(color='#f59e0b', width=2)),
    )
    fig.update_layout(
        modebar_add=['drawline','drawopenpath','drawclosedpath','drawcircle','drawrect','eraseshape'],
        modebar=dict(bgcolor='rgba(0,0,0,0.5)', color='#94a3b8', activecolor='#f59e0b'),
    )
    fig.update_xaxes(title_text='Time (IST)', gridcolor='rgba(128,128,128,0.15)', row=3, col=1)
    fig.update_yaxes(title_text='Spot (₹)',           secondary_y=False, gridcolor='rgba(128,128,128,0.15)', row=1, col=1)
    fig.update_yaxes(title_text='CoG Strike (₹)',     secondary_y=True,  showgrid=False, row=1, col=1)
    fig.update_yaxes(title_text='Concentration (%)',  gridcolor='rgba(128,128,128,0.15)', row=2, col=1)
    fig.update_yaxes(title_text='Asym Ratio (x)',     gridcolor='rgba(128,128,128,0.15)', row=3, col=1)

    return fig


# ============================================================================
# VANNA FLIP ZONE ENGINE + BREAKOUT PROBABILITY
# ============================================================================

def identify_vanna_flip_zones(df: pd.DataFrame, spot_price: float) -> List[Dict]:
    """
    Find strikes where cumulative net VANNA crosses zero.
    Returns list of flip zone dicts with direction, magnitude and zone type.

    Zone types:
      POS_TO_NEG  – positive VANNA above → negative below (trap door)
      NEG_TO_POS  – negative VANNA above → positive below (spring floor)

    Spot-relative role:
      flip above spot + POS_TO_NEG  → resistance ceiling (IV expansion = breakdown)
      flip above spot + NEG_TO_POS  → vacuum / acceleration zone (IV expansion = squeeze UP)
      flip below spot + POS_TO_NEG  → trap door  (IV expansion = acceleration DOWN)
      flip below spot + NEG_TO_POS  → support floor (IV compression = hold)
    """
    df_s = df.sort_values('strike').reset_index(drop=True)
    zones = []
    for i in range(len(df_s) - 1):
        cur_v  = df_s.iloc[i]['net_vanna']
        nxt_v  = df_s.iloc[i+1]['net_vanna']
        cur_k  = df_s.iloc[i]['strike']
        nxt_k  = df_s.iloc[i+1]['strike']
        if (cur_v > 0 and nxt_v < 0) or (cur_v < 0 and nxt_v > 0):
            # linear interpolation for exact flip level
            w         = abs(cur_v) / (abs(cur_v) + abs(nxt_v) + 1e-12)
            flip_k    = cur_k + (nxt_k - cur_k) * w
            magnitude = (abs(cur_v) + abs(nxt_v)) / 2
            flip_type = 'POS_TO_NEG' if cur_v > 0 else 'NEG_TO_POS'
            above_spot = flip_k > spot_price

            # Determine role
            if above_spot and flip_type == 'POS_TO_NEG':
                role = 'RESISTANCE_CEILING'
                role_desc = 'Resistance ceiling — IV ↑ = breakdown through here'
                color = '#ef4444'
                icon  = '🔴'
            elif above_spot and flip_type == 'NEG_TO_POS':
                role = 'VACUUM_ZONE'
                role_desc = 'Vacuum / acceleration zone — IV ↑ = rapid squeeze UP'
                color = '#10b981'
                icon  = '🚀'
            elif not above_spot and flip_type == 'POS_TO_NEG':
                role = 'TRAP_DOOR'
                role_desc = 'Trap door — IV ↑ = acceleration DOWN below this level'
                color = '#f59e0b'
                icon  = '⚠️'
            else:  # below spot, NEG_TO_POS
                role = 'SUPPORT_FLOOR'
                role_desc = 'Support floor — IV compression holds price up'
                color = '#06b6d4'
                icon  = '🛡️'

            zones.append({
                'strike'      : flip_k,
                'lower_strike': cur_k,
                'upper_strike': nxt_k,
                'lower_vanna' : cur_v,
                'upper_vanna' : nxt_v,
                'flip_type'   : flip_type,
                'role'        : role,
                'role_desc'   : role_desc,
                'magnitude'   : magnitude,
                'above_spot'  : above_spot,
                'color'       : color,
                'icon'        : icon,
                'distance_pct': abs(flip_k - spot_price) / spot_price * 100,
            })
    return sorted(zones, key=lambda z: abs(z['strike'] - spot_price))


def compute_iv_trend(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate call_iv and put_iv at ATM strike across timestamps.
    Returns a timeline DataFrame with IV trend and rate-of-change.
    ATM = strike closest to spot at each timestamp.
    """
    rows = []
    for ts, grp in df.sort_values('timestamp').groupby('timestamp'):
        spot   = grp['spot_price'].iloc[0]
        # find ATM row
        atm_idx = (grp['strike'] - spot).abs().idxmin()
        atm_row = grp.loc[atm_idx]
        call_iv = atm_row.get('call_iv', 15)
        put_iv  = atm_row.get('put_iv',  15)
        avg_iv  = (call_iv + put_iv) / 2
        # skew: call_iv - put_iv, positive = calls expensive (fear of rally)
        skew    = call_iv - put_iv
        rows.append({
            'timestamp': ts,
            'spot'     : spot,
            'call_iv'  : call_iv,
            'put_iv'   : put_iv,
            'avg_iv'   : avg_iv,
            'iv_skew'  : skew,
        })
    iv_df = pd.DataFrame(rows).sort_values('timestamp').reset_index(drop=True)
    if len(iv_df) > 1:
        iv_df['iv_change']     = iv_df['avg_iv'].diff().fillna(0)
        iv_df['iv_expanding']  = iv_df['iv_change'] > 0
        # rolling 3-bar IV slope
        iv_df['iv_slope']      = iv_df['avg_iv'].rolling(3, min_periods=1).apply(
            lambda x: (x.iloc[-1] - x.iloc[0]) / max(len(x)-1, 1), raw=False)
        iv_df['iv_regime']     = iv_df['iv_slope'].apply(
            lambda s: 'EXPANDING' if s > 0.1 else ('COMPRESSING' if s < -0.1 else 'FLAT'))
    else:
        iv_df['iv_change']    = 0.0
        iv_df['iv_expanding'] = False
        iv_df['iv_slope']     = 0.0
        iv_df['iv_regime']    = 'FLAT'
    return iv_df


def compute_breakout_probability(
    flip_zones: List[Dict],
    iv_df: pd.DataFrame,
    spot_price: float,
    tte: float = 7/365,
    df_selected: pd.DataFrame = None,
) -> pd.DataFrame:
    """
    Score each VANNA flip zone for DIRECTIONAL breakout probability.

    Per-zone scores (0-100):
      bull_score  – probability this zone drives a BULLISH move
      bear_score  – probability this zone drives a BEARISH move
      final_score – max(bull, bear) — overall activation probability
      direction   – BULLISH / BEARISH / CONFLICTED / NEUTRAL

    Zone × IV logic:
      VACUUM_ZONE + IV EXPANDING         → strong BULLISH (dealers forced to BUY delta)
      VACUUM_ZONE + IV COMPRESSING       → weak BEARISH  (dealers sell delta, fade move)
      RESISTANCE_CEILING + IV EXPANDING  → strong BEARISH (dealers forced to SELL delta)
      RESISTANCE_CEILING + IV COMPRESSING→ weak BULLISH  (ceiling absorbed, grind up)
      TRAP_DOOR + IV EXPANDING           → strong BEARISH (drop accelerates below)
      TRAP_DOOR + IV COMPRESSING         → weak BULLISH  (floor recovers)
      SUPPORT_FLOOR + IV COMPRESSING     → strong BULLISH (dealers buy delta, floor holds)
      SUPPORT_FLOOR + IV EXPANDING       → BEARISH (paradox: floor breaks under vol)

    Session-level bias signals also returned in each row:
      vanna_balance  – net VANNA above spot vs below spot
      skew_bias      – call IV vs put IV tilt
      spot_zone_pos  – is spot above or below nearest flip zone
    """
    if not flip_zones or iv_df.empty:
        return pd.DataFrame()

    latest_iv   = iv_df.iloc[-1]
    iv_regime   = str(latest_iv['iv_regime']) if 'iv_regime' in latest_iv.index else 'FLAT'
    iv_skew     = float(latest_iv['iv_skew'])   if 'iv_skew'   in latest_iv.index else 0.0
    call_iv_cur = float(latest_iv['call_iv'])   if 'call_iv'   in latest_iv.index else 15.0
    put_iv_cur  = float(latest_iv['put_iv'])    if 'put_iv'    in latest_iv.index else 15.0
    max_mag     = max(z['magnitude'] for z in flip_zones) or 1

    # ── Session-level directional signals ────────────────────────────────
    # 1. VANNA balance: sum |VANNA| above vs below spot
    vanna_above = sum(z['magnitude'] for z in flip_zones if z['above_spot'])
    vanna_below = sum(z['magnitude'] for z in flip_zones if not z['above_spot'])
    total_mag   = vanna_above + vanna_below or 1
    # >50 means more sensitivity above → IV expansion pulls price UP more
    vanna_balance_pct = vanna_above / total_mag * 100   # >50 = bullish bias

    # 2. Skew bias: positive skew = calls expensive = institutional long delta
    # normalise to 0-100 (50 = neutral, >50 = bullish, <50 = bearish)
    skew_bias_pct = np.clip(50 + iv_skew * 4, 0, 100)

    # 3. IV regime bias: expanding IV + more VANNA above = bullish ignition
    #                    expanding IV + more VANNA below = bearish ignition
    if iv_regime == 'EXPANDING':
        iv_dir_bias = 'BULLISH' if vanna_above > vanna_below else 'BEARISH'
    elif iv_regime == 'COMPRESSING':
        iv_dir_bias = 'BEARISH' if vanna_above > vanna_below else 'BULLISH'
    else:
        iv_dir_bias = 'NEUTRAL'

    rows = []
    for z in flip_zones:
        dist_pct = z['distance_pct']
        role     = z['role']

        # ── Distance score (same for both directions) ─────────────────────
        dist_score = 100 * np.exp(-dist_pct / 1.5)

        # ── Magnitude score ────────────────────────────────────────────────
        mag_score = min(100, z['magnitude'] / max_mag * 100)

        # ── TTE score ──────────────────────────────────────────────────────
        tte_score = min(100, (1 / (tte * 365 + 0.5)) * 3)

        # ── Bull / Bear IV scores based on zone role × IV regime ──────────
        # Each returns (bull_iv_score, bear_iv_score)
        if role == 'VACUUM_ZONE':
            # Above spot. IV↑ → dealers BUY delta → squeeze UP.
            # FLAT/COMPRESSING = no squeeze fuel → zone acts as ceiling not magnet.
            if iv_regime == 'EXPANDING':
                bull_iv, bear_iv = 90, 10   # strong squeeze up
            elif iv_regime == 'FLAT':
                bull_iv, bear_iv = 35, 50   # no fuel → zone caps, slight bear lean
            else:  # COMPRESSING
                bull_iv, bear_iv = 20, 65   # IV falling → dealers selling hard, fade the zone

        elif role == 'RESISTANCE_CEILING':
            # Above spot. IV↑ → dealers SELL delta → breakdown
            if iv_regime == 'EXPANDING':
                bull_iv, bear_iv = 10, 85
            elif iv_regime == 'FLAT':
                bull_iv, bear_iv = 40, 35   # ambiguous, grind
            else:  # COMPRESSING
                bull_iv, bear_iv = 60, 20   # ceiling absorbed, slow grind up

        elif role == 'TRAP_DOOR':
            # Below spot. IV↑ → dealers SELL delta below → drop accelerates
            if iv_regime == 'EXPANDING':
                bull_iv, bear_iv = 5, 90
            elif iv_regime == 'FLAT':
                bull_iv, bear_iv = 30, 45
            else:  # COMPRESSING
                bull_iv, bear_iv = 65, 15   # floor recovers, bounce

        else:  # SUPPORT_FLOOR
            # Below spot. IV↓ → dealers BUY delta → price held.
            # FLAT = some buying but uncertain. EXPANDING = floor at risk.
            if iv_regime == 'COMPRESSING':
                bull_iv, bear_iv = 88, 8    # strong floor — dealers buying
            elif iv_regime == 'FLAT':
                bull_iv, bear_iv = 52, 38   # mild support — better than neutral but not confirmed
            else:  # EXPANDING — floor breaks under vol
                bull_iv, bear_iv = 15, 78   # floor breaks, dealers forced to sell delta below

        # ── Skew alignment bonus (+/- up to 15 pts) ───────────────────────
        # Positive skew (call > put) = market pricing upside = bull aligned
        skew_bull_bonus = np.clip(iv_skew * 3, -15, 15)
        skew_bear_bonus = np.clip(-iv_skew * 3, -15, 15)

        # ── VANNA balance bonus for this zone's direction ─────────────────
        # Zone above spot benefits from more VANNA above (bull) or below (bear)
        if z['above_spot']:
            # above-spot zones: more VANNA above = stronger move when triggered
            vb_bull = np.clip((vanna_balance_pct - 50) * 0.6, -10, 10)
            vb_bear = -vb_bull
        else:
            vb_bear = np.clip((50 - vanna_balance_pct) * 0.6, -10, 10)
            vb_bull = -vb_bear

        # ── Combine into directional scores ───────────────────────────────
        bull_score = np.clip(
            0.30 * dist_score +
            0.30 * bull_iv    +
            0.20 * mag_score  +
            0.10 * tte_score  +
            skew_bull_bonus   +
            vb_bull,
            0, 100
        )
        bear_score = np.clip(
            0.30 * dist_score +
            0.30 * bear_iv    +
            0.20 * mag_score  +
            0.10 * tte_score  +
            skew_bear_bonus   +
            vb_bear,
            0, 100
        )

        final_score = max(bull_score, bear_score)

        # Direction classification
        diff = bull_score - bear_score
        if   diff >  20: direction = 'BULLISH'
        elif diff < -20: direction = 'BEARISH'
        elif final_score >= 40: direction = 'CONFLICTED'
        else:            direction = 'NEUTRAL'

        dir_color = {'BULLISH':'#10b981','BEARISH':'#ef4444',
                     'CONFLICTED':'#f59e0b','NEUTRAL':'#64748b'}[direction]
        dir_icon  = {'BULLISH':'🟢','BEARISH':'🔴',
                     'CONFLICTED':'⚡','NEUTRAL':'⬜'}[direction]

        if final_score >= 70:   signal = '🔥 HIGH'
        elif final_score >= 50: signal = '⚡ MOD'
        elif final_score >= 30: signal = '👁️ WATCH'
        else:                   signal = '💤 LOW'

        rows.append({
            'strike'           : z['strike'],
            'role'             : role,
            'role_desc'        : z['role_desc'],
            'icon'             : z['icon'],
            'color'            : z['color'],
            'distance_pct'     : dist_pct,
            'flip_type'        : z['flip_type'],
            'magnitude'        : z['magnitude'],
            'above_spot'       : z['above_spot'],
            'bull_score'       : bull_score,
            'bear_score'       : bear_score,
            'final_score'      : final_score,
            'direction'        : direction,
            'dir_color'        : dir_color,
            'dir_icon'         : dir_icon,
            'signal'           : signal,
            'iv_regime'        : iv_regime,
            'iv_skew'          : iv_skew,
            'vanna_balance_pct': vanna_balance_pct,
            'skew_bias_pct'    : skew_bias_pct,
            'iv_dir_bias'      : iv_dir_bias,
        })

    return pd.DataFrame(rows).sort_values('final_score', ascending=False).reset_index(drop=True)


def compute_session_bias(
    flip_zones: List[Dict],
    iv_df: pd.DataFrame,
    df_selected: pd.DataFrame,
    spot_price: float,
) -> Dict:
    """
    Compute a single session-level BULLISH / BEARISH score (0-100 each).

    Combines four independent signals:
      1. VANNA zone balance    — more activation potential above vs below spot
      2. IV skew               — call IV vs put IV premium
      3. Net VANNA above/below — raw dealer exposure tilt
      4. IV regime direction   — is vol expanding toward bullish or bearish zones

    Returns dict with bull_pct, bear_pct, bias, confidence, explanation lines.
    """
    if not flip_zones or iv_df.empty:
        return {'bull_pct':50,'bear_pct':50,'bias':'NEUTRAL',
                'confidence':'LOW','lines':[],'iv_regime':'FLAT','iv_skew':0}

    latest_iv = iv_df.iloc[-1]
    iv_regime = str(latest_iv['iv_regime']) if 'iv_regime' in latest_iv.index else 'FLAT'
    iv_skew   = float(latest_iv['iv_skew']) if 'iv_skew'   in latest_iv.index else 0.0

    signals   = {}
    lines     = []

    # ── Signal 1: VANNA balance (which side has more flip magnitude) ──────
    v_above = sum(z['magnitude'] for z in flip_zones if z['above_spot'])
    v_below = sum(z['magnitude'] for z in flip_zones if not z['above_spot'])
    total_v = v_above + v_below or 1
    v_pct   = v_above / total_v * 100   # >50 = more VANNA above
    # More VANNA above + expanding IV = dealers buy delta = bullish
    # More VANNA below + expanding IV = dealers sell delta = bearish
    if iv_regime == 'EXPANDING':
        # More VANNA above + expanding IV = dealers forced to buy delta above = bullish
        sig1_bull = v_pct
        sig1_bear = 100 - v_pct
    elif iv_regime == 'COMPRESSING':
        # More VANNA above + compressing IV = dealers selling into rallies = bearish
        sig1_bull = 100 - v_pct
        sig1_bear = v_pct
    else:
        # FLAT IV: VANNA above still creates resistance (dealers sell small into rallies)
        # Not fully reversed but bear-leaning when v_pct > 50
        # v_pct=70 (70% above) → sig1_bull=40, sig1_bear=60
        sig1_bull = np.clip(50 - (v_pct - 50) * 0.4, 0, 100)
        sig1_bear = 100 - sig1_bull

    signals['vanna_balance'] = (sig1_bull, sig1_bear)
    dir1 = '🟢 Bullish' if sig1_bull > sig1_bear + 10 else ('🔴 Bearish' if sig1_bear > sig1_bull + 10 else '⚖️ Neutral')
    lines.append(f"VANNA Balance: {v_pct:.0f}% above spot | IV {iv_regime} → {dir1}")

    # ── Signal 2: IV Skew ─────────────────────────────────────────────────
    # Positive skew: calls pricier → institutional buying upside → bullish
    skew_bull = np.clip(50 + iv_skew * 5, 0, 100)
    skew_bear = 100 - skew_bull
    signals['skew'] = (skew_bull, skew_bear)
    dir2 = '🟢 Call heavy' if iv_skew > 1 else ('🔴 Put heavy' if iv_skew < -1 else '⚖️ Neutral')
    lines.append(f"IV Skew: {iv_skew:+.1f}% (CE-PE) → {dir2}")

    # ── Signal 3: Net VANNA above vs below — IV-regime-aware ────────────
    # CRITICAL: direction interpretation FLIPS based on IV regime.
    #
    # Positive VANNA above spot means:
    #   IV EXPANDING  → dealers MUST BUY delta above → squeeze UP → BULLISH
    #   IV COMPRESSING→ dealers SELL delta into rallies → cap/resistance → BEARISH
    #   IV FLAT       → dealers mildly selling into rallies (resistance lean) → SLIGHTLY BEARISH
    #
    # Positive VANNA below spot means:
    #   IV EXPANDING  → dealers MUST SELL delta below → accelerate DOWN → BEARISH
    #   IV COMPRESSING→ dealers BUY delta on dips → support → BULLISH
    net_above = 0.0; net_below = 0.0
    if df_selected is not None and 'net_vanna' in df_selected.columns:
        net_above = df_selected[df_selected['strike'] > spot_price]['net_vanna'].sum()
        net_below = df_selected[df_selected['strike'] < spot_price]['net_vanna'].sum()
    total_net = abs(net_above) + abs(net_below) or 1
    above_pct = net_above / total_net   # +1 = all above, -1 = all below

    if iv_regime == 'EXPANDING':
        # VANNA above + expanding = forced dealer buying above = bullish
        nv_bull = np.clip(50 + above_pct * 50, 0, 100)
    elif iv_regime == 'COMPRESSING':
        # VANNA above + compressing = dealers selling rallies = bearish
        nv_bull = np.clip(50 - above_pct * 50, 0, 100)
    else:  # FLAT — slight resistance lean when VANNA concentrated above
        # above_pct > 0 means more VANNA above → slight bear lean (capping effect)
        nv_bull = np.clip(50 - above_pct * 25, 0, 100)
    nv_bear = 100 - nv_bull

    signals['net_vanna'] = (nv_bull, nv_bear)
    if iv_regime == 'EXPANDING':
        dir3 = '🟢 Bullish' if net_above > 0 else '🔴 Bearish'
    elif iv_regime == 'COMPRESSING':
        dir3 = '🔴 Bearish (VANNA caps rally)' if net_above > 0 else '🟢 Bullish (VANNA supports dip)'
    else:
        dir3 = '⚖️ Slight bear lean (VANNA above = resistance)' if net_above > 0 else '⚖️ Slight bull lean'
    lines.append(f"Net VANNA: above={net_above:.2f} below={net_below:.2f} | IV {iv_regime} → {dir3}")

    # ── Signal 4: Zone role count — IV-regime-adjusted ───────────────────
    # Zone roles are only as valid as the IV regime confirms them.
    # VACUUM_ZONE = bullish ONLY if IV is expanding (squeeze fuel)
    #             = bearish (ceiling) if IV is flat or compressing
    # RESISTANCE_CEILING = bearish if IV expanding, weakly bullish if compressing
    # TRAP_DOOR = bearish always (worst when IV expands)
    # SUPPORT_FLOOR = bullish if IV compressing, bearish if IV expanding
    bull_score_r = 0.0
    bear_score_r = 0.0
    for z in flip_zones:
        r = z['role']
        if r == 'VACUUM_ZONE':
            if iv_regime == 'EXPANDING':
                bull_score_r += 1.0
            elif iv_regime == 'FLAT':
                bear_score_r += 0.5   # ceiling effect
            else:  # COMPRESSING
                bear_score_r += 1.0
        elif r == 'RESISTANCE_CEILING':
            if iv_regime == 'EXPANDING':
                bear_score_r += 1.0
            elif iv_regime == 'FLAT':
                bear_score_r += 0.6
            else:  # COMPRESSING
                bull_score_r += 0.3   # weakly absorbed
        elif r == 'TRAP_DOOR':
            if iv_regime == 'EXPANDING':
                bear_score_r += 1.0
            elif iv_regime == 'FLAT':
                bear_score_r += 0.7
            else:  # COMPRESSING
                bull_score_r += 0.4   # bounce likely
        else:  # SUPPORT_FLOOR
            if iv_regime == 'COMPRESSING':
                bull_score_r += 1.0
            elif iv_regime == 'FLAT':
                bull_score_r += 0.5
            else:  # EXPANDING
                bear_score_r += 0.8   # floor at risk

    tot_r = bull_score_r + bear_score_r or 1
    role_bull = bull_score_r / tot_r * 100
    role_bear = bear_score_r / tot_r * 100
    signals['zone_roles'] = (role_bull, role_bear)
    dir4 = '🟢 Bullish zones confirmed by IV' if role_bull > role_bear + 10         else ('🔴 Bearish zones confirmed by IV' if role_bear > role_bull + 10 else '⚖️ Mixed')
    n_bull_raw = sum(1 for z in flip_zones if z['role'] in ('VACUUM_ZONE','SUPPORT_FLOOR'))
    n_bear_raw = sum(1 for z in flip_zones if z['role'] in ('RESISTANCE_CEILING','TRAP_DOOR'))
    lines.append(f"Zone Roles: {n_bull_raw} structural bull / {n_bear_raw} structural bear | IV-adj → {dir4}")

    # ── Weighted aggregate ────────────────────────────────────────────────
    weights = {'vanna_balance':0.35, 'skew':0.25, 'net_vanna':0.25, 'zone_roles':0.15}
    bull_final = sum(weights[k] * signals[k][0] for k in weights)
    bear_final = sum(weights[k] * signals[k][1] for k in weights)

    # Normalise to sum to 100
    total = bull_final + bear_final or 1
    bull_pct = round(bull_final / total * 100, 1)
    bear_pct = round(bear_final / total * 100, 1)

    diff = bull_pct - bear_pct
    if   diff >  20: bias = 'BULLISH'
    elif diff < -20: bias = 'BEARISH'
    else:            bias = 'CONFLICTED'

    if   abs(diff) >= 30: confidence = 'HIGH'
    elif abs(diff) >= 15: confidence = 'MODERATE'
    else:                 confidence = 'LOW'

    return {
        'bull_pct'  : bull_pct,
        'bear_pct'  : bear_pct,
        'bias'      : bias,
        'confidence': confidence,
        'lines'     : lines,
        'iv_regime' : iv_regime,
        'iv_skew'   : iv_skew,
        'vanna_balance_pct': v_above / total_v * 100,
        'net_vanna_above': net_above,
        'net_vanna_below': net_below,
    }


def create_vanna_flip_breakout_chart(
    df_selected: pd.DataFrame,
    df_full: pd.DataFrame,
    spot_price: float,
    unit_label: str = "B",
    tte: float = 7/365,
) -> Tuple[go.Figure, pd.DataFrame, pd.DataFrame]:
    """
    5-row VANNA Flip & Breakout Probability chart:
      Row 1 — VANNA profile (strike axis) with flip zones annotated
      Row 2 — Spot price intraday with flip zone horizontal bands
      Row 3 — ATM IV trend: call IV, put IV, skew
      Row 4 — Breakout probability score per flip zone (horizontal bar)
      Row 5 — IV regime timeline (EXPANDING / COMPRESSING / FLAT)

    Returns (fig, flip_zones_df, iv_df)
    """
    df_s     = df_selected.sort_values('strike').reset_index(drop=True)
    iv_df    = compute_iv_trend(df_full)
    flip_zones = identify_vanna_flip_zones(df_s, spot_price)
    prob_df    = compute_breakout_probability(flip_zones, iv_df, spot_price, tte)

    # ── Row 1 & Row 4 are different axes — use make_subplots with mixed
    fig = make_subplots(
        rows=5, cols=1,
        shared_xaxes=False,                 # Row 1 uses strike axis; rows 2-5 use time axis
        subplot_titles=(
            f'VANNA Profile (Strike Axis) + Flip Zones',
            'Spot Price Intraday with VANNA Flip Levels',
            'ATM Implied Volatility Trend (Call IV / Put IV / Skew)',
            'Breakout Probability Score per Flip Zone',
            'IV Regime Timeline (EXPANDING → Vol-driven moves likely)',
        ),
        vertical_spacing=0.06,
        row_heights=[0.28, 0.16, 0.18, 0.20, 0.18],
        specs=[
            [{"secondary_y": False}],
            [{"secondary_y": False}],
            [{"secondary_y": True}],
            [{"secondary_y": False}],
            [{"secondary_y": False}],
        ],
    )

    # ── Row 1: VANNA profile horizontal bars ─────────────────────────────────
    vanna_colors = ['#06b6d4' if v >= 0 else '#f59e0b' for v in df_s['net_vanna']]
    fig.add_trace(go.Bar(
        y=df_s['strike'], x=df_s['net_vanna'],
        orientation='h',
        marker=dict(color=vanna_colors, opacity=0.8, line=dict(color='rgba(255,255,255,0.1)', width=0.5)),
        name='Net VANNA',
        hovertemplate=f'Strike: %{{y:,.0f}}<br>Net VANNA: %{{x:.4f}}{unit_label}<extra></extra>',
    ), row=1, col=1)

    # Spot line on VANNA chart
    fig.add_hline(y=spot_price, line_dash='dash', line_color='white', line_width=2.5,
                  annotation_text=f'Spot ₹{spot_price:,.0f}',
                  annotation=dict(font=dict(color='white', size=11, family='Arial Black'),
                                  bgcolor='rgba(0,0,0,0.7)'),
                  annotation_position='right', row=1, col=1)
    fig.add_vline(x=0, line_dash='dot', line_color='rgba(255,255,255,0.3)', line_width=1.5, row=1, col=1)

    # Annotate flip zones on VANNA chart
    for z in flip_zones[:8]:    # max 8 to avoid clutter
        fig.add_hline(
            y=z['strike'], line_dash='dot', line_color=z['color'], line_width=2.5,
            annotation_text=f"{z['icon']} {z['strike']:,.0f} ({z['role'].replace('_',' ')})",
            annotation_position='left',
            annotation=dict(font=dict(color=z['color'], size=9),
                            bgcolor='rgba(0,0,0,0.75)', bordercolor=z['color'], borderwidth=1),
            row=1, col=1,
        )
        fig.add_hrect(
            y0=z['lower_strike'], y1=z['upper_strike'],
            fillcolor=z['color'], opacity=0.07, line_width=0, row=1, col=1,
        )

    # ── Row 2: Spot price intraday ────────────────────────────────────────────
    ts = iv_df['timestamp']
    fig.add_trace(go.Scatter(
        x=ts, y=iv_df['spot'],
        mode='lines', line=dict(color='#3b82f6', width=2),
        fill='tozeroy', fillcolor='rgba(59,130,246,0.06)',
        name='Spot Price',
        hovertemplate='%{x|%H:%M}<br>₹%{y:,.2f}<extra></extra>',
    ), row=2, col=1)

    # Flip zone horizontal lines on spot chart
    for z in flip_zones[:8]:
        fig.add_hline(
            y=z['strike'], line_dash='dot', line_color=z['color'], line_width=1.8,
            annotation_text=f"{z['icon']} {z['strike']:,.0f}",
            annotation_position='right',
            annotation=dict(font=dict(color=z['color'], size=9),
                            bgcolor='rgba(0,0,0,0.6)', bordercolor=z['color'], borderwidth=1),
            row=2, col=1,
        )

    # ── Row 3: ATM IV trend ───────────────────────────────────────────────────
    fig.add_trace(go.Scatter(
        x=ts, y=iv_df['call_iv'],
        mode='lines', line=dict(color='#10b981', width=2),
        name='Call IV (%)',
        hovertemplate='%{x|%H:%M}<br>Call IV: %{y:.1f}%<extra></extra>',
    ), row=3, col=1, secondary_y=False)

    fig.add_trace(go.Scatter(
        x=ts, y=iv_df['put_iv'],
        mode='lines', line=dict(color='#ef4444', width=2),
        name='Put IV (%)',
        hovertemplate='%{x|%H:%M}<br>Put IV: %{y:.1f}%<extra></extra>',
    ), row=3, col=1, secondary_y=False)

    # IV skew on secondary y
    skew_colors = ['#10b981' if s > 0 else '#ef4444' for s in iv_df['iv_skew']]
    fig.add_trace(go.Bar(
        x=ts, y=iv_df['iv_skew'],
        marker=dict(color=skew_colors, opacity=0.5),
        name='IV Skew (Call−Put)',
        hovertemplate='%{x|%H:%M}<br>Skew: %{y:+.1f}%<extra></extra>',
        yaxis='y6',
    ), row=3, col=1, secondary_y=True)

    fig.add_hline(y=0, line_dash='dot', line_color='rgba(255,255,255,0.2)', line_width=1, row=3, col=1)

    # ── Row 4: Breakout probability horizontal bars ───────────────────────────
    if not prob_df.empty:
        bar_colors = [r['color'] for _, r in prob_df.iterrows()]
        bar_labels = [f"{r['icon']} ₹{r['strike']:,.0f}" for _, r in prob_df.iterrows()]
        fig.add_trace(go.Bar(
            y=bar_labels,
            x=prob_df['final_score'],
            orientation='h',
            marker=dict(
                color=bar_colors,
                opacity=0.85,
                line=dict(color='white', width=1),
            ),
            text=[f"{r['signal']}  {r['final_score']:.0f}%" for _, r in prob_df.iterrows()],
            textposition='inside',
            textfont=dict(color='white', size=10, family='JetBrains Mono'),
            name='Breakout Prob Score',
            customdata=prob_df[['role_desc','iv_regime','distance_pct','magnitude']].values,
            hovertemplate=(
                'Strike: %{y}<br>'
                'Score: %{x:.1f}%<br>'
                'Role: %{customdata[0]}<br>'
                'IV Regime: %{customdata[1]}<br>'
                'Distance: %{customdata[2]:.2f}%<br>'
                'VANNA Mag: %{customdata[3]:.4f}<extra></extra>'
            ),
        ), row=4, col=1)

        # threshold lines on prob chart
        for level, color, label in [
            (70, 'rgba(239,68,68,0.8)',   '70% HIGH PROB'),
            (50, 'rgba(245,158,11,0.6)',  '50% MODERATE'),
            (30, 'rgba(100,116,139,0.5)', '30% WATCH'),
        ]:
            fig.add_vline(x=level, line_dash='dash', line_color=color, line_width=1.5,
                          annotation_text=label, annotation_position='top',
                          annotation=dict(font=dict(color=color, size=9)), row=4, col=1)
    else:
        fig.add_annotation(text="No VANNA flip zones detected in current strike range",
                           xref="paper", yref="paper", x=0.5, y=0.5,
                           showarrow=False, font=dict(color="#94a3b8", size=13), row=4, col=1)

    # ── Row 5: IV regime timeline ─────────────────────────────────────────────
    regime_color_map = {'EXPANDING': '#ef4444', 'COMPRESSING': '#10b981', 'FLAT': '#64748b'}
    regime_y_map     = {'EXPANDING': 2, 'COMPRESSING': -2, 'FLAT': 0}

    if 'iv_regime' in iv_df.columns:
        r_colors = [regime_color_map.get(r, '#64748b') for r in iv_df['iv_regime']]
        r_y      = [regime_y_map.get(r, 0)            for r in iv_df['iv_regime']]
        fig.add_trace(go.Bar(
            x=ts, y=r_y,
            marker=dict(color=r_colors, opacity=0.75, line=dict(width=0)),
            name='IV Regime',
            text=iv_df['iv_regime'],
            textposition='inside',
            textfont=dict(color='white', size=9),
            hovertemplate='%{x|%H:%M}<br>Regime: %{text}<br>IV Δ: %{customdata:.2f}%<extra></extra>',
            customdata=iv_df['iv_change'],
        ), row=5, col=1)

        fig.add_trace(go.Scatter(
            x=ts, y=iv_df['iv_slope'],
            mode='lines', line=dict(color='#f59e0b', width=2),
            name='IV Slope (3-bar)',
            hovertemplate='%{x|%H:%M}<br>Slope: %{y:+.2f}%<extra></extra>',
        ), row=5, col=1)

        fig.add_hline(y=0.1,  line_dash='dash', line_color='rgba(239,68,68,0.5)',  line_width=1, row=5, col=1)
        fig.add_hline(y=-0.1, line_dash='dash', line_color='rgba(16,185,129,0.5)', line_width=1, row=5, col=1)
        fig.add_hline(y=0,    line_dash='dot',  line_color='rgba(255,255,255,0.2)', line_width=1, row=5, col=1)

    # ── Layout ───────────────────────────────────────────────────────────────
    latest_regime = iv_df['iv_regime'].iloc[-1] if len(iv_df) > 0 else 'FLAT'
    latest_skew   = iv_df['iv_skew'].iloc[-1]   if len(iv_df) > 0 else 0
    skew_dir      = 'calls expensive (upward lean)' if latest_skew > 0 else 'puts expensive (downward lean)'

    fig.update_layout(
        title=dict(
            text=(
                f'<b>⚡ VANNA Flip Zones & Breakout Probability</b><br>'
                f'<sub>'
                f'🔴 Resistance Ceiling = IV↑ drives breakdown | '
                f'🚀 Vacuum Zone = IV↑ drives squeeze UP | '
                f'⚠️ Trap Door = IV↑ accelerates DOWN | '
                f'🛡️ Support Floor = IV↓ holds price<br>'
                f'Current IV Regime: <b>{latest_regime}</b> | '
                f'IV Skew: {latest_skew:+.1f}% ({skew_dir})'
                f'</sub>'
            ),
            font=dict(size=14, color='white'),
        ),
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(26,35,50,0.8)',
        height=1220,
        barmode='overlay',
        hovermode='closest',
        legend=dict(
            orientation='h', yanchor='bottom', y=1.01, xanchor='right', x=1,
            font=dict(color='white', size=10),
            bgcolor='rgba(0,0,0,0.8)', bordercolor='rgba(255,255,255,0.2)', borderwidth=1,
        ),
        margin=dict(l=80, r=140, t=140, b=60),
        dragmode='drawline',
        newshape=dict(line=dict(color='#f59e0b', width=2)),
    )
    fig.update_layout(
        modebar_add=['drawline','drawopenpath','drawclosedpath','drawcircle','drawrect','eraseshape'],
        modebar=dict(bgcolor='rgba(0,0,0,0.5)', color='#94a3b8', activecolor='#f59e0b'),
    )

    # axis labels
    fig.update_xaxes(title_text=f'Net VANNA (₹{unit_label})', row=1, col=1, gridcolor='rgba(128,128,128,0.15)')
    fig.update_yaxes(title_text='Strike Price (₹)',            row=1, col=1, gridcolor='rgba(128,128,128,0.15)', autorange=True)
    fig.update_xaxes(title_text='Time (IST)', gridcolor='rgba(128,128,128,0.15)', row=2, col=1)
    fig.update_yaxes(title_text='Spot (₹)',   row=2, col=1, gridcolor='rgba(128,128,128,0.15)')
    fig.update_xaxes(title_text='Time (IST)', gridcolor='rgba(128,128,128,0.15)', row=3, col=1)
    fig.update_yaxes(title_text='IV (%)',     row=3, col=1, secondary_y=False, gridcolor='rgba(128,128,128,0.15)')
    fig.update_yaxes(title_text='Skew (%)',   row=3, col=1, secondary_y=True, showgrid=False)
    fig.update_xaxes(title_text='Probability Score (%)', gridcolor='rgba(128,128,128,0.15)', row=4, col=1, range=[0,100])
    fig.update_yaxes(title_text='Flip Zone',  row=4, col=1, gridcolor='rgba(128,128,128,0.15)', autorange=True)
    fig.update_xaxes(title_text='Time (IST)', gridcolor='rgba(128,128,128,0.15)', row=5, col=1)
    fig.update_yaxes(title_text='IV Slope / Regime', row=5, col=1, gridcolor='rgba(128,128,128,0.15)')

    return fig, prob_df, iv_df

def detect_vacuum_breakout(
    df: pd.DataFrame,
    tte: float = 7/365,
) -> pd.DataFrame:
    """
    Scans every timestamp to detect when spot price BREAKS and HOLDS above
    a VACUUM ZONE (NEG_TO_POS flip above spot).

    Breakout states per timestamp:
      NO_ZONE       — no vacuum zone found at this bar
      BELOW         — spot below vacuum zone (normal state)
      ATTEMPTED     — spot first crossed above zone this bar (1 bar only so far)
      CONFIRMED     — spot held above zone for ≥2 consecutive bars
      FALSE         — spot crossed back below after attempted breakout
      EXTENDED      — confirmed + IV regime turned EXPANDING (maximum conviction)

    Returns DataFrame with columns:
      timestamp, spot, vacuum_strike, state, state_color, bull_override,
      bull_pct_override, bear_pct_override, label, hover
    """
    all_ts = sorted(df['timestamp'].unique())
    iv_full = compute_iv_trend(df)

    rows_out = []
    prev_state         = 'NO_ZONE'
    attempt_bar        = None   # index when ATTEMPTED started
    last_vacuum_strike = None   # tracks last known vacuum zone strike

    for idx, ts in enumerate(all_ts):
        df_ts    = df[df['timestamp'] == ts].copy()
        if df_ts.empty: continue
        spot_ts  = float(df_ts['spot_price'].iloc[0])
        iv_slice = iv_full[iv_full['timestamp'] <= ts]
        if iv_slice.empty: iv_slice = iv_full.iloc[:1]

        zones        = identify_vanna_flip_zones(df_ts, spot_ts)
        vacuum_zones = [z for z in zones if z['role'] == 'VACUUM_ZONE']

        if not vacuum_zones:
            # No vacuum zone visible at this bar.
            # If spot has moved ABOVE the last known zone → zone was absorbed by price.
            if prev_state in ('CONFIRMED', 'EXTENDED'):
                iv_row = iv_slice.iloc[-1]
                iv_reg = str(iv_row['iv_regime']) if 'iv_regime' in iv_row.index else 'FLAT'
                state  = 'EXTENDED' if iv_reg == 'EXPANDING' else 'CONFIRMED'
            elif prev_state == 'BELOW' and last_vacuum_strike is not None and spot_ts > last_vacuum_strike:
                state = 'ATTEMPTED'   # spot jumped through zone in single bar
                attempt_bar = idx
            elif prev_state == 'ATTEMPTED' and last_vacuum_strike is not None and spot_ts > last_vacuum_strike:
                state = 'CONFIRMED'   # held above — zone absorbed = confirmed
            else:
                state = 'NO_ZONE'
            vacuum_strike = last_vacuum_strike   # carry last known for display
        else:
            # Take nearest vacuum zone
            vz = min(vacuum_zones, key=lambda z: z['distance_pct'])
            vacuum_strike = vz['strike']
            last_vacuum_strike = vacuum_strike   # update tracker
            above = spot_ts > vacuum_strike

            if not above:
                # Spot below zone
                if prev_state in ('ATTEMPTED', 'CONFIRMED', 'EXTENDED'):
                    state = 'FALSE'   # was above, now back below
                    attempt_bar = None
                else:
                    state = 'BELOW'
                    attempt_bar = None
            else:
                # Spot above zone
                if prev_state in ('BELOW', 'FALSE', 'NO_ZONE'):
                    state = 'ATTEMPTED'
                    attempt_bar = idx
                elif prev_state == 'ATTEMPTED':
                    state = 'CONFIRMED'
                elif prev_state in ('CONFIRMED', 'EXTENDED'):
                    iv_row = iv_slice.iloc[-1]
                    iv_reg = str(iv_row['iv_regime']) if 'iv_regime' in iv_row.index else 'FLAT'
                    state  = 'EXTENDED' if iv_reg == 'EXPANDING' else 'CONFIRMED'
                else:
                    state = 'ATTEMPTED'

        # ── Bull override scores based on state ──────────────────────────
        override_map = {
            'NO_ZONE'  : (None,  None,  False),
            'BELOW'    : (None,  None,  False),
            'ATTEMPTED': (72,    28,    True),   # tentative breakout
            'CONFIRMED': (85,    15,    True),   # confirmed — strong bull
            'FALSE'    : (None,  None,  False),  # no override — let normal signals work
            'EXTENDED' : (95,    5,     True),   # IV expanding above zone — maximum conviction
        }
        bull_ov, bear_ov, do_override = override_map.get(state, (None, None, False))

        state_colors = {
            'NO_ZONE'  : '#64748b',
            'BELOW'    : '#94a3b8',
            'ATTEMPTED': '#f59e0b',
            'CONFIRMED': '#10b981',
            'FALSE'    : '#ef4444',
            'EXTENDED' : '#06b6d4',
        }
        state_icons = {
            'NO_ZONE'  : '⬜',
            'BELOW'    : '⬇️',
            'ATTEMPTED': '⚡',
            'CONFIRMED': '🚀',
            'FALSE'    : '❌',
            'EXTENDED' : '🔥',
        }

        label = f"{state_icons.get(state,'')} {state}"
        hover = (
            f"{ts.strftime('%H:%M')} | Spot ₹{spot_ts:,.0f}<br>"
            f"Zone: {'₹' + f'{vacuum_strike:,.0f}' if vacuum_strike else 'none'}<br>"
            f"Breakout State: <b>{state}</b><br>"
            + (f"Bull Override: {bull_ov}% | Bear Override: {bear_ov}%" if do_override else "No override")
        )

        rows_out.append({
            'timestamp'        : ts,
            'spot'             : spot_ts,
            'vacuum_strike'    : vacuum_strike,
            'state'            : state,
            'state_color'      : state_colors.get(state, '#64748b'),
            'state_icon'       : state_icons.get(state, ''),
            'bull_override'    : do_override,
            'bull_pct_override': bull_ov,
            'bear_pct_override': bear_ov,
            'label'            : label,
            'hover'            : hover,
        })
        prev_state = state

    return pd.DataFrame(rows_out)


def create_bias_transition_chart(
    df: pd.DataFrame,
    spot_price: float,
    selected_ts,
    tte: float = 7/365,
) -> go.Figure:
    """
    Plots Bull% and Bear% (from compute_session_bias) across every timestamp
    in the session. Marks:
      🔄 CROSSOVER  — lines cross (Bull overtakes Bear or vice versa)
      ⚡ FLIP       — bias label changes (BULLISH→BEARISH or reverse)
      🔥 SURGE      — either line moves >10% in a single bar
      ▼  Selected   — vertical line at the currently-selected timestamp
    """
    all_ts = sorted(df['timestamp'].unique())
    if len(all_ts) < 2:
        fig = go.Figure()
        fig.update_layout(template='plotly_dark', height=300,
                          title='Not enough timestamps for transition chart')
        return fig

    iv_full = compute_iv_trend(df)

    # Detect vacuum zone breakout states across the full session
    bk_df = detect_vacuum_breakout(df, tte)
    bk_map = {}
    if not bk_df.empty:
        for _, row in bk_df.iterrows():
            bk_map[row['timestamp']] = row

    times, bulls, bears, regimes, skews, biases = [], [], [], [], [], []
    breakout_states = []   # parallel list for override info
    prev_bias = None

    for ts in all_ts:
        df_ts = df[df['timestamp'] == ts].copy()
        if df_ts.empty:
            continue
        spot_ts = float(df_ts['spot_price'].iloc[0])

        # iv sliced up to this ts (same logic as tab 5)
        iv_slice = iv_full[iv_full['timestamp'] <= ts]
        if iv_slice.empty:
            iv_slice = iv_full.iloc[:1]

        zones = identify_vanna_flip_zones(df_ts, spot_ts)
        bd    = compute_session_bias(zones, iv_slice, df_ts, spot_ts)

        # Apply breakout override if active at this timestamp
        bk = bk_map.get(ts)
        if bk is not None and bk['bull_override']:
            bull_val = float(bk['bull_pct_override'])
            bear_val = float(bk['bear_pct_override'])
            bias_val = 'BULLISH'
        else:
            bull_val = bd['bull_pct']
            bear_val = bd['bear_pct']
            bias_val = bd['bias']

        times.append(ts)
        bulls.append(bull_val)
        bears.append(bear_val)
        regimes.append(bd['iv_regime'])
        skews.append(bd['iv_skew'])
        biases.append(bias_val)
        breakout_states.append(bk['state'] if bk is not None else 'NO_ZONE')

    if not times:
        fig = go.Figure()
        fig.update_layout(template='plotly_dark', height=300)
        return fig

    times_str = [t.strftime('%H:%M') for t in times]

    # ── Detect transition events ─────────────────────────────────────────
    # ── Significant event detection (filtered) ──────────────────────────
    # Rules designed to keep <5 events per chart:
    #   CROSSOVER: lines must cross AND gap must be ≥8% before & after,
    #              AND a minimum of 3 bars cooldown from last crossover
    #   FLIP:      bias label changes BULLISH↔BEARISH (CONFLICTED doesn't count),
    #              AND the new bias is held for ≥2 bars (not a one-bar flicker)
    #   SURGE:     single-bar move ≥15% on either line, NOT immediately reversed
    #              (next bar move is < half the surge size)
    MIN_GAP_BARS   = 3    # minimum bars between same-type events
    MIN_CROSS_DIFF = 8.0  # lines must diverge by ≥8% to qualify as meaningful cross
    SURGE_THRESH   = 15.0 # minimum single-bar move to qualify as surge

    crossovers, flips, surges = [], [], []
    last_cross = -MIN_GAP_BARS

    for i in range(1, len(times)):
        prev_b, curr_b = bulls[i-1], bulls[i]
        prev_r, curr_r = bears[i-1], bears[i]

        # CROSSOVER — must actually cross AND diverge meaningfully after
        prev_bull_lead = prev_b > prev_r
        curr_bull_lead = curr_b > curr_r
        gap_after = abs(curr_b - curr_r)
        if (prev_bull_lead != curr_bull_lead
                and gap_after >= MIN_CROSS_DIFF
                and (i - last_cross) >= MIN_GAP_BARS):
            crossovers.append(i)
            last_cross = i

        # FLIP — BULLISH↔BEARISH only (skip CONFLICTED), held ≥2 bars
        is_directional_flip = (
            biases[i] in ('BULLISH', 'BEARISH')
            and biases[i-1] in ('BEARISH', 'BULLISH')
            and biases[i] != biases[i-1]
        )
        if is_directional_flip:
            # Check it holds for ≥2 bars
            held = (i + 1 < len(biases) and biases[i+1] == biases[i])
            if held:
                flips.append(i)

        # SURGE — ≥15% move NOT immediately reversed
        bull_move = abs(curr_b - prev_b)
        bear_move = abs(curr_r - prev_r)
        max_move  = max(bull_move, bear_move)
        if max_move >= SURGE_THRESH:
            # not immediately reversed
            if i + 1 < len(times):
                next_bull_move = abs(bulls[i+1] - curr_b) if i+1 < len(bulls) else 0
                if next_bull_move < max_move * 0.5:   # reversal < half surge
                    surges.append(i)
            else:
                surges.append(i)

    fig = go.Figure()

    # ── Bull% line ────────────────────────────────────────────────────────
    fig.add_trace(go.Scatter(
        x=times_str, y=bulls,
        mode='lines',
        name='🟢 Bull%',
        line=dict(color='#10b981', width=2.5),
        fill='tozeroy',
        fillcolor='rgba(16,185,129,0.07)',
        hovertemplate='%{x}<br>🟢 Bull: <b>%{y:.1f}%</b><extra></extra>',
    ))

    # ── Bear% line ────────────────────────────────────────────────────────
    fig.add_trace(go.Scatter(
        x=times_str, y=bears,
        mode='lines',
        name='🔴 Bear%',
        line=dict(color='#ef4444', width=2.5),
        fill='tozeroy',
        fillcolor='rgba(239,68,68,0.07)',
        hovertemplate='%{x}<br>🔴 Bear: <b>%{y:.1f}%</b><extra></extra>',
    ))

    # ── 50% neutral reference ─────────────────────────────────────────────
    fig.add_hline(
        y=50, line_dash='dot', line_color='rgba(148,163,184,0.35)', line_width=1.5,
        annotation_text='50% neutral',
        annotation=dict(font=dict(color='#64748b', size=9)),
        annotation_position='right',
    )

    # ── CROSSOVER markers — single consolidated trace ─────────────────────
    # Bull-cross and Bear-cross as two separate traces (different colours)
    bull_cross_x, bull_cross_y, bull_cross_txt = [], [], []
    bear_cross_x, bear_cross_y, bear_cross_txt = [], [], []
    for i in crossovers:
        mid_y = (bulls[i] + bears[i]) / 2
        if bulls[i] > bears[i]:
            bull_cross_x.append(times_str[i])
            bull_cross_y.append(mid_y)
            bull_cross_txt.append(f'🟢 CROSS<br>Bull {bulls[i]:.0f}% overtakes')
        else:
            bear_cross_x.append(times_str[i])
            bear_cross_y.append(mid_y)
            bear_cross_txt.append(f'🔴 CROSS<br>Bear {bears[i]:.0f}% overtakes')

    if bull_cross_x:
        fig.add_trace(go.Scatter(
            x=bull_cross_x, y=bull_cross_y,
            mode='markers+text',
            marker=dict(symbol='star', size=18, color='#10b981',
                        line=dict(color='white', width=1.5)),
            text=['BULL CROSS'] * len(bull_cross_x),
            textposition='top center',
            textfont=dict(color='#10b981', size=9, family='JetBrains Mono'),
            name='🟢 Bull Cross',
            hovertemplate='%{x}<br>%{customdata}<extra></extra>',
            customdata=bull_cross_txt,
        ))
    if bear_cross_x:
        fig.add_trace(go.Scatter(
            x=bear_cross_x, y=bear_cross_y,
            mode='markers+text',
            marker=dict(symbol='star', size=18, color='#ef4444',
                        line=dict(color='white', width=1.5)),
            text=['BEAR CROSS'] * len(bear_cross_x),
            textposition='top center',
            textfont=dict(color='#ef4444', size=9, family='JetBrains Mono'),
            name='🔴 Bear Cross',
            hovertemplate='%{x}<br>%{customdata}<extra></extra>',
            customdata=bear_cross_txt,
        ))

    # ── FLIP markers — single consolidated trace ──────────────────────────
    bull_flip_x, bull_flip_y = [], []
    bear_flip_x, bear_flip_y = [], []
    bull_flip_txt, bear_flip_txt = [], []
    for i in flips:
        if biases[i] == 'BULLISH':
            bull_flip_x.append(times_str[i])
            bull_flip_y.append(bulls[i] + 3)
            bull_flip_txt.append(f'⚡ BULL FLIP<br>{bears[i-1]:.0f}%→{bulls[i]:.0f}% Bull')
        else:
            bear_flip_x.append(times_str[i])
            bear_flip_y.append(bears[i] + 3)
            bear_flip_txt.append(f'⚡ BEAR FLIP<br>{bulls[i-1]:.0f}%→{bears[i]:.0f}% Bear')

    if bull_flip_x:
        fig.add_trace(go.Scatter(
            x=bull_flip_x, y=bull_flip_y,
            mode='markers+text',
            marker=dict(symbol='triangle-up', size=15, color='#10b981',
                        line=dict(color='white', width=1.5)),
            text=['⚡ BULL FLIP'] * len(bull_flip_x),
            textposition='top center',
            textfont=dict(color='#10b981', size=9, family='JetBrains Mono'),
            name='⚡ Bull Flip',
            hovertemplate='%{x}<br>%{customdata}<extra></extra>',
            customdata=bull_flip_txt,
        ))
    if bear_flip_x:
        fig.add_trace(go.Scatter(
            x=bear_flip_x, y=bear_flip_y,
            mode='markers+text',
            marker=dict(symbol='triangle-down', size=15, color='#ef4444',
                        line=dict(color='white', width=1.5)),
            text=['⚡ BEAR FLIP'] * len(bear_flip_x),
            textposition='bottom center',
            textfont=dict(color='#ef4444', size=9, family='JetBrains Mono'),
            name='⚡ Bear Flip',
            hovertemplate='%{x}<br>%{customdata}<extra></extra>',
            customdata=bear_flip_txt,
        ))

    # ── SURGE markers — single consolidated trace ─────────────────────────
    surge_x, surge_y, surge_txt = [], [], []
    for i in surges:
        bull_move = abs(bulls[i] - bulls[i-1])
        bear_move = abs(bears[i] - bears[i-1])
        is_bull_surge = bull_move >= bear_move
        surge_x.append(times_str[i])
        surge_y.append(bulls[i] if is_bull_surge else bears[i])
        surge_txt.append(
            f'🔥 {"BULL" if is_bull_surge else "BEAR"} SURGE<br>'
            f'{("+" if bulls[i]>bulls[i-1] else "")}{bulls[i]-bulls[i-1]:.0f}% Bull  '
            f'{("+" if bears[i]>bears[i-1] else "")}{bears[i]-bears[i-1]:.0f}% Bear'
        )
    if surge_x:
        fig.add_trace(go.Scatter(
            x=surge_x, y=surge_y,
            mode='markers',
            marker=dict(symbol='diamond', size=13, color='#f59e0b',
                        line=dict(color='white', width=1.5)),
            name='🔥 Surge (≥15%)',
            hovertemplate='%{x}<br>%{customdata}<extra></extra>',
            customdata=surge_txt,
        ))

    # ── Shaded background via fillcolor on the scatter fills above ───────
    # (already done via fill='tozeroy' on bull/bear lines — no vrect needed)

    # ── Selected timestamp vertical line ──────────────────────────────────
    sel_str = selected_ts.strftime('%H:%M')
    if sel_str in times_str:
        sel_idx   = times_str.index(sel_str)
        sel_bull  = bulls[sel_idx]
        sel_bear  = bears[sel_idx]
        sel_bias  = biases[sel_idx]
        sel_color = '#10b981' if sel_bias=='BULLISH' else ('#ef4444' if sel_bias=='BEARISH' else '#f59e0b')
        # add_vline fails on categorical x-axis — use add_shape + scatter annotation
        fig.add_shape(
            type='line', xref='x', yref='paper',
            x0=sel_str, x1=sel_str, y0=0, y1=1,
            line=dict(color=sel_color, width=2.5, dash='dash'),
        )
        fig.add_trace(go.Scatter(
            x=[sel_str], y=[102],
            mode='text',
            text=[f'▼ NOW  🟢{sel_bull:.0f}% 🔴{sel_bear:.0f}%'],
            textfont=dict(color=sel_color, size=11, family='Arial Black'),
            textposition='bottom center',
            showlegend=False,
            hoverinfo='skip',
        ))

    # ── VACUUM ZONE BREAKOUT markers ─────────────────────────────────────
    # Three distinct event types: ATTEMPTED (⚡ amber), CONFIRMED (🚀 green), EXTENDED (🔥 cyan)
    # FALSE (❌ red)
    bk_events = {
        'ATTEMPTED': {'x':[], 'y':[], 'txt':[], 'color':'#f59e0b', 'symbol':'triangle-up',    'size':16, 'name':'⚡ Breakout Attempt'},
        'CONFIRMED': {'x':[], 'y':[], 'txt':[], 'color':'#10b981', 'symbol':'star',            'size':22, 'name':'🚀 Breakout Confirmed'},
        'EXTENDED' : {'x':[], 'y':[], 'txt':[], 'color':'#06b6d4', 'symbol':'star',            'size':24, 'name':'🔥 Breakout Extended (IV↑)'},
        'FALSE'    : {'x':[], 'y':[], 'txt':[], 'color':'#ef4444', 'symbol':'x',               'size':14, 'name':'❌ False Breakout'},
    }

    # Add green shaded background from first CONFIRMED bar onward
    confirmed_start = None
    false_end       = None
    for i, (ts_s, state) in enumerate(zip(times_str, breakout_states)):
        if state == 'CONFIRMED' and confirmed_start is None:
            confirmed_start = ts_s
        if state == 'FALSE' and confirmed_start is not None:
            false_end = ts_s
            break

    if confirmed_start is not None:
        end_ts = false_end if false_end else times_str[-1]
        fig.add_shape(
            type='rect', xref='x', yref='paper',
            x0=confirmed_start, x1=end_ts, y0=0, y1=1,
            fillcolor='rgba(16,185,129,0.06)',
            line=dict(color='rgba(16,185,129,0.3)', width=1, dash='dot'),
        )
        fig.add_annotation(
            x=confirmed_start, y=98, xref='x', yref='y',
            text='🚀 BREAKOUT ZONE',
            showarrow=False,
            font=dict(color='#10b981', size=9, family='JetBrains Mono'),
            xanchor='left', bgcolor='rgba(16,185,129,0.15)',
            bordercolor='rgba(16,185,129,0.4)', borderwidth=1,
        )

    # Plot each event state
    for i, (ts_s, state) in enumerate(zip(times_str, breakout_states)):
        if state not in bk_events: continue
        bucket = bk_events[state]
        y_val  = bulls[i] + 4 if state in ('CONFIRMED','EXTENDED','ATTEMPTED') else bears[i] + 4
        bucket['x'].append(ts_s)
        bucket['y'].append(y_val)
        # Get hover from bk_map
        ts_obj = times[i]
        bk_row = bk_map.get(ts_obj)
        bucket['txt'].append(bk_row['hover'] if bk_row is not None else state)

    for state_key, bdata in bk_events.items():
        if not bdata['x']: continue
        show_text = state_key in ('CONFIRMED', 'EXTENDED', 'FALSE')
        fig.add_trace(go.Scatter(
            x=bdata['x'], y=bdata['y'],
            mode='markers+text' if show_text else 'markers',
            marker=dict(symbol=bdata['symbol'], size=bdata['size'],
                        color=bdata['color'], line=dict(color='white', width=1.5)),
            text=[bdata['name'].split(' ',1)[1] if show_text else ''] * len(bdata['x']),
            textposition='top center',
            textfont=dict(color=bdata['color'], size=9, family='JetBrains Mono'),
            name=bdata['name'],
            hovertemplate='%{customdata}<extra></extra>',
            customdata=bdata['txt'],
        ))

    # ── IV Regime as coloured scatter dots along the bottom ─────────────────
    regime_colors = {'EXPANDING':'#ef4444','COMPRESSING':'#10b981','FLAT':'#94a3b8'}
    regime_vals   = [2] * len(times_str)   # fixed y near bottom
    reg_colors    = [regime_colors.get(r, '#64748b') for r in regimes]
    fig.add_trace(go.Scatter(
        x=times_str, y=regime_vals,
        mode='markers',
        marker=dict(color=reg_colors, size=8, symbol='square'),
        name='IV Regime',
        hovertemplate='%{x}<br>IV: %{text}<extra></extra>',
        text=regimes,
        showlegend=True,
    ))

    # ── Summary stats for title ───────────────────────────────────────────
    n_cross = len(crossovers)
    n_flip  = len(flips)
    n_surge = len(surges)
    final_b = bulls[-1]; final_r = bears[-1]
    final_bias_label = biases[-1]
    fb_color = '#10b981' if final_bias_label=='BULLISH' else ('#ef4444' if final_bias_label=='BEARISH' else '#f59e0b')

    # Breakout status summary for title
    bk_states_list = list(breakout_states)
    n_confirmed = bk_states_list.count('CONFIRMED') + bk_states_list.count('EXTENDED')
    n_false     = bk_states_list.count('FALSE')
    bk_status   = ''
    if n_confirmed > 0 and n_false == 0:
        bk_status = f' | 🚀 VACUUM BREAKOUT CONFIRMED ({n_confirmed} bars above zone)'
    elif n_confirmed > 0 and n_false > 0:
        bk_status = f' | ❌ FALSE BREAKOUT ({n_confirmed} bars above, then reversed)'
    elif bk_states_list.count('ATTEMPTED') > 0:
        bk_status = ' | ⚡ BREAKOUT ATTEMPTED (not yet confirmed)'

    fig.update_layout(
        title=dict(
            text=(
                f'<b>📊 Bull vs Bear Probability Transition — Full Session</b><br>'
                f'<sub>'
                f'Significant events only — '
                f'★ {n_cross} cross{"" if n_cross==1 else "es"} (gap≥8%) | '
                f'⚡ {n_flip} directional flip{"" if n_flip==1 else "s"} (held≥2 bars) | '
                f'◆ {n_surge} surge{"" if n_surge==1 else "s"} (≥15% move) | '
                f'Latest: 🟢 {final_b:.0f}% vs 🔴 {final_r:.0f}% → <b>{final_bias_label}</b>'
                f'{bk_status} | '
                f'Dots = IV Regime (🟢 Compress · 🔴 Expand · ⬜ Flat)'
                f'</sub>'
            ),
            font=dict(size=14, color='white'),
        ),
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(26,35,50,0.8)',
        height=420,
        hovermode='x unified',
        legend=dict(
            orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1,
            font=dict(color='white', size=10),
            bgcolor='rgba(0,0,0,0.7)', bordercolor='rgba(255,255,255,0.2)', borderwidth=1,
        ),
        xaxis=dict(
            title='Time (IST)',
            gridcolor='rgba(128,128,128,0.15)',
            tickfont=dict(size=10),
        ),
        yaxis=dict(
            title='Probability %',
            range=[0, 105],
            gridcolor='rgba(128,128,128,0.15)',
            ticksuffix='%',
        ),
        margin=dict(l=60, r=60, t=110, b=50),
        dragmode='drawline',
        newshape=dict(line=dict(color='#f59e0b', width=2)),
    )
    fig.update_layout(
        modebar_add=['drawline','drawopenpath','drawcircle','drawrect','eraseshape'],
        modebar=dict(bgcolor='rgba(0,0,0,0.5)', color='#94a3b8', activecolor='#f59e0b'),
    )
    return fig


def create_dex_chart(df: pd.DataFrame, spot_price: float, unit_label: str = "B") -> go.Figure:
    df_sorted = df.sort_values('strike').reset_index(drop=True)
    colors = ['#10b981' if x > 0 else '#ef4444' for x in df_sorted['net_dex']]
    fig = go.Figure()
    fig.add_trace(go.Bar(y=df_sorted['strike'], x=df_sorted['net_dex'], orientation='h',
                         marker_color=colors, name='Net DEX', showlegend=True,
                         hovertemplate=f'Strike: %{{y:,.0f}}<br>Net DEX: %{{x:.4f}}{unit_label}<extra></extra>'))
    fig = _add_volume_overlay_horizontal(fig, df_sorted)
    fig.add_hline(y=spot_price, line_dash='dash', line_color='#06b6d4', line_width=3,
                  annotation_text=f'Spot: {spot_price:,.2f}', annotation_position='top right')
    fig.update_layout(
        title=dict(text='<b>📊 Delta Exposure (DEX)</b><br><sub>🟩🟥 = Call/Put Volume overlay (top axis)</sub>', font=dict(size=18, color='white')),
        xaxis_title=f'DEX (₹ {unit_label})', yaxis_title='Strike Price',
        template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(26,35,50,0.8)',
        height=700, barmode='overlay',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1,
                    font=dict(color='white', size=11), bgcolor='rgba(0,0,0,0.8)', bordercolor='white', borderwidth=1),
        hovermode='closest', dragmode='drawline', newshape=dict(line=dict(color='#f59e0b', width=2)),
    )
    fig = _configure_volume_xaxis2(fig, df_sorted)
    fig.update_layout(modebar_add=['drawline','drawopenpath','drawclosedpath','drawcircle','drawrect','eraseshape'])
    return fig


def create_oi_distribution_chart(df: pd.DataFrame, spot_price: float) -> go.Figure:
    df_sorted = df.sort_values('strike').reset_index(drop=True)
    fig = go.Figure()
    fig.add_trace(go.Bar(y=df_sorted['strike'], x=df_sorted['call_oi'], orientation='h',
                         name='Call OI', marker_color='#10b981', opacity=0.7))
    fig.add_trace(go.Bar(y=df_sorted['strike'], x=-df_sorted['put_oi'], orientation='h',
                         name='Put OI', marker_color='#ef4444', opacity=0.7))
    if 'total_volume' in df_sorted.columns:
        oi_max  = max(df_sorted['call_oi'].max(), df_sorted['put_oi'].max(), 1)
        vol_max = df_sorted['total_volume'].fillna(0).max() or 1
        scale   = oi_max / vol_max
        fig.add_trace(go.Scatter(y=df_sorted['strike'], x=df_sorted['total_volume'].fillna(0)*scale,
                                 mode='lines', line=dict(color='rgba(245,158,11,0.7)', width=2, dash='dot'),
                                 name='Total Volume (scaled)', fill='tozerox', fillcolor='rgba(245,158,11,0.08)',
                                 hovertemplate='Strike: %{y:,.0f}<br>Total Vol: %{customdata:,.0f}<extra></extra>',
                                 customdata=df_sorted['total_volume'].fillna(0)))
    fig.add_hline(y=spot_price, line_dash='dash', line_color='#06b6d4', line_width=2)
    fig.update_layout(
        title=dict(text='<b>📋 Open Interest Distribution</b><br><sub>🟡 Dotted = Total Volume (scaled to OI axis)</sub>', font=dict(size=18, color='white')),
        template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(26,35,50,0.8)',
        height=600, barmode='overlay', xaxis_title='Open Interest (Contracts)', yaxis_title='Strike Price',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1,
                    font=dict(color='white', size=11), bgcolor='rgba(0,0,0,0.8)', bordercolor='white', borderwidth=1),
    )
    return fig

# ============================================================================
# UNIFIED DATA FETCHER
# ============================================================================

class UnifiedOptionsFetcher:
    def __init__(self, config: DhanConfig):
        self.config  = config
        self.headers = {'access-token': config.access_token, 'client-id': config.client_id, 'Content-Type': 'application/json'}
        self.base_url = "https://api.dhan.co/v2"
        self.bs_calc  = BlackScholesCalculator()
        self.risk_free_rate = 0.07

    def get_instrument_type(self, symbol):
        if symbol in DHAN_INDEX_SECURITY_IDS: return "INDEX"
        if symbol in DHAN_STOCK_SECURITY_IDS:  return "STOCK"
        return "UNKNOWN"

    def get_security_id(self, symbol):
        return DHAN_INDEX_SECURITY_IDS.get(symbol) or DHAN_STOCK_SECURITY_IDS.get(symbol)

    def get_contract_size(self, symbol):
        cfg = SYMBOL_CONFIG.get(symbol, {})
        return cfg.get('contract_size', cfg.get('lot_size', 50))

    def fetch_rolling_data(self, symbol, from_date, to_date, strike_type='ATM', option_type='CALL',
                           interval='60', expiry_code=1, expiry_flag='WEEK'):
        try:
            sec_id     = self.get_security_id(symbol)
            if sec_id is None: return None
            instrument = "OPTIDX" if self.get_instrument_type(symbol) == "INDEX" else "OPTSTK"
            payload = {
                "exchangeSegment": "NSE_FNO", "interval": interval,
                "securityId": sec_id, "instrument": instrument,
                "expiryFlag": expiry_flag, "expiryCode": expiry_code,
                "strike": strike_type, "drvOptionType": option_type,
                "requiredData": ["open","high","low","close","volume","oi","iv","strike","spot"],
                "fromDate": from_date, "toDate": to_date,
            }
            resp = requests.post(f"{self.base_url}/charts/rollingoption",
                                 headers=self.headers, json=payload, timeout=30)
            if resp.status_code == 200:
                return resp.json().get('data', {})
            return None
        except Exception as e:
            st.error(f"API Error: {e}")
            return None

    def process_historical_data(self, symbol, target_date, strikes, interval='60',
                                expiry_code=1, expiry_flag='WEEK',
                                from_timestamp=None, incremental=False):
        target_dt = datetime.strptime(target_date, '%Y-%m-%d')
        from_date = (from_timestamp.strftime('%Y-%m-%d') if incremental and from_timestamp
                     else (target_dt - timedelta(days=2)).strftime('%Y-%m-%d'))
        to_date   = (target_dt + timedelta(days=2)).strftime('%Y-%m-%d')

        instrument_type = self.get_instrument_type(symbol)
        contract_size   = self.get_contract_size(symbol)
        tte             = 7/365 if expiry_flag == 'WEEK' else 30/365
        scaling_factor  = 1e9 if instrument_type == 'INDEX' else 1e7
        unit_label      = 'B'  if instrument_type == 'INDEX' else 'Cr'

        all_data = []
        progress_bar = st.progress(0)
        status_text  = st.empty()
        total_steps  = len(strikes) * 2
        current_step = 0

        for strike_type in strikes:
            mode = "Incremental" if incremental else "Fetching"
            status_text.text(f"[{mode}] {symbol} {strike_type} ({expiry_flag} {expiry_code})...")
            call_data = self.fetch_rolling_data(symbol, from_date, to_date, strike_type, 'CALL', interval, expiry_code, expiry_flag)
            current_step += 1; progress_bar.progress(current_step / total_steps); time.sleep(0.3)
            put_data  = self.fetch_rolling_data(symbol, from_date, to_date, strike_type, 'PUT',  interval, expiry_code, expiry_flag)
            current_step += 1; progress_bar.progress(current_step / total_steps); time.sleep(0.3)
            if not call_data or not put_data: continue
            ce = call_data.get('ce', {}); pe = put_data.get('pe', {})
            if not ce: continue
            for i, ts in enumerate(ce.get('timestamp', [])):
                try:
                    dt_ist = datetime.fromtimestamp(ts, tz=pytz.UTC).astimezone(IST)
                    if dt_ist.date() != target_dt.date(): continue
                    if incremental and from_timestamp and dt_ist <= from_timestamp: continue
                    spot   = ce.get('spot',   [0])[i] if i < len(ce.get('spot',   [])) else 0
                    strike = ce.get('strike', [0])[i] if i < len(ce.get('strike', [])) else 0
                    if spot == 0 or strike == 0: continue
                    call_oi  = ce.get('oi',    [0])[i] if i < len(ce.get('oi',    [])) else 0
                    put_oi   = pe.get('oi',    [0])[i] if i < len(pe.get('oi',    [])) else 0
                    call_vol = ce.get('volume',[0])[i] if i < len(ce.get('volume', [])) else 0
                    put_vol  = pe.get('volume',[0])[i] if i < len(pe.get('volume', [])) else 0
                    call_iv  = ce.get('iv',   [15])[i] if i < len(ce.get('iv',   [])) else 15
                    put_iv   = pe.get('iv',   [15])[i] if i < len(pe.get('iv',   [])) else 15
                    civ_d = call_iv/100 if call_iv > 1 else call_iv
                    piv_d = put_iv /100 if put_iv  > 1 else put_iv
                    cg  = self.bs_calc.calculate_gamma(spot, strike, tte, self.risk_free_rate, civ_d)
                    pg  = self.bs_calc.calculate_gamma(spot, strike, tte, self.risk_free_rate, piv_d)
                    cd  = self.bs_calc.calculate_call_delta(spot, strike, tte, self.risk_free_rate, civ_d)
                    pd_ = self.bs_calc.calculate_put_delta( spot, strike, tte, self.risk_free_rate, piv_d)
                    cv  = self.bs_calc.calculate_vanna(spot, strike, tte, self.risk_free_rate, civ_d)
                    pv  = self.bs_calc.calculate_vanna(spot, strike, tte, self.risk_free_rate, piv_d)
                    cc  = self.bs_calc.calculate_charm(spot, strike, tte, self.risk_free_rate, civ_d, 'call')
                    pc  = self.bs_calc.calculate_charm(spot, strike, tte, self.risk_free_rate, piv_d, 'put')
                    all_data.append({
                        'timestamp': dt_ist, 'time': dt_ist.strftime('%H:%M IST'),
                        'spot_price': spot, 'strike': strike, 'strike_type': strike_type,
                        'call_oi': call_oi, 'put_oi': put_oi,
                        'call_volume': call_vol, 'put_volume': put_vol, 'total_volume': call_vol + put_vol,
                        'call_iv': call_iv, 'put_iv': put_iv,
                        'call_gex': (call_oi*cg*spot**2*contract_size)/scaling_factor,
                        'put_gex':  -(put_oi*pg*spot**2*contract_size)/scaling_factor,
                        'net_gex':  (call_oi*cg - put_oi*pg)*spot**2*contract_size/scaling_factor,
                        'call_dex': (call_oi*cd*spot*contract_size)/scaling_factor,
                        'put_dex':  (put_oi*pd_*spot*contract_size)/scaling_factor,
                        'net_dex':  (call_oi*cd + put_oi*pd_)*spot*contract_size/scaling_factor,
                        'call_vanna': (call_oi*cv*spot*contract_size)/scaling_factor,
                        'put_vanna':  (put_oi*pv*spot*contract_size)/scaling_factor,
                        'net_vanna':  (call_oi*cv + put_oi*pv)*spot*contract_size/scaling_factor,
                        'call_charm': (call_oi*cc*spot*contract_size)/scaling_factor,
                        'put_charm':  (put_oi*pc*spot*contract_size)/scaling_factor,
                        'net_charm':  (call_oi*cc + put_oi*pc)*spot*contract_size/scaling_factor,
                    })
                except: continue
        progress_bar.empty(); status_text.empty()
        if not all_data: return None, None
        df = pd.DataFrame(all_data).sort_values(['strike','timestamp']).reset_index(drop=True)
        # flow columns
        for col in ['call_gex_flow','put_gex_flow','net_gex_flow','call_dex_flow','put_dex_flow','net_dex_flow',
                    'call_oi_change','put_oi_change','call_oi_gex','put_oi_gex','net_oi_gex']:
            df[col] = 0.0
        for strike in df['strike'].unique():
            m = df['strike'] == strike
            sd = df[m]
            if len(sd) > 1:
                for base, flow in [('call_gex','call_gex_flow'),('put_gex','put_gex_flow'),('net_gex','net_gex_flow'),
                                   ('call_dex','call_dex_flow'),('put_dex','put_dex_flow'),('net_dex','net_dex_flow'),
                                   ('call_oi','call_oi_change'),('put_oi','put_oi_change')]:
                    df.loc[m, flow] = sd[base].diff().fillna(0)
        max_gex = df['net_gex'].abs().max()
        df['hedging_pressure'] = (df['net_gex'] / max_gex * 100) if max_gex > 0 else 0
        latest     = df.sort_values('timestamp').iloc[-1]
        spot_prices = df['spot_price'].unique()
        meta = {
            'symbol': symbol, 'instrument_type': instrument_type, 'date': target_date,
            'spot_price': latest['spot_price'],
            'spot_price_min': spot_prices.min(), 'spot_price_max': spot_prices.max(),
            'spot_variation_pct': (spot_prices.max()-spot_prices.min())/spot_prices.mean()*100,
            'total_records': len(df),
            'time_range': f"{df['time'].min()} - {df['time'].max()}",
            'strikes_count': df['strike'].nunique(),
            'interval': f"{interval} minutes" if interval != '1' else '1 minute',
            'expiry_code': expiry_code, 'expiry_flag': expiry_flag,
            'contract_size': contract_size, 'unit_label': unit_label,
            'fetch_time': datetime.now(IST).strftime('%H:%M:%S IST'),
            'is_incremental': incremental,
        }
        return df, meta

# ============================================================================
# SMART DATA FETCHER
# ============================================================================

def fetch_data_with_smart_cache(symbol, target_date, strikes, interval, expiry_code, expiry_flag,
                                 force_refresh=False):
    fetcher          = UnifiedOptionsFetcher(DhanConfig())
    instrument_type  = fetcher.get_instrument_type(symbol)
    is_current_day   = cache_manager.is_current_trading_day(target_date)
    is_market_open   = cache_manager.is_market_hours()
    cached_df, cached_meta, last_ts = cache_manager.get_cached_data(
        symbol, target_date, strikes, interval, expiry_code, expiry_flag, instrument_type)

    if not is_current_day:
        if cached_df is not None and not force_refresh:
            cached_meta['fetch_mode'] = 'cached'
            cached_meta['fetch_time'] = datetime.now(IST).strftime('%H:%M:%S IST')
            return cached_df, cached_meta, 'cached'
        df, meta = fetcher.process_historical_data(symbol, target_date, strikes, interval, expiry_code, expiry_flag)
        if df is not None:
            cache_manager.save_to_cache(df, meta, symbol, target_date, strikes, interval, expiry_code, expiry_flag, instrument_type)
        return df, meta, 'full_fetch'

    if not is_market_open and cached_df is not None and not force_refresh:
        cached_meta['fetch_mode'] = 'cached'
        cached_meta['fetch_time'] = datetime.now(IST).strftime('%H:%M:%S IST')
        return cached_df, cached_meta, 'cached'

    if cached_df is not None and last_ts is not None and not force_refresh:
        new_df, new_meta = fetcher.process_historical_data(
            symbol, target_date, strikes, interval, expiry_code, expiry_flag,
            from_timestamp=last_ts, incremental=True)
        if new_df is not None and len(new_df) > 0:
            merged = cache_manager.merge_incremental_data(cached_df, new_df)
            merged_meta = new_meta.copy()
            merged_meta.update({'total_records': len(merged),
                                'time_range': f"{merged['time'].min()} - {merged['time'].max()}",
                                'fetch_mode': 'incremental', 'new_records': len(new_df)})
            cache_manager.save_to_cache(merged, merged_meta, symbol, target_date, strikes, interval, expiry_code, expiry_flag, instrument_type)
            return merged, merged_meta, 'incremental'
        cached_meta['fetch_mode'] = 'cached'
        cached_meta['fetch_time'] = datetime.now(IST).strftime('%H:%M:%S IST')
        return cached_df, cached_meta, 'cached'

    df, meta = fetcher.process_historical_data(symbol, target_date, strikes, interval, expiry_code, expiry_flag)
    if df is not None:
        cache_manager.save_to_cache(df, meta, symbol, target_date, strikes, interval, expiry_code, expiry_flag, instrument_type)
    return df, meta, 'full_fetch'

# ============================================================================
# MAIN APP
# ============================================================================

def main():
    current_time   = datetime.now(IST).strftime('%H:%M:%S IST')
    is_market_open = cache_manager.is_market_hours()
    market_status  = "🟢 MARKET OPEN" if is_market_open else "🔴 MARKET CLOSED"
    market_color   = "#10b981" if is_market_open else "#ef4444"

    st.markdown(f"""
    <div class="main-header">
        <div style="display:flex;justify-content:space-between;align-items:center;">
            <div>
                <h1 class="main-title">📊 NYZTrade UNIFIED Dashboard</h1>
                <p class="sub-title">INDEX + STOCK Options | GEX/DEX/VANNA/CHARM | Smart Caching | Volume Spike Detection</p>
            </div>
            <div style="display:flex;gap:12px;align-items:center;">
                <div class="live-indicator">
                    <div class="live-dot"></div>
                    <span style="color:#ef4444;font-family:'JetBrains Mono',monospace;font-size:0.8rem;">{current_time}</span>
                </div>
                <div style="padding:6px 14px;background:rgba(30,30,30,0.5);border:1px solid {market_color}40;border-radius:20px;">
                    <span style="color:{market_color};font-family:'JetBrains Mono',monospace;font-size:0.75rem;">{market_status}</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Sidebar ───────────────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown("### ⚙️ Configuration")
        instrument_type = st.radio("📈 Instrument Type", ["Index Options","Stock Options"], index=0, horizontal=True)
        st.markdown("---")

        if instrument_type == "Index Options":
            symbol = st.selectbox("🎯 Select Index", list(DHAN_INDEX_SECURITY_IDS.keys()), index=0)
            cfg    = INDEX_CONFIG.get(symbol, INDEX_CONFIG["NIFTY"])
            st.markdown(f'<div class="index-badge">📊 INDEX | Lot: {cfg["contract_size"]} | Strike: ₹{cfg["strike_interval"]}</div>', unsafe_allow_html=True)
            default_expiry_type = "Weekly"
        else:
            category = st.selectbox("📂 Stock Category", list(STOCK_CATEGORIES.keys()), index=0)
            symbol   = st.selectbox("🎯 Select Stock", STOCK_CATEGORIES[category], index=0)
            cfg      = STOCK_CONFIG.get(symbol, {"lot_size": 500, "strike_interval": 10})
            st.markdown(f'<div class="stock-badge">📈 STOCK | Lot: {cfg["lot_size"]} | Strike: ₹{cfg["strike_interval"]}</div>', unsafe_allow_html=True)
            default_expiry_type = "Monthly"

        st.markdown("---")
        target_date = st.date_input("📅 Select Date", value=datetime.now(), max_value=datetime.now()).strftime('%Y-%m-%d')
        is_current_day = cache_manager.is_current_trading_day(target_date)
        if is_current_day:
            st.info("📡 **LIVE MODE**: Incremental updates")
        else:
            st.success("📦 **HISTORICAL**: Cached after first fetch")
        st.markdown("---")

        expiry_type = st.selectbox("📆 Expiry Type", ["Weekly","Monthly"], index=0 if default_expiry_type=="Weekly" else 1)
        expiry_flag = "WEEK" if expiry_type == "Weekly" else "MONTH"
        expiry_code = st.selectbox("Expiry Code", [1,2,3], index=0,
                                   format_func=lambda x: {1:"Current Expiry",2:"Next Expiry",3:"Far Expiry"}[x])
        st.markdown("---")

        all_strikes = ["ATM"] + [f"ATM+{i}" for i in range(1,11)] + [f"ATM-{i}" for i in range(1,11)]
        strikes = st.multiselect("⚡ Select Strikes", all_strikes, default=all_strikes)
        interval = st.selectbox("⏱️ Interval", ["1","5","15","60"], index=1,
                                format_func=lambda x: f"{x} minute" if x=="1" else f"{x} minutes")
        st.markdown("---")

        st.markdown("### 🔄 Live Controls")
        auto_refresh_enabled = is_current_day and is_market_open
        auto_refresh, refresh_interval = False, 60
        if auto_refresh_enabled:
            auto_refresh = st.checkbox("🔄 Enable Auto-Refresh", value=False)
            if auto_refresh:
                refresh_interval = st.slider("Refresh Interval (s)", 10, 300, 60, 10)
                st.info(f"⏱️ Incremental update every {refresh_interval}s")
        else:
            st.info("ℹ️ Auto-refresh disabled" + (" for historical data" if not is_current_day else " (market closed)"))

        col1, col2 = st.columns(2)
        with col1: fetch_button   = st.button("🚀 Fetch Data", use_container_width=True, type="primary")
        with col2: refresh_button = st.button("🔄 Update" if is_current_day else "🔄 Refresh", use_container_width=True)
        force_refresh = st.checkbox("🔥 Force Full Refresh", value=False, help="Ignore cache")

        st.markdown("---")
        st.markdown("### 📊 Cache Status")
        cs = cache_manager.get_cache_stats()
        st.markdown(f"- **Entries**: {cs['num_entries']}\n- **Size**: {cs['total_size_mb']:.2f} MB")
        if st.button("🗑️ Clear All Cache", use_container_width=True):
            cache_manager.clear_cache(); st.success("Cache cleared!"); st.rerun()

        st.markdown("---")
        st.markdown("### ✏️ Drawing Tools")
        st.markdown("""<div style="font-size:0.8rem;color:#94a3b8;">Hover on any chart to see toolbar:<ul style="margin:4px 0;padding-left:16px;">
        <li>📏 Line | ✍️ Open Path | 🔷 Closed Path</li>
        <li>⭕ Circle | ⬜ Rectangle | 🧹 Eraser</li></ul><i>Drawings are session-only</i></div>""", unsafe_allow_html=True)

    # ── Session state ─────────────────────────────────────────────────────────
    if 'last_refresh_time' not in st.session_state:
        st.session_state.last_refresh_time = None

    if fetch_button or refresh_button:
        st.session_state.fetch_config = {
            'symbol': symbol, 'target_date': target_date, 'strikes': strikes,
            'interval': interval, 'expiry_code': expiry_code, 'expiry_flag': expiry_flag,
            'force_refresh': force_refresh,
        }
        st.session_state.data_fetched     = False
        st.session_state.last_refresh_time = datetime.now()

    if auto_refresh and auto_refresh_enabled:
        if st.session_state.last_refresh_time is None:
            st.session_state.last_refresh_time = datetime.now()
        elapsed   = (datetime.now() - st.session_state.last_refresh_time).total_seconds()
        remaining = max(0, int(refresh_interval - elapsed))
        if remaining > 0:
            st.sidebar.success(f"⏳ Next update in: **{remaining}s**")
        else:
            st.sidebar.warning("🔄 Updating...")
        if elapsed >= refresh_interval and hasattr(st.session_state, 'fetch_config'):
            st.session_state.fetch_config['force_refresh'] = False
            st.session_state.data_fetched = False
            st.session_state.last_refresh_time = datetime.now()
        time.sleep(1); st.rerun()

    # ── Main content ──────────────────────────────────────────────────────────
    if fetch_button or refresh_button or (hasattr(st.session_state, 'fetch_config') and st.session_state.get('data_fetched', False)):
        if hasattr(st.session_state, 'fetch_config'):
            fc = st.session_state.fetch_config
            symbol       = fc['symbol'];       target_date  = fc['target_date']
            strikes      = fc['strikes'];      interval     = fc['interval']
            expiry_code  = fc.get('expiry_code', 1)
            expiry_flag  = fc.get('expiry_flag', 'WEEK')
            force_refresh = fc.get('force_refresh', False)

        if not strikes:
            st.error("❌ Please select at least one strike"); return

        need_fetch = (not st.session_state.get('data_fetched', False) or
                      'df_data' not in st.session_state or fetch_button or refresh_button)
        if need_fetch:
            try:
                df, meta, fetch_mode = fetch_data_with_smart_cache(
                    symbol, target_date, strikes, interval, expiry_code, expiry_flag, force_refresh)
                if df is None or len(df) == 0:
                    st.error("❌ No data available for the selected date/time."); return
                st.session_state.df_data    = df
                st.session_state.meta_data  = meta
                st.session_state.fetch_mode = fetch_mode
                st.session_state.data_fetched = True
                if not auto_refresh: st.rerun()
            except Exception as e:
                st.error(f"❌ Error: {e}"); return

        df         = st.session_state.df_data
        meta       = st.session_state.meta_data
        fetch_mode = st.session_state.get('fetch_mode', 'unknown')
        unit_label = meta.get('unit_label', 'B')

        all_timestamps = sorted(df['timestamp'].unique())
        if 'timestamp_idx' not in st.session_state:
            st.session_state.timestamp_idx = len(all_timestamps) - 1

        selected_ts_idx = st.slider("⏱️ Select Time Point", 0, len(all_timestamps)-1,
                                    min(st.session_state.timestamp_idx, len(all_timestamps)-1))
        selected_ts   = all_timestamps[selected_ts_idx]
        df_selected   = df[df['timestamp'] == selected_ts].copy()
        spot_price    = df_selected['spot_price'].iloc[0] if len(df_selected) > 0 else 0

        # Status bar
        mode_cfg = {'cached':('📦 CACHED','#10b981'), 'incremental':(f"📡 INCREMENTAL (+{meta.get('new_records',0)} new)",'#06b6d4'),
                    'full_fetch':('🚀 FULL FETCH','#8b5cf6')}
        mode_badge, mode_color = mode_cfg.get(fetch_mode, ('❓ UNKNOWN','#64748b'))
        inst_badge = (f'<span class="index-badge">📊 INDEX</span>' if meta.get('instrument_type') == 'INDEX'
                      else f'<span class="stock-badge">📈 STOCK</span>')
        st.markdown(f"""
        <div style="display:flex;gap:12px;align-items:center;margin-bottom:16px;flex-wrap:wrap;">
            {inst_badge}
            <span style="padding:6px 12px;background:{mode_color}20;border:1px solid {mode_color}40;border-radius:8px;
                  color:{mode_color};font-family:'JetBrains Mono',monospace;font-size:0.8rem;">{mode_badge}</span>
            <span style="color:#94a3b8;font-family:'JetBrains Mono',monospace;font-size:0.85rem;">
                {meta.get('symbol',symbol)} | {selected_ts.strftime('%H:%M:%S IST')} | ₹{spot_price:,.2f} | Records: {meta.get('total_records',0)}
            </span>
        </div>
        """, unsafe_allow_html=True)

        # KPI strip
        net_gex     = df_selected['net_gex'].sum()
        net_dex     = df_selected['net_dex'].sum()
        net_vanna   = df_selected['net_vanna'].sum()
        total_vol   = df_selected['total_volume'].sum() if 'total_volume' in df_selected.columns else 0
        flip_zones  = identify_gamma_flip_zones(df_selected, spot_price)

        c1,c2,c3,c4,c5,c6 = st.columns(6)
        for col, label, val, sub, clr in [
            (c1,'NET GEX',    f'{net_gex:.4f}{unit_label}',  '🟢 Bullish' if net_gex>0 else '🔴 Bearish',   'positive' if net_gex>0 else 'negative'),
            (c2,'NET DEX',    f'{net_dex:.4f}{unit_label}',  '📈 Long' if net_dex>0 else '📉 Short',         'positive' if net_dex>0 else 'negative'),
            (c3,'NET VANNA',  f'{net_vanna:.4f}{unit_label}','Vol Sensitivity',                               'positive' if net_vanna>0 else 'negative'),
            (c4,'SPOT PRICE', f'₹{spot_price:,.2f}',         meta.get('symbol',symbol),                      'neutral'),
            (c5,'TOTAL VOL',  f'{total_vol:,.0f}',           '📊 Contracts',                                 'neutral'),
            (c6,'FLIP ZONES', str(len(flip_zones)),          'Gamma Crossovers',                             'neutral'),
        ]:
            with col:
                st.markdown(f'<div class="metric-card {clr}"><div class="metric-label">{label}</div>'
                            f'<div class="metric-value {clr}">{val}</div>'
                            f'<div class="metric-delta">{sub}</div></div>', unsafe_allow_html=True)

        st.markdown("---")

        # ── Tabs ──────────────────────────────────────────────────────────────
        tabs = st.tabs([
            "📈 Intraday + Spike Detection",
            "🎯 Standard GEX",
            "🚀 Enhanced GEX Overlay",
            "🎯 Significant GEX",
            "🌊 Standard VANNA",
            "🌊 VANNA + ⚡ Flip Breakout",
            "📊 DEX Analysis",
            "📋 OI Distribution",
            "📁 Data Table",
        ])

        # ── TAB 0: Intraday + Volume Spike Detection ──────────────────────────
        with tabs[0]:
            st.markdown("### 📈 Intraday Evolution + Volume Spike Detection")

            col_z, col_info = st.columns([1, 3])
            with col_z:
                z_thresh = st.slider(
                    "Spike Sensitivity (σ threshold)",
                    min_value=1.0, max_value=4.0, value=2.0, step=0.25,
                    help="Lower = more spikes detected. 2σ ≈ top 5% of bars.",
                    key="z_thresh_slider",
                )
            with col_info:
                st.markdown("""
                <div class="spike-legend">
                🚀 <b style="color:#10b981">Confirmed Bullish</b> = Call-dominant volume spike AND GEX rising significantly<br>
                💥 <b style="color:#ef4444">Confirmed Bearish</b> = Put-dominant volume spike AND GEX falling significantly<br>
                ⚠️ <b style="color:#f59e0b">Divergence</b> = Volume direction conflicts with GEX direction — wait for resolution<br>
                📊 <b style="color:#8b5cf6">Unconfirmed</b> = Volume spike detected but GEX did not move enough to confirm<br>
                🔶 <b style="color:#64748b">Extreme 4σ+ / Strong 3σ+</b> = Severity bands in Z-Score panel
                </div>
                """, unsafe_allow_html=True)

            spike_fig, df_spikes = create_intraday_timeline_with_spikes(df, unit_label, z_thresh)
            st.plotly_chart(spike_fig, use_container_width=True)

            st.markdown("#### 🔍 Detected Spike Events")
            spike_summary = build_spike_summary(df_spikes, unit_label)

            if spike_summary.empty:
                st.info(f"No volume spikes detected at {z_thresh}σ threshold. Try lowering the slider.")
            else:
                def _row_color(row):
                    c = {'CONFIRMED_BULLISH':'background-color:rgba(16,185,129,0.12)',
                         'CONFIRMED_BEARISH':'background-color:rgba(239,68,68,0.12)',
                         'DIVERGENCE':       'background-color:rgba(245,158,11,0.12)',
                         'UNCONFIRMED':      'background-color:rgba(139,92,246,0.08)'}.get(row['GEX Signal'],'')
                    return [c] * len(row)

                st.dataframe(spike_summary.style.apply(_row_color, axis=1),
                             use_container_width=True, hide_index=True)

                k1,k2,k3,k4,k5 = st.columns(5)
                k1.metric("Total Spikes",         len(spike_summary))
                k2.metric("🚀 Confirmed Bullish", (spike_summary['GEX Signal']=='CONFIRMED_BULLISH').sum())
                k3.metric("💥 Confirmed Bearish", (spike_summary['GEX Signal']=='CONFIRMED_BEARISH').sum())
                k4.metric("⚠️ Divergence",        (spike_summary['GEX Signal']=='DIVERGENCE').sum())
                k5.metric("🔥 Extreme (4σ+)",     (spike_summary['Strength']=='EXTREME').sum())

                st.download_button(
                    "📥 Download Spike Log (CSV)",
                    data=spike_summary.to_csv(index=False),
                    file_name=f"nyztrade_spikes_{meta.get('symbol','')}.csv",
                    mime="text/csv",
                )

        # ── TAB 1: Standard GEX ───────────────────────────────────────────────
        with tabs[1]:
            st.markdown("### 🎯 Standard Gamma Exposure (GEX)")
            st.plotly_chart(create_separate_gex_chart(df_selected, spot_price, unit_label), use_container_width=True)
            c1,c2,c3 = st.columns(3)
            c1.metric("Positive GEX", f"{df_selected[df_selected['net_gex']>0]['net_gex'].sum():.4f}{unit_label}")
            c2.metric("Negative GEX", f"{df_selected[df_selected['net_gex']<0]['net_gex'].sum():.4f}{unit_label}")
            c3.metric("Total Volume",  f"{df_selected.get('total_volume', pd.Series([0])).sum():,.0f}" if 'total_volume' in df_selected.columns else "N/A")

        # ── TAB 2: Enhanced GEX Overlay ───────────────────────────────────────
        with tabs[2]:
            st.markdown("### 🚀 Enhanced GEX Overlay")
            st.plotly_chart(create_enhanced_gex_overlay_chart(df_selected, spot_price, unit_label), use_container_width=True)
            c1,c2,c3,c4 = st.columns(4)
            orig_t = df_selected['net_gex'].sum()
            c1.metric("Original GEX Total", f"{orig_t:.4f}{unit_label}")
            c4.metric("Total Volume", f"{df_selected['total_volume'].sum():,.0f}" if 'total_volume' in df_selected.columns else "N/A")

        # ── TAB 3: Significant GEX ────────────────────────────────────────────
        with tabs[3]:
            st.markdown("### 🎯 Significant GEX: Addition vs Unwind")
            sig_fig, df_classified = create_significant_gex_chart(df_selected, spot_price, unit_label)
            st.plotly_chart(sig_fig, use_container_width=True)

            st.markdown("#### 📊 High-Significance Strikes")
            strong_only = df_classified[df_classified['gex_category'].isin(['STRONG_ADD','STRONG_UNWIND'])
                                       ].sort_values('significance_pct', ascending=False)
            if not strong_only.empty:
                disp_cols = [c for c in ['strike','gex_category','significance_pct','net_gex',
                                         'call_oi_change','put_oi_change','total_volume'] if c in strong_only.columns]
                def _cat_color(val):
                    if val == 'STRONG_ADD':    return 'background-color:rgba(16,185,129,0.25)'
                    if val == 'STRONG_UNWIND': return 'background-color:rgba(239,68,68,0.25)'
                    return ''
                st.dataframe(strong_only[disp_cols].style.applymap(_cat_color, subset=['gex_category']),
                             use_container_width=True, height=300)
                k1,k2,k3,k4 = st.columns(4)
                k1.metric("🟢 Strong Additions",  (df_classified['gex_category']=='STRONG_ADD').sum())
                k2.metric("🔴 Strong Unwinds",    (df_classified['gex_category']=='STRONG_UNWIND').sum())
                k3.metric("⬜ Noise Strikes",      (df_classified['gex_category']=='NOISE').sum())
                top_str = strong_only.iloc[0]['strike'] if not strong_only.empty else 'N/A'
                k4.metric("⭐ Most Significant",  f"₹{top_str:,.0f}" if isinstance(top_str,(int,float)) else top_str)
            else:
                st.info("No strongly significant GEX moves at this timestamp. Try a different time point.")

        # ── TAB 4: Standard VANNA ─────────────────────────────────────────────
        with tabs[4]:
            st.markdown("### 🌊 Standard VANNA Exposure")
            st.plotly_chart(create_standard_vanna_chart(df_selected, spot_price, unit_label), use_container_width=True)
            c1,c2,c3 = st.columns(3)
            c1.metric("Call VANNA", f"{df_selected['call_vanna'].sum():.4f}{unit_label}")
            c2.metric("Put VANNA",  f"{df_selected['put_vanna'].sum():.4f}{unit_label}")
            c3.metric("Net VANNA",  f"{df_selected['net_vanna'].sum():.4f}{unit_label}")

        # ── TAB 5: Enhanced VANNA Overlay + Flip Breakout ────────────────────
        with tabs[5]:
            st.markdown("### 🌊 Enhanced VANNA Overlay + ⚡ VANNA Flip Breakout Probability")
            st.markdown("""<div class="spike-legend">
            🔴 <b style="color:#ef4444">Resistance Ceiling</b> = POS→NEG flip above spot — IV↑ forces dealers to SELL delta → breakdown accelerates<br>
            🚀 <b style="color:#10b981">Vacuum Zone</b> = NEG→POS flip above spot — IV↑ forces dealers to BUY delta → fast squeeze UP<br>
            ⚠️ <b style="color:#f59e0b">Trap Door</b> = POS→NEG flip below spot — IV↑ below = drop accelerates with no support<br>
            🛡️ <b style="color:#06b6d4">Support Floor</b> = NEG→POS flip below spot — IV compression = dealers buy delta, price held<br>
            <b>Probability score</b> = distance × IV regime × VANNA magnitude × TTE × skew. Above 70% = high institutional activity expected.
            </div>""", unsafe_allow_html=True)

            tte_days = 7 if meta.get('expiry_flag','WEEK') == 'WEEK' else 30
            tte_val  = tte_days / 365

            # ── Step 1: build full-day IV trend, then slice to selected_ts ──
            # All signals (banner, table, chart title) must reflect the same moment.
            iv_df_full = compute_iv_trend(df)     # full day — needed for chart sparkline
            if 'timestamp' in iv_df_full.columns and len(iv_df_full) > 0:
                iv_at_ts = iv_df_full[iv_df_full['timestamp'] <= selected_ts]
                if iv_at_ts.empty:
                    iv_at_ts = iv_df_full.iloc[:1]
            else:
                iv_at_ts = iv_df_full

            # ── Step 2: flip zones & bias — all use iv_at_ts ─────────────
            vf_zones  = identify_vanna_flip_zones(df_selected, spot_price)
            bias_data = compute_session_bias(vf_zones, iv_at_ts, df_selected, spot_price)
            prob_df   = compute_breakout_probability(vf_zones, iv_at_ts, spot_price, tte_val, df_selected)

            # ── Step 3: extract iv scalars for this timestamp ─────────────
            _raw_iv = iv_at_ts.iloc[-1]
            latest_iv = {
                'iv_regime': str(_raw_iv['iv_regime'])  if 'iv_regime' in _raw_iv.index else 'N/A',
                'iv_skew'  : float(_raw_iv['iv_skew'])  if 'iv_skew'   in _raw_iv.index else 0.0,
                'call_iv'  : float(_raw_iv['call_iv'])  if 'call_iv'   in _raw_iv.index else 0.0,
                'put_iv'   : float(_raw_iv['put_iv'])   if 'put_iv'    in _raw_iv.index else 0.0,
            }

            # ── Step 4: render chart — pass iv_at_ts so title also reflects ts ─
            enh_fig, _, _ = create_enhanced_vanna_overlay_chart(
                df_selected, spot_price, unit_label,
                df_full=df, tte=tte_val, iv_df_override=iv_at_ts
            )
            st.plotly_chart(enh_fig, use_container_width=True)

            # ── Volume Spike × VANNA Coincidence panel ────────────────────
            with st.expander("⚡ Volume Spike × VANNA Coincidence", expanded=True):
                _spike_z = st.slider(
                    "Spike sensitivity (Z-threshold)", 1.5, 4.0, 2.0, 0.1,
                    key="vanna_spike_z",
                    help="Lower = more spikes. 2.0σ = moderate, 3.0σ = strong only.",
                )
                _sp_fig, _sp_df = create_vanna_spike_panel(df, unit_label, z_threshold=_spike_z)
                st.plotly_chart(_sp_fig, use_container_width=True)
                _sp_events = _sp_df[_sp_df['vol_spike']][
                    ['timestamp','spike_type','spike_strength','gex_confirmation','vol_z_score']
                ].rename(columns={
                    'timestamp'      : 'Time',
                    'spike_type'     : 'Type',
                    'spike_strength' : 'Strength',
                    'gex_confirmation': 'GEX Confirmation',
                    'vol_z_score'    : 'Z-Score',
                })
                if not _sp_events.empty:
                    _sp_events['Time'] = _sp_events['Time'].dt.strftime('%H:%M')
                    _sp_events['Z-Score'] = _sp_events['Z-Score'].round(2)
                    st.dataframe(_sp_events, use_container_width=True, hide_index=True)

            bull_pct   = bias_data['bull_pct']
            bear_pct   = bias_data['bear_pct']
            bias       = bias_data['bias']
            confidence = bias_data['confidence']
            iv_regime  = bias_data['iv_regime']
            iv_skew    = bias_data['iv_skew']

            # ── Session bias banner ───────────────────────────────────────
            bias_cfg = {
                'BULLISH'   : ('#10b981', '🟢 BULLISH BIAS'),
                'BEARISH'   : ('#ef4444', '🔴 BEARISH BIAS'),
                'CONFLICTED': ('#f59e0b', '⚡ CONFLICTED'),
            }
            bc, bl = bias_cfg.get(bias, ('#64748b','⬜ NEUTRAL'))
            conf_color = {'HIGH':'#10b981','MODERATE':'#f59e0b','LOW':'#64748b'}[confidence]
            rc = {'EXPANDING':'#ef4444','COMPRESSING':'#10b981','FLAT':'#94a3b8'}.get(iv_regime,'#94a3b8')

            st.markdown(f"""
            <div style="display:flex;gap:10px;align-items:stretch;margin:8px 0 16px 0;flex-wrap:wrap;">
              <!-- Bullish gauge -->
              <div style="flex:1;min-width:160px;padding:14px 18px;
                   background:rgba(16,185,129,0.10);border:1.5px solid rgba(16,185,129,0.45);
                   border-radius:12px;text-align:center;">
                <div style="font-size:2rem;font-weight:800;color:#10b981;
                     font-family:'JetBrains Mono',monospace;">{bull_pct:.0f}%</div>
                <div style="font-size:0.85rem;color:#10b981;margin-top:2px;">🟢 BULLISH PROBABILITY</div>
                <div style="background:rgba(16,185,129,0.2);border-radius:6px;height:6px;margin-top:8px;">
                  <div style="background:#10b981;width:{bull_pct}%;height:6px;border-radius:6px;"></div>
                </div>
              </div>
              <!-- Direction verdict -->
              <div style="flex:1;min-width:180px;padding:14px 18px;
                   background:{bc}18;border:2px solid {bc}55;
                   border-radius:12px;text-align:center;">
                <div style="font-size:1.3rem;font-weight:800;color:{bc};
                     font-family:'JetBrains Mono',monospace;">{bl}</div>
                <div style="font-size:0.78rem;color:{conf_color};margin-top:6px;">
                  Confidence: <b>{confidence}</b></div>
                <div style="font-size:0.75rem;color:#94a3b8;margin-top:4px;">
                  IV: <span style="color:{rc}"><b>{iv_regime}</b></span> |
                  Skew: <span style="color:{'#10b981' if iv_skew>0 else '#ef4444'}">{iv_skew:+.1f}%</span>
                </div>
              </div>
              <!-- Bearish gauge -->
              <div style="flex:1;min-width:160px;padding:14px 18px;
                   background:rgba(239,68,68,0.10);border:1.5px solid rgba(239,68,68,0.45);
                   border-radius:12px;text-align:center;">
                <div style="font-size:2rem;font-weight:800;color:#ef4444;
                     font-family:'JetBrains Mono',monospace;">{bear_pct:.0f}%</div>
                <div style="font-size:0.85rem;color:#ef4444;margin-top:2px;">🔴 BEARISH PROBABILITY</div>
                <div style="background:rgba(239,68,68,0.2);border-radius:6px;height:6px;margin-top:8px;">
                  <div style="background:#ef4444;width:{bear_pct}%;height:6px;border-radius:6px;"></div>
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

            # ── Bias Transition Chart ─────────────────────────────────────
            st.markdown("#### 📊 Bull vs Bear Probability Transition")
            transition_fig = create_bias_transition_chart(df, spot_price, selected_ts, tte_val)
            st.plotly_chart(transition_fig, use_container_width=True)

            # ── Signal breakdown ──────────────────────────────────────────
            with st.expander("📡 Signal Breakdown (4 independent signals)"):
                for line in bias_data['lines']:
                    st.markdown(f"• {line}")
                st.markdown(f"""
                **VANNA Balance:** {bias_data['vanna_balance_pct']:.1f}% of flip magnitude above spot
                (>50% = IV expansion pushes price UP more than DOWN)

                **Net VANNA above spot:** `{bias_data['net_vanna_above']:.4f}` |
                **below spot:** `{bias_data['net_vanna_below']:.4f}`
                """)

            # ── KPI strip ─────────────────────────────────────────────────
            k1,k2,k3,k4,k5,k6 = st.columns(6)
            k1.metric("Flip Zones",    len(vf_zones))
            k2.metric("🚀 Vacuum",    sum(1 for z in vf_zones if z['role']=='VACUUM_ZONE'))
            k3.metric("🔴 Resistance",sum(1 for z in vf_zones if z['role']=='RESISTANCE_CEILING'))
            k4.metric("⚠️ Trap Doors",sum(1 for z in vf_zones if z['role']=='TRAP_DOOR'))
            k5.metric("IV Regime",     latest_iv.get('iv_regime', 'N/A'))
            k6.metric("IV Skew",       f"{latest_iv.get('iv_skew', 0.0):+.1f}%")

            # ── Directional probability table ──────────────────────────────
            if not prob_df.empty:
                st.markdown("#### 🎯 Flip Zone Directional Probability")

                def _prob_bg(row):
                    d = row.get('Direction','')
                    if 'BULLISH'    in str(d): return ['background-color:rgba(16,185,129,0.15)']*len(row)
                    if 'BEARISH'    in str(d): return ['background-color:rgba(239,68,68,0.15)']*len(row)
                    if 'CONFLICTED' in str(d): return ['background-color:rgba(245,158,11,0.12)']*len(row)
                    return ['']*len(row)

                # Build display table — no empty-string column names
                dp = prob_df[[
                    'strike','role','distance_pct',
                    'bull_score','bear_score','final_score',
                    'direction','dir_icon','signal','iv_regime'
                ]].copy()
                # Combine icon into Direction string before renaming
                dp['direction'] = prob_df['dir_icon'] + ' ' + prob_df['direction']
                dp.columns = [
                    'Strike','Role','Dist%',
                    '🟢 Bull%','🔴 Bear%','Best%',
                    'Direction','_drop','Signal','IV'
                ]
                dp.drop(columns=['_drop'], inplace=True)
                dp['Strike'] = dp['Strike'].apply(lambda x: f"₹{x:,.0f}")
                dp['Dist%']  = dp['Dist%'].apply(lambda x: f"{x:.2f}%")
                for c in ['🟢 Bull%','🔴 Bear%','Best%']:
                    dp[c] = dp[c].apply(lambda x: f"{x:.1f}%")

                st.dataframe(dp.style.apply(_prob_bg, axis=1),
                             use_container_width=True, hide_index=True,
                             height=min(420, 44 + len(dp)*40))

                # ── Top zone trade guidance card ──────────────────────────
                top = prob_df.iloc[0]
                is_bull = top['direction'] == 'BULLISH'
                is_bear = top['direction'] == 'BEARISH'

                guidance = {
                    ('VACUUM_ZONE',     True ): ("🚀 SQUEEZE SETUP",
                        f"₹{top['strike']:,.0f} Vacuum zone. IV expanding → dealers BUY delta above. "
                        f"Bull score {top['bull_score']:.0f}% vs Bear {top['bear_score']:.0f}%. "
                        f"Enter: break+close above ₹{top['strike']:,.0f}. "
                        f"Target: next VANNA flip zone above. Stop: below entry 0.5%."),
                    ('VACUUM_ZONE',     False): ("📉 VACUUM FADE",
                        f"₹{top['strike']:,.0f} Vacuum zone but IV compressing. "
                        f"Dealers selling delta. Bear score {top['bear_score']:.0f}%. "
                        f"Expect price to fall away from this zone rather than squeeze through it."),
                    ('RESISTANCE_CEILING', False): ("🔴 BREAKDOWN WATCH",
                        f"₹{top['strike']:,.0f} Resistance ceiling. IV expanding → dealers SELL delta. "
                        f"Bear score {top['bear_score']:.0f}% vs Bull {top['bull_score']:.0f}%. "
                        f"Enter: break+close below ceiling with IV rising. "
                        f"Target: next VANNA flip support below. Stop: reclaim ceiling."),
                    ('RESISTANCE_CEILING', True ): ("🟢 CEILING ABSORBED",
                        f"₹{top['strike']:,.0f} Resistance ceiling but IV compressing. "
                        f"Dealers absorbing. Bull score {top['bull_score']:.0f}%. "
                        f"Slow grind up likely if IV stays flat. Not a momentum trade."),
                    ('TRAP_DOOR',       False): ("⚠️ TRAP DOOR ARMED",
                        f"₹{top['strike']:,.0f} trap door below spot. IV expanding → drop accelerates below. "
                        f"Bear score {top['bear_score']:.0f}%. "
                        f"High-vol candle below this level = acceleration. "
                        f"No natural support until next VANNA flip below."),
                    ('TRAP_DOOR',       True ): ("🛡️ TRAP DOOR HEALING",
                        f"₹{top['strike']:,.0f} below spot. IV compressing → dealers buying. "
                        f"Bull score {top['bull_score']:.0f}%. Bounce likely from this zone."),
                    ('SUPPORT_FLOOR',   True ): ("🛡️ SUPPORT ACTIVE",
                        f"₹{top['strike']:,.0f} VANNA support floor. IV compressing → dealers buy delta. "
                        f"Bull score {top['bull_score']:.0f}%. "
                        f"Hold long while IV stays flat/falling near this level. "
                        f"Invalidated if IV starts expanding."),
                    ('SUPPORT_FLOOR',   False): ("💥 FLOOR BREAKING",
                        f"₹{top['strike']:,.0f} VANNA floor but IV EXPANDING. "
                        f"Bear score {top['bear_score']:.0f}%. "
                        f"Floor breaks under vol expansion — dealers forced to SELL delta. "
                        f"Short signal if price closes below ₹{top['strike']:,.0f}."),
                }
                key  = (top['role'], is_bull)
                lbl, desc = guidance.get(key, ("📊 MONITOR","Watch this level closely."))
                card_col = '#10b981' if is_bull else ('#ef4444' if is_bear else '#f59e0b')

                st.markdown(f"""
                <div style="margin-top:14px;padding:14px 20px;
                     background:{card_col}12;border:1.5px solid {card_col}45;
                     border-radius:12px;font-family:'JetBrains Mono',monospace;">
                  <div style="display:flex;justify-content:space-between;align-items:center;">
                    <b style="color:{card_col};font-size:1rem;">{lbl}</b>
                    <span style="font-size:0.78rem;color:#94a3b8;">
                      {top['dir_icon']} {top['direction']} | {top['signal']}
                    </span>
                  </div>
                  <div style="font-size:0.81rem;color:#cbd5e1;line-height:1.75;margin-top:8px;">
                    {desc}
                  </div>
                  <div style="display:flex;gap:20px;margin-top:10px;font-size:0.75rem;color:#64748b;">
                    <span>🟢 Bull: <b style="color:#10b981">{top['bull_score']:.0f}%</b></span>
                    <span>🔴 Bear: <b style="color:#ef4444">{top['bear_score']:.0f}%</b></span>
                    <span>IV: <b style="color:{rc}">{iv_regime}</b></span>
                    <span>Skew: {iv_skew:+.1f}%</span>
                    <span>Dist: {top['distance_pct']:.2f}%</span>
                  </div>
                </div>
                """, unsafe_allow_html=True)

                st.download_button("📥 Download Directional Analysis CSV",
                    data=prob_df.to_csv(index=False),
                    file_name=f"vanna_directional_{meta.get('symbol','')}.csv",
                    mime="text/csv")
            else:
                st.info("No VANNA flip zones found. Select wider strikes (ATM±5 or more).")

        # ── TAB 6: DEX ────────────────────────────────────────────────────────
        with tabs[6]:
            st.markdown("### 📊 Delta Exposure (DEX)")
            st.plotly_chart(create_dex_chart(df_selected, spot_price, unit_label), use_container_width=True)
            c1,c2,c3 = st.columns(3)
            c1.metric("Call DEX", f"{df_selected['call_dex'].sum():.4f}{unit_label}")
            c2.metric("Put DEX",  f"{df_selected['put_dex'].sum():.4f}{unit_label}")
            c3.metric("Net DEX",  f"{df_selected['net_dex'].sum():.4f}{unit_label}")

        # ── TAB 7: OI Distribution ────────────────────────────────────────────
        with tabs[7]:
            st.markdown("### 📋 Open Interest Distribution")
            st.plotly_chart(create_oi_distribution_chart(df_selected, spot_price), use_container_width=True)

        # ── TAB 8: Data Table ─────────────────────────────────────────────────
        with tabs[8]:
            st.markdown("### 📁 Data Summary")
            st.markdown(f"""
            **Symbol**: {meta.get('symbol',symbol)} ({meta.get('instrument_type','INDEX')})
            | **Fetch Mode**: {fetch_mode.upper()}
            | **Last Fetch**: {meta.get('fetch_time','N/A')}
            | **Total Records**: {meta.get('total_records',0)}
            | **Time Range**: {meta.get('time_range','N/A')}
            | **Contract Size**: {meta.get('contract_size','N/A')}
            | **Unit**: ₹ {unit_label}
            """)
            disp = ['strike','net_gex','net_dex','net_vanna','total_volume','call_volume','put_volume',
                    'call_oi','put_oi','call_iv','put_iv']
            avail = [c for c in disp if c in df_selected.columns]
            st.dataframe(df_selected[avail], use_container_width=True, height=400)
            st.download_button("📥 Download Data (CSV)", data=df_selected.to_csv(index=False),
                               file_name=f"nyztrade_{meta.get('symbol',symbol)}_{target_date}.csv", mime="text/csv",
                               use_container_width=True)

    else:
        st.info("""
        👋 **Welcome to NYZTrade UNIFIED Dashboard!**

        **New in this version — Volume Spike Detection (Tab 0):**
        - 🚀 Confirmed Bullish = Call-dominant spike + GEX rising
        - 💥 Confirmed Bearish = Put-dominant spike + GEX falling
        - ⚠️ Divergence = Volume & GEX conflict — wait for resolution
        - 📊 Unconfirmed = Volume spike but GEX flat
        - Adjustable σ threshold slider for sensitivity control
        - Downloadable spike log CSV

        **New — Significant GEX Tab (Tab 3):**
        - Separates Strong Additions from Strong Unwinds
        - Classifies noise/residual OI automatically
        - Significance score overlay line

        **Select your instrument and click 🚀 Fetch Data to begin!**
        """)

    st.markdown("---")
    st.markdown(f"""
    <div style="text-align:center;padding:20px;color:#64748b;">
        <p style="font-family:'JetBrains Mono',monospace;font-size:0.85rem;">
            NYZTrade Unified GEX/DEX Dashboard | INDEX + STOCK Options<br>
            Smart Caching | VANNA/CHARM | Gamma Flip Zones | Volume Spike Detection | Significant GEX | Drawing Tools
        </p>
        <p style="font-size:0.75rem;margin-top:8px;">
            ⚠️ For educational and research purposes only. Not financial advice.
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
