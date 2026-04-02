import streamlit as st
import requests
import json
import os

st.set_page_config(layout="wide", page_title="NegotiatorAI")

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.3-70b-versatile"

# ── Read API key from environment ────────────────────────────────────────────
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

# ── Session state init ────────────────────────────────────────────────────────
for k in ["step","result","deals","handle_reply_id","handle_reply_result","error"]:
    if k not in st.session_state:
        st.session_state[k] = None
if "deals" not in st.session_state or st.session_state.deals is None:
    st.session_state.deals = []
if "step" not in st.session_state or st.session_state.step is None:
    st.session_state.step = 1

def call_groq(messages):
    resp = requests.post(
        GROQ_URL,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {GROQ_API_KEY}"},
        json={"model": MODEL, "temperature": 0.65, "max_tokens": 1800, "messages": messages},
        timeout=60
    )
    data = resp.json()
    if "error" in data:
        raise Exception(data["error"].get("message", "Groq API error"))
    return data["choices"][0]["message"]["content"]

def parse_json(text):
    text = text.replace("```json","").replace("```","").strip()
    try:
        return json.loads(text)
    except:
        import re
        m = re.search(r'\{[\s\S]*\}', text)
        if m:
            try: return json.loads(m.group(0))
            except: pass
    return None

def fmt_pct(quoted, target):
    try:
        import re
        q = float(re.sub(r'[^0-9.]','',quoted))
        t = float(re.sub(r'[^0-9.]','',target))
        if q > 0: return f"{round((q-t)/q*100)}%"
    except: pass
    return ""

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
:root {
  --bg: #0d0f14;
  --sf: #13161d;
  --card: #181c26;
  --b1: #1e2330;
  --b2: #252c3d;
  --tx: #e4e9f4;
  --mu: #5a6480;
  --blue: #4f9cf9;
  --green: #00e096;
  --red: #ff4f5e;
  --yellow: #f5c542;
}

html, body, .stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
  background: var(--bg) !important;
  color: var(--tx) !important;
  font-family: Arial, sans-serif !important;
}

header[data-testid="stHeader"],
footer,
[data-testid="stToolbar"],
[data-testid="stDecoration"] {
  display: none !important;
}

.block-container {
  padding: 0 !important;
  max-width: 100% !important;
}

