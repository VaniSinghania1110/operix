import streamlit as st
import pandas as pd

st.set_page_config(layout="wide", page_title="SpendGuard — Cloud Spend Intelligence")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, .stApp {
    background: #050c15 !important;
    color: #c8d8ee !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

/* Hide streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ── HERO PANEL ─────────────────────────────────────────── */
.hero-panel {
    padding: 3.5rem 3rem 2.5rem;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    background: linear-gradient(135deg, #050c15 0%, #0a1628 100%);
    position: relative;
    overflow: hidden;
}
.hero-panel::before {
    content: '';
    position: absolute;
    top: -60px; left: -60px;
    width: 320px; height: 320px;
    background: radial-gradient(circle, rgba(0,255,180,0.06) 0%, transparent 70%);
    pointer-events: none;
}
.hero-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.18em;
    color: #3a8fff;
    text-transform: uppercase;
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    gap: 10px;
}
.hero-eyebrow::before {
    content: '';
    display: inline-block;
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #3a8fff;
    box-shadow: 0 0 8px #3a8fff;
}
.hero-title {
    font-size: clamp(2.4rem, 4vw, 3.6rem);
    font-weight: 700;
    line-height: 1.08;
    margin: 0 0 0.5rem;
    color: #ffffff;
}
.hero-title .accent-teal   { color: #00e5aa; }
.hero-title .accent-blue   { color: #3a8fff; }
.hero-title .accent-coral  { color: #ff6b47; }
.hero-desc {
    font-size: 1.0rem;
    color: #7b95b8;
    max-width: 560px;
    line-height: 1.7;
    margin: 1rem 0 1.6rem;
}
.pill-strip {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 1.2rem;
}
.pill {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10.5px;
    letter-spacing: 0.04em;
    padding: 5px 13px;
    border: 1px solid rgba(58,143,255,0.25);
    border-radius: 3px;
    color: #6da4e8;
    background: rgba(58,143,255,0.06);
}

/* ── AGENT CARDS (right column) ─────────────────────────── */
.agent-card {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 14px 16px;
    background: #0c1828;
    border: 1px solid rgba(255,255,255,0.07);
    border-left: 3px solid;
    border-radius: 6px;
    margin-bottom: 8px;
    transition: background 0.2s;
}
.agent-card:hover { background: #0f2035; }
.agent-icon {
    width: 44px; height: 44px;
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 20px;
    flex-shrink: 0;
}
.agent-name {
    font-weight: 600;
    font-size: 14px;
    color: #ddeeff;
    margin: 0 0 3px;
}
.agent-desc {
    font-size: 12px;
    color: #5d7a99;
    margin: 0;
}
.agent-badge {
    margin-left: auto;
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    font-weight: 500;
    padding: 3px 9px;
    border-radius: 3px;
    flex-shrink: 0;
}
.badge-active   { background: rgba(0,229,170,0.12); color: #00e5aa; border: 1px solid rgba(0,229,170,0.3); }
.badge-inactive { background: rgba(255,255,255,0.04); color: #506070; border: 1px solid rgba(255,255,255,0.08); }

/* ── MAIN BODY ───────────────────────────────────────────── */
.body-wrapper {
    padding: 2.5rem 3rem;
}
.section-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10.5px;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #3a5a80;
    margin-bottom: 1.2rem;
}

/* ── METRIC CARDS ────────────────────────────────────────── */
.metric-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin: 1.5rem 0 2rem;
}
.metric-card {
    background: #0c1828;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 8px;
    padding: 1.2rem 1.4rem;
    position: relative;
    overflow: hidden;
}
.metric-card::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
}
.metric-card.c-blue::after   { background: #3a8fff; }
.metric-card.c-teal::after   { background: #00e5aa; }
.metric-card.c-coral::after  { background: #ff6b47; }
.metric-card.c-amber::after  { background: #f5a623; }
.metric-label {
    font-size: 11px;
    color: #4d6a88;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 8px;
    font-family: 'JetBrains Mono', monospace;
}
.metric-value {
    font-size: 28px;
    font-weight: 700;
    color: #ffffff;
    line-height: 1;
}
.metric-sub {
    font-size: 11px;
    color: #3a5a70;
    margin-top: 5px;
}

/* ── ANOMALY TABLE ───────────────────────────────────────── */
.anomaly-row {
    display: grid;
    grid-template-columns: 2fr 1.5fr 1.5fr 1fr 1.5fr 1.4fr;
    padding: 12px 16px;
    border-bottom: 1px solid rgba(255,255,255,0.04);
    align-items: center;
    font-size: 13.5px;
}
.anomaly-row.header {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #3a5a80;
    background: #080f1c;
    border-radius: 6px 6px 0 0;
    padding: 10px 16px;
}
.anomaly-row:not(.header):hover { background: rgba(58,143,255,0.04); }
.service-name { font-weight: 600; color: #c8d8ee; }
.spike-pill {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 3px 10px;
    border-radius: 4px;
    font-size: 12px;
    font-weight: 600;
    font-family: 'JetBrains Mono', monospace;
}
.spike-high   { background: rgba(255,107,71,0.12); color: #ff6b47; border: 1px solid rgba(255,107,71,0.25); }
.spike-medium { background: rgba(245,166,35,0.12); color: #f5a623; border: 1px solid rgba(245,166,35,0.25); }
.spike-low    { background: rgba(58,143,255,0.12); color: #3a8fff; border: 1px solid rgba(58,143,255,0.25); }
.action-tag {
    font-size: 11px;
    font-family: 'JetBrains Mono', monospace;
    color: #3a5a80;
    background: rgba(58,143,255,0.06);
    border: 1px solid rgba(58,143,255,0.12);
    border-radius: 3px;
    padding: 3px 8px;
}

/* ── UPLOAD ZONE ─────────────────────────────────────────── */
.stFileUploader > div {
    background: #0c1828 !important;
    border: 1px dashed rgba(58,143,255,0.3) !important;
    border-radius: 8px !important;
}
.stFileUploader label { color: #5d7a99 !important; }

/* ── BUTTON ──────────────────────────────────────────────── */
.stButton > button {
    background: linear-gradient(135deg, #1a4a80 0%, #0d2a50 100%) !important;
    color: #7bbfff !important;
    border: 1px solid rgba(58,143,255,0.4) !important;
    border-radius: 5px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 12px !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    padding: 0.6rem 2rem !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #2255a0 0%, #12366a 100%) !important;
    border-color: rgba(58,143,255,0.7) !important;
    color: #aad4ff !important;
}

/* ── DATAFRAME ───────────────────────────────────────────── */
.stDataFrame { border-radius: 8px; overflow: hidden; }
.stDataFrame * { color: #c8d8ee !important; background: #0c1828 !important; font-family: 'JetBrains Mono', monospace !important; font-size: 12px !important; }

/* ── DIVIDER ─────────────────────────────────────────────── */
hr { border-color: rgba(255,255,255,0.05) !important; }

/* ── SUCCESS / ERROR ─────────────────────────────────────── */
.stSuccess { background: rgba(0,229,170,0.08) !important; border: 1px solid rgba(0,229,170,0.2) !important; color: #00e5aa !important; border-radius: 6px !important; }
.stError   { background: rgba(255,107,71,0.08) !important; border: 1px solid rgba(255,107,71,0.2) !important; color: #ff6b47 !important; border-radius: 6px !important; }
</style>
""", unsafe_allow_html=True)

# ── HERO + AGENT PANEL ────────────────────────────────────────────────────────
col_hero, col_agents = st.columns([1.1, 1], gap="large")

with col_hero:
    st.markdown("""
    <div class="hero-panel">
        <div class="hero-eyebrow">AI-Powered Cloud Operations</div>
        <div class="hero-title">
            One Platform.<br>
            <span class="accent-teal">Detect.</span>
            <span class="accent-blue"> Analyse.</span><br>
            <span class="accent-coral">Cut Waste.</span>
        </div>
        <div class="hero-desc">
            SpendGuard is an intelligent cloud spend operations agent that surfaces
            cost anomalies early, flags wasted spend, and delivers prioritised
            recommendations — powered by a 7-agent AI platform.
        </div>
        <div class="pill-strip">
            <span class="pill">Anomaly Detection</span>
            <span class="pill">Cost Intelligence</span>
            <span class="pill">Spike Analysis</span>
            <span class="pill">Waste Recovery</span>
            <span class="pill">Resource Rightsizing</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_agents:
    st.markdown("<br>", unsafe_allow_html=True)
    agents = [
        ("🔔", "#ff6b47", "Anomaly Detection Agent",    "Predict spikes, auto-escalate and recover on time", True),
        ("⚙️", "#3a8fff", "Resource Optimisation",      "Rebalance team load and capacity intelligently",    True),
        ("📊", "#3a8fff", "Improvement Reports",         "Track trends, simulate scenarios, gain insights",   True),
        ("🔍", "#f5a623", "Cost Spike Detector",         "Surface hidden outliers and spend irregularities",  True),
        ("🔗", "#3a8fff", "Duplicate Vendor Agent",      "Identify and merge redundant vendor records",       False),
        ("🤝", "#a78bfa", "Negotiator Agent",            "AI-driven contract and vendor negotiation",         False),
        ("✂️", "#f5a623", "Cost Cutter Agent",           "Spot waste, right-size spend, maximise savings",    True),
    ]
    for icon, color, name, desc, active in agents:
        badge_cls = "badge-active" if active else "badge-inactive"
        badge_txt = "ACTIVE" if active else "IDLE"
        st.markdown(f"""
        <div class="agent-card" style="border-left-color:{color};">
            <div class="agent-icon" style="background:rgba(255,255,255,0.05);">{icon}</div>
            <div>
                <div class="agent-name">{name}</div>
                <div class="agent-desc">{desc}</div>
            </div>
            <span class="agent-badge {badge_cls}">{badge_txt}</span>
        </div>
        """, unsafe_allow_html=True)

# ── BODY ──────────────────────────────────────────────────────────────────────
st.markdown('<div class="body-wrapper">', unsafe_allow_html=True)

st.markdown('<div class="section-label">// Upload Spend Data</div>', unsafe_allow_html=True)

up_col, schema_col = st.columns([1.4, 1], gap="large")

with up_col:
    uploaded = st.file_uploader("Upload spend CSV", type=["csv"], label_visibility="collapsed")
    st.markdown("<br>", unsafe_allow_html=True)

with schema_col:
    st.markdown("""
    <div style="background:#0c1828; border:1px solid rgba(255,255,255,0.07); border-radius:8px; padding:1.2rem 1.5rem;">
        <div class="section-label">Expected Schema</div>
        <code style="font-family:'JetBrains Mono',monospace; font-size:12px; color:#3a8fff; display:block; line-height:2;">
            service, previous_cost, current_cost
        </code>
        <div style="font-size:12px; color:#3a5a80; margin-top:8px;">Costs in any currency. Spike threshold: &gt;20% increase.</div>
    </div>
    """, unsafe_allow_html=True)

sample = pd.DataFrame({
    "service": ["EC2", "Azure AKS", "BigQuery"],
    "previous_cost": [280000, 210000, 88000],
    "current_cost": [420000, 310000, 95000]
})

st.markdown('<div class="section-label" style="margin-top:1.5rem;">// Sample Format</div>', unsafe_allow_html=True)
st.dataframe(sample, use_container_width=True)

if uploaded:
    df = pd.read_csv(uploaded)
    required_cols = {"service", "previous_cost", "current_cost"}
    if not required_cols.issubset(df.columns):
        st.error("⚠  CSV must contain: service, previous_cost, current_cost")
    else:
        st.markdown("""
        <div style="background:rgba(0,229,170,0.06); border:1px solid rgba(0,229,170,0.18);
             border-radius:6px; padding:10px 16px; color:#00e5aa; font-size:13px; margin:1rem 0;">
            ✓ &nbsp; Data loaded — {n} services ready for analysis
        </div>
        """.format(n=len(df)), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("▶  RUN ANOMALY AGENT"):
            df["spike_pct"] = ((df["current_cost"] - df["previous_cost"]) / df["previous_cost"]) * 100
            anomalies = df[df["spike_pct"] > 20].copy()
            anomalies["wasted_spend"] = anomalies["current_cost"] - anomalies["previous_cost"]

            total_services = len(df)
            anomaly_count  = len(anomalies)
            avg_spike      = round(df["spike_pct"].mean(), 1)
            total_wasted   = int(anomalies["wasted_spend"].sum()) if anomaly_count > 0 else 0

            # ── METRIC CARDS
            st.markdown(f"""
            <div class="metric-row">
                <div class="metric-card c-blue">
                    <div class="metric-label">Total Services</div>
                    <div class="metric-value">{total_services}</div>
                    <div class="metric-sub">In scope</div>
                </div>
                <div class="metric-card c-coral">
                    <div class="metric-label">Anomalies</div>
                    <div class="metric-value">{anomaly_count}</div>
                    <div class="metric-sub">&gt;20% spike threshold</div>
                </div>
                <div class="metric-card c-amber">
                    <div class="metric-label">Avg Spike</div>
                    <div class="metric-value">{avg_spike}%</div>
                    <div class="metric-sub">Across all services</div>
                </div>
                <div class="metric-card c-teal">
                    <div class="metric-label">Wasted Spend</div>
                    <div class="metric-value">₹{total_wasted:,}</div>
                    <div class="metric-sub">Recoverable</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # ── ANOMALY TABLE
            st.markdown('<div class="section-label" style="margin-top:2rem;">// Detected Anomalies</div>', unsafe_allow_html=True)

            if anomaly_count == 0:
                st.markdown("""
                <div style="text-align:center; padding:3rem; color:#2a5a40; font-size:14px;">
                    ✓ &nbsp; No anomalies detected above threshold
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="background:#080f1c; border:1px solid rgba(255,255,255,0.06); border-radius:8px; overflow:hidden; margin-bottom:2rem;">
                <div class="anomaly-row header">
                    <span>Service</span><span>Previous</span><span>Current</span>
                    <span>Spike</span><span>Wasted</span><span>Action</span>
                </div>
                """, unsafe_allow_html=True)

                for _, row in anomalies.iterrows():
                    spike = row["spike_pct"]
                    spike_cls = "spike-high" if spike > 40 else ("spike-medium" if spike > 25 else "spike-low")
                    st.markdown(f"""
                    <div class="anomaly-row">
                        <span class="service-name">{row['service']}</span>
                        <span style="color:#5d7a99; font-family:'JetBrains Mono',monospace; font-size:13px;">₹{int(row['previous_cost']):,}</span>
                        <span style="color:#c8d8ee; font-family:'JetBrains Mono',monospace; font-size:13px; font-weight:600;">₹{int(row['current_cost']):,}</span>
                        <span><span class="spike-pill {spike_cls}">↑ {spike:.1f}%</span></span>
                        <span style="color:#ff6b47; font-family:'JetBrains Mono',monospace; font-size:13px; font-weight:600;">₹{int(row['wasted_spend']):,}</span>
                        <span><span class="action-tag">investigate</span></span>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)

                # ── RECOMMENDED ACTIONS
                st.markdown('<div class="section-label">// Recommended Actions</div>', unsafe_allow_html=True)
                for _, row in anomalies.iterrows():
                    spike = row["spike_pct"]
                    priority = "HIGH" if spike > 40 else ("MEDIUM" if spike > 25 else "LOW")
                    pr_color = "#ff6b47" if priority == "HIGH" else ("#f5a623" if priority == "MEDIUM" else "#3a8fff")
                    st.markdown(f"""
                    <div style="background:#0c1828; border:1px solid rgba(255,255,255,0.07); border-left:3px solid {pr_color};
                         border-radius:6px; padding:1rem 1.4rem; margin-bottom:10px;">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                            <span style="font-weight:600; color:#ddeeff; font-size:14px;">{row['service']}</span>
                            <span style="font-family:'JetBrains Mono',monospace; font-size:10px; color:{pr_color};
                                  background:rgba(255,255,255,0.05); border:1px solid {pr_color}33;
                                  padding:2px 9px; border-radius:3px;">{priority} PRIORITY</span>
                        </div>
                        <div style="font-size:12.5px; color:#5d7a99; line-height:1.8;">
                            Spike of <span style="color:{pr_color}; font-weight:600;">{spike:.1f}%</span> detected &nbsp;·&nbsp;
                            Potential waste: <span style="color:#ff6b47; font-weight:600;">₹{int(row['wasted_spend']):,}</span>
                            &nbsp;·&nbsp; Investigate scaling events, idle resources, and misconfigured autoscaling policies.
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
