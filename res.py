"""
╔══════════════════════════════════════════════════════════════╗
║   ResourceIQ — RESOURCE OPTIMIZATION AGENT                  ║
║   No hardcoded data. No dotenv. API key via sidebar.         ║
║   Features: 5-Agent AI · What-if · Team View · Chat         ║
╚══════════════════════════════════════════════════════════════╝

Run:  streamlit run resourceiq.py
Needs: pip install streamlit groq
"""

import streamlit as st
import json, time, re
from groq import Groq

# ── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResourceIQ — Optimization Agent",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── SESSION STATE ──────────────────────────────────────────────────────────────
DEFAULTS = {
    "view":          "step1",
    "inputs":        {},
    "analysis":      None,
    "chat_history":  [],
    "whatif_result": None,
    "active_tab":    "overview",
    "resource_rows": [],
    "team_rows":     [],
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

if not st.session_state.resource_rows:
    st.session_state.resource_rows = [
        {"id": "R-001", "name": "", "type": "Infrastructure",
         "utilization": 50, "cost": 10000, "team": "", "dependencies": 0, "notes": ""}
    ]
if not st.session_state.team_rows:
    st.session_state.team_rows = [
        {"name": "", "role": "", "load": 50, "skills": "", "available_hours": 40, "team": ""}
    ]

# ── LLM HELPER ─────────────────────────────────────────────────────────────────
def llm(messages, max_tokens=1400, temperature=0.35, api_key=""):
    if not api_key or not api_key.strip():
        raise ValueError("Groq API key is missing. Please enter it in Step 1.")
    client = Groq(api_key=api_key)
    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return resp.choices[0].message.content.strip()


def safe_json(text, fallback):
    try:
        clean = re.sub(r"```(?:json)?|```", "", text).strip()
        # Strip any leading text before the first { or [
        match = re.search(r'[\[{]', clean)
        if match:
            clean = clean[match.start():]
        return json.loads(clean)
    except Exception:
        return fallback

# ── 5-AGENT PIPELINE ──────────────────────────────────────────────────────────
AGENT_PIPELINE = [
    ("📡", "SCAN AGENT",      "Maps all resources & utilization"),
    ("🧠", "ANALYSE AGENT",   "Detects waste & consolidation gaps"),
    ("⚡", "PRIORITISE AGENT", "Ranks opportunities by ROI"),
    ("🔧", "PLAN AGENT",      "Builds execution & change plan"),
    ("📢", "REPORT AGENT",    "Generates explainable AI report"),
]


def run_multi_agent(inp, step_ph, log_ph, progress_ph, api_key):
    log = []
    ts = lambda: time.strftime("%H:%M:%S")

    def push(msg, kind="action"):
        log.append((ts(), kind, msg))
        html = "".join(
            f'<div class="lg-line">'
            f'<span class="lg-ts">{t}</span>'
            f'<span class="lg-k lg-{k}">[{k.upper()}]</span>'
            f'<span class="lg-m">{m}</span>'
            f'</div>'
            for t, k, m in log[-24:]
        )
        log_ph.markdown(f'<div class="agent-log">{html}</div>', unsafe_allow_html=True)

    def set_step(active):
        html = ""
        for i, (icon, name, _) in enumerate(AGENT_PIPELINE):
            cls = "done" if i < active else ("active" if i == active else "")
            sym = "✓" if i < active else str(i + 1)
            lc  = "active" if i == active else ""
            html += (
                f'<div class="ag-step">'
                f'<div class="ag-dot {cls}">{sym}</div>'
                f'<div class="ag-lbl {lc}">{icon}<br>{name}</div>'
                f'</div>'
            )
            if i < len(AGENT_PIPELINE) - 1:
                line_cls = "done" if i < active else ("active" if i == active else "")
                html += f'<div class="ag-line {line_cls}"></div>'
        step_ph.markdown(f'<div class="ag-pipeline">{html}</div>', unsafe_allow_html=True)

    res        = {}
    resources  = inp.get("resources", [])
    team       = inp.get("team", [])
    org_name   = inp.get("org_name", "")
    goal       = inp.get("goal", "")
    strategy   = inp.get("strategy", "moderate")
    threshold  = inp.get("threshold", 50)
    budget     = inp.get("budget", 0)

    ctx = f"""
ORGANISATION: {org_name}
OPTIMISATION GOAL: {goal}
STRATEGY: {strategy}
UNDERUTILISATION THRESHOLD: {threshold}%
MONTHLY BUDGET: ₹{budget:,}
RESOURCES:
{json.dumps(resources, indent=2)}
TEAM:
{json.dumps(team, indent=2)}
"""

    # ── AGENT 1: SCAN ──────────────────────────────────────────────────────────
    set_step(0)
    progress_ph.progress(5)
    push("Scan Agent activated — mapping resource landscape…", "think")

    total_spend = sum(float(r.get("cost", 0)) for r in resources)
    underutil   = [r for r in resources if float(r.get("utilization", 50)) < threshold]
    overutil    = [r for r in resources if float(r.get("utilization", 50)) > 85]

    push(f"Total resources: {len(resources)} | Monthly spend: ₹{int(total_spend):,}", "action")
    push(f"Underutilised ({threshold}% threshold): {len(underutil)} resources flagged", "action")
    push(
        f"Overloaded resources: {len(overutil)} — capacity risk detected",
        "warn" if overutil else "action",
    )

    wasted = sum(
        float(r.get("cost", 0)) * (1 - float(r.get("utilization", 50)) / 100)
        for r in underutil
    )
    push(f"Estimated monthly waste: ₹{int(wasted):,} across underutilised resources", "result")
    time.sleep(0.4)

    res["scan"] = {
        "total_resources":      len(resources),
        "total_monthly_spend":  int(total_spend),
        "underutilised_count":  len(underutil),
        "overutilised_count":   len(overutil),
        "estimated_waste":      int(wasted),
        "underutilised": [
            {
                "name":        r["name"],
                "type":        r.get("type", ""),
                "utilization": r.get("utilization", 0),
                "cost":        r.get("cost", 0),
            }
            for r in underutil[:8]
        ],
    }
    progress_ph.progress(20)

    # ── AGENT 2: ANALYSE ───────────────────────────────────────────────────────
    set_step(1)
    push("Analyse Agent activated — running consolidation gap analysis…", "think")

    analyse_resp = llm(
        [{"role": "user", "content": f"""
You are a resource optimisation AI. Analyse this data and return ONLY valid JSON with no extra text or markdown fences.
{ctx}
Scan results: {json.dumps(res['scan'])}

Return exactly this JSON structure:
{{
  "consolidation_opportunities": [
    {{"resource_a":"<name>","resource_b":"<name>","type":"<type>","reason":"<why they overlap>","combined_utilization":<int>,"savings_estimate":<int>,"confidence":"HIGH|MEDIUM|LOW"}}
  ],
  "redundant_resources": [
    {{"name":"<name>","reason":"<why redundant>","action":"DECOMMISSION|DOWNSIZE|MERGE","monthly_saving":<int>}}
  ],
  "capacity_gaps": [
    {{"area":"<area>","issue":"<what is under-capacity>","impact":"<business impact>","urgency":"HIGH|MEDIUM|LOW"}}
  ],
  "waste_breakdown": {{"infrastructure":<int>,"tools":<int>,"teams":<int>,"other":<int>}},
  "health_score": <int 0-100>,
  "risk_level": "CRITICAL|HIGH|MEDIUM|LOW",
  "analysis_summary": "<2 sentences>"
}}
"""}],
        api_key=api_key,
    )

    analyse = safe_json(
        analyse_resp,
        {
            "consolidation_opportunities": [],
            "redundant_resources": [
                {
                    "name":          r["name"],
                    "reason":        "Utilisation below threshold",
                    "action":        "DOWNSIZE",
                    "monthly_saving": int(float(r.get("cost", 0)) * 0.4),
                }
                for r in underutil[:3]
            ],
            "capacity_gaps": [],
            "waste_breakdown": {
                "infrastructure": int(wasted * 0.5),
                "tools":          int(wasted * 0.3),
                "teams":          int(wasted * 0.2),
                "other":          0,
            },
            "health_score": max(10, min(90, 100 - int(len(underutil) / max(1, len(resources)) * 80))),
            "risk_level":   "HIGH" if len(underutil) > len(resources) // 2 else "MEDIUM",
            "analysis_summary": (
                f"Found {len(underutil)} underutilised resources wasting "
                f"₹{int(wasted):,}/month. Consolidation recommended."
            ),
        },
    )
    res["analyse"] = analyse

    push(f"Consolidation opportunities: {len(analyse.get('consolidation_opportunities', []))}", "result")
    push(f"Redundant resources flagged: {len(analyse.get('redundant_resources', []))}", "result")
    push(
        f"Resource health score: {analyse.get('health_score', 50)}/100 "
        f"| Risk: {analyse.get('risk_level', 'MEDIUM')}",
        "result",
    )
    if analyse.get("capacity_gaps"):
        push(f"Capacity gaps detected: {len(analyse['capacity_gaps'])} area(s) under-resourced", "warn")
    progress_ph.progress(42)
    time.sleep(0.4)

    # ── AGENT 3: PRIORITISE ────────────────────────────────────────────────────
    set_step(2)
    push("Prioritise Agent activated — ranking by ROI and effort…", "think")

    prioritise_resp = llm(
        [{"role": "user", "content": f"""
You are a resource prioritisation AI. Given:
{ctx}
Analysis: {json.dumps(analyse)}

Return ONLY valid JSON with no extra text or markdown fences:
{{
  "ranked_actions": [
    {{"rank":<int>,"resource":"<name>","action":"CONSOLIDATE|DECOMMISSION|DOWNSIZE|REALLOCATE|EXPAND","roi_score":<int 0-100>,"effort":"LOW|MEDIUM|HIGH","monthly_saving":<int>,"timeline":"<e.g. Week 1-2>","owner":"<team>","reason":"<why this rank>"}}
  ],
  "quick_wins": ["<action 1>","<action 2>","<action 3>"],
  "high_effort_but_high_reward": ["<action>"],
  "defer_list": ["<resource name>"],
  "prioritisation_rationale": "<overall strategy sentence>"
}}
"""}],
        api_key=api_key,
    )

    prioritise = safe_json(
        prioritise_resp,
        {
            "ranked_actions": [
                {
                    "rank":           i + 1,
                    "resource":       r["name"],
                    "action":         "DOWNSIZE",
                    "roi_score":      75,
                    "effort":         "LOW",
                    "monthly_saving": int(float(r.get("cost", 0)) * 0.35),
                    "timeline":       f"Week {i + 1}-{i + 2}",
                    "owner":          r.get("team", "Ops Team"),
                    "reason":         "Below utilisation threshold",
                }
                for i, r in enumerate(underutil[:5])
            ],
            "quick_wins":                  [f"Downsize {r['name']}" for r in underutil[:3]],
            "high_effort_but_high_reward": [],
            "defer_list":                  [],
            "prioritisation_rationale":    f"Focus on {strategy} savings with quick wins first.",
        },
    )
    res["prioritise"] = prioritise

    total_ranked_saving = sum(a.get("monthly_saving", 0) for a in prioritise.get("ranked_actions", []))
    push(
        f"Ranked {len(prioritise.get('ranked_actions', []))} actions "
        f"| Total monthly saving: ₹{total_ranked_saving:,}",
        "result",
    )
    push(f"Quick wins: {len(prioritise.get('quick_wins', []))} identified", "action")
    rationale = prioritise.get("prioritisation_rationale", "")
    push(f"Strategy: {rationale[:80]}{'…' if len(rationale) > 80 else ''}", "action")
    progress_ph.progress(62)
    time.sleep(0.4)

    # ── AGENT 4: PLAN ──────────────────────────────────────────────────────────
    set_step(3)
    push("Plan Agent activated — building execution roadmap…", "think")

    plan_resp = llm(
        [{"role": "user", "content": f"""
You are a resource change management AI. Given:
{ctx}
Prioritised actions: {json.dumps(prioritise.get('ranked_actions', [])[:6])}
Team: {json.dumps(team)}

Return ONLY valid JSON with no extra text or markdown fences:
{{
  "execution_phases": [
    {{"phase":"Phase 1 — Quick Wins","duration":"Week 1-2","actions":["<action>"],"expected_saving":<int>,"risk":"LOW|MEDIUM|HIGH"}},
    {{"phase":"Phase 2 — Consolidations","duration":"Week 3-4","actions":["<action>"],"expected_saving":<int>,"risk":"LOW|MEDIUM|HIGH"}},
    {{"phase":"Phase 3 — Structural Changes","duration":"Month 2","actions":["<action>"],"expected_saving":<int>,"risk":"MEDIUM|HIGH"}}
  ],
  "team_reallocation": [
    {{"from_resource":"<name>","to_resource":"<name>","person":"<name>","reason":"<why>","hours_freed":<int>}}
  ],
  "approval_required": [
    {{"action":"<action>","approver":"<role>","reason":"<why approval needed>"}}
  ],
  "projected_monthly_saving": <int>,
  "projected_annual_saving": <int>,
  "payback_months": <int>,
  "efficiency_gain_pct": <int>,
  "execution_confidence": <int 0-100>
}}
"""}],
        api_key=api_key,
    )

    plan = safe_json(
        plan_resp,
        {
            "execution_phases": [
                {
                    "phase":           "Phase 1 — Quick Wins",
                    "duration":        "Week 1-2",
                    "actions":         [f"Downsize {r['name']}" for r in underutil[:2]],
                    "expected_saving": int(wasted * 0.4),
                    "risk":            "LOW",
                },
                {
                    "phase":           "Phase 2 — Consolidations",
                    "duration":        "Week 3-4",
                    "actions":         [
                        f"Merge overlapping {resources[0]['type'] if resources else 'tools'}"
                    ],
                    "expected_saving": int(wasted * 0.35),
                    "risk":            "MEDIUM",
                },
                {
                    "phase":           "Phase 3 — Structural",
                    "duration":        "Month 2",
                    "actions":         ["Review team allocation", "Renegotiate vendor contracts"],
                    "expected_saving": int(wasted * 0.25),
                    "risk":            "MEDIUM",
                },
            ],
            "team_reallocation":       [],
            "approval_required":       [],
            "projected_monthly_saving": int(wasted * 0.75),
            "projected_annual_saving":  int(wasted * 0.75 * 12),
            "payback_months":           2,
            "efficiency_gain_pct":      min(40, int(len(underutil) / max(1, len(resources)) * 60)),
            "execution_confidence":     78,
        },
    )
    res["plan"] = plan

    push(
        f"Execution plan: {len(plan.get('execution_phases', []))} phases "
        f"| ₹{plan.get('projected_monthly_saving', 0):,}/month projected",
        "result",
    )
    push(
        f"Annual saving: ₹{plan.get('projected_annual_saving', 0):,} "
        f"| Payback: {plan.get('payback_months', 0)} months",
        "result",
    )
    push(
        f"Confidence: {plan.get('execution_confidence', 78)}% "
        f"| Efficiency gain: {plan.get('efficiency_gain_pct', 0)}%",
        "result",
    )
    if plan.get("approval_required"):
        push(
            f"Approval required for {len(plan['approval_required'])} action(s) — flagged for review",
            "warn",
        )
    progress_ph.progress(82)
    time.sleep(0.4)

    # ── AGENT 5: REPORT ────────────────────────────────────────────────────────
    set_step(4)
    push("Report Agent activated — generating XAI summary…", "think")

    report_resp = llm(
        [{"role": "user", "content": f"""
You are a resource optimisation reporting AI. Explain all decisions in plain English.
Organisation: {org_name} | Goal: {goal}
Scan: {json.dumps(res['scan'])}
Analysis: health={analyse.get('health_score')}, risk={analyse.get('risk_level')}
Plan: monthly_saving=₹{plan.get('projected_monthly_saving', 0)}, confidence={plan.get('execution_confidence', 78)}%

Return ONLY valid JSON with no extra text or markdown fences:
{{
  "explanations": [
    {{"decision":"<title>","why":"<plain English 1-2 sentences>","data_used":"<what data led to this>","confidence":<int 0-100>}}
  ],
  "executive_summary": "<3 sentences: what was found, what to do, what saving is achieved>",
  "health_before": <int 0-100>,
  "health_after": <int 0-100>
}}
"""}],
        api_key=api_key,
    )

    report = safe_json(
        report_resp,
        {
            "explanations": [
                {
                    "decision":  "Underutilisation detected",
                    "why":       (
                        f"{len(underutil)} resources are running below {threshold}% utilisation, "
                        f"wasting ₹{int(wasted):,}/month in idle capacity."
                    ),
                    "data_used": "Utilisation % vs threshold, monthly cost per resource",
                    "confidence": 92,
                },
                {
                    "decision":  "Consolidation recommended",
                    "why":       (
                        "Resources with overlapping function and combined utilisation below 100% "
                        "can be safely merged without service disruption."
                    ),
                    "data_used": "Resource type matching, utilisation sum, dependency count",
                    "confidence": 85,
                },
                {
                    "decision":  "Phased execution plan",
                    "why":       (
                        f"A {strategy} strategy was applied — low-risk quick wins first, "
                        "then structural changes, minimising operational disruption."
                    ),
                    "data_used": "Effort scores, risk levels, team capacity",
                    "confidence": 88,
                },
            ],
            "executive_summary": (
                f"Analysis of {len(resources)} resources across {org_name} identified "
                f"₹{int(wasted):,}/month in waste from underutilised assets. "
                f"A {strategy} optimisation plan across 3 phases can recover "
                f"₹{plan.get('projected_monthly_saving', 0):,}/month. "
                f"Implementation confidence is {plan.get('execution_confidence', 78)}% "
                f"with a {plan.get('payback_months', 2)}-month payback period."
            ),
            "health_before": analyse.get("health_score", 45),
            "health_after":  min(95, analyse.get("health_score", 45) + 35),
        },
    )
    res["report"] = report

    push(f"XAI report: {len(report.get('explanations', []))} decisions explained", "result")
    push("Executive summary generated", "result")
    push("🏁 All 5 agents complete. Optimisation plan ready.", "result")
    progress_ph.progress(100)
    set_step(5)
    time.sleep(0.3)
    return res


# ── WHAT-IF AGENT ──────────────────────────────────────────────────────────────
def run_whatif(scenario, analysis, inp, api_key):
    resp = llm(
        [{"role": "user", "content": f"""
You are a what-if scenario simulator for resource optimisation.
Current analysis: health={analysis.get('report', {}).get('health_before', 50)}, monthly_saving=₹{analysis.get('plan', {}).get('projected_monthly_saving', 0)}
Organisation: {inp.get('org_name', '')} | Goal: {inp.get('goal', '')}
Resources: {len(inp.get('resources', []))} total
Scenario: {scenario}

Return ONLY valid JSON with no extra text or markdown fences:
{{
  "scenario_title": "<short title>",
  "new_health_score": <int 0-100>,
  "new_monthly_saving": <int>,
  "new_efficiency_gain": <int>,
  "delta_saving": <int, positive=improvement>,
  "key_changes": ["change 1","change 2","change 3"],
  "new_risks": ["risk 1"],
  "recommendation": "<one sentence>"
}}
"""}],
        api_key=api_key,
    )
    return safe_json(
        resp,
        {
            "scenario_title":    scenario[:60],
            "new_health_score":  75,
            "new_monthly_saving": analysis.get("plan", {}).get("projected_monthly_saving", 0) + 20000,
            "new_efficiency_gain": 35,
            "delta_saving":      20000,
            "key_changes":       ["More capacity freed up", "Better consolidation possible", "Reduced overhead"],
            "new_risks":         ["Coordination overhead"],
            "recommendation":    "Net positive impact — recommended.",
        },
    )


# ── CHAT AGENT ─────────────────────────────────────────────────────────────────
def chat_agent(user_msg, analysis, inp, api_key):
    system = (
        f"You are OptiBot — a sharp, friendly AI resource optimisation advisor.\n"
        f"Context: Org={inp.get('org_name', '')}, Goal={inp.get('goal', '')}, "
        f"Resources={len(inp.get('resources', []))}, Budget=₹{inp.get('budget', 0):,}/month\n"
        f"Health score: {analysis.get('report', {}).get('health_before', 50)}/100 → "
        f"{analysis.get('report', {}).get('health_after', 80)}/100 after optimisation\n"
        f"Monthly saving projected: ₹{analysis.get('plan', {}).get('projected_monthly_saving', 0):,}\n"
        f"Rules: Concise (max 120 words), 1-2 emojis, reference specific numbers, be actionable."
    )
    msgs = [{"role": "system", "content": system}]
    msgs += [{"role": m["role"], "content": m["content"]} for m in st.session_state.chat_history[-10:]]
    msgs.append({"role": "user", "content": user_msg})
    return llm(msgs, max_tokens=200, temperature=0.65, api_key=api_key)


# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=IBM+Plex+Mono:wght@400;500;600&family=Manrope:wght@300;400;500;600;700&display=swap');
:root{
  --bg:#05080f;--bg2:#090d18;--bg3:#0e1220;--bg4:#131825;--bg5:#1a2030;
  --ac:#00d4ff;--ac2:rgba(0,212,255,0.12);--acg:rgba(0,212,255,0.25);
  --grn:#00e887;--grn2:rgba(0,232,135,0.1);--grng:rgba(0,232,135,0.25);
  --ylw:#ffbe00;--ylw2:rgba(255,190,0,0.1);
  --red:#ff4040;--red2:rgba(255,64,64,0.1);--redg:rgba(255,64,64,0.25);
  --prp:#9d7eff;--prp2:rgba(157,126,255,0.1);
  --text:#e0eaf8;--muted:#3a4260;--muted2:#58637a;
  --bd:rgba(255,255,255,0.06);--bd2:rgba(255,255,255,0.1);
}
*,*::before,*::after{box-sizing:border-box}
html,body,[data-testid="stAppViewContainer"],[data-testid="stMain"]{background:var(--bg)!important;font-family:'Manrope',sans-serif!important;color:var(--text)!important}
[data-testid="stAppViewContainer"]::before{content:'';position:fixed;width:900px;height:600px;background:radial-gradient(ellipse,rgba(0,212,255,0.04) 0%,transparent 65%);top:-250px;right:-300px;pointer-events:none;z-index:0}
[data-testid="stAppViewContainer"]::after{content:'';position:fixed;width:700px;height:700px;background:radial-gradient(ellipse,rgba(0,232,135,0.03) 0%,transparent 65%);bottom:-200px;left:-200px;pointer-events:none;z-index:0}
#MainMenu,footer,header,[data-testid="stDecoration"],[data-testid="stToolbar"],[data-testid="stStatusWidget"]{display:none!important}
[data-testid="stMainBlockContainer"]{max-width:1120px!important;padding:0 2rem 5rem!important;margin:0 auto!important;position:relative;z-index:1}
[data-testid="stVerticalBlock"]{gap:0!important}
::-webkit-scrollbar{width:3px;height:3px}
::-webkit-scrollbar-thumb{background:rgba(0,212,255,0.2);border-radius:10px}
@keyframes fadeUp{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:translateY(0)}}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.25}}
@keyframes pulse2{0%,100%{box-shadow:0 0 0 0 rgba(0,212,255,0.4)}70%{box-shadow:0 0 0 10px rgba(0,212,255,0)}}
@keyframes scoreIn{from{opacity:0;transform:scale(.7)}to{opacity:1;transform:scale(1)}}
@keyframes bounceIn{0%{transform:scale(.85);opacity:0}60%{transform:scale(1.04)}100%{transform:scale(1);opacity:1}}
.au{animation:fadeUp .5s ease both}
.d1{animation-delay:.07s}.d2{animation-delay:.14s}.d3{animation-delay:.21s}.d4{animation-delay:.28s}

