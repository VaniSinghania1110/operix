"""
SpendGuard — Cloud Spend Anomaly Detection & Response Agent
Economic Times GenAI Hackathon — Streamlit Version

Run:   streamlit run spendguard_streamlit.py
Need:  pip install streamlit groq python-dotenv plotly pandas

.env:
    GROQ_API_KEY=gsk_...
"""

import streamlit as st
from groq import Groq
import json, time, os, random, html as _html
from dotenv import load_dotenv
import plotly.graph_objects as go
import pandas as pd

def esc(t):
    """HTML-escape any dynamic/LLM text before embedding in HTML strings."""
    return _html.escape(str(t) if t is not None else "")

load_dotenv()

# ── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SpendGuard — Cloud Spend Anomaly Agent",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CONSTANTS ─────────────────────────────────────────────────────────────────
PROVIDERS  = ["AWS", "Azure", "GCP", "Oracle Cloud", "IBM Cloud"]
CATEGORIES = ["Compute", "Storage", "Database", "Networking", "Analytics", "ML/AI", "CDN", "Security", "Other"]
REGIONS    = ["us-east-1", "us-west-2", "eu-west-1", "ap-south-1", "ap-southeast-1", "me-south-1", "sa-east-1"]

SAMPLE_SERVICES = [
    {"ID":"SVC-001","Service Name":"EC2 Web Cluster","Provider":"AWS","Category":"Compute","Current Cost (₹)":420000,"Previous Cost (₹)":280000,"Instances":48,"Region":"us-east-1","Notes":"Auto-scaling enabled"},
    {"ID":"SVC-002","Service Name":"RDS Aurora","Provider":"AWS","Category":"Database","Current Cost (₹)":185000,"Previous Cost (₹)":180000,"Instances":3,"Region":"us-east-1","Notes":""},
    {"ID":"SVC-003","Service Name":"S3 Data Lake","Provider":"AWS","Category":"Storage","Current Cost (₹)":68000,"Previous Cost (₹)":62000,"Instances":0,"Region":"ap-south-1","Notes":""},
    {"ID":"SVC-004","Service Name":"Azure Kubernetes","Provider":"Azure","Category":"Compute","Current Cost (₹)":310000,"Previous Cost (₹)":210000,"Instances":32,"Region":"eu-west-1","Notes":"New node pools added"},
    {"ID":"SVC-005","Service Name":"GCP BigQuery","Provider":"GCP","Category":"Analytics","Current Cost (₹)":95000,"Previous Cost (₹)":88000,"Instances":0,"Region":"us-east-1","Notes":""},
    {"ID":"SVC-006","Service Name":"CloudFront CDN","Provider":"AWS","Category":"CDN","Current Cost (₹)":42000,"Previous Cost (₹)":38000,"Instances":0,"Region":"us-east-1","Notes":""},
    {"ID":"SVC-007","Service Name":"Lambda Functions","Provider":"AWS","Category":"Compute","Current Cost (₹)":28000,"Previous Cost (₹)":29000,"Instances":0,"Region":"ap-south-1","Notes":""},
    {"ID":"SVC-008","Service Name":"Azure AI Services","Provider":"Azure","Category":"ML/AI","Current Cost (₹)":156000,"Previous Cost (₹)":90000,"Instances":8,"Region":"eu-west-1","Notes":"New model deployments"},
    {"ID":"SVC-009","Service Name":"GCP GKE Cluster","Provider":"GCP","Category":"Compute","Current Cost (₹)":88000,"Previous Cost (₹)":85000,"Instances":12,"Region":"ap-southeast-1","Notes":""},
    {"ID":"SVC-010","Service Name":"AWS Redshift","Provider":"AWS","Category":"Database","Current Cost (₹)":125000,"Previous Cost (₹)":72000,"Instances":4,"Region":"us-east-1","Notes":"DC2 to RA3 migration test"},
]

# ── SESSION STATE ─────────────────────────────────────────────────────────────
_DEFAULTS = {
    "page": "step1",
    "org_name": "",
    "threshold": 20,
    "period": "Month-over-Month",
    "auto_exec": "recommend",
    "ctx_info": "",
    "services_df": None,
    "analysis": None,
    "chat_history": [],
    "executed_actions": set(),
    "whatif_scenario": "",
}
for k, v in _DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

if st.session_state.services_df is None:
    st.session_state.services_df = pd.DataFrame(columns=[
        "ID", "Service Name", "Provider", "Category",
        "Current Cost (₹)", "Previous Cost (₹)", "Instances", "Region", "Notes"
    ])

# ── GROQ CLIENT ───────────────────────────────────────────────────────────────
@st.cache_resource
def get_client():
    key = os.getenv("GROQ_API_KEY")
    if not key:
        st.error("GROQ_API_KEY not found in environment / .env file.")
        st.stop()
    return Groq(api_key=key)

def call_llm(messages, max_tokens=1600):
    client = get_client()
    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        max_tokens=int(max_tokens),
        temperature=0.3,
    )
    return resp.choices[0].message.content.strip()

def safe_json(text, fallback):
    try:
        clean = text.replace("```json", "").replace("```", "").strip()
        return json.loads(clean)
    except Exception:
        return fallback