/* ── Navbar ── */
.on-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 32px;
  border-bottom: 1px solid var(--b1);
  background: var(--bg);
}
.on-logo-wrap { display: flex; align-items: center; gap: 12px; }
.on-logo {
  width: 36px; height: 36px; border-radius: 10px;
  background: linear-gradient(135deg,#4f9cf9,#a855f7);
  display: flex; align-items: center; justify-content: center; font-size: 18px;
}
.on-brand { font-size: 18px; font-weight: 700; }
.on-badge {
  padding: 3px 10px; border: 1px solid var(--b2); border-radius: 20px;
  font-size: 9px; color: var(--mu); font-weight: 600;
  letter-spacing: 1.5px; text-transform: uppercase; font-family: 'Courier New', monospace;
}

/* ── Hero ── */
.hero-label {
  font-size: 9px; font-weight: 600; letter-spacing: 2px;
  text-transform: uppercase; color: var(--mu); margin-bottom: 10px;
  font-family: 'Courier New', monospace;
}
.hero-h1 { font-size: 36px; font-weight: 700; line-height: 1.1; margin-bottom: 14px; }
.c-white { color: var(--tx); }
.c-blue { color: var(--blue); }
.c-green { color: var(--green); }
.feat-tags { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 20px; }
.feat-tag {
  border: 1px solid var(--b2); padding: 3px 8px; border-radius: 4px;
  font-size: 10px; color: var(--mu); display: inline-block;
}

/* ── Step bar ── */
.steps-bar {
  display: flex; gap: 6px; margin-bottom: 20px;
}
.step-tab {
  flex: 1; display: flex; flex-direction: column; align-items: center;
  gap: 3px; padding: 10px 4px 8px; border-radius: 8px;
  border: 1px solid var(--b1); background: var(--sf);
}
.step-tab.active { border-color: var(--blue); background: rgba(79,156,249,0.06); }
.step-tab.done  { border-color: rgba(0,224,150,0.3); background: rgba(0,224,150,0.04); }
.st-num {
  font-size: 9px; font-weight: 700; color: var(--mu);
  font-family: 'Courier New', monospace; letter-spacing: 1px;
}
.step-tab.active .st-num { color: var(--blue); }
.step-tab.done  .st-num  { color: var(--green); }
.st-ico  { font-size: 14px; }
.st-label {
  font-size: 9px; font-weight: 600; color: var(--mu);
  letter-spacing: 0.5px; text-transform: uppercase;
}
.step-tab.active .st-label { color: var(--blue); }
.step-tab.done  .st-label  { color: var(--green); }

/* ── Section rule ── */
.srule { display: flex; align-items: center; gap: 10px; margin-bottom: 16px; }
.srule-title {
  font-size: 9px; font-weight: 700; letter-spacing: 2px;
  text-transform: uppercase; color: var(--mu); white-space: nowrap;
  font-family: 'Courier New', monospace;
}
.srule-line { flex: 1; height: 1px; background: var(--b1); }

/* ── Tip box ── */
.tip-box {
  display: flex; align-items: flex-start; gap: 8px;
  background: rgba(79,156,249,0.06); border: 1px solid rgba(79,156,249,0.18);
  border-radius: 8px; padding: 12px 14px; font-size: 12px;
  color: var(--mu); line-height: 1.6; margin-bottom: 16px;
}

/* ── Cards ── */
.kpi-card, .result-card, .deal-card {
  background: var(--sf); border: 1px solid var(--b1);
  border-radius: 10px; padding: 16px; margin-bottom: 12px;
}
.kpi-label {
  font-size: 9px; font-weight: 600; letter-spacing: 1.5px;
  text-transform: uppercase; color: var(--mu);
  font-family: 'Courier New', monospace; margin-bottom: 6px;
}
.kpi-val {
  font-size: 20px; font-weight: 700;
  font-family: 'Courier New', monospace; letter-spacing: -1px;
}

/* ── Result cards ── */
.result-card.rc-yellow { background: rgba(245,197,66,0.06); border: 1px solid rgba(245,197,66,0.2); }
.result-card.rc-blue   { background: rgba(79,156,249,0.06);  border: 1px solid rgba(79,156,249,0.2); }
.rc-header {
  font-size: 9px; font-weight: 700; letter-spacing: 2px;
  text-transform: uppercase; font-family: 'Courier New', monospace; margin-bottom: 6px;
}
.rc-content { font-size: 12px; color: var(--tx); line-height: 1.7; }

/* ── Email preview ── */
.email-preview {
  background: var(--sf); border: 1px solid var(--b1);
  border-radius: 10px; overflow: hidden; margin-bottom: 14px;
}
.ep-header {
  border-bottom: 1px solid var(--b1); padding: 12px 16px;
  display: flex; flex-direction: column; gap: 6px;
}
.ep-row { display: flex; align-items: baseline; gap: 10px; font-size: 11px; }
.ep-k {
  font-family: 'Courier New', monospace; font-size: 9px; font-weight: 700;
  letter-spacing: 1px; text-transform: uppercase; color: var(--mu); min-width: 60px;
}
.ep-v { color: var(--tx); flex: 1; word-break: break-word; }
.ep-body {
  padding: 16px; font-size: 12px; line-height: 1.8;
  color: var(--tx); white-space: pre-wrap; word-break: break-word;
}

/* ── Power meter ── */
.power-track {
  height: 4px; background: var(--b2); border-radius: 2px; overflow: hidden; margin-top: 4px;
}
.power-fill { height: 100%; border-radius: 2px; }

/* ── Agent cards ── */
.agent-card {
  display: flex; align-items: center; gap: 12px;
  padding: 12px 14px; border-radius: 10px;
  border: 1px solid var(--b1); background: var(--sf);
  margin-bottom: 8px; position: relative; overflow: hidden;
}
.agent-ico {
  width: 36px; height: 36px; border-radius: 8px;
  border: 1px solid var(--b2); display: flex;
  align-items: center; justify-content: center;
  font-size: 16px; flex-shrink: 0; background: var(--card);
}
.agent-info { flex: 1; min-width: 0; }
.agent-name { font-size: 13px; font-weight: 600; color: var(--tx); }
.agent-desc { font-size: 10px; color: var(--mu); margin-top: 2px; line-height: 1.4; }
.agent-badge {
  font-size: 8px; font-weight: 700; letter-spacing: 1.5px;
  text-transform: uppercase; padding: 3px 8px; border-radius: 20px;
  flex-shrink: 0;
}
.badge-active {
  background: rgba(0,224,150,0.12);
  border: 1px solid rgba(0,224,150,0.3);
  color: var(--green);
}

/* ── Strategy items ── */
.strat-item {
  display: flex; align-items: center; gap: 10px;
  padding: 10px 12px; border-radius: 8px;
  border: 1px solid var(--b1); background: var(--sf);
  margin-bottom: 6px; cursor: pointer;
}
.strat-item.selected { border-color: var(--blue); background: rgba(79,156,249,0.06); }

/* ── Deal card ── */
.deal-card { position: relative; padding-left: 18px; }
.deal-top { display: flex; align-items: flex-start; gap: 10px; }
.deal-vendor { font-size: 13px; font-weight: 700; color: var(--tx); margin-bottom: 2px; }
.deal-product { font-size: 11px; color: var(--mu); }
.deal-prices { text-align: right; margin-left: auto; }
.dp-orig { font-size: 10px; color: var(--mu); text-decoration: line-through; }
.dp-current { font-size: 14px; font-weight: 700; color: var(--green); font-family: 'Courier New', monospace; }
.dp-save { font-size: 10px; color: var(--yellow); }
.dc { display: inline-block; font-size: 9px; font-weight: 700; letter-spacing: 1px;
      text-transform: uppercase; padding: 3px 8px; border-radius: 4px;
      font-family: 'Courier New', monospace; margin-top: 6px; }
.dc-sent { background: rgba(79,156,249,0.12); border: 1px solid rgba(79,156,249,0.3); color: var(--blue); }
.dc-neg  { background: rgba(245,197,66,0.12); border: 1px solid rgba(245,197,66,0.3); color: var(--yellow); }
.dc-done { background: rgba(0,224,150,0.12);  border: 1px solid rgba(0,224,150,0.3);  color: var(--green); }

/* ── Stat strip ── */
.stat-strip {
  display: grid; grid-template-columns: repeat(3,1fr);
  border: 1px solid var(--b1); border-radius: 10px;
  overflow: hidden; margin-top: 20px;
}
.stat-cell { padding: 18px; text-align: center; }
.stat-val { font-size: 28px; font-weight: 700; font-family: 'Courier New', monospace; letter-spacing: -2px; }
.stat-lbl {
  font-size: 9px; color: var(--mu); font-family: 'Courier New', monospace;
  letter-spacing: 1px; text-transform: uppercase; margin-top: 4px;
}

/* ── How-it-works steps ── */
.how-step {
  display: flex; align-items: flex-start; gap: 12px;
  padding: 14px 0; border-bottom: 1px solid var(--b1); position: relative;
}
.how-num {
  width: 28px; height: 28px; border-radius: 50%;
  background: var(--card); display: flex; align-items: center;
  justify-content: center; font-size: 11px; font-weight: 700;
  font-family: 'Courier New', monospace; flex-shrink: 0;
}
.how-title { font-size: 13px; font-weight: 600; color: var(--tx); margin-bottom: 3px; }
.how-desc  { font-size: 11px; color: var(--mu); font-family: 'Courier New', monospace; line-height: 1.6; }

/* ── Empty state ── */
.empty-state { text-align: center; padding: 36px 20px; color: var(--mu); }
.empty-state .ei { font-size: 32px; margin-bottom: 10px; }
.empty-state h3 { font-size: 15px; color: var(--tx); margin: 0 0 6px; }
.empty-state p  { font-size: 12px; margin: 0; }

/* ── Ready badge ── */
.ready-badge {
  padding: 5px 12px; background: rgba(0,224,150,0.12);
  border: 1px solid rgba(0,224,150,0.3); border-radius: 4px;
  font-size: 9px; font-weight: 700; letter-spacing: 2px;
  text-transform: uppercase; color: var(--green); font-family: 'Courier New', monospace;
}

/* ── Streamlit widget overrides ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
  background: var(--card) !important;
  border: 1px solid var(--b2) !important;
  border-radius: 8px !important;
  color: var(--tx) !important;
  font-size: 13px !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
  border-color: var(--blue) !important;
  box-shadow: none !important;
}
label { color: var(--mu) !important; font-size: 11px !important; font-weight: 600 !important; }
.stButton > button {
  background: var(--blue) !important; color: #fff !important;
  border: none !important; border-radius: 8px !important;
  font-weight: 600 !important; width: 100% !important;
}
.stButton > button[kind="secondary"] {
  background: transparent !important; color: var(--mu) !important;
  border: 1px solid var(--b2) !important;
}
.stRadio > div { gap: 6px !important; }
.stRadio > div > label {
  background: var(--sf) !important; border: 1px solid var(--b1) !important;
  border-radius: 8px !important; padding: 10px 12px !important;
  cursor: pointer !important; width: 100% !important;
}
.stAlert { border-radius: 8px !important; }
</style>
""", unsafe_allow_html=True)

# ── Top Navbar ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="on-nav">
  <div class="on-logo-wrap">
    <div class="on-logo">🤝</div>
    <div class="on-brand">Negotiator<span style="color:#4f9cf9">AI</span></div>
    <div class="on-badge">AI PROCUREMENT AGENT</div>
  </div>
  <div style="font-size:11px;color:#5a6480;font-family:'Courier New',monospace">
    Groq · LLaMA 3.3 70B · 4-Step Wizard
  </div>
</div>
""", unsafe_allow_html=True)

# ── Layout ────────────────────────────────────────────────────────────────────
left, right = st.columns([1.2, 1],gap="small")

with left:
    st.markdown("<div style='padding:24px 12px 0'>", unsafe_allow_html=True)

    # Hero
    st.markdown("""
    <div style='margin-bottom:18px'>
      <div class="hero-label">AI-Powered Procurement Negotiation</div>
      <div class="hero-h1">
        <span class="c-white">One Tool.</span><br>
        <span class="c-blue">Negotiate.</span><br>
        <span class="c-green">Save More.</span>
      </div>
      <p style='font-size:13px;color:var(--mu);line-height:1.75;margin-bottom:12px'>
        NegotiatorAI detects the best leverage, crafts killer emails, and handles vendor replies automatically.
      </p>
      <div class="feat-tags">
        <span class="feat-tag">Email Crafter</span>
        <span class="feat-tag">Reply Handler</span>
        <span class="feat-tag">Power Analyser</span>
        <span class="feat-tag">Leverage Max</span>
        <span class="feat-tag">Deal Closer</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Step bar
    s = st.session_state.step
    def tab_cls(n):
        if n == s: return "active"
        if n < s: return "done"
        return ""

    st.markdown(f"""
    <div class="steps-bar">
      <div class="step-tab {tab_cls(1)}">
        <span class="st-num">01</span><span class="st-ico">🔧</span><span class="st-label">Setup</span>
      </div>
      <div class="step-tab {tab_cls(2)}">
        <span class="st-num">02</span><span class="st-ico">📋</span><span class="st-label">Deal Info</span>
      </div>
      <div class="step-tab {tab_cls(3)}">
        <span class="st-num">03</span><span class="st-ico">⚔️</span><span class="st-label">Strategy</span>
      </div>
      <div class="step-tab {tab_cls(4)}">
        <span class="st-num">04</span><span class="st-ico">🚀</span><span class="st-label">Track</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── STEP 1: SETUP ─────────────────────────────────────────────────────────
    if s == 1:
        api_ready = bool(GROQ_API_KEY)
        tip_color = "rgba(0,224,150,0.06)" if api_ready else "rgba(79,156,249,0.06)"
        tip_border = "rgba(0,224,150,0.25)" if api_ready else "rgba(79,156,249,0.18)"
        tip_icon = "✅" if api_ready else "💡"
        tip_text = (
            "<strong style='color:var(--green)'>Groq API key loaded</strong> — the AI engine is ready."
            if api_ready else
            "<strong style='color:var(--red)'>Missing:</strong> Set GROQ_API_KEY in your environment."
        )
        st.markdown(f"""
        <div class="srule"><div class="srule-title">Configuration</div><div class="srule-line"></div></div>
        <div class="tip-box" style="background:{tip_color};border-color:{tip_border}">
          {tip_icon}&nbsp;<span>{tip_text}</span>
        </div>
        """, unsafe_allow_html=True)

        with st.form("form_step1"):
            c1, c2 = st.columns(2)
            with c1:
                name = st.text_input("Your Name / Company ✱", placeholder="Rahul Sharma / TechCorp",
                                     value=st.session_state.get("cfg_name","Your Company"))
            with c2:
                email = st.text_input("Your Email ✱", placeholder="procurement@company.com",
                                      value=st.session_state.get("cfg_email","procurement@company.com"))
            go1 = st.form_submit_button("→  Continue to Deal Details", disabled=not api_ready)
        if go1:
            if not name.strip() or not email.strip():
                st.error("Name and email are required.")
            else:
                st.session_state.cfg_name = name.strip()
                st.session_state.cfg_email = email.strip()
                st.session_state.step = 2
                st.rerun()

    # ── STEP 2: DEAL INFO ─────────────────────────────────────────────────────
    elif s == 2:
        st.markdown("""<div class="srule"><div class="srule-title">Procurement Information</div><div class="srule-line"></div></div>""", unsafe_allow_html=True)
        with st.form("form_step2"):
            c1, c2 = st.columns(2)
            with c1: vendor = st.text_input("Vendor / Supplier ✱", placeholder="Samsung India, Infosys...", value=st.session_state.get("n_vendor",""))
            with c2: vemail = st.text_input("Vendor Email", placeholder="sales@vendor.com", value=st.session_state.get("n_email",""))
            c1, c2, c3 = st.columns(3)
            with c1: product = st.text_input("Product / Service ✱", placeholder="Laptops, Raw Materials...", value=st.session_state.get("n_product",""))
            with c2: qty = st.text_input("Quantity", placeholder="50 units, 500 kg...", value=st.session_state.get("n_qty",""))
            with c3: delivery = st.selectbox("Delivery Needed",
                ["Immediately / ASAP","Within 2 weeks","Within 1 month","Within 3 months","Flexible"], index=2)
            c1, c2, c3 = st.columns(3)
            with c1: quoted = st.text_input("Vendor's Quoted Price ✱", placeholder="₹5,00,000", value=st.session_state.get("n_quoted",""))
            with c2: target = st.text_input("Your Target Price ✱", placeholder="₹3,50,000", value=st.session_state.get("n_target",""))
            with c3: budget = st.text_input("Max Budget (private)", placeholder="₹4,00,000", value=st.session_state.get("n_budget",""))
            c1, c2 = st.columns(2)
            with c1: payment = st.selectbox("Payment Terms",
                ["100% upfront — best leverage","50/50 split","Net 30 days","Net 60 days","Milestone-based"])
            with c2: tone = st.selectbox("Negotiation Tone",
                ["Firm & professional","Highly aggressive","Collaborative partner","Urgent — hard deadline"])
            c1b, c2b = st.columns(2)
            with c1b: back2 = st.form_submit_button("← Back")
            with c2b: go2 = st.form_submit_button("→  Continue to Strategy")
        if back2:
            st.session_state.step = 1; st.rerun()
        if go2:
            if not vendor.strip() or not product.strip() or not quoted.strip() or not target.strip():
                st.error("Vendor, product, quoted price and target price are required.")
            else:
                for k,v in [("n_vendor",vendor),("n_email",vemail),("n_product",product),
                             ("n_qty",qty),("n_delivery",delivery),("n_quoted",quoted),
                             ("n_target",target),("n_budget",budget),("n_payment",payment),("n_tone",tone)]:
                    st.session_state[k] = v
                st.session_state.step = 3; st.rerun()

    # ── STEP 3: STRATEGY ──────────────────────────────────────────────────────
    elif s == 3:
        st.markdown("""<div class="srule"><div class="srule-title">Negotiation Strategy</div><div class="srule-line"></div></div>""", unsafe_allow_html=True)

        strats = [
            ("📦","Bulk Discount","Use quantity as leverage","bulk volume discount"),
            ("💰","Pay Upfront","Offer instant full payment","full upfront payment for discount"),
            ("🤝","Long-term Partner","Promise repeat business","long-term partnership and repeat business"),
            ("⚔️","Beat Competitor","Mention rival quotes","competitor price matching — we have better quotes"),
            ("📊","Budget Cap","Hard limit approach","strict budget constraint — cannot exceed"),
            ("🎁","Bundle Deal","Package multiple items","bundle multiple products for total deal"),
        ]
        saved_strat = st.session_state.get("n_strategy","bulk volume discount")
        strat_names  = [f"{s[0]} {s[1]}" for s in strats]
        strat_values = [s[3] for s in strats]

        st.markdown("""<div style='font-family:"Courier New",monospace;font-size:9px;font-weight:600;letter-spacing:2px;text-transform:uppercase;color:var(--mu);margin-bottom:10px'>Primary Strategy</div>""", unsafe_allow_html=True)
        strat_choice = st.radio("", strat_names, horizontal=False,
                                index=strat_values.index(saved_strat) if saved_strat in strat_values else 0,
                                label_visibility="collapsed")
        chosen_strat = strat_values[strat_names.index(strat_choice)]

        st.markdown("""<div class="srule" style="margin-top:16px"><div class="srule-title">Leverage & Context</div><div class="srule-line"></div></div>""", unsafe_allow_html=True)

        with st.form("form_step3"):
            leverage = st.text_area("Your Leverage Points ✱",
                placeholder="List everything:\n• Buying in bulk (50 units)\n• Can pay 100% upfront today\n• Loyal customer 3 years\n• Comparing 3 quotes right now",
                height=110, value=st.session_state.get("n_leverage",""))
            comp = st.text_input("Competitor Quotes (very powerful)",
                placeholder="e.g. Competitor A quoted ₹3,80,000 · Vendor B at ₹4,00,000",
                value=st.session_state.get("n_comp",""))
            context = st.text_area("Additional Context (optional)",
                placeholder="Past relationship, previous orders, urgency...",
                height=68, value=st.session_state.get("n_context",""))

            power = 0
            for fk in ["n_vendor","n_email","n_product","n_quoted","n_target"]:
                if st.session_state.get(fk,""): power += 10
            if len(st.session_state.get("n_leverage","")) > 30: power += 25
            elif st.session_state.get("n_leverage",""): power += 10
            if st.session_state.get("n_comp",""): power += 15
            if st.session_state.get("n_budget",""): power += 5

            pcolor = "#ff4f5e" if power < 25 else "#ff6b35" if power < 50 else "#f5c542" if power < 75 else "#00e096"
            plabel = "Weak" if power < 25 else "Building" if power < 50 else "Strong 💪" if power < 75 else "Maximum 🔥"
            st.markdown(f"""
            <div style='margin-bottom:8px'>
              <div style='display:flex;justify-content:space-between;margin-bottom:6px'>
                <span style='font-family:"Courier New",monospace;font-size:9px;font-weight:600;letter-spacing:2px;text-transform:uppercase;color:var(--mu)'>Negotiation Power</span>
                <span style='font-family:"Courier New",monospace;font-size:12px;font-weight:700;color:{pcolor}'>{power}% {plabel}</span>
              </div>
              <div class="power-track"><div class="power-fill" style="width:{power}%;background:{pcolor}"></div></div>
            </div>
            """, unsafe_allow_html=True)

            c1b, c2b = st.columns(2)
            with c1b: back3 = st.form_submit_button("← Back")
            with c2b: go3 = st.form_submit_button("🚀  Generate Email")

        if back3:
            st.session_state.step = 2; st.rerun()
        if go3:
            if not leverage.strip():
                st.error("Please add at least one leverage point — this is how the AI negotiates!")
            else:
                st.session_state.n_leverage = leverage
                st.session_state.n_comp = comp
                st.session_state.n_context = context
                st.session_state.n_strategy = chosen_strat

                v = st.session_state
                SYS = """You are an elite procurement negotiation AI agent. Write devastatingly effective negotiation emails.
Rules:
- Use EVERY leverage point — never waste a single one
- Be firm and authoritative, never desperate or weak
- Make a SPECIFIC counter-offer with crystal-clear reasoning
- Use competitor quotes as hard leverage if provided
- Create urgency: mention a decision deadline (end of week)
- Never reveal the maximum budget
- Sign professionally as the buyer
Return ONLY valid JSON (no markdown):
{"subject":"subject","email":"full email body","reasoning":"why this will work (2 sentences)","confidence":85,"predicted_response":"vendor will likely say..."}"""

                USR = f"""Write procurement negotiation email:
From: {v.cfg_name} ({v.cfg_email})
To: {v.n_vendor}
Product: {v.n_product}{f" | Qty: {v.n_qty}" if v.n_qty else ""}
Delivery: {v.n_delivery}
Quoted: {v.n_quoted}
Target: {v.n_target}{f"\nMax budget (NEVER reveal): {v.n_budget}" if v.n_budget else ""}
Payment offer: {v.n_payment}
Tone: {v.n_tone}
Strategy: {v.n_strategy}
Leverage:
{leverage}{f"\nCompetitor quotes (use hard): {comp}" if comp else ""}{f"\nContext: {context}" if context else ""}

Craft the most powerful email to get us to {v.n_target}. Sign as {v.cfg_name}."""

                with st.spinner("LLaMA 3.3 70B crafting your negotiation email..."):
                    try:
                        raw = call_groq([
                            {"role":"system","content":SYS},
                            {"role":"user","content":USR}
                        ])
                        result = parse_json(raw)
                        if not result:
                            result = {"subject":f"Re: {v.n_product} — Pricing Discussion",
                                      "email":raw,"reasoning":"Direct leverage approach.",
                                      "confidence":72,"predicted_response":"Vendor will offer partial reduction."}
                        st.session_state.result = result
                        st.session_state.error = None

                        import time
                        deal = {
                            "id": int(time.time()*1000),
                            "vendor": v.n_vendor, "vendorEmail": v.n_email,
                            "product": v.n_product, "qty": v.n_qty,
                            "quoted": v.n_quoted, "target": v.n_target,
                            "myName": v.cfg_name, "myEmail": v.cfg_email,
                            "subject": result["subject"], "emailBody": result["email"],
                            "confidence": result.get("confidence",72),
                            "status": "sent",
                            "timestamp": __import__('datetime').datetime.now().strftime("%d %b %Y, %H:%M"),
                            "rounds": 0
                        }
                        st.session_state.deals = [deal] + (st.session_state.deals or [])
                        st.session_state.step = 4
                        st.rerun()
                    except Exception as e:
                        st.session_state.error = str(e)
                        st.error(f"API Error: {e}")

    # ── STEP 4: TRACK ─────────────────────────────────────────────────────────
    elif s == 4:
        if st.button("← New Negotiation"):
            st.session_state.step = 1
            st.session_state.result = None
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ── RIGHT PANEL ───────────────────────────────────────────────────────────────
with right:
    st.markdown(
        "<div style='padding:24px 16px 0;border-left:1px solid var(--b1);height:auto;'>",
        unsafe_allow_html=True
    )
    s = st.session_state.step

    # ── Step 1 right panel: Agent cards ───────────────────────────────────────
    if s == 1:
        st.markdown("""
        <div style='font-family:"Courier New",monospace;font-size:10px;font-weight:600;letter-spacing:3px;
        color:var(--mu);text-transform:uppercase;padding-bottom:14px;
        border-bottom:1px solid var(--b1);margin-bottom:16px'>
          Negotiation Agents — 5 Active
        </div>
        """, unsafe_allow_html=True)

        agents = [
            ("#4f9cf9","📝","Email Crafter",    "Writes devastating negotiation emails tailored to your leverage"),
            ("#00e096","🔄","Reply Handler",     "Reads vendor responses and auto-generates counter-offers"),
            ("#f5c542","📊","Power Analyser",    "Scores your negotiation strength and suggests improvements"),
            ("#ff4f5e","⚔️","Leverage Maximiser","Extracts every advantage from your context data"),
            ("#a855f7","🏆","Deal Closer",       "Knows when to push harder and when to close"),
        ]
        for color, ico, name, desc in agents:
            st.markdown(f"""
            <div class="agent-card" style="border-left:3px solid {color}">
              <div class="agent-ico" style="border-color:{color}33">{ico}</div>
              <div class="agent-info">
                <div class="agent-name">{name}</div>
                <div class="agent-desc">{desc}</div>
              </div>
              <span class="agent-badge badge-active">ACTIVE</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div class="stat-strip" style="display:grid;grid-template-columns:repeat(3,1fr);
        border:1px solid var(--b1);border-radius:10px;overflow:hidden;margin-top:20px">
          <div class="stat-cell" style="padding:18px;border-right:1px solid var(--b1);text-align:center">
            <div class="stat-val" style="color:var(--blue)">5</div>
            <div class="stat-lbl">Agents</div>
          </div>
          <div class="stat-cell" style="padding:18px;border-right:1px solid var(--b1);text-align:center">
            <div class="stat-val" style="color:var(--green)">AI</div>
            <div class="stat-lbl">Powered</div>
          </div>
          <div class="stat-cell" style="padding:18px;text-align:center">
            <div class="stat-val" style="color:var(--yellow)">4s</div>
            <div class="stat-lbl">Avg Speed</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Steps 2 & 3 right panel: How It Works ─────────────────────────────────
    elif s in [2, 3]:
        st.markdown("""
        <div style='font-family:"Courier New",monospace;font-size:10px;font-weight:600;
        letter-spacing:3px;color:var(--mu);text-transform:uppercase;
        padding-bottom:14px;border-bottom:1px solid var(--b1);margin-bottom:16px'>
          How It Works
        </div>
        """, unsafe_allow_html=True)

        steps_info = [
            ("#4f9cf9","1","Fill deal details",   "Enter vendor info, quoted price and your target in Step 2"),
            ("#00e096","2","Choose strategy",      "Pick the negotiation angle that fits your situation in Step 3"),
            ("#f5c542","3","Add leverage",         "The more leverage points you list, the stronger your email"),
            ("#a855f7","4","AI generates email",   "LLaMA 3.3 70B on Groq writes a powerful negotiation email"),
            ("#ff4f5e","5","Handle replies",        "Paste vendor replies and AI auto-crafts the perfect counter"),
        ]
        for color, num, title, desc in steps_info:
            st.markdown(f"""
            <div class="how-step" style="border-left:3px solid {color};padding-left:12px">
              <div class="how-num" style="border:1px solid {color}44;color:{color}">{num}</div>
              <div>
                <div class="how-title">{title}</div>
                <div class="how-desc">{desc}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    # ── Step 4 right panel: Email output + Deal tracker ───────────────────────
    elif s == 4:
        result = st.session_state.get("result")
        deals  = st.session_state.get("deals", [])

        if result:
            st.markdown("""
            <div style='display:flex;align-items:center;justify-content:space-between;
            padding-bottom:14px;border-bottom:1px solid var(--b1);margin-bottom:14px'>
              <span style='font-size:16px;font-weight:700;color:var(--tx)'>Email Generated</span>
              <span class="ready-badge">✓ READY</span>
            </div>
            """, unsafe_allow_html=True)

            conf = result.get("confidence", 72)
            pct  = fmt_pct(st.session_state.get("n_quoted",""), st.session_state.get("n_target",""))
            c1, c2, c3 = st.columns(3)
            for col, label, val, color in [
                (c1, "Target Price", st.session_state.get("n_target","—"), "var(--green)"),
                (c2, "Confidence",   f"{conf}%",                           "var(--blue)"),
                (c3, "Reduction",    pct or "—",                           "var(--yellow)"),
            ]:
                with col:
                    st.markdown(f"""
                    <div class="kpi-card">
                      <div class="kpi-label">{label}</div>
                      <div class="kpi-val" style="color:{color}">{val}</div>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="result-card rc-yellow">
              <div class="rc-header" style="color:var(--yellow)">Why This Will Work</div>
              <div class="rc-content">{result.get("reasoning","")}</div>
            </div>
            <div class="result-card rc-blue">
              <div class="rc-header" style="color:var(--blue)">Predicted Vendor Response</div>
              <div class="rc-content">{result.get("predicted_response","")}</div>
            </div>
            """, unsafe_allow_html=True)

            v = st.session_state
            st.markdown(f"""
            <div class="email-preview">
              <div class="ep-header">
                <div class="ep-row"><span class="ep-k">FROM</span><span class="ep-v">{v.get("cfg_name","")} &lt;{v.get("cfg_email","")}&gt;</span></div>
                <div class="ep-row"><span class="ep-k">TO</span><span class="ep-v">{v.get("n_vendor","")} &lt;{v.get("n_email","")}&gt;</span></div>
                <div class="ep-row"><span class="ep-k">SUBJECT</span><span class="ep-v">{result.get("subject","")}</span></div>
              </div>
              <div class="ep-body">{result.get("email","").replace("<","&lt;").replace(">","&gt;")}</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

        # Deal Tracker
        st.markdown("""<div class="srule"><div class="srule-title">Deal Tracker</div><div class="srule-line"></div></div>""", unsafe_allow_html=True)

        if not deals:
            st.markdown("""
            <div class="empty-state">
              <div class="ei">📁</div>
              <h3>No deals yet</h3>
              <p>Complete the form to see deals here</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            deal_colors = {"sent":"#4f9cf9","negotiating":"#f5c542","closed":"#00e096"}
            for deal in deals:
                status = deal.get("status","sent")
                ico = "📤" if status=="sent" else "🔄" if status=="negotiating" else "🏆"
                badge_cls = "dc-sent" if status=="sent" else "dc-neg" if status=="negotiating" else "dc-done"
                badge_label = "Email Sent" if status=="sent" else f"Negotiating · Round {deal.get('rounds',0)}" if status=="negotiating" else "Deal Closed"
                display_price = deal.get("finalPrice") or deal.get("predicted") or deal.get("target","")
                pct_str = fmt_pct(deal.get("quoted",""), display_price)
                dc = deal_colors.get(status, "#4f9cf9")

                st.markdown(f"""
                <div class="deal-card" style="border-left:3px solid {dc}">
                  <div class="deal-top">
                    <div style="font-size:18px;flex-shrink:0;margin-top:2px">{ico}</div>
                    <div style="flex:1;min-width:0">
                      <div class="deal-vendor">{deal['vendor']}</div>
                      <div class="deal-product">{deal['product']}{f" — {deal['qty']}" if deal.get('qty') else ""}</div>
                      <div style="font-size:10px;color:var(--mu);font-style:italic;margin-bottom:4px">{deal.get('subject','')}</div>
                      <span class="dc {badge_cls}">{badge_label}</span>
                    </div>
                    <div class="deal-prices">
                      <div class="dp-orig">{deal['quoted']}</div>
                      <div class="dp-current">{display_price}</div>
                      {f'<div class="dp-save">↓ {pct_str} off</div>' if pct_str else ''}
                    </div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

                if status != "closed":
                    col_a, col_b = st.columns(2)
                    with col_a:
                        if st.button(f"🔄 Handle Reply", key=f"reply_{deal['id']}"):
                            st.session_state.handle_reply_id = deal["id"]
                            st.rerun()
                    with col_b:
                        if st.button(f"✅ Close Deal", key=f"close_{deal['id']}"):
                            deal["status"] = "closed"
                            deal["finalPrice"] = deal.get("predicted") or deal["target"]
                            st.rerun()

            if st.session_state.handle_reply_id:
                deal_id = st.session_state.handle_reply_id
                deal = next((d for d in deals if d["id"] == deal_id), None)
                if deal:
                    st.markdown(f"""
                    <div style='background:rgba(79,156,249,0.06);border:1px solid rgba(79,156,249,0.2);
                    border-radius:8px;padding:14px;margin-top:12px;
                    font-family:"Courier New",monospace;font-size:11px;color:var(--blue)'>
                      Paste vendor reply for <strong style='color:var(--tx)'>{deal['vendor']}</strong> below:
                    </div>
                    """, unsafe_allow_html=True)

                    with st.form(f"reply_form_{deal_id}"):
                        vendor_reply = st.text_area("Vendor's Reply Email",
                            placeholder="Paste their full response here...", height=120)
                        c1r, c2r = st.columns(2)
                        with c1r: cancel_reply = st.form_submit_button("Cancel")
                        with c2r: send_reply = st.form_submit_button("🤖 Generate Counter-Offer")

                    if cancel_reply:
                        st.session_state.handle_reply_id = None
                        st.rerun()

                    if send_reply:
                        if not vendor_reply.strip():
                            st.error("Please paste the vendor's reply.")
                        else:
                            SYS2 = """You are an elite procurement negotiation AI. Vendor has replied. Craft the strongest counter-response.
Rules:
- Acknowledge them professionally
- Identify and dismantle weak excuses
- Push firmly toward target price
- Use any new info as additional leverage
Return ONLY valid JSON:
{"subject":"subject","email":"full counter-email","analysis":"what their reply reveals","new_predicted_price":"achievable price","confidence":80,"recommendation":"push more | accept | close deal"}"""
                            USR2 = f"""Context: Vendor={deal['vendor']} | Product={deal['product']} | Quote={deal['quoted']} | Target={deal['target']}

Vendor's reply:
{vendor_reply}

Write strongest counter-response toward {deal['target']}. Sign as {deal['myName']}."""
                            with st.spinner("AI reading reply and crafting counter-offer..."):
                                try:
                                    raw = call_groq([
                                        {"role":"system","content":SYS2},
                                        {"role":"user","content":USR2}
                                    ])
                                    r = parse_json(raw)
                                    if not r:
                                        r = {"subject":f"Re: {deal['product']}","email":raw,
                                             "analysis":"Vendor is open to negotiation.",
                                             "new_predicted_price":deal["target"],
                                             "confidence":70,"recommendation":"push more"}
                                    deal["status"] = "negotiating"
                                    deal["predicted"] = r.get("new_predicted_price", deal["target"])
                                    deal["rounds"] = deal.get("rounds",0) + 1
                                    st.session_state.handle_reply_id = None
                                    st.session_state.result = {
                                        "subject": r["subject"],
                                        "email": r["email"],
                                        "reasoning": r.get("analysis",""),
                                        "confidence": r.get("confidence",72),
                                        "predicted_response": f"Recommendation: {r.get('recommendation','')} — Predicted: {r.get('new_predicted_price','')}"
                                    }
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"API Error: {e}")

    st.markdown("</div>", unsafe_allow_html=True)