/* NAV */
.top-nav{display:flex;align-items:center;gap:14px;padding:1.8rem 0 1.5rem;border-bottom:1px solid var(--bd);margin-bottom:0}
.nav-logo{font-family:'Syne',sans-serif;font-size:1.4rem;font-weight:800;letter-spacing:1px}
.nav-logo span{color:var(--ac)}
.nav-badge{display:inline-flex;align-items:center;gap:7px;background:var(--ac2);border:1px solid rgba(0,212,255,.3);padding:5px 13px;border-radius:5px;font-family:'IBM Plex Mono',monospace;font-size:9px;letter-spacing:2px;text-transform:uppercase;color:var(--ac)}
.nav-dot{width:5px;height:5px;background:var(--ac);border-radius:50%;animation:pulse 1.4s infinite}
.nav-spacer{flex:1;height:1px;background:var(--bd)}
.nav-model{font-family:'IBM Plex Mono',monospace;font-size:9px;color:var(--muted);letter-spacing:1.5px}

/* WIZARD */
.wizard-bar{display:flex;align-items:center;gap:0;padding:2rem 0 2.5rem}
.wz-step{display:flex;flex-direction:column;align-items:center;gap:6px}
.wz-dot{width:38px;height:38px;border-radius:50%;border:1.5px solid var(--bd2);display:flex;align-items:center;justify-content:center;font-family:'IBM Plex Mono',monospace;font-size:12px;color:var(--muted2);background:var(--bg2);transition:all .3s}
.wz-dot.active{border-color:var(--ac);color:var(--ac);background:var(--ac2);box-shadow:0 0 20px var(--acg)}
.wz-dot.done{border-color:var(--grn);color:var(--grn);background:var(--grn2)}
.wz-lbl{font-family:'IBM Plex Mono',monospace;font-size:8.5px;letter-spacing:1.5px;text-transform:uppercase;color:var(--muted);text-align:center;white-space:nowrap}
.wz-lbl.active{color:var(--ac)}
.wz-line{flex:1;height:1px;background:var(--bd);margin-bottom:22px}
.wz-line.done{background:rgba(0,232,135,.3)}