def fmt_inr(n):
    n = int(n)
    if n >= 10_000_000: return f"₹{n/10_000_000:.1f}Cr"
    if n >= 100_000:    return f"₹{n/100_000:.1f}L"
    if n >= 1_000:      return f"₹{n/1_000:.0f}K"
    return f"₹{n}"

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Base dark theme ── */
[data-testid="stAppViewContainer"]   { background-color: #04080f; }
[data-testid="stHeader"]             { background-color: #04080f; border-bottom: 1px solid #111d2e; }
[data-testid="stSidebar"]            { display: none; }
[data-testid="collapsedControl"]     { display: none; }
.block-container { padding-top: 1.2rem; padding-bottom: 2rem; max-width: 1180px; }
#MainMenu, footer, header { visibility: hidden; }

/* ── Typography ── */
body, p, div, span, label { color: #e0eaf8 !important; }
h1,h2,h3 { color: #e0eaf8 !important; }

/* ── Text & Number inputs ── */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
textarea {
    background: #0d1624 !important;
    border: 1px solid #1e3050 !important;
    border-radius: 4px !important;
    color: #e0eaf8 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 13px !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stNumberInput"] input:focus {
    border-color: #00d4ff !important;
    box-shadow: 0 0 0 2px rgba(0,212,255,.08) !important;
}

/* ── Selectbox — target every layer Streamlit renders ── */
[data-testid="stSelectbox"] > div,
[data-testid="stSelectbox"] > div > div,
[data-testid="stSelectbox"] [data-baseweb="select"],
[data-testid="stSelectbox"] [data-baseweb="select"] > div,
[data-testid="stSelectbox"] [data-baseweb="select"] > div > div {
    background-color: #0d1624 !important;
    border-color: #1e3050 !important;
    color: #e0eaf8 !important;
}
[data-testid="stSelectbox"] [data-baseweb="select"] > div:first-child {
    border: 1px solid #1e3050 !important;
    border-radius: 4px !important;
    background-color: #0d1624 !important;
}
/* Value text inside selectbox */
[data-testid="stSelectbox"] [data-baseweb="select"] span,
[data-testid="stSelectbox"] [data-baseweb="select"] input,
[data-testid="stSelectbox"] [class*="valueContainer"] * {
    background-color: transparent !important;
    color: #e0eaf8 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 13px !important;
}
/* Dropdown arrow */
[data-testid="stSelectbox"] svg { fill: #58637a !important; }

/* ── Dropdown portal menu (renders outside stSelectbox wrapper) ── */
[data-baseweb="popover"],
[data-baseweb="popover"] > div,
[data-baseweb="menu"],
ul[data-baseweb="menu"] {
    background-color: #0d1624 !important;
    border: 1px solid #1e3050 !important;
    border-radius: 4px !important;
}
[data-baseweb="menu"] li,
[data-baseweb="option"],
[role="option"] {
    background-color: #0d1624 !important;
    color: #e0eaf8 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 13px !important;
}
[data-baseweb="menu"] li:hover,
[data-baseweb="option"]:hover,
[role="option"]:hover {
    background-color: #162540 !important;
    color: #00d4ff !important;
}
[aria-selected="true"][role="option"] {
    background-color: rgba(0,212,255,.1) !important;
    color: #00d4ff !important;
}

/* ── Number input +/- buttons ── */
[data-testid="stNumberInput"] button {
    background: #0d1624 !important;
    border: 1px solid #1e3050 !important;
    color: #58637a !important;
    border-radius: 4px !important;
}
[data-testid="stNumberInput"] button:hover {
    color: #00d4ff !important;
    border-color: #00d4ff !important;
}

/* ── DataEditor ── */
[data-testid="stDataEditor"] {
    background: #080f1a !important;
    border: 1px solid #111d2e !important;
    border-radius: 6px !important;
}

/* ── All generic st.buttons ── */
[data-testid="stButton"] > button {
    background: transparent !important;
    border: 1px solid #1e3050 !important;
    color: #58637a !important;
    border-radius: 4px !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 12px !important;
    transition: all .2s !important;
}
[data-testid="stButton"] > button:hover {
    border-color: #00d4ff !important;
    color: #00d4ff !important;
    background: rgba(0,212,255,.05) !important;
}
/* Primary cyan button */
.primary-btn [data-testid="stButton"] > button {
    background: #00d4ff !important;
    color: #04080f !important;
    border: none !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    padding: 0.55rem 1.4rem !important;
}
.primary-btn [data-testid="stButton"] > button:hover {
    background: #00bbee !important;
    color: #04080f !important;
}
/* Launch red button */
.launch-btn [data-testid="stButton"] > button {
    background: linear-gradient(135deg,#ff4040,#c00) !important;
    color: #fff !important;
    border: none !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    box-shadow: 0 0 24px rgba(255,64,64,.25) !important;
}

/* ── Metrics ── */
[data-testid="metric-container"] {
    background: #080f1a !important;
    border: 1px solid #111d2e !important;
    border-radius: 6px !important;
    padding: 14px !important;
}
[data-testid="metric-container"] label {
    color: #58637a !important;
    font-size: 10px !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase;
}
[data-testid="stMetricValue"] { color: #e0eaf8 !important; font-weight: 900 !important; }
[data-testid="stMetricDelta"] { display: none; }

/* ── Progress bar ── */
[data-testid="stProgressBar"] > div { background: #111d2e; }
[data-testid="stProgressBar"] > div > div { background: linear-gradient(90deg,#00d4ff,#00e887); }

/* ── Chat ── */
[data-testid="stChatMessageContent"] { background: #0d1624 !important; border: 1px solid #1e3050 !important; }
[data-testid="stChatInput"] textarea { background: #0d1624 !important; border: 1px solid #1e3050 !important; color: #e0eaf8 !important; }

/* ── Tab bar ── */
[data-testid="stTabs"] [role="tablist"] { border-bottom: 1px solid #111d2e; background: transparent; }
[data-testid="stTabs"] button[role="tab"] {
    background: transparent !important;
    color: #58637a !important;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    letter-spacing: 1px;
    border-bottom: 2px solid transparent !important;
    padding: 10px 16px;
}
[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
    color: #00d4ff !important;
    border-bottom: 2px solid #00d4ff !important;
}

/* ── Spinner ── */
[data-testid="stSpinner"] { color: #00d4ff !important; }

/* ── Alerts / info boxes ── */
[data-testid="stAlert"] { background: #080f1a !important; border-radius: 6px !important; }

/* ── Widget labels ── */
[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] label {
    color: #58637a !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 12px !important;
}
</style>
""", unsafe_allow_html=True)


# ── SHARED WIDGETS ────────────────────────────────────────────────────────────
def render_header():
    st.markdown("""
    <div style="display:flex;align-items:center;justify-content:space-between;
                padding:12px 0 20px;border-bottom:1px solid #111d2e;margin-bottom:20px">
        <div style="display:flex;align-items:center;gap:12px">
            <div style="width:38px;height:38px;background:#ff4040;
                        clip-path:polygon(50% 0%,100% 25%,100% 75%,50% 100%,0% 75%,0% 25%);
                        display:flex;align-items:center;justify-content:center;
                        font-size:16px;color:#04080f;font-weight:900">S</div>
            <div style="font-size:26px;font-weight:900;letter-spacing:-1px;color:#e0eaf8">
                Spend<span style="color:#ff4040">Guard</span>
            </div>
        </div>
        <div style="font-family:monospace;font-size:10px;letter-spacing:2px;color:#ff4040;
                    border:1px solid rgba(255,64,64,.3);padding:4px 12px;border-radius:2px;
                    display:flex;align-items:center;gap:6px">
            <span style="width:5px;height:5px;background:#ff4040;border-radius:50%;
                          display:inline-block;animation:none"></span>
            5-AGENT AI ACTIVE
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_wizard(active: int):
    steps = [("01","Configuration"), ("02","Services"), ("03","Launch")]
    cols = st.columns([1, 0.25, 1, 0.25, 1])
    for i, (num, label) in enumerate(steps):
        if i < active:
            dot_style = "background:rgba(0,232,135,.1);border:1.5px solid #00e887;color:#00e887"
            lbl_color, sym = "#00e887", "✓"
        elif i == active:
            dot_style = "background:rgba(0,212,255,.12);border:1.5px solid #00d4ff;color:#00d4ff"
            lbl_color, sym = "#00d4ff", num
        else:
            dot_style = "background:#080f1a;border:1.5px solid #111d2e;color:#3a4260"
            lbl_color, sym = "#3a4260", num
        with cols[i * 2]:
            st.markdown(f"""
            <div style="text-align:center">
                <div style="width:40px;height:40px;border-radius:50%;{dot_style};
                            display:flex;align-items:center;justify-content:center;
                            font-family:monospace;font-size:13px;margin:0 auto">{sym}</div>
                <div style="font-family:monospace;font-size:9px;letter-spacing:1.5px;
                            text-transform:uppercase;color:{lbl_color};margin-top:6px">{label}</div>
            </div>""", unsafe_allow_html=True)
        if i < 2:
            lc = "rgba(0,232,135,.3)" if i < active else "#111d2e"
            with cols[i * 2 + 1]:
                st.markdown(f'<div style="height:1px;background:{lc};margin-top:20px"></div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)


def card_open(accent="#00d4ff"):
    st.markdown(f"""
    <div style="background:#080f1a;border:1px solid #111d2e;border-radius:8px;
                padding:20px 24px;margin-bottom:16px;position:relative;overflow:hidden">
        <div style="position:absolute;top:0;left:0;right:0;height:2px;
                    background:linear-gradient(90deg,transparent,{accent},transparent)"></div>
    """, unsafe_allow_html=True)

def card_close():
    st.markdown("</div>", unsafe_allow_html=True)

def section_label(text):
    st.markdown(f"""
    <div style="font-family:monospace;font-size:9px;letter-spacing:2px;text-transform:uppercase;
                color:#3a4260;margin-bottom:12px;display:flex;align-items:center;gap:8px">
        {text}
        <div style="flex:1;height:1px;background:#111d2e"></div>
    </div>""", unsafe_allow_html=True)

# ── PAGE: STEP 1 ──────────────────────────────────────────────────────────────
def show_step1():
    render_header()
    st.markdown("""
    <div style="padding:32px 0 24px">
        <div style="font-family:monospace;font-size:11px;letter-spacing:3px;color:#ff4040;
                    text-transform:uppercase;margin-bottom:12px;opacity:.8">
            Track 3 — Cost Intelligence &amp; Autonomous Action</div>
        <div style="font-size:clamp(36px,5vw,64px);font-weight:900;line-height:.95;
                    letter-spacing:-1px;color:#e0eaf8;margin-bottom:16px">
            DETECT. DIAGNOSE.<br><span style="color:#00d4ff">NEUTRALISE.</span></div>
        <div style="font-size:15px;color:#58637a;max-width:600px;line-height:1.8;font-weight:300">
            Agentic AI that catches cloud spend anomalies in real time — diagnoses whether the spike
            is a provisioning error, seasonal traffic, or misconfigured auto-scaling — then executes
            the right corrective action autonomously.</div>
    </div>""", unsafe_allow_html=True)

    render_wizard(0)
    card_open()
    st.markdown('<div style="font-family:monospace;font-size:10px;letter-spacing:2px;text-transform:uppercase;color:#58637a;margin-bottom:16px">⚙ AGENT CONFIGURATION</div>', unsafe_allow_html=True)

    org = st.text_input("Organisation / Project", value=st.session_state.org_name,
                        placeholder="e.g. Acme Engineering, ET Cloud Infra…")

    c1, c2, c3 = st.columns(3)
    with c1:
        threshold = st.number_input("Alert Threshold (%)", min_value=5, max_value=200,
                                    value=st.session_state.threshold)
    with c2:
        period_opts = ["Month-over-Month","Week-over-Week","Day-over-Day","Quarter-over-Quarter"]
        period = st.selectbox("Time Period", period_opts,
                              index=period_opts.index(st.session_state.period))
    with c3:
        ae_labels = ["Recommend Only","Auto-Execute Low Risk","Auto-Execute All"]
        ae_keys   = ["recommend","low","all"]
        ae_sel    = st.selectbox("Auto-Execute Actions", ae_labels,
                                 index=ae_keys.index(st.session_state.auto_exec))
        auto_exec = ae_keys[ae_labels.index(ae_sel)]

    ctx_info = st.text_input("Additional Context (optional)", value=st.session_state.ctx_info,
                              placeholder="e.g. Q4 product launch expected, migrating to new region…")
    card_close()

    _, _, right = st.columns([3, 1, 1])
    with right:
        st.markdown('<div class="primary-btn">', unsafe_allow_html=True)
        if st.button("Next: Add Cloud Services →", use_container_width=True, key="go_step2"):
            if not org.strip():
                st.error("Please enter an organisation name.")
            else:
                st.session_state.org_name   = org.strip()
                st.session_state.threshold  = threshold
                st.session_state.period     = period
                st.session_state.auto_exec  = auto_exec
                st.session_state.ctx_info   = ctx_info
                if len(st.session_state.services_df) == 0:
                    st.session_state.services_df = pd.DataFrame([{
                        "ID":"SVC-001","Service Name":"","Provider":"AWS",
                        "Category":"Compute","Current Cost (₹)":0,"Previous Cost (₹)":0,
                        "Instances":0,"Region":"us-east-1","Notes":""
                    }])
                st.session_state.page = "step2"
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ── PAGE: STEP 2 ──────────────────────────────────────────────────────────────
def show_step2():
    render_header()
    render_wizard(1)
    card_open()
    st.markdown('<div style="font-family:monospace;font-size:10px;letter-spacing:2px;text-transform:uppercase;color:#58637a;margin-bottom:10px">☁ CLOUD SERVICE SPEND DATA</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="background:rgba(0,212,255,.08);border:1px solid rgba(0,212,255,.2);border-left:3px solid #00d4ff;border-radius:4px;padding:10px 14px;font-size:13px;margin-bottom:14px;color:#e0eaf8">Enter current and previous period costs for each cloud service. The agent will detect anomalies automatically based on your <strong>{st.session_state.threshold}%</strong> threshold.</div>', unsafe_allow_html=True)

    edited_df = st.data_editor(
        st.session_state.services_df,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "ID":                 st.column_config.TextColumn("ID", width=90),
            "Service Name":       st.column_config.TextColumn("Service Name", width=160),
            "Provider":           st.column_config.SelectboxColumn("Provider", options=PROVIDERS, width=110),
            "Category":           st.column_config.SelectboxColumn("Category", options=CATEGORIES, width=120),
            "Current Cost (₹)":   st.column_config.NumberColumn("Current Cost (₹)", min_value=0, format="₹%d", width=140),
            "Previous Cost (₹)":  st.column_config.NumberColumn("Previous Cost (₹)", min_value=0, format="₹%d", width=140),
            "Instances":          st.column_config.NumberColumn("Instances", min_value=0, width=90),
            "Region":             st.column_config.SelectboxColumn("Region", options=REGIONS, width=130),
            "Notes":              st.column_config.TextColumn("Notes", width=180),
        },
        key="svc_editor",
    )
    st.session_state.services_df = edited_df
    card_close()

    c1, c2 = st.columns([1, 4])
    with c1:
        if st.button("⚡ Load Sample Dataset"):
            st.session_state.services_df = pd.DataFrame(SAMPLE_SERVICES)
            st.rerun()

    # Live anomaly preview
    vdf = edited_df[edited_df["Service Name"].astype(str).str.strip() != ""].copy()
    if len(vdf) > 0 and vdf["Previous Cost (₹)"].sum() > 0:
        vdf["spike_pct"] = (vdf["Current Cost (₹)"] - vdf["Previous Cost (₹)"]) / vdf["Previous Cost (₹)"].replace(0, float("nan")) * 100
        anom = vdf[vdf["spike_pct"] > st.session_state.threshold]
        if len(anom) > 0:
            tc = vdf["Current Cost (₹)"].sum(); tp = vdf["Previous Cost (₹)"].sum()
            overall = (tc - tp) / tp * 100 if tp else 0
            spike_color = "#ff4040" if overall > st.session_state.threshold else "#ffbe00"
            st.markdown(f"""
            <div style="background:#080f1a;border:1px solid #111d2e;border-radius:6px;
                        padding:16px;margin:12px 0;position:relative;overflow:hidden">
                <div style="position:absolute;top:0;left:0;right:0;height:2px;background:#ff4040"></div>
                <div style="font-family:monospace;font-size:9px;letter-spacing:2px;color:#ff4040;
                            text-transform:uppercase;margin-bottom:12px">🚨 LIVE ANOMALY PREVIEW</div>
                <div style="display:flex;gap:28px;flex-wrap:wrap">
                    <div><div style="font-family:monospace;font-size:9px;color:#58637a;letter-spacing:2px;margin-bottom:4px">ANOMALIES</div>
                         <div style="font-size:28px;font-weight:900;color:#ff4040">{len(anom)}</div></div>
                    <div style="width:1px;background:#111d2e"></div>
                    <div><div style="font-family:monospace;font-size:9px;color:#58637a;letter-spacing:2px;margin-bottom:4px">OVERALL SPIKE</div>
                         <div style="font-size:28px;font-weight:900;color:{spike_color}">+{overall:.1f}%</div></div>
                    <div style="width:1px;background:#111d2e"></div>
                    <div><div style="font-family:monospace;font-size:9px;color:#58637a;letter-spacing:2px;margin-bottom:4px">TOTAL SPEND</div>
                         <div style="font-size:28px;font-weight:900;color:#e0eaf8">₹{tc:,.0f}</div></div>
                </div>
            </div>""", unsafe_allow_html=True)

    col_back, _, col_launch = st.columns([1, 3, 1])
    with col_back:
        if st.button("← Back"):
            st.session_state.page = "step1"; st.rerun()
    with col_launch:
        st.markdown('<div class="launch-btn">', unsafe_allow_html=True)
        if st.button("⚡ Launch 5-Agent Pipeline →", use_container_width=True, key="launch"):
            valid = st.session_state.services_df[
                st.session_state.services_df["Service Name"].astype(str).str.strip() != ""
            ]
            if len(valid) == 0:
                st.error("Please add at least one service.")
            else:
                st.session_state.services_df = valid.reset_index(drop=True)
                st.session_state.page = "running"; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ── PAGE: RUNNING ─────────────────────────────────────────────────────────────
def show_running():
    render_header()
    st.markdown("""
    <div style="padding:28px 0 16px;text-align:center">
        <div style="font-family:monospace;font-size:10px;letter-spacing:3px;color:#00d4ff;
                    text-transform:uppercase;margin-bottom:10px">5-Agent Pipeline Executing</div>
        <div style="font-size:36px;font-weight:900;color:#e0eaf8;margin-bottom:8px">
            Analysing Cloud Spend…</div>
        <div style="font-size:14px;color:#58637a">
            Detect → Diagnose → Classify → Execute → Report</div>
    </div>""", unsafe_allow_html=True)

    pipe_ph   = st.empty()
    prog_bar  = st.progress(0)
    prog_text = st.empty()
    st.markdown('<div style="font-family:monospace;font-size:9px;letter-spacing:2px;color:#3a4260;text-transform:uppercase;margin:12px 0 4px">Agent Reasoning Log</div>', unsafe_allow_html=True)
    log_ph = st.empty()

    logs = []
    PIPE_STEPS = [("🔍","DETECT","Scans for anomalies"), ("🧠","DIAGNOSE","Root cause AI"),
                  ("🏷","CLASSIFY","Labels cause type"), ("⚡","EXECUTE","Runs corrective actions"),
                  ("📋","REPORT","Generates insights")]

    def upd_pipe(active):
        html = '<div style="display:flex;align-items:center;padding:14px 0;flex-wrap:wrap">'
        for i, (icon, label, sub) in enumerate(PIPE_STEPS):
            if i < active:
                ds = "background:rgba(0,232,135,.1);border:1.5px solid #00e887;color:#00e887"; sym="✓"; lc="#00e887"
            elif i == active:
                ds = "background:rgba(0,212,255,.12);border:1.5px solid #00d4ff;color:#00d4ff"; sym=icon; lc="#00d4ff"
            else:
                ds = "background:#080f1a;border:1.5px solid #111d2e;color:#3a4260"; sym=icon; lc="#3a4260"
            html += f'<div style="flex:1;min-width:70px;text-align:center"><div style="width:40px;height:40px;border-radius:50%;{ds};display:flex;align-items:center;justify-content:center;font-size:15px;margin:0 auto">{sym}</div><div style="font-family:monospace;font-size:8px;letter-spacing:1.5px;text-transform:uppercase;color:{lc};margin-top:6px">{label}<br><span style="font-size:7px;opacity:.6">{sub}</span></div></div>'
            if i < 4:
                lc2 = "rgba(0,232,135,.3)" if i < active else ("rgba(0,212,255,.4)" if i==active else "#111d2e")
                html += f'<div style="flex:.4;height:1px;background:{lc2};margin-bottom:14px"></div>'
        html += "</div>"
        pipe_ph.markdown(html, unsafe_allow_html=True)

    TAG_STYLE = {
        "scan":     ("rgba(0,212,255,.12)","#00d4ff"),
        "diagnose": ("rgba(255,190,0,.1)","#ffbe00"),
        "classify": ("rgba(245,166,35,.1)","#f5a623"),
        "action":   ("rgba(255,64,64,.1)","#ff4040"),
        "result":   ("rgba(0,232,135,.1)","#00e887"),
        "think":    ("rgba(157,126,255,.1)","#9d7eff"),
    }

    def push_log(msg, kind="scan"):
        ts = time.strftime("%H:%M:%S")
        bg, col = TAG_STYLE.get(kind, ("rgba(88,99,122,.1)","#58637a"))
        logs.append(f'<div style="padding:3px 0;border-bottom:1px solid rgba(255,255,255,.025);display:flex;gap:8px;font-family:monospace;font-size:11.5px"><span style="color:#3a4260;font-size:10px;flex-shrink:0">{ts}</span><span style="font-size:9px;padding:1px 5px;border-radius:2px;background:{bg};color:{col};flex-shrink:0">[{kind.upper()}]</span><span style="color:#58637a;flex:1">{msg}</span></div>')
        inner = "".join(logs[-22:])
        log_ph.markdown(f'<div style="background:#04080f;border:1px solid #111d2e;border-radius:6px;padding:12px;max-height:280px;overflow-y:auto">{inner}</div>', unsafe_allow_html=True)

    def set_prog(pct):
        prog_bar.progress(pct / 100)
        prog_text.markdown(f'<div style="font-family:monospace;font-size:10px;color:#00d4ff;text-align:right">{pct}%</div>', unsafe_allow_html=True)

    # ── Build context ─────────────────────────────────────────────────────────
    df         = st.session_state.services_df
    total_curr = int(df["Current Cost (₹)"].sum())
    total_prev = int(df["Previous Cost (₹)"].sum())
    overall_sp = ((total_curr - total_prev) / total_prev * 100) if total_prev else 0

    ctx = {
        "org": st.session_state.org_name, "period": st.session_state.period,
        "threshold": st.session_state.threshold, "autoExec": st.session_state.auto_exec,
        "context": st.session_state.ctx_info,
        "totalCurr": total_curr, "totalPrev": total_prev,
        "services": [
            {"id": r["ID"], "name": r["Service Name"], "provider": r["Provider"],
             "category": r["Category"], "currCost": int(r["Current Cost (₹)"]),
             "prevCost": int(r["Previous Cost (₹)"]),
             "spike": f"{(r['Current Cost (₹)']-r['Previous Cost (₹)'])/r['Previous Cost (₹)']*100:.1f}%" if r["Previous Cost (₹)"] > 0 else "N/A",
             "instances": int(r["Instances"]), "region": r["Region"], "notes": r["Notes"]}
            for _, r in df.iterrows()
        ],
    }
    result = {}

    try:
        # ── AGENT 1: DETECT ───────────────────────────────────────────────────
        upd_pipe(0); set_prog(5)
        push_log(f"Scan Agent activated — scanning {len(ctx['services'])} cloud services…", "scan")
        push_log(f"Total spend: ₹{total_curr:,} vs ₹{total_prev:,} previous", "scan")
        push_log(f"Overall spend change: +{overall_sp:.1f}% {st.session_state.period} | Threshold: {st.session_state.threshold}%", "scan")

        anomalies = [s for s in ctx["services"] if s["prevCost"] > 0 and (s["currCost"]-s["prevCost"])/s["prevCost"]*100 > st.session_state.threshold]
        push_log(f"Anomaly detection: {len(anomalies)} services exceed threshold", "result")
        for s in anomalies:
            sp = (s["currCost"]-s["prevCost"])/s["prevCost"]*100
            push_log(f"⚠ {s['name']} ({s['provider']}) spiked +{sp:.0f}% | ₹{s['prevCost']:,} → ₹{s['currCost']:,}", "scan")

        detect_raw = call_llm([{"role":"user","content":
            f"You are a cloud cost anomaly detection AI. Analyse this data and return ONLY valid JSON:\n{json.dumps(ctx)}\n\nReturn:\n"
            '{"total_spike_pct":<float>,"anomaly_count":<int>,"anomalous_services":[{"id":"","name":"","spike_pct":<float>,"severity":"CRITICAL|HIGH|MEDIUM","wasted_spend":<int>,"likely_cause_hint":"provisioning_error|seasonal_traffic|auto_scaling|normal_growth|configuration_change"}],"normal_services":[{"id":"","name":""}],"total_wasted_spend":<int>,"risk_level":"CRITICAL|HIGH|MEDIUM|LOW"}'
        }], 800)

        result["detect"] = safe_json(detect_raw, {
            "total_spike_pct": round(overall_sp, 1),
            "anomaly_count": len(anomalies),
            "anomalous_services": [{"id":s["id"],"name":s["name"],
                "spike_pct": round((s["currCost"]-s["prevCost"])/s["prevCost"]*100, 1),
                "severity": "CRITICAL" if (s["currCost"]-s["prevCost"])/s["prevCost"]*100 > 60 else "HIGH",
                "wasted_spend": round((s["currCost"]-s["prevCost"])*0.7),
                "likely_cause_hint": "auto_scaling"} for s in anomalies],
            "normal_services": [{"id":s["id"],"name":s["name"]} for s in ctx["services"] if s not in anomalies],
            "total_wasted_spend": round((total_curr-total_prev)*0.65),
            "risk_level": "CRITICAL" if overall_sp > 40 else "HIGH" if overall_sp > 20 else "MEDIUM",
        })
        push_log(f"Detect Agent complete. Risk: {result['detect']['risk_level']}. Wasted: ₹{result['detect']['total_wasted_spend']:,}", "result")
        set_prog(20); time.sleep(0.3)

        # ── AGENT 2: DIAGNOSE ─────────────────────────────────────────────────
        upd_pipe(1); set_prog(22)
        push_log("Diagnose Agent activated — running root cause analysis…", "diagnose")
        push_log(f"Analysing {len(result['detect']['anomalous_services'])} anomalous services…", "think")

        diag_raw = call_llm([{"role":"user","content":
            f"You are a cloud cost root cause analysis AI.\nOrg: {st.session_state.org_name}\nContext: {st.session_state.ctx_info}\n"
            f"Anomalies:\n{json.dumps(result['detect']['anomalous_services'])}\nFull data:\n{json.dumps(ctx['services'])}\n\n"
            "For each anomalous service diagnose root cause. Return ONLY valid JSON:\n"
            '{"diagnoses":[{"service_id":"","service_name":"","primary_cause":"provisioning_error|seasonal_traffic|auto_scaling_misconfiguration|legitimate_growth|configuration_change","cause_probability":<int 0-100>,"secondary_cause":"","confidence":<int>,"evidence":["",""],"financial_impact":<int>,"urgency":"IMMEDIATE|HIGH|MEDIUM|LOW","technical_details":"<2 sentences>"}],"overall_diagnosis":"<3 sentences>","total_recoverable_spend":<int>}'
        }], 1200)

        CAUSE_LIST = ["provisioning_error","seasonal_traffic","auto_scaling_misconfiguration","configuration_change","legitimate_growth"]
        result["diagnose"] = safe_json(diag_raw, {
            "diagnoses": [{"service_id":s["id"],"service_name":s["name"],
                "primary_cause": CAUSE_LIST[i % len(CAUSE_LIST)],
                "cause_probability": 65 + (i*7) % 25, "secondary_cause":"legitimate_growth",
                "confidence": 72, "evidence":["Spike correlates with deployment","Instance count increased"],
                "financial_impact": s["wasted_spend"],
                "urgency": "IMMEDIATE" if s["severity"]=="CRITICAL" else "HIGH",
                "technical_details": f"Resource allocation exceeded baseline by {s['spike_pct']}%. Pattern suggests {CAUSE_LIST[i % len(CAUSE_LIST)].replace('_',' ')}."}
                for i, s in enumerate(result["detect"]["anomalous_services"])],
            "overall_diagnosis": f"Analysis of {len(ctx['services'])} services identified {result['detect']['anomaly_count']} anomalies with mixed root causes.",
            "total_recoverable_spend": result["detect"]["total_wasted_spend"],
        })
        for d in result["diagnose"]["diagnoses"]:
            push_log(f"{d['service_name']}: {d['primary_cause'].replace('_',' ')} ({d['cause_probability']}%) | ₹{d['financial_impact']:,}", "diagnose")
        push_log(f"Diagnose Agent complete. Recoverable: ₹{result['diagnose']['total_recoverable_spend']:,}", "result")
        set_prog(42); time.sleep(0.3)

        # ── AGENT 3: CLASSIFY ─────────────────────────────────────────────────
        upd_pipe(2); set_prog(44)
        push_log("Classify Agent activated — labelling causes and corrective categories…", "classify")

        cls_raw = call_llm([{"role":"user","content":
            f"You are a cloud cost classification AI.\nDiagnoses:\n{json.dumps(result['diagnose']['diagnoses'])}\nAuto-execute: {st.session_state.auto_exec}\n\n"
            "Classify and recommend actions. Return ONLY valid JSON:\n"
            '{"classifications":[{"service_id":"","cause_category":"PROVISIONING_ERROR|SEASONAL_TRAFFIC|AUTO_SCALING_MISCONFIGURATION|LEGITIMATE_GROWTH|CONFIGURATION_CHANGE","category_label":"","corrective_actions":[{"action":"","action_type":"TERMINATE|RESIZE|RECONFIGURE|ALERT|MONITOR|SCALE_DOWN|ROLLBACK","risk_level":"LOW|MEDIUM|HIGH","auto_executable":<bool>,"estimated_saving":<int>,"priority":1,"command_hint":""}],"resolution_timeline":""}],"cause_distribution":{"provisioning_error":<int>,"seasonal_traffic":<int>,"auto_scaling_misconfiguration":<int>,"legitimate_growth":<int>,"other":<int>}}'
        }], 1200)

        CAT_MAP = {"provisioning_error":"PROVISIONING_ERROR","seasonal_traffic":"SEASONAL_TRAFFIC",
                   "auto_scaling_misconfiguration":"AUTO_SCALING_MISCONFIGURATION",
                   "configuration_change":"CONFIGURATION_CHANGE","legitimate_growth":"LEGITIMATE_GROWTH"}
        result["classify"] = safe_json(cls_raw, {
            "classifications": [{"service_id":d["service_id"],
                "cause_category": CAT_MAP.get(d["primary_cause"],"PROVISIONING_ERROR"),
                "category_label": CAT_MAP.get(d["primary_cause"],"PROVISIONING_ERROR").replace("_"," "),
                "corrective_actions":[
                    {"action":"Scale down over-provisioned instances to baseline","action_type":"SCALE_DOWN","risk_level":"LOW","auto_executable":True,"estimated_saving":round(d["financial_impact"]*0.6),"priority":1,"command_hint":"aws ec2 modify-instance-attribute --instance-type t3.large"},
                    {"action":"Set cost alert at 110% of baseline spend","action_type":"ALERT","risk_level":"LOW","auto_executable":True,"estimated_saving":0,"priority":2,"command_hint":"aws budgets create-budget --budget ..."},
                    {"action":"Review auto-scaling policies and set max capacity limit","action_type":"RECONFIGURE","risk_level":"MEDIUM","auto_executable":False,"estimated_saving":round(d["financial_impact"]*0.3),"priority":3,"command_hint":"aws autoscaling update-auto-scaling-group --max-size 20"},
                ],"resolution_timeline":"Immediate — 4 hours"}
                for d in result["diagnose"]["diagnoses"]],
            "cause_distribution":{"provisioning_error":1,"seasonal_traffic":1,"auto_scaling_misconfiguration":2,"legitimate_growth":1,"other":0},
        })
        for c in result["classify"]["classifications"]:
            na = sum(1 for a in c["corrective_actions"] if a["auto_executable"])
            push_log(f"{c['cause_category'].replace('_',' ')} — {len(c['corrective_actions'])} actions ({na} auto-executable)", "classify")
        set_prog(62); time.sleep(0.3)

        # ── AGENT 4: EXECUTE ──────────────────────────────────────────────────
        upd_pipe(3); set_prog(64)
        push_log("Execute Agent activated — running approved corrective actions…", "action")

        exec_actions = []
        for c in result["classify"]["classifications"]:
            for a in c["corrective_actions"]:
                should = st.session_state.auto_exec == "all" or (st.session_state.auto_exec == "low" and a["risk_level"] == "LOW")
                exec_actions.append({**a, "service_id":c["service_id"], "executed":should,
                                     "status":"done" if should else "pending",
                                     "timestamp":time.strftime("%H:%M:%S")})
                if should:
                    push_log(f"⚡ AUTO-EXECUTED: {a['action'][:60]} [{a['action_type']}]", "action")
                    st.session_state.executed_actions.add(a["action"])
                else:
                    push_log(f"📋 QUEUED: {a['action'][:60]} — awaiting approval", "result")

        result["execute"] = exec_actions
        executed_cnt = sum(1 for e in exec_actions if e["executed"])
        total_rec = sum(e["estimated_saving"] for e in exec_actions if e["executed"])
        push_log(f"Execute Agent complete. {executed_cnt} actions executed. Saving: ₹{total_rec:,}", "result")
        set_prog(82); time.sleep(0.3)

        # ── AGENT 5: REPORT ───────────────────────────────────────────────────
        upd_pipe(4); set_prog(84)
        push_log("Report Agent activated — generating final analysis and recommendations…", "scan")

        rep_raw = call_llm([{"role":"user","content":
            f"You are a cloud cost reporting AI for {st.session_state.org_name}.\nContext: {st.session_state.ctx_info}\n"
            f"Detect: total_spike={result['detect']['total_spike_pct']}%, anomalies={result['detect']['anomaly_count']}, risk={result['detect']['risk_level']}\n"
            f"Diagnosis: {result['diagnose']['overall_diagnosis']}\nRecoverable: ₹{result['diagnose']['total_recoverable_spend']}\nPeriod: {st.session_state.period}\n\n"
            "Generate executive summary. Return ONLY valid JSON:\n"
            '{"executive_summary":"<3-4 sentences with specific numbers>","key_findings":["","","",""],"immediate_actions":["","",""],"preventive_measures":["","",""],"projected_savings_30d":<int>,"projected_savings_90d":<int>,"health_score_before":<int 0-100>,"health_score_after":<int 0-100>,"confidence":<int>}'
        }], 900)

        anom_svcs = result["detect"]["anomalous_services"]
        result["report"] = safe_json(rep_raw, {
            "executive_summary": f"Analysis of {len(ctx['services'])} cloud services at {st.session_state.org_name} identified {result['detect']['anomaly_count']} spend anomalies contributing to a {overall_sp:.1f}% overall cost spike {st.session_state.period}. Root cause analysis attributes the spike to auto-scaling misconfigurations and provisioning errors. Corrective actions can recover ₹{result['diagnose']['total_recoverable_spend']:,} within 30 days.",
            "key_findings": [f"Overall spend spiked +{overall_sp:.1f}% vs previous period",
                             f"Top anomaly: {anom_svcs[0]['name'] if anom_svcs else 'N/A'} at +{anom_svcs[0]['spike_pct'] if anom_svcs else 0}%",
                             f"₹{result['detect']['total_wasted_spend']:,} identified as recoverable wasted spend",
                             f"Auto-scaling misconfiguration is primary driver across {max(1,result['detect']['anomaly_count']//2)} services"],
            "immediate_actions": ["Rollback auto-scaling max capacity to previous limits","Terminate untagged idle instances >24 hours","Enable cost anomaly detection alerts at 110% baseline"],
            "preventive_measures": ["Implement budget alerts on all services at 120% of 3-month average","Enforce tagging policy — no instance launch without cost-centre tag","Weekly FinOps review with auto-generated spend diff reports"],
            "projected_savings_30d": round(result["diagnose"]["total_recoverable_spend"] * 0.6),
            "projected_savings_90d": round(result["diagnose"]["total_recoverable_spend"] * 1.4),
            "health_score_before": max(10, 100 - round(overall_sp * 1.2)),
            "health_score_after":  min(92, 100 - round(overall_sp * 0.3)),
            "confidence": 87,
        })
        push_log(f"Report Agent complete. Health: {result['report']['health_score_before']} → {result['report']['health_score_after']} | Confidence: {result['report']['confidence']}%", "result")
        push_log("🏁 All 5 agents complete. Dashboard ready.", "result")
        set_prog(100); upd_pipe(5)

        result["ctx"] = ctx
        st.session_state.analysis = result
        time.sleep(0.8)
        st.session_state.page = "results"; st.rerun()

    except Exception as e:
        st.error(f"Agent error: {e}\n\nCheck your GROQ_API_KEY and try again.")
        if st.button("← Back to Services"):
            st.session_state.page = "step2"; st.rerun()

# ── PAGE: RESULTS ─────────────────────────────────────────────────────────────
def show_results():
    render_header()
    a = st.session_state.analysis
    df = st.session_state.services_df

    if not a:
        st.error("No analysis found. Please run the agent pipeline first.")
        if st.button("← Start Over"): st.session_state.page = "step1"; st.rerun()
        return

    c1, c2, c3, _ = st.columns([1, 1, 1, 4])
    with c1:
        if st.button("← New Analysis"):
            for k in list(st.session_state.keys()): del st.session_state[k]
            st.rerun()
    with c2:
        if st.button("✏ Edit Services"): st.session_state.page = "step2"; st.rerun()
    with c3:
        if st.button("🔄 Re-run Agents"): st.session_state.page = "running"; st.rerun()

    tabs = st.tabs(["📊 Overview","🧠 Diagnosis","🚨 Anomalies","⚡ Execute","📈 Trends","🔮 What-If","💬 AnomalyBot"])
    with tabs[0]: tab_overview(a, df)
    with tabs[1]: tab_diagnosis(a, df)
    with tabs[2]: tab_anomalies(a, df)
    with tabs[3]: tab_actions(a, df)
    with tabs[4]: tab_trends(a, df)
    with tabs[5]: tab_whatif(a)
    with tabs[6]: tab_chat(a, df)

# ── TAB: OVERVIEW ─────────────────────────────────────────────────────────────
def tab_overview(a, df):
    r = a["report"]; d = a["detect"]
    tc = a["ctx"]["totalCurr"]; tp = a["ctx"]["totalPrev"]

    c1,c2,c3,c4,c5,c6 = st.columns(6)
    for col, lbl, val, hlp in [
        (c1,"TOTAL SPEND",fmt_inr(tc),"Current period"),
        (c2,"COST SPIKE",f"+{d['total_spike_pct']:.1f}%","vs previous"),
        (c3,"ANOMALIES",str(d["anomaly_count"]),"Services spiked"),
        (c4,"RECOVERABLE",fmt_inr(d["total_wasted_spend"]),"Wasted spend"),
        (c5,"HEALTH SCORE",f"{r['health_score_after']}/100","After recovery"),
        (c6,"CONFIDENCE",f"{r['confidence']}%","Agent confidence"),
    ]:
        with col: st.metric(label=lbl, value=val, help=hlp)

    st.markdown("<br>", unsafe_allow_html=True)

    col_l, col_r = st.columns(2)
    with col_l:
        names = [s[:12]+"…" if len(s)>12 else s for s in df["Service Name"]]
        fig = go.Figure()
        fig.add_trace(go.Bar(name="Current", x=names, y=df["Current Cost (₹)"], marker_color="rgba(255,64,64,.7)", marker_cornerradius=3))
        fig.add_trace(go.Bar(name="Previous", x=names, y=df["Previous Cost (₹)"], marker_color="rgba(88,99,122,.5)", marker_cornerradius=3))
        _chart_style(fig, "Spend by Service (Current vs Previous)", barmode="group", ytickprefix="₹")
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        dist = a["classify"]["cause_distribution"]
        labels = [k.replace("_"," ").title() for k,v in dist.items() if v>0]
        vals   = [v for v in dist.values() if v>0]
        fig2 = go.Figure(go.Pie(labels=labels, values=vals, hole=.62,
                                 marker_colors=["#ff4040","#ffbe00","#9d7eff","#00e887","#00d4ff"][:len(labels)],
                                 textfont=dict(color="#58637a",size=10)))
        _chart_style(fig2, "Anomaly Cause Distribution")
        st.plotly_chart(fig2, use_container_width=True)

    # Executive summary
    r = a["report"]
    findings_html = "".join(f'<div style="display:flex;gap:8px;padding:7px 0;border-bottom:1px solid rgba(255,255,255,.04);font-size:13px;color:#e0eaf8"><span style="color:#00d4ff">→</span><span>{esc(f)}</span></div>' for f in r.get("key_findings",[]))
    measures_html = "".join(f'<div style="display:flex;gap:8px;padding:7px 0;border-bottom:1px solid rgba(255,255,255,.04);font-size:13px;color:#e0eaf8"><span style="color:#00e887">✓</span><span>{esc(m)}</span></div>' for m in r.get("preventive_measures",[]))
    st.markdown(f"""
    <div style="background:#080f1a;border:1px solid #111d2e;border-left:3px solid #00e887;
                border-radius:6px;padding:20px 24px">
        <div style="font-family:monospace;font-size:9px;letter-spacing:2px;text-transform:uppercase;
                    color:#58637a;margin-bottom:14px">✦ EXECUTIVE SUMMARY</div>
        <p style="font-size:14px;line-height:1.8;color:#e0eaf8;margin-bottom:16px">{esc(r['executive_summary'])}</p>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:24px">
            <div><div style="font-family:monospace;font-size:9px;letter-spacing:2px;color:#58637a;margin-bottom:10px">KEY FINDINGS</div>{findings_html}</div>
            <div><div style="font-family:monospace;font-size:9px;letter-spacing:2px;color:#58637a;margin-bottom:10px">PREVENTIVE MEASURES</div>{measures_html}</div>
        </div>
        <div style="display:flex;gap:16px;margin-top:16px">
            <div style="flex:1;background:#04080f;border:1px solid #111d2e;border-bottom:2px solid #00e887;border-radius:6px;padding:14px">
                <div style="font-family:monospace;font-size:9px;color:#58637a;letter-spacing:2px">30-DAY SAVING</div>
                <div style="font-size:22px;font-weight:900;color:#00e887">₹{r['projected_savings_30d']:,}</div>
            </div>
            <div style="flex:1;background:#04080f;border:1px solid #111d2e;border-bottom:2px solid #00d4ff;border-radius:6px;padding:14px">
                <div style="font-family:monospace;font-size:9px;color:#58637a;letter-spacing:2px">90-DAY SAVING</div>
                <div style="font-size:22px;font-weight:900;color:#00d4ff">₹{r['projected_savings_90d']:,}</div>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

# ── TAB: DIAGNOSIS ────────────────────────────────────────────────────────────
def tab_diagnosis(a, df):
    diagnoses = a["diagnose"]["diagnoses"]
    CAUSES = {
        "provisioning_error":            ("🔴","Provisioning Error","#ff4040"),
        "seasonal_traffic":              ("🌊","Seasonal Traffic","#ffbe00"),
        "auto_scaling_misconfiguration": ("⚙️","Auto-Scaling Misconfiguration","#9d7eff"),
        "configuration_change":          ("🔧","Configuration Change","#f5a623"),
        "legitimate_growth":             ("📈","Legitimate Growth","#00d4ff"),
    }
    if not diagnoses: st.info("No diagnoses available."); return

    section_label("ROOT CAUSE ANALYSIS — TOP ANOMALY")
    top = diagnoses[0]
    causes3 = [
        ("provisioning_error",            top["cause_probability"] if top.get("primary_cause")=="provisioning_error" else round(top["cause_probability"]*0.3)),
        ("seasonal_traffic",              top["cause_probability"] if top.get("primary_cause")=="seasonal_traffic" else round(top["cause_probability"]*0.25)),
        ("auto_scaling_misconfiguration", top["cause_probability"] if top.get("primary_cause")=="auto_scaling_misconfiguration" else round(top["cause_probability"]*0.35)),
    ]
    cols = st.columns(3)
    for i, (key, prob) in enumerate(causes3):
        icon, label, color = CAUSES.get(key, ("⚠️", key, "#58637a"))
        is_winner  = top.get("primary_cause") == key
        border     = "3px solid #ff4040" if is_winner else "1px solid #111d2e"
        bg         = "rgba(255,64,64,.05)" if is_winner else "#080f1a"
        pc         = "#ff4040" if is_winner else "#00d4ff"
        name_color = "#ff4040" if is_winner else "#e0eaf8"
        # Build optional PRIMARY badge as a separate variable — avoids dict-in-fstring ambiguity
        primary_badge = (
            "<div style=\"position:absolute;top:8px;right:8px;font-family:monospace;"
            "font-size:9px;color:#ff4040;background:rgba(255,64,64,.1);"
            "padding:2px 7px;border-radius:2px\">PRIMARY</div>"
        ) if is_winner else ""
        safe_label = esc(label)
        safe_icon  = esc(icon)
        with cols[i]:
            html_card = (
                f'<div style="background:{bg};border:{border};border-radius:6px;' +
                f'padding:16px;text-align:center;position:relative;margin-bottom:8px">' +
                primary_badge +
                f'<div style="font-size:26px;margin-bottom:8px">{safe_icon}</div>' +
                f'<div style="font-weight:700;font-size:13px;color:{name_color};margin-bottom:4px">{safe_label}</div>' +
                f'<div style="font-size:32px;font-weight:900;color:{pc};margin-bottom:4px">{prob}%</div>' +
                '<div style="font-size:11px;color:#58637a;margin-bottom:10px">Probability</div>' +
                '<div style="height:4px;background:#111d2e;border-radius:2px;overflow:hidden">' +
                f'<div style="width:{prob}%;height:100%;background:{pc};border-radius:2px"></div>' +
                '</div></div>'
            )
            st.markdown(html_card, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if top.get("technical_details"):
        evidence_html = "".join(f'<div style="display:flex;gap:8px;padding:6px 0;font-size:13px;border-bottom:1px solid rgba(255,255,255,.03);color:#e0eaf8"><span style="color:#ffbe00">▸</span><span>{esc(e)}</span></div>' for e in top.get("evidence",[]))
        st.markdown(f"""
        <div style="background:#080f1a;border:1px solid #111d2e;border-radius:6px;padding:20px;margin-bottom:16px">
            <div style="font-family:monospace;font-size:9px;letter-spacing:2px;color:#58637a;margin-bottom:12px">⚡ DETAILED DIAGNOSIS</div>
            <p style="font-size:14px;line-height:1.8;color:#e0eaf8;margin-bottom:14px">{esc(top.get('technical_details',''))}</p>
            <div style="font-family:monospace;font-size:9px;letter-spacing:2px;color:#58637a;margin-bottom:8px">EVIDENCE</div>
            {evidence_html}
        </div>""", unsafe_allow_html=True)

    section_label("ALL SERVICE DIAGNOSIS")
    rows = []
    for d in diagnoses:
        svc = df[df["ID"] == d["service_id"]]
        if len(svc) == 0: continue
        row = svc.iloc[0]
        sp = f"+{(row['Current Cost (₹)']-row['Previous Cost (₹)'])/row['Previous Cost (₹)']*100:.1f}%" if row["Previous Cost (₹)"] > 0 else "N/A"
        icon, label, _ = CAUSES.get(d["primary_cause"], ("⚠️",d.get("primary_cause",""),"#58637a"))
        rows.append({"Service":d["service_name"],"Spike":sp,"Primary Cause":f"{icon} {label}",
                     "Confidence":f"{d['confidence']}%","Urgency":d["urgency"],
                     "Impact (₹)":f"₹{d['financial_impact']:,}"})
    if rows: st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

# ── TAB: ANOMALIES ────────────────────────────────────────────────────────────
def tab_anomalies(a, df):
    CAUSES = {
        "PROVISIONING_ERROR":            ("🔴","Provisioning Error","critical","#ff4040"),
        "SEASONAL_TRAFFIC":              ("🌊","Seasonal Traffic","high","#ffbe00"),
        "AUTO_SCALING_MISCONFIGURATION": ("⚙️","Auto-Scaling Misconfiguration","high","#ffbe00"),
        "CONFIGURATION_CHANGE":          ("🔧","Configuration Change","medium","#00d4ff"),
        "LEGITIMATE_GROWTH":             ("📈","Legitimate Growth","medium","#00d4ff"),
    }
    classifications = a["classify"]["classifications"]
    if not classifications: st.info("No anomalies detected above threshold."); return

    cols = st.columns(2)
    for i, c in enumerate(classifications):
        svc_df = df[df["ID"] == c["service_id"]]
        if len(svc_df) == 0: continue
        svc  = svc_df.iloc[0]
        diag = next((d for d in a["diagnose"]["diagnoses"] if d["service_id"]==c["service_id"]), {})
        sp   = f"+{(svc['Current Cost (₹)']-svc['Previous Cost (₹)'])/svc['Previous Cost (₹)']*100:.1f}%" if svc["Previous Cost (₹)"] > 0 else "N/A"
        icon, label, _, bc = CAUSES.get(c["cause_category"], ("⚠️",c.get("category_label","Unknown"),"medium","#111d2e"))

        acts_html = ""
        for act in c["corrective_actions"]:
            is_exec = act["action"] in st.session_state.executed_actions
            bg  = "rgba(0,232,135,.08)" if is_exec else "rgba(255,64,64,.08)"
            bdr = "rgba(0,232,135,.3)"  if is_exec else "rgba(255,64,64,.2)"
            badge = "DONE" if is_exec else ("AUTO" if act["auto_executable"] else "MANUAL")
            bb   = "rgba(0,232,135,.1)" if is_exec else ("rgba(255,64,64,.15)" if act["auto_executable"] else "rgba(255,190,0,.1)")
            bc2  = "#00e887" if is_exec else ("#ff4040" if act["auto_executable"] else "#ffbe00")
            aico = "✅" if is_exec else ("⚡" if act["auto_executable"] else "📋")
            acts_html += f'<div style="background:{bg};border:1px solid {bdr};border-radius:4px;padding:8px 12px;margin-bottom:6px;display:flex;align-items:center;gap:8px;font-size:12px;color:#e0eaf8"><span>{aico}</span><span style="flex:1">{act["action"]}</span><span style="font-size:9px;padding:2px 7px;border-radius:2px;background:{bb};color:{bc2}">{badge}</span></div>'

        with cols[i % 2]:
            st.markdown(f"""
            <div style="background:#080f1a;border:1px solid #111d2e;border-top:3px solid {bc};
                        border-radius:6px;padding:16px;margin-bottom:12px">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:10px">
                    <div>
                        <div style="font-size:15px;font-weight:700;color:#e0eaf8">{svc['Service Name']}</div>
                        <div style="font-family:monospace;font-size:10px;color:#58637a;margin-top:2px">{svc['Provider']} · {svc['Category']} · {svc['Region']}</div>
                    </div>
                    <div style="text-align:right">
                        <div style="font-size:26px;font-weight:900;color:#ff4040">{sp}</div>
                        <div style="font-family:monospace;font-size:9px;color:#58637a">spike</div>
                    </div>
                </div>
                <div style="background:#0d1624;border-radius:4px;border-left:3px solid rgba(255,64,64,.5);
                            padding:8px 12px;margin-bottom:10px;display:flex;gap:8px;align-items:center">
                    <span style="font-size:16px">{icon}</span>
                    <div style="flex:1"><strong style="color:#e0eaf8">{esc(label)}</strong><br>
                    <span style="font-size:12px;color:#e0eaf8">{esc(diag.get('technical_details',''))}</span></div>
                    <span style="font-family:monospace;font-size:10px;color:#58637a">{diag.get('confidence',0)}%</span>
                </div>
                <div style="display:flex;justify-content:space-between;font-family:monospace;font-size:11px;color:#58637a;margin-bottom:10px">
                    <span>Current: ₹{svc['Current Cost (₹)']:,}</span>
                    <span>Previous: ₹{svc['Previous Cost (₹)']:,}</span>
                    <span style="color:#00e887">Save: ₹{diag.get('financial_impact',0):,}</span>
                </div>
                {acts_html}
                <div style="font-family:monospace;font-size:10px;color:#58637a;margin-top:8px">⏱ {c.get('resolution_timeline','N/A')}</div>
            </div>""", unsafe_allow_html=True)

            for ai, act in enumerate(c["corrective_actions"]):
                if act["action"] not in st.session_state.executed_actions:
                    if st.button(f"⚡ Execute action {ai+1}", key=f"anom_exec_{i}_{ai}", use_container_width=True):
                        st.session_state.executed_actions.add(act["action"]); st.rerun()

# ── TAB: ACTIONS ──────────────────────────────────────────────────────────────
def tab_actions(a, df):
    exec_list = a.get("execute", [])
    done = [e for e in exec_list if e["executed"]]
    also_done = [e for e in exec_list if not e["executed"] and e["action"] in st.session_state.executed_actions]
    all_done = done + also_done

    items_html = "".join(f'<div style="display:flex;gap:10px;align-items:flex-start;padding:10px 0;border-bottom:1px solid rgba(255,255,255,.03)"><div style="width:8px;height:8px;border-radius:50%;background:#00e887;flex-shrink:0;margin-top:4px"></div><div style="flex:1"><div style="font-size:13px;color:#e0eaf8;font-weight:500">{e["action"]}</div><div style="font-family:monospace;font-size:11px;color:#58637a">{e.get("command_hint","Auto-executed")}</div></div><div style="font-family:monospace;font-size:10px;color:#3a4260">{e.get("timestamp","")}</div></div>' for e in all_done)
    empty_html = '<div style="color:#3a4260;font-family:monospace;font-size:11px;text-align:center;padding:16px">No actions executed yet</div>'
    st.markdown(f"""
    <div style="background:#0d1624;border:1px solid #111d2e;border-radius:6px;padding:16px;margin-bottom:16px">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px">
            <div style="font-family:monospace;font-size:9px;letter-spacing:2px;color:#58637a">EXECUTION LOG</div>
            <div style="font-family:monospace;font-size:10px;color:#58637a">{len(all_done)} action(s)</div>
        </div>
        {items_html if all_done else empty_html}
    </div>""", unsafe_allow_html=True)

    section_label("ALL RECOMMENDED ACTIONS")
    all_acts = []
    for c in a["classify"]["classifications"]:
        svc = df[df["ID"]==c["service_id"]]
        svc_name = svc.iloc[0]["Service Name"] if len(svc) > 0 else c["service_id"]
        for act in c["corrective_actions"]:
            all_acts.append({**act, "service_name": svc_name})
    all_acts.sort(key=lambda x: x.get("priority", 99))

    for i, act in enumerate(all_acts):
        rc = {"LOW":"#00e887","MEDIUM":"#ffbe00","HIGH":"#ff4040"}.get(act["risk_level"],"#58637a")
        is_done = act["action"] in st.session_state.executed_actions
        col_m, col_b = st.columns([5,1])
        with col_m:
            cmd_html = f'<div style="font-family:monospace;font-size:11px;color:#3a4260;margin-top:4px;word-break:break-all">$ {act["command_hint"]}</div>' if act.get("command_hint") else ""
            st.markdown(f"""
            <div style="background:#0d1624;border:1px solid #111d2e;border-radius:6px;padding:14px 16px;
                        margin-bottom:8px;display:flex;gap:12px;align-items:flex-start">
                <div style="width:28px;height:28px;border-radius:6px;background:rgba(255,255,255,.03);
                            border:1px solid #111d2e;display:flex;align-items:center;justify-content:center;
                            font-family:monospace;font-size:12px;color:#00d4ff;flex-shrink:0">{i+1}</div>
                <div style="flex:1">
                    <div style="font-size:13.5px;font-weight:500;color:#e0eaf8;margin-bottom:4px">{act['action']}</div>
                    <div style="font-family:monospace;font-size:11px;color:#58637a">{act['service_name']} · {act['action_type']} · ₹{act['estimated_saving']:,} saving</div>
                    {cmd_html}
                </div>
                <span style="font-family:monospace;font-size:9px;color:{rc};padding:2px 8px;
                             border-radius:2px;border:1px solid {rc}40;flex-shrink:0">{act['risk_level']} RISK</span>
            </div>""", unsafe_allow_html=True)
        with col_b:
            if is_done:
                st.markdown('<div style="padding:10px 0;text-align:center"><span style="color:#00e887;font-size:14px">✅ Done</span></div>', unsafe_allow_html=True)
            else:
                if st.button("⚡ Execute", key=f"act_list_{i}", use_container_width=True):
                    st.session_state.executed_actions.add(act["action"]); st.rerun()

# ── TAB: TRENDS ───────────────────────────────────────────────────────────────
def tab_trends(a, df):
    tc = a["ctx"]["totalCurr"]; tp = a["ctx"]["totalPrev"]
    baseline = tp * 0.85
    months = ["Aug","Sep","Oct","Nov","Dec","Jan"]
    random.seed(42)
    trend    = [round(baseline*(0.9+i*0.04+random.random()*0.04)) for i in range(4)] + [tp, tc]
    forecast = [None]*4 + [tp, round(tp*1.05)]
    anom_pts = [None]*5 + [tc]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=months, y=trend, name="Actual", line=dict(color="#00d4ff",width=2), fill="tozeroy", fillcolor="rgba(0,212,255,.06)", mode="lines+markers", marker=dict(color="#00d4ff",size=5)))
    fig.add_trace(go.Scatter(x=months, y=forecast, name="Forecast", line=dict(color="#00e887",width=2,dash="dash"), mode="lines+markers", marker=dict(color="#00e887",size=5)))
    fig.add_trace(go.Scatter(x=months, y=anom_pts, name="Anomaly", mode="markers", marker=dict(color="#ff4040",size=12)))
    _chart_style(fig, "Simulated 6-Month Spend Trend", ytickprefix="₹")
    st.plotly_chart(fig, use_container_width=True)

    col_l, col_r = st.columns(2)
    with col_l:
        cats = {}
        for _, row in df.iterrows():
            cats[row["Category"]] = cats.get(row["Category"],0) + row["Current Cost (₹)"]
        COLS = ["rgba(255,64,64,.7)","rgba(0,212,255,.7)","rgba(157,126,255,.7)","rgba(0,232,135,.7)","rgba(255,190,0,.7)","rgba(245,166,35,.7)"]
        fig3 = go.Figure(go.Barpolar(r=list(cats.values()), theta=list(cats.keys()),
                                      marker_color=COLS[:len(cats)], marker_line_color="#04080f", marker_line_width=1))
        fig3.update_layout(title="Spend by Category",
                           polar=dict(bgcolor="#04080f", radialaxis=dict(showticklabels=False,gridcolor="#111d2e"),
                                      angularaxis=dict(color="#58637a")),
                           paper_bgcolor="#080f1a", font=dict(color="#58637a",size=10),
                           title_font=dict(color="#58637a",size=10),
                           margin=dict(l=10,r=10,t=40,b=10))
        st.plotly_chart(fig3, use_container_width=True)

    with col_r:
        spikes = sorted(
            [(row["Service Name"][:12]+"…" if len(row["Service Name"])>12 else row["Service Name"],
              round((row["Current Cost (₹)"]-row["Previous Cost (₹)"])/row["Previous Cost (₹)"]*100,1))
             for _, row in df.iterrows() if row["Previous Cost (₹)"] > 0],
            key=lambda x: x[1], reverse=True
        )
        fig4 = go.Figure(go.Bar(
            x=[s[1] for s in spikes], y=[s[0] for s in spikes], orientation="h",
            marker_color=["rgba(255,64,64,.7)" if s[1]>st.session_state.threshold else "rgba(0,212,255,.5)" for s in spikes],
            marker_cornerradius=3
        ))
        _chart_style(fig4, "Cost Spike Distribution", xtickprefix="", xtick_suffix="%")
        st.plotly_chart(fig4, use_container_width=True)

# ── TAB: WHAT-IF ──────────────────────────────────────────────────────────────
def tab_whatif(a):
    st.markdown('<div style="font-family:monospace;font-size:10px;letter-spacing:2px;color:#3a4260;margin-bottom:16px">SIMULATE A SCENARIO — THE AGENT WILL PREDICT THE NEW SPEND OUTCOME</div>', unsafe_allow_html=True)

    svc0 = st.session_state.services_df.iloc[0]["Service Name"] if len(st.session_state.services_df) > 0 else "EC2 cluster"
    scenarios = [
        ("💡","What if we right-size all over-provisioned EC2 instances?"),
        ("🔔","What if we enable cost anomaly alerts at 110% of baseline?"),
        ("🌊","What if the spike is entirely seasonal — no action needed?"),
        ("⚙️","What if we revert the last auto-scaling configuration change?"),
        ("🔄",f"What if we migrate {svc0} to Spot/Preemptible instances?"),
        ("📉",f"What if we implement a spending cap of ₹{round(a['ctx']['totalPrev']*1.15):,}?"),
    ]
    c1, c2 = st.columns(2)
    for i, (icon, text) in enumerate(scenarios):
        with (c1 if i%2==0 else c2):
            if st.button(f"{icon} {text}", key=f"wi_sc_{i}", use_container_width=True):
                st.session_state.whatif_scenario = text; st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    scenario = st.text_input("Or type your own scenario…",
                              value=st.session_state.whatif_scenario,
                              placeholder="e.g. What if we migrate EC2 to Spot instances?")
    if st.button("🔮 Simulate", key="simulate_btn"):
        if not scenario.strip():
            st.warning("Please enter a scenario.")
        else:
            with st.spinner("Simulating scenario…"):
                try:
                    resp = call_llm([{"role":"user","content":
                        f"You are a cloud cost what-if simulator.\nCurrent: ₹{a['ctx']['totalCurr']:,}\nPrevious: ₹{a['ctx']['totalPrev']:,}\nAnomalies: {a['detect']['anomaly_count']}\nRecoverable: ₹{a['detect']['total_wasted_spend']:,}\nOrg: {st.session_state.org_name}\nScenario: {scenario}\n\nReturn ONLY valid JSON:\n"
                        '{"scenario_title":"","new_monthly_spend":<int>,"new_spike_pct":<float>,"delta_saving":<int>,"new_health_score":<int 0-100>,"outcome":"BETTER|WORSE|NEUTRAL","key_changes":["","",""],"risks":["",""],"recommendation":"<1 sentence>"}'
                    }], 600)
                    wi = safe_json(resp, {
                        "scenario_title": scenario[:60],
                        "new_monthly_spend": round(a["ctx"]["totalCurr"]*0.8),
                        "new_spike_pct": round(a["detect"]["total_spike_pct"]*0.4,1),
                        "delta_saving": round(a["ctx"]["totalCurr"]*0.2),
                        "new_health_score": min(92, a["report"]["health_score_after"]+12),
                        "outcome":"BETTER",
                        "key_changes":["Spend reduced","Anomaly risk eliminated","Baseline normalised"],
                        "risks":["May affect auto-scaling during peak traffic"],
                        "recommendation":"Recommended with low-risk implementation first.",
                    })
                    oc = {"BETTER":"#00e887","WORSE":"#ff4040","NEUTRAL":"#00d4ff"}.get(wi["outcome"],"#00d4ff")
                    changes_html = "".join(f'<div style="font-size:13px;padding:5px 0;border-bottom:1px solid rgba(255,255,255,.03);display:flex;gap:8px;color:#e0eaf8"><span style="color:#00e887">→</span><span>{c}</span></div>' for c in wi.get("key_changes",[]))
                    risks_html   = "".join(f'<div style="font-size:13px;padding:5px 0;border-bottom:1px solid rgba(255,255,255,.03);display:flex;gap:8px;color:#e0eaf8"><span style="color:#ffbe00">⚠</span><span>{r}</span></div>' for r in wi.get("risks",[]))
                    st.markdown(f"""
                    <div style="background:#080f1a;border:1px solid #111d2e;border-radius:6px;padding:20px;margin-top:16px">
                        <div style="font-family:monospace;font-size:9px;color:#58637a;margin-bottom:12px">Scenario: {wi['scenario_title']}</div>
                        <div style="display:flex;gap:24px;flex-wrap:wrap;margin-bottom:16px">
                            <div><div style="font-family:monospace;font-size:9px;color:#58637a;margin-bottom:4px">OUTCOME</div><div style="font-size:28px;font-weight:900;color:{oc}">{wi['outcome']}</div></div>
                            <div><div style="font-family:monospace;font-size:9px;color:#58637a;margin-bottom:4px">NEW SPEND</div><div style="font-size:28px;font-weight:900;color:#e0eaf8">₹{wi['new_monthly_spend']:,}</div></div>
                            <div><div style="font-family:monospace;font-size:9px;color:#58637a;margin-bottom:4px">ADDITIONAL SAVING</div><div style="font-size:28px;font-weight:900;color:#00e887">₹{wi['delta_saving']:,}</div></div>
                            <div><div style="font-family:monospace;font-size:9px;color:#58637a;margin-bottom:4px">NEW HEALTH</div><div style="font-size:28px;font-weight:900;color:#00d4ff">{wi['new_health_score']}/100</div></div>
                        </div>
                        <div style="display:flex;gap:16px">
                            <div style="flex:1"><div style="font-family:monospace;font-size:9px;color:#58637a;margin-bottom:8px">KEY CHANGES</div>{changes_html}</div>
                            <div style="flex:1"><div style="font-family:monospace;font-size:9px;color:#58637a;margin-bottom:8px">RISKS</div>{risks_html}</div>
                        </div>
                        <div style="margin-top:16px;background:rgba(0,212,255,.08);border:1px solid rgba(0,212,255,.2);border-radius:4px;padding:12px 16px;font-size:13px;color:#e0eaf8">💡 {wi.get('recommendation','')}</div>
                    </div>""", unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Simulation error: {e}")

# ── TAB: CHAT ─────────────────────────────────────────────────────────────────
def tab_chat(a, df):
    st.markdown("""
    <div style="background:#0d1624;border:1px solid #111d2e;border-radius:6px 6px 0 0;
                padding:14px 18px;display:flex;align-items:center;gap:12px;border-bottom:1px solid #111d2e">
        <div style="width:36px;height:36px;border-radius:8px;background:rgba(255,64,64,.1);
                    border:1px solid rgba(255,64,64,.3);display:flex;align-items:center;
                    justify-content:center;font-size:18px">🤖</div>
        <div>
            <div style="font-size:14px;font-weight:700;color:#e0eaf8">AnomalyBot</div>
            <div style="font-family:monospace;font-size:10px;color:#58637a">
                Your AI cloud cost advisor — knows your full analysis</div>
        </div>
        <div style="margin-left:auto;width:7px;height:7px;border-radius:50%;background:#00e887"></div>
    </div>""", unsafe_allow_html=True)

    sugs = ["What caused the biggest spike?","How much can I save?",
            "Which service is most critical?","What actions should I execute first?"]
    sug_cols = st.columns(len(sugs))

    system_prompt = (
        f"You are AnomalyBot — a sharp, concise AI cloud cost advisor. "
        f"Context: Org={st.session_state.org_name}, {st.session_state.period} analysis, "
        f"overall spike={a['detect']['total_spike_pct']:.1f}%, "
        f"anomalies={a['detect']['anomaly_count']}, "
        f"recoverable=₹{a['detect']['total_wasted_spend']:,}, "
        f"risk={a['detect']['risk_level']}. "
        f"Services: {', '.join(r['Service Name'] for _,r in df.iterrows())}. "
        f"Keep answers under 120 words. Use ₹ for currency. Be specific with numbers."
    )

    def _llm_reply(user_msg):
        msgs = [{"role":"system","content":system_prompt}] + st.session_state.chat_history[-10:] + [{"role":"user","content":user_msg}]
        return call_llm(msgs, 200)

    for i, sug in enumerate(sugs):
        with sug_cols[i]:
            if st.button(sug, key=f"sug_btn_{i}", use_container_width=True):
                st.session_state.chat_history.append({"role":"user","content":sug})
                with st.spinner("AnomalyBot is thinking…"):
                    try:
                        reply = _llm_reply(sug)
                    except Exception as e:
                        reply = f"Error: {e}"
                st.session_state.chat_history.append({"role":"assistant","content":reply})
                st.rerun()

    for msg in st.session_state.chat_history:
        with st.chat_message("user" if msg["role"]=="user" else "assistant"):
            st.write(msg["content"])

    if prompt := st.chat_input("Ask AnomalyBot…"):
        st.session_state.chat_history.append({"role":"user","content":prompt})
        with st.chat_message("user"): st.write(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Thinking…"):
                try:
                    reply = _llm_reply(prompt)
                except Exception as e:
                    reply = f"Error: {e}"
            st.write(reply)
            st.session_state.chat_history.append({"role":"assistant","content":reply})

# ── CHART HELPER ──────────────────────────────────────────────────────────────
def _chart_style(fig, title, barmode=None, ytickprefix="", xtickprefix="", xtick_suffix=""):
    opts = dict(
        title=title,
        plot_bgcolor="#04080f", paper_bgcolor="#080f1a",
        font=dict(color="#58637a", size=10),
        title_font=dict(color="#58637a", size=10),
        legend=dict(font=dict(color="#58637a")),
        yaxis=dict(gridcolor="#111d2e", tickprefix=ytickprefix),
        xaxis=dict(gridcolor="#111d2e", tickprefix=xtickprefix, ticksuffix=xtick_suffix),
        margin=dict(l=10, r=10, t=40, b=10),
    )
    if barmode: opts["barmode"] = barmode
    fig.update_layout(**opts)

# ── MAIN ROUTER ───────────────────────────────────────────────────────────────
_PAGE = st.session_state.page
if   _PAGE == "step1":   show_step1()
elif _PAGE == "step2":   show_step2()
elif _PAGE == "running": show_running()
elif _PAGE == "results": show_results()
