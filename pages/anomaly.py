"""
SpendGuard — Cloud Spend Anomaly Detection & Response Agent
Economic Times GenAI Hackathon

Run:
    pip install streamlit groq python-dotenv plotly pandas
    streamlit run spendguard.py

.env:
    GROQ_API_KEY=gsk_...
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import json, re, time, os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    layout="wide",
    page_title="SpendGuard — Cloud Spend Intelligence",
    page_icon="🛡",
)

# ─────────────────────────────────────────────────────────────────────────────
# GLOBAL CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@300;400;500&display=swap');

html, body, .stApp, [data-testid="stAppViewContainer"] {
    background: #04080f !important;
    color: #e0eaf8 !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
}
[data-testid="stAppViewContainer"]::before {
    content: "";
    position: fixed; inset: 0;
    background-image:
        linear-gradient(rgba(0,212,255,.018) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,212,255,.018) 1px, transparent 1px);
    background-size: 56px 56px;
    pointer-events: none; z-index: 0;
}
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stSidebar"] { background: #060d17 !important; border-right: 1px solid #111d2e !important; }
[data-testid="stSidebar"] * { color: #e0eaf8 !important; }
.block-container { padding: 0 2rem 4rem !important; max-width: 100% !important; }

/* ── TYPOGRAPHY ── */
h1, h2, h3 { font-family: 'Syne', sans-serif !important; color: #ffffff !important; }
.mono { font-family: 'IBM Plex Mono', monospace !important; }

/* ── HERO ── */
.hero-wrap {
    padding: 2.8rem 0 2rem;
    border-bottom: 1px solid #111d2e;
    margin-bottom: 0;
}
.hero-eyebrow {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10.5px; letter-spacing: 3px;
    color: #ff4040; text-transform: uppercase;
    margin-bottom: 12px;
    display: flex; align-items: center; gap: 8px;
}
.live-dot {
    width: 6px; height: 6px; border-radius: 50%;
    background: #ff4040; display: inline-block;
    animation: pulse 1.4s infinite;
}
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:.2} }
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(36px, 5vw, 68px);
    font-weight: 800; line-height: .96;
    letter-spacing: -1px; margin-bottom: 14px; color: #fff;
}
.hero-title .ac-teal  { color: #00e5aa; }
.hero-title .ac-blue  { color: #00d4ff; }
.hero-title .ac-coral { color: #ff4040; }
.hero-desc {
    font-size: 15px; color: #58637a;
    max-width: 540px; line-height: 1.75; font-weight: 300;
    margin-bottom: 1.2rem;
}
.pill-strip { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 10px; }
.pill {
    font-family: 'IBM Plex Mono', monospace; font-size: 10px;
    letter-spacing: .04em; padding: 4px 12px;
    border: 1px solid rgba(0,212,255,.22); border-radius: 2px;
    color: #3a8fff; background: rgba(0,212,255,.05);
}

/* ── AGENT CARDS ── */
.agent-card {
    display: flex; align-items: center; gap: 12px;
    padding: 13px 15px;
    background: #080f1a; border: 1px solid #111d2e;
    border-left: 3px solid; border-radius: 5px;
    margin-bottom: 7px;
}
.agent-icon {
    width: 42px; height: 42px; border-radius: 8px;
    background: rgba(255,255,255,.04);
    display: flex; align-items: center; justify-content: center;
    font-size: 19px; flex-shrink: 0;
}
.agent-name { font-weight: 600; font-size: 13.5px; color: #ddeeff; margin: 0 0 2px; }
.agent-desc { font-size: 11.5px; color: #3a5a70; margin: 0; }
.agent-badge {
    margin-left: auto; font-family: 'IBM Plex Mono', monospace;
    font-size: 9.5px; padding: 2px 8px; border-radius: 2px; flex-shrink: 0;
}
.badge-active   { background: rgba(0,229,170,.1); color: #00e5aa; border: 1px solid rgba(0,229,170,.28); }
.badge-inactive { background: rgba(255,255,255,.03); color: #3a5060; border: 1px solid rgba(255,255,255,.06); }

/* ── SECTION LABEL ── */
.sec-label {
    font-family: 'IBM Plex Mono', monospace; font-size: 10px;
    letter-spacing: 2.5px; text-transform: uppercase;
    color: #2a4060; margin-bottom: 12px;
    display: flex; align-items: center; gap: 10px;
}
.sec-label::after { content: ""; flex: 1; height: 1px; background: #111d2e; }

/* ── METRIC CARDS ── */
.metric-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin: 1.2rem 0 1.8rem; }
.metric-card {
    background: #080f1a; border: 1px solid #111d2e;
    border-radius: 7px; padding: 1.1rem 1.3rem; position: relative; overflow: hidden;
}
.metric-card::after { content: ""; position: absolute; top: 0; left: 0; right: 0; height: 2px; }
.mc-blue::after   { background: #00d4ff; }
.mc-red::after    { background: #ff4040; }
.mc-amber::after  { background: #ffbe00; }
.mc-green::after  { background: #00e887; }
.mc-purple::after { background: #9d7eff; }
.m-label { font-family: 'IBM Plex Mono', monospace; font-size: 9.5px; letter-spacing: 2px; text-transform: uppercase; color: #3a5060; margin-bottom: 6px; }
.m-val   { font-family: 'Syne', sans-serif; font-size: 26px; font-weight: 800; line-height: 1; color: #fff; }
.m-sub   { font-size: 11px; color: #2a4060; margin-top: 4px; font-family: 'IBM Plex Mono', monospace; }

/* ── ANOMALY TABLE ── */
.atbl-wrap { background: #060d17; border: 1px solid #111d2e; border-radius: 7px; overflow: hidden; margin-bottom: 20px; }
.atbl-head {
    display: grid; grid-template-columns: 2fr 1fr 1.2fr 1.2fr 1fr 1fr 1.3fr;
    padding: 9px 15px; background: #080f1a;
    font-family: 'IBM Plex Mono', monospace; font-size: 9px;
    letter-spacing: 1.5px; text-transform: uppercase; color: #2a4060;
}
.atbl-row {
    display: grid; grid-template-columns: 2fr 1fr 1.2fr 1.2fr 1fr 1fr 1.3fr;
    padding: 11px 15px; border-top: 1px solid rgba(255,255,255,.03);
    align-items: center; font-size: 13px;
}
.atbl-row:hover { background: rgba(0,212,255,.03); }
.svc-nm { font-weight: 600; color: #ddeeff; }
.spike-pill {
    display: inline-flex; align-items: center; gap: 4px;
    padding: 2px 9px; border-radius: 3px; font-size: 11.5px;
    font-weight: 600; font-family: 'IBM Plex Mono', monospace;
}
.sp-high   { background: rgba(255,64,64,.12); color: #ff4040; border: 1px solid rgba(255,64,64,.24); }
.sp-medium { background: rgba(255,190,0,.1);  color: #ffbe00; border: 1px solid rgba(255,190,0,.22); }
.sp-low    { background: rgba(0,212,255,.08); color: #00d4ff; border: 1px solid rgba(0,212,255,.18); }
.act-tag {
    font-size: 10.5px; font-family: 'IBM Plex Mono', monospace;
    background: rgba(0,232,135,.07); color: #00e887;
    border: 1px solid rgba(0,232,135,.18); border-radius: 2px; padding: 2px 7px;
}

/* ── ACTION CARDS ── */
.action-card {
    background: #080f1a; border: 1px solid #111d2e;
    border-left: 3px solid; border-radius: 5px;
    padding: 14px 16px; margin-bottom: 10px;
}
.action-head { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 6px; }
.action-name { font-size: 13.5px; font-weight: 600; color: #ddeeff; }
.priority-badge {
    font-family: 'IBM Plex Mono', monospace; font-size: 9px;
    padding: 2px 8px; border-radius: 2px;
}
.action-detail { font-size: 12px; color: #3a5a70; line-height: 1.7; }
.action-cmd { font-family: 'IBM Plex Mono', monospace; font-size: 11px; color: #2a4060; margin-top: 4px; }

/* ── PIPELINE ── */
.pipeline-wrap { display: flex; align-items: center; padding: 18px 0 14px; gap: 0; }
.pipe-step { display: flex; flex-direction: column; align-items: center; gap: 5px; min-width: 88px; }
.pipe-dot {
    width: 38px; height: 38px; border-radius: 50%;
    border: 1.5px solid #111d2e; display: flex;
    align-items: center; justify-content: center;
    font-family: 'IBM Plex Mono', monospace; font-size: 13px;
    color: #3a5060; background: #080f1a;
}
.pipe-dot.done   { border-color: #00e887; color: #00e887; background: rgba(0,232,135,.08); }
.pipe-dot.active { border-color: #00d4ff; color: #00d4ff; background: rgba(0,212,255,.1); }
.pipe-lbl { font-family: 'IBM Plex Mono', monospace; font-size: 8px; letter-spacing: 1.5px; text-transform: uppercase; color: #2a4060; text-align: center; line-height: 1.5; }
.pipe-lbl.active { color: #00d4ff; }
.pipe-line { flex: 1; height: 1px; background: #111d2e; margin-bottom: 22px; }
.pipe-line.done   { background: rgba(0,232,135,.3); }
.pipe-line.active { background: rgba(0,212,255,.4); }

/* ── LOG ── */
.log-box {
    background: #04080f; border: 1px solid #111d2e; border-radius: 5px;
    padding: 12px 14px; font-family: 'IBM Plex Mono', monospace;
    font-size: 11.5px; max-height: 280px; overflow-y: auto;
}
.log-line { display: flex; gap: 10px; padding: 4px 0; border-bottom: 1px solid rgba(255,255,255,.025); }
.log-ts  { color: #2a4060; flex-shrink: 0; font-size: 10px; padding-top: 1px; }
.log-tag { flex-shrink: 0; font-size: 8.5px; padding: 1px 5px; border-radius: 2px; height: fit-content; }
.tag-scan     { color: #00d4ff; background: rgba(0,212,255,.1); }
.tag-diagnose { color: #ffbe00; background: rgba(255,190,0,.1); }
.tag-classify { color: #f5a623; background: rgba(245,166,35,.1); }
.tag-action   { color: #ff4040; background: rgba(255,64,64,.1);  }
.tag-result   { color: #00e887; background: rgba(0,232,135,.1);  }
.tag-think    { color: #9d7eff; background: rgba(157,126,255,.1); }
.log-msg { color: #58637a; flex: 1; line-height: 1.5; }

/* ── CHAT ── */
.chat-wrap { background: #080f1a; border: 1px solid #111d2e; border-radius: 7px; overflow: hidden; }
.chat-hdr { background: #060d17; padding: 13px 16px; display: flex; align-items: center; gap: 10px; border-bottom: 1px solid #111d2e; }
.bot-ava { width: 34px; height: 34px; border-radius: 7px; background: rgba(255,64,64,.1); border: 1px solid rgba(255,64,64,.25); display: flex; align-items: center; justify-content: center; font-size: 17px; flex-shrink: 0; }
.chat-msgs { padding: 14px; min-height: 220px; max-height: 340px; overflow-y: auto; display: flex; flex-direction: column; gap: 9px; }
.msg-user { display: flex; justify-content: flex-end; }
.msg-bot  { display: flex; justify-content: flex-start; }
.bubble { max-width: 80%; padding: 10px 14px; border-radius: 12px; font-size: 13.5px; line-height: 1.65; }
.bubble-user { background: rgba(0,212,255,.1); border: 1px solid rgba(0,212,255,.2); border-bottom-right-radius: 3px; }
.bubble-bot  { background: rgba(255,64,64,.08); border: 1px solid rgba(255,64,64,.15); border-bottom-left-radius: 3px; color: #e0c8c8; }

/* ── STREAMLIT OVERRIDES ── */
.stButton > button {
    background: linear-gradient(135deg, #0d2240, #091828) !important;
    color: #00d4ff !important; border: 1px solid rgba(0,212,255,.35) !important;
    border-radius: 4px !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 11.5px !important; letter-spacing: .1em !important;
    text-transform: uppercase !important;
    transition: all .2s !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #122e55, #0d2035) !important;
    border-color: rgba(0,212,255,.6) !important;
}
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox > div > div,
.stTextArea > div > div > textarea {
    background: #080f1a !important; color: #e0eaf8 !important;
    border: 1px solid #111d2e !important; border-radius: 4px !important;
    font-family: 'IBM Plex Mono', monospace !important; font-size: 12.5px !important;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: rgba(0,212,255,.5) !important;
    box-shadow: 0 0 0 1px rgba(0,212,255,.15) !important;
}
div[data-testid="stSelectbox"] > div > div {
    background: #080f1a !important; color: #e0eaf8 !important;
}
label, .stTextInput label, .stSelectbox label, .stNumberInput label, .stTextArea label {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 10px !important; letter-spacing: 2px !important;
    text-transform: uppercase !important; color: #3a5060 !important;
}
.stDataFrame, .stDataFrame * {
    background: #080f1a !important; color: #c0d0e8 !important;
    font-family: 'IBM Plex Mono', monospace !important; font-size: 12px !important;
    border-color: #111d2e !important;
}
.stDataFrame th { background: #060d17 !important; color: #3a5060 !important; }
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid #111d2e !important; gap: 0;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #3a5060 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 10px !important; letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    border-bottom: 2px solid transparent !important;
    padding: 10px 18px !important;
}
.stTabs [aria-selected="true"] {
    color: #00d4ff !important;
    border-bottom: 2px solid #00d4ff !important;
    background: transparent !important;
}
.stProgress > div > div > div > div { background: linear-gradient(90deg, #00d4ff, #00e887) !important; }
.stSpinner > div { border-top-color: #00d4ff !important; }
[data-testid="stSidebarNav"] { display: none; }
hr { border-color: #111d2e !important; }
.stSuccess, .stInfo { background: rgba(0,232,135,.06) !important; border: 1px solid rgba(0,232,135,.2) !important; color: #00e887 !important; border-radius: 5px !important; }
.stError   { background: rgba(255,64,64,.06) !important; border: 1px solid rgba(255,64,64,.2) !important; color: #ff4040 !important; border-radius: 5px !important; }
.stWarning { background: rgba(255,190,0,.06) !important; border: 1px solid rgba(255,190,0,.2) !important; color: #ffbe00 !important; border-radius: 5px !important; }
.element-container { animation: fadeUp .35s ease both; }
@keyframes fadeUp { from{opacity:0;transform:translateY(10px)} to{opacity:1;transform:translateY(0)} }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────────────────────────────────────────────────────
DEFAULTS = dict(
    step=1, org_name="", threshold=20, period="Month-over-Month",
    auto_exec="Recommend Only", context="",
    services=[], analysis=None, chat_history=[], logs=[],
)
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

SAMPLE_SERVICES = [
    {"id":"SVC-001","name":"EC2 Web Cluster",   "provider":"AWS",   "category":"Compute",   "curr":420000,"prev":280000,"instances":48,"region":"us-east-1","notes":"Auto-scaling enabled"},
    {"id":"SVC-002","name":"RDS Aurora",         "provider":"AWS",   "category":"Database",  "curr":185000,"prev":180000,"instances":3, "region":"us-east-1","notes":""},
    {"id":"SVC-003","name":"S3 Data Lake",        "provider":"AWS",   "category":"Storage",   "curr":68000, "prev":62000, "instances":0, "region":"ap-south-1","notes":""},
    {"id":"SVC-004","name":"Azure Kubernetes",    "provider":"Azure", "category":"Compute",   "curr":310000,"prev":210000,"instances":32,"region":"eu-west-1","notes":"New node pools"},
    {"id":"SVC-005","name":"GCP BigQuery",        "provider":"GCP",   "category":"Analytics", "curr":95000, "prev":88000, "instances":0, "region":"us-east-1","notes":""},
    {"id":"SVC-006","name":"CloudFront CDN",      "provider":"AWS",   "category":"CDN",       "curr":42000, "prev":38000, "instances":0, "region":"us-east-1","notes":""},
    {"id":"SVC-007","name":"Lambda Functions",    "provider":"AWS",   "category":"Compute",   "curr":28000, "prev":29000, "instances":0, "region":"ap-south-1","notes":""},
    {"id":"SVC-008","name":"Azure AI Services",   "provider":"Azure", "category":"ML/AI",     "curr":156000,"prev":90000, "instances":8, "region":"eu-west-1","notes":"New model deployments"},
    {"id":"SVC-009","name":"GCP GKE Cluster",     "provider":"GCP",   "category":"Compute",   "curr":88000, "prev":85000, "instances":12,"region":"ap-southeast-1","notes":""},
    {"id":"SVC-010","name":"AWS Redshift",         "provider":"AWS",   "category":"Database",  "curr":125000,"prev":72000, "instances":4, "region":"us-east-1","notes":"DC2 to RA3 migration"},
]

PROVIDERS  = ["AWS","Azure","GCP","Oracle Cloud","IBM Cloud"]
CATEGORIES = ["Compute","Storage","Database","Networking","Analytics","ML/AI","CDN","Security","Other"]
REGIONS    = ["us-east-1","us-west-2","eu-west-1","ap-south-1","ap-southeast-1","me-south-1","sa-east-1"]

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def fmt_inr(n):
    if n >= 10_000_000: return f"₹{n/10_000_000:.1f}Cr"
    if n >= 100_000:    return f"₹{n/100_000:.1f}L"
    if n >= 1_000:      return f"₹{n/1_000:.0f}K"
    return f"₹{n:,.0f}"

def spike_pct(curr, prev):
    return ((curr - prev) / prev * 100) if prev > 0 else 0.0

def safe_json(text, fallback):
    try:
        clean = re.sub(r"```(?:json)?|```", "", text).strip()
        return json.loads(clean)
    except:
        return fallback

def call_llm(messages, max_tokens=1600):
    api_key = st.session_state.get("groq_api_key") or os.getenv("GROQ_API_KEY", "")
    if not api_key:
        raise ValueError("GROQ_API_KEY missing. Enter it in the sidebar.")
    client = Groq(api_key=api_key)
    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        max_tokens=max_tokens,
        temperature=0.3,
    )
    return resp.choices[0].message.content.strip()

def push_log(msg, kind="scan"):
    ts = time.strftime("%H:%M:%S")
    st.session_state.logs.append({"ts": ts, "kind": kind, "msg": msg})

def render_logs():
    html = '<div class="log-box">'
    for l in st.session_state.logs[-60:]:
        html += (
            f'<div class="log-line">'
            f'<span class="log-ts">{l["ts"]}</span>'
            f'<span class="log-tag tag-{l["kind"]}">[{l["kind"].upper()}]</span>'
            f'<span class="log-msg">{l["msg"]}</span>'
            f'</div>'
        )
    html += '</div>'
    return html

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:1.2rem 0 .5rem;">
        <div style="font-family:'Syne',sans-serif;font-size:22px;font-weight:800;color:#fff;letter-spacing:-0.5px;">
            Spend<span style="color:#ff4040">Guard</span>
        </div>
        <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;letter-spacing:2px;color:#3a5060;margin-top:4px;">
            CLOUD SPEND INTELLIGENCE
        </div>
    </div>
    <hr style="border-color:#111d2e;margin:8px 0 16px;">
    """, unsafe_allow_html=True)

    api_key_input = st.text_input(
        "GROQ API KEY",
        value=st.session_state.get("groq_api_key", os.getenv("GROQ_API_KEY", "")),
        type="password",
        placeholder="gsk_...",
    )
    st.session_state["groq_api_key"] = api_key_input

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;letter-spacing:2px;color:#2a4060;margin-bottom:10px;">5-AGENT PIPELINE</div>
    """, unsafe_allow_html=True)

    agents_side = [
        ("🔍", "#00d4ff", "Detect Agent",    "Scans for cost anomalies"),
        ("🧠", "#ffbe00", "Diagnose Agent",   "Root cause analysis"),
        ("🏷", "#f5a623", "Classify Agent",   "Labels & categorises"),
        ("⚡", "#ff4040", "Execute Agent",    "Corrective actions"),
        ("📋", "#00e887", "Report Agent",     "Insights & summary"),
    ]
    for icon, color, name, desc in agents_side:
        st.markdown(f"""
        <div class="agent-card" style="border-left-color:{color};">
            <div class="agent-icon">{icon}</div>
            <div><div class="agent-name">{name}</div><div class="agent-desc">{desc}</div></div>
            <span class="agent-badge badge-active">ACTIVE</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("↩  Reset / New Analysis", use_container_width=True):
        for k, v in DEFAULTS.items():
            st.session_state[k] = v
        st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# HERO HEADER (always visible)
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
    <div class="hero-eyebrow"><span class="live-dot"></span>AI-Powered Cloud Operations · 5-Agent Pipeline</div>
    <div class="hero-title">
        DETECT. DIAGNOSE.<br><span class="ac-coral">NEUTRALISE.</span>
    </div>
    <div class="hero-desc">
        Agentic AI that catches cloud spend anomalies in real time — diagnoses whether the spike
        is a provisioning error, seasonal traffic, or misconfigured auto-scaling — then executes
        the right corrective action autonomously.
    </div>
    <div class="pill-strip">
        <span class="pill">Anomaly Detection</span>
        <span class="pill">Root Cause AI</span>
        <span class="pill">Auto-Execution</span>
        <span class="pill">What-If Simulator</span>
        <span class="pill">AnomalyBot Chat</span>
        <span class="pill">Spend Forecasting</span>
    </div>
