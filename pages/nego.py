import streamlit as st
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os, json, csv, io, time
from difflib import SequenceMatcher

load_dotenv()

st.set_page_config(layout="wide", page_title="VendorIQ — Procurement Intelligence")

# ── LLM ──────────────────────────────────────────────────────────────────────
@st.cache_resource
def get_llm():
    return ChatGroq(model="llama-3.1-8b-instant", api_key=os.getenv("GROQ_API_KEY"))

# ── SIMILARITY HELPERS ────────────────────────────────────────────────────────

def name_similarity(a, b):
    a, b = a.lower().strip(), b.lower().strip()
    if a == b: return 1.0
    for suffix in [" ltd"," inc"," pvt"," llc"," corp"," co"," limited"," private","."]:
        a = a.replace(suffix, ""); b = b.replace(suffix, "")
    a, b = a.strip(), b.strip()
    if a == b: return 0.97
    return SequenceMatcher(None, a, b).ratio()

def service_similarity(a, b):
    if not a or not b: return 0.0
    a, b = a.lower().strip(), b.lower().strip()
    if a == b: return 1.0
    wa, wb = set(a.split()), set(b.split())
    if not wa or not wb: return 0.0
    return max(len(wa & wb) / len(wa | wb), SequenceMatcher(None, a, b).ratio())

def is_duplicate(v1, v2):
    ns = name_similarity(v1.get("name",""), v2.get("name",""))
    ss = service_similarity(v1.get("service",""), v2.get("service",""))
    if ns >= 0.97: return True, ns, ss, "exact_name"
    if ns >= 0.72 and ss >= 0.55: return True, ns, ss, "name_and_service"
    if ss >= 0.9 and ns >= 0.55: return True, ns, ss, "same_service"
    return False, ns, ss, None

def is_low_value(vendor):
    score = 0; reasons = []
    spend  = float(vendor.get("annual_spend", 0) or 0)
    txn    = int(vendor.get("transactions", 0) or 0)
    rating = float(vendor.get("rating", 3) or 3)
    cat    = vendor.get("service","").lower()
    if spend < 10000:   score += 3; reasons.append("Very low annual spend")
    elif spend < 50000: score += 1; reasons.append("Low annual spend")
    if txn < 3:    score += 3; reasons.append("Fewer than 3 transactions")
    elif txn < 10: score += 1; reasons.append("Low transaction count")
    if rating < 2.5:   score += 3; reasons.append("Poor performance rating")
    elif rating < 3.5: score += 1; reasons.append("Below-average rating")
    risky = ["misc","miscellaneous","one-time","temp","trial","test","unknown","other"]
    if any(k in cat for k in risky): score += 2; reasons.append("High-risk category")
    return score >= 4, score, reasons

def parse_vendors(data_str):
    try:
        reader = csv.DictReader(io.StringIO(data_str.strip()))
        vendors = [dict(r) for r in reader]
        if vendors and any(k.strip() for k in vendors[0]): return vendors
    except: pass
    try: return json.loads(data_str)
    except: pass
    return []

def generate_sample_vendors():
    return [
        {"id":"V001","name":"Infosys Ltd","service":"IT Consulting","annual_spend":850000,"transactions":42,"rating":4.2,"location":"Bangalore","contact":"infosys@corp.com"},
        {"id":"V002","name":"Infosys Limited","service":"IT Consulting","annual_spend":120000,"transactions":8,"rating":3.9,"location":"Mumbai","contact":"infosys.ltd@vendor.com"},
        {"id":"V003","name":"TCS","service":"Software Development","annual_spend":1200000,"transactions":67,"rating":4.5,"location":"Mumbai","contact":"tcs@corp.com"},
        {"id":"V004","name":"Tata Consultancy Services","service":"Software Development","annual_spend":95000,"transactions":5,"rating":4.0,"location":"Pune","contact":"tcs.vendor@email.com"},
        {"id":"V005","name":"Wipro","service":"Cloud Services","annual_spend":430000,"transactions":28,"rating":3.8,"location":"Bangalore","contact":"wipro@corp.com"},
        {"id":"V006","name":"Wipro Technologies","service":"Cloud Services","annual_spend":67000,"transactions":4,"rating":3.5,"location":"Hyderabad","contact":"wipro.tech@vendor.com"},
        {"id":"V007","name":"Amazon Web Services","service":"Cloud Hosting","annual_spend":920000,"transactions":365,"rating":4.7,"location":"USA","contact":"aws@corp.com"},
        {"id":"V008","name":"AWS","service":"Cloud Hosting","annual_spend":15000,"transactions":2,"rating":4.6,"location":"USA","contact":"aws.billing@company.com"},
        {"id":"V009","name":"Quick Stationary","service":"Office Supplies","annual_spend":4200,"transactions":2,"rating":2.1,"location":"Delhi","contact":"qs@gmail.com"},
        {"id":"V010","name":"Misc Vendor A","service":"Miscellaneous","annual_spend":1800,"transactions":1,"rating":2.0,"location":"Unknown","contact":"misc@temp.com"},
        {"id":"V011","name":"Cognizant","service":"IT Consulting","annual_spend":540000,"transactions":31,"rating":4.1,"location":"Chennai","contact":"cognizant@corp.com"},
        {"id":"V012","name":"HCL Technologies","service":"IT Services","annual_spend":380000,"transactions":24,"rating":4.0,"location":"Noida","contact":"hcl@corp.com"},
        {"id":"V013","name":"HCL Tech","service":"IT Services","annual_spend":88000,"transactions":6,"rating":3.7,"location":"Gurgaon","contact":"hcltech@vendor.com"},
        {"id":"V014","name":"Reliance Jio","service":"Telecom","annual_spend":240000,"transactions":12,"rating":3.9,"location":"Mumbai","contact":"jio@corp.com"},
        {"id":"V015","name":"One-Time Printer Repair","service":"One-Time","annual_spend":3500,"transactions":1,"rating":3.0,"location":"Delhi","contact":"printer@temp.com"},
        {"id":"V016","name":"Microsoft","service":"Software Licensing","annual_spend":760000,"transactions":12,"rating":4.6,"location":"USA","contact":"msft@corp.com"},
        {"id":"V017","name":"Microsoft Corp","service":"Software Licensing","annual_spend":45000,"transactions":3,"rating":4.4,"location":"USA","contact":"microsoft.vendor@email.com"},
        {"id":"V018","name":"Zomato Business","service":"Food Catering","annual_spend":180000,"transactions":48,"rating":4.0,"location":"Bangalore","contact":"zomato@corp.com"},
        {"id":"V019","name":"TestVendor XYZ","service":"Test Services","annual_spend":500,"transactions":1,"rating":1.5,"location":"Unknown","contact":"test@test.com"},
        {"id":"V020","name":"Oracle","service":"Database Software","annual_spend":920000,"transactions":4,"rating":4.3,"location":"USA","contact":"oracle@corp.com"},
    ]