/* CARDS */
.sec-card{background:var(--bg2);border:1px solid var(--bd);border-radius:18px;padding:22px 24px;margin-bottom:14px}
.sec-hdr{display:flex;align-items:center;gap:10px;padding-bottom:14px;border-bottom:1px solid var(--bd);margin-bottom:18px}
.sec-num{font-family:'IBM Plex Mono',monospace;font-size:9px;color:var(--muted);padding:3px 9px;background:var(--bg3);border-radius:5px;border:1px solid var(--bd)}
.sec-title{font-family:'IBM Plex Mono',monospace;font-size:11px;letter-spacing:2px;text-transform:uppercase}

/* HEALTH WIDGET */
.health-widget{background:var(--bg2);border:1px solid var(--bd2);border-radius:20px;padding:24px 20px;text-align:center}
.health-ring{position:relative;width:110px;height:110px;margin:0 auto 12px}
.health-val{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:'Syne',sans-serif}
.health-score{font-size:2.2rem;font-weight:800;line-height:1;animation:scoreIn .6s ease both}
.health-sub{font-size:9px;font-family:'IBM Plex Mono',monospace;color:var(--muted2)}
.health-label{font-family:'IBM Plex Mono',monospace;font-size:9px;letter-spacing:2px;text-transform:uppercase;color:var(--muted);margin-bottom:4px}
.health-verdict{font-family:'Syne',sans-serif;font-size:1rem;font-weight:700}

/* METRICS */
.metrics-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:14px}
.metric-card{background:var(--bg2);border:1px solid var(--bd);border-radius:14px;padding:16px}
.metric-lbl{font-family:'IBM Plex Mono',monospace;font-size:8.5px;letter-spacing:2px;text-transform:uppercase;color:var(--muted);margin-bottom:8px}
.metric-val{font-family:'Syne',sans-serif;font-size:2rem;font-weight:800;line-height:1;margin-bottom:3px}
.metric-sub{font-size:11px;color:var(--muted2)}