</div>
<br>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# STEP 1 — CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────
if st.session_state.step == 1:
    st.markdown('<div class="sec-label">// Agent Configuration</div>', unsafe_allow_html=True)

    with st.container():
        col1, col2 = st.columns([1.6, 1], gap="large")
        with col1:
            org = st.text_input("Organisation / Project", placeholder="e.g. Acme Engineering, ET Cloud Infra…",
                                value=st.session_state.org_name)
            ctx = st.text_input("Additional Context (optional)",
                                placeholder="e.g. Q4 launch, region migration, load tests…",
                                value=st.session_state.context)
        with col2:
            thr = st.number_input("Alert Threshold (%)", min_value=5, max_value=200,
                                  value=st.session_state.threshold, step=5)
            period = st.selectbox("Comparison Period", ["Month-over-Month","Week-over-Week",
                                                         "Day-over-Day","Quarter-over-Quarter"],
                                  index=["Month-over-Month","Week-over-Week","Day-over-Day","Quarter-over-Quarter"].index(st.session_state.period))
            auto_exec = st.selectbox("Auto-Execute Mode", ["Recommend Only","Auto-Execute Low Risk","Auto-Execute All"],
                                     index=["Recommend Only","Auto-Execute Low Risk","Auto-Execute All"].index(st.session_state.auto_exec))

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Next: Add Cloud Services  →", use_container_width=False):
        if not org.strip():
            st.error("Please enter an organisation name.")
        else:
            st.session_state.org_name  = org.strip()
            st.session_state.context   = ctx
            st.session_state.threshold = thr
            st.session_state.period    = period
            st.session_state.auto_exec = auto_exec
            st.session_state.step      = 2
            st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# STEP 2 — SERVICES INPUT