# ── AGENT TOOLS ───────────────────────────────────────────────────────────────

def tool_parse_dataset(vendors):
    total_spend = sum(float(v.get("annual_spend",0) or 0) for v in vendors)
    services = list(set(v.get("service","") for v in vendors if v.get("service")))
    return {
        "total_vendors": len(vendors),
        "total_spend": int(total_spend),
        "unique_services": len(services),
        "top_services": services[:5],
        "avg_spend": int(total_spend / len(vendors)) if vendors else 0
    }

def tool_find_duplicates(vendors):
    duplicates = []
    seen = set()
    for i in range(len(vendors)):
        for j in range(i+1, len(vendors)):
            if (i,j) in seen: continue
            dup, ns, ss, reason = is_duplicate(vendors[i], vendors[j])
            if dup:
                seen.add((i,j))
                s1 = float(vendors[i].get("annual_spend",0) or 0)
                s2 = float(vendors[j].get("annual_spend",0) or 0)
                primary   = vendors[i] if s1 >= s2 else vendors[j]
                secondary = vendors[j] if s1 >= s2 else vendors[i]
                savings = min(s1,s2) * 0.85
                duplicates.append({
                    "primary": primary, "secondary": secondary,
                    "name_similarity": round(ns*100), "service_similarity": round(ss*100),
                    "reason": reason, "potential_savings": round(savings),
                    "priority": "HIGH" if savings>50000 else "MEDIUM" if savings>10000 else "LOW"
                })
    duplicates.sort(key=lambda x: x["potential_savings"], reverse=True)
    return duplicates

def tool_flag_low_value(vendors, dup_secondaries):
    dup_ids = {v.get("id") for v in dup_secondaries}
    low_value = []
    for v in vendors:
        if v.get("id") in dup_ids: continue
        flagged, score, reasons = is_low_value(v)
        if flagged:
            spend = float(v.get("annual_spend",0) or 0)
            low_value.append({
                "vendor": v, "score": score, "reasons": reasons,
                "potential_savings": round(spend*0.9),
                "recommendation": "TERMINATE" if score>=6 else "REVIEW"
            })
    low_value.sort(key=lambda x: x["score"], reverse=True)
    return low_value

def tool_build_action_plan(duplicates, low_value, vendors):
    total_spend   = sum(float(v.get("annual_spend",0) or 0) for v in vendors)
    dup_savings   = sum(d["potential_savings"] for d in duplicates)
    lv_savings    = sum(l["potential_savings"] for l in low_value)
    total_savings = dup_savings + lv_savings
    actions = []
    rank = 1
    for d in duplicates[:6]:
        actions.append({
            "rank": rank, "type": "CONSOLIDATE",
            "action": "Consolidate " + d["secondary"].get("name","") + " into " + d["primary"].get("name",""),
            "savings": d["potential_savings"], "priority": d["priority"],
            "effort": "LOW", "timeline": "30 days"
        })
        rank += 1
    for l in low_value[:5]:
        v = l["vendor"]
        actions.append({
            "rank": rank, "type": l["recommendation"],
            "action": l["recommendation"] + " vendor: " + v.get("name","") + " — " + "; ".join(l["reasons"][:2]),
            "savings": l["potential_savings"], "priority": "HIGH" if l["score"]>=6 else "MEDIUM",
            "effort": "MEDIUM", "timeline": "60 days"
        })
        rank += 1
    actions.sort(key=lambda x: x["savings"], reverse=True)
    for i,a in enumerate(actions): a["rank"] = i+1
    return {
        "total_vendors": len(vendors), "total_spend": int(total_spend),
        "duplicate_pairs": len(duplicates), "low_value_vendors": len(low_value),
        "potential_savings": int(total_savings),
        "savings_percent": round((total_savings/total_spend*100) if total_spend else 0,1),
        "action_plan": actions, "executive_summary": ""
    }