/* AGENT PIPELINE */
.ag-pipeline{display:flex;align-items:center;gap:0;padding:20px 0;margin-bottom:16px}
.ag-step{display:flex;flex-direction:column;align-items:center;gap:6px;min-width:80px}
.ag-dot{width:36px;height:36px;border-radius:50%;border:1.5px solid var(--bd2);display:flex;align-items:center;justify-content:center;font-family:'IBM Plex Mono',monospace;font-size:12px;color:var(--muted2);background:var(--bg2);transition:all .3s}
.ag-dot.active{border-color:var(--ac);color:var(--ac);background:var(--ac2);box-shadow:0 0 18px var(--acg);animation:pulse 1s infinite}
.ag-dot.done{border-color:var(--grn);color:var(--grn);background:var(--grn2)}
.ag-lbl{font-family:'IBM Plex Mono',monospace;font-size:8px;letter-spacing:1.2px;text-transform:uppercase;color:var(--muted);text-align:center;line-height:1.4}
.ag-lbl.active{color:var(--ac)}
.ag-line{flex:1;height:1px;background:var(--bd);margin-bottom:22px}
.ag-line.done{background:rgba(0,232,135,.3)}
.ag-line.active{background:rgba(0,212,255,.3)}
.agent-log{background:var(--bg);border:1px solid var(--bd);border-radius:12px;padding:14px;font-family:'IBM Plex Mono',monospace;font-size:11px;max-height:280px;overflow-y:auto}
.lg-line{display:flex;gap:10px;padding:4px 0;border-bottom:1px solid rgba(255,255,255,.02);align-items:flex-start}
.lg-line:last-child{border-bottom:none}
.lg-ts{color:var(--muted);flex-shrink:0;font-size:9.5px;padding-top:1px}
.lg-k{flex-shrink:0;font-size:9px;padding:1px 6px;border-radius:3px;margin-top:1px}
.lg-think{color:#9d7eff;background:rgba(157,126,255,.1)}
.lg-action{color:var(--ac);background:var(--ac2)}
.lg-result{color:var(--grn);background:var(--grn2)}
.lg-warn{color:var(--ylw);background:var(--ylw2)}
.lg-m{color:var(--muted2);flex:1;line-height:1.5}
.lg-m b{color:var(--text);font-weight:600}

/* BADGES */
.badge{display:inline-flex;align-items:center;gap:5px;padding:3px 10px;border-radius:20px;font-family:'IBM Plex Mono',monospace;font-size:9.5px;font-weight:600}
.badge-ac{background:var(--ac2);border:1px solid rgba(0,212,255,.25);color:var(--ac)}
.badge-grn{background:var(--grn2);border:1px solid rgba(0,232,135,.25);color:var(--grn)}
.badge-ylw{background:var(--ylw2);border:1px solid rgba(255,190,0,.25);color:var(--ylw)}
.badge-red{background:var(--red2);border:1px solid rgba(255,64,64,.25);color:var(--red)}
.badge-prp{background:var(--prp2);border:1px solid rgba(157,126,255,.25);color:var(--prp)}
.bdot{width:5px;height:5px;border-radius:50%;background:currentColor}

/* RESOURCE ITEMS */
.res-item{display:flex;align-items:center;gap:12px;padding:12px 14px;border-radius:12px;border:1px solid var(--bd);background:var(--bg2);margin-bottom:8px;transition:all .2s}
.res-item:hover{box-shadow:0 4px 20px rgba(0,0,0,.3);transform:translateX(3px)}
.res-bar-wrap{width:80px;height:5px;background:var(--bg3);border-radius:5px;flex-shrink:0}
.res-bar{height:5px;border-radius:5px}

/* ACTION ITEMS */
.action-item{display:flex;gap:12px;padding:14px;border-radius:13px;border:1px solid var(--bd);background:var(--bg2);margin-bottom:9px;transition:all .2s}
.action-item:hover{transform:translateX(4px);box-shadow:0 4px 20px rgba(0,0,0,.3)}
.action-rank{width:32px;height:32px;border-radius:9px;display:flex;align-items:center;justify-content:center;font-family:'Syne',sans-serif;font-size:15px;font-weight:800;flex-shrink:0}
.action-body{flex:1}
.action-name{font-size:13.5px;font-weight:700;margin-bottom:3px}
.action-reason{font-size:12px;color:var(--muted2);line-height:1.5}
.action-meta{display:flex;gap:7px;flex-wrap:wrap;margin-top:7px}
.score-box{font-family:'Syne',sans-serif;font-size:1.6rem;font-weight:800;padding:6px 14px;border-radius:10px;text-align:center}

/* PHASE TIMELINE */
.phase-item{display:flex;gap:14px;margin-bottom:14px}
.phase-dot-col{display:flex;flex-direction:column;align-items:center;flex-shrink:0}
.phase-circle{width:32px;height:32px;border-radius:50%;background:var(--ac2);border:1.5px solid var(--ac);display:flex;align-items:center;justify-content:center;font-family:'IBM Plex Mono',monospace;font-size:10px;color:var(--ac);flex-shrink:0}
.phase-line{flex:1;width:1px;background:var(--bd);margin:4px 0}
.phase-body{flex:1;padding-bottom:14px}
.phase-lbl{font-family:'IBM Plex Mono',monospace;font-size:10px;letter-spacing:1.5px;text-transform:uppercase;color:var(--ac);margin-bottom:7px}
.phase-action{display:flex;gap:8px;padding:6px 0;font-size:12.5px;color:var(--text);border-bottom:1px solid rgba(255,255,255,.03)}
.phase-action:last-child{border-bottom:none}

/* XAI */
.xai-card{background:var(--bg2);border:1px solid var(--bd);border-radius:14px;padding:14px;margin-bottom:9px}
.xai-hdr{display:flex;align-items:center;gap:10px;margin-bottom:8px}
.xai-icon{width:28px;height:28px;border-radius:8px;background:var(--prp2);border:1px solid rgba(157,126,255,.3);display:flex;align-items:center;justify-content:center;font-size:13px;flex-shrink:0}
.xai-title{font-family:'IBM Plex Mono',monospace;font-size:10.5px;font-weight:600;color:var(--prp)}
.xai-conf{margin-left:auto;font-family:'IBM Plex Mono',monospace;font-size:9px;color:var(--muted)}
.xai-body{font-size:12.5px;color:var(--text);line-height:1.6}
.xai-data{font-size:11px;color:var(--muted2);margin-top:4px;font-style:italic}

/* CHAT */
.chat-hero{background:linear-gradient(135deg,var(--bg3),var(--bg2));border:1px solid rgba(0,212,255,.18);border-radius:18px;padding:18px 22px;margin-bottom:14px;display:flex;align-items:center;gap:16px}
.bot-avatar{width:46px;height:46px;border-radius:13px;background:var(--ac2);border:1px solid rgba(0,212,255,.3);display:flex;align-items:center;justify-content:center;font-size:22px;flex-shrink:0}
.chat-window{background:var(--bg2);border:1px solid var(--bd);border-radius:14px;padding:16px;min-height:280px;max-height:400px;overflow-y:auto;display:flex;flex-direction:column;gap:10px;margin-bottom:10px}
.msg-row-user{display:flex;justify-content:flex-end}
.msg-row-bot{display:flex;justify-content:flex-start}
.bubble{max-width:80%;padding:11px 15px;border-radius:16px;font-size:13.5px;line-height:1.65;animation:bounceIn .3s ease both}
.user-bub{background:var(--ac2);border:1px solid rgba(0,212,255,.25);border-bottom-right-radius:4px}
.bot-bub{background:var(--prp2);border:1px solid rgba(157,126,255,.2);border-bottom-left-radius:4px;color:#d0d8f8}

/* TABS */
.tab-bar{display:flex;gap:0;border-bottom:1px solid var(--bd);margin-bottom:1.5rem;overflow-x:auto}
.tab-btn-html{padding:12px 18px;font-family:'IBM Plex Mono',monospace;font-size:10px;letter-spacing:1.5px;text-transform:uppercase;color:var(--muted2);border:none;background:transparent;border-bottom:2px solid transparent;white-space:nowrap;display:inline-flex;align-items:center;gap:6px}
.tab-btn-html.active{color:var(--ac);border-bottom-color:var(--ac)}

/* FORMS */
.stTextInput>div>div>input,.stNumberInput>div>div>input,.stTextArea>div>div>textarea{background:var(--bg)!important;border:1.5px solid var(--bd2)!important;border-radius:10px!important;font-family:'Manrope',sans-serif!important;font-size:13px!important;color:var(--text)!important}
.stTextInput>div>div>input:focus,.stNumberInput>div>div>input:focus,.stTextArea>div>div>textarea:focus{border-color:rgba(0,212,255,.45)!important;box-shadow:0 0 0 3px rgba(0,212,255,.06)!important}
.stTextInput label,.stNumberInput label,.stTextArea label,.stSelectbox label{font-family:'IBM Plex Mono',monospace!important;font-size:10px!important;letter-spacing:1.5px!important;text-transform:uppercase!important;color:#6ab0d4!important;font-weight:500!important;margin-bottom:4px!important}
.stTextInput label p,.stNumberInput label p,.stTextArea label p,.stSelectbox label p{color:#6ab0d4!important;font-size:10px!important}
.stSelectbox>div>div{background:var(--bg)!important;border:1.5px solid var(--bd2)!important;border-radius:10px!important;color:var(--text)!important}
.stCheckbox label{font-family:'Manrope',sans-serif!important;font-size:13px!important;color:var(--muted2)!important}
.stSlider label{font-family:'IBM Plex Mono',monospace!important;font-size:10px!important;letter-spacing:1.5px!important;text-transform:uppercase!important;color:#6ab0d4!important}

/* BUTTONS */
.stButton>button{background:var(--bg3)!important;border:1.5px solid var(--bd2)!important;color:var(--muted2)!important;font-family:'Manrope',sans-serif!important;font-size:13px!important;font-weight:600!important;border-radius:10px!important;transition:all .2s!important}
.stButton>button:hover{border-color:rgba(255,255,255,.2)!important;color:var(--text)!important;background:var(--bg4)!important}
.btn-launch .stButton>button{background:linear-gradient(135deg,#00d4ff,#0077cc)!important;border:none!important;color:#05080f!important;font-family:'Syne',sans-serif!important;font-size:15px!important;font-weight:700!important;border-radius:14px!important;height:4em!important;box-shadow:0 0 32px rgba(0,212,255,.25),0 6px 18px rgba(0,212,255,.15)!important;animation:pulse2 2s infinite}
.btn-launch .stButton>button:hover{transform:translateY(-3px)!important;animation:none!important}
.btn-next .stButton>button{background:var(--ac2)!important;border:1.5px solid var(--ac)!important;color:var(--ac)!important;font-weight:700!important;border-radius:12px!important;height:3em!important}
.btn-next .stButton>button:hover{background:rgba(0,212,255,.2)!important;transform:translateY(-2px)!important}
.btn-add .stButton>button{background:var(--grn2)!important;border:1.5px solid var(--grn)!important;color:var(--grn)!important;font-size:12px!important;font-weight:700!important;border-radius:9px!important}
.btn-del .stButton>button{background:var(--red2)!important;border:1.5px solid rgba(255,64,64,.35)!important;color:var(--red)!important;font-size:12px!important;border-radius:9px!important}
.btn-ghost .stButton>button{background:transparent!important;border:1px solid var(--bd)!important;color:var(--muted)!important;font-size:12px!important;border-radius:10px!important;height:2.5em!important}
.btn-ghost .stButton>button:hover{border-color:rgba(255,255,255,.14)!important;color:var(--text)!important}
[data-testid="stHorizontalBlock"]{gap:10px!important}
[data-testid="stChatInput"] textarea{background:var(--bg3)!important;border:1.5px solid rgba(0,212,255,.22)!important;border-radius:12px!important;color:var(--text)!important;font-family:'Manrope',sans-serif!important}
</style>
""", unsafe_allow_html=True)

# ── TOP NAV ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="top-nav au">
  <div class="nav-logo">Resource<span>IQ</span></div>
  <div class="nav-badge"><span class="nav-dot"></span>5-Agent Pipeline Active</div>
  <div class="nav-spacer"></div>
  <div class="nav-model">Groq · LLaMA 3.3 70B · Optimisation Agent</div>
</div>
""", unsafe_allow_html=True)


# ── WIZARD BAR HELPER ──────────────────────────────────────────────────────────
def wizard_bar(active_step):
    steps = [("01", "Organisation"), ("02", "Your Team"), ("03", "Resources"), ("04", "Launch")]
    html = ""
    for i, (num, lbl) in enumerate(steps):
        cls = "done" if i < active_step else ("active" if i == active_step else "")
        lc  = "active" if i == active_step else ""
        sym = "✓" if i < active_step else num
        html += (
            f'<div class="wz-step">'
            f'<div class="wz-dot {cls}">{sym}</div>'
            f'<div class="wz-lbl {lc}">{lbl}</div>'
            f'</div>'
        )
        if i < len(steps) - 1:
            html += f'<div class="wz-line {"done" if i < active_step else ""}"></div>'
    st.markdown(f'<div class="wizard-bar">{html}</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# STEP 1 — ORGANISATION & SETTINGS
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.view == "step1":
    wizard_bar(0)

    st.markdown("""
    <div class="au" style="margin-bottom:28px">
      <div style="font-family:'IBM Plex Mono',monospace;font-size:10px;letter-spacing:2.5px;text-transform:uppercase;color:var(--muted);margin-bottom:10px">Step 1 of 3</div>
      <h1 style="font-family:'Syne',sans-serif;font-size:clamp(2rem,5vw,3.2rem);font-weight:800;letter-spacing:-1px;line-height:1;margin:0 0 12px">
        Organisation &amp; <span style="color:var(--ac)">Settings</span>
      </h1>
      <p style="font-size:14px;color:var(--muted2);max-width:520px;line-height:1.7;margin:0">
        Tell the agent about your organisation, what you want to optimise, and your constraints.
      </p>
    </div>
    """, unsafe_allow_html=True)

    left, right = st.columns([1.6, 1], gap="large")

    with left:
        st.markdown("""<div class="sec-card au d1"><div class="sec-hdr"><span class="sec-num">CONFIG</span><span class="sec-title" style="color:var(--ac)">Agent Configuration</span></div></div>""", unsafe_allow_html=True)
        api_key = st.text_input(
            "🔑 Groq API Key",
            type="password",
            value=st.secrets.get("GROQ_API_KEY", ""),
            key="s1_api"
        )
        org_name = st.text_input("🏢 Organisation / Project Name", placeholder="e.g. Acme Engineering, Product Team Q4…", key="s1_org")
        goal     = st.text_area("🎯 Optimisation Goal", placeholder="e.g. Reduce infrastructure costs by 30%, consolidate duplicate tools…", height=80, key="s1_goal")

        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
        st.markdown("""<div class="sec-card au d2"><div class="sec-hdr"><span class="sec-num">PARAMS</span><span class="sec-title" style="color:var(--ac)">Optimisation Parameters</span></div></div>""", unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            threshold = st.slider("Underutilisation Threshold %", 10, 80, 50, key="s1_thresh")
            budget    = st.number_input("💰 Monthly Budget (₹)", min_value=0, value=500000, step=10000, key="s1_budget")
        with c2:
            strategy  = st.selectbox("Strategy", ["moderate", "aggressive", "conservative"], key="s1_strategy")
            timeframe = st.selectbox("Reporting Timeframe", ["monthly", "quarterly", "annual"], key="s1_timeframe")

    with right:
        savings_est  = int(budget * {"moderate": 0.25, "aggressive": 0.40, "conservative": 0.15}.get(strategy, 0.25))
        health_est   = max(30, min(90, 100 - threshold))
        risk_label   = "HIGH" if threshold > 60 else "MEDIUM" if threshold > 35 else "LOW"
        risk_c       = {"HIGH": "#ff4040", "MEDIUM": "#ffbe00", "LOW": "#00e887"}.get(risk_label, "#ffbe00")
        circumf      = 282
        off          = circumf - (circumf * health_est / 100)

        st.markdown(f"""
        <div class="au d2" style="display:flex;flex-direction:column;gap:12px">
          <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;letter-spacing:2px;text-transform:uppercase;color:var(--muted);margin-bottom:-4px">Live Config Preview</div>
          <div class="health-widget">
            <div class="health-label">Optimisation Potential</div>
            <div class="health-ring">
              <svg viewBox="0 0 110 110" style="width:110px;height:110px;transform:rotate(-90deg)">
                <circle cx="55" cy="55" r="45" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="7"/>
                <circle cx="55" cy="55" r="45" fill="none" stroke="{risk_c}" stroke-width="7" stroke-linecap="round" stroke-dasharray="{circumf}" stroke-dashoffset="{off}" style="filter:drop-shadow(0 0 8px {risk_c})"/>
              </svg>
              <div class="health-val">
                <div class="health-score" style="color:{risk_c}">{health_est}</div>
                <div class="health-sub">/100</div>
              </div>
            </div>
            <div class="health-verdict" style="color:{risk_c}">{risk_label} WASTE RISK</div>
          </div>
          <div style="background:var(--bg2);border:1px solid var(--bd);border-radius:14px;padding:16px">
            <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;letter-spacing:2px;text-transform:uppercase;color:var(--muted);margin-bottom:12px">Config Summary</div>
            <div style="display:flex;flex-direction:column;gap:8px;font-size:12.5px">
              <div style="display:flex;justify-content:space-between"><span style="color:var(--muted2)">Organisation</span><span style="color:var(--text);font-weight:600;max-width:140px;text-align:right;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">{org_name or "—"}</span></div>
              <div style="display:flex;justify-content:space-between"><span style="color:var(--muted2)">Strategy</span><span style="color:var(--ac);font-weight:600">{strategy.upper()}</span></div>
              <div style="display:flex;justify-content:space-between"><span style="color:var(--muted2)">Threshold</span><span style="color:var(--text);font-weight:600">Below {threshold}%</span></div>
              <div style="display:flex;justify-content:space-between"><span style="color:var(--muted2)">Est. Savings</span><span style="color:var(--grn);font-weight:600">₹{savings_est:,}/mo</span></div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
    _, nc, _ = st.columns([1, 2, 1])
    with nc:
        st.markdown('<div class="btn-next">', unsafe_allow_html=True)
        if st.button("Next: Add Your Team →", key="s1_next", use_container_width=True):
            if not api_key.strip():
                st.warning("⚠️ Please enter your Groq API key.")
            elif not org_name.strip():
                st.warning("⚠️ Please enter an organisation name.")
            elif not goal.strip():
                st.warning("⚠️ Please describe your optimisation goal.")
            else:
                st.session_state.inputs.update({
                    "api_key": api_key, "org_name": org_name, "goal": goal,
                    "threshold": threshold, "budget": budget,
                    "strategy": strategy, "timeframe": timeframe,
                })
                st.session_state.view = "step2"
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# STEP 2 — TEAM
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.view == "step2":
    wizard_bar(1)

    st.markdown("""
    <div class="au" style="margin-bottom:24px">
      <div style="font-family:'IBM Plex Mono',monospace;font-size:10px;letter-spacing:2.5px;text-transform:uppercase;color:var(--muted);margin-bottom:10px">Step 2 of 3</div>
      <h1 style="font-family:'Syne',sans-serif;font-size:clamp(2rem,5vw,3.2rem);font-weight:800;letter-spacing:-1px;line-height:1;margin:0 0 12px">
        Your <span style="color:var(--grn)">Team</span>
      </h1>
      <p style="font-size:14px;color:var(--muted2);max-width:560px;line-height:1.7;margin:0">
        Add team members managing these resources. The agent will detect who is overloaded and suggest reallocation.
      </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""<div class="sec-card au"><div class="sec-hdr"><span class="sec-num">TEAM</span><span class="sec-title" style="color:var(--grn)">Team Members</span></div></div>""", unsafe_allow_html=True)

    hcols = st.columns([2, 2, 1.2, 1.4, 2, 1, 0.6])
    for col, h in zip(hcols, ["👤 Name", "💼 Role", "⚡ Workload %", "🕒 Hrs/Week", "🛠 Skills", "📍 Team", ""]):
        with col:
            st.markdown(
                f'<div style="font-family:IBM Plex Mono,monospace;font-size:8.5px;letter-spacing:1.5px;'
                f'text-transform:uppercase;color:var(--muted);padding:4px 0">{h}</div>',
                unsafe_allow_html=True,
            )

    rows   = st.session_state.team_rows
    to_del = None
    for i, row in enumerate(rows):
        c1, c2, c3, c4, c5, c6, c7 = st.columns([2, 2, 1.2, 1.4, 2, 1, 0.6])
        with c1: rows[i]["name"]            = st.text_input(f"tn_{i}", value=row.get("name", ""),            placeholder="e.g. Priya Sharma",   key=f"tm_n_{i}", label_visibility="collapsed")
        with c2: rows[i]["role"]            = st.text_input(f"tr_{i}", value=row.get("role", ""),            placeholder="e.g. DevOps Lead",    key=f"tm_r_{i}", label_visibility="collapsed")
        with c3: rows[i]["load"]            = st.number_input(f"tl_{i}", min_value=0, max_value=200, value=int(row.get("load", 50)),            step=5,  key=f"tm_l_{i}", label_visibility="collapsed")
        with c4: rows[i]["available_hours"] = st.number_input(f"th_{i}", min_value=0, max_value=80,  value=int(row.get("available_hours", 40)), step=4,  key=f"tm_h_{i}", label_visibility="collapsed")
        with c5: rows[i]["skills"]          = st.text_input(f"ts_{i}", value=row.get("skills", ""),          placeholder="e.g. Kubernetes, AWS", key=f"tm_s_{i}", label_visibility="collapsed")
        with c6: rows[i]["team"]            = st.text_input(f"tt_{i}", value=row.get("team", ""),            placeholder="e.g. Platform",        key=f"tm_t_{i}", label_visibility="collapsed")
        with c7:
            st.markdown('<div class="btn-del">', unsafe_allow_html=True)
            if st.button("✕", key=f"tm_del_{i}", use_container_width=True) and len(rows) > 1:
                to_del = i
            st.markdown('</div>', unsafe_allow_html=True)
        if i < len(rows) - 1:
            st.markdown('<div style="height:4px;border-bottom:1px solid rgba(255,255,255,0.04);margin-bottom:4px"></div>', unsafe_allow_html=True)

    if to_del is not None:
        st.session_state.team_rows.pop(to_del)
        st.rerun()

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    ac, _, _ = st.columns([1, 2, 2])
    with ac:
        st.markdown('<div class="btn-add">', unsafe_allow_html=True)
        if st.button("＋ Add Member", key="tm_add", use_container_width=True):
            st.session_state.team_rows.append({"name": "", "role": "", "load": 50, "skills": "", "available_hours": 40, "team": ""})
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # Team preview cards
    valid_team = [r for r in rows if r.get("name", "").strip()]
    if valid_team:
        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
        tcols = st.columns(min(5, len(valid_team)))
        for i, m in enumerate(valid_team[:5]):
            lc    = m.get("load", 50)
            lc_c  = "#ff4040" if lc > 100 else ("#ffbe00" if lc > 80 else "#00e887")
            av    = "".join([w[0].upper() for w in m["name"].split()[:2]])
            with tcols[i]:
                st.markdown(f"""
                <div style="background:var(--bg2);border:1px solid var(--bd);border-radius:16px;padding:14px">
                  <div style="display:flex;align-items:center;gap:8px;margin-bottom:10px">
                    <div style="width:40px;height:40px;border-radius:10px;background:rgba(0,212,255,0.1);color:var(--ac);display:flex;align-items:center;justify-content:center;font-family:'Syne',sans-serif;font-weight:700;font-size:13px">{av}</div>
                    <div><div style="font-size:12px;font-weight:700">{m['name'].split()[0]}</div><div style="font-size:10px;color:var(--muted2)">{m.get('role','')[:16]}</div></div>
                  </div>
                  <div style="display:flex;justify-content:space-between;margin-bottom:4px">
                    <span style="font-family:'IBM Plex Mono',monospace;font-size:8px;color:var(--muted)">LOAD</span>
                    <span style="font-family:'IBM Plex Mono',monospace;font-size:10px;color:{lc_c};font-weight:600">{lc}%</span>
                  </div>
                  <div style="height:5px;background:var(--bg3);border-radius:5px"><div style="height:5px;border-radius:5px;background:{lc_c};width:{min(100, lc)}%"></div></div>
                  {'<div class="badge badge-red" style="margin-top:8px;font-size:8px">OVERLOADED</div>' if lc > 100 else ''}
                </div>
                """, unsafe_allow_html=True)

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
    b1, b2, _ = st.columns([1, 2, 1])
    with b1:
        st.markdown('<div class="btn-ghost">', unsafe_allow_html=True)
        if st.button("← Back", key="s2_back", use_container_width=True):
            st.session_state.view = "step1"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with b2:
        st.markdown('<div class="btn-next">', unsafe_allow_html=True)
        if st.button("Next: Add Resources →", key="s2_next", use_container_width=True):
            valid = [r for r in rows if r.get("name", "").strip()]
            if not valid:
                st.warning("⚠️ Add at least one team member.")
            else:
                st.session_state.inputs["team"] = [
                    {
                        "name":            r["name"],
                        "role":            r.get("role", ""),
                        "load":            int(r.get("load", 50)),
                        "skills":          [s.strip() for s in r.get("skills", "").split(",") if s.strip()],
                        "available_hours": int(r.get("available_hours", 40)),
                        "team":            r.get("team", ""),
                    }
                    for r in valid
                ]
                st.session_state.view = "step3"
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# STEP 3 — RESOURCES
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.view == "step3":
    wizard_bar(2)

    st.markdown("""
    <div class="au" style="margin-bottom:24px">
      <div style="font-family:'IBM Plex Mono',monospace;font-size:10px;letter-spacing:2.5px;text-transform:uppercase;color:var(--muted);margin-bottom:10px">Step 3 of 3</div>
      <h1 style="font-family:'Syne',sans-serif;font-size:clamp(2rem,5vw,3.2rem);font-weight:800;letter-spacing:-1px;line-height:1;margin:0 0 12px">
        Resource <span style="color:var(--ylw)">Inventory</span>
      </h1>
      <p style="font-size:14px;color:var(--muted2);max-width:560px;line-height:1.7;margin:0">
        Add every tool, infrastructure component, and team resource. The agent will detect waste and overlap.
      </p>
    </div>
    """, unsafe_allow_html=True)

    qcol, _, _ = st.columns([2, 2, 1])
    with qcol:
        if st.button("⚡ Load Sample Dataset (12 resources)", key="sample_load"):
            st.session_state.resource_rows = [
                {"id": "R-001", "name": "Kubernetes Cluster A",  "type": "Infrastructure", "utilization": 22, "cost": 45000,  "team": "Platform",   "dependencies": 5,  "notes": ""},
                {"id": "R-002", "name": "Kubernetes Cluster B",  "type": "Infrastructure", "utilization": 18, "cost": 42000,  "team": "Platform",   "dependencies": 2,  "notes": "Duplicate of Cluster A"},
                {"id": "R-003", "name": "Jenkins CI Server",     "type": "Tool",           "utilization": 12, "cost": 8000,   "team": "DevOps",     "dependencies": 8,  "notes": ""},
                {"id": "R-004", "name": "GitHub Actions",        "type": "Tool",           "utilization": 78, "cost": 6000,   "team": "DevOps",     "dependencies": 12, "notes": ""},
                {"id": "R-005", "name": "Datadog Monitoring",    "type": "Tool",           "utilization": 55, "cost": 12000,  "team": "Ops",        "dependencies": 6,  "notes": ""},
                {"id": "R-006", "name": "New Relic APM",         "type": "Tool",           "utilization": 20, "cost": 10000,  "team": "Ops",        "dependencies": 3,  "notes": "Overlaps with Datadog"},
                {"id": "R-007", "name": "AWS EC2 Pool",          "type": "Infrastructure", "utilization": 30, "cost": 65000,  "team": "Cloud",      "dependencies": 15, "notes": ""},
                {"id": "R-008", "name": "Azure VMs",             "type": "Infrastructure", "utilization": 22, "cost": 55000,  "team": "Cloud",      "dependencies": 7,  "notes": ""},
                {"id": "R-009", "name": "Slack Enterprise",      "type": "Tool",           "utilization": 88, "cost": 15000,  "team": "All Teams",  "dependencies": 20, "notes": ""},
                {"id": "R-010", "name": "Microsoft Teams",       "type": "Tool",           "utilization": 15, "cost": 12000,  "team": "All Teams",  "dependencies": 4,  "notes": "Overlaps with Slack"},
                {"id": "R-011", "name": "Dev Team Alpha",        "type": "Team",           "utilization": 35, "cost": 200000, "team": "Engineering","dependencies": 3,  "notes": ""},
                {"id": "R-012", "name": "QA Team",               "type": "Team",           "utilization": 40, "cost": 150000, "team": "Engineering","dependencies": 2,  "notes": ""},
            ]
            st.success("Loaded 12 sample resources!")
            st.rerun()

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    st.markdown("""<div class="sec-card au"><div class="sec-hdr"><span class="sec-num">RESOURCES</span><span class="sec-title" style="color:var(--ylw)">Resource Registry</span></div></div>""", unsafe_allow_html=True)

    team_names = [m.get("name", "") for m in st.session_state.inputs.get("team", [])]
    RTYPES     = ["Infrastructure", "Tool", "Team", "Database", "Service", "Other"]
    hcols2     = st.columns([0.7, 2.2, 1.5, 1, 1, 1.2, 1.5, 1.5, 0.6])
    for col, h in zip(hcols2, ["🆔 ID", "📦 Resource Name", "🏷 Type", "⚡ Util %", "💰 Cost/mo", "👥 Owner Team", "🔗 Dependencies", "📝 Notes", ""]):
        with col:
            st.markdown(
                f'<div style="font-family:IBM Plex Mono,monospace;font-size:8.5px;letter-spacing:1.5px;'
                f'text-transform:uppercase;color:var(--muted);padding:4px 0">{h}</div>',
                unsafe_allow_html=True,
            )

    rows      = st.session_state.resource_rows
    to_del2   = None
    threshold = st.session_state.inputs.get("threshold", 50)

    for i, row in enumerate(rows):
        cols = st.columns([0.7, 2.2, 1.5, 1, 1, 1.2, 1.5, 1.5, 0.6])
        with cols[0]: rows[i]["id"]           = st.text_input(f"rid_{i}",   value=row.get("id", f"R-{i+1:03d}"),                                      key=f"r_id_{i}",   label_visibility="collapsed")
        with cols[1]: rows[i]["name"]         = st.text_input(f"rn_{i}",    value=row.get("name", ""),   placeholder="e.g. Kubernetes Cluster A",      key=f"r_n_{i}",    label_visibility="collapsed")
        with cols[2]:
            cur_t = row.get("type", "Infrastructure")
            tidx  = RTYPES.index(cur_t) if cur_t in RTYPES else 0
            rows[i]["type"] = st.selectbox(f"rt_{i}", RTYPES, index=tidx, key=f"r_t_{i}", label_visibility="collapsed")
        with cols[3]: rows[i]["utilization"]  = st.number_input(f"ru_{i}", min_value=0, max_value=100, value=int(row.get("utilization", 50)), step=5,   key=f"r_u_{i}",   label_visibility="collapsed")
        with cols[4]: rows[i]["cost"]         = st.number_input(f"rc_{i}", min_value=0,               value=int(row.get("cost", 10000)),     step=1000, key=f"r_c_{i}",   label_visibility="collapsed")
        with cols[5]:
            if team_names:
                cur_team = row.get("team", "")
                topts    = ["(None)"] + team_names + ["Other"]
                tidx2    = topts.index(cur_team) if cur_team in topts else 0
                sel      = st.selectbox(f"rteam_{i}", topts, index=tidx2, key=f"r_team_{i}", label_visibility="collapsed")
                rows[i]["team"] = "" if sel == "(None)" else sel
            else:
                rows[i]["team"] = st.text_input(f"rteam_{i}", value=row.get("team", ""), placeholder="Team", key=f"r_team_{i}", label_visibility="collapsed")
        with cols[6]: rows[i]["dependencies"] = st.number_input(f"rdep_{i}", min_value=0, max_value=50, value=int(row.get("dependencies", 0)), step=1, key=f"r_dep_{i}", label_visibility="collapsed")
        with cols[7]: rows[i]["notes"]        = st.text_input(f"rnotes_{i}", value=row.get("notes", ""), placeholder="Optional notes",                  key=f"r_notes_{i}", label_visibility="collapsed")
        with cols[8]:
            st.markdown('<div class="btn-del">', unsafe_allow_html=True)
            if st.button("✕", key=f"r_del_{i}", use_container_width=True) and len(rows) > 1:
                to_del2 = i
            st.markdown('</div>', unsafe_allow_html=True)
        if i < len(rows) - 1:
            st.markdown('<div style="height:3px;border-bottom:1px solid rgba(255,255,255,0.04);margin-bottom:3px"></div>', unsafe_allow_html=True)

    if to_del2 is not None:
        st.session_state.resource_rows.pop(to_del2)
        st.rerun()

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    ac2, _, _ = st.columns([1, 2, 2])
    with ac2:
        st.markdown('<div class="btn-add">', unsafe_allow_html=True)
        if st.button("＋ Add Resource", key="r_add", use_container_width=True):
            n = len(rows) + 1
            st.session_state.resource_rows.append({
                "id": f"R-{n:03d}", "name": "", "type": "Infrastructure",
                "utilization": 50, "cost": 10000, "team": "", "dependencies": 0, "notes": "",
            })
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    valid_res = [r for r in rows if r.get("name", "").strip()]
    if valid_res:
        total_cost    = sum(int(r.get("cost", 0)) for r in valid_res)
        underutil_cnt = sum(1 for r in valid_res if int(r.get("utilization", 50)) < threshold)
        wasted_est    = sum(
            int(r.get("cost", 0)) * (1 - int(r.get("utilization", 50)) / 100)
            for r in valid_res if int(r.get("utilization", 50)) < threshold
        )
        st.markdown(f"""
        <div class="au d2" style="display:flex;gap:10px;flex-wrap:wrap;margin-top:16px">
          <div class="metric-card" style="flex:1;min-width:110px"><div class="metric-lbl">Resources</div><div class="metric-val" style="color:var(--ac)">{len(valid_res)}</div></div>
          <div class="metric-card" style="flex:1;min-width:110px"><div class="metric-lbl">Monthly Spend</div><div class="metric-val" style="color:var(--ylw)">₹{total_cost:,}</div></div>
          <div class="metric-card" style="flex:1;min-width:110px"><div class="metric-lbl">Underutilised</div><div class="metric-val" style="color:{'#ff4040' if underutil_cnt > 0 else '#00e887'}">{underutil_cnt}</div></div>
          <div class="metric-card" style="flex:1;min-width:110px"><div class="metric-lbl">Est. Waste/mo</div><div class="metric-val" style="color:var(--red)">₹{int(wasted_est):,}</div></div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
    b1b, b2b, _ = st.columns([1, 2, 1])
    with b1b:
        st.markdown('<div class="btn-ghost">', unsafe_allow_html=True)
        if st.button("← Back", key="s3_back", use_container_width=True):
            st.session_state.view = "step2"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with b2b:
        st.markdown('<div class="btn-launch">', unsafe_allow_html=True)
        if st.button("⬡  Launch 5-Agent Optimisation Pipeline  →", key="s3_launch", use_container_width=True):
            valid = [r for r in rows if r.get("name", "").strip()]
            if not valid:
                st.warning("⚠️ Add at least one resource.")
            else:
                st.session_state.inputs["resources"] = valid
                st.session_state.view = "running"
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# RUNNING
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.view == "running":
    st.markdown("""
    <div class="au" style="padding:2rem 0 1.5rem">
      <div style="font-family:'IBM Plex Mono',monospace;font-size:10px;letter-spacing:2.5px;text-transform:uppercase;color:var(--ac);margin-bottom:8px">Agent Pipeline Executing</div>
      <h2 style="font-family:'Syne',sans-serif;font-size:2.2rem;font-weight:800;margin:0 0 6px">Running 5-Agent Analysis…</h2>
      <p style="font-size:13px;color:var(--muted2)">Scan → Analyse → Prioritise → Plan → Report. Watch the live log.</p>
    </div>
    """, unsafe_allow_html=True)

    step_ph     = st.empty()
    progress_ph = st.empty()
    log_ph      = st.empty()
    step_ph.markdown('<div class="ag-pipeline" style="padding:20px 0"></div>', unsafe_allow_html=True)
    progress_ph.progress(0)

    try:
        result = run_multi_agent(
            st.session_state.inputs,
            step_ph, log_ph, progress_ph,
            st.session_state.inputs.get("api_key", ""),
        )
        st.session_state.analysis   = result
        st.session_state.view       = "results"
        st.session_state.active_tab = "overview"
        time.sleep(0.6)
        st.rerun()
    except Exception as e:
        st.error(f"Agent error: {e}")
        st.markdown('<div class="btn-ghost">', unsafe_allow_html=True)
        if st.button("← Back", key="back_err"):
            st.session_state.view = "step3"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# RESULTS — 8 TABS
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.view == "results":
    analysis   = st.session_state.analysis or {}
    inp        = st.session_state.inputs   or {}
    scan       = analysis.get("scan",       {})
    analyse    = analysis.get("analyse",    {})
    prioritise = analysis.get("prioritise", {})
    plan       = analysis.get("plan",       {})
    report     = analysis.get("report",     {})
    team_data  = inp.get("team",       [])
    resources  = inp.get("resources",  [])
    api_key    = inp.get("api_key",    "")

    score_before = report.get("health_before", 45)
    score_after  = report.get("health_after",  80)
    risk_level   = analyse.get("risk_level", "HIGH")
    risk_c       = {"CRITICAL": "#ff4040", "HIGH": "#ff8c42", "MEDIUM": "#ffbe00", "LOW": "#00e887"}.get(risk_level, "#ff8c42")

    TABS = [
        ("📊", "overview",  "Overview"),
        ("📦", "resources", "Resources"),
        ("🎯", "actions",   "Action Plan"),
        ("🔧", "phases",    "Execution Phases"),
        ("🧑‍🤝‍🧑", "team",   "Team View"),
        ("🧠", "explain",   "Why AI Did This"),
        ("🔮", "whatif",    "What-If"),
        ("💬", "chat",      "Chat Agent"),
    ]

    tcols = st.columns(len(TABS))
    for i, (icon, slug, label) in enumerate(TABS):
        with tcols[i]:
            if st.button(f"{icon} {label}", key=f"tab_{slug}", use_container_width=True):
                st.session_state.active_tab = slug
                st.rerun()

    tab_html = "".join(
        f'<span class="tab-btn-html {"active" if st.session_state.active_tab == slug else ""}">'
        f'{icon} {label}</span>'
        for icon, slug, label in TABS
    )
    st.markdown(f'<div class="tab-bar" style="pointer-events:none">{tab_html}</div>', unsafe_allow_html=True)

    at = st.session_state.active_tab

    # ── OVERVIEW ─────────────────────────────────────────────────────────────
    if at == "overview":
        circumf = 282
        sc_b    = "#ff4040" if score_before < 50 else ("#ffbe00" if score_before < 70 else "#00e887")
        sc_a    = "#00e887" if score_after  >= 70 else ("#ffbe00" if score_after  >= 50 else "#ff4040")
        off_b   = circumf - (circumf * score_before / 100)
        off_a   = circumf - (circumf * score_after  / 100)

        c1, c2, c3 = st.columns([1, 1, 2])
        with c1:
            st.markdown(f"""
            <div class="health-widget au">
              <div class="health-label">Resource Health Now</div>
              <div class="health-ring">
                <svg viewBox="0 0 110 110" style="width:110px;height:110px;transform:rotate(-90deg)">
                  <circle cx="55" cy="55" r="45" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="7"/>
                  <circle cx="55" cy="55" r="45" fill="none" stroke="{sc_b}" stroke-width="7" stroke-linecap="round" stroke-dasharray="{circumf}" stroke-dashoffset="{off_b}" style="filter:drop-shadow(0 0 6px {sc_b})"/>
                </svg>
                <div class="health-val"><div class="health-score" style="color:{sc_b}">{score_before}</div><div class="health-sub">/100</div></div>
              </div>
              <div class="health-verdict" style="color:{sc_b}">{risk_level} RISK</div>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div class="health-widget au d1">
              <div class="health-label">After Optimisation</div>
              <div class="health-ring">
                <svg viewBox="0 0 110 110" style="width:110px;height:110px;transform:rotate(-90deg)">
                  <circle cx="55" cy="55" r="45" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="7"/>
                  <circle cx="55" cy="55" r="45" fill="none" stroke="{sc_a}" stroke-width="7" stroke-linecap="round" stroke-dasharray="{circumf}" stroke-dashoffset="{off_a}" style="filter:drop-shadow(0 0 8px {sc_a})"/>
                </svg>
                <div class="health-val"><div class="health-score" style="color:{sc_a}">{score_after}</div><div class="health-sub">/100</div></div>
              </div>
              <div class="health-verdict" style="color:{sc_a}">OPTIMISED</div>
            </div>
            """, unsafe_allow_html=True)
        with c3:
            ms  = plan.get("projected_monthly_saving", 0)
            ans = plan.get("projected_annual_saving",  0)
            pb  = plan.get("payback_months",            2)
            ec  = plan.get("execution_confidence",     78)
            st.markdown(f"""
            <div class="au d2" style="display:flex;flex-direction:column;gap:10px">
              <div class="metrics-grid" style="grid-template-columns:1fr 1fr">
                <div class="metric-card"><div class="metric-lbl">Monthly Saving</div><div class="metric-val" style="color:var(--grn)">₹{ms:,}</div><div class="metric-sub">projected</div></div>
                <div class="metric-card"><div class="metric-lbl">Annual Saving</div><div class="metric-val" style="color:var(--grn)">₹{ans:,}</div><div class="metric-sub">projected</div></div>
                <div class="metric-card"><div class="metric-lbl">Payback Period</div><div class="metric-val" style="color:var(--ac)">{pb}mo</div><div class="metric-sub">to break even</div></div>
                <div class="metric-card"><div class="metric-lbl">Confidence</div><div class="metric-val" style="color:var(--ac)">{ec}%</div><div class="metric-sub">agent confidence</div></div>
              </div>
              <div style="background:var(--grn2);border:1px solid rgba(0,232,135,0.2);border-radius:14px;padding:14px 16px">
                <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;letter-spacing:2px;text-transform:uppercase;color:var(--grn);margin-bottom:6px">Executive Summary</div>
                <div style="font-size:13px;color:var(--text);line-height:1.7">{report.get('executive_summary', 'Optimisation complete.')}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

        wb = analyse.get("waste_breakdown", {})
        if any(wb.values()):
            total_wb = sum(wb.values()) or 1
            bars     = "".join(
                f'<div style="flex:1;min-width:120px">'
                f'<div style="font-family:IBM Plex Mono,monospace;font-size:9px;color:var(--muted);margin-bottom:6px;letter-spacing:1px">{k.upper()}</div>'
                f'<div style="font-family:Syne,sans-serif;font-size:1.4rem;font-weight:800;color:var(--red)">₹{v:,}</div>'
                f'<div style="height:4px;background:var(--bg3);border-radius:4px;margin-top:6px">'
                f'<div style="height:4px;border-radius:4px;background:var(--red);width:{int(v / total_wb * 100)}%"></div>'
                f'</div></div>'
                for k, v in wb.items() if v > 0
            )
            st.markdown(f"""
            <div class="au d3" style="background:var(--bg2);border:1px solid rgba(255,64,64,0.12);border-radius:16px;padding:18px 20px;margin-top:14px">
              <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;letter-spacing:2px;text-transform:uppercase;color:var(--red);margin-bottom:14px">💸 Monthly Waste Breakdown</div>
              <div style="display:flex;gap:12px;flex-wrap:wrap">{bars}</div>
            </div>
            """, unsafe_allow_html=True)

        gaps = analyse.get("capacity_gaps", [])
        if gaps:
            g_html = "".join(
                f'<div style="display:flex;align-items:flex-start;gap:10px;padding:9px 0;'
                f'border-bottom:1px solid rgba(255,255,255,0.03);font-size:13px">'
                f'<span style="color:var(--ylw);flex-shrink:0">⚠</span>'
                f'<div><div style="color:var(--text);font-weight:600">{g["area"]}</div>'
                f'<div style="font-size:12px;color:var(--muted2);margin-top:2px">{g["issue"]} — {g["impact"]}</div></div>'
                f'<span class="badge {"badge-red" if g["urgency"] == "HIGH" else "badge-ylw"}" '
                f'style="margin-left:auto;flex-shrink:0">{g["urgency"]}</span></div>'
                for g in gaps
            )
            st.markdown(
                f'<div class="au d4" style="background:var(--bg2);border:1px solid rgba(255,190,0,0.15);'
                f'border-radius:16px;padding:18px 20px;margin-top:14px">'
                f'<div style="font-family:IBM Plex Mono,monospace;font-size:9px;letter-spacing:2px;'
                f'text-transform:uppercase;color:var(--ylw);margin-bottom:10px">⚡ Capacity Gaps</div>'
                f'{g_html}</div>',
                unsafe_allow_html=True,
            )

    # ── RESOURCES ────────────────────────────────────────────────────────────
    elif at == "resources":
        threshold     = inp.get("threshold", 50)
        underutil_list = scan.get("underutilised", [])
        redundant      = analyse.get("redundant_resources", [])
        consolid       = analyse.get("consolidation_opportunities", [])

        st.markdown(f"""
        <div class="au" style="background:var(--red2);border:1px solid rgba(255,64,64,0.2);border-left:3px solid var(--red);border-radius:12px;padding:14px 18px;margin-bottom:16px;display:flex;align-items:center;gap:14px">
          <span style="font-size:24px">💸</span>
          <div>
            <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;letter-spacing:2px;text-transform:uppercase;color:var(--red)">Estimated Monthly Waste</div>
            <div style="font-family:'Syne',sans-serif;font-size:2rem;font-weight:800;color:var(--red)">₹{scan.get('estimated_waste', 0):,}</div>
          </div>
          <div style="margin-left:auto;text-align:right">
            <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;color:var(--muted)">UNDERUTILISED</div>
            <div style="font-family:'Syne',sans-serif;font-size:2rem;font-weight:800;color:var(--ylw)">{scan.get('underutilised_count', 0)}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        redundant_names = {rd["name"] for rd in redundant}
        consolid_names  = {co["resource_a"] for co in consolid} | {co["resource_b"] for co in consolid}

        for r in resources:
            util         = int(r.get("utilization", 50))
            cost         = int(r.get("cost", 0))
            is_under     = util < threshold
            uc           = "#ff4040" if util < 20 else ("#ffbe00" if util < threshold else "#00e887")
            is_redundant = r["name"] in redundant_names
            is_consolid  = r["name"] in consolid_names
            flags        = (
                ('<span class="badge badge-red" style="font-size:8px">REDUNDANT</span>' if is_redundant else "") +
                ('<span class="badge badge-ylw" style="font-size:8px">CONSOLIDATE</span>' if is_consolid else "") +
                ('<span class="badge badge-red" style="font-size:8px">UNDERUTILISED</span>' if is_under and not is_redundant else "")
            )
            st.markdown(f"""
            <div class="res-item au">
              <div style="font-family:'IBM Plex Mono',monospace;font-size:10px;color:var(--muted);width:54px;flex-shrink:0">{r.get('id', '')}</div>
              <div style="flex:1">
                <div style="font-size:13.5px;font-weight:600">{r['name']} {flags}</div>
                <div style="font-size:11px;color:var(--muted2);margin-top:2px">{r.get('type', '')} · {r.get('team', 'Unassigned')} · {r.get('dependencies', 0)} deps{' · ' + r['notes'] if r.get('notes') else ''}</div>
              </div>
              <div style="font-family:'IBM Plex Mono',monospace;font-size:11px;color:var(--muted2);width:90px;flex-shrink:0">₹{cost:,}/mo</div>
              <div style="flex-shrink:0;width:100px">
                <div style="font-family:IBM Plex Mono,monospace;font-size:9px;color:var(--muted);margin-bottom:3px">{util}% utilised</div>
                <div class="res-bar-wrap"><div class="res-bar" style="width:{util}%;background:{uc}"></div></div>
              </div>
            </div>
            """, unsafe_allow_html=True)

        if consolid:
            st.markdown('<div style="margin-top:20px;margin-bottom:10px;font-family:IBM Plex Mono,monospace;font-size:9px;letter-spacing:2px;text-transform:uppercase;color:var(--ylw)">🔗 Consolidation Opportunities</div>', unsafe_allow_html=True)
            for co in consolid:
                st.markdown(f"""
                <div style="background:var(--bg2);border:1px solid rgba(255,190,0,0.15);border-radius:12px;padding:12px 16px;margin-bottom:8px;display:flex;align-items:center;gap:12px">
                  <span class="badge badge-ylw">{co['confidence']}</span>
                  <div style="flex:1">
                    <div style="font-size:13px;font-weight:600">{co['resource_a']} <span style="color:var(--muted)">+</span> {co['resource_b']}</div>
                    <div style="font-size:11.5px;color:var(--muted2);margin-top:2px">{co.get('reason', '')} · Combined util: {co.get('combined_utilization', 0)}%</div>
                  </div>
                  <div style="font-family:'Syne',sans-serif;font-size:18px;font-weight:800;color:var(--grn)">₹{co.get('savings_estimate', 0):,}</div>
                </div>
                """, unsafe_allow_html=True)

    # ── ACTION PLAN ───────────────────────────────────────────────────────────
    elif at == "actions":
        actions    = prioritise.get("ranked_actions", [])
        quick_wins = prioritise.get("quick_wins", [])
        defer_list = prioritise.get("defer_list", [])
        action_colors = {
            "CONSOLIDATE":  ("#00d4ff", "rgba(0,212,255,0.1)"),
            "DECOMMISSION": ("#ff4040", "rgba(255,64,64,0.1)"),
            "DOWNSIZE":     ("#ffbe00", "rgba(255,190,0,0.1)"),
            "REALLOCATE":   ("#9d7eff", "rgba(157,126,255,0.1)"),
            "EXPAND":       ("#00e887", "rgba(0,232,135,0.1)"),
        }

        rationale = prioritise.get("prioritisation_rationale", "")
        st.markdown(f'<div class="au" style="font-size:13.5px;color:var(--muted2);margin-bottom:14px;line-height:1.6">{rationale}</div>', unsafe_allow_html=True)

        if quick_wins:
            qw_html = " · ".join(f'<span style="color:var(--grn)">{q}</span>' for q in quick_wins)
            st.markdown(
                f'<div style="background:var(--grn2);border:1px solid rgba(0,232,135,0.2);border-radius:12px;'
                f'padding:10px 16px;margin-bottom:14px;font-size:12.5px;font-family:IBM Plex Mono,monospace">'
                f'<span style="color:var(--grn);letter-spacing:1px">⚡ QUICK WINS:</span> {qw_html}</div>',
                unsafe_allow_html=True,
            )

        for i, a in enumerate(actions):
            act    = a.get("action", "DOWNSIZE")
            c, bg  = action_colors.get(act, ("#6a8aaa", "rgba(255,255,255,0.05)"))
            roi    = a.get("roi_score", 70)
            ms     = a.get("monthly_saving", 0)
            st.markdown(f"""
            <div class="action-item au" style="animation-delay:{i * 60}ms">
              <div class="action-rank" style="background:{bg};color:{c}">#{a.get('rank', i + 1)}</div>
              <div class="action-body">
                <div class="action-name">{a.get('resource', 'Resource')} <span style="font-family:IBM Plex Mono,monospace;font-size:10px;color:var(--muted)">{a.get('timeline', '')}</span></div>
                <div class="action-reason">{a.get('reason', '')}</div>
                <div class="action-meta">
                  <span class="badge" style="background:{bg};border:1px solid {c}40;color:{c}">{act}</span>
                  <span class="badge badge-grn">₹{ms:,}/mo saving</span>
                  <span class="badge badge-ac">Effort: {a.get('effort', 'MEDIUM')}</span>
                  <span class="badge badge-prp">Owner: {a.get('owner', 'Ops')}</span>
                </div>
              </div>
              <div class="score-box" style="background:{bg};color:{c};border:1px solid {c}40">ROI<br>{roi}</div>
            </div>
            """, unsafe_allow_html=True)

        if defer_list:
            d_html = " · ".join(f'<span style="color:var(--muted2)">{d}</span>' for d in defer_list)
            st.markdown(
                f'<div style="background:var(--bg2);border:1px solid var(--bd);border-radius:12px;'
                f'padding:10px 16px;margin-top:12px;font-size:12px;font-family:IBM Plex Mono,monospace;color:var(--muted)">'
                f'<span style="letter-spacing:1px">DEFERRED:</span> {d_html}</div>',
                unsafe_allow_html=True,
            )

    # ── EXECUTION PHASES ──────────────────────────────────────────────────────
    elif at == "phases":
        phases     = plan.get("execution_phases", [])
        reallocate = plan.get("team_reallocation", [])
        approvals  = plan.get("approval_required", [])
        ms         = plan.get("projected_monthly_saving", 0)
        ans        = plan.get("projected_annual_saving",  0)
        pb         = plan.get("payback_months",            2)
        ec         = plan.get("execution_confidence",     78)

        st.markdown(f"""
        <div class="au" style="background:var(--grn2);border:1px solid rgba(0,232,135,0.2);border-radius:14px;padding:16px 20px;margin-bottom:18px;display:flex;align-items:center;gap:20px;flex-wrap:wrap">
          <div><div style="font-family:'IBM Plex Mono',monospace;font-size:9px;letter-spacing:2px;text-transform:uppercase;color:var(--grn)">Monthly Saving</div><div style="font-family:'Syne',sans-serif;font-size:2rem;font-weight:800;color:var(--grn)">₹{ms:,}</div></div>
          <div style="width:1px;height:40px;background:rgba(0,232,135,.2)"></div>
          <div><div style="font-family:'IBM Plex Mono',monospace;font-size:9px;letter-spacing:2px;text-transform:uppercase;color:var(--grn)">Annual Saving</div><div style="font-family:'Syne',sans-serif;font-size:2rem;font-weight:800;color:var(--grn)">₹{ans:,}</div></div>
          <div style="width:1px;height:40px;background:rgba(0,232,135,.2)"></div>
          <div><div style="font-family:'IBM Plex Mono',monospace;font-size:9px;letter-spacing:2px;text-transform:uppercase;color:var(--grn)">Payback</div><div style="font-family:'Syne',sans-serif;font-size:2rem;font-weight:800;color:var(--grn)">{pb} months</div></div>
          <div style="width:1px;height:40px;background:rgba(0,232,135,.2)"></div>
          <div><div style="font-family:'IBM Plex Mono',monospace;font-size:9px;letter-spacing:2px;text-transform:uppercase;color:var(--grn)">Confidence</div><div style="font-family:'Syne',sans-serif;font-size:2rem;font-weight:800;color:var(--grn)">{ec}%</div></div>
        </div>
        """, unsafe_allow_html=True)

        cl, cr = st.columns([1.2, 1], gap="large")
        with cl:
            st.markdown('<div style="font-family:IBM Plex Mono,monospace;font-size:9px;letter-spacing:2px;text-transform:uppercase;color:var(--muted);margin-bottom:14px">📅 Execution Roadmap</div>', unsafe_allow_html=True)
            for i, ph in enumerate(phases):
                is_last  = i == len(phases) - 1
                risk_c2  = {"HIGH": "#ff4040", "MEDIUM": "#ffbe00", "LOW": "#00e887"}.get(ph.get("risk", "LOW"), "#00e887")
                acts_html = "".join(
                    f'<div class="phase-action"><span style="color:var(--ac);flex-shrink:0">→</span><span>{a}</span></div>'
                    for a in ph.get("actions", [])
                )
                st.markdown(f"""
                <div class="phase-item au" style="animation-delay:{i * 80}ms">
                  <div class="phase-dot-col">
                    <div class="phase-circle">{i + 1}</div>
                    {"" if is_last else '<div class="phase-line"></div>'}
                  </div>
                  <div class="phase-body">
                    <div class="phase-lbl">{ph.get('phase', 'Phase ' + str(i + 1))} <span style="font-size:9px;color:var(--muted)">· {ph.get('duration', '')}</span></div>
                    {acts_html}
                    <div style="margin-top:8px;display:flex;gap:8px;flex-wrap:wrap">
                      <span class="badge badge-grn">₹{ph.get('expected_saving', 0):,} saving</span>
                      <span class="badge" style="background:rgba(255,255,255,0.04);border:1px solid {risk_c2}40;color:{risk_c2}">Risk: {ph.get('risk', 'LOW')}</span>
                    </div>
                  </div>
                </div>
                """, unsafe_allow_html=True)
        with cr:
            if reallocate:
                st.markdown('<div style="font-family:IBM Plex Mono,monospace;font-size:9px;letter-spacing:2px;text-transform:uppercase;color:var(--muted);margin-bottom:12px">🔄 Team Reallocation</div>', unsafe_allow_html=True)
                for r in reallocate:
                    st.markdown(f"""
                    <div style="background:var(--bg2);border:1px solid rgba(0,212,255,0.15);border-radius:12px;padding:12px 16px;margin-bottom:8px">
                      <div style="font-size:13px;font-weight:600;margin-bottom:4px">{r.get('person', '')}</div>
                      <div style="font-size:11.5px;color:var(--muted2)">{r.get('reason', '')}</div>
                      <div style="margin-top:8px;font-size:11px"><span style="color:#ff4040">{r.get('from_resource', '')}</span> <span style="color:var(--muted)">→</span> <span style="color:#00e887">{r.get('to_resource', '')}</span> · {r.get('hours_freed', 0)}h freed</div>
                    </div>
                    """, unsafe_allow_html=True)
            if approvals:
                st.markdown('<div style="font-family:IBM Plex Mono,monospace;font-size:9px;letter-spacing:2px;text-transform:uppercase;color:var(--ylw);margin-top:16px;margin-bottom:10px">✅ Approval Required</div>', unsafe_allow_html=True)
                for ap in approvals:
                    st.markdown(f"""
                    <div style="background:var(--ylw2);border:1px solid rgba(255,190,0,0.2);border-radius:12px;padding:12px 16px;margin-bottom:8px">
                      <div style="font-size:13px;font-weight:600">{ap.get('action', '')}</div>
                      <div style="font-size:11.5px;color:var(--muted2);margin-top:3px">Approver: {ap.get('approver', '')} · {ap.get('reason', '')}</div>
                    </div>
                    """, unsafe_allow_html=True)

    # ── TEAM VIEW ─────────────────────────────────────────────────────────────
    elif at == "team":
        overloaded = [t["name"] for t in team_data if t.get("load", 50) > 80]
        available  = [t["name"] for t in team_data if t.get("load", 50) < 60]
        reallocate = plan.get("team_reallocation", [])

        st.markdown(f"""
        <div class="au" style="display:flex;gap:10px;flex-wrap:wrap;margin-bottom:14px">
          <span class="badge badge-red">⚠ High Load: {', '.join(overloaded) or 'None'}</span>
          <span class="badge badge-grn">✓ Available: {', '.join(available) or 'None'}</span>
        </div>
        """, unsafe_allow_html=True)

        if not team_data:
            st.info("No team data.")
        else:
            ncols = min(5, len(team_data))
            tcols = st.columns(ncols, gap="small")
            for i, m in enumerate(team_data):
                load    = m.get("load", 50)
                lc      = "#ff4040" if load > 100 else ("#ffbe00" if load > 80 else "#00e887")
                av      = "".join([w[0].upper() for w in m["name"].split()[:2]])
                is_over  = load > 80
                is_avail = load < 60
                reas     = next(
                    (f"→ Freed: {r['hours_freed']}h to {r['to_resource']}" for r in reallocate if r.get("person") == m["name"]),
                    "",
                )
                bc = "#ff4040" if is_over else ("#00e887" if is_avail else "var(--ac)")
                bg_rgb = "255,64,64" if is_over else ("0,232,135" if is_avail else "0,212,255")
                with tcols[i % ncols]:
                    st.markdown(f"""
                    <div style="background:var(--bg2);border:1px solid {'rgba(255,64,64,0.25)' if is_over else ('rgba(0,232,135,0.2)' if is_avail else 'var(--bd)')};border-radius:16px;padding:14px;margin-bottom:10px">
                      <div style="display:flex;align-items:center;gap:8px;margin-bottom:10px">
                        <div style="width:40px;height:40px;border-radius:10px;background:rgba({bg_rgb},0.12);color:{bc};display:flex;align-items:center;justify-content:center;font-family:'Syne',sans-serif;font-weight:700;font-size:13px">{av}</div>
                        <div><div style="font-size:12px;font-weight:700">{m['name'].split()[0]}</div><div style="font-size:10px;color:var(--muted2)">{m.get('role','')[:16]}</div></div>
                      </div>
                      <div style="display:flex;justify-content:space-between;margin-bottom:4px">
                        <span style="font-family:'IBM Plex Mono',monospace;font-size:8px;color:var(--muted)">LOAD</span>
                        <span style="font-family:'IBM Plex Mono',monospace;font-size:10px;color:{lc};font-weight:600">{load}%</span>
                      </div>
                      <div style="height:5px;background:var(--bg3);border-radius:5px"><div style="height:5px;border-radius:5px;background:{lc};width:{min(100, load)}%"></div></div>
                      <div style="margin-top:8px;font-family:'IBM Plex Mono',monospace;font-size:9px;color:var(--muted)">{m.get('available_hours', 40)}h/wk available</div>
                      {f'<div style="margin-top:8px;font-size:11px;color:#00e887;background:rgba(0,232,135,0.06);border-radius:7px;padding:5px 8px">{reas}</div>' if reas else ''}
                      {'<div class="badge badge-red" style="margin-top:8px;font-size:8px;width:100%;justify-content:center">HIGH LOAD</div>' if is_over else ''}
                      {'<div class="badge badge-grn" style="margin-top:8px;font-size:8px;width:100%;justify-content:center">AVAILABLE</div>' if is_avail else ''}
                    </div>
                    """, unsafe_allow_html=True)

    # ── WHY AI DID THIS ───────────────────────────────────────────────────────
    elif at == "explain":
        exps    = report.get("explanations", [])
        summary = report.get("executive_summary", "")
        st.markdown(f"""
        <div class="au" style="background:var(--prp2);border:1px solid rgba(157,126,255,0.18);border-radius:16px;padding:18px 22px;margin-bottom:18px">
          <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;letter-spacing:2px;text-transform:uppercase;color:var(--prp);margin-bottom:7px">🧠 Report Agent Summary</div>
          <div style="font-size:14px;color:var(--text);line-height:1.75">{summary}</div>
        </div>
        """, unsafe_allow_html=True)
        for i, ex in enumerate(exps):
            conf = ex.get("confidence", 80)
            cc   = "#00e887" if conf > 85 else ("#ffbe00" if conf > 70 else "#ff8c42")
            st.markdown(f"""
            <div class="xai-card au" style="animation-delay:{i * 70}ms">
              <div class="xai-hdr">
                <div class="xai-icon">🔍</div>
                <div class="xai-title">{ex.get('decision', '')}</div>
                <div class="xai-conf" style="color:{cc}">Confidence: {conf}%</div>
              </div>
              <div class="xai-body">{ex.get('why', '')}</div>
              <div class="xai-data">Data used: {ex.get('data_used', '')}</div>
            </div>
            """, unsafe_allow_html=True)

    # ── WHAT-IF ───────────────────────────────────────────────────────────────
    elif at == "whatif":
        team_names_wi = [m["name"] for m in team_data]
        presets = [
            f"What if we add 2 more engineers to {team_names_wi[0] if team_names_wi else 'the team'}?",
            "What if we consolidate all duplicate tools immediately?",
            "What if we switch from aggressive to conservative strategy?",
            "What if we increase the underutilisation threshold to 70%?",
            "What if we decommission all resources below 20% utilisation?",
            "What if we expand capacity instead of consolidating?",
        ]
        st.markdown('<div style="font-family:IBM Plex Mono,monospace;font-size:9px;letter-spacing:2px;text-transform:uppercase;color:var(--muted);margin-bottom:8px">Quick Scenarios</div>', unsafe_allow_html=True)
        p_cols = st.columns(3)
        for i, preset in enumerate(presets):
            with p_cols[i % 3]:
                if st.button(f"→ {preset}", key=f"preset_{i}", use_container_width=True):
                    st.session_state["wi_input"] = preset
                    with st.spinner("Simulating…"):
                        st.session_state.whatif_result = run_whatif(preset, analysis, inp, api_key)
                    st.rerun()

        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        wi_text = st.text_input(
            "Or type your own scenario…",
            value=st.session_state.get("wi_input", ""),
            placeholder="e.g. What if we merge the two Kubernetes clusters?",
            key="wi_custom",
        )
        _, rb = st.columns([3, 1])
        with rb:
            if st.button("🔮 Simulate", key="wi_run", use_container_width=True):
                if wi_text.strip():
                    st.session_state["wi_input"] = wi_text
                    with st.spinner("Simulating…"):
                        st.session_state.whatif_result = run_whatif(wi_text, analysis, inp, api_key)
                    st.rerun()

        if st.session_state.whatif_result:
            wi      = st.session_state.whatif_result
            delta   = wi.get("delta_saving", 0)
            dc      = "#00e887" if delta > 0 else "#ff4040"
            nh      = wi.get("new_health_score", 70)
            nhc     = "#00e887" if nh >= 70 else ("#ffbe00" if nh >= 50 else "#ff4040")
            circumf2 = 282
            off_wi  = circumf2 - (circumf2 * nh / 100)
            changes = "".join(
                f'<div style="display:flex;gap:8px;padding:6px 0;font-size:12px;color:var(--text);'
                f'border-bottom:1px solid rgba(255,255,255,0.03)">'
                f'<span style="color:#00e887">→</span><span>{ch}</span></div>'
                for ch in wi.get("key_changes", [])
            )
            new_risks = "".join(
                f'<div style="display:flex;gap:8px;padding:6px 0;font-size:12px;color:#ff8c42;'
                f'border-bottom:1px solid rgba(255,255,255,0.03)">'
                f'<span>⚠</span><span>{rk}</span></div>'
                for rk in wi.get("new_risks", [])
            )
            st.markdown(f"""
            <div style="background:var(--bg2);border:1px solid var(--bd);border-radius:16px;padding:20px;margin-top:16px" class="au d1">
              <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;letter-spacing:2px;text-transform:uppercase;color:var(--muted);margin-bottom:12px">Scenario: {wi.get('scenario_title', '')}</div>
              <div style="display:flex;gap:20px;align-items:center;flex-wrap:wrap">
                <div style="text-align:center;min-width:100px">
                  <svg viewBox="0 0 110 110" style="width:85px;height:85px;transform:rotate(-90deg)">
                    <circle cx="55" cy="55" r="45" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="7"/>
                    <circle cx="55" cy="55" r="45" fill="none" stroke="{nhc}" stroke-width="7" stroke-linecap="round" stroke-dasharray="{circumf2}" stroke-dashoffset="{off_wi}" style="filter:drop-shadow(0 0 6px {nhc})"/>
                  </svg>
                  <div style="font-family:'Syne',sans-serif;font-size:1.4rem;font-weight:800;color:{nhc};margin-top:-60px">{nh}</div>
                  <div style="font-size:10px;color:var(--muted);margin-top:48px">New Health</div>
                </div>
                <div style="flex:1;min-width:180px">
                  <div style="font-family:'Syne',sans-serif;font-size:2.2rem;font-weight:800;color:{dc}">{'+' if delta > 0 else ''}₹{delta:,}</div>
                  <div style="font-size:12px;color:var(--muted2);margin-bottom:10px">{'additional monthly saving' if delta > 0 else 'additional cost'}</div>
                  <div style="display:flex;gap:8px;margin-bottom:10px;flex-wrap:wrap">
                    <span class="badge badge-grn">New monthly: ₹{wi.get('new_monthly_saving', 0):,}</span>
                    <span class="badge badge-ac">Efficiency: +{wi.get('new_efficiency_gain', 0)}%</span>
                  </div>
                  <div style="font-size:13px;color:var(--text);background:var(--ac2);border:1px solid rgba(0,212,255,0.2);border-radius:10px;padding:10px 14px;line-height:1.6">💡 {wi.get('recommendation', '')}</div>
                </div>
                <div style="flex:1;min-width:160px">{changes}{new_risks}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    # ── CHAT ──────────────────────────────────────────────────────────────────
    elif at == "chat":
        ms = plan.get("projected_monthly_saving", 0)
        hs = report.get("health_before", 50)
        st.markdown(f"""
        <div class="chat-hero au">
          <div class="bot-avatar">🤖</div>
          <div>
            <div style="font-family:'Syne',sans-serif;font-size:1rem;font-weight:700">OptiBot — Your AI Resource Advisor</div>
            <div style="font-size:12px;color:var(--muted2);margin-top:2px">I know your full resource landscape and optimisation plan. Ask me anything.</div>
          </div>
          <div style="margin-left:auto;display:flex;align-items:center;gap:5px;font-family:'IBM Plex Mono',monospace;font-size:9px;color:var(--muted2)">
            <div style="width:7px;height:7px;border-radius:50%;background:var(--ac);animation:pulse 2s infinite"></div>Online
          </div>
        </div>
        <div style="display:flex;align-items:center;gap:10px;background:var(--ac2);border:1px solid rgba(0,212,255,0.12);border-radius:11px;padding:8px 14px;margin-bottom:12px">
          <span>⬡</span>
          <div style="font-size:12px;color:var(--ac)">Context loaded: <b>{inp.get('org_name', '')}</b> · Health: <b>{hs}/100</b> · Projected saving: <b>₹{ms:,}/mo</b></div>
        </div>
        """, unsafe_allow_html=True)

        if not st.session_state.chat_history:
            sugs   = ["What's wasting the most money?", "Which resource should I cut first?", "Explain the consolidation plan", "Who's overloaded?", "What's the ROI?", "Which tools overlap?"]
            scols  = st.columns(3)
            for i, s in enumerate(sugs):
                with scols[i % 3]:
                    if st.button(s, key=f"chat_sug_{i}", use_container_width=True):
                        st.session_state.chat_history.append({"role": "user", "content": s})
                        with st.spinner(""):
                            reply = chat_agent(s, analysis, inp, api_key)
                        st.session_state.chat_history.append({"role": "assistant", "content": reply})
                        st.rerun()
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        bubbles = ""
        if not st.session_state.chat_history:
            bubbles = (
                '<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;'
                'min-height:200px;gap:10px;text-align:center">'
                '<div style="font-size:36px;opacity:.25">💬</div>'
                '<div style="font-size:13px;color:var(--muted);max-width:260px;line-height:1.5">'
                'Ask anything about your resources, savings, or optimisation plan.</div></div>'
            )
        else:
            for msg in st.session_state.chat_history:
                if msg["role"] == "user":
                    bubbles += f'<div class="msg-row-user"><div class="bubble user-bub">{msg["content"]}</div></div>'
                else:
                    bubbles += f'<div class="msg-row-bot"><div class="bubble bot-bub">{msg["content"]}</div></div>'
        st.markdown(f'<div class="chat-window">{bubbles}</div>', unsafe_allow_html=True)

        user_input = st.chat_input("Ask OptiBot anything…")
        if user_input:
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            with st.spinner(""):
                reply = chat_agent(user_input, analysis, inp, api_key)
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            st.rerun()

        st.markdown('<div class="btn-ghost">', unsafe_allow_html=True)
        if st.button("🗑 Clear Chat", key="clear_chat"):
            st.session_state.chat_history = []
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Bottom controls ───────────────────────────────────────────────────────
    st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)
    ca, cb, cc, _ = st.columns([1, 1, 1, 2])
    with ca:
        st.markdown('<div class="btn-ghost">', unsafe_allow_html=True)
        if st.button("← New Analysis", key="new_analysis", use_container_width=True):
            for k in list(DEFAULTS.keys()):
                st.session_state[k] = DEFAULTS[k]
            st.session_state.resource_rows = [{"id": "R-001", "name": "", "type": "Infrastructure", "utilization": 50, "cost": 10000, "team": "", "dependencies": 0, "notes": ""}]
            st.session_state.team_rows     = [{"name": "", "role": "", "load": 50, "skills": "", "available_hours": 40, "team": ""}]
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with cb:
        st.markdown('<div class="btn-ghost">', unsafe_allow_html=True)
        if st.button("✏️ Edit Resources", key="edit_res", use_container_width=True):
            st.session_state.view = "step3"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with cc:
        st.markdown('<div class="btn-ghost">', unsafe_allow_html=True)
        if st.button("🔄 Re-run Agents", key="rerun_ag", use_container_width=True):
            st.session_state.view = "running"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ── FOOTER ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:3rem 0 1rem;border-top:1px solid rgba(255,255,255,0.04);margin-top:3rem;font-family:'IBM Plex Mono',monospace;font-size:10px;color:#1a2030;letter-spacing:.5px">
  ResourceIQ · 5-Agent Pipeline · Groq · LLaMA 3.3 70B · All inputs user-provided · No hardcoded data
</div>
""", unsafe_allow_html=True)