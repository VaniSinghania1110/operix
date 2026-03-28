"""
╔══════════════════════════════════════════════════════════════╗
║   OPERIX — AI Operations Intelligence Platform               ║
║   Front Page: Equal navigation to all 7 modules              ║
║   Run: streamlit run app.py                                  ║
╚══════════════════════════════════════════════════════════════╝

Folder structure:
    app.py                       ← this file
    pages/
        sla.py
        res.py
        app1.py
        anomaly.py
        costcutter.py
        neg.py
        dup.py
"""

import streamlit as st

st.set_page_config(
    page_title="Operix — AI Ops Intelligence",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=IBM+Plex+Mono:wght@400;500;600&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500&display=swap');

:root {
  --bg:   #07080f;
  --bg2:  #0d0f1c;
  --bg3:  #121525;
  --bg4:  #181c2e;
  --c1:   #ff5353;
  --c2:   #00d97e;
  --c3:   #4d9fff;
  --c4:   #f0b429;
  --c5:   #a855f7;
  --c6:   #f97316;
  --c7:   #06b6d4;
  --gold: #f0b429;
  --text: #dde3f5;
  --sub:  #5a6282;
  --sub2: #8490b5;
  --bd:   rgba(255,255,255,0.055);
  --bd2:  rgba(255,255,255,0.10);
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
  background: var(--bg) !important;
  font-family: 'DM Sans', sans-serif !important;
  color: var(--text) !important;
}

#MainMenu, footer, header,
[data-testid="stDecoration"],
[data-testid="stToolbar"],
[data-testid="stStatusWidget"],
[data-testid="stSidebarNav"] { display: none !important; }

[data-testid="stMainBlockContainer"] {
  max-width: 1080px !important;
  padding: 0 2rem 5rem !important;
  margin: 0 auto !important;
}
[data-testid="stVerticalBlock"] { gap: 0 !important; }
[data-testid="stHorizontalBlock"] { gap: 16px !important; }

::-webkit-scrollbar { width: 3px; }
::-webkit-scrollbar-thumb { background: rgba(77,159,255,0.2); border-radius: 10px; }

@keyframes fadeUp  { from { opacity:0; transform:translateY(18px); } to { opacity:1; transform:translateY(0); } }
@keyframes pulse   { 0%,100%{opacity:1} 50%{opacity:.25} }
@keyframes orbF    { 0%,100%{transform:translateY(0) translateX(0)} 50%{transform:translateY(-12px) translateX(6px)} }
@keyframes barGrow { from{width:0} }

.au { animation: fadeUp .5s ease both; }
.d1{animation-delay:.07s} .d2{animation-delay:.14s} .d3{animation-delay:.21s}
.d4{animation-delay:.28s} .d5{animation-delay:.35s} .d6{animation-delay:.42s}

/* NAV */
.nav {
  display:flex; align-items:center; gap:16px;
  padding:1.5rem 0 1.2rem; border-bottom:1px solid var(--bd);
}
.nav-logo {
  display:flex; align-items:center; gap:11px;
  font-family:'Syne',sans-serif; font-size:1.35rem;
  font-weight:800; color:var(--text);
}
.nav-mark {
  width:36px; height:36px; border-radius:10px;
  background:linear-gradient(135deg,#4d9fff,#1a5fcc);
  display:flex; align-items:center; justify-content:center;
  font-size:16px; font-weight:900; color:white;
  box-shadow:0 0 20px rgba(77,159,255,0.3);
}
.nav-pill {
  display:inline-flex; align-items:center; gap:7px;
  background:rgba(77,159,255,0.08); border:1px solid rgba(77,159,255,0.22);
  padding:5px 13px; border-radius:5px;
  font-family:'IBM Plex Mono',monospace; font-size:9px;
  letter-spacing:2px; text-transform:uppercase; color:var(--c3);
}
.nav-dot { width:5px; height:5px; border-radius:50%; background:var(--c3); animation:pulse 1.4s infinite; }
.nav-sp  { flex:1; }
.nav-mdl { font-family:'IBM Plex Mono',monospace; font-size:9px; color:var(--sub); letter-spacing:1.5px; }

/* HERO */
.eyebrow {
  font-family:'IBM Plex Mono',monospace; font-size:10px;
  letter-spacing:3px; text-transform:uppercase; color:var(--sub);
  margin-bottom:16px; display:flex; align-items:center; gap:10px;
}
.eyebrow-line { height:1px; width:50px; background:var(--bd2); }
.h1 {
  font-family:'Syne',sans-serif;
  font-size:clamp(2.6rem,5vw,4rem);
  font-weight:800; letter-spacing:-1.5px; line-height:1.08; margin-bottom:20px;
}
.h1 .w1{color:var(--c3)} .h1 .w2{color:var(--c2)} .h1 .w3{color:var(--c1)}
.hero-sub {
  font-size:15px; color:var(--sub2); line-height:1.75;
  max-width:480px; margin-bottom:30px;
}
.hero-tags { display:flex; flex-wrap:wrap; gap:8px; margin-bottom:28px; }
.htag {
  font-family:'IBM Plex Mono',monospace; font-size:9.5px;
  padding:4px 11px; border-radius:4px;
  border:1px solid var(--bd2); color:var(--sub2);
}

/* MODULE PREVIEWS */
.mod-stack { display:flex; flex-direction:column; gap:10px; }
.mod-card {
  background:var(--bg2); border:1px solid var(--bd);
  border-radius:14px; padding:14px 16px;
  display:flex; align-items:center; gap:14px;
  transition:all .25s; position:relative; overflow:hidden;
}
.mod-card::before {
  content:''; position:absolute; top:0; left:0; width:3px; bottom:0; border-radius:14px 0 0 14px;
}
.mod-card.red::before{background:var(--c1)}
.mod-card.grn::before{background:var(--c2)}
.mod-card.blu::before{background:var(--c3)}
.mod-card.gold::before{background:var(--c4)}
.mod-card.pur::before{background:var(--c5)}
.mod-card.ora::before{background:var(--c6)}
.mod-card.cyn::before{background:var(--c7)}
.mod-card:hover { transform:translateX(5px); border-color:var(--bd2); }
.mi {
  width:42px; height:42px; border-radius:11px;
  display:flex; align-items:center; justify-content:center;
  font-size:20px; flex-shrink:0;
}
.mi.red{background:rgba(255,83,83,0.1)}
.mi.grn{background:rgba(0,217,126,0.1)}
.mi.blu{background:rgba(77,159,255,0.1)}
.mi.gold{background:rgba(240,180,41,0.1)}
.mi.pur{background:rgba(168,85,247,0.1)}
.mi.ora{background:rgba(249,115,22,0.1)}
.mi.cyn{background:rgba(6,182,212,0.1)}
.mn { font-family:'Syne',sans-serif; font-size:14px; font-weight:700; color:var(--text); margin-bottom:3px; }
.md { font-size:11.5px; color:var(--sub2); line-height:1.5; }
.mbadge {
  font-family:'IBM Plex Mono',monospace; font-size:8.5px;
  padding:2px 8px; border-radius:4px; flex-shrink:0;
  letter-spacing:1px; text-transform:uppercase;
}
.mbadge.red{background:rgba(255,83,83,0.1);color:var(--c1);border:1px solid rgba(255,83,83,0.2)}
.mbadge.grn{background:rgba(0,217,126,0.1);color:var(--c2);border:1px solid rgba(0,217,126,0.2)}
.mbadge.blu{background:rgba(77,159,255,0.1);color:var(--c3);border:1px solid rgba(77,159,255,0.2)}
.mbadge.gold{background:rgba(240,180,41,0.1);color:var(--c4);border:1px solid rgba(240,180,41,0.2)}
.mbadge.pur{background:rgba(168,85,247,0.1);color:var(--c5);border:1px solid rgba(168,85,247,0.2)}
.mbadge.ora{background:rgba(249,115,22,0.1);color:var(--c6);border:1px solid rgba(249,115,22,0.2)}
.mbadge.cyn{background:rgba(6,182,212,0.1);color:var(--c7);border:1px solid rgba(6,182,212,0.2)}

.hstat-row { display:grid; grid-template-columns:repeat(3,1fr); gap:10px; margin-top:12px; }
.hstat {
  background:var(--bg2); border:1px solid var(--bd);
  border-radius:12px; padding:12px 14px; text-align:center;
}
.hstat-n { font-family:'Syne',sans-serif; font-size:1.55rem; font-weight:800; line-height:1; margin-bottom:4px; }
.hstat-l { font-family:'IBM Plex Mono',monospace; font-size:8.5px; letter-spacing:1.5px; text-transform:uppercase; color:var(--sub); }

/* STATS GRID */
.sg { display:grid; grid-template-columns:repeat(4,1fr); gap:12px; margin:28px 0; }
.sb { background:var(--bg2); border:1px solid var(--bd); border-radius:14px; padding:18px 16px; position:relative; overflow:hidden; }
.sb::after { content:''; position:absolute; bottom:0; left:0; right:0; height:2px; }
.sb.r::after{background:linear-gradient(90deg,var(--c1),transparent)}
.sb.g::after{background:linear-gradient(90deg,var(--c2),transparent)}
.sb.b::after{background:linear-gradient(90deg,var(--c3),transparent)}
.sb.y::after{background:linear-gradient(90deg,var(--gold),transparent)}
.sbn { font-family:'Syne',sans-serif; font-size:2.2rem; font-weight:800; line-height:1; margin-bottom:5px; }
.sbl { font-family:'IBM Plex Mono',monospace; font-size:8.5px; letter-spacing:2px; text-transform:uppercase; color:var(--sub); }
.sbm { font-size:11.5px; color:var(--sub2); margin-top:4px; }

/* SECTION HEADER */
.sec-lbl { font-family:'IBM Plex Mono',monospace; font-size:9px; letter-spacing:3px; text-transform:uppercase; color:var(--sub); margin-bottom:8px; }
.sec-ttl { font-family:'Syne',sans-serif; font-size:1.75rem; font-weight:800; letter-spacing:-.5px; color:var(--text); margin-bottom:6px; }
.sec-sub { font-size:14px; color:var(--sub2); margin-bottom:28px; }

/* FEATURE CARDS */
.fcard {
  background:var(--bg2); border:1px solid var(--bd);
  border-radius:20px; padding:26px 22px 22px;
  position:relative; overflow:hidden;
  transition:all .25s cubic-bezier(.4,0,.2,1); height:100%;
}
.fcard:hover { transform:translateY(-5px); border-color:var(--bd2); box-shadow:0 24px 60px rgba(0,0,0,.5); }
.fcg { position:absolute; top:-60px; right:-60px; width:180px; height:180px; border-radius:50%; opacity:0; transition:opacity .3s; pointer-events:none; }
.fcard:hover .fcg { opacity:1; }
.fcard.red .fcg{background:radial-gradient(circle,rgba(255,83,83,.12) 0%,transparent 70%)}
.fcard.grn .fcg{background:radial-gradient(circle,rgba(0,217,126,.10) 0%,transparent 70%)}
.fcard.blu .fcg{background:radial-gradient(circle,rgba(77,159,255,.10) 0%,transparent 70%)}
.fcard.gold .fcg{background:radial-gradient(circle,rgba(240,180,41,.10) 0%,transparent 70%)}
.fcard.pur .fcg{background:radial-gradient(circle,rgba(168,85,247,.10) 0%,transparent 70%)}
.fcard.ora .fcg{background:radial-gradient(circle,rgba(249,115,22,.10) 0%,transparent 70%)}
.fcard.cyn .fcg{background:radial-gradient(circle,rgba(6,182,212,.10) 0%,transparent 70%)}
.fcard-top { display:flex; align-items:flex-start; justify-content:space-between; margin-bottom:18px; }
.fci { width:50px; height:50px; border-radius:14px; display:flex; align-items:center; justify-content:center; font-size:22px; }
.fci.red{background:rgba(255,83,83,0.1);border:1px solid rgba(255,83,83,0.2)}
.fci.grn{background:rgba(0,217,126,0.08);border:1px solid rgba(0,217,126,0.18)}
.fci.blu{background:rgba(77,159,255,0.1);border:1px solid rgba(77,159,255,0.18)}
.fci.gold{background:rgba(240,180,41,0.08);border:1px solid rgba(240,180,41,0.2)}
.fci.pur{background:rgba(168,85,247,0.1);border:1px solid rgba(168,85,247,0.2)}
.fci.ora{background:rgba(249,115,22,0.1);border:1px solid rgba(249,115,22,0.2)}
.fci.cyn{background:rgba(6,182,212,0.08);border:1px solid rgba(6,182,212,0.2)}
.fclbl {
  font-family:'IBM Plex Mono',monospace; font-size:8.5px;
  padding:3px 9px; border-radius:4px; letter-spacing:1.5px; text-transform:uppercase; margin-top:2px;
}
.fclbl.red{background:rgba(255,83,83,0.1);color:var(--c1);border:1px solid rgba(255,83,83,0.22)}
.fclbl.grn{background:rgba(0,217,126,0.08);color:var(--c2);border:1px solid rgba(0,217,126,0.2)}
.fclbl.blu{background:rgba(77,159,255,0.1);color:var(--c3);border:1px solid rgba(77,159,255,0.2)}
.fclbl.gold{background:rgba(240,180,41,0.08);color:var(--c4);border:1px solid rgba(240,180,41,0.2)}
.fclbl.pur{background:rgba(168,85,247,0.1);color:var(--c5);border:1px solid rgba(168,85,247,0.2)}
.fclbl.ora{background:rgba(249,115,22,0.1);color:var(--c6);border:1px solid rgba(249,115,22,0.2)}
.fclbl.cyn{background:rgba(6,182,212,0.08);color:var(--c7);border:1px solid rgba(6,182,212,0.2)}
.fcttl { font-family:'Syne',sans-serif; font-size:1.2rem; font-weight:700; color:var(--text); margin-bottom:10px; letter-spacing:-.3px; }
.fcdesc { font-size:13px; color:var(--sub2); line-height:1.7; margin-bottom:18px; }
.fcchips { display:flex; flex-wrap:wrap; gap:6px; margin-bottom:20px; }
.chip { font-family:'IBM Plex Mono',monospace; font-size:9px; padding:3px 9px; border-radius:20px; border:1px solid var(--bd2); color:var(--sub2); }
.fcfoot { border-top:1px solid var(--bd); padding-top:14px; display:flex; align-items:center; justify-content:space-between; }
.fclink { font-family:'IBM Plex Mono',monospace; font-size:9.5px; letter-spacing:1.5px; text-transform:uppercase; }
.fclink.red{color:var(--c1)} .fclink.grn{color:var(--c2)} .fclink.blu{color:var(--c3)}
.fclink.gold{color:var(--c4)} .fclink.pur{color:var(--c5)} .fclink.ora{color:var(--c6)} .fclink.cyn{color:var(--c7)}
.fcarr { width:28px; height:28px; border-radius:8px; display:flex; align-items:center; justify-content:center; font-size:13px; transition:transform .2s; }
.fcard:hover .fcarr { transform:translate(3px,-3px); }
.fcarr.red{background:rgba(255,83,83,0.1)} .fcarr.grn{background:rgba(0,217,126,0.08)} .fcarr.blu{background:rgba(77,159,255,0.1)}
.fcarr.gold{background:rgba(240,180,41,0.1)} .fcarr.pur{background:rgba(168,85,247,0.1)} .fcarr.ora{background:rgba(249,115,22,0.1)} .fcarr.cyn{background:rgba(6,182,212,0.08)}

/* PIPELINE */
.pipeline { display:grid; grid-template-columns:repeat(5,1fr); gap:0; background:var(--bg2); border:1px solid var(--bd); border-radius:18px; overflow:hidden; margin:28px 0; }
.pip-step { padding:20px 14px; text-align:center; border-right:1px solid var(--bd); position:relative; }
.pip-step:last-child { border-right:none; }
.pip-icon { font-size:22px; margin-bottom:10px; display:block; }
.pip-num { position:absolute; top:12px; right:12px; font-family:'IBM Plex Mono',monospace; font-size:9px; color:var(--sub); }
.pip-name { font-family:'Syne',sans-serif; font-size:12.5px; font-weight:700; color:var(--text); margin-bottom:5px; }
.pip-desc { font-size:11px; color:var(--sub2); line-height:1.55; }
.pip-agent { font-family:'IBM Plex Mono',monospace; font-size:8px; color:var(--sub); margin-top:8px; letter-spacing:1px; text-transform:uppercase; }

/* CTA */
.cta {
  background:var(--bg2); border:1px solid var(--bd); border-radius:20px;
  padding:2.8rem 2.5rem; text-align:center; position:relative; overflow:hidden; margin:3rem 0 1rem;
}
.cta::before { content:''; position:absolute; inset:0; background:radial-gradient(ellipse at 50% 0%,rgba(77,159,255,0.07) 0%,transparent 65%); pointer-events:none; }
.cta-h { font-family:'Syne',sans-serif; font-size:2rem; font-weight:800; letter-spacing:-1px; color:var(--text); margin-bottom:10px; position:relative; }
.cta-p { font-size:14px; color:var(--sub2); position:relative; }

/* BUTTONS — base */
.stButton > button {
  background:var(--bg3) !important; border:1.5px solid var(--bd2) !important;
  color:var(--sub2) !important; font-family:'DM Sans',sans-serif !important;
  font-size:13px !important; font-weight:600 !important;
  border-radius:10px !important; transition:all .2s !important;
}
.stButton > button:hover {
  border-color:rgba(255,255,255,.2) !important; color:var(--text) !important;
  background:var(--bg4) !important; transform:translateY(-1px) !important;
}

/* red */
.btn-red .stButton > button {
  background:linear-gradient(135deg,#ff5353,#b82020) !important;
  border:none !important; color:white !important;
  font-family:'Syne',sans-serif !important; font-size:14px !important;
  font-weight:700 !important; border-radius:12px !important; height:3.4em !important;
  box-shadow:0 0 28px rgba(255,83,83,.22),0 6px 16px rgba(255,83,83,.12) !important;
}
.btn-red .stButton > button:hover { transform:translateY(-3px) !important; box-shadow:0 0 48px rgba(255,83,83,.38),0 12px 28px rgba(255,83,83,.2) !important; }

/* green */
.btn-grn .stButton > button {
  background:linear-gradient(135deg,#00b866,#006636) !important;
  border:none !important; color:white !important;
  font-family:'Syne',sans-serif !important; font-size:14px !important;
  font-weight:700 !important; border-radius:12px !important; height:3.4em !important;
  box-shadow:0 0 28px rgba(0,217,126,.18) !important;
}
.btn-grn .stButton > button:hover { transform:translateY(-3px) !important; box-shadow:0 0 48px rgba(0,217,126,.32) !important; }

/* blue */
.btn-blu .stButton > button {
  background:linear-gradient(135deg,#3080e8,#154090) !important;
  border:none !important; color:white !important;
  font-family:'Syne',sans-serif !important; font-size:14px !important;
  font-weight:700 !important; border-radius:12px !important; height:3.4em !important;
  box-shadow:0 0 28px rgba(77,159,255,.18) !important;
}
.btn-blu .stButton > button:hover { transform:translateY(-3px) !important; box-shadow:0 0 48px rgba(77,159,255,.32) !important; }

/* gold */
.btn-gold .stButton > button {
  background:linear-gradient(135deg,#f0b429,#a07210) !important;
  border:none !important; color:white !important;
  font-family:'Syne',sans-serif !important; font-size:14px !important;
  font-weight:700 !important; border-radius:12px !important; height:3.4em !important;
  box-shadow:0 0 28px rgba(240,180,41,.18) !important;
}
.btn-gold .stButton > button:hover { transform:translateY(-3px) !important; box-shadow:0 0 48px rgba(240,180,41,.32) !important; }

/* purple */
.btn-pur .stButton > button {
  background:linear-gradient(135deg,#a855f7,#6b21a8) !important;
  border:none !important; color:white !important;
  font-family:'Syne',sans-serif !important; font-size:14px !important;
  font-weight:700 !important; border-radius:12px !important; height:3.4em !important;
  box-shadow:0 0 28px rgba(168,85,247,.18) !important;
}
.btn-pur .stButton > button:hover { transform:translateY(-3px) !important; box-shadow:0 0 48px rgba(168,85,247,.32) !important; }

/* orange */
.btn-ora .stButton > button {
  background:linear-gradient(135deg,#f97316,#9a3f08) !important;
  border:none !important; color:white !important;
  font-family:'Syne',sans-serif !important; font-size:14px !important;
  font-weight:700 !important; border-radius:12px !important; height:3.4em !important;
  box-shadow:0 0 28px rgba(249,115,22,.18) !important;
}
.btn-ora .stButton > button:hover { transform:translateY(-3px) !important; box-shadow:0 0 48px rgba(249,115,22,.32) !important; }

/* cyan */
.btn-cyn .stButton > button {
  background:linear-gradient(135deg,#06b6d4,#0e5f72) !important;
  border:none !important; color:white !important;
  font-family:'Syne',sans-serif !important; font-size:14px !important;
  font-weight:700 !important; border-radius:12px !important; height:3.4em !important;
  box-shadow:0 0 28px rgba(6,182,212,.18) !important;
}
.btn-cyn .stButton > button:hover { transform:translateY(-3px) !important; box-shadow:0 0 48px rgba(6,182,212,.32) !important; }

/* FOOTER */
.foot { text-align:center; padding:2.5rem 0 .5rem; border-top:1px solid var(--bd); margin-top:2rem; font-family:'IBM Plex Mono',monospace; font-size:9.5px; color:var(--sub); }
.foot em { color:var(--c3); font-style:normal; }

/* MODULE GRID — 7-up quick-launch strip */
.mod-grid {
  display:grid; grid-template-columns:repeat(7,1fr); gap:10px; margin:20px 0 0;
}
</style>
""", unsafe_allow_html=True)


# ── NAVBAR ──────────────────────────────────────────────────
st.markdown("""
<div class="nav au">
  <div class="nav-logo">
    <div class="nav-mark">O</div>
    Oper<span style="color:var(--c3)">ix</span>
  </div>
  <div class="nav-pill"><span class="nav-dot"></span>AI Ops Intelligence</div>
  <div class="nav-sp"></div>
  <div class="nav-mdl">Groq · LLaMA 3.3 70B · 7-Agent Platform</div>
</div>
""", unsafe_allow_html=True)


# ── HERO ────────────────────────────────────────────────────
hl, hr = st.columns([1.15, 1], gap="large")

with hl:
    st.markdown("""
    <div class="au" style="padding:3.5rem 0 1rem;">
      <div class="eyebrow">⬡ AI-Powered Project Operations <span class="eyebrow-line"></span></div>
      <h1 class="h1">
        One Platform.<br>
        <span class="w1">Predict.</span> <span class="w2">Optimise.</span><br>
        <span class="w3">Improve.</span>
      </h1>
      <p class="hero-sub">
        Operix is an intelligent operations assistant that detects SLA risks early,
        balances your team's workload, eliminates cost waste, flags anomalies, deduplicates
        vendors, and continuously improves delivery — powered by a 7-agent AI platform.
      </p>
      <div class="hero-tags">
        <span class="htag">SLA Breach Prediction</span>
        <span class="htag">Resource Rebalancing</span>
        <span class="htag">AI Recovery Plans</span>
        <span class="htag">Anomaly Detection</span>
        <span class="htag">Cost Intelligence</span>
        <span class="htag">Vendor Deduplication</span>
        <span class="htag">Smart Negotiation</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── 7 hero quick-launch buttons ──────────────────────────
    hb1, hb2, hb3, hb4, hb5, hb6, hb7 = st.columns(7)
    with hb1:
        st.markdown('<div class="btn-red">', unsafe_allow_html=True)
        if st.button("🚨 SLA", key="h_sla", use_container_width=True):
            st.switch_page("pages/sla.py")
        st.markdown("</div>", unsafe_allow_html=True)
    with hb2:
        st.markdown('<div class="btn-grn">', unsafe_allow_html=True)
        if st.button("⚙️ Res", key="h_res", use_container_width=True):
            st.switch_page("pages/res.py")
        st.markdown("</div>", unsafe_allow_html=True)
    with hb3:
        st.markdown('<div class="btn-blu">', unsafe_allow_html=True)
        if st.button("📈 Imp", key="h_imp", use_container_width=True):
            st.switch_page("pages/app1.py")
        st.markdown("</div>", unsafe_allow_html=True)
    with hb4:
        st.markdown('<div class="btn-gold">', unsafe_allow_html=True)
        if st.button("🔍 Anom", key="h_ana", use_container_width=True):
            st.switch_page("pages/anomaly.py")
        st.markdown("</div>", unsafe_allow_html=True)
    with hb5:
        st.markdown('<div class="btn-cyn">', unsafe_allow_html=True)
        if st.button("🔗 Dup", key="h_dup", use_container_width=True):
            st.switch_page("pages/nego.py")
        st.markdown("</div>", unsafe_allow_html=True)
    with hb6:
        st.markdown('<div class="btn-pur">', unsafe_allow_html=True)
        if st.button("🤝 Neg", key="h_neg", use_container_width=True):
            st.switch_page("pages/dup.py")
        st.markdown("</div>", unsafe_allow_html=True)
    with hb7:
        st.markdown('<div class="btn-ora">', unsafe_allow_html=True)
        if st.button("✂️ Cost", key="h_ccb", use_container_width=True):
            st.switch_page("pages/costcut.py")
        st.markdown("</div>", unsafe_allow_html=True)


with hr:
    st.markdown("""
    <div class="au d2" style="padding-top:3.5rem;">
      <div class="mod-stack">
        <div class="mod-card red">
          <div class="mi red">🚨</div>
          <div style="flex:1">
            <div class="mn">SLA Penalty Agent</div>
            <div class="md">Predict breaches, auto-escalate and recover on time</div>
          </div>
          <span class="mbadge red">Active</span>
        </div>
        <div class="mod-card grn">
          <div class="mi grn">⚙️</div>
          <div style="flex:1">
            <div class="mn">Resource Optimisation</div>
            <div class="md">Rebalance team load and capacity intelligently</div>
          </div>
          <span class="mbadge grn">Active</span>
        </div>
        <div class="mod-card blu">
          <div class="mi blu">📈</div>
          <div style="flex:1">
            <div class="mn">Improvement Reports</div>
            <div class="md">Track trends, simulate scenarios, gain insights</div>
          </div>
          <span class="mbadge blu">Active</span>
        </div>
        <div class="mod-card gold">
          <div class="mi gold">🔍</div>
          <div style="flex:1">
            <div class="mn">Anomaly Detection</div>
            <div class="md">Surface hidden outliers and operational irregularities</div>
          </div>
          <span class="mbadge gold">Active</span>
        </div>
        <div class="mod-card cyn">
          <div class="mi cyn">🔗</div>
          <div style="flex:1">
            <div class="mn">Duplicate Vendor Agent</div>
            <div class="md">Identify and merge redundant vendor records</div>
          </div>
          <span class="mbadge cyn">Active</span>
        </div>
        <div class="mod-card pur">
          <div class="mi pur">🤝</div>
          <div style="flex:1">
            <div class="mn">Negotiator Agent</div>
            <div class="md">AI-driven contract and vendor negotiation playbooks</div>
          </div>
          <span class="mbadge pur">Active</span>
        </div>
        <div class="mod-card ora">
          <div class="mi ora">✂️</div>
          <div style="flex:1">
            <div class="mn">Cost Cutter Agent</div>
            <div class="md">Spot waste, right-size spend, maximise savings</div>
          </div>
          <span class="mbadge ora">Active</span>
        </div>
      </div>
      <div class="hstat-row">
        <div class="hstat">
          <div class="hstat-n" style="color:var(--c1)">7</div>
          <div class="hstat-l">AI Agents</div>
        </div>
        <div class="hstat">
          <div class="hstat-n" style="color:var(--c2)">96%</div>
          <div class="hstat-l">Recovery Rate</div>
        </div>
        <div class="hstat">
          <div class="hstat-n" style="color:var(--c3)">3s</div>
          <div class="hstat-l">Analysis Time</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)


# ── STATS BAND ──────────────────────────────────────────────
st.markdown("""
<div class="sg au d3">
  <div class="sb r">
    <div class="sbn" style="color:var(--c1)">78%</div>
    <div class="sbl">Avg Breach Risk Detected</div>
    <div class="sbm">Before it causes penalties</div>
  </div>
  <div class="sb g">
    <div class="sbn" style="color:var(--c2)">+42pt</div>
    <div class="sbl">SLA Health Improvement</div>
    <div class="sbm">Average after recovery plan</div>
  </div>
  <div class="sb b">
    <div class="sbn" style="color:var(--c3)">81%</div>
    <div class="sbl">AI Confidence Score</div>
    <div class="sbm">Agent prediction accuracy</div>
  </div>
  <div class="sb y">
    <div class="sbn" style="color:var(--gold)">₹5L</div>
    <div class="sbl">Avg Penalty Saved</div>
    <div class="sbm">Per intervention cycle</div>
  </div>
</div>
""", unsafe_allow_html=True)


# ── FEATURE CARDS — Row 1 (original 3) ──────────────────────
st.markdown("""
<div class="au d3" style="margin-top:2.5rem">
  <div class="sec-lbl">⬡ Platform Modules</div>
  <div class="sec-ttl">Everything in One Place</div>
  <div class="sec-sub">Seven specialised AI agents. One unified platform. Zero missed deadlines.</div>
</div>
""", unsafe_allow_html=True)

fc1, fc2, fc3 = st.columns(3, gap="medium")

with fc1:
    st.markdown("""
    <div class="fcard red au d3">
      <div class="fcg"></div>
      <div class="fcard-top">
        <div class="fci red">🚨</div>
        <span class="fclbl red">AI Agent</span>
      </div>
      <div class="fcttl">SLA Penalty Agent</div>
      <div class="fcdesc">
        A 5-stage AI pipeline that reads your project data, predicts SLA breaches,
        finds bottlenecks, reassigns tasks, and generates a complete recovery plan
        with escalation emails — automatically.
      </div>
      <div class="fcchips">
        <span class="chip">Breach Prediction</span>
        <span class="chip">Task Priority Matrix</span>
        <span class="chip">Auto Escalation</span>
        <span class="chip">OpsBot Chat</span>
        <span class="chip">XAI Reasoning</span>
      </div>
      <div class="fcfoot">
        <span class="fclink red">Launch Agent →</span>
        <div class="fcarr red">↗</div>
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="btn-red">', unsafe_allow_html=True)
    if st.button("🚨  Open SLA Agent", key="fc_sla", use_container_width=True):
        st.switch_page("pages/sla.py")
    st.markdown("</div>", unsafe_allow_html=True)

with fc2:
    st.markdown("""
    <div class="fcard grn au d4">
      <div class="fcg"></div>
      <div class="fcard-top">
        <div class="fci grn">⚙️</div>
        <span class="fclbl grn">Optimiser</span>
      </div>
      <div class="fcttl">Resource Optimisation</div>
      <div class="fcdesc">
        Detect overloaded team members, redistribute work based on skill and
        capacity, simulate overtime plans, and build smarter sprint schedules.
        AI-powered capacity heatmaps included.
      </div>
      <div class="fcchips">
        <span class="chip">Capacity Heatmap</span>
        <span class="chip">Smart Reassignment</span>
        <span class="chip">Overtime Planner</span>
        <span class="chip">Skill Matrix</span>
        <span class="chip">Load Balancer</span>
      </div>
      <div class="fcfoot">
        <span class="fclink grn">Optimise Team →</span>
        <div class="fcarr grn">↗</div>
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="btn-grn">', unsafe_allow_html=True)
    if st.button("⚙️  Open Optimiser", key="fc_res", use_container_width=True):
        st.switch_page("pages/res.py")
    st.markdown("</div>", unsafe_allow_html=True)

with fc3:
    st.markdown("""
    <div class="fcard blu au d5">
      <div class="fcg"></div>
      <div class="fcard-top">
        <div class="fci blu">📈</div>
        <span class="fclbl blu">Analytics</span>
      </div>
      <div class="fcttl">Improvement Reports</div>
      <div class="fcdesc">
        Track SLA health over time, measure how recovery plans performed,
        run what-if simulations, and receive AI-generated suggestions to
        prevent future breaches from repeating.
      </div>
      <div class="fcchips">
        <span class="chip">Health Trends</span>
        <span class="chip">KPI Dashboard</span>
        <span class="chip">What-If Simulator</span>
        <span class="chip">AI Suggestions</span>
        <span class="chip">Export Reports</span>
      </div>
      <div class="fcfoot">
        <span class="fclink blu">View Reports →</span>
        <div class="fcarr blu">↗</div>
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="btn-blu">', unsafe_allow_html=True)
    if st.button("📈  View Improvements", key="fc_imp", use_container_width=True):
        st.switch_page("pages/app1.py")
    st.markdown("</div>", unsafe_allow_html=True)


# ── FEATURE CARDS — Row 2 (4 new agents) ────────────────────
st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

fc4, fc5, fc6, fc7 = st.columns(4, gap="medium")

with fc4:
    st.markdown("""
    <div class="fcard gold au d3">
      <div class="fcg"></div>
      <div class="fcard-top">
        <div class="fci gold">🔍</div>
        <span class="fclbl gold">Detector</span>
      </div>
      <div class="fcttl">Anomaly Detection</div>
      <div class="fcdesc">
        Continuously scans operational data to surface hidden outliers,
        irregular spikes, unusual patterns, and early warning signals
        before they cascade into incidents.
      </div>
      <div class="fcchips">
        <span class="chip">Outlier Scoring</span>
        <span class="chip">Pattern Alerts</span>
        <span class="chip">Trend Deviation</span>
        <span class="chip">Root Cause</span>
      </div>
      <div class="fcfoot">
        <span class="fclink gold">Detect Now →</span>
        <div class="fcarr gold">↗</div>
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="btn-gold">', unsafe_allow_html=True)
    if st.button("🔍  Anomaly Detection", key="fc_ana", use_container_width=True):
        st.switch_page("pages/anomaly.py")
    st.markdown("</div>", unsafe_allow_html=True)

with fc5:
    st.markdown("""
    <div class="fcard cyn au d4">
      <div class="fcg"></div>
      <div class="fcard-top">
        <div class="fci cyn">🔗</div>
        <span class="fclbl cyn">Deduplicator</span>
      </div>
      <div class="fcttl">Duplicate Vendor Agent</div>
      <div class="fcdesc">
        Identifies redundant, near-duplicate or alias vendor records
        across your procurement database and recommends consolidation
        to eliminate wasted spend and compliance risk.
      </div>
      <div class="fcchips">
        <span class="chip">Fuzzy Match</span>
        <span class="chip">Entity Resolution</span>
        <span class="chip">Merge Advisor</span>
        <span class="chip">Risk Flag</span>
      </div>
      <div class="fcfoot">
        <span class="fclink cyn">Find Duplicates →</span>
        <div class="fcarr cyn">↗</div>
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="btn-cyn">', unsafe_allow_html=True)
    if st.button("🔗  Duplicate Vendors", key="fc_dup", use_container_width=True):
        st.switch_page("pages/nego.py")
    st.markdown("</div>", unsafe_allow_html=True)

with fc6:
    st.markdown("""
    <div class="fcard pur au d5">
      <div class="fcg"></div>
      <div class="fcard-top">
        <div class="fci pur">🤝</div>
        <span class="fclbl pur">Negotiator</span>
      </div>
      <div class="fcttl">Negotiator Agent</div>
      <div class="fcdesc">
        Generates AI-powered negotiation playbooks for vendor contracts,
        renewal terms, and pricing discussions — backed by market
        benchmarks and your historical deal data.
      </div>
      <div class="fcchips">
        <span class="chip">Playbook Gen</span>
        <span class="chip">Benchmark Data</span>
        <span class="chip">Counter Offers</span>
        <span class="chip">Deal Scoring</span>
      </div>
      <div class="fcfoot">
        <span class="fclink pur">Negotiate →</span>
        <div class="fcarr pur">↗</div>
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="btn-pur">', unsafe_allow_html=True)
    if st.button("🤝  Negotiator", key="fc_neg", use_container_width=True):
        st.switch_page("pages/dup.py")
    st.markdown("</div>", unsafe_allow_html=True)

with fc7:
    st.markdown("""
    <div class="fcard ora au d6">
      <div class="fcg"></div>
      <div class="fcard-top">
        <div class="fci ora">✂️</div>
        <span class="fclbl ora">Cost AI</span>
      </div>
      <div class="fcttl">Cost Cutter Agent</div>
      <div class="fcdesc">
        Analyses spend categories, surfaces waste, flags over-budget
        line items, and proposes right-sizing actions to maximise
        savings without disrupting operations.
      </div>
      <div class="fcchips">
        <span class="chip">Spend Analysis</span>
        <span class="chip">Waste Detection</span>
        <span class="chip">Right-Sizing</span>
        <span class="chip">Savings Forecast</span>
      </div>
      <div class="fcfoot">
        <span class="fclink ora">Cut Costs →</span>
        <div class="fcarr ora">↗</div>
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="btn-ora">', unsafe_allow_html=True)
    if st.button("✂️  Cost Cutter", key="fc_ccb", use_container_width=True):
        st.switch_page("pages/costcut.py")
    st.markdown("</div>", unsafe_allow_html=True)


# ── HOW IT WORKS ────────────────────────────────────────────
st.markdown("""
<div class="au d4" style="margin-top:3rem">
  <div class="sec-lbl">⬡ Under the Hood</div>
  <div class="sec-ttl">The 5-Agent AI Pipeline</div>
  <div class="sec-sub">Every request runs through five specialised agents in sequence.</div>
</div>
<div class="pipeline au d5">
  <div class="pip-step">
    <span class="pip-num">01</span>
    <span class="pip-icon">👁️</span>
    <div class="pip-name">Observe</div>
    <div class="pip-desc">Reads tasks, deadlines, team load and flags blockers</div>
    <div class="pip-agent">Input Agent</div>
  </div>
  <div class="pip-step">
    <span class="pip-num">02</span>
    <span class="pip-icon">🧠</span>
    <div class="pip-name">Think</div>
    <div class="pip-desc">Calculates breach probability and gamified health score</div>
    <div class="pip-agent">Think Agent</div>
  </div>
  <div class="pip-step">
    <span class="pip-num">03</span>
    <span class="pip-icon">⚡</span>
    <div class="pip-name">Decide</div>
    <div class="pip-desc">Ranks tasks by urgency × impact priority matrix</div>
    <div class="pip-agent">Decision Agent</div>
  </div>
  <div class="pip-step">
    <span class="pip-num">04</span>
    <span class="pip-icon">🔧</span>
    <div class="pip-name">Act</div>
    <div class="pip-desc">Reassigns tasks, builds recovery timeline, drafts escalation</div>
    <div class="pip-agent">Action Agent</div>
  </div>
  <div class="pip-step">
    <span class="pip-num">05</span>
    <span class="pip-icon">📢</span>
    <div class="pip-name">Explain</div>
    <div class="pip-desc">Every decision explained in plain English with confidence</div>
    <div class="pip-agent">Explain Agent</div>
  </div>
</div>
""", unsafe_allow_html=True)


# ── CTA ─────────────────────────────────────────────────────
st.markdown("""
<div class="cta au d5">
  <div class="cta-h">Ready to Take Control of Your Delivery?</div>
  <div class="cta-p">Pick a module and let Operix's AI agents get to work instantly.</div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

_, cc1, cc2, cc3, cc4, cc5, cc6, cc7, _ = st.columns([0.15, 1, 1, 1, 1, 1, 1, 1, 0.15])
with cc1:
    st.markdown('<div class="btn-red">', unsafe_allow_html=True)
    if st.button("🚨 SLA Agent", key="cta_sla", use_container_width=True):
        st.switch_page("pages/sla.py")
    st.markdown("</div>", unsafe_allow_html=True)
with cc2:
    st.markdown('<div class="btn-grn">', unsafe_allow_html=True)
    if st.button("⚙️ Resources", key="cta_res", use_container_width=True):
        st.switch_page("pages/res.py")
    st.markdown("</div>", unsafe_allow_html=True)
with cc3:
    st.markdown('<div class="btn-blu">', unsafe_allow_html=True)
    if st.button("📈 Reports", key="cta_imp", use_container_width=True):
        st.switch_page("pages/app1.py")
    st.markdown("</div>", unsafe_allow_html=True)
with cc4:
    st.markdown('<div class="btn-gold">', unsafe_allow_html=True)
    if st.button("🔍 Anomaly", key="cta_ana", use_container_width=True):
        st.switch_page("pages/anomaly.py")
    st.markdown("</div>", unsafe_allow_html=True)
with cc5:
    st.markdown('<div class="btn-cyn">', unsafe_allow_html=True)
    if st.button("🔗 Duplicates", key="cta_dup", use_container_width=True):
        st.switch_page("pages/nego.py")
    st.markdown("</div>", unsafe_allow_html=True)
with cc6:
    st.markdown('<div class="btn-pur">', unsafe_allow_html=True)
    if st.button("🤝 Negotiate", key="cta_neg", use_container_width=True):
        st.switch_page("pages/dup.py")
    st.markdown("</div>", unsafe_allow_html=True)
with cc7:
    st.markdown('<div class="btn-ora">', unsafe_allow_html=True)
    if st.button("✂️ Cut Costs", key="cta_ccb", use_container_width=True):
        st.switch_page("pages/costcut.py")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center;margin-top:12px;font-family:'IBM Plex Mono',monospace;
            font-size:10px;color:var(--sub);">
  Observe · Think · Decide · Act · Explain
</div>
""", unsafe_allow_html=True)


# ── FOOTER ──────────────────────────────────────────────────
st.markdown("""
<div class="foot au d6">
  <em>Operix</em> · AI Operations Intelligence Platform ·
  Groq · LLaMA 3.3 70B · 7-Agent Platform
</div>
""", unsafe_allow_html=True)