def tool_generate_summary(report, duplicates, low_value):
    llm = get_llm()
    prompt = (
        "You are a procurement intelligence expert.\n"
        "Findings: " + str(report["total_vendors"]) + " vendors analyzed, "
        + str(report["duplicate_pairs"]) + " duplicate pairs found, "
        + str(report["low_value_vendors"]) + " low-value vendors flagged.\n"
        "Total spend: Rs." + str(report["total_spend"]) + "\n"
        "Potential savings: Rs." + str(report["potential_savings"]) + " (" + str(report["savings_percent"]) + "%)\n"
        "Top duplicate pairs: " + ", ".join([d["primary"].get("name","") + " vs " + d["secondary"].get("name","") for d in duplicates[:3]]) + "\n"
        "Write a sharp 2-sentence executive summary. Be specific with numbers. No preamble."
    )
    try:
        return llm.invoke(prompt).content.strip()
    except:
        return ("Identified " + str(report["duplicate_pairs"]) + " duplicate vendor pairs and "
            + str(report["low_value_vendors"]) + " low-value vendors across a Rs."
            + str(report["total_spend"]) + " procurement base. "
            "Immediate consolidation and termination actions can recover Rs."
            + str(report["potential_savings"]) + " (" + str(report["savings_percent"]) + "% of spend).")

# ── AGENTIC PIPELINE (with Streamlit live log) ────────────────────────────────

def run_agent(vendors, log_placeholder, progress_bar):
    logs = []

    def push(icon, label, text):
        logs.append((icon, label, text))
        render_log(log_placeholder, logs)

    def render_log(placeholder, entries):
        html = ""
        for ic, lb, tx in entries:
            html += f"""
            <div style="display:flex;gap:10px;align-items:flex-start;padding:6px 0;
                        border-bottom:1px solid rgba(255,255,255,.04);animation:none">
              <span style="font-family:monospace;font-size:10px;padding:2px 6px;border-radius:2px;
                           flex-shrink:0;letter-spacing:1px;{ic['style']}">{lb}</span>
              <span style="font-family:monospace;font-size:12px;color:#6a8aaa;line-height:1.6">{tx}</span>
            </div>"""
        placeholder.markdown(
            f"""<div style="background:#04080f;border:1px solid #162540;border-radius:6px;
                            padding:16px;max-height:340px;overflow-y:auto">{html}</div>""",
            unsafe_allow_html=True)

    think_style = "background:rgba(0,212,255,.1);color:#00d4ff;border:1px solid rgba(0,212,255,.2)"
    tool_style  = "background:rgba(245,166,35,.1);color:#f5a623;border:1px solid rgba(245,166,35,.2)"
    obs_style   = "background:rgba(0,224,144,.1);color:#00e090;border:1px solid rgba(0,224,144,.2)"
    act_style   = "background:rgba(255,64,96,.1);color:#ff4060;border:1px solid rgba(255,64,96,.2)"
    done_style  = "background:rgba(0,224,144,.15);color:#00e090;border:1px solid rgba(0,224,144,.3)"

    # STEP 1
    push({"style":think_style}, "THINK", f"Received {len(vendors)} vendors. Planning analysis strategy...")
    progress_bar.progress(8)
    time.sleep(0.3)

    # STEP 2
    push({"style":tool_style}, "TOOL", "parse_dataset — Scanning dataset structure, spend distribution, and service taxonomy")
    progress_bar.progress(15)
    time.sleep(0.4)
    stats = tool_parse_dataset(vendors)
    push({"style":obs_style}, "OBS", f"Total spend Rs.{stats['total_spend']:,} across {stats['unique_services']} service categories. Avg vendor spend: Rs.{stats['avg_spend']:,}")
    progress_bar.progress(20)
    time.sleep(0.2)

    # STEP 3
    push({"style":think_style}, "THINK", "High vendor count relative to service categories suggests consolidation opportunity. Running pairwise similarity engine...")
    progress_bar.progress(25)
    time.sleep(0.4)

    # STEP 4
    n_pairs = len(vendors)*(len(vendors)-1)//2
    push({"style":tool_style}, "TOOL", f"find_duplicates — Running name similarity (SequenceMatcher) + service overlap scoring on all {n_pairs} vendor pairs")
    progress_bar.progress(35)
    time.sleep(0.5)
    duplicates = tool_find_duplicates(vendors)
    high_prio  = sum(1 for d in duplicates if d["priority"]=="HIGH")
    dup_savings = sum(d["potential_savings"] for d in duplicates)
    push({"style":obs_style}, "OBS", f"Found {len(duplicates)} duplicate pairs ({high_prio} HIGH priority). Recoverable spend: Rs.{dup_savings:,}")
    progress_bar.progress(50)
    time.sleep(0.3)

    # STEP 5
    if duplicates:
        top = duplicates[0]
        push({"style":think_style}, "THINK",
             f"Highest impact duplicate: {top['secondary'].get('name','')} vs {top['primary'].get('name','')} — "
             f"{top['name_similarity']}% name match, Rs.{top['potential_savings']:,} recoverable. Proceeding to low-value scan...")
    else:
        push({"style":think_style}, "THINK", "No duplicates found. Proceeding to low-value vendor scan...")
    progress_bar.progress(55)
    time.sleep(0.4)

    # STEP 6
    secondary_vendors = [d["secondary"] for d in duplicates]
    push({"style":tool_style}, "TOOL", "flag_low_value — Scoring vendors on spend, transaction frequency, performance rating, and category risk")
    progress_bar.progress(65)
    time.sleep(0.5)
    low_value = tool_flag_low_value(vendors, secondary_vendors)
    terminate = sum(1 for l in low_value if l["recommendation"]=="TERMINATE")
    review    = sum(1 for l in low_value if l["recommendation"]=="REVIEW")
    lv_savings = sum(l["potential_savings"] for l in low_value)
    push({"style":obs_style}, "OBS", f"Flagged {len(low_value)} low-value vendors: {terminate} TERMINATE, {review} REVIEW. Recoverable: Rs.{lv_savings:,}")
    progress_bar.progress(72)
    time.sleep(0.3)

    # STEP 7
    push({"style":tool_style}, "TOOL", "build_action_plan — Ranking all actions by savings potential and implementation effort")
    progress_bar.progress(80)
    time.sleep(0.4)
    report = tool_build_action_plan(duplicates, low_value, vendors)

    # STEP 8
    push({"style":tool_style}, "TOOL", "generate_executive_summary — Invoking LLM to synthesize findings into executive summary")
    progress_bar.progress(88)
    time.sleep(0.3)
    report["executive_summary"] = tool_generate_summary(report, duplicates, low_value)
    push({"style":obs_style}, "OBS",
         f"Executive summary generated. Total optimization potential: Rs.{report['potential_savings']:,} ({report['savings_percent']}% of spend)")
    progress_bar.progress(94)
    time.sleep(0.3)

    # STEP 9
    if report["action_plan"]:
        top_a = report["action_plan"][0]
        push({"style":act_style}, "ACT",
             f"Top autonomous recommendation: {top_a['action']} [{top_a['priority']} PRIORITY, Rs.{top_a['savings']:,} savings]")
        progress_bar.progress(97)
        time.sleep(0.4)

    push({"style":done_style}, "DONE", f"{len(report['action_plan'])} actions ready. Agent handing off to dashboard.")
    progress_bar.progress(100)

    return {"report": report, "duplicates": duplicates, "low_value": low_value, "vendors": vendors}

