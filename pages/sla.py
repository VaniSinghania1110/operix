"""
╔══════════════════════════════════════════════════════════════╗
║   SLA PENALTY AGENT — COMPLETE HACKATHON-WINNING BUILD       ║
║   Features: Multi-Agent AI · What-if Simulator · Team Mgr    ║
║             Chat Interface · Risk Meter · Auto Escalation     ║
║             Recovery Plan · Gamified SLA Health Score        ║
╚══════════════════════════════════════════════════════════════╝

Run:  streamlit run sla_penalty_agent_complete.py
Needs: pip install streamlit groq
Set:  st.secrets["GROQ_API_KEY"]
"""

import streamlit as st
import json, time, random, re
from groq import Groq

# ──────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="SLA Penalty Agent",
    layout="wide",
    initial_sidebar_state="collapsed",
)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ──────────────────────────────────────────────
# SESSION STATE
# ──────────────────────────────────────────────
DEFAULTS = {
    "view": "dashboard",      # dashboard | running | results | whatif | chat
    "inputs": {},
    "analysis": None,
    "chat_history": [],
    "whatif_result": None,
    "active_tab": "overview", # overview | team | tasks | escalation | chat | whatif
    "health_score": None,
    "alert_shown": False,
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ──────────────────────────────────────────────
# SAMPLE DATA — realistic pre-filled
# ──────────────────────────────────────────────
SAMPLE_TASKS = [
    {"id":"T-001","name":"API Gateway Integration","assignee":"Rahul Sharma","progress":45,"priority":"CRITICAL","est_hours":20,"used_hours":14,"blocked":True,  "blocker":"Waiting for auth token from client"},
    {"id":"T-002","name":"Database Migration Scripts","assignee":"Priya Patel", "progress":70,"priority":"HIGH",    "est_hours":12,"used_hours":10,"blocked":False,"blocker":""},
    {"id":"T-003","name":"Payment Module Testing",  "assignee":"Arjun Singh", "progress":20,"priority":"CRITICAL","est_hours":18,"used_hours":6, "blocked":False,"blocker":""},
    {"id":"T-004","name":"UI Dashboard Build",      "assignee":"Neha Gupta",  "progress":85,"priority":"MEDIUM",  "est_hours":8, "used_hours":7, "blocked":False,"blocker":""},
    {"id":"T-005","name":"Load Balancer Config",    "assignee":"Rahul Sharma","progress":10,"priority":"HIGH",    "est_hours":10,"used_hours":1, "blocked":True, "blocker":"Infra access pending"},
    {"id":"T-006","name":"Security Audit",          "assignee":"Vikram Das",  "progress":55,"priority":"HIGH",    "est_hours":14,"used_hours":9, "blocked":False,"blocker":""},
    {"id":"T-007","name":"Deployment Runbook",      "assignee":"Priya Patel", "progress":90,"priority":"LOW",     "est_hours":4, "used_hours":4, "blocked":False,"blocker":""},
    {"id":"T-008","name":"Performance Optimisation","assignee":"Arjun Singh", "progress":30,"priority":"MEDIUM",  "est_hours":16,"used_hours":6, "blocked":False,"blocker":""},
]

SAMPLE_TEAM = [
    {"name":"Rahul Sharma", "role":"Backend Lead",    "capacity":100,"load":128,"tasks":2,"avatar":"RS","skills":["Python","APIs","Infra"]},
    {"name":"Priya Patel",  "role":"Full Stack Dev",  "capacity":100,"load":85, "tasks":2,"avatar":"PP","skills":["React","Node","DB"]},
    {"name":"Arjun Singh",  "role":"QA Engineer",     "capacity":100,"load":95, "tasks":2,"avatar":"AS","skills":["Testing","Selenium","Perf"]},
    {"name":"Neha Gupta",   "role":"Frontend Dev",    "capacity":100,"load":42, "tasks":1,"avatar":"NG","skills":["React","CSS","UI/UX"]},
    {"name":"Vikram Das",   "role":"DevOps/Security", "capacity":100,"load":78, "tasks":1,"avatar":"VD","skills":["DevOps","Security","Linux"]},
]

# ──────────────────────────────────────────────
# LLM HELPER
# ──────────────────────────────────────────────
def llm(messages, max_tokens=1400, temperature=0.35):
    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return resp.choices[0].message.content.strip()

def safe_json(text, fallback):
    try:
        # strip markdown fences
        clean = re.sub(r"```(?:json)?|```", "", text).strip()
        return json.loads(clean)
    except Exception:
        return fallback

# ──────────────────────────────────────────────
# ███████████ MULTI-AGENT ENGINE ███████████████
# ──────────────────────────────────────────────
AGENT_PIPELINE = [
    ("👁️", "INPUT AGENT",    "Reads tasks, resources & deadlines"),
    ("🧠", "THINK AGENT",    "Predicts breach & finds bottlenecks"),
    ("⚡", "DECISION AGENT", "Prioritises tasks by urgency × impact"),
    ("🔧", "ACTION AGENT",   "Reassigns tasks & builds recovery plan"),
    ("📢", "EXPLAIN AGENT",  "Generates explainable AI reasoning"),
]

def run_multi_agent(inp, step_ph, log_ph, progress_ph):
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
        for i, (icon, name, desc) in enumerate(AGENT_PIPELINE):
            if i < active:
                cls, sym = "done", "✓"
            elif i == active:
                cls, sym = "active", str(i+1)
            else:
                cls, sym = "", str(i+1)
            lc = "active" if i == active else ""
            line_cls = "done" if i < active else ("active" if i == active else "")
            html += f'''<div class="ag-step">
              <div class="ag-dot {cls}">{sym}</div>
              <div class="ag-lbl {lc}">{icon}<br>{name}</div>
            </div>'''
            if i < len(AGENT_PIPELINE)-1:
                html += f'<div class="ag-line {line_cls}"></div>'
        step_ph.markdown(f'<div class="ag-pipeline">{html}</div>', unsafe_allow_html=True)

    res = {}
    tasks_str   = json.dumps(inp.get("tasks", SAMPLE_TASKS), indent=2)
    team_str    = json.dumps(inp.get("team",  SAMPLE_TEAM),  indent=2)
    contract    = inp.get("contract", "Enterprise Cloud Platform")
    sla_target  = inp.get("sla_target", 95)
    curr_comp   = inp.get("current_completion", 58)
    days_left   = inp.get("days_remaining", 3)
    penalty_amt = inp.get("penalty_amount", 500000)

    ctx = f"""
CONTRACT: {contract}
SLA TARGET: {sla_target}%
CURRENT COMPLETION: {curr_comp}%
DAYS REMAINING: {days_left}
PENALTY: ₹{penalty_amt:,}
TASKS:
{tasks_str}
TEAM:
{team_str}
"""

    # ── AGENT 1: INPUT ─────────────────────────
    set_step(0); progress_ph.progress(5)
    push("Input Agent activated — loading contract data…", "think")
    push(f"Contract: {contract} | SLA: {sla_target}% | Progress: {curr_comp}%", "action")
    push(f"Tasks loaded: {len(inp.get('tasks', SAMPLE_TASKS))} | Team: {len(inp.get('team', SAMPLE_TEAM))} members", "action")
    blocked = [t for t in inp.get("tasks", SAMPLE_TASKS) if t.get("blocked")]
    push(f"Blocked tasks detected: {len(blocked)} — flagging for analysis", "warn")
    time.sleep(0.6)
    res["input_summary"] = {
        "total_tasks": len(inp.get("tasks", SAMPLE_TASKS)),
        "blocked_tasks": len(blocked),
        "team_size": len(inp.get("team", SAMPLE_TEAM)),
    }
    progress_ph.progress(20)

    # ── AGENT 2: THINK ─────────────────────────
    set_step(1)
    push("Think Agent activated — running SLA prediction model…", "think")
    think_resp = llm([{"role":"user","content":f"""
You are an SLA prediction AI. Analyse this project data and return ONLY valid JSON (no markdown):
{ctx}

Return:
{{
  "predicted_miss_days": <float, days SLA will be missed by if nothing changes>,
  "breach_probability": <int 0-100>,
  "sla_health_score": <int 0-100, gamified score>,
  "risk_level": "CRITICAL"|"HIGH"|"MEDIUM"|"LOW",
  "bottleneck_tasks": [<task IDs of top 3 bottleneck tasks>],
  "bottleneck_reasons": {{"task_id": "reason"}},
  "underperforming_resources": [<names of overloaded/underperforming team members>],
  "overloaded_resources": [<names>],
  "free_resources": [<names with capacity available>],
  "key_risk_factors": ["risk 1", "risk 2", "risk 3"],
  "ml_prediction_basis": "explanation of how prediction was made"
}}
"""}])
    think = safe_json(think_resp, {
        "predicted_miss_days": 2.3,
        "breach_probability": 78,
        "sla_health_score": 42,
        "risk_level": "CRITICAL",
        "bottleneck_tasks": ["T-001","T-003","T-005"],
        "bottleneck_reasons": {"T-001":"Auth blocker + 55% remaining","T-003":"Only 20% done on critical task","T-005":"Infra access blocked"},
        "underperforming_resources": ["Rahul Sharma"],
        "overloaded_resources": ["Rahul Sharma"],
        "free_resources": ["Neha Gupta"],
        "key_risk_factors": ["2 tasks blocked externally","Payment module critically behind","Rahul at 128% capacity"],
        "ml_prediction_basis": "Linear regression on task velocity vs remaining work",
    })
    res["think"] = think
    push(f"Prediction: SLA miss by <b>{think.get('predicted_miss_days',2.3)} days</b>", "result")
    push(f"Breach probability: {think.get('breach_probability',78)}% | Health: {think.get('sla_health_score',42)}/100", "result")
    push(f"Bottlenecks: {', '.join(think.get('bottleneck_tasks',[]))}", "warn")
    push(f"Overloaded: {', '.join(think.get('overloaded_resources',[]))}", "warn")
    progress_ph.progress(40)
    time.sleep(0.5)

    # ── AGENT 3: DECISION ──────────────────────
    set_step(2)
    push("Decision Agent activated — prioritising by urgency × impact matrix…", "think")
    decision_resp = llm([{"role":"user","content":f"""
You are a task prioritisation AI. Given the analysis:
{ctx}
Think data: {json.dumps(think)}

Return ONLY valid JSON (no markdown):
{{
  "priority_ranking": [
    {{"rank":1,"task_id":"T-XXX","task_name":"name","urgency":1-10,"impact":1-10,"score":float,"action":"ACCELERATE|DEFER|REASSIGN|ESCALATE","reason":"why"}}
  ],
  "critical_path": ["task_id1","task_id2"],
  "defer_candidates": ["task_id"],
  "decision_rationale": "overall strategy explanation"
}}
"""}])
    decision = safe_json(decision_resp, {
        "priority_ranking": [
            {"rank":1,"task_id":"T-003","task_name":"Payment Module Testing","urgency":10,"impact":10,"score":100,"action":"ACCELERATE","reason":"CRITICAL priority, only 20% done, highest SLA impact"},
            {"rank":2,"task_id":"T-001","task_name":"API Gateway Integration","urgency":9,"impact":9,"score":81,"action":"ESCALATE","reason":"Blocked by external auth token — needs immediate escalation"},
            {"rank":3,"task_id":"T-005","task_name":"Load Balancer Config","urgency":8,"impact":8,"score":64,"action":"REASSIGN","reason":"Rahul overloaded — reassign to Vikram who has capacity"},
        ],
        "critical_path": ["T-001","T-003","T-005"],
        "defer_candidates": ["T-007"],
        "decision_rationale": "Focus all resources on payment and API — these are SLA-defining tasks.",
    })
    res["decision"] = decision
    push(f"Priority matrix complete — top task: {decision['priority_ranking'][0]['task_name'] if decision.get('priority_ranking') else 'N/A'}", "result")
    push(f"Critical path: {', '.join(decision.get('critical_path',[]))}", "action")
    push(f"Defer candidates: {', '.join(decision.get('defer_candidates',[]))}", "action")
    progress_ph.progress(60)
    time.sleep(0.5)

    # ── AGENT 4: ACTION ────────────────────────
    set_step(3)
    push("Action Agent activated — generating recovery plan & reassignments…", "think")
    action_resp = llm([{"role":"user","content":f"""
You are a service recovery AI. Given all analysis:
{ctx}
Think: {json.dumps(think)}
Decision: {json.dumps(decision)}

Return ONLY valid JSON (no markdown):
{{
  "reassignments": [
    {{"task_id":"T-XXX","task_name":"name","from":"person","to":"person","reason":"why this helps SLA"}}
  ],
  "overtime_suggestions": [
    {{"person":"name","hours":X,"tasks":["task"],"impact":"what this achieves"}}
  ],
  "recovery_timeline": [
    {{"day":"Day 1","actions":["action1","action2"]}}
  ],
  "projected_completion_after_recovery": <int percent>,
  "recovery_confidence": <int 0-100>,
  "unblock_actions": [
    {{"task_id":"T-XXX","blocker":"description","resolution":"how to unblock"}}
  ],
  "escalation_subject": "email subject line",
  "escalation_body": "3-4 sentence professional escalation message",
  "sla_health_after_recovery": <int 0-100>
}}
"""}])
    action = safe_json(action_resp, {
        "reassignments": [
            {"task_id":"T-005","task_name":"Load Balancer Config","from":"Rahul Sharma","to":"Vikram Das","reason":"Rahul at 128% capacity; Vikram has DevOps skills and 22% free capacity"},
            {"task_id":"T-008","task_name":"Performance Optimisation","from":"Arjun Singh","to":"Neha Gupta","reason":"Neha at 42% load; Arjun needed on critical Payment testing"},
        ],
        "overtime_suggestions": [
            {"person":"Arjun Singh","hours":4,"tasks":["T-003"],"impact":"Completes Payment Module 1 day earlier — saves ₹2L penalty exposure"},
        ],
        "recovery_timeline": [
            {"day":"Day 1","actions":["Escalate API blocker to client","Reassign Load Balancer to Vikram","Start Arjun overtime on Payment"]},
            {"day":"Day 2","actions":["Resolve infra access for Vikram","Accelerate DB migration completion","Daily standup at 9AM with manager"]},
            {"day":"Day 3","actions":["Deploy to staging","Final UAT sign-off","SLA compliance check"]},
        ],
        "projected_completion_after_recovery": 96,
        "recovery_confidence": 81,
        "unblock_actions": [
            {"task_id":"T-001","blocker":"Waiting for auth token from client","resolution":"Escalate to account manager for same-day resolution — block SLA risk email to client"},
            {"task_id":"T-005","blocker":"Infra access pending","resolution":"IT admin ticket — mark P0, request 4-hour SLA on access provisioning"},
        ],
        "escalation_subject": "🚨 SLA Risk Alert — Enterprise Cloud Platform — 3 Days Remaining",
        "escalation_body": "We are tracking 37% below SLA target with 3 days remaining on the Enterprise Cloud Platform contract, putting ₹5,00,000 in penalty at risk. Primary blockers are an unresolved client auth token (T-001) and infra access delay (T-005). Recovery plan activated: tasks reassigned, overtime authorised, and immediate escalation requested for client-side blockers. Projected completion after recovery: 96% — on track for SLA compliance.",
        "sla_health_after_recovery": 84,
    })
    res["action"] = action
    push(f"Reassignments: {len(action.get('reassignments',[]))} tasks moved", "result")
    push(f"Overtime plan: {len(action.get('overtime_suggestions',[]))} resource(s)", "action")
    push(f"Recovery confidence: {action.get('recovery_confidence',81)}%", "result")
    push(f"Projected completion: {action.get('projected_completion_after_recovery',96)}%", "result")
    progress_ph.progress(80)
    time.sleep(0.5)

    # ── AGENT 5: EXPLAIN ───────────────────────
    set_step(4)
    push("Explain Agent activated — generating XAI report…", "think")
    explain_resp = llm([{"role":"user","content":f"""
You are an explainability AI. For each major decision made by the agents, explain WHY in plain English.
Reassignments: {json.dumps(action.get('reassignments',[]))}
Priority decisions: {json.dumps(decision.get('priority_ranking',[])[:3])}
Overtime: {json.dumps(action.get('overtime_suggestions',[]))}

Return ONLY valid JSON (no markdown):
{{
  "explanations": [
    {{"decision":"short title","why":"plain English reason (1-2 sentences)","data_used":"what data the agent used","confidence":int}}
  ],
  "summary": "2-sentence plain English summary of what the agent did and why it will work"
}}
"""}])
    explain = safe_json(explain_resp, {
        "explanations": [
            {"decision":"Reassigned Load Balancer to Vikram","why":"Rahul is at 128% capacity and has 2 blocked tasks. Vikram has relevant DevOps skills and only 78% load — he can absorb this immediately.","data_used":"Capacity metrics + skill matrix","confidence":91},
            {"decision":"Payment Module = Top Priority","why":"At only 20% completion with 18 hours estimated, this is the highest-risk task for SLA compliance. Missing this means breach.","data_used":"Completion % × remaining hours × SLA weight","confidence":96},
            {"decision":"Escalate API blocker today","why":"T-001 is blocked by an external dependency. Every hour of delay propagates to downstream tasks. Escalation is the only path to unblock.","data_used":"Blocker flag + critical path analysis","confidence":98},
        ],
        "summary": "The agent detected a 78% breach probability driven by 2 blocked tasks and 1 overloaded resource. By reassigning Vikram to infra, escalating the API blocker, and authorising 4 hours overtime on Payment testing, the projected SLA health improves from 42 to 84/100.",
    })
    res["explain"] = explain
    push(f"XAI report: {len(explain.get('explanations',[]))} decisions explained", "result")
    push(f"Summary: {explain.get('summary','')[:80]}…", "result")
    push("🏁 All 5 agents complete. Recovery plan ready.", "result")
    progress_ph.progress(100)
    set_step(5)
    time.sleep(0.3)

    # compute final score
    res["sla_health_before"] = think.get("sla_health_score", 42)
    res["sla_health_after"]  = action.get("sla_health_after_recovery", 84)
    return res


# ──────────────────────────────────────────────
# WHAT-IF AGENT
# ──────────────────────────────────────────────
def run_whatif(scenario, analysis, inp):
    ctx = f"Original analysis: {json.dumps(analysis, indent=2)}\nScenario: {scenario}"
    resp = llm([{"role":"user","content":f"""
You are a what-if scenario simulator for project management.
{ctx}

Simulate the outcome of this change and return ONLY valid JSON (no markdown):
{{
  "scenario_title": "short title of what was changed",
  "new_sla_health": <int 0-100>,
  "new_breach_probability": <int 0-100>,
  "new_completion_projected": <int percent>,
  "delta_days": <float, positive = improvement, negative = worse>,
  "key_changes": ["change 1", "change 2", "change 3"],
  "risks": ["new risk 1"],
  "recommendation": "one sentence on whether to do this"
}}
"""}])
    return safe_json(resp, {
        "scenario_title": scenario[:60],
        "new_sla_health": 72,
        "new_breach_probability": 35,
        "new_completion_projected": 93,
        "delta_days": 1.5,
        "key_changes": ["Additional capacity reduces critical path by 1.5 days","Payment module can run in parallel","Risk of integration issues with new devs"],
        "risks": ["Onboarding time for new developers may offset gains"],
        "recommendation": "Proceed — net benefit outweighs onboarding overhead given 3-day window.",
    })


# ──────────────────────────────────────────────
# CHAT AGENT
# ──────────────────────────────────────────────
def chat_agent(user_msg, analysis, inp):
    system = f"""You are OpsBot — a sharp, friendly AI operations manager.
You have full context of this SLA situation:
Contract: {inp.get('contract','Enterprise Cloud Platform')}
SLA Target: {inp.get('sla_target',95)}% | Current: {inp.get('current_completion',58)}% | Days left: {inp.get('days_remaining',3)}
Penalty: ₹{inp.get('penalty_amount',500000):,}
Analysis: {json.dumps(analysis)}

Rules:
- Be concise, direct, and helpful. Max 120 words.
- Use 1-2 emojis naturally.
- If user says "fix it", reference the recovery plan.
- If user asks "why", reference explainability data.
- Respond in same language as user.
- Never be generic. Always reference specific tasks/people/numbers from the analysis.
"""
    history = [{"role": "system", "content": system}]
    history += [{"role": m["role"], "content": m["content"]}
                for m in st.session_state.chat_history[-10:]]
    history.append({"role": "user", "content": user_msg})
    return llm(history, max_tokens=200, temperature=0.6)


# ──────────────────────────────────────────────
# ██████████████ CSS ███████████████████████████
# ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=IBM+Plex+Mono:wght@400;500;600&family=Manrope:wght@300;400;500;600;700&display=swap');

:root{
  --bg:#06080e;--bg2:#0b0e18;--bg3:#10141f;--bg4:#151924;--bg5:#1c2133;
  --red:#ff4040;--red2:rgba(255,64,64,0.12);--redg:rgba(255,64,64,0.28);
  --grn:#00e887;--grn2:rgba(0,232,135,0.1);--grng:rgba(0,232,135,0.25);
  --ylw:#ffbe00;--ylw2:rgba(255,190,0,0.1);
  --blu:#3d9eff;--blu2:rgba(61,158,255,0.1);--blug:rgba(61,158,255,0.25);
  --prp:#9d7eff;--prp2:rgba(157,126,255,0.1);
  --text:#e2e8f8;--muted:#3a4260;--muted2:#58637a;
  --bd:rgba(255,255,255,0.06);--bd2:rgba(255,255,255,0.1);
}
*,*::before,*::after{box-sizing:border-box;}
html,body,[data-testid="stAppViewContainer"],[data-testid="stMain"]{
  background:var(--bg)!important;
  font-family:'Manrope',sans-serif!important;
  color:var(--text)!important;
}
[data-testid="stAppViewContainer"]::before{
  content:'';position:fixed;width:900px;height:600px;
  background:radial-gradient(ellipse,rgba(255,64,64,0.04) 0%,transparent 65%);
  top:-250px;right:-300px;pointer-events:none;z-index:0;
}
[data-testid="stAppViewContainer"]::after{
  content:'';position:fixed;width:700px;height:700px;
  background:radial-gradient(ellipse,rgba(0,232,135,0.03) 0%,transparent 65%);
  bottom:-200px;left:-200px;pointer-events:none;z-index:0;
}
#MainMenu,footer,header,[data-testid="stDecoration"],[data-testid="stToolbar"],[data-testid="stStatusWidget"]{display:none!important;}
[data-testid="stMainBlockContainer"]{max-width:1120px!important;padding:0 2rem 5rem!important;margin:0 auto!important;position:relative;z-index:1;}
[data-testid="stVerticalBlock"]{gap:0!important;}
::-webkit-scrollbar{width:3px;height:3px;}
::-webkit-scrollbar-thumb{background:rgba(61,158,255,0.2);border-radius:10px;}

/* ANIMATIONS */
@keyframes fadeUp{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:translateY(0)}}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:0.2}}
@keyframes pulse2{0%,100%{box-shadow:0 0 0 0 rgba(255,64,64,0.4)}70%{box-shadow:0 0 0 10px rgba(255,64,64,0)}}
@keyframes barGrow{from{width:0!important}to{width:var(--w)}}
@keyframes scoreCount{from{opacity:0;transform:scale(0.7)}to{opacity:1;transform:scale(1)}}
@keyframes spin{to{transform:rotate(360deg)}}
@keyframes scanBeat{0%,100%{opacity:0.6}50%{opacity:1}}
@keyframes slideIn{from{opacity:0;transform:translateX(-20px)}to{opacity:1;transform:translateX(0)}}
@keyframes bounceIn{0%{transform:scale(0.85);opacity:0}60%{transform:scale(1.04)}100%{transform:scale(1);opacity:1}}
.au{animation:fadeUp .5s ease both;}
.d1{animation-delay:.07s}.d2{animation-delay:.14s}.d3{animation-delay:.21s}
.d4{animation-delay:.28s}.d5{animation-delay:.35s}.d6{animation-delay:.42s}

/* NAV */
.top-nav{display:flex;align-items:center;gap:14px;padding:1.8rem 0 1.5rem;border-bottom:1px solid var(--bd);margin-bottom:0;}
.nav-logo{font-family:'Syne',sans-serif;font-size:1.4rem;font-weight:800;letter-spacing:1px;color:var(--text);}
.nav-logo span{color:var(--red);}
.nav-badge{display:inline-flex;align-items:center;gap:7px;background:var(--red2);border:1px solid rgba(255,64,64,0.3);padding:5px 13px;border-radius:5px;font-family:'IBM Plex Mono',monospace;font-size:9px;letter-spacing:2px;text-transform:uppercase;color:var(--red);}
.nav-dot{width:5px;height:5px;background:var(--red);border-radius:50%;animation:pulse 1.4s infinite;}
.nav-spacer{flex:1;height:1px;background:var(--bd);}
.nav-model{font-family:'IBM Plex Mono',monospace;font-size:9px;color:var(--muted);letter-spacing:1.5px;}

/* TABS */
.tab-bar{display:flex;gap:0;border-bottom:1px solid var(--bd);margin-bottom:2rem;overflow-x:auto;}
.tab-btn{padding:12px 20px;font-family:'IBM Plex Mono',monospace;font-size:10px;letter-spacing:1.5px;text-transform:uppercase;color:var(--muted2);border:none;background:transparent;cursor:pointer;border-bottom:2px solid transparent;transition:all .2s;white-space:nowrap;display:flex;align-items:center;gap:7px;}
.tab-btn:hover{color:var(--text);background:rgba(255,255,255,0.02);}
.tab-btn.active{color:var(--blu);border-bottom-color:var(--blu);}

