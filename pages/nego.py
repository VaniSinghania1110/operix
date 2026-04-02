import streamlit as st

st.set_page_config(layout="wide", page_title="VendorIQ")

PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>VendorIQ</title>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@300;400;500;600;700&family=IBM+Plex+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}

:root{
  --bg:#0b0d0f;
  --sf:#13161a;
  --card:#181c21;
  --b1:#232830;
  --b2:#2e3540;
  --tx:#e8edf2;
  --mu:#5a6578;
  --dim:#3a4455;
  --blue:#4da6ff;
  --green:#00e090;
  --red:#ff4757;
  --orange:#ff6b35;
  --yellow:#ffc947;
  --teal:#00cfc8;
  --purple:#b06bff;
}

body{
  background:var(--bg);
  color:var(--tx);
  font-family:'IBM Plex Sans',sans-serif;
  min-height:100vh;
}

body::before{
  content:'';
  position:fixed;inset:0;
  background-image:
    linear-gradient(rgba(255,255,255,0.018) 1px,transparent 1px),
    linear-gradient(90deg,rgba(255,255,255,0.018) 1px,transparent 1px);
  background-size:48px 48px;
  pointer-events:none;z-index:0;
}

/* NAV */
nav{
  display:flex;align-items:center;justify-content:space-between;
  padding:18px 40px;
  border-bottom:1px solid var(--b1);
  position:relative;z-index:10;
  backdrop-filter:blur(8px);
}
.nav-left{display:flex;align-items:center;gap:14px}
.nav-logo-box{
  width:36px;height:36px;
  background:linear-gradient(135deg,var(--blue),#2060cc);
  border-radius:8px;
  display:flex;align-items:center;justify-content:center;
  font-family:'IBM Plex Mono',monospace;font-weight:700;font-size:14px;color:#fff;
}
.nav-brand{font-size:22px;font-weight:700;letter-spacing:-0.5px}
.nav-brand span{color:var(--blue)}
.nav-badge{
  display:flex;align-items:center;gap:6px;
  border:1px solid var(--b2);border-radius:20px;
  padding:5px 12px;
  font-family:'IBM Plex Mono',monospace;font-size:10px;letter-spacing:1.5px;color:var(--tx);
}
.nav-badge::before{
  content:'';width:6px;height:6px;border-radius:50%;
  background:var(--green);box-shadow:0 0 8px var(--green);
}
.nav-right{font-family:'IBM Plex Mono',monospace;font-size:11px;color:var(--mu);letter-spacing:0.5px}
.nav-right span{color:var(--dim)}

/* MAIN GRID */
.main{
  display:grid;grid-template-columns:380px 1fr;
  min-height:calc(100vh - 73px);
  position:relative;z-index:1;
}

/* LEFT PANEL */
.left-panel{
  border-right:1px solid var(--b1);
  padding:36px 28px;
  display:flex;flex-direction:column;gap:24px;
}
.hero-eyebrow{
  font-family:'IBM Plex Mono',monospace;font-size:10px;
  font-weight:500;letter-spacing:3px;color:var(--mu);text-transform:uppercase;
  display:flex;align-items:center;gap:10px;margin-bottom:4px;
}
.hero-eyebrow::before{content:'○';font-size:12px}
.hero-heading{
  font-size:44px;font-weight:700;line-height:1.1;letter-spacing:-1.5px;margin-bottom:8px;
}
.hero-heading .l1{color:var(--tx)}
.hero-heading .l2{color:var(--blue)}
.hero-heading .l3{color:var(--green)}
.hero-heading .l4{color:var(--orange)}
.hero-desc{font-size:13px;color:var(--mu);line-height:1.75;margin-bottom:8px}

.tag-row{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:4px}
.tag{
  border:1px solid var(--b2);border-radius:4px;padding:4px 10px;
  font-family:'IBM Plex Mono',monospace;font-size:10px;color:var(--mu);
  transition:border-color 0.2s,color 0.2s;cursor:default;
}
.tag:hover{border-color:var(--blue);color:var(--blue)}

/* FORM */
.field-label{
  font-family:'IBM Plex Mono',monospace;font-size:9px;font-weight:500;
  letter-spacing:2.5px;text-transform:uppercase;color:var(--mu);
  margin-bottom:7px;display:flex;align-items:center;gap:7px;
}
.field-label::before{content:'';width:4px;height:4px;border-radius:50%;background:var(--blue)}

select{
  width:100%;padding:12px 14px;
  background:var(--sf);border:1px solid var(--b2);border-radius:6px;
  color:var(--tx);font-family:'IBM Plex Mono',monospace;font-size:12px;
  outline:none;cursor:pointer;
  transition:border-color 0.2s;appearance:none;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='8' viewBox='0 0 12 8'%3E%3Cpath d='M1 1l5 5 5-5' stroke='%235a6578' stroke-width='1.5' fill='none'/%3E%3C/svg%3E");
  background-repeat:no-repeat;background-position:right 14px center;padding-right:36px;
}
select:focus{border-color:var(--blue)}

textarea{
  width:100%;min-height:130px;
  background:var(--sf);border:1px solid var(--b2);border-radius:6px;
  color:var(--tx);font-family:'IBM Plex Mono',monospace;font-size:11px;
  padding:12px;outline:none;resize:vertical;line-height:1.6;
  transition:border-color 0.2s;
}
textarea:focus{border-color:var(--blue)}

.run-btn{
  width:100%;padding:16px 24px;
  background:var(--blue);border:none;border-radius:6px;
  font-family:'IBM Plex Mono',monospace;font-size:12px;font-weight:600;
  letter-spacing:2px;text-transform:uppercase;color:#fff;
  cursor:pointer;transition:all 0.2s;
  display:flex;align-items:center;justify-content:center;gap:10px;
}
.run-btn:hover{background:#5db5ff;box-shadow:0 0 24px rgba(77,166,255,0.35);transform:translateY(-1px)}
.run-btn:disabled{background:var(--b2);color:var(--mu);cursor:not-allowed;transform:none;box-shadow:none}

/* RIGHT PANEL */
.right-panel{padding:36px 32px;overflow-y:auto;display:flex;flex-direction:column;gap:20px}

.rp-header{
  font-family:'IBM Plex Mono',monospace;font-size:10px;font-weight:500;
  letter-spacing:3px;color:var(--mu);text-transform:uppercase;
  padding-bottom:16px;border-bottom:1px solid var(--b1);
}

/* MODULE CARDS (idle state) */
.module-list{display:flex;flex-direction:column;gap:0}
.mod-card{
  display:flex;align-items:center;gap:14px;padding:16px 14px;
  border-bottom:1px solid var(--b1);position:relative;
  transition:background 0.15s;cursor:default;
  animation:fadeInRow 0.4s ease both;
}
.mod-card:hover{background:var(--sf)}
.mod-card::before{
  content:'';position:absolute;left:0;top:0;bottom:0;
  width:3px;border-radius:0 2px 2px 0;
}
.mc-red::before{background:var(--red)}
.mc-green::before{background:var(--green)}
.mc-blue::before{background:var(--blue)}
.mc-yellow::before{background:var(--yellow)}
.mc-teal::before{background:var(--teal)}
.mc-purple::before{background:var(--purple)}
.mc-orange::before{background:var(--orange)}
.mod-card:nth-child(1){animation-delay:.05s}
.mod-card:nth-child(2){animation-delay:.1s}
.mod-card:nth-child(3){animation-delay:.15s}
.mod-card:nth-child(4){animation-delay:.2s}
.mod-card:nth-child(5){animation-delay:.25s}
.mod-card:nth-child(6){animation-delay:.3s}
.mod-card:nth-child(7){animation-delay:.35s}
@keyframes fadeInRow{from{opacity:0;transform:translateX(12px)}to{opacity:1;transform:translateX(0)}}

.mod-icon{
  width:42px;height:42px;border-radius:8px;
  display:flex;align-items:center;justify-content:center;font-size:18px;
  flex-shrink:0;background:var(--sf);border:1px solid var(--b2);
}
.mc-red .mod-icon{background:rgba(255,71,87,.12);border-color:rgba(255,71,87,.25)}
.mc-green .mod-icon{background:rgba(0,224,144,.1);border-color:rgba(0,224,144,.2)}
.mc-blue .mod-icon{background:rgba(77,166,255,.1);border-color:rgba(77,166,255,.2)}
.mc-yellow .mod-icon{background:rgba(255,201,71,.1);border-color:rgba(255,201,71,.2)}
.mc-teal .mod-icon{background:rgba(0,207,200,.1);border-color:rgba(0,207,200,.2)}
.mc-purple .mod-icon{background:rgba(176,107,255,.1);border-color:rgba(176,107,255,.2)}
.mc-orange .mod-icon{background:rgba(255,107,53,.1);border-color:rgba(255,107,53,.2)}

.mod-info{flex:1;min-width:0}
.mod-name{font-size:14px;font-weight:600;margin-bottom:3px}
.mod-desc{font-size:11px;color:var(--mu);font-family:'IBM Plex Mono',monospace;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.status-pill{
  padding:4px 10px;border-radius:3px;
  font-family:'IBM Plex Mono',monospace;font-size:9px;font-weight:600;letter-spacing:1.5px;text-transform:uppercase;flex-shrink:0;
}
.s-active{background:rgba(0,224,144,.15);color:var(--green);border:1px solid rgba(0,224,144,.3)}
.s-idle{background:rgba(90,101,120,.2);color:var(--mu);border:1px solid var(--b2)}
.s-running{background:rgba(77,166,255,.15);color:var(--blue);border:1px solid rgba(77,166,255,.3);animation:blink 1s ease-in-out infinite}
@keyframes blink{0%,100%{opacity:1}50%{opacity:.5}}

/* LOGS */
.log-section{display:none}
.log-section.on{display:block}
.log-header{
  font-family:'IBM Plex Mono',monospace;font-size:9px;font-weight:500;
  letter-spacing:2.5px;text-transform:uppercase;color:var(--mu);
  margin-bottom:12px;display:flex;align-items:center;gap:8px;
}
.log-header::before{content:'';width:4px;height:4px;border-radius:50%;background:var(--blue)}
.log-entry{
  display:flex;align-items:flex-start;gap:10px;
  padding:8px 12px;margin-bottom:6px;
  background:var(--sf);border-left:3px solid var(--blue);border-radius:0 4px 4px 0;
  font-family:'IBM Plex Mono',monospace;font-size:11px;color:var(--tx);line-height:1.5;
  animation:slideIn 0.3s ease both;
}
.log-entry.ok{border-left-color:var(--green)}
.log-entry.warn{border-left-color:var(--yellow)}
.log-ts{color:var(--mu);font-size:10px;min-width:50px}
@keyframes slideIn{from{opacity:0;transform:translateX(-8px)}to{opacity:1;transform:translateX(0)}}

/* RESULTS */
.results-section{display:none}
.results-section.on{display:block;animation:fadeUp 0.5s ease both}
@keyframes fadeUp{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}

.res-title-row{
  display:flex;align-items:center;justify-content:space-between;
  padding-bottom:16px;border-bottom:1px solid var(--b1);margin-bottom:16px;
}
.res-main-title{font-size:20px;font-weight:700;letter-spacing:-0.5px}
.res-badge{
  padding:5px 12px;background:rgba(0,224,144,.12);
  border:1px solid rgba(0,224,144,.3);border-radius:3px;
  font-family:'IBM Plex Mono',monospace;font-size:9px;font-weight:600;letter-spacing:2px;text-transform:uppercase;color:var(--green);
}

/* KPI GRID */
.kpi-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:16px}
.kpi-card{
  background:var(--sf);border:1px solid var(--b1);border-radius:6px;padding:16px;
  position:relative;overflow:hidden;
}
.kpi-card::before{
  content:'';position:absolute;left:0;top:0;bottom:0;width:3px;border-radius:0 2px 2px 0;
}
.kpi-blue::before{background:var(--blue)}
.kpi-red::before{background:var(--red)}
.kpi-yellow::before{background:var(--yellow)}
.kpi-green::before{background:var(--green)}
.kpi-label{font-family:'IBM Plex Mono',monospace;font-size:9px;letter-spacing:2px;text-transform:uppercase;color:var(--mu);margin-bottom:8px}
.kpi-val{font-size:28px;font-weight:700;letter-spacing:-1px;line-height:1}
.kpi-blue .kpi-val{color:var(--blue)}
.kpi-red .kpi-val{color:var(--red)}
.kpi-yellow .kpi-val{color:var(--yellow)}
.kpi-green .kpi-val{color:var(--green)}

/* RESULT CARDS */
.rcard{
  background:var(--sf);border:1px solid var(--b1);border-radius:6px;
  padding:20px;margin-bottom:12px;position:relative;
}
.rcard::before{
  content:'';position:absolute;left:0;top:0;bottom:0;width:3px;border-radius:0 2px 2px 0;
}
.rcard-blue::before{background:var(--blue)}
.rcard-green::before{background:var(--green)}
.rcard-orange::before{background:var(--orange)}
.rcard-red::before{background:var(--red)}
.rcard-purple::before{background:var(--purple)}

.rcard-header{
  font-family:'IBM Plex Mono',monospace;font-size:9px;font-weight:500;
  letter-spacing:2.5px;text-transform:uppercase;color:var(--mu);
  margin-bottom:12px;display:flex;align-items:center;gap:7px;
}
.rcard-header::before{content:'';width:4px;height:4px;border-radius:50%;background:currentColor}

.rcard-content{font-size:13px;color:var(--mu);line-height:1.8}
.rcard-content strong{color:var(--tx);font-weight:600}

/* TABLE */
.vtable{width:100%;border-collapse:collapse;margin-top:8px;font-size:12px}
.vtable th{
  font-family:'IBM Plex Mono',monospace;font-size:9px;letter-spacing:2px;text-transform:uppercase;
  color:var(--mu);padding:10px 12px;border-bottom:1px solid var(--b2);text-align:left;
}
.vtable td{padding:10px 12px;border-bottom:1px solid var(--b1);font-family:'IBM Plex Mono',monospace;font-size:11px;color:var(--tx)}
.vtable tr:hover td{background:var(--card)}

.chip{
  display:inline-flex;align-items:center;gap:4px;
  padding:3px 8px;background:rgba(255,71,87,.1);border:1px solid rgba(255,71,87,.25);
  border-radius:3px;font-family:'IBM Plex Mono',monospace;font-size:9px;color:var(--red);
}
.chip.ok{background:rgba(0,224,144,.1);border-color:rgba(0,224,144,.25);color:var(--green)}
.chip.warn{background:rgba(255,201,71,.1);border-color:rgba(255,201,71,.25);color:var(--yellow)}

.reset-btn{
  width:100%;padding:13px 24px;
  background:transparent;border:1px solid var(--b2);border-radius:6px;
  font-family:'IBM Plex Mono',monospace;font-size:10px;font-weight:500;
  letter-spacing:2px;text-transform:uppercase;color:var(--mu);cursor:pointer;
  transition:all 0.2s;margin-top:4px;
}
.reset-btn:hover{border-color:var(--blue);color:var(--blue)}

.err-box{
  background:rgba(255,71,87,.08);border:1px solid rgba(255,71,87,.25);
  border-radius:6px;padding:16px;
  font-family:'IBM Plex Mono',monospace;font-size:12px;color:var(--red);line-height:1.6;
}
</style>
</head>
<body>

<nav>
  <div class="nav-left">
    <div class="nav-logo-box">V</div>
    <div class="nav-brand">Vendor<span>IQ</span></div>
    <div class="nav-badge">AI PROCUREMENT INTELLIGENCE</div>
  </div>
  <div class="nav-right">Claude AI &nbsp;<span>·</span>&nbsp; Duplicate Detection &nbsp;<span>·</span>&nbsp; Negotiation Engine</div>
</nav>

<div class="main">

  <!-- LEFT PANEL -->
  <div class="left-panel">
    <div>
      <div class="hero-eyebrow">AI-Powered Vendor Operations</div>
      <div class="hero-heading">
        <div class="l1">One Dataset.</div>
        <div class="l2">Detect.</div>
        <div class="l3">Negotiate.</div>
        <div class="l4">Save.</div>
      </div>
      <p class="hero-desc">VendorIQ uses AI to analyse your vendor list, detect duplicates, flag low-value contracts, and generate a full negotiation playbook — powered by Claude.</p>
    </div>

    <div class="tag-row">
      <span class="tag">Duplicate Detection</span>
      <span class="tag">Spend Analysis</span>
      <span class="tag">Contract Review</span>
      <span class="tag">Negotiation Playbook</span>
      <span class="tag">Consolidation Plan</span>
    </div>

    <!-- FORM -->
    <div id="input-section">
      <div style="margin-bottom:16px">
        <div class="field-label">Data Mode</div>
        <select id="mode" onchange="handleModeChange()">
          <option value="sample">Use Sample Data</option>
          <option value="csv">Paste CSV</option>
          <option value="json">Paste JSON</option>
        </select>
      </div>

      <div id="paste-area" style="display:none;margin-bottom:16px">
        <div class="field-label">Paste Vendor Data</div>
        <textarea id="vendor-input" placeholder="Paste your CSV or JSON here..."></textarea>
      </div>

      <button class="run-btn" id="run-btn" onclick="runAnalysis()">
        <span>→</span> Run Vendor Analysis
      </button>
    </div>
  </div>

  <!-- RIGHT PANEL -->
  <div class="right-panel" id="right-panel">

    <!-- Module list (idle) -->
    <div id="module-list">
      <div class="rp-header">Analysis Modules — 7 Active</div>
      <div class="module-list">
        <div class="mod-card mc-red"><div class="mod-icon">🔍</div><div class="mod-info"><div class="mod-name">Duplicate Detector</div><div class="mod-desc">Fuzzy-match vendor names and tax IDs</div></div><div class="status-pill s-active" id="st-0">ACTIVE</div></div>
        <div class="mod-card mc-green"><div class="mod-icon">💰</div><div class="mod-info"><div class="mod-name">Spend Analyser</div><div class="mod-desc">Classify spend tiers and flag low-value contracts</div></div><div class="status-pill s-active" id="st-1">ACTIVE</div></div>
        <div class="mod-card mc-blue"><div class="mod-icon">📊</div><div class="mod-info"><div class="mod-name">Risk Scorer</div><div class="mod-desc">Assess vendor concentration and dependency risk</div></div><div class="status-pill s-active" id="st-2">ACTIVE</div></div>
        <div class="mod-card mc-yellow"><div class="mod-icon">🤝</div><div class="mod-info"><div class="mod-name">Negotiation Planner</div><div class="mod-desc">Generate playbooks and saving targets per vendor</div></div><div class="status-pill s-active" id="st-3">ACTIVE</div></div>
        <div class="mod-card mc-teal"><div class="mod-icon">🏭</div><div class="mod-info"><div class="mod-name">Consolidation Engine</div><div class="mod-desc">Recommend vendor merges and contract rationalisation</div></div><div class="status-pill s-active" id="st-4">ACTIVE</div></div>
        <div class="mod-card mc-purple"><div class="mod-icon">📋</div><div class="mod-info"><div class="mod-name">Report Generator</div><div class="mod-desc">Compile findings into executive summary</div></div><div class="status-pill s-active" id="st-5">ACTIVE</div></div>
        <div class="mod-card mc-orange"><div class="mod-icon">⚡</div><div class="mod-info"><div class="mod-name">Action Prioritiser</div><div class="mod-desc">Rank actions by ROI and implementation effort</div></div><div class="status-pill s-active" id="st-6">ACTIVE</div></div>
      </div>
    </div>

    <!-- Logs (shown during run) -->
    <div class="log-section" id="log-section">
      <div class="log-header">Agent Reasoning Log</div>
      <div id="agent-log"></div>
    </div>

    <!-- Results -->
    <div class="results-section" id="results-section">
      <div class="res-title-row">
        <div class="res-main-title">Analysis Complete</div>
        <div class="res-badge">✓ Report Ready</div>
      </div>

      <!-- KPIs -->
      <div class="kpi-grid" id="kpi-grid"></div>

      <!-- AI Result Cards -->
      <div id="result-cards"></div>

      <button class="reset-btn" onclick="resetApp()">← New Analysis</button>
    </div>

  </div>
</div>

<script>
var logCount = 0;
var logStart = Date.now();

function G(id){return document.getElementById(id)}

function handleModeChange(){
  var m = G("mode").value;
  G("paste-area").style.display = (m === "sample") ? "none" : "block";
}

function addLog(text, type){
  type = type || "info";
  var el = document.createElement("div");
  el.className = "log-entry " + (type==="ok"?"ok":type==="warn"?"warn":"");
  var elapsed = ((Date.now() - logStart)/1000).toFixed(1) + "s";
  el.innerHTML = "<span class='log-ts'>+" + elapsed + "</span><span>" + text + "</span>";
  G("agent-log").appendChild(el);
  G("agent-log").scrollTop = G("agent-log").scrollHeight;
}

function getSampleData(){
  return [
    {id:"V001",name:"Infosys Ltd",category:"IT Services",spend:850000,contracts:3,country:"India"},
    {id:"V002",name:"Infosys Limited",category:"IT Services",spend:120000,contracts:1,country:"India"},
    {id:"V003",name:"Tata Consultancy Services",category:"IT Consulting",spend:650000,contracts:2,country:"India"},
    {id:"V004",name:"TCS",category:"IT Consulting",spend:95000,contracts:1,country:"India"},
    {id:"V005",name:"AWS",category:"Cloud",spend:420000,contracts:1,country:"USA"},
    {id:"V006",name:"Amazon Web Services",category:"Cloud",spend:85000,contracts:1,country:"USA"},
    {id:"V007",name:"ABC Services",category:"Facilities",spend:10000,contracts:1,country:"India"},
    {id:"V008",name:"XYZ Logistics",category:"Logistics",spend:18000,contracts:1,country:"India"},
    {id:"V009",name:"Wipro Technologies",category:"IT Services",spend:380000,contracts:2,country:"India"},
    {id:"V010",name:"Microsoft",category:"Software",spend:510000,contracts:3,country:"USA"}
  ];
}

async function runAnalysis(){
  G("run-btn").disabled = true;
  G("input-section").style.display = "none";
  G("module-list").style.display = "none";
  G("log-section").classList.add("on");
  logStart = Date.now();

  addLog("Initialising VendorIQ analysis engine...");

  var mode = G("mode").value;
  var vendors;

  try{
    if(mode === "sample"){
      vendors = getSampleData();
      addLog("Loaded sample vendor dataset — 10 vendors");
    } else {
      var raw = G("vendor-input").value.trim();
      if(!raw){ throw new Error("No data pasted"); }
      if(mode === "csv"){
        vendors = parseCSV(raw);
        addLog("Parsed CSV — " + vendors.length + " vendors found");
      } else {
        vendors = JSON.parse(raw);
        addLog("Parsed JSON — " + vendors.length + " vendors found");
      }
    }
  } catch(e){
    addLog("❌ Data parse error: " + e.message, "warn");
    showError("Could not parse your data. Please check the format and try again.<br><br>" + e.message);
    return;
  }

  addLog("Sending to Claude AI for deep analysis...");
  addLog("Running duplicate detection module...", "info");
  addLog("Running spend classification module...", "info");
  addLog("Running negotiation strategy engine...", "info");

  var prompt = buildPrompt(vendors);

  try{
    var result = await callClaude(prompt);
    addLog("Claude analysis complete ✓", "ok");
    addLog("Parsing and rendering results...", "ok");
    renderResults(result, vendors);
  } catch(e){
    addLog("❌ API error: " + e.message, "warn");
    showError("Claude API error: " + e.message + "<br><br>Make sure you have a valid API key configured.");
  }
}

function buildPrompt(vendors){
  return `You are VendorIQ, an expert AI procurement analyst. Analyse the following vendor dataset and return a detailed JSON report.

VENDOR DATA:
${JSON.stringify(vendors, null, 2)}

Return ONLY a valid JSON object (no markdown, no explanation) with this exact structure:
{
  "summary": "2-3 sentence executive summary of findings",
  "kpis": {
    "total_vendors": <number>,
    "duplicate_pairs": <number>,
    "low_value_count": <number>,
    "total_savings_inr": <number>
  },
  "duplicates": [
    {"vendor_a": "name", "vendor_b": "name", "similarity": <0-100>, "reason": "why they are duplicates", "action": "recommended action", "saving_inr": <number>}
  ],
  "low_value_vendors": [
    {"id": "V001", "name": "name", "spend": <number>, "action": "Terminate|Review|Consolidate", "reason": "why"}
  ],
  "action_plan": [
    {"priority": 1, "action": "description", "saving_inr": <number>, "effort": "Low|Medium|High"}
  ],
  "negotiation_targets": [
    {"vendor": "name", "current_spend": <number>, "target_saving_pct": <number>, "strategy": "negotiation approach"}
  ],
  "vendor_registry": [
    {"id": "V001", "name": "name", "category": "category", "spend": <number>, "status": "Keep|Review|Terminate|Duplicate"}
  ]
}`;
}

async function callClaude(prompt){
  var resp = await fetch("https://api.anthropic.com/v1/messages",{
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body: JSON.stringify({
      model:"claude-sonnet-4-20250514",
      max_tokens:2000,
      messages:[{role:"user", content: prompt}]
    })
  });
  if(!resp.ok){
    var err = await resp.json();
    throw new Error(err.error?.message || ("HTTP " + resp.status));
  }
  var data = await resp.json();
  var text = data.content.map(b => b.text || "").join("");
  text = text.replace(/```json|```/g,"").trim();
  return JSON.parse(text);
}

function renderResults(d, vendors){
  G("log-section").classList.remove("on");
  G("results-section").classList.add("on");

  // KPIs
  var savings = d.kpis.total_savings_inr;
  var savFmt = savings >= 100000 ? "₹" + (savings/100000).toFixed(1) + "L" : "₹" + savings.toLocaleString();
  G("kpi-grid").innerHTML =
    kpiCard("Total Vendors", d.kpis.total_vendors, "kpi-blue") +
    kpiCard("Duplicate Pairs", d.kpis.duplicate_pairs, "kpi-red") +
    kpiCard("Low Value", d.kpis.low_value_count, "kpi-yellow") +
    kpiCard("Est. Savings", savFmt, "kpi-green");

  var html = "";

  // Executive summary
  html += rcard("blue", "Executive Summary",
    "<p class='rcard-content'>" + d.summary + "</p>");

  // Action plan
  var apRows = (d.action_plan||[]).map(function(a,i){
    var effortColor = a.effort==="Low"?"ok":a.effort==="High"?"":"warn";
    var sav = a.saving_inr >= 100000 ? "₹"+(a.saving_inr/100000).toFixed(1)+"L" : "₹"+a.saving_inr.toLocaleString();
    return "<tr><td style='color:var(--blue);font-weight:600'>" + (i+1) + "</td><td>" + a.action + "</td><td><span class='chip ok'>"+sav+"</span></td><td><span class='chip "+effortColor+"'>"+a.effort+"</span></td></tr>";
  }).join("");
  html += rcard("green", "Priority Action Plan",
    "<table class='vtable'><tr><th>#</th><th>Action</th><th>Saving</th><th>Effort</th></tr>" + apRows + "</table>");

  // Duplicates
  var dupRows = (d.duplicates||[]).map(function(dp){
    var sim = dp.similarity || "—";
    return "<tr><td style='color:var(--orange)'>" + dp.vendor_a + "</td><td style='color:var(--mu)'>↔</td><td style='color:var(--orange)'>" + dp.vendor_b + "</td><td>" + sim + "%</td><td style='color:var(--mu);font-size:10px'>" + dp.action + "</td></tr>";
  }).join("");
  html += rcard("orange", "Duplicate Vendors",
    dupRows ? "<table class='vtable'><tr><th>Vendor A</th><th></th><th>Vendor B</th><th>Match</th><th>Action</th></tr>" + dupRows + "</table>"
            : "<p class='rcard-content'>No duplicate vendors detected.</p>");

  // Low value
  var lvRows = (d.low_value_vendors||[]).map(function(v){
    var actionColor = v.action==="Terminate"?"":"warn";
    return "<tr><td>" + (v.id||"—") + "</td><td>" + v.name + "</td><td style='color:var(--mu)'>₹" + (v.spend||0).toLocaleString() + "</td><td><span class='chip "+actionColor+"'>"+v.action+"</span></td><td style='color:var(--mu);font-size:10px'>" + (v.reason||"") + "</td></tr>";
  }).join("");
  html += rcard("red", "Low Value Vendors",
    lvRows ? "<table class='vtable'><tr><th>ID</th><th>Vendor</th><th>Spend</th><th>Action</th><th>Reason</th></tr>" + lvRows + "</table>"
           : "<p class='rcard-content'>No low-value vendors flagged.</p>");

  // Negotiation targets
  var negRows = (d.negotiation_targets||[]).map(function(n){
    return "<tr><td style='color:var(--tx)'>" + n.vendor + "</td><td>₹" + (n.current_spend||0).toLocaleString() + "</td><td style='color:var(--green)'>" + n.target_saving_pct + "%</td><td style='color:var(--mu);font-size:10px'>" + n.strategy + "</td></tr>";
  }).join("");
  if(negRows){
    html += rcard("purple", "Negotiation Targets",
      "<table class='vtable'><tr><th>Vendor</th><th>Spend</th><th>Target Save</th><th>Strategy</th></tr>" + negRows + "</table>");
  }

  // Full registry
  var regRows = (d.vendor_registry||[]).map(function(v){
    var sc = v.status==="Keep"?"ok":v.status==="Terminate"?"":v.status==="Duplicate"?"warn":"warn";
    return "<tr><td style='color:var(--mu)'>" + (v.id||"") + "</td><td>" + v.name + "</td><td style='color:var(--mu)'>" + (v.category||"—") + "</td><td>₹" + (v.spend||0).toLocaleString() + "</td><td><span class='chip "+sc+"'>"+v.status+"</span></td></tr>";
  }).join("");
  html += rcard("blue", "Full Vendor Registry",
    regRows ? "<table class='vtable'><tr><th>ID</th><th>Name</th><th>Category</th><th>Spend</th><th>Status</th></tr>" + regRows + "</table>"
            : "<p class='rcard-content'>No data available.</p>");

  G("result-cards").innerHTML = html;
}

function kpiCard(label, val, cls){
  return "<div class='kpi-card "+cls+"'><div class='kpi-label'>"+label+"</div><div class='kpi-val'>"+val+"</div></div>";
}

function rcard(color, label, body){
  return "<div class='rcard rcard-"+color+"'><div class='rcard-header' style='color:var(--"+colorVar(color)+")'>" + label + "</div>" + body + "</div>";
}

function colorVar(c){
  var m={blue:"blue",green:"green",orange:"orange",red:"red",purple:"purple"};
  return m[c]||"blue";
}

function parseCSV(raw){
  var lines = raw.trim().split("\n");
  var headers = lines[0].split(",").map(function(h){return h.trim().toLowerCase().replace(/[^a-z0-9_]/g,"_")});
  return lines.slice(1).map(function(line,i){
    var vals = line.split(",");
    var obj = {id:"V"+(i+1).toString().padStart(3,"0")};
    headers.forEach(function(h,j){
      var v = (vals[j]||"").trim().replace(/^"|"$/g,"");
      obj[h] = isNaN(v) ? v : Number(v);
    });
    return obj;
  });
}

function showError(msg){
  G("log-section").classList.remove("on");
  G("results-section").classList.add("on");
  G("kpi-grid").innerHTML = "";
  G("result-cards").innerHTML = "<div class='err-box'>⚠ &nbsp;" + msg + "</div><button class='reset-btn' onclick='resetApp()' style='margin-top:12px'>← Try Again</button>";
}

function resetApp(){
  location.reload();
}
</script>
</body>
</html>
"""

st.components.v1.html(PAGE, height=1000, scrolling=True)