# ── STREAMLIT UI ──────────────────────────────────────────────────────────────

# Inject custom CSS matching original dark theme
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    background-color: #04080f !important;
    color: #e0eaf8 !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stApp { background-color: #04080f !important; }
.block-container { padding-top: 2rem !important; max-width: 1100px !important; }

/* hide default streamlit elements */
#MainMenu, footer, header { visibility: hidden; }

/* metric cards */
[data-testid="metric-container"] {
    background: #080f1a !important;
    border: 1px solid #162540 !important;
    border-radius: 6px !important;
    padding: 16px !important;
}
[data-testid="metric-container"] label {
    font-family: 'DM Mono', monospace !important;
    font-size: 10px !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    color: #6a8aaa !important;
}
[data-testid="metric-container"] [data-testid="metric-value"] {
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 32px !important;
    color: #00d4ff !important;
}

/* buttons */
.stButton > button {
    background: #00d4ff !important;
    color: #04080f !important;
    border: none !important;
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 18px !important;
    letter-spacing: 2px !important;
    border-radius: 4px !important;
    padding: 12px 28px !important;
    width: 100% !important;
    transition: all .15s !important;
}
.stButton > button:hover { background: #00bbee !important; }

/* text areas */
.stTextArea textarea {
    background: #0d1624 !important;
    border: 1px solid #162540 !important;
    color: #e0eaf8 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 12px !important;
    border-radius: 4px !important;
}

/* tabs */
.stTabs [data-baseweb="tab-list"] {
    background: #0d1624 !important;
    border-radius: 4px !important;
    gap: 4px !important;
    padding: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'DM Mono', monospace !important;
    font-size: 12px !important;
    letter-spacing: 1px !important;
    color: #6a8aaa !important;
    background: transparent !important;
    border-radius: 3px !important;
    padding: 8px 16px !important;
}
.stTabs [aria-selected="true"] {
    background: #162540 !important;
    color: #00d4ff !important;
}

/* dataframe */
[data-testid="stDataFrame"] {
    background: #080f1a !important;
    border: 1px solid #162540 !important;
    border-radius: 6px !important;
}

/* expander */
.streamlit-expanderHeader {
    background: #080f1a !important;
    border: 1px solid #162540 !important;
    border-radius: 6px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 12px !important;
    color: #6a8aaa !important;
}
</style>
""", unsafe_allow_html=True)

def fmt(n):
    return f"Rs.{int(n):,}"

def nav_html():
    return """
    <div style="display:flex;align-items:center;justify-content:space-between;
                padding:20px 0;border-bottom:1px solid #162540;margin-bottom:36px">
      <div style="display:flex;align-items:center;gap:12px">
        <div style="width:36px;height:36px;background:#00d4ff;
                    clip-path:polygon(50% 0%,100% 25%,100% 75%,50% 100%,0% 75%,0% 25%);
                    display:flex;align-items:center;justify-content:center;
                    font-family:'Bebas Neue',sans-serif;font-size:18px;color:#04080f">V</div>
        <div style="font-family:'Bebas Neue',sans-serif;font-size:28px;letter-spacing:2px">
          Vendor<span style="color:#00d4ff">IQ</span></div>
      </div>
      <div style="font-family:'DM Mono',monospace;font-size:11px;color:#6a8aaa;
                  border:1px solid #162540;padding:4px 12px;border-radius:2px;letter-spacing:1px">
        PROCUREMENT INTELLIGENCE AGENT</div>
    </div>
    <div style="margin-bottom:40px">
      <div style="font-family:'DM Mono',monospace;font-size:11px;letter-spacing:3px;
                  color:#00d4ff;text-transform:uppercase;margin-bottom:10px;opacity:.8">
        Track 3 — Cost Intelligence &amp; Autonomous Action</div>
      <div style="font-family:'Bebas Neue',sans-serif;font-size:clamp(40px,6vw,72px);
                  line-height:.95;letter-spacing:1px;margin-bottom:14px">
        DETECT.<br><span style="color:#00d4ff">CONSOLIDATE.</span><br>SAVE.</div>
      <div style="font-size:15px;color:#6a8aaa;max-width:540px;line-height:1.7;font-weight:300">
        AI-powered vendor deduplication and spend optimization.
        Upload 500+ vendors, get a prioritized action plan in seconds.</div>
    </div>"""

st.markdown(nav_html(), unsafe_allow_html=True)

# ── SESSION STATE ─────────────────────────────────────────────────────────────
if "results" not in st.session_state:
    st.session_state.results = None

# ── INPUT SECTION ─────────────────────────────────────────────────────────────
if st.session_state.results is None:
    st.markdown("""
    <div style="background:#080f1a;border:1px solid #162540;border-radius:6px;
                padding:28px;position:relative;overflow:hidden;margin-bottom:24px">
      <div style="position:absolute;top:0;left:0;right:0;height:2px;
                  background:linear-gradient(90deg,transparent,#00d4ff,transparent)"></div>
      <div style="display:flex;align-items:center;gap:10px;margin-bottom:20px">
        <div style="font-family:'DM Mono',monospace;font-size:11px;color:#00d4ff;
                    border:1px solid #00d4ff;width:24px;height:24px;
                    display:flex;align-items:center;justify-content:center;
                    border-radius:2px;opacity:.7">01</div>
        <div style="font-family:'Bebas Neue',sans-serif;font-size:20px;letter-spacing:1px">
          VENDOR DATA INPUT</div>
      </div>
    </div>""", unsafe_allow_html=True)

    tab_sample, tab_csv, tab_json = st.tabs(["USE SAMPLE DATA", "PASTE CSV", "PASTE JSON"])

    vendors_to_run = None

    with tab_sample:
        st.markdown("""
        <div style="background:#0d1624;border:1px solid #162540;border-left:3px solid #00d4ff;
                    border-radius:4px;padding:16px;font-size:13px;color:#6a8aaa;line-height:1.7">
          <strong style="color:#00d4ff">20 pre-loaded vendors</strong> including duplicates
          (Infosys/Infosys Limited, TCS/Tata Consultancy Services, AWS/Amazon Web Services,
          Microsoft/Microsoft Corp, HCL/HCL Tech, Wipro/Wipro Technologies) and low-value/useless
          vendors for a full demo.
        </div>""", unsafe_allow_html=True)
        if st.button("RUN VENDOR INTELLIGENCE AGENT", key="run_sample"):
            vendors_to_run = generate_sample_vendors()

    with tab_csv:
        csv_input = st.text_area(
            "Paste CSV data",
            placeholder="id,name,service,annual_spend,transactions,rating,location,contact\nV001,Infosys Ltd,IT Consulting,850000,42,4.2,Bangalore,info@corp.com\n...",
            height=140, label_visibility="collapsed")
        st.markdown('<div style="font-family:DM Mono,monospace;font-size:11px;color:#4a6080;margin-top:6px">'
                    'Required columns: name, service, annual_spend &nbsp;|&nbsp; Optional: id, transactions, rating, location, contact</div>',
                    unsafe_allow_html=True)
        if st.button("RUN VENDOR INTELLIGENCE AGENT", key="run_csv"):
            if not csv_input.strip():
                st.error("Please paste CSV data first.")
            else:
                vendors_to_run = parse_vendors(csv_input)
                if not vendors_to_run:
                    st.error("Could not parse CSV data.")
                    vendors_to_run = None

    with tab_json:
        json_input = st.text_area(
            "Paste JSON data",
            placeholder='[{"id":"V001","name":"Infosys Ltd","service":"IT Consulting","annual_spend":850000,...}]',
            height=140, label_visibility="collapsed")
        if st.button("RUN VENDOR INTELLIGENCE AGENT", key="run_json"):
            if not json_input.strip():
                st.error("Please paste JSON data first.")
            else:
                vendors_to_run = parse_vendors(json_input)
                if not vendors_to_run:
                    st.error("Could not parse JSON data.")
                    vendors_to_run = None

    # ── RUN AGENT ─────────────────────────────────────────────────────────────
    if vendors_to_run:
        st.markdown("""
        <div style="background:#080f1a;border:1px solid #162540;border-radius:6px;
                    overflow:hidden;margin-bottom:24px">
          <div style="display:flex;align-items:center;gap:10px;padding:14px 20px;
                      border-bottom:1px solid #111d2e;background:#0d1624">
            <div style="width:8px;height:8px;border-radius:50%;background:#00d4ff;
                        animation:pulse 1.5s ease infinite"></div>
            <div style="font-family:'DM Mono',monospace;font-size:12px;letter-spacing:1px;color:#00d4ff">
              AGENT RUNNING — REASONING IN PROGRESS</div>
          </div>
        </div>""", unsafe_allow_html=True)

        log_placeholder = st.empty()
        progress_bar = st.progress(0)

        with st.spinner(""):
            data = run_agent(vendors_to_run, log_placeholder, progress_bar)

        st.session_state.results = data
        st.rerun()

# ── RESULTS SECTION ───────────────────────────────────────────────────────────
else:
    data      = st.session_state.results
    report    = data["report"]
    duplicates= data["duplicates"]
    low_value = data["low_value"]
    vendors   = data["vendors"]

    # KPI row
    c1,c2,c3,c4,c5 = st.columns(5)
    with c1:
        st.metric("TOTAL VENDORS", report["total_vendors"], help="Analyzed")
    with c2:
        st.metric("DUPLICATE PAIRS", report["duplicate_pairs"], help="Overlapping vendors")
    with c3:
        st.metric("LOW-VALUE FLAGS", report["low_value_vendors"], help="Review or terminate")
    with c4:
        st.metric("POTENTIAL SAVINGS", fmt(report["potential_savings"]), help=f"{report['savings_percent']}% of total spend")
    with c5:
        st.metric("TOTAL SPEND", fmt(report["total_spend"]), help="Annual procurement spend")

    st.markdown("<div style='margin-bottom:16px'></div>", unsafe_allow_html=True)

    # Executive summary
    st.markdown(f"""
    <div style="background:#080f1a;border:1px solid #162540;border-left:3px solid #00d4ff;
                border-radius:6px;padding:22px 26px;margin-bottom:28px">
      <div style="font-family:'DM Mono',monospace;font-size:10px;letter-spacing:2px;
                  color:#00d4ff;text-transform:uppercase;margin-bottom:10px;opacity:.8">
        Executive Summary</div>
      <div style="font-size:15px;line-height:1.75;color:#6a8aaa;font-weight:300">
        {report['executive_summary']}</div>
    </div>""", unsafe_allow_html=True)

    # ── ACTION PLAN ──
    st.markdown("""
    <div style="display:flex;align-items:baseline;gap:12px;margin-bottom:16px;
                padding-bottom:12px;border-bottom:1px solid #111d2e">
      <div style="font-family:'Bebas Neue',sans-serif;font-size:22px;letter-spacing:1px">
        PRIORITY ACTION PLAN</div>
    </div>""", unsafe_allow_html=True)

    TYPE_COLORS = {
        "CONSOLIDATE": ("rgba(0,212,255,.1)", "#00d4ff", "rgba(0,212,255,.2)"),
        "TERMINATE":   ("rgba(255,64,96,.1)",  "#ff4060", "rgba(255,64,96,.2)"),
        "REVIEW":      ("rgba(255,176,32,.1)", "#ffb020", "rgba(255,176,32,.2)"),
    }
    PRIORITY_COLORS = {"HIGH": "#ff4060", "MEDIUM": "#ffb020", "LOW": "#6a8aaa"}

    if report["action_plan"]:
        rows_html = ""
        for a in report["action_plan"]:
            tc = TYPE_COLORS.get(a["type"], TYPE_COLORS["REVIEW"])
            pc = PRIORITY_COLORS.get(a["priority"], "#6a8aaa")
            rows_html += f"""
            <tr style="transition:background .2s">
              <td style="padding:12px 14px">
                <div style="font-family:'DM Mono',monospace;font-size:11px;width:28px;height:28px;
                            border-radius:2px;display:flex;align-items:center;justify-content:center;
                            background:#162540;color:#00d4ff">{a['rank']}</div></td>
              <td style="padding:12px 14px">
                <span style="display:inline-block;font-family:'DM Mono',monospace;font-size:10px;
                             letter-spacing:1px;padding:3px 8px;border-radius:2px;
                             background:{tc[0]};color:{tc[1]};border:1px solid {tc[2]}">{a['type']}</span></td>
              <td style="padding:12px 14px;max-width:320px;font-size:13px;color:#6a8aaa">{a['action']}</td>
              <td style="padding:12px 14px;font-family:'DM Mono',monospace;color:#00e090;font-size:13px">{fmt(a['savings'])}</td>
              <td style="padding:12px 14px;color:{pc};font-size:13px;font-weight:500">{a['priority']}</td>
              <td style="padding:12px 14px;font-family:'DM Mono',monospace;font-size:11px;color:#4a6080">{a['timeline']}</td>
            </tr>"""

        st.markdown(f"""
        <div style="overflow-x:auto;margin-bottom:32px">
        <table style="width:100%;border-collapse:collapse">
          <thead>
            <tr style="background:#0d1624">
              {''.join(f'<th style="font-family:DM Mono,monospace;font-size:10px;letter-spacing:2px;color:#4a6080;text-transform:uppercase;padding:10px 14px;text-align:left;border-bottom:1px solid #162540">{h}</th>' for h in ['#','TYPE','ACTION','SAVINGS','PRIORITY','TIMELINE'])}
            </tr>
          </thead>
          <tbody>{rows_html}</tbody>
        </table></div>""", unsafe_allow_html=True)

    # ── DUPLICATE PAIRS ──
    st.markdown("""
    <div style="display:flex;align-items:baseline;gap:12px;margin-bottom:16px;
                padding-bottom:12px;border-bottom:1px solid #111d2e">
      <div style="font-family:'Bebas Neue',sans-serif;font-size:22px;letter-spacing:1px">
        DUPLICATE VENDOR PAIRS</div>
    </div>""", unsafe_allow_html=True)

    if not duplicates:
        st.markdown('<div style="font-family:DM Mono,monospace;font-size:13px;color:#4a6080;'
                    'padding:24px;text-align:center;border:1px dashed #162540;border-radius:4px">'
                    'No duplicate vendors detected</div>', unsafe_allow_html=True)
    else:
        cols = st.columns(min(2, len(duplicates)))
        for idx, d in enumerate(duplicates):
            col = cols[idx % 2]
            p, s = d["primary"], d["secondary"]
            pc_color = "#ff4060" if d["priority"]=="HIGH" else "#ffb020" if d["priority"]=="MEDIUM" else "#6a8aaa"
            with col:
                st.markdown(f"""
                <div style="background:#080f1a;border:1px solid #162540;border-radius:6px;
                            padding:18px;position:relative;overflow:hidden;margin-bottom:14px">
                  <div style="position:absolute;top:0;left:0;right:0;height:2px;
                              background:linear-gradient(90deg,#ff4060,#ffb020)"></div>
                  <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px">
                    <span style="font-family:'DM Mono',monospace;font-size:10px;padding:3px 8px;
                                 background:rgba(255,64,96,.1);color:#ff4060;
                                 border:1px solid rgba(255,64,96,.2);border-radius:2px">DUPLICATE</span>
                    <span style="font-family:'DM Mono',monospace;font-size:10px;
                                 letter-spacing:1px;color:{pc_color}">{d['priority']} PRIORITY</span>
                  </div>
                  <div style="margin-bottom:12px">
                    <div style="display:flex;align-items:center;gap:8px;margin-bottom:7px">
                      <div style="width:8px;height:8px;border-radius:50%;background:#00d4ff;flex-shrink:0"></div>
                      <div>
                        <div style="font-size:13px;font-weight:500;color:#e0eaf8">{p.get('name','')}</div>
                        <div style="font-family:'DM Mono',monospace;font-size:11px;color:#6a8aaa">{p.get('service','')}</div>
                      </div>
                      <div style="margin-left:auto;font-family:'DM Mono',monospace;font-size:11px;color:#4a6080">
                        Rs.{int(float(p.get('annual_spend',0) or 0)):,}</div>
                    </div>
                    <div style="display:flex;align-items:center;gap:8px">
                      <div style="width:8px;height:8px;border-radius:50%;background:#ff4060;flex-shrink:0"></div>
                      <div>
                        <div style="font-size:13px;font-weight:500;color:#e0eaf8">{s.get('name','')}</div>
                        <div style="font-family:'DM Mono',monospace;font-size:11px;color:#6a8aaa">{s.get('service','')}</div>
                      </div>
                      <div style="margin-left:auto;font-family:'DM Mono',monospace;font-size:11px;color:#4a6080">
                        Rs.{int(float(s.get('annual_spend',0) or 0)):,}</div>
                    </div>
                  </div>
                  <div style="display:flex;gap:12px;margin-bottom:10px">
                    <div style="flex:1">
                      <div style="font-family:'DM Mono',monospace;font-size:10px;color:#4a6080;margin-bottom:4px">Name similarity</div>
                      <div style="height:3px;background:#162540;border-radius:2px;overflow:hidden">
                        <div style="height:100%;width:{d['name_similarity']}%;background:#ffb020;border-radius:2px"></div>
                      </div>
                      <div style="font-family:'DM Mono',monospace;font-size:10px;color:#6a8aaa;margin-top:3px">{d['name_similarity']}%</div>
                    </div>
                    <div style="flex:1">
                      <div style="font-family:'DM Mono',monospace;font-size:10px;color:#4a6080;margin-bottom:4px">Service match</div>
                      <div style="height:3px;background:#162540;border-radius:2px;overflow:hidden">
                        <div style="height:100%;width:{d['service_similarity']}%;background:#00d4ff;border-radius:2px"></div>
                      </div>
                      <div style="font-family:'DM Mono',monospace;font-size:10px;color:#6a8aaa;margin-top:3px">{d['service_similarity']}%</div>
                    </div>
                  </div>
                  <div style="font-family:'DM Mono',monospace;font-size:12px;color:#00e090">
                    Savings potential: Rs.{d['potential_savings']:,}</div>
                </div>""", unsafe_allow_html=True)

    # ── LOW VALUE VENDORS ──
    st.markdown("""
    <div style="display:flex;align-items:baseline;gap:12px;margin-bottom:16px;
                padding-bottom:12px;border-bottom:1px solid #111d2e">
      <div style="font-family:'Bebas Neue',sans-serif;font-size:22px;letter-spacing:1px">
        LOW-VALUE &amp; USELESS VENDORS</div>
    </div>""", unsafe_allow_html=True)

    if not low_value:
        st.markdown('<div style="font-family:DM Mono,monospace;font-size:13px;color:#4a6080;'
                    'padding:24px;text-align:center;border:1px dashed #162540;border-radius:4px">'
                    'No low-value vendors detected</div>', unsafe_allow_html=True)
    else:
        lv_cols = st.columns(min(3, len(low_value)))
        for idx, l in enumerate(low_value):
            v = l["vendor"]
            col = lv_cols[idx % 3]
            cls_color = "#ff4060" if l["recommendation"]=="TERMINATE" else "#ffb020"
            with col:
                reasons_html = "".join(
                    f'<div style="font-size:12px;color:#6a8aaa;display:flex;align-items:center;gap:6px;padding:3px 0">'
                    f'<span style="width:4px;height:4px;border-radius:50%;background:#ffb020;flex-shrink:0;display:inline-block"></span>'
                    f'{r}</div>' for r in l["reasons"])
                st.markdown(f"""
                <div style="background:#080f1a;border:1px solid #162540;border-radius:6px;
                            padding:16px;position:relative;overflow:hidden;margin-bottom:12px">
                  <div style="position:absolute;top:0;left:0;right:0;height:2px;background:{cls_color}"></div>
                  <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:4px">
                    <div style="font-size:14px;font-weight:500;color:#e0eaf8">{v.get('name','')}</div>
                    <span style="font-family:'DM Mono',monospace;font-size:10px;padding:2px 8px;border-radius:2px;
                                 background:rgba(255,64,96,.1) if l['recommendation']=='TERMINATE' else rgba(255,176,32,.1);
                                 color:{cls_color};border:1px solid {cls_color}33">{l['recommendation']}</span>
                  </div>
                  <div style="font-family:'DM Mono',monospace;font-size:11px;color:#6a8aaa;margin-bottom:10px">
                    {v.get('service','N/A')}</div>
                  <div style="margin-bottom:10px">{reasons_html}</div>
                  <div style="display:flex;gap:12px;font-family:'DM Mono',monospace;font-size:11px;color:#4a6080">
                    <span>Spend: Rs.{int(float(v.get('annual_spend',0) or 0)):,}</span>
                    <span>Txn: {v.get('transactions',0)}</span>
                    <span>Rating: {v.get('rating','N/A')}</span>
                  </div>
                </div>""", unsafe_allow_html=True)

    # ── FULL VENDOR REGISTRY ──
    st.markdown("""
    <div style="display:flex;align-items:baseline;gap:12px;margin-bottom:16px;
                padding-bottom:12px;border-bottom:1px solid #111d2e">
      <div style="font-family:'Bebas Neue',sans-serif;font-size:22px;letter-spacing:1px">
        FULL VENDOR REGISTRY</div>
    </div>""", unsafe_allow_html=True)

    dup_ids = {d["secondary"].get("id") or d["secondary"].get("name") for d in duplicates}
    lv_ids  = {l["vendor"].get("id") or l["vendor"].get("name") for l in low_value}

    table_rows = []
    for v in vendors:
        vid = v.get("id") or v.get("name")
        is_dup = vid in dup_ids
        is_lv  = vid in lv_ids
        status = "Duplicate" if is_dup else ("Low Value" if is_lv else "Active")
        table_rows.append({
            "ID": v.get("id","-"),
            "Vendor Name": v.get("name",""),
            "Service": v.get("service","-"),
            "Annual Spend": fmt(v.get("annual_spend",0) or 0),
            "Transactions": v.get("transactions","-"),
            "Rating": v.get("rating","-"),
            "Status": status
        })

    import pandas as pd
    df = pd.DataFrame(table_rows)
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.markdown("<div style='margin-top:24px'></div>", unsafe_allow_html=True)
    if st.button("← NEW ANALYSIS", key="reset"):
        st.session_state.results = None
        st.rerun()