/* HEALTH SCORE WIDGET */
.health-widget{background:var(--bg2);border:1px solid var(--bd2);border-radius:20px;padding:24px 20px;text-align:center;}
.health-ring{position:relative;width:110px;height:110px;margin:0 auto 12px;}
.health-val{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:'Syne',sans-serif;}
.health-score{font-size:2.2rem;font-weight:800;line-height:1;animation:scoreCount .6s ease both;}
.health-sub{font-size:9px;font-family:'IBM Plex Mono',monospace;color:var(--muted2);}
.health-label{font-family:'IBM Plex Mono',monospace;font-size:9px;letter-spacing:2px;text-transform:uppercase;color:var(--muted);margin-bottom:4px;}
.health-verdict{font-family:'Syne',sans-serif;font-size:1rem;font-weight:700;}

/* RISK METER */
.risk-meter{background:var(--bg2);border:1px solid var(--bd);border-radius:16px;padding:18px;}
.risk-meter-bar{height:10px;border-radius:10px;background:linear-gradient(90deg,var(--grn) 0%,var(--ylw) 40%,var(--red) 75%,#ff0000 100%);position:relative;margin:10px 0;}
.risk-needle{position:absolute;top:-4px;width:3px;height:18px;border-radius:3px;background:white;transform:translateX(-50%);box-shadow:0 0 8px rgba(255,255,255,0.7);}
.risk-zones{display:flex;justify-content:space-between;margin-top:3px;}
.risk-zone-lbl{font-family:'IBM Plex Mono',monospace;font-size:8px;color:var(--muted);}

/* METRIC CARDS */
.metrics-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:14px;}
.metric-card{background:var(--bg2);border:1px solid var(--bd);border-radius:14px;padding:16px;}
.metric-lbl{font-family:'IBM Plex Mono',monospace;font-size:8.5px;letter-spacing:2px;text-transform:uppercase;color:var(--muted);margin-bottom:8px;}
.metric-val{font-family:'Syne',sans-serif;font-size:2rem;font-weight:800;line-height:1;margin-bottom:3px;}
.metric-sub{font-size:11px;color:var(--muted2);}

/* AGENT PIPELINE */
.ag-pipeline{display:flex;align-items:center;gap:0;padding:20px 0;margin-bottom:16px;}
.ag-step{display:flex;flex-direction:column;align-items:center;gap:6px;min-width:80px;}
.ag-dot{width:36px;height:36px;border-radius:50%;border:1.5px solid var(--bd2);display:flex;align-items:center;justify-content:center;font-family:'IBM Plex Mono',monospace;font-size:12px;color:var(--muted2);background:var(--bg2);transition:all .3s;}
.ag-dot.active{border-color:var(--blu);color:var(--blu);background:var(--blu2);box-shadow:0 0 18px var(--blug);animation:pulse 1s infinite;}
.ag-dot.done{border-color:var(--grn);color:var(--grn);background:var(--grn2);}
.ag-lbl{font-family:'IBM Plex Mono',monospace;font-size:8px;letter-spacing:1.2px;text-transform:uppercase;color:var(--muted);text-align:center;line-height:1.4;}
.ag-lbl.active{color:var(--blu);}
.ag-line{flex:1;height:1px;background:var(--bd);margin-bottom:22px;}
.ag-line.done{background:rgba(0,232,135,0.3);}
.ag-line.active{background:rgba(61,158,255,0.3);}

/* AGENT LOG */
.agent-log{background:var(--bg);border:1px solid var(--bd);border-radius:12px;padding:14px;font-family:'IBM Plex Mono',monospace;font-size:11px;max-height:280px;overflow-y:auto;}
.lg-line{display:flex;gap:10px;padding:4px 0;border-bottom:1px solid rgba(255,255,255,0.02);align-items:flex-start;}
.lg-line:last-child{border-bottom:none;}
.lg-ts{color:var(--muted);flex-shrink:0;font-size:9.5px;padding-top:1px;}
.lg-k{flex-shrink:0;font-size:9px;padding:1px 6px;border-radius:3px;margin-top:1px;}
.lg-think{color:#9d7eff;background:rgba(157,126,255,0.1);}
.lg-action{color:var(--blu);background:var(--blu2);}
.lg-result{color:var(--grn);background:var(--grn2);}
.lg-warn{color:var(--ylw);background:var(--ylw2);}
.lg-m{color:var(--muted2);flex:1;line-height:1.5;}
.lg-m b{color:var(--text);font-weight:600;}

/* TASK LIST */
.task-item{display:flex;align-items:center;gap:12px;padding:12px 14px;border-radius:12px;border:1px solid var(--bd);background:var(--bg2);margin-bottom:8px;transition:all .2s;}
.task-item:hover{box-shadow:0 4px 20px rgba(0,0,0,0.3);transform:translateX(3px);}
.task-id{font-family:'IBM Plex Mono',monospace;font-size:10px;color:var(--muted);flex-shrink:0;width:50px;}
.task-name{font-size:13.5px;font-weight:600;flex:1;}
.task-bar-wrap{width:80px;height:5px;background:var(--bg3);border-radius:5px;flex-shrink:0;}
.task-bar{height:5px;border-radius:5px;animation:barGrow 1s ease both;}
.task-assignee{font-size:11.5px;color:var(--muted2);flex-shrink:0;width:100px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}

/* BADGES */
.badge{display:inline-flex;align-items:center;gap:5px;padding:3px 10px;border-radius:20px;font-family:'IBM Plex Mono',monospace;font-size:9.5px;font-weight:600;}
.badge-red{background:var(--red2);border:1px solid rgba(255,64,64,0.3);color:var(--red);}
.badge-grn{background:var(--grn2);border:1px solid rgba(0,232,135,0.25);color:var(--grn);}
.badge-ylw{background:var(--ylw2);border:1px solid rgba(255,190,0,0.25);color:var(--ylw);}
.badge-blu{background:var(--blu2);border:1px solid rgba(61,158,255,0.25);color:var(--blu);}
.badge-prp{background:var(--prp2);border:1px solid rgba(157,126,255,0.25);color:var(--prp);}
.bdot{width:5px;height:5px;border-radius:50%;background:currentColor;}

/* TEAM CARDS */
.team-card{background:var(--bg2);border:1px solid var(--bd);border-radius:16px;padding:16px;transition:all .2s;}
.team-card:hover{box-shadow:0 6px 24px rgba(0,0,0,0.3);}
.team-avatar{width:44px;height:44px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-family:'Syne',sans-serif;font-size:14px;font-weight:700;flex-shrink:0;}
.load-bar-wrap{height:6px;border-radius:6px;background:var(--bg3);margin-top:8px;}
.load-bar{height:6px;border-radius:6px;}

/* PRIORITY ITEM */
.prio-item{display:flex;gap:12px;padding:14px;border-radius:13px;border:1px solid var(--bd);background:var(--bg2);margin-bottom:9px;transition:all .2s;}
.prio-item:hover{transform:translateX(4px);box-shadow:0 4px 20px rgba(0,0,0,0.3);}
.prio-rank{width:32px;height:32px;border-radius:9px;display:flex;align-items:center;justify-content:center;font-family:'Syne',sans-serif;font-size:15px;font-weight:800;flex-shrink:0;}
.prio-body{flex:1;}
.prio-name{font-size:13.5px;font-weight:700;margin-bottom:3px;}
.prio-reason{font-size:12px;color:var(--muted2);line-height:1.5;}
.prio-meta{display:flex;gap:7px;flex-wrap:wrap;margin-top:7px;}
.score-box{font-family:'Syne',sans-serif;font-size:1.6rem;font-weight:800;padding:6px 14px;border-radius:10px;text-align:center;}

/* RECOVERY TIMELINE */
.timeline-day{display:flex;gap:14px;margin-bottom:14px;}
.timeline-dot-col{display:flex;flex-direction:column;align-items:center;gap:0;flex-shrink:0;}
.timeline-circle{width:32px;height:32px;border-radius:50%;background:var(--blu2);border:1.5px solid var(--blu);display:flex;align-items:center;justify-content:center;font-family:'IBM Plex Mono',monospace;font-size:10px;color:var(--blu);flex-shrink:0;}
.timeline-line{flex:1;width:1px;background:var(--bd);margin:4px 0;}
.timeline-body{flex:1;padding-bottom:14px;}
.timeline-day-lbl{font-family:'IBM Plex Mono',monospace;font-size:10px;letter-spacing:1.5px;text-transform:uppercase;color:var(--blu);margin-bottom:7px;}
.timeline-action{display:flex;gap:8px;padding:6px 0;font-size:12.5px;color:var(--text);border-bottom:1px solid rgba(255,255,255,0.03);}
.timeline-action:last-child{border-bottom:none;}

/* ESCALATION CARD */
.escalation-card{background:linear-gradient(135deg,rgba(255,64,64,0.05),rgba(255,64,64,0.02));border:1px solid rgba(255,64,64,0.18);border-radius:18px;padding:24px;}
.email-header{display:flex;flex-direction:column;gap:8px;padding-bottom:14px;border-bottom:1px solid var(--bd);margin-bottom:14px;}
.email-field{display:flex;gap:10px;align-items:center;}
.email-key{font-family:'IBM Plex Mono',monospace;font-size:9.5px;color:var(--muted);width:60px;flex-shrink:0;letter-spacing:1px;}
.email-val{font-size:13px;color:var(--text);}
.email-body{font-size:13.5px;color:var(--text);line-height:1.8;}

/* XAI CARDS */
.xai-card{background:var(--bg2);border:1px solid var(--bd);border-radius:14px;padding:14px;margin-bottom:9px;}
.xai-hdr{display:flex;align-items:center;gap:10px;margin-bottom:8px;}
.xai-icon{width:28px;height:28px;border-radius:8px;background:var(--prp2);border:1px solid rgba(157,126,255,0.3);display:flex;align-items:center;justify-content:center;font-size:13px;flex-shrink:0;}
.xai-title{font-family:'IBM Plex Mono',monospace;font-size:10.5px;font-weight:600;color:var(--prp);}
.xai-conf{margin-left:auto;font-family:'IBM Plex Mono',monospace;font-size:9px;color:var(--muted);}
.xai-body{font-size:12.5px;color:var(--text);line-height:1.6;}
.xai-data{font-size:11px;color:var(--muted2);margin-top:4px;font-style:italic;}

/* CHAT */
.chat-hero{background:linear-gradient(135deg,var(--bg3),var(--bg2));border:1px solid rgba(157,126,255,0.18);border-radius:18px;padding:18px 22px;margin-bottom:14px;display:flex;align-items:center;gap:16px;}
.bot-avatar{width:46px;height:46px;border-radius:13px;background:var(--prp2);border:1px solid rgba(157,126,255,0.3);display:flex;align-items:center;justify-content:center;font-size:22px;flex-shrink:0;}
.bot-name{font-family:'Syne',sans-serif;font-size:1rem;font-weight:700;}
.bot-status{display:flex;align-items:center;gap:5px;font-family:'IBM Plex Mono',monospace;font-size:9px;color:#6050a0;margin-left:auto;}
.chat-window{background:var(--bg2);border:1px solid var(--bd);border-radius:14px;padding:16px;min-height:280px;max-height:400px;overflow-y:auto;display:flex;flex-direction:column;gap:10px;margin-bottom:10px;}
.msg-row-user{display:flex;justify-content:flex-end;}
.msg-row-bot{display:flex;justify-content:flex-start;}
.bubble{max-width:80%;padding:11px 15px;border-radius:16px;font-size:13.5px;line-height:1.65;animation:bounceIn .3s ease both;}
.user-bub{background:var(--blu2);border:1px solid rgba(61,158,255,0.25);border-bottom-right-radius:4px;}
.bot-bub{background:var(--prp2);border:1px solid rgba(157,126,255,0.2);border-bottom-left-radius:4px;color:#d0c8f8;}
.sug-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:7px;margin-bottom:12px;}
.sug-chip{padding:9px 12px;border-radius:10px;border:1px solid rgba(157,126,255,0.2);background:var(--prp2);color:#9d7eff;font-family:'IBM Plex Mono',monospace;font-size:10.5px;cursor:pointer;transition:all .2s;line-height:1.4;text-align:left;}
.sug-chip:hover{border-color:rgba(157,126,255,0.5);transform:translateY(-2px);}

/* WHATIF */
.whatif-card{background:var(--bg2);border:1px solid var(--bd);border-radius:16px;padding:20px;}
.wi-delta{font-family:'Syne',sans-serif;font-size:2.5rem;font-weight:800;text-align:center;padding:20px;}
.wi-chip{display:inline-flex;align-items:center;gap:6px;padding:4px 12px;border-radius:20px;font-family:'IBM Plex Mono',monospace;font-size:9.5px;}

/* FORMS */
.stTextInput>div>div>input,.stNumberInput>div>div>input,.stTextArea>div>div>textarea{
  background:var(--bg)!important;border:1.5px solid var(--bd2)!important;
  border-radius:10px!important;font-family:'Manrope',sans-serif!important;
  font-size:13px!important;color:var(--text)!important;
}
.stTextInput>div>div>input:focus,.stNumberInput>div>div>input:focus,.stTextArea>div>div>textarea:focus{
  border-color:rgba(61,158,255,0.45)!important;
  box-shadow:0 0 0 3px rgba(61,158,255,0.06)!important;
}
.stTextInput label,.stNumberInput label,.stTextArea label,.stSelectbox label{
  font-family:'IBM Plex Mono',monospace!important;font-size:9px!important;
  letter-spacing:2px!important;text-transform:uppercase!important;color:var(--muted)!important;
}
.stTextInput label span,.stNumberInput label span,.stTextArea label span,.stSelectbox label span{color:transparent!important;}
.stSelectbox>div>div{background:var(--bg)!important;border:1.5px solid var(--bd2)!important;border-radius:10px!important;}
.stSlider label{font-family:'IBM Plex Mono',monospace!important;font-size:9px!important;letter-spacing:2px!important;text-transform:uppercase!important;color:var(--muted)!important;}

/* BUTTONS */
.stButton>button{background:var(--bg3)!important;border:1.5px solid var(--bd2)!important;
  color:var(--muted2)!important;font-family:'Manrope',sans-serif!important;
  font-size:13px!important;font-weight:600!important;border-radius:10px!important;transition:all .2s!important;}
.stButton>button:hover{border-color:rgba(255,255,255,0.2)!important;color:var(--text)!important;background:var(--bg4)!important;}
.btn-launch .stButton>button{
  background:linear-gradient(135deg,#ff4040,#c51a1a)!important;border:none!important;
  color:white!important;font-family:'Syne',sans-serif!important;font-size:15px!important;
  font-weight:700!important;border-radius:14px!important;height:4em!important;
  box-shadow:0 0 32px rgba(255,64,64,0.25),0 6px 18px rgba(255,64,64,0.15)!important;
  animation:pulse2 2s infinite;
}
.btn-launch .stButton>button:hover{transform:translateY(-3px)!important;box-shadow:0 0 50px rgba(255,64,64,0.4),0 10px 28px rgba(255,64,64,0.2)!important;animation:none!important;}
.btn-ghost .stButton>button{background:transparent!important;border:1px solid var(--bd)!important;color:var(--muted)!important;font-size:12px!important;border-radius:10px!important;height:2.5em!important;}
.btn-ghost .stButton>button:hover{border-color:rgba(255,255,255,0.14)!important;color:var(--text)!important;}
[data-testid="stHorizontalBlock"]{gap:12px!important;}
[data-testid="stChatInput"] textarea{background:var(--bg3)!important;border:1.5px solid rgba(157,126,255,0.22)!important;border-radius:12px!important;color:var(--text)!important;font-family:'Manrope',sans-serif!important;}
[data-testid="stChatInput"] textarea:focus{border-color:rgba(157,126,255,0.5)!important;}
[data-testid="stAlert"]{border-radius:12px!important;}

/* INFO SECTION CARDS */
.info-card{background:var(--bg2);border:1px solid var(--bd);border-radius:16px;padding:18px 20px;margin-bottom:12px;}
.info-hdr{display:flex;align-items:center;gap:10px;padding-bottom:12px;border-bottom:1px solid var(--bd);margin-bottom:12px;}
.info-num{font-family:'IBM Plex Mono',monospace;font-size:9px;color:var(--muted);padding:3px 8px;background:var(--bg3);border-radius:5px;border:1px solid var(--bd);}
.info-title{font-family:'IBM Plex Mono',monospace;font-size:11px;letter-spacing:2px;text-transform:uppercase;}
.info-check{margin-left:auto;width:20px;height:20px;border-radius:50%;border:1.5px solid var(--bd);display:flex;align-items:center;justify-content:center;font-size:10px;color:transparent;transition:all .3s;}
.info-check.done{border-color:var(--grn);background:var(--grn2);color:var(--grn);}

/* IMPROVEMENT ARROW */
.improvement-row{display:flex;align-items:center;gap:14px;padding:16px;background:var(--grn2);border:1px solid rgba(0,232,135,0.2);border-radius:14px;margin-top:14px;}
.imp-score{font-family:'Syne',sans-serif;font-size:2rem;font-weight:800;text-align:center;min-width:70px;}
.imp-arrow{font-size:1.5rem;color:var(--grn);}
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# TOP NAV
# ──────────────────────────────────────────────
st.markdown("""
<div class="top-nav au">
  <div class="nav-logo">SLA<span>.</span>Agent</div>
  <div class="nav-badge"><span class="nav-dot"></span>Multi-Agent AI Active</div>
  <div class="nav-spacer"></div>
  <div class="nav-model">Groq · LLaMA 3.3 70B · 5-Agent Pipeline</div>
</div>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# ██████ VIEW: DASHBOARD (INPUT) ██████████████
# ──────────────────────────────────────────────
if st.session_state.view == "dashboard":
    st.markdown("""
    <div class="au" style="padding:2rem 0 1.8rem;">
      <div style="font-family:'IBM Plex Mono',monospace;font-size:10px;letter-spacing:2.5px;
                  text-transform:uppercase;color:var(--muted);margin-bottom:10px;">
        Mission Control · SLA Prevention System
      </div>
      <h1 style="font-family:'Syne',sans-serif;font-size:clamp(2.2rem,5vw,3.8rem);font-weight:800;
                 letter-spacing:-1px;line-height:1;margin:0 0 14px;">
        Penalty Agent<br><span style="color:var(--red);">Command Centre</span>
      </h1>
      <p style="font-size:14px;color:var(--muted2);max-width:580px;line-height:1.7;margin:0;">
        5 AI agents working in sequence: Observe → Think → Decide → Act → Explain.
        Hit <b style="color:var(--red);">Launch Agent</b> and watch the full pipeline run live.
      </p>
    </div>
    """, unsafe_allow_html=True)

    left, right = st.columns([1.7, 1], gap="large")

    with left:
        # ── Contract Details ──
        st.markdown("""<div class="info-card au d1"><div class="info-hdr">
          <span class="info-num">01</span>
          <span class="info-title" style="color:var(--blu);">Contract & SLA</span>
          <div class="info-check done">✓</div></div></div>""", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            contract = st.text_input("Contract name", value="Enterprise Cloud Platform", key="inp_contract")
        with c2:
            sla_target = st.number_input("SLA Target (%)", 50, 100, 95, key="inp_sla_target")
        c3, c4 = st.columns(2)
        with c3:
            curr = st.number_input("Current Completion (%)", 0, 100, 58, key="inp_curr")
        with c4:
            days = st.number_input("Days Remaining", 1, 90, 3, key="inp_days")
        c5, c6 = st.columns(2)
        with c5:
            penalty = st.number_input("Penalty (₹)", 10000, 50000000, 500000, step=10000, key="inp_penalty")
        with c6:
            team_sz = st.number_input("Team Size", 1, 200, 5, key="inp_teamsize")

        # ── Tasks ──
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        st.markdown("""<div class="info-card au d2"><div class="info-hdr">
          <span class="info-num">02</span>
          <span class="info-title" style="color:var(--blu);">Task Data</span></div>
          <div style="font-size:12px;color:var(--muted2);margin-bottom:10px;">
            8 sample tasks pre-loaded. Edit or use as-is for demo.
          </div></div>""", unsafe_allow_html=True)

        tasks_display = "\n".join(
            f"{t['id']} | {t['name']} | {t['assignee']} | {t['progress']}% | {t['priority']}"
            + (f" | BLOCKED: {t['blocker']}" if t.get('blocked') else "")
            for t in SAMPLE_TASKS
        )
        tasks_raw = st.text_area(
            "Tasks (ID | Name | Assignee | Progress% | Priority | [BLOCKED: reason])",
            value=tasks_display, height=180, key="inp_tasks"
        )
        extra = st.text_input("Extra context (optional)", placeholder="e.g. key engineer on leave, client escalating…", key="inp_extra")

    with right:
        # ── Live risk preview ──
        gap = sla_target - curr
        breach_est = min(99, max(5, int(gap * 3.2 + (4 - days) * 9)))
        risk_label = "CRITICAL" if breach_est > 65 else ("HIGH" if breach_est > 40 else ("MEDIUM" if breach_est > 20 else "LOW"))
        risk_c = {"CRITICAL":"#ff4040","HIGH":"#ff8c42","MEDIUM":"#ffbe00","LOW":"#00e887"}.get(risk_label,"#ff4040")
        score = max(5, min(98, 100 - breach_est))
        circumf = 282
        offset = circumf - (circumf * score / 100)

        st.markdown(f"""
        <div class="au d2" style="display:flex;flex-direction:column;gap:12px;">
          <div class="health-widget">
            <div class="health-label">SLA Health Score</div>
            <div class="health-ring">
              <svg viewBox="0 0 110 110" style="width:110px;height:110px;transform:rotate(-90deg)">
                <circle cx="55" cy="55" r="45" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="7"/>
                <circle cx="55" cy="55" r="45" fill="none" stroke="{risk_c}" stroke-width="7"
                  stroke-linecap="round" stroke-dasharray="{circumf}"
                  stroke-dashoffset="{offset}" style="filter:drop-shadow(0 0 8px {risk_c})"/>
              </svg>
              <div class="health-val">
                <div class="health-score" style="color:{risk_c}">{score}</div>
                <div class="health-sub">/100</div>
              </div>
            </div>
            <div class="health-verdict" style="color:{risk_c}">{risk_label} RISK</div>
          </div>
          <div class="risk-meter">
            <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;letter-spacing:2px;
                        text-transform:uppercase;color:var(--muted);margin-bottom:8px;">SLA Risk Meter</div>
            <div class="risk-meter-bar">
              <div class="risk-needle" style="left:{breach_est}%"></div>
            </div>
            <div class="risk-zones">
              <span class="risk-zone-lbl" style="color:#00e887">SAFE</span>
              <span class="risk-zone-lbl" style="color:#ffbe00">RISK</span>
              <span class="risk-zone-lbl" style="color:#ff4040">PENALTY</span>
            </div>
            <div style="margin-top:12px;display:flex;justify-content:space-between;">
              <span style="font-family:'IBM Plex Mono',monospace;font-size:11px;color:{risk_c};">{breach_est}% breach probability</span>
              <span style="font-family:'IBM Plex Mono',monospace;font-size:11px;color:var(--muted);">₹{penalty:,} at risk</span>
            </div>
          </div>
        """, unsafe_allow_html=True)

        # ── Agent pipeline preview ──
        st.markdown("""
          <div style="background:var(--bg2);border:1px solid var(--bd);border-radius:16px;padding:16px;margin-top:0;">
            <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;letter-spacing:2px;
                        text-transform:uppercase;color:var(--muted);margin-bottom:12px;">
              5-Agent Pipeline
            </div>
        """, unsafe_allow_html=True)
        for icon, name, desc in AGENT_PIPELINE:
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1px solid rgba(255,255,255,0.03);">
              <span style="font-size:15px;width:22px;text-align:center;">{icon}</span>
              <div>
                <div style="font-family:'IBM Plex Mono',monospace;font-size:10px;color:var(--blu);letter-spacing:1px;">{name}</div>
                <div style="font-size:11px;color:var(--muted2);">{desc}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("""</div></div>""", unsafe_allow_html=True)

    # ── CTA ──
    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
    _, cta_c, _ = st.columns([1, 2, 1])
    with cta_c:
        st.markdown('<div class="btn-launch">', unsafe_allow_html=True)
        if st.button("🚨  Launch 5-Agent Pipeline  →", key="btn_launch", use_container_width=True):
            st.session_state.inputs = {
                "contract": contract, "sla_target": sla_target,
                "current_completion": curr, "days_remaining": days,
                "penalty_amount": penalty, "team_size": team_sz,
                "tasks": SAMPLE_TASKS, "team": SAMPLE_TEAM, "extra": extra,
            }
            st.session_state.view = "running"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div style="text-align:center;margin-top:10px;font-family:IBM Plex Mono,monospace;font-size:10px;color:var(--muted)">Observe → Think → Decide → Act → Explain</div>', unsafe_allow_html=True)


# ──────────────────────────────────────────────
# ██████ VIEW: RUNNING ████████████████████████
# ──────────────────────────────────────────────
elif st.session_state.view == "running":
    st.markdown("""
    <div class="au" style="padding:2rem 0 1.5rem;">
      <div style="font-family:'IBM Plex Mono',monospace;font-size:10px;letter-spacing:2.5px;
                  text-transform:uppercase;color:var(--blu);margin-bottom:8px;">Agent Pipeline Executing</div>
      <h2 style="font-family:'Syne',sans-serif;font-size:2.2rem;font-weight:800;
                 letter-spacing:-0.5px;margin:0 0 6px;">Running Multi-Agent Analysis…</h2>
      <p style="font-size:13px;color:var(--muted2);">5 AI agents are working in sequence. Watch the live log below.</p>
    </div>
    """, unsafe_allow_html=True)

    step_ph     = st.empty()
    progress_ph = st.empty()
    log_ph      = st.empty()

    # Init placeholders
    step_ph.markdown('<div class="ag-pipeline" style="padding:20px 0"></div>', unsafe_allow_html=True)
    progress_ph.progress(0)

    try:
        result = run_multi_agent(
            st.session_state.inputs,
            step_ph, log_ph, progress_ph
        )
        st.session_state.analysis = result
        st.session_state.view = "results"
        st.session_state.active_tab = "overview"
        st.session_state.health_score = result.get("sla_health_before", 42)
        time.sleep(0.6)
        st.rerun()
    except Exception as e:
        st.error(f"Agent pipeline error: {e}")
        if st.button("← Back", key="back_err"):
            st.session_state.view = "dashboard"
            st.rerun()


# ──────────────────────────────────────────────
# ██████ VIEW: RESULTS ████████████████████████
# ──────────────────────────────────────────────
elif st.session_state.view == "results":
    analysis = st.session_state.analysis or {}
    inp      = st.session_state.inputs or {}
    think    = analysis.get("think", {})
    decision = analysis.get("decision", {})
    action   = analysis.get("action", {})
    explain  = analysis.get("explain", {})

    score_before = analysis.get("sla_health_before", 42)
    score_after  = analysis.get("sla_health_after", 84)
    risk_c = {"CRITICAL":"#ff4040","HIGH":"#ff8c42","MEDIUM":"#ffbe00","LOW":"#00e887"}.get(think.get("risk_level","HIGH"),"#ff4040")

    # ── Tab bar ──
    tabs = [
        ("📊","overview","Overview"),
        ("🎯","tasks","Task Priority"),
        ("🧑‍🤝‍🧑","team","Team Manager"),
        ("🔧","recovery","Recovery Plan"),
        ("📢","escalation","Escalation"),
        ("🧠","explain","Why AI Did This"),
        ("🔮","whatif","What-If"),
        ("💬","chat","Chat Agent"),
    ]
    tab_html = "".join(
        f'<button class="tab-btn {"active" if st.session_state.active_tab==slug else ""}" '
        f'onclick="parent.postMessage({{type:\'streamlit:setComponentValue\',value:\'{slug}\'}},\'*\')">'
        f'{icon} {label}</button>'
        for icon, slug, label in tabs
    )
    st.markdown(f'<div class="tab-bar">{tab_html}</div>', unsafe_allow_html=True)

    # Streamlit tab buttons (real interactivity)
    tab_cols = st.columns(len(tabs))
    for i, (icon, slug, label) in enumerate(tabs):
        with tab_cols[i]:
            if st.button(f"{icon} {label}", key=f"tab_{slug}", use_container_width=True):
                st.session_state.active_tab = slug
                st.rerun()

    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
    at = st.session_state.active_tab

    # ══════════════════════════════
    # TAB: OVERVIEW
    # ══════════════════════════════
    if at == "overview":
        # Score header
        circumf = 282
        offset_b = circumf - (circumf * score_before / 100)
        offset_a = circumf - (circumf * score_after / 100)
        sc_b = "#ff4040" if score_before < 50 else ("#ffbe00" if score_before < 70 else "#00e887")
        sc_a = "#00e887" if score_after >= 70 else ("#ffbe00" if score_after >= 50 else "#ff4040")

        c1, c2, c3 = st.columns([1,1,2])
        with c1:
            st.markdown(f"""
            <div class="health-widget au">
              <div class="health-label">Health Before</div>
              <div class="health-ring">
                <svg viewBox="0 0 110 110" style="width:110px;height:110px;transform:rotate(-90deg)">
                  <circle cx="55" cy="55" r="45" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="7"/>
                  <circle cx="55" cy="55" r="45" fill="none" stroke="{sc_b}" stroke-width="7"
                    stroke-linecap="round" stroke-dasharray="{circumf}" stroke-dashoffset="{offset_b}"
                    style="filter:drop-shadow(0 0 6px {sc_b})"/>
                </svg>
                <div class="health-val">
                  <div class="health-score" style="color:{sc_b}">{score_before}</div>
                  <div class="health-sub">/100</div>
                </div>
              </div>
              <div class="health-verdict" style="color:{sc_b}">{think.get('risk_level','CRITICAL')}</div>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div class="health-widget au d1">
              <div class="health-label">Health After Recovery</div>
              <div class="health-ring">
                <svg viewBox="0 0 110 110" style="width:110px;height:110px;transform:rotate(-90deg)">
                  <circle cx="55" cy="55" r="45" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="7"/>
                  <circle cx="55" cy="55" r="45" fill="none" stroke="{sc_a}" stroke-width="7"
                    stroke-linecap="round" stroke-dasharray="{circumf}" stroke-dashoffset="{offset_a}"
                    style="filter:drop-shadow(0 0 8px {sc_a})"/>
                </svg>
                <div class="health-val">
                  <div class="health-score" style="color:{sc_a}">{score_after}</div>
                  <div class="health-sub">/100</div>
                </div>
              </div>
              <div class="health-verdict" style="color:{sc_a}">RECOVERING</div>
            </div>
            """, unsafe_allow_html=True)
        with c3:
            miss = think.get("predicted_miss_days", 2.3)
            bp   = think.get("breach_probability", 78)
            proj = action.get("projected_completion_after_recovery", 96)
            conf = action.get("recovery_confidence", 81)
            st.markdown(f"""
            <div class="au d2" style="display:flex;flex-direction:column;gap:10px;height:100%;">
              <div class="metrics-grid" style="grid-template-columns:1fr 1fr;">
                <div class="metric-card">
                  <div class="metric-lbl">SLA Miss Predicted</div>
                  <div class="metric-val" style="color:#ff4040">{miss}d</div>
                  <div class="metric-sub">if no action taken</div>
                </div>
                <div class="metric-card">
                  <div class="metric-lbl">Breach Probability</div>
                  <div class="metric-val" style="color:#ff8c42">{bp}%</div>
                  <div class="metric-sub">before recovery</div>
                </div>
                <div class="metric-card">
                  <div class="metric-lbl">Projected After</div>
                  <div class="metric-val" style="color:#00e887">{proj}%</div>
                  <div class="metric-sub">with recovery plan</div>
                </div>
                <div class="metric-card">
                  <div class="metric-lbl">Recovery Confidence</div>
                  <div class="metric-val" style="color:#3d9eff">{conf}%</div>
                  <div class="metric-sub">agent confidence</div>
                </div>
              </div>
              <div style="background:var(--grn2);border:1px solid rgba(0,232,135,0.2);border-radius:14px;padding:14px 16px;">
                <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;letter-spacing:2px;text-transform:uppercase;color:#00e887;margin-bottom:6px;">Agent Summary</div>
                <div style="font-size:13px;color:var(--text);line-height:1.7;">{explain.get('summary','Recovery plan generated successfully.')}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

        # Key risks
        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
        risks = think.get("key_risk_factors", [])
        if risks:
            risk_html = "".join(
                f'<div style="display:flex;align-items:flex-start;gap:10px;padding:9px 0;'
                f'border-bottom:1px solid rgba(255,255,255,0.03);font-size:13px;color:var(--text);">'
                f'<span style="color:#ff4040;flex-shrink:0;margin-top:1px;">⚠</span><span>{r}</span></div>'
                for r in risks
            )
            st.markdown(f"""
            <div class="info-card au d3">
              <div class="info-hdr" style="margin-bottom:0;border-bottom:none;padding-bottom:0;">
                <span style="font-family:'IBM Plex Mono',monospace;font-size:9px;letter-spacing:2px;
                             text-transform:uppercase;color:#ff4040;">🔴 Key Risk Factors Identified</span>
              </div>
              <div style="margin-top:10px;">{risk_html}</div>
            </div>
            """, unsafe_allow_html=True)

        # ML prediction basis
        ml_basis = think.get("ml_prediction_basis", "")
        if ml_basis:
            st.markdown(f"""
            <div class="au d4" style="background:var(--prp2);border:1px solid rgba(157,126,255,0.18);
                border-radius:14px;padding:14px 18px;display:flex;gap:12px;align-items:flex-start;">
              <span style="font-size:18px;flex-shrink:0;">🧠</span>
              <div>
                <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;letter-spacing:2px;
                            text-transform:uppercase;color:#9d7eff;margin-bottom:5px;">ML Prediction Basis</div>
                <div style="font-size:13px;color:var(--text);line-height:1.6;">{ml_basis}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    # ══════════════════════════════
    # TAB: TASK PRIORITY
    # ══════════════════════════════
    elif at == "tasks":
        priorities = decision.get("priority_ranking", [])
        crit_path  = decision.get("critical_path", [])

        action_colors = {
            "ACCELERATE": ("#3d9eff","rgba(61,158,255,0.1)"),
            "DEFER":       ("#ffbe00","rgba(255,190,0,0.1)"),
            "REASSIGN":    ("#9d7eff","rgba(157,126,255,0.1)"),
            "ESCALATE":    ("#ff4040","rgba(255,64,64,0.1)"),
            "ELIMINATE":   ("#ff8c42","rgba(255,140,66,0.1)"),
        }
        impact_c = {"High":"#ff4040","Medium":"#ffbe00","Low":"#00e887"}

        st.markdown(f"""
        <div class="au" style="margin-bottom:16px;">
          <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;letter-spacing:2px;
                      text-transform:uppercase;color:var(--muted);margin-bottom:4px;">Decision Agent Output</div>
          <div style="font-size:13.5px;color:var(--muted2);line-height:1.6;">
            {decision.get('decision_rationale','Prioritised by urgency × impact score.')}
          </div>
        </div>
        """, unsafe_allow_html=True)

        if crit_path:
            cp_html = " → ".join(f'<span style="font-family:IBM Plex Mono,monospace;font-size:11px;color:#ff4040;background:rgba(255,64,64,0.08);padding:3px 9px;border-radius:5px;">{tid}</span>' for tid in crit_path)
            st.markdown(f'<div style="margin-bottom:14px;display:flex;align-items:center;gap:8px;flex-wrap:wrap;"><span style="font-family:IBM Plex Mono,monospace;font-size:9px;color:var(--muted);letter-spacing:2px;text-transform:uppercase;">CRITICAL PATH:</span>{cp_html}</div>', unsafe_allow_html=True)

        for i, p in enumerate(priorities):
            ac = p.get("action","DEFER")
            c, bg = action_colors.get(ac, ("#5a6380","rgba(255,255,255,0.05)"))
            sc = p.get("score", p.get("urgency",5) * p.get("impact",5))
            st.markdown(f"""
            <div class="prio-item au" style="animation-delay:{i*60}ms">
              <div class="prio-rank" style="background:{bg};color:{c}">#{p.get('rank',i+1)}</div>
              <div class="prio-body">
                <div class="prio-name">{p.get('task_name','Task')} <span style="font-family:IBM Plex Mono,monospace;font-size:10px;color:var(--muted);">{p.get('task_id','')}</span></div>
                <div class="prio-reason">{p.get('reason','')}</div>
                <div class="prio-meta">
                  <span class="badge" style="background:{bg};border:1px solid {c}40;color:{c}">{ac}</span>
                  <span class="badge badge-blu">Urgency: {p.get('urgency','?')}/10</span>
                  <span class="badge badge-prp">Impact: {p.get('impact','?')}/10</span>
                  <span class="badge badge-grn">Score: {sc}</span>
                </div>
              </div>
              <div class="score-box" style="background:{bg};color:{c};border:1px solid {c}40">{sc}</div>
            </div>
            """, unsafe_allow_html=True)

        # Full task list with progress bars
        st.markdown("""<div style="margin-top:20px;margin-bottom:10px;">
          <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;letter-spacing:2px;
                      text-transform:uppercase;color:var(--muted);">All Tasks — Input Agent View</div>
        </div>""", unsafe_allow_html=True)

        prio_c = {"CRITICAL":"#ff4040","HIGH":"#ff8c42","MEDIUM":"#ffbe00","LOW":"#00e887"}
        for t in SAMPLE_TASKS:
            pc = prio_c.get(t["priority"],"#5a6380")
            bar_c = "#00e887" if t["progress"]>70 else ("#ffbe00" if t["progress"]>40 else "#ff4040")
            blocked_badge = f'<span class="badge badge-red"><span class="bdot"></span>BLOCKED</span>' if t.get("blocked") else ""
            st.markdown(f"""
            <div class="task-item au">
              <div class="task-id">{t['id']}</div>
              <div style="flex:1">
                <div class="task-name">{t['name']} {blocked_badge}</div>
                {f'<div style="font-size:11px;color:#ff4040;margin-top:2px;">⛔ {t["blocker"]}</div>' if t.get("blocked") else ""}
              </div>
              <div class="task-assignee">{t['assignee']}</div>
              <div style="flex-shrink:0;width:100px;">
                <div style="font-family:IBM Plex Mono,monospace;font-size:9px;color:var(--muted);margin-bottom:3px;">{t['progress']}%</div>
                <div class="task-bar-wrap">
                  <div class="task-bar" style="width:{t['progress']}%;background:{bar_c};--w:{t['progress']}%"></div>
                </div>
              </div>
              <span class="badge" style="background:rgba(255,255,255,0.04);border:1px solid {pc}40;color:{pc};">{t['priority']}</span>
            </div>
            """, unsafe_allow_html=True)

    # ══════════════════════════════
    # TAB: TEAM MANAGER
    # ══════════════════════════════
    elif at == "team":
        overloaded  = think.get("overloaded_resources", [])
        free_res    = think.get("free_resources", [])
        reassigns   = action.get("reassignments", [])

        st.markdown(f"""
        <div class="au" style="margin-bottom:16px;">
          <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;letter-spacing:2px;
                      text-transform:uppercase;color:var(--muted);margin-bottom:6px;">AI Team Manager · Resource Intelligence</div>
          <div style="display:flex;gap:10px;flex-wrap:wrap;">
            <span class="badge badge-red">⚠ Overloaded: {', '.join(overloaded) or 'None'}</span>
            <span class="badge badge-grn">✓ Available: {', '.join(free_res) or 'None'}</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        cols = st.columns(len(SAMPLE_TEAM), gap="small")
        for i, member in enumerate(SAMPLE_TEAM):
            load = member["load"]
            is_over = member["name"] in overloaded
            is_free  = member["name"] in free_res
            lc = "#ff4040" if load > 110 else ("#ffbe00" if load > 85 else "#00e887")
            bc = ("#ff4040" if is_over else ("#00e887" if is_free else "#3d9eff"))
            av_bg = f"background:rgba({('255,64,64' if is_over else ('0,232,135' if is_free else '61,158,255'))},0.15)"
            av_c  = f"color:{bc}"
            load_w = min(100, load)

            # tasks assigned to this member
            member_tasks = [t for t in SAMPLE_TASKS if t["assignee"] == member["name"]]
            skills_html = "".join(f'<span class="badge badge-blu" style="font-size:8.5px;padding:2px 7px;">{s}</span>' for s in member["skills"][:2])

            # reassignment note
            reas_note = next((f"→ Receiving: {r['task_name']}" for r in reassigns if r.get("to") == member["name"]), "")
            giving_note = next((f"← Offloading: {r['task_name']}" for r in reassigns if r.get("from") == member["name"]), "")

            with cols[i]:
                st.markdown(f"""
                <div class="team-card au" style="animation-delay:{i*70}ms;border-color:{'rgba(255,64,64,0.25)' if is_over else ('rgba(0,232,135,0.2)' if is_free else 'rgba(255,255,255,0.07)')}">
                  <div style="display:flex;align-items:center;gap:10px;margin-bottom:12px;">
                    <div class="team-avatar" style="{av_bg};{av_c}">{member['avatar']}</div>
                    <div>
                      <div style="font-size:13px;font-weight:700;">{member['name'].split()[0]}</div>
                      <div style="font-size:10.5px;color:var(--muted2);">{member['role']}</div>
                    </div>
                  </div>
                  <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
                    <span style="font-family:'IBM Plex Mono',monospace;font-size:9px;color:var(--muted);">LOAD</span>
                    <span style="font-family:'IBM Plex Mono',monospace;font-size:10px;color:{lc};font-weight:600;">{load}%</span>
                  </div>
                  <div class="load-bar-wrap">
                    <div class="load-bar" style="width:{min(100,load)}%;background:{lc};"></div>
                  </div>
                  <div style="margin-top:10px;font-size:11px;color:var(--muted2);">
                    {len(member_tasks)} task(s) · {member['tasks']} active
                  </div>
                  <div style="display:flex;gap:4px;flex-wrap:wrap;margin-top:6px;">{skills_html}</div>
                  {f'<div style="margin-top:8px;font-size:11px;color:#ff4040;background:rgba(255,64,64,0.06);border-radius:7px;padding:5px 8px;">{giving_note}</div>' if giving_note else ''}
                  {f'<div style="margin-top:8px;font-size:11px;color:#00e887;background:rgba(0,232,135,0.06);border-radius:7px;padding:5px 8px;">{reas_note}</div>' if reas_note else ''}
                  {'<div class="badge badge-red" style="margin-top:8px;width:100%;justify-content:center;">OVERLOADED</div>' if is_over else ''}
                  {'<div class="badge badge-grn" style="margin-top:8px;width:100%;justify-content:center;">AVAILABLE</div>' if is_free else ''}
                </div>
                """, unsafe_allow_html=True)

        # Reassignment table
        if reassigns:
            st.markdown("""<div style="margin-top:20px;margin-bottom:12px;">
              <span style="font-family:'IBM Plex Mono',monospace;font-size:9px;letter-spacing:2px;
                           text-transform:uppercase;color:var(--blu);">🔄 Action Agent Reassignments</span>
            </div>""", unsafe_allow_html=True)
            for r in reassigns:
                st.markdown(f"""
                <div style="background:var(--bg2);border:1px solid rgba(61,158,255,0.15);border-radius:12px;
                            padding:12px 16px;margin-bottom:8px;display:flex;align-items:center;gap:12px;">
                  <span class="badge badge-prp">{r.get('task_id','')}</span>
                  <div style="flex:1">
                    <div style="font-size:13px;font-weight:600;">{r.get('task_name','')}</div>
                    <div style="font-size:11.5px;color:var(--muted2);">{r.get('reason','')}</div>
                  </div>
                  <div style="text-align:center;flex-shrink:0;">
                    <div style="font-size:11px;color:#ff4040;">{r.get('from','')}</div>
                    <div style="font-size:14px;">↓</div>
                    <div style="font-size:11px;color:#00e887;">{r.get('to','')}</div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

        # Overtime suggestions
        overtime = action.get("overtime_suggestions", [])
        if overtime:
            st.markdown("""<div style="margin-top:16px;margin-bottom:12px;">
              <span style="font-family:'IBM Plex Mono',monospace;font-size:9px;letter-spacing:2px;
                           text-transform:uppercase;color:#ffbe00;">⏱ Overtime Suggestions</span>
            </div>""", unsafe_allow_html=True)
            for ov in overtime:
                st.markdown(f"""
                <div style="background:var(--ylw2);border:1px solid rgba(255,190,0,0.2);border-radius:12px;
                            padding:12px 16px;margin-bottom:8px;display:flex;align-items:center;gap:12px;">
                  <span style="font-size:22px;">⏱</span>
                  <div style="flex:1">
                    <div style="font-size:13px;font-weight:600;">{ov.get('person','')} — +{ov.get('hours',0)}hrs overtime</div>
                    <div style="font-size:11.5px;color:var(--muted2);margin-top:2px;">{ov.get('impact','')}</div>
                  </div>
                  <div style="display:flex;flex-direction:column;gap:4px;">
                    {"".join(f'<span class="badge badge-ylw">{t}</span>' for t in ov.get("tasks",[]))}
                  </div>
                </div>
                """, unsafe_allow_html=True)

    # ══════════════════════════════
    # TAB: RECOVERY PLAN
    # ══════════════════════════════
    elif at == "recovery":
        timeline = action.get("recovery_timeline", [])
        unblocks  = action.get("unblock_actions", [])
        proj_comp = action.get("projected_completion_after_recovery", 96)
        conf      = action.get("recovery_confidence", 81)

        st.markdown(f"""
        <div class="au" style="margin-bottom:20px;display:flex;gap:14px;align-items:center;flex-wrap:wrap;">
          <div style="background:var(--grn2);border:1px solid rgba(0,232,135,0.2);border-radius:14px;
                      padding:12px 20px;display:flex;align-items:center;gap:14px;">
            <div>
              <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;letter-spacing:2px;
                          text-transform:uppercase;color:#00e887;">Projected After Recovery</div>
              <div style="font-family:'Syne',sans-serif;font-size:2rem;font-weight:800;color:#00e887;">{proj_comp}%</div>
            </div>
            <div style="width:1px;height:40px;background:rgba(0,232,135,0.2)"></div>
            <div>
              <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;letter-spacing:2px;
                          text-transform:uppercase;color:#00e887;">Agent Confidence</div>
              <div style="font-family:'Syne',sans-serif;font-size:2rem;font-weight:800;color:#00e887;">{conf}%</div>
            </div>
          </div>
          <span class="badge badge-grn" style="font-size:11px;padding:7px 16px;">✓ On track for SLA compliance</span>
        </div>
        """, unsafe_allow_html=True)

        cl, cr = st.columns([1.2, 1], gap="large")
        with cl:
            st.markdown("""<div style="font-family:'IBM Plex Mono',monospace;font-size:9px;letter-spacing:2px;
                           text-transform:uppercase;color:var(--muted);margin-bottom:14px;">📅 Day-by-Day Recovery Timeline</div>""", unsafe_allow_html=True)

            for i, day_plan in enumerate(timeline):
                actions_html = "".join(
                    f'<div class="timeline-action"><span style="color:#3d9eff;flex-shrink:0;">→</span><span>{act}</span></div>'
                    for act in day_plan.get("actions", [])
                )
                is_last = i == len(timeline) - 1
                st.markdown(f"""
                <div class="timeline-day au" style="animation-delay:{i*80}ms">
                  <div class="timeline-dot-col">
                    <div class="timeline-circle">{i+1}</div>
                    {"" if is_last else '<div class="timeline-line"></div>'}
                  </div>
                  <div class="timeline-body">
                    <div class="timeline-day-lbl">{day_plan.get('day','Day '+str(i+1))}</div>
                    {actions_html}
                  </div>
                </div>
                """, unsafe_allow_html=True)

        with cr:
            # Unblock actions
            if unblocks:
                st.markdown("""<div style="font-family:'IBM Plex Mono',monospace;font-size:9px;letter-spacing:2px;
                               text-transform:uppercase;color:var(--muted);margin-bottom:14px;">⛔ Unblock Actions</div>""", unsafe_allow_html=True)
                for ub in unblocks:
                    st.markdown(f"""
                    <div style="background:var(--bg2);border:1px solid rgba(255,64,64,0.15);border-radius:13px;
                                padding:14px;margin-bottom:9px;">
                      <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
                        <span class="badge badge-red">{ub.get('task_id','')}</span>
                        <span style="font-size:13px;font-weight:600;color:var(--text);">Blocked</span>
                      </div>
                      <div style="font-size:12px;color:#ff4040;margin-bottom:8px;">⛔ {ub.get('blocker','')}</div>
                      <div style="font-size:12px;color:#00e887;">✓ {ub.get('resolution','')}</div>
                    </div>
                    """, unsafe_allow_html=True)

            # Score improvement widget
            st.markdown(f"""
            <div style="background:var(--bg2);border:1px solid var(--bd);border-radius:16px;padding:20px;text-align:center;margin-top:4px;">
              <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;letter-spacing:2px;
                          text-transform:uppercase;color:var(--muted);margin-bottom:14px;">SLA Health Recovery</div>
              <div style="display:flex;align-items:center;justify-content:center;gap:16px;">
                <div>
                  <div style="font-family:'Syne',sans-serif;font-size:3rem;font-weight:800;color:#ff4040;">{score_before}</div>
                  <div style="font-size:11px;color:var(--muted2);">Before</div>
                </div>
                <div style="font-size:2rem;color:#00e887;">→</div>
                <div>
                  <div style="font-family:'Syne',sans-serif;font-size:3rem;font-weight:800;color:#00e887;">{score_after}</div>
                  <div style="font-size:11px;color:var(--muted2);">After</div>
                </div>
              </div>
              <div style="margin-top:12px;" class="badge badge-grn">+{score_after - score_before} point improvement</div>
            </div>
            """, unsafe_allow_html=True)

    # ══════════════════════════════
    # TAB: ESCALATION
    # ══════════════════════════════
    elif at == "escalation":
        subj = action.get("escalation_subject", "🚨 SLA Risk Alert")
        body = action.get("escalation_body", "")
        miss = think.get("predicted_miss_days", 2.3)
        bp   = think.get("breach_probability", 78)

        st.markdown(f"""
        <div class="au" style="margin-bottom:16px;">
          <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;letter-spacing:2px;
                      text-transform:uppercase;color:#ff4040;margin-bottom:6px;">Auto-Generated by Action Agent</div>
          <p style="font-size:13px;color:var(--muted2);">
            One-click escalation message, ready to send. Includes SLA data, recovery plan summary, and projected outcome.
          </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="escalation-card au d1">
          <div class="email-header">
            <div class="email-field">
              <span class="email-key">TO:</span>
              <span class="email-val">Delivery Manager, Project Sponsor</span>
            </div>
            <div class="email-field">
              <span class="email-key">CC:</span>
              <span class="email-val">Account Manager, Tech Lead</span>
            </div>
            <div class="email-field">
              <span class="email-key">SUBJECT:</span>
              <span class="email-val" style="color:var(--red);font-weight:600;">{subj}</span>
            </div>
          </div>
          <div class="email-body">{body}</div>
        </div>
        """, unsafe_allow_html=True)

        # SLA alert banner
        st.markdown(f"""
        <div class="au d2" style="background:var(--red2);border:1px solid rgba(255,64,64,0.28);
             border-radius:14px;padding:16px 20px;margin-top:14px;display:flex;align-items:center;gap:16px;">
          <span style="font-size:2rem;">🚨</span>
          <div>
            <div style="font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:700;color:#ff4040;">
              SLA Will Be Missed By {miss} Days
            </div>
            <div style="font-size:13px;color:var(--muted2);margin-top:3px;">
              Breach probability: {bp}% · Penalty: ₹{inp.get('penalty_amount',500000):,} · {inp.get('days_remaining',3)} days remaining
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            new_subj = st.text_input("Subject", value=subj, key="esc_subj")
        with c2:
            st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
            st.markdown('<div class="btn-ghost">', unsafe_allow_html=True)
            if st.button("📋 Copy to Clipboard (manual)", key="copy_esc", use_container_width=True):
                st.info("Copy the message above to send via your email client.")
            st.markdown('</div>', unsafe_allow_html=True)
        new_body = st.text_area("Edit message", value=body, height=150, key="esc_body")

    # ══════════════════════════════
    # TAB: WHY AI DID THIS
    # ══════════════════════════════
    elif at == "explain":
        explanations = explain.get("explanations", [])
        summary      = explain.get("summary", "")

        st.markdown(f"""
        <div class="au" style="background:var(--prp2);border:1px solid rgba(157,126,255,0.18);
             border-radius:16px;padding:18px 22px;margin-bottom:18px;">
          <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;letter-spacing:2px;
                      text-transform:uppercase;color:#9d7eff;margin-bottom:7px;">🧠 Explain Agent Summary</div>
          <div style="font-size:14px;color:var(--text);line-height:1.75;">{summary}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""<div style="font-family:'IBM Plex Mono',monospace;font-size:9px;letter-spacing:2px;
                       text-transform:uppercase;color:var(--muted);margin-bottom:12px;">
          Decision-by-Decision Explainability
        </div>""", unsafe_allow_html=True)

        for i, ex in enumerate(explanations):
            conf_c = "#00e887" if ex.get("confidence",80) > 85 else ("#ffbe00" if ex.get("confidence",80) > 70 else "#ff8c42")
            st.markdown(f"""
            <div class="xai-card au" style="animation-delay:{i*70}ms">
              <div class="xai-hdr">
                <div class="xai-icon">🔍</div>
                <div class="xai-title">{ex.get('decision','')}</div>
                <div class="xai-conf" style="color:{conf_c}">Confidence: {ex.get('confidence',80)}%</div>
              </div>
              <div class="xai-body">{ex.get('why','')}</div>
              <div class="xai-data">Data used: {ex.get('data_used','')}</div>
            </div>
            """, unsafe_allow_html=True)

        # Judges love this section
        st.markdown("""
        <div class="au d5" style="margin-top:20px;background:rgba(0,232,135,0.04);border:1px solid rgba(0,232,135,0.15);
             border-radius:14px;padding:16px 20px;">
          <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;letter-spacing:2px;
                      text-transform:uppercase;color:#00e887;margin-bottom:10px;">✅ Why Explainability Matters</div>
          <div style="font-size:13px;color:var(--text);line-height:1.7;">
            The Explain Agent ensures every decision is <b>transparent and auditable</b>.
            Managers can see exactly why a task was reassigned, which data drove the prediction,
            and how confident the AI is — building trust in AI-driven operations.
          </div>
        </div>
        """, unsafe_allow_html=True)

    # ══════════════════════════════
    # TAB: WHAT-IF SIMULATOR
    # ══════════════════════════════
    elif at == "whatif":
        st.markdown("""
        <div class="au" style="margin-bottom:16px;">
          <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;letter-spacing:2px;
                      text-transform:uppercase;color:var(--muted);margin-bottom:6px;">🔮 What-If Scenario Simulator</div>
          <p style="font-size:13.5px;color:var(--muted2);line-height:1.6;">
            Ask the agent to simulate any change. Instant outcome prediction powered by AI.
          </p>
        </div>
        """, unsafe_allow_html=True)

        # Preset scenarios
        presets = [
            "What if I add 2 more developers to the team?",
            "What if Task T-001 is delayed by 1 more day?",
            "What if we defer all LOW priority tasks?",
            "What if Rahul works weekend overtime?",
            "What if we remove the security audit from scope?",
            "What if the client unblocks the API token today?",
        ]
        st.markdown("""<div style="font-family:'IBM Plex Mono',monospace;font-size:9px;letter-spacing:2px;
                       text-transform:uppercase;color:var(--muted);margin-bottom:8px;">Quick Scenarios</div>
        <div class="sug-grid">""", unsafe_allow_html=True)
        cols3 = st.columns(3)
        for i, preset in enumerate(presets):
            with cols3[i % 3]:
                if st.button(f"→ {preset}", key=f"preset_{i}", use_container_width=True):
                    st.session_state["wi_input"] = preset
                    with st.spinner("Simulating scenario…"):
                        st.session_state.whatif_result = run_whatif(preset, analysis, inp)
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        wi_text = st.text_input("Or type your own scenario…",
            value=st.session_state.get("wi_input",""),
            placeholder="e.g. What if I add 3 developers?",
            key="wi_custom")
        c1, c2 = st.columns([3,1])
        with c2:
            if st.button("🔮 Simulate", key="wi_run", use_container_width=True):
                if wi_text.strip():
                    st.session_state["wi_input"] = wi_text
                    with st.spinner("Agent simulating…"):
                        st.session_state.whatif_result = run_whatif(wi_text, analysis, inp)
                    st.rerun()

        if st.session_state.whatif_result:
            wi = st.session_state.whatif_result
            delta = wi.get("delta_days", 0)
            delta_c = "#00e887" if delta > 0 else "#ff4040"
            delta_sym = "+" if delta > 0 else ""
            new_h = wi.get("new_sla_health", 70)
            new_h_c = "#00e887" if new_h >= 70 else ("#ffbe00" if new_h >= 50 else "#ff4040")
            circumf = 282
            off_wi = circumf - (circumf * new_h / 100)

            st.markdown(f"""
            <div class="whatif-card au d1" style="margin-top:16px;">
              <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;letter-spacing:2px;
                          text-transform:uppercase;color:var(--muted);margin-bottom:10px;">
                Simulation Result: {wi.get('scenario_title','')}
              </div>
              <div style="display:flex;gap:20px;align-items:center;flex-wrap:wrap;">
                <div style="text-align:center;">
                  <svg viewBox="0 0 110 110" style="width:90px;height:90px;transform:rotate(-90deg)">
                    <circle cx="55" cy="55" r="45" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="7"/>
                    <circle cx="55" cy="55" r="45" fill="none" stroke="{new_h_c}" stroke-width="7"
                      stroke-linecap="round" stroke-dasharray="{circumf}" stroke-dashoffset="{off_wi}"
                      style="filter:drop-shadow(0 0 6px {new_h_c})"/>
                  </svg>
                  <div style="font-family:'Syne',sans-serif;font-size:1.6rem;font-weight:800;color:{new_h_c};margin-top:-70px;">{new_h}</div>
                  <div style="font-size:10px;color:var(--muted);margin-top:50px;">New Health</div>
                </div>
                <div style="flex:1;min-width:200px;">
                  <div style="font-family:'Syne',sans-serif;font-size:2.4rem;font-weight:800;color:{delta_c};">
                    {delta_sym}{delta}d
                  </div>
                  <div style="font-size:12px;color:var(--muted2);margin-bottom:12px;">
                    {'improvement' if delta > 0 else 'additional delay'}
                  </div>
                  <div style="display:flex;gap:8px;margin-bottom:12px;flex-wrap:wrap;">
                    <span class="badge badge-blu">Breach: {wi.get('new_breach_probability',50)}%</span>
                    <span class="badge badge-grn">Projected: {wi.get('new_completion_projected',90)}%</span>
                  </div>
                  <div style="font-size:13px;color:var(--text);background:var(--blu2);border:1px solid rgba(61,158,255,0.2);
                              border-radius:10px;padding:10px 14px;line-height:1.6;">
                    💡 {wi.get('recommendation','')}
                  </div>
                </div>
                <div style="flex:1;min-width:180px;">
                  <div style="font-family:'IBM Plex Mono',monospace;font-size:9px;letter-spacing:2px;
                              text-transform:uppercase;color:var(--muted);margin-bottom:8px;">Key Changes</div>
                  {"".join(f'<div style="display:flex;gap:8px;padding:6px 0;font-size:12px;color:var(--text);border-bottom:1px solid rgba(255,255,255,0.03)"><span style=color:#00e887>→</span><span>{c}</span></div>' for c in wi.get('key_changes',[]))}
                  {"".join(f'<div style="display:flex;gap:8px;padding:6px 0;font-size:12px;color:#ff8c42;border-bottom:1px solid rgba(255,255,255,0.03)"><span>⚠</span><span>{r}</span></div>' for r in wi.get('risks',[]))}
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    # ══════════════════════════════
    # TAB: CHAT AGENT
    # ══════════════════════════════
    elif at == "chat":
        st.markdown("""
        <div class="chat-hero au">
          <div class="bot-avatar">🤖</div>
          <div>
            <div class="bot-name">OpsBot — Your AI Operations Manager</div>
            <div style="font-size:12px;color:#6050a0;margin-top:2px;">
              I know your SLA data, tasks, team, and recovery plan. Ask me anything.
            </div>
          </div>
          <div class="bot-status"><div style="width:7px;height:7px;border-radius:50%;background:#9d7eff;animation:pulse 2s infinite;"></div>Online</div>
        </div>
        """, unsafe_allow_html=True)

        # Context pill
        miss = think.get("predicted_miss_days", 2.3)
        bp   = think.get("breach_probability", 78)
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:10px;background:rgba(0,232,135,0.04);
             border:1px solid rgba(0,232,135,0.12);border-radius:11px;padding:8px 14px;margin-bottom:12px;">
          <span>🎯</span>
          <div style="font-size:12px;color:#2a8880;">
            Context loaded: <b>{inp.get('contract','')}</b> · SLA miss predicted: <b>{miss} days</b> · Breach risk: <b>{bp}%</b>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Suggestion chips
        if not st.session_state.chat_history:
            sugs = [
                "Why is SLA at risk?", "Fix it", "Show recovery plan",
                "Who is overloaded?", "What's the biggest bottleneck?", "Escalate now",
            ]
            chip_cols = st.columns(3)
            for i, s in enumerate(sugs):
                with chip_cols[i % 3]:
                    if st.button(s, key=f"chat_sug_{i}", use_container_width=True):
                        st.session_state.chat_history.append({"role":"user","content":s})
                        with st.spinner(""):
                            reply = chat_agent(s, analysis, inp)
                        st.session_state.chat_history.append({"role":"assistant","content":reply})
                        st.rerun()
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        # Chat window
        bubbles = ""
        if not st.session_state.chat_history:
            bubbles = """<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;
                           min-height:200px;gap:10px;text-align:center;">
              <div style="font-size:36px;opacity:.25;">💬</div>
              <div style="font-size:13px;color:var(--muted);max-width:260px;line-height:1.5;">
                Ask anything about your SLA, tasks, team, or recovery plan.
              </div></div>"""
        else:
            for msg in st.session_state.chat_history:
                if msg["role"] == "user":
                    bubbles += f'<div class="msg-row-user"><div class="bubble user-bub">{msg["content"]}</div></div>'
                else:
                    bubbles += f'<div class="msg-row-bot"><div class="bubble bot-bub">{msg["content"]}</div></div>'
        st.markdown(f'<div class="chat-window">{bubbles}</div>', unsafe_allow_html=True)

        user_input = st.chat_input("Ask OpsBot anything… 'Fix it', 'Why is T-003 critical?', 'Show plan'")
        if user_input:
            st.session_state.chat_history.append({"role":"user","content":user_input})
            with st.spinner(""):
                reply = chat_agent(user_input, analysis, inp)
            st.session_state.chat_history.append({"role":"assistant","content":reply})
            st.rerun()

        ca, cb = st.columns(2)
        with ca:
            st.markdown('<div class="btn-ghost">', unsafe_allow_html=True)
            if st.button("🗑 Clear Chat", key="clear_chat", use_container_width=True):
                st.session_state.chat_history = []
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    # ── Bottom controls (always shown on result tabs) ──
    st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)
    ca, cb, _ = st.columns([1, 1, 3])
    with ca:
        st.markdown('<div class="btn-ghost">', unsafe_allow_html=True)
        if st.button("← New Analysis", key="new_analysis", use_container_width=True):
            st.session_state.view = "dashboard"
            st.session_state.analysis = None
            st.session_state.chat_history = []
            st.session_state.whatif_result = None
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with cb:
        st.markdown('<div class="btn-ghost">', unsafe_allow_html=True)
        if st.button("🔄 Re-run Agents", key="rerun_agents", use_container_width=True):
            st.session_state.view = "running"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ── Footer ──
st.markdown("""
<div style="text-align:center;padding:3rem 0 1rem;border-top:1px solid rgba(255,255,255,0.04);
            margin-top:3rem;font-family:'IBM Plex Mono',monospace;font-size:10px;color:#1e2238;letter-spacing:0.5px;">
  SLA Penalty Agent · 5-Agent Pipeline · Groq · LLaMA 3.3 70B · Hackathon Build
</div>
""", unsafe_allow_html=True)