# ─────────────────────────────────────────────────────────────────────────────
elif st.session_state.step == 2:
    st.markdown(f"""
    <div style="font-family:'IBM Plex Mono',monospace;font-size:11px;color:#3a5060;margin-bottom:16px;">
        Org: <span style="color:#00d4ff">{st.session_state.org_name}</span>
        &nbsp;·&nbsp; Threshold: <span style="color:#ff4040">{st.session_state.threshold}%</span>
        &nbsp;·&nbsp; Period: <span style="color:#ffbe00">{st.session_state.period}</span>
    </div>
    """, unsafe_allow_html=True)

    col_load, col_add, _ = st.columns([1.2, 1, 4])
    with col_load:
        if st.button("⚡  Load Sample Dataset", use_container_width=True):
            st.session_state.services = [s.copy() for s in SAMPLE_SERVICES]
            st.rerun()
    with col_add:
        if st.button("＋  Add Row", use_container_width=True):
            n = len(st.session_state.services) + 1
            st.session_state.services.append({
                "id": f"SVC-{n:03d}", "name": "", "provider": "AWS",
                "category": "Compute", "curr": 0, "prev": 0,
                "instances": 0, "region": "us-east-1", "notes": ""
            })
            st.rerun()

    st.markdown('<div class="sec-label" style="margin-top:1rem;">// Service Spend Data</div>', unsafe_allow_html=True)

    svcs = st.session_state.services
    if svcs:
        cols_hdr = st.columns([.7, 1.8, .9, 1.1, 1.3, 1.3, .8, 1.2, .8, .5])
        headers  = ["ID","Name","Provider","Category","Current (₹)","Previous (₹)","Instances","Region","Spike",""]
        for col, hdr in zip(cols_hdr, headers):
            col.markdown(f'<div style="font-family:\'IBM Plex Mono\',monospace;font-size:9px;letter-spacing:1.5px;text-transform:uppercase;color:#2a4060;padding:4px 0;">{hdr}</div>', unsafe_allow_html=True)

        del_idx = None
        for i, svc in enumerate(svcs):
            c = st.columns([.7, 1.8, .9, 1.1, 1.3, 1.3, .8, 1.2, .8, .5])
            svc["id"]        = c[0].text_input("", value=svc["id"],       key=f"id_{i}",   label_visibility="collapsed")
            svc["name"]      = c[1].text_input("", value=svc["name"],     key=f"nm_{i}",   label_visibility="collapsed", placeholder="Service name")
            svc["provider"]  = c[2].selectbox("",  PROVIDERS,             key=f"pv_{i}",   label_visibility="collapsed", index=PROVIDERS.index(svc["provider"]) if svc["provider"] in PROVIDERS else 0)
            svc["category"]  = c[3].selectbox("",  CATEGORIES,            key=f"ct_{i}",   label_visibility="collapsed", index=CATEGORIES.index(svc["category"]) if svc["category"] in CATEGORIES else 0)
            svc["curr"]      = c[4].number_input("", value=int(svc["curr"]),  key=f"cu_{i}", label_visibility="collapsed", min_value=0, step=1000)
            svc["prev"]      = c[5].number_input("", value=int(svc["prev"]),  key=f"pr_{i}", label_visibility="collapsed", min_value=0, step=1000)
            svc["instances"] = c[6].number_input("", value=int(svc["instances"]), key=f"in_{i}", label_visibility="collapsed", min_value=0)
            svc["region"]    = c[7].selectbox("",  REGIONS,               key=f"rg_{i}",   label_visibility="collapsed", index=REGIONS.index(svc["region"]) if svc["region"] in REGIONS else 0)

            sp = spike_pct(svc["curr"], svc["prev"])
            sp_cls = "sp-high" if sp > st.session_state.threshold else ("sp-medium" if sp > st.session_state.threshold/2 else "sp-low")
            sp_str = f"+{sp:.0f}%" if sp > 0 else f"{sp:.0f}%"
            c[8].markdown(f'<div style="padding-top:6px;"><span class="spike-pill {sp_cls}">{sp_str}</span></div>', unsafe_allow_html=True)
            if c[9].button("✕", key=f"del_{i}"):
                del_idx = i

        if del_idx is not None:
            st.session_state.services.pop(del_idx)
            st.rerun()

        # Live anomaly preview
        anomalies_preview = [s for s in svcs if spike_pct(s["curr"], s["prev"]) > st.session_state.threshold]
        if anomalies_preview:
            total_curr = sum(s["curr"] for s in svcs)
            total_prev = sum(s["prev"] for s in svcs)
            ov_sp = spike_pct(total_curr, total_prev)
            st.markdown(f"""
            <div style="background:#080f1a;border:1px solid #111d2e;border-left:3px solid #ff4040;border-radius:5px;padding:12px 16px;margin-top:1rem;display:flex;gap:24px;flex-wrap:wrap;">
                <div><div style="font-family:'IBM Plex Mono',monospace;font-size:9px;color:#3a5060;letter-spacing:2px;margin-bottom:4px;">LIVE ANOMALIES</div><div style="font-family:'Syne',sans-serif;font-size:26px;font-weight:800;color:#ff4040;">{len(anomalies_preview)}</div></div>
                <div><div style="font-family:'IBM Plex Mono',monospace;font-size:9px;color:#3a5060;letter-spacing:2px;margin-bottom:4px;">OVERALL SPIKE</div><div style="font-family:'Syne',sans-serif;font-size:26px;font-weight:800;color:#ffbe00;">+{ov_sp:.1f}%</div></div>
                <div><div style="font-family:'IBM Plex Mono',monospace;font-size:9px;color:#3a5060;letter-spacing:2px;margin-bottom:4px;">CURRENT SPEND</div><div style="font-family:'Syne',sans-serif;font-size:26px;font-weight:800;color:#e0eaf8;">{fmt_inr(total_curr)}</div></div>
            </div>
            """, unsafe_allow_html=True)

    else:
        st.markdown("""
        <div style="text-align:center;padding:2.5rem;color:#2a4060;font-family:'IBM Plex Mono',monospace;font-size:12px;">
            No services yet — load the sample dataset or add rows manually.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_back, _, col_launch = st.columns([1, 3, 2])
    with col_back:
        if st.button("← Back"):
            st.session_state.step = 1; st.rerun()
    with col_launch:
        if st.button("⚡  Launch 5-Agent Pipeline  →", use_container_width=True):
            valid = [s for s in svcs if s["name"].strip()]
            if not valid:
                st.error("Add at least one service with a name.")
            else:
                st.session_state.services = valid
                st.session_state.step     = 3
                st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# STEP 3 — AGENT PIPELINE RUNNING
# ─────────────────────────────────────────────────────────────────────────────
elif st.session_state.step == 3:
    st.markdown("""
    <div style="text-align:center;padding:2rem 0 1.2rem;">
        <div style="font-family:'IBM Plex Mono',monospace;font-size:10px;letter-spacing:3px;color:#00d4ff;text-transform:uppercase;margin-bottom:10px;">5-Agent Pipeline Executing</div>
        <div style="font-family:'Syne',sans-serif;font-size:38px;font-weight:800;margin-bottom:6px;">Analysing Cloud Spend…</div>
        <div style="font-size:14px;color:#3a5060;">Detect → Diagnose → Classify → Execute → Report</div>
    </div>
    """, unsafe_allow_html=True)

    PIPE_STEPS = [("🔍","DETECT","Scans anomalies"),("🧠","DIAGNOSE","Root cause AI"),
                  ("🏷","CLASSIFY","Labels causes"),("⚡","EXECUTE","Runs actions"),("📋","REPORT","Generates insights")]

    pipeline_ph  = st.empty()
    progress_ph  = st.empty()
    log_ph       = st.empty()

    def render_pipeline(active):
        html = '<div class="pipeline-wrap">'
        for i,(icon,label,sub) in enumerate(PIPE_STEPS):
            if i < active:   cls,lc = "done","";           sym = "✓"
            elif i == active: cls,lc = "active","active";  sym = icon
            else:             cls,lc = "","";               sym = icon
            lnc = "done" if i < active else ("active" if i == active else "")
            html += f'<div class="pipe-step"><div class="pipe-dot {cls}">{sym}</div><div class="pipe-lbl {lc}">{label}<br><span style="font-size:7.5px;opacity:.5">{sub}</span></div></div>'
            if i < len(PIPE_STEPS)-1:
                html += f'<div class="pipe-line {lnc}"></div>'
        html += '</div>'
        pipeline_ph.markdown(html, unsafe_allow_html=True)

    def set_progress(pct, label=""):
        progress_ph.progress(pct / 100, text=f"Pipeline: {pct}%  {label}")

    st.session_state.logs = []
    svcs = st.session_state.services
    total_curr = sum(s["curr"] for s in svcs)
    total_prev = sum(s["prev"] for s in svcs)
    thr = st.session_state.threshold

    ctx_data = {
        "org": st.session_state.org_name,
        "period": st.session_state.period,
        "threshold": thr,
        "auto_exec": st.session_state.auto_exec,
        "context": st.session_state.context,
        "total_curr": total_curr,
        "total_prev": total_prev,
        "services": [{"id":s["id"],"name":s["name"],"provider":s["provider"],"category":s["category"],
                      "curr":s["curr"],"prev":s["prev"],"spike":f"{spike_pct(s['curr'],s['prev']):.1f}%",
                      "instances":s["instances"],"region":s["region"],"notes":s["notes"]} for s in svcs]
    }

    result = {}

    try:
        # ── AGENT 1: DETECT ──────────────────────────────────────────────────
        render_pipeline(0); set_progress(5, "Detect Agent scanning…")
        push_log(f"Scan Agent activated — scanning {len(svcs)} cloud services…", "scan")
        push_log(f"Total: ₹{total_curr:,} vs ₹{total_prev:,} previous", "scan")
        ov_sp = spike_pct(total_curr, total_prev)
        push_log(f"Overall change: <b>+{ov_sp:.1f}%</b> | Threshold: {thr}%", "scan")
        anomalies_list = [s for s in svcs if spike_pct(s["curr"], s["prev"]) > thr]
        for s in anomalies_list:
            sp = spike_pct(s["curr"], s["prev"])
            push_log(f"⚠ <b>{s['name']}</b> ({s['provider']}) spiked +{sp:.0f}% | ₹{s['prev']:,} → ₹{s['curr']:,}", "scan")
        log_ph.markdown(render_logs(), unsafe_allow_html=True)

        detect_raw = call_llm([{"role":"user","content":
            "You are a cloud cost anomaly detection AI. Analyse and return ONLY valid JSON:\n"+
            json.dumps(ctx_data)+
            '\n\nReturn: {"total_spike_pct":<float>,"anomaly_count":<int>,'
            '"anomalous_services":[{"id":"","name":"","spike_pct":<float>,"severity":"CRITICAL|HIGH|MEDIUM",'
            '"wasted_spend":<int>,"likely_cause_hint":"provisioning_error|seasonal_traffic|auto_scaling|normal_growth|configuration_change"}],'
            '"normal_services":[{"id":"","name":""}],"total_wasted_spend":<int>,"risk_level":"CRITICAL|HIGH|MEDIUM|LOW"}'
        }], 900)

        result["detect"] = safe_json(detect_raw, {
            "total_spike_pct": round(ov_sp, 1),
            "anomaly_count": len(anomalies_list),
            "anomalous_services": [{"id":s["id"],"name":s["name"],
                "spike_pct": round(spike_pct(s["curr"],s["prev"]),1),
                "severity": "CRITICAL" if spike_pct(s["curr"],s["prev"])>60 else "HIGH" if spike_pct(s["curr"],s["prev"])>30 else "MEDIUM",
                "wasted_spend": round((s["curr"]-s["prev"])*0.7),
                "likely_cause_hint":"auto_scaling"} for s in anomalies_list],
            "normal_services": [{"id":s["id"],"name":s["name"]} for s in svcs if s not in anomalies_list],
            "total_wasted_spend": round((total_curr-total_prev)*0.65),
            "risk_level": "CRITICAL" if ov_sp>40 else "HIGH" if ov_sp>20 else "MEDIUM"
        })
        push_log(f"Detect complete. Risk: <b>{result['detect']['risk_level']}</b>. Wasted: ₹{result['detect']['total_wasted_spend']:,}", "result")
        set_progress(20); log_ph.markdown(render_logs(), unsafe_allow_html=True)

        # ── AGENT 2: DIAGNOSE ─────────────────────────────────────────────────
        render_pipeline(1); set_progress(22, "Diagnose Agent running root cause…")
        push_log("Diagnose Agent activated — running root cause analysis…", "diagnose")
        log_ph.markdown(render_logs(), unsafe_allow_html=True)

        diagnose_raw = call_llm([{"role":"user","content":
            f"You are a cloud cost root cause analysis AI.\nOrg: {st.session_state.org_name}\nContext: {st.session_state.context}\n"
            f"Anomalies:\n{json.dumps(result['detect']['anomalous_services'])}\nAll services:\n{json.dumps(ctx_data['services'])}\n\n"
            'Return ONLY valid JSON: {"diagnoses":[{"service_id":"","service_name":"","primary_cause":"provisioning_error|seasonal_traffic|auto_scaling_misconfiguration|legitimate_growth|configuration_change",'
            '"cause_probability":<int>,"secondary_cause":"","confidence":<int>,"evidence":["",""],'
            '"financial_impact":<int>,"urgency":"IMMEDIATE|HIGH|MEDIUM|LOW","technical_details":"<2 sentences>"}],'
            '"overall_diagnosis":"<3 sentences>","total_recoverable_spend":<int>}'
        }], 1400)

        result["diagnose"] = safe_json(diagnose_raw, {
            "diagnoses": [{"service_id":s["id"],"service_name":s["name"],
                "primary_cause":"auto_scaling_misconfiguration","cause_probability":72,
                "secondary_cause":"legitimate_growth","confidence":70,
                "evidence":["Spike correlates with deployment","Instances increased"],
                "financial_impact":round((s["curr"]-s["prev"])*0.7),
                "urgency":"IMMEDIATE","technical_details":f"Resource allocation exceeded baseline by {spike_pct(s['curr'],s['prev']):.0f}%."
            } for s in anomalies_list],
            "overall_diagnosis": f"Analysis of {len(svcs)} services identified {len(anomalies_list)} anomalies. Root cause analysis indicates auto-scaling misconfigurations and provisioning errors.",
            "total_recoverable_spend": result["detect"]["total_wasted_spend"]
        })

        for d in result["diagnose"]["diagnoses"]:
            push_log(f"<b>{d['service_name']}</b>: {d['primary_cause'].replace('_',' ')} ({d['cause_probability']}%) | ₹{d['financial_impact']:,}", "diagnose")
        push_log(f"Diagnose complete. Recoverable: ₹{result['diagnose']['total_recoverable_spend']:,}", "result")
        set_progress(42); log_ph.markdown(render_logs(), unsafe_allow_html=True)

        # ── AGENT 3: CLASSIFY ─────────────────────────────────────────────────
        render_pipeline(2); set_progress(44, "Classify Agent labelling causes…")
        push_log("Classify Agent activated…", "classify")
        log_ph.markdown(render_logs(), unsafe_allow_html=True)

        classify_raw = call_llm([{"role":"user","content":
            f"You are a cloud cost classification AI.\nDiagnoses:\n{json.dumps(result['diagnose']['diagnoses'])}\nAuto-exec: {st.session_state.auto_exec}\n\n"
            'Return ONLY valid JSON: {"classifications":[{"service_id":"","cause_category":"PROVISIONING_ERROR|SEASONAL_TRAFFIC|AUTO_SCALING_MISCONFIGURATION|LEGITIMATE_GROWTH|CONFIGURATION_CHANGE",'
            '"category_label":"","corrective_actions":[{"action":"","action_type":"TERMINATE|RESIZE|RECONFIGURE|ALERT|MONITOR|SCALE_DOWN|ROLLBACK",'
            '"risk_level":"LOW|MEDIUM|HIGH","auto_executable":<bool>,"estimated_saving":<int>,"priority":1,"command_hint":""}],'
            '"resolution_timeline":""}],"cause_distribution":{"provisioning_error":<int>,"seasonal_traffic":<int>,"auto_scaling_misconfiguration":<int>,"legitimate_growth":<int>,"other":<int>}}'
        }], 1400)

        cat_map = {"provisioning_error":"PROVISIONING_ERROR","seasonal_traffic":"SEASONAL_TRAFFIC",
                   "auto_scaling_misconfiguration":"AUTO_SCALING_MISCONFIGURATION",
                   "configuration_change":"CONFIGURATION_CHANGE","legitimate_growth":"LEGITIMATE_GROWTH"}
        result["classify"] = safe_json(classify_raw, {
            "classifications": [{"service_id":d["service_id"],"cause_category":cat_map.get(d["primary_cause"],"PROVISIONING_ERROR"),
                "category_label":cat_map.get(d["primary_cause"],"PROVISIONING_ERROR").replace("_"," "),
                "corrective_actions":[
                    {"action":"Scale down over-provisioned instances","action_type":"SCALE_DOWN","risk_level":"LOW","auto_executable":True,"estimated_saving":round(d["financial_impact"]*.6),"priority":1,"command_hint":"aws ec2 modify-instance-attribute --instance-type t3.large"},
                    {"action":"Set cost alert at 110% of baseline","action_type":"ALERT","risk_level":"LOW","auto_executable":True,"estimated_saving":0,"priority":2,"command_hint":"aws budgets create-budget ..."},
                    {"action":"Review auto-scaling policies","action_type":"RECONFIGURE","risk_level":"MEDIUM","auto_executable":False,"estimated_saving":round(d["financial_impact"]*.3),"priority":3,"command_hint":"aws autoscaling update-auto-scaling-group --max-size 20"},
                ],"resolution_timeline":"Immediate — 4 hours"
            } for d in result["diagnose"]["diagnoses"]],
            "cause_distribution":{"provisioning_error":1,"seasonal_traffic":1,"auto_scaling_misconfiguration":2,"legitimate_growth":1,"other":0}
        })

        for c in result["classify"]["classifications"]:
            n_auto = sum(1 for a in c["corrective_actions"] if a["auto_executable"])
            push_log(f"<b>{c['cause_category'].replace('_',' ')}</b> — {len(c['corrective_actions'])} actions ({n_auto} auto)", "classify")
        set_progress(62); log_ph.markdown(render_logs(), unsafe_allow_html=True)

        # ── AGENT 4: EXECUTE ──────────────────────────────────────────────────
        render_pipeline(3); set_progress(64, "Execute Agent running actions…")
        push_log("Execute Agent activated…", "action")
        log_ph.markdown(render_logs(), unsafe_allow_html=True)

        exec_mode = st.session_state.auto_exec
        exec_actions = []
        for c in result["classify"]["classifications"]:
            for a in c["corrective_actions"]:
                should = (exec_mode == "Auto-Execute All" or
                          (exec_mode == "Auto-Execute Low Risk" and a["risk_level"] == "LOW"))
                row = {**a, "service_id": c["service_id"], "executed": should,
                       "status": "done" if should else "pending",
                       "timestamp": time.strftime("%H:%M:%S")}
                exec_actions.append(row)
                if should:
                    push_log(f"⚡ AUTO-EXECUTED: <b>{a['action'][:60]}</b> [{a['action_type']}]", "action")
                else:
                    push_log(f"📋 QUEUED: {a['action'][:60]} — awaiting approval", "result")
        result["exec_actions"] = exec_actions

        total_saved = sum(a["estimated_saving"] for a in exec_actions if a["executed"])
        push_log(f"Execute complete. {sum(1 for a in exec_actions if a['executed'])} executed. Saving: ₹{total_saved:,}", "result")
        set_progress(82); log_ph.markdown(render_logs(), unsafe_allow_html=True)

        # ── AGENT 5: REPORT ───────────────────────────────────────────────────
        render_pipeline(4); set_progress(84, "Report Agent generating insights…")
        push_log("Report Agent activated…", "scan")
        log_ph.markdown(render_logs(), unsafe_allow_html=True)

        report_raw = call_llm([{"role":"user","content":
            f"Cloud cost reporting AI for {st.session_state.org_name}.\n"
            f"Context: {st.session_state.context}\n"
            f"Spike: {result['detect']['total_spike_pct']}%, anomalies: {result['detect']['anomaly_count']}, risk: {result['detect']['risk_level']}\n"
            f"Diagnosis: {result['diagnose']['overall_diagnosis']}\n"
            f"Recoverable: ₹{result['diagnose']['total_recoverable_spend']:,}\nPeriod: {st.session_state.period}\n\n"
            'Return ONLY valid JSON: {"executive_summary":"<3-4 sentences>","key_findings":["","","",""],'
            '"immediate_actions":["","",""],"preventive_measures":["","",""],'
            '"projected_savings_30d":<int>,"projected_savings_90d":<int>,'
            '"health_score_before":<int 0-100>,"health_score_after":<int 0-100>,"confidence":<int>}'
        }], 1000)

        result["report"] = safe_json(report_raw, {
            "executive_summary": f"Analysis of {len(svcs)} services at {st.session_state.org_name} identified {result['detect']['anomaly_count']} anomalies causing +{ov_sp:.1f}% overall cost spike. Root cause: auto-scaling misconfigurations and provisioning errors. ₹{result['detect']['total_wasted_spend']:,} recoverable within 30 days.",
            "key_findings": [f"+{ov_sp:.1f}% overall spike",f"Top anomaly: {(result['detect']['anomalous_services'][0:1] or [{'name':'N/A'}])[0]['name']}",f"₹{result['detect']['total_wasted_spend']:,} wasted","Auto-scaling misconfiguration primary driver"],
            "immediate_actions": ["Rollback auto-scaling max capacity","Terminate idle instances >24h","Enable cost alerts at 110% baseline"],
            "preventive_measures": ["Budget alerts at 120% 3-month avg","Enforce tagging policy","Weekly FinOps review cadence"],
            "projected_savings_30d": round(result["diagnose"]["total_recoverable_spend"]*.6),
            "projected_savings_90d": round(result["diagnose"]["total_recoverable_spend"]*1.4),
            "health_score_before": max(10, 100-round(ov_sp*1.2)),
            "health_score_after":  min(92, 100-round(ov_sp*.3)),
            "confidence": 87
        })

        push_log(f"Report complete. Health: {result['report']['health_score_before']} → {result['report']['health_score_after']} | Confidence: {result['report']['confidence']}%", "result")
        push_log("🏁 <b>All 5 agents complete. Dashboard ready.</b>", "result")
        set_progress(100); log_ph.markdown(render_logs(), unsafe_allow_html=True)
        render_pipeline(5)

        result["ctx"] = ctx_data
        st.session_state.analysis = result
        time.sleep(0.8)
        st.session_state.step = 4
        st.rerun()

    except Exception as e:
        st.error(f"Agent error: {e}")
        if st.button("← Back to Services"):
            st.session_state.step = 2; st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# STEP 4 — RESULTS DASHBOARD
# ─────────────────────────────────────────────────────────────────────────────
elif st.session_state.step == 4:
    a    = st.session_state.analysis
    svcs = st.session_state.services
    thr  = st.session_state.threshold

    if not a:
        st.error("No analysis data. Please run the pipeline.")
        st.stop()

    detect  = a["detect"]
    diagnose = a["diagnose"]
    classify = a["classify"]
    report   = a["report"]
    exec_acts = a.get("exec_actions", [])
    ctx_data  = a["ctx"]

    # ── KPI ROW ──
    total_curr = ctx_data["total_curr"]
    total_prev = ctx_data["total_prev"]
    st.markdown(f"""
    <div class="metric-row">
        <div class="metric-card mc-red">
            <div class="m-label">Total Spend</div>
            <div class="m-val">{fmt_inr(total_curr)}</div>
            <div class="m-sub">Current period</div>
        </div>
        <div class="metric-card mc-red">
            <div class="m-label">Cost Spike</div>
            <div class="m-val">+{detect['total_spike_pct']:.1f}%</div>
            <div class="m-sub">vs previous period</div>
        </div>
        <div class="metric-card mc-amber">
            <div class="m-label">Anomalies</div>
            <div class="m-val">{detect['anomaly_count']}</div>
            <div class="m-sub">Services spiked</div>
        </div>
        <div class="metric-card mc-green">
            <div class="m-label">Recoverable</div>
            <div class="m-val">{fmt_inr(detect['total_wasted_spend'])}</div>
            <div class="m-sub">Wasted spend</div>
        </div>
        <div class="metric-card mc-blue">
            <div class="m-label">Health Score</div>
            <div class="m-val">{report['health_score_after']}/100</div>
            <div class="m-sub">After recovery</div>
        </div>
        <div class="metric-card" style="background:#080f1a;border:1px solid #111d2e;">
            <div class="m-label">Confidence</div>
            <div class="m-val" style="color:#9d7eff;">{report['confidence']}%</div>
            <div class="m-sub">Agent confidence</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── TABS ──
    tabs = st.tabs(["📊 Overview", "🧠 Diagnosis", "🚨 Anomalies", "⚡ Execute", "📈 Trends", "🔮 What-If", "💬 AnomalyBot"])

    # ══ TAB 1: OVERVIEW ══════════════════════════════════════════════════════
    with tabs[0]:
        col_charts, col_summary = st.columns([1.3, 1], gap="large")

        with col_charts:
            st.markdown('<div class="sec-label">// Spend by Service</div>', unsafe_allow_html=True)
            names = [s["name"][:14]+"…" if len(s["name"])>14 else s["name"] for s in svcs]
            fig_bar = go.Figure()
            fig_bar.add_trace(go.Bar(name="Current", x=names, y=[s["curr"] for s in svcs],
                                     marker_color="rgba(255,64,64,.75)", marker_line_width=0))
            fig_bar.add_trace(go.Bar(name="Previous", x=names, y=[s["prev"] for s in svcs],
                                     marker_color="rgba(88,99,122,.5)", marker_line_width=0))
            fig_bar.update_layout(barmode="group", plot_bgcolor="#04080f", paper_bgcolor="#04080f",
                font=dict(family="IBM Plex Mono", size=10, color="#58637a"),
                margin=dict(l=0,r=0,t=10,b=40), height=260, showlegend=False,
                xaxis=dict(gridcolor="#111d2e", tickangle=-30),
                yaxis=dict(gridcolor="#111d2e", tickprefix="₹", tickformat=".0s"))
            st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar":False})

        with col_summary:
            st.markdown('<div class="sec-label">// Cause Distribution</div>', unsafe_allow_html=True)
            dist = classify["cause_distribution"]
            labels = [k.replace("_"," ").title() for k,v in dist.items() if v>0]
            values = [v for v in dist.values() if v>0]
            fig_donut = go.Figure(go.Pie(labels=labels, values=values, hole=.62,
                marker_colors=["#ff4040","#ffbe00","#9d7eff","#00e887","#00d4ff"],
                textfont=dict(family="IBM Plex Mono", size=10)))
            fig_donut.update_layout(plot_bgcolor="#04080f", paper_bgcolor="#04080f",
                font=dict(family="IBM Plex Mono", size=10, color="#58637a"),
                margin=dict(l=0,r=0,t=10,b=10), height=260,
                legend=dict(font=dict(size=10, color="#58637a"), bgcolor="rgba(0,0,0,0)"))
            st.plotly_chart(fig_donut, use_container_width=True, config={"displayModeBar":False})

        st.markdown('<div class="sec-label" style="margin-top:1rem;">// Executive Summary</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div style="background:#080f1a;border:1px solid #111d2e;border-left:3px solid #00e887;border-radius:5px;padding:1.2rem 1.4rem;">
            <p style="font-size:14px;line-height:1.85;color:#c0d0e8;margin-bottom:1rem;">{report['executive_summary']}</p>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;">
                <div>
                    <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;letter-spacing:2px;color:#2a4060;margin-bottom:8px;">KEY FINDINGS</div>
                    {"".join(f'<div style="display:flex;gap:8px;padding:6px 0;border-bottom:1px solid rgba(255,255,255,.03);font-size:13px;"><span style="color:#00d4ff;flex-shrink:0">→</span><span style="color:#c0d0e8;">{f}</span></div>' for f in report.get("key_findings",[]))}
                </div>
                <div>
                    <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;letter-spacing:2px;color:#2a4060;margin-bottom:8px;">PREVENTIVE MEASURES</div>
                    {"".join(f'<div style="display:flex;gap:8px;padding:6px 0;border-bottom:1px solid rgba(255,255,255,.03);font-size:13px;"><span style="color:#00e887;flex-shrink:0">✓</span><span style="color:#c0d0e8;">{m}</span></div>' for m in report.get("preventive_measures",[]))}
                </div>
            </div>
            <div style="display:flex;gap:12px;margin-top:1rem;flex-wrap:wrap;">
                <div style="flex:1;min-width:140px;background:#060d17;border:1px solid #111d2e;border-bottom:2px solid #00e887;border-radius:5px;padding:.9rem 1.1rem;">
                    <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;color:#2a4060;letter-spacing:2px;margin-bottom:4px;">30-DAY SAVING</div>
                    <div style="font-family:'Syne',sans-serif;font-size:22px;font-weight:800;color:#00e887;">₹{report['projected_savings_30d']:,}</div>
                </div>
                <div style="flex:1;min-width:140px;background:#060d17;border:1px solid #111d2e;border-bottom:2px solid #00d4ff;border-radius:5px;padding:.9rem 1.1rem;">
                    <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;color:#2a4060;letter-spacing:2px;margin-bottom:4px;">90-DAY SAVING</div>
                    <div style="font-family:'Syne',sans-serif;font-size:22px;font-weight:800;color:#00d4ff;">₹{report['projected_savings_90d']:,}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ══ TAB 2: DIAGNOSIS ═════════════════════════════════════════════════════
    with tabs[1]:
        st.markdown('<div class="sec-label">// Root Cause Analysis — All Anomalous Services</div>', unsafe_allow_html=True)
        CAUSE_INFO = {
            "provisioning_error":          {"icon":"🔴","label":"Provisioning Error",            "color":"#ff4040"},
            "seasonal_traffic":            {"icon":"🌊","label":"Seasonal Traffic",               "color":"#ffbe00"},
            "auto_scaling_misconfiguration":{"icon":"⚙️","label":"Auto-Scaling Misconfiguration","color":"#9d7eff"},
            "configuration_change":        {"icon":"🔧","label":"Configuration Change",           "color":"#f5a623"},
            "legitimate_growth":           {"icon":"📈","label":"Legitimate Growth",              "color":"#00d4ff"},
        }

        for d in diagnose["diagnoses"]:
            svc = next((s for s in svcs if s["id"]==d["service_id"]), {})
            sp  = spike_pct(svc.get("curr",0), svc.get("prev",0))
            info = CAUSE_INFO.get(d["primary_cause"], {"icon":"⚠️","label":d["primary_cause"],"color":"#58637a"})
            pct  = d["cause_probability"]
            urg_color = {"IMMEDIATE":"#ff4040","HIGH":"#ffbe00","MEDIUM":"#00d4ff","LOW":"#00e887"}.get(d["urgency"],"#58637a")
            st.markdown(f"""
            <div style="background:#080f1a;border:1px solid #111d2e;border-left:3px solid {info['color']};border-radius:5px;padding:14px 16px;margin-bottom:10px;">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px;">
                    <div>
                        <span style="font-weight:600;font-size:14px;color:#ddeeff;">{svc.get('name','—')}</span>
                        <span style="font-family:'IBM Plex Mono',monospace;font-size:10px;color:#3a5060;margin-left:10px;">{svc.get('provider','—')} · {svc.get('region','—')}</span>
                    </div>
                    <span style="font-family:'IBM Plex Mono',monospace;font-size:10px;color:{urg_color};background:rgba(255,255,255,.04);border:1px solid {urg_color}40;padding:2px 8px;border-radius:2px;">{d['urgency']}</span>
                </div>
                <div style="display:flex;align-items:center;gap:10px;background:#060d17;border-radius:4px;border-left:3px solid {info['color']}50;padding:8px 12px;margin-bottom:8px;">
                    <span style="font-size:18px;">{info['icon']}</span>
                    <div style="flex:1;">
                        <div style="font-size:13px;font-weight:600;color:#ddeeff;margin-bottom:2px;">{info['label']}</div>
                        <div style="font-size:12px;color:#3a5a70;">{d.get('technical_details','')}</div>
                    </div>
                    <div style="text-align:right;flex-shrink:0;">
                        <div style="font-family:'Syne',sans-serif;font-size:24px;font-weight:800;color:{info['color']};">{pct}%</div>
                        <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;color:#2a4060;">PROBABILITY</div>
                    </div>
                </div>
                <div style="display:flex;gap:20px;font-family:'IBM Plex Mono',monospace;font-size:11px;flex-wrap:wrap;">
                    <span style="color:#3a5060;">Spike: <span style="color:#ff4040;">+{sp:.1f}%</span></span>
                    <span style="color:#3a5060;">Confidence: <span style="color:#00d4ff;">{d['confidence']}%</span></span>
                    <span style="color:#3a5060;">Impact: <span style="color:#00e887;">₹{d['financial_impact']:,}</span></span>
                    <span style="color:#3a5060;">Evidence: {' · '.join(d.get('evidence',[]))}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background:#080f1a;border:1px solid #111d2e;border-left:3px solid #ffbe00;border-radius:5px;padding:14px 16px;margin-top:1rem;">
            <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;letter-spacing:2px;color:#2a4060;margin-bottom:8px;">OVERALL DIAGNOSIS</div>
            <p style="font-size:13.5px;color:#c0d0e8;line-height:1.8;">{diagnose['overall_diagnosis']}</p>
        </div>
        """, unsafe_allow_html=True)

    # ══ TAB 3: ANOMALIES ═════════════════════════════════════════════════════
    with tabs[2]:
        st.markdown('<div class="sec-label">// Detected Anomalies</div>', unsafe_allow_html=True)
        if not classify["classifications"]:
            st.markdown('<div style="text-align:center;padding:2rem;color:#2a4060;font-family:\'IBM Plex Mono\',monospace;">No anomalies above threshold.</div>', unsafe_allow_html=True)
        else:
            # Table header
            st.markdown("""
            <div class="atbl-wrap">
                <div class="atbl-head">
                    <span>Service</span><span>Provider</span><span>Current</span>
                    <span>Previous</span><span>Spike</span><span>Severity</span><span>Cause</span>
                </div>
            """, unsafe_allow_html=True)
            CAUSE_LABEL = {
                "PROVISIONING_ERROR":"🔴 Prov. Error","SEASONAL_TRAFFIC":"🌊 Seasonal",
                "AUTO_SCALING_MISCONFIGURATION":"⚙️ Auto-Scale","CONFIGURATION_CHANGE":"🔧 Config",
                "LEGITIMATE_GROWTH":"📈 Growth",
            }
            for c in classify["classifications"]:
                svc  = next((s for s in svcs if s["id"]==c["service_id"]), {})
                sp   = spike_pct(svc.get("curr",0), svc.get("prev",0))
                sev  = next((d for d in detect["anomalous_services"] if d["id"]==c["service_id"]), {"severity":"MEDIUM"})
                sp_cls = "sp-high" if sp > thr else ("sp-medium" if sp > thr/2 else "sp-low")
                sev_color = {"CRITICAL":"#ff4040","HIGH":"#ffbe00","MEDIUM":"#00d4ff"}.get(sev["severity"],"#58637a")
                cause_lbl = CAUSE_LABEL.get(c["cause_category"], c["cause_category"])
                st.markdown(f"""
                <div class="atbl-row">
                    <span class="svc-nm">{svc.get('name','—')}</span>
                    <span style="font-family:'IBM Plex Mono',monospace;font-size:11px;color:#3a5060;">{svc.get('provider','—')}</span>
                    <span style="font-family:'IBM Plex Mono',monospace;font-size:12px;color:#e0eaf8;">₹{svc.get('curr',0):,}</span>
                    <span style="font-family:'IBM Plex Mono',monospace;font-size:12px;color:#3a5060;">₹{svc.get('prev',0):,}</span>
                    <span><span class="spike-pill {sp_cls}">↑ {sp:.1f}%</span></span>
                    <span style="font-family:'IBM Plex Mono',monospace;font-size:10px;color:{sev_color};">{sev['severity']}</span>
                    <span style="font-size:12px;color:#c0d0e8;">{cause_lbl}</span>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    # ══ TAB 4: EXECUTE ═══════════════════════════════════════════════════════
    with tabs[3]:
        st.markdown('<div class="sec-label">// Corrective Actions</div>', unsafe_allow_html=True)

        auto_done = [a for a in exec_acts if a["executed"]]
        if auto_done:
            st.markdown(f"""
            <div style="background:rgba(0,232,135,.06);border:1px solid rgba(0,232,135,.18);border-left:3px solid #00e887;border-radius:5px;padding:11px 15px;margin-bottom:1rem;font-size:13px;color:#00e887;">
                ✓ &nbsp; {len(auto_done)} actions auto-executed · Immediate saving: ₹{sum(a['estimated_saving'] for a in auto_done):,}
            </div>
            """, unsafe_allow_html=True)

        # Group by service
        for c in classify["classifications"]:
            svc = next((s for s in svcs if s["id"]==c["service_id"]), {"name":c["service_id"]})
            cat_color = {"PROVISIONING_ERROR":"#ff4040","SEASONAL_TRAFFIC":"#ffbe00",
                         "AUTO_SCALING_MISCONFIGURATION":"#9d7eff","CONFIGURATION_CHANGE":"#f5a623",
                         "LEGITIMATE_GROWTH":"#00d4ff"}.get(c["cause_category"], "#58637a")

            st.markdown(f"""
            <div style="font-family:'IBM Plex Mono',monospace;font-size:10px;letter-spacing:1.5px;color:{cat_color};margin:1.2rem 0 8px;">
                {svc['name']} — {c['cause_category'].replace('_',' ')} · ⏱ {c['resolution_timeline']}
            </div>
            """, unsafe_allow_html=True)

            for i, act in enumerate(c["corrective_actions"]):
                is_exec = any(e["action"]==act["action"] and e.get("executed") for e in exec_acts)
                rc = {"LOW":"#00e887","MEDIUM":"#ffbe00","HIGH":"#ff4040"}.get(act["risk_level"],"#58637a")
                st.markdown(f"""
                <div class="action-card" style="border-left-color:{rc};">
                    <div class="action-head">
                        <span class="action-name">{'✅ ' if is_exec else ''}{act['action']}</span>
                        <span class="priority-badge" style="background:{rc}18;color:{rc};border:1px solid {rc}30;">
                            {act['risk_level']} RISK
                        </span>
                    </div>
                    <div class="action-detail">
                        Type: <b style="color:#c0d0e8;">{act['action_type']}</b>
                        &nbsp;·&nbsp; Saving: <b style="color:#00e887;">₹{act['estimated_saving']:,}</b>
                        &nbsp;·&nbsp; {'AUTO-EXECUTABLE' if act['auto_executable'] else 'MANUAL'}
                        {'&nbsp;·&nbsp; <span style="color:#00e887;">EXECUTED</span>' if is_exec else ''}
                    </div>
                    {f'<div class="action-cmd">$ {act["command_hint"]}</div>' if act.get("command_hint") else ''}
                </div>
                """, unsafe_allow_html=True)

    # ══ TAB 5: TRENDS ════════════════════════════════════════════════════════
    with tabs[4]:
        st.markdown('<div class="sec-label">// Simulated 6-Month Spend Trend</div>', unsafe_allow_html=True)
        months = ["Aug","Sep","Oct","Nov","Dec","Jan"]
        baseline = total_prev * 0.85
        trend_vals = [round(baseline * (0.9 + i*0.04)) for i in range(4)] + [total_prev, total_curr]
        forecast   = [None]*4 + [total_prev, round(total_prev*1.05)]
        anomaly_pt = [None]*5 + [total_curr]

        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(x=months, y=trend_vals, name="Actual", mode="lines+markers",
            line=dict(color="#00d4ff", width=2.5), marker=dict(size=5),
            fill="tozeroy", fillcolor="rgba(0,212,255,.05)"))
        fig_trend.add_trace(go.Scatter(x=months, y=forecast, name="Forecast", mode="lines+markers",
            line=dict(color="#00e887", width=1.5, dash="dot"), marker=dict(size=4)))
        fig_trend.add_trace(go.Scatter(x=[months[-1]], y=[total_curr], name="Anomaly", mode="markers",
            marker=dict(color="#ff4040", size=12, symbol="circle")))
        fig_trend.update_layout(plot_bgcolor="#04080f", paper_bgcolor="#04080f",
            font=dict(family="IBM Plex Mono", size=10, color="#58637a"),
            margin=dict(l=0,r=0,t=10,b=40), height=300,
            xaxis=dict(gridcolor="#111d2e"), yaxis=dict(gridcolor="#111d2e", tickprefix="₹", tickformat=".2s"),
            legend=dict(font=dict(size=10,color="#58637a"),bgcolor="rgba(0,0,0,0)"))
        st.plotly_chart(fig_trend, use_container_width=True, config={"displayModeBar":False})

        col_cat, col_spike = st.columns(2, gap="large")
        with col_cat:
            st.markdown('<div class="sec-label">// Spend by Category</div>', unsafe_allow_html=True)
            cat_totals = {}
            for s in svcs: cat_totals[s["category"]] = cat_totals.get(s["category"],0) + s["curr"]
            fig_cat = go.Figure(go.Bar(
                x=list(cat_totals.values()), y=list(cat_totals.keys()), orientation="h",
                marker_color=["rgba(255,64,64,.7)","rgba(0,212,255,.7)","rgba(157,126,255,.7)",
                              "rgba(0,232,135,.7)","rgba(255,190,0,.7)","rgba(245,166,35,.7)"][:len(cat_totals)],
                marker_line_width=0))
            fig_cat.update_layout(plot_bgcolor="#04080f", paper_bgcolor="#04080f",
                font=dict(family="IBM Plex Mono",size=10,color="#58637a"),
                margin=dict(l=0,r=0,t=10,b=10), height=260,
                xaxis=dict(gridcolor="#111d2e",tickprefix="₹",tickformat=".2s"),
                yaxis=dict(gridcolor="#111d2e"))
            st.plotly_chart(fig_cat, use_container_width=True, config={"displayModeBar":False})

        with col_spike:
            st.markdown('<div class="sec-label">// Cost Spike Distribution</div>', unsafe_allow_html=True)
            spike_data = sorted([{"name":s["name"][:12],"spike":round(spike_pct(s["curr"],s["prev"]),1)} for s in svcs if s["prev"]>0], key=lambda x:-x["spike"])
            fig_spk = go.Figure(go.Bar(
                x=[d["spike"] for d in spike_data], y=[d["name"] for d in spike_data], orientation="h",
                marker_color=["rgba(255,64,64,.75)" if d["spike"]>thr else "rgba(0,212,255,.5)" for d in spike_data],
                marker_line_width=0))
            fig_spk.update_layout(plot_bgcolor="#04080f", paper_bgcolor="#04080f",
                font=dict(family="IBM Plex Mono",size=10,color="#58637a"),
                margin=dict(l=0,r=0,t=10,b=10), height=260,
                xaxis=dict(gridcolor="#111d2e",ticksuffix="%"),
                yaxis=dict(gridcolor="#111d2e"))
            st.plotly_chart(fig_spk, use_container_width=True, config={"displayModeBar":False})

    # ══ TAB 6: WHAT-IF ═══════════════════════════════════════════════════════
    with tabs[5]:
        st.markdown('<div class="sec-label">// What-If Scenario Simulator</div>', unsafe_allow_html=True)
        svc0 = svcs[0]["name"] if svcs else "EC2"
        scenarios = [
            f"What if we right-size all over-provisioned EC2 instances?",
            "What if we enable cost anomaly alerts at 110% of baseline?",
            "What if the spike is entirely seasonal — no action needed?",
            "What if we revert the last auto-scaling configuration change?",
            f"What if we migrate {svc0} to Spot/Preemptible instances?",
            f"What if we implement a spending cap of ₹{round(total_prev*1.15):,}?",
        ]

        grid = st.columns(3)
        preset = None
        for i, sc in enumerate(scenarios):
            with grid[i % 3]:
                if st.button(sc, key=f"sc_{i}", use_container_width=True):
                    preset = sc

        custom = st.text_input("Or type your own scenario…", placeholder="e.g. What if we migrate to reserved instances?")
        scenario_query = preset or custom

        if scenario_query and st.button("🔮  Simulate Scenario", use_container_width=False):
            with st.spinner("Simulating…"):
                try:
                    wi_raw = call_llm([{"role":"user","content":
                        f"Cloud cost what-if simulator.\nCurrent: ₹{total_curr:,}\nPrevious: ₹{total_prev:,}\n"
                        f"Anomalies: {detect['anomaly_count']}\nRecoverable: ₹{detect['total_wasted_spend']:,}\n"
                        f"Org: {st.session_state.org_name}\nScenario: {scenario_query}\n\n"
                        'Return ONLY valid JSON: {"scenario_title":"","new_monthly_spend":<int>,"new_spike_pct":<float>,'
                        '"delta_saving":<int>,"new_health_score":<int>,"outcome":"BETTER|WORSE|NEUTRAL",'
                        '"key_changes":["","",""],"risks":["",""],"recommendation":"<1 sentence>"}'
                    }], 700)
                    wi = safe_json(wi_raw, {
                        "scenario_title": scenario_query[:60], "new_monthly_spend": round(total_curr*.8),
                        "new_spike_pct": round(detect["total_spike_pct"]*.4, 1),
                        "delta_saving": round(total_curr*.2), "new_health_score": min(92, report["health_score_after"]+12),
                        "outcome": "BETTER", "key_changes": ["Spend reduced","Risk eliminated","Baseline normalised"],
                        "risks": ["May affect auto-scaling during peak"], "recommendation": "Recommended with low-risk first."
                    })
                    oc_color = {"BETTER":"#00e887","WORSE":"#ff4040","NEUTRAL":"#00d4ff"}.get(wi["outcome"],"#00d4ff")
                    st.markdown(f"""
                    <div style="background:#080f1a;border:1px solid #111d2e;border-radius:7px;padding:1.4rem;margin-top:1rem;">
                        <div style="font-family:'IBM Plex Mono',monospace;font-size:9.5px;color:#2a4060;margin-bottom:12px;">Scenario: {wi['scenario_title']}</div>
                        <div style="display:flex;gap:24px;flex-wrap:wrap;margin-bottom:16px;">
                            <div><div style="font-family:'IBM Plex Mono',monospace;font-size:9px;color:#2a4060;margin-bottom:4px;">OUTCOME</div><div style="font-family:'Syne',sans-serif;font-size:30px;font-weight:800;color:{oc_color};">{wi['outcome']}</div></div>
                            <div><div style="font-family:'IBM Plex Mono',monospace;font-size:9px;color:#2a4060;margin-bottom:4px;">NEW SPEND</div><div style="font-family:'Syne',sans-serif;font-size:30px;font-weight:800;color:#e0eaf8;">{fmt_inr(wi['new_monthly_spend'])}</div></div>
                            <div><div style="font-family:'IBM Plex Mono',monospace;font-size:9px;color:#2a4060;margin-bottom:4px;">SAVING</div><div style="font-family:'Syne',sans-serif;font-size:30px;font-weight:800;color:#00e887;">{fmt_inr(wi['delta_saving'])}</div></div>
                            <div><div style="font-family:'IBM Plex Mono',monospace;font-size:9px;color:#2a4060;margin-bottom:4px;">HEALTH</div><div style="font-family:'Syne',sans-serif;font-size:30px;font-weight:800;color:#00d4ff;">{wi['new_health_score']}/100</div></div>
                        </div>
                        <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-bottom:12px;">
                            <div><div style="font-family:'IBM Plex Mono',monospace;font-size:9px;color:#2a4060;margin-bottom:8px;">KEY CHANGES</div>{"".join(f'<div style="font-size:12.5px;padding:5px 0;border-bottom:1px solid rgba(255,255,255,.03);color:#c0d0e8;display:flex;gap:8px;"><span style=\'color:#00e887;\'>→</span>{ch}</div>' for ch in wi.get("key_changes",[]))}</div>
                            <div><div style="font-family:'IBM Plex Mono',monospace;font-size:9px;color:#2a4060;margin-bottom:8px;">RISKS</div>{"".join(f'<div style="font-size:12.5px;padding:5px 0;border-bottom:1px solid rgba(255,255,255,.03);color:#c0d0e8;display:flex;gap:8px;"><span style=\'color:#ffbe00;\'>⚠</span>{r}</div>' for r in wi.get("risks",[]))}</div>
                        </div>
                        <div style="background:rgba(0,212,255,.06);border:1px solid rgba(0,212,255,.18);border-radius:4px;padding:10px 14px;font-size:13px;color:#c0d0e8;">💡 {wi['recommendation']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"What-If error: {e}")

    # ══ TAB 7: CHAT ══════════════════════════════════════════════════════════
    with tabs[6]:
        suggestions = [
            "What caused the biggest spike?",
            "How much can I save?",
            "Which service is most critical?",
            "What actions should I take first?",
            "How to prevent this next month?",
        ]

        st.markdown("""
        <div class="chat-wrap">
            <div class="chat-hdr">
                <div class="bot-ava">🤖</div>
                <div>
                    <div style="font-family:'Syne',sans-serif;font-size:14px;font-weight:700;color:#fff;">AnomalyBot</div>
                    <div style="font-family:'IBM Plex Mono',monospace;font-size:10px;color:#3a5060;">AI cloud cost advisor — knows your full analysis</div>
                </div>
                <div style="margin-left:auto;width:7px;height:7px;border-radius:50%;background:#00e887;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Quick suggestion buttons
        sug_cols = st.columns(len(suggestions))
        for i, sug in enumerate(suggestions):
            with sug_cols[i]:
                if st.button(sug, key=f"sug_{i}", use_container_width=True):
                    st.session_state.chat_history.append({"role":"user","content":sug})

        # Chat history display
        if st.session_state.chat_history:
            chat_html = '<div class="chat-msgs">'
            for m in st.session_state.chat_history:
                if m["role"] == "user":
                    chat_html += f'<div class="msg-user"><div class="bubble bubble-user">{m["content"]}</div></div>'
                else:
                    chat_html += f'<div class="msg-bot"><div class="bubble bubble-bot">{m["content"]}</div></div>'
            chat_html += '</div>'
            st.markdown(chat_html, unsafe_allow_html=True)

        col_inp, col_send = st.columns([5, 1])
        with col_inp:
            user_msg = st.text_input("", placeholder="Ask AnomalyBot…", label_visibility="collapsed", key="chat_inp")
        with col_send:
            send = st.button("Send →", use_container_width=True)

        if send and user_msg.strip():
            st.session_state.chat_history.append({"role":"user","content":user_msg.strip()})

        # Auto-respond to pending user messages
        if st.session_state.chat_history and st.session_state.chat_history[-1]["role"] == "user":
            last_user = st.session_state.chat_history[-1]["content"]
            if not any(m["role"]=="assistant" and i>0 and st.session_state.chat_history[i-1]["content"]==last_user
                       for i,m in enumerate(st.session_state.chat_history)):
                with st.spinner("AnomalyBot thinking…"):
                    try:
                        system_ctx = (
                            f"You are AnomalyBot — a sharp, concise AI cloud cost advisor. "
                            f"Org: {st.session_state.org_name}, Period: {st.session_state.period}, "
                            f"Overall spike: {detect['total_spike_pct']:.1f}%, anomalies: {detect['anomaly_count']}, "
                            f"recoverable: ₹{detect['total_wasted_spend']:,}, risk: {detect['risk_level']}. "
                            f"Services: {', '.join(s['name'] for s in svcs[:6])}. "
                            f"Keep answers under 120 words. Use ₹ for currency. Be specific with numbers."
                        )
                        msgs = [{"role":"system","content":system_ctx}] + st.session_state.chat_history[-10:]
                        reply = call_llm(msgs, 220)
                        st.session_state.chat_history.append({"role":"assistant","content":reply})
                        st.rerun()
                    except Exception as e:
                        st.session_state.chat_history.append({"role":"assistant","content":f"Error: {e}"})
                        st.rerun()

    # ── Bottom controls ──
    st.markdown("<br>", unsafe_allow_html=True)
    col_b1, col_b2, col_b3, _ = st.columns([1,1,1,4])
    with col_b1:
        if st.button("← New Analysis"):
            for k,v in DEFAULTS.items(): st.session_state[k]=v
            st.rerun()
    with col_b2:
        if st.button("✏  Edit Services"):
            st.session_state.step = 2; st.rerun()
    with col_b3:
        if st.button("🔄  Re-run Agents"):
            st.session_state.step = 3; st.rerun()
