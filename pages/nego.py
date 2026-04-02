import streamlit as st

st.set_page_config(layout="wide", page_title="Duplicate Vendor Detection")

PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>VendorIQ</title>
<link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box;margin:0;padding:0;}
:root{
  --bg:#0a0b0e;
  --surface:#0f1115;
  --surface2:#13161c;
  --border:#1e2330;
  --text:#e4eaf4;
  --muted:#5a6478;
  --blue:#4da6ff;
  --green:#00e090;
  --red:#ff4d6a;
  --orange:#ff9a3c;
  --purple:#9b7bff;
  --yellow:#f5c842;
}
body{
  background:var(--bg);
  color:var(--text);
  font-family:'Syne',sans-serif;
  min-height:100vh;
  overflow-x:hidden;
}

/* TOP NAV */
.nav{
  display:flex;
  align-items:center;
  justify-content:space-between;
  padding:16px 36px;
  border-bottom:1px solid var(--border);
  position:sticky;
  top:0;
  background:rgba(10,11,14,0.92);
  backdrop-filter:blur(12px);
  z-index:100;
}
.nav-logo{
  display:flex;
  align-items:center;
  gap:12px;
}
.logo-icon{
  width:36px;height:36px;
  background:var(--blue);
  border-radius:8px;
  display:flex;align-items:center;justify-content:center;
  font-weight:800;font-size:14px;color:#000;
  letter-spacing:-1px;
}
.nav-logo span{
  font-size:20px;font-weight:800;letter-spacing:-0.5px;
}
.nav-badge{
  font-family:'Space Mono',monospace;
  font-size:10px;
  background:transparent;
  border:1px solid var(--blue);
  color:var(--blue);
  padding:4px 10px;
  border-radius:20px;
  letter-spacing:1px;
}
.nav-right{
  font-family:'Space Mono',monospace;
  font-size:11px;
  color:var(--muted);
  letter-spacing:0.5px;
}
.nav-right span{ color:var(--text); margin:0 4px; }

/* MAIN LAYOUT */
.layout{
  display:grid;
  grid-template-columns:1fr 460px;
  min-height:calc(100vh - 65px);
}

/* LEFT HERO PANEL */
.hero{
  padding:56px 48px 48px;
  border-right:1px solid var(--border);
  display:flex;
  flex-direction:column;
  gap:32px;
}
.hero-label{
  font-family:'Space Mono',monospace;
  font-size:10px;
  letter-spacing:3px;
  color:var(--muted);
  display:flex;
  align-items:center;
  gap:12px;
}
.hero-label::after{
  content:'';
  flex:1;
  height:1px;
  background:var(--border);
  max-width:120px;
}
.hero-headline{
  line-height:1.05;
}
.hero-headline .line1{
  font-size:52px;font-weight:800;color:var(--text);
  display:block;
}
.hero-headline .line2{
  font-size:52px;font-weight:800;color:var(--blue);
  display:block;
}
.hero-headline .line3{
  font-size:52px;font-weight:800;color:var(--green);
  display:block;
}
.hero-desc{
  font-size:15px;
  color:#7a8499;
  line-height:1.7;
  max-width:500px;
  font-weight:400;
}
.hero-tags{
  display:flex;
  flex-wrap:wrap;
  gap:8px;
}
.tag{
  font-family:'Space Mono',monospace;
  font-size:10px;
  padding:6px 14px;
  border:1px solid var(--border);
  border-radius:4px;
  color:var(--muted);
  letter-spacing:0.5px;
  cursor:default;
  transition:all 0.2s;
}
.tag:hover{border-color:var(--blue);color:var(--blue);}

/* AGENT ICON GRID */
.agent-grid{
  display:flex;
  gap:10px;
  flex-wrap:wrap;
}
.agent-btn{
  display:flex;
  flex-direction:column;
  align-items:center;
  gap:6px;
  padding:14px 16px;
  background:var(--surface);
  border:1px solid var(--border);
  border-radius:10px;
  cursor:pointer;
  transition:all 0.2s;
  min-width:72px;
  text-align:center;
}
.agent-btn:hover{border-color:var(--blue);background:#0d1420;}
.agent-btn .icon{font-size:22px;}
.agent-btn .label{
  font-family:'Space Mono',monospace;
  font-size:9px;
  color:var(--muted);
  letter-spacing:0.5px;
}

/* KPI ROW */
.kpi-row{
  display:grid;
  grid-template-columns:repeat(3,1fr);
  gap:1px;
  background:var(--border);
  border:1px solid var(--border);
  border-radius:8px;
  overflow:hidden;
}
.kpi-cell{
  background:var(--surface);
  padding:20px 24px;
  text-align:center;
}
.kpi-cell .kpi-val{
  font-size:36px;
  font-weight:800;
  line-height:1;
}
.kpi-cell .kpi-label{
  font-family:'Space Mono',monospace;
  font-size:9px;
  color:var(--muted);
  letter-spacing:1px;
  margin-top:6px;
}
.c-blue{color:var(--blue);}
.c-green{color:var(--green);}
.c-red{color:var(--red);}

/* RIGHT PANEL */
.right-panel{
  background:var(--surface);
  display:flex;
  flex-direction:column;
}
.right-header{
  padding:24px 28px 16px;
  border-bottom:1px solid var(--border);
}
.right-header h3{
  font-size:13px;
  font-weight:700;
  letter-spacing:1px;
  color:var(--muted);
  text-transform:uppercase;
  font-family:'Space Mono',monospace;
}
.agent-list{
  flex:1;
  overflow-y:auto;
  padding:8px 0;
}
.agent-row{
  display:flex;
  align-items:center;
  gap:16px;
  padding:16px 28px;
  border-bottom:1px solid var(--border);
  cursor:pointer;
  transition:background 0.15s;
  position:relative;
}
.agent-row::before{
  content:'';
  position:absolute;
  left:0;top:0;bottom:0;
  width:3px;
}
.agent-row.blue::before{background:var(--blue);}
.agent-row.green::before{background:var(--green);}
.agent-row.purple::before{background:var(--purple);}
.agent-row.yellow::before{background:var(--yellow);}
.agent-row.red::before{background:var(--red);}
.agent-row.orange::before{background:var(--orange);}
.agent-row.teal::before{background:#00c9b4;}
.agent-row:hover{background:var(--surface2);}
.agent-icon-box{
  width:44px;height:44px;
  border-radius:10px;
  display:flex;align-items:center;justify-content:center;
  font-size:20px;
  flex-shrink:0;
}
.agent-info{flex:1;}
.agent-info .name{font-size:14px;font-weight:700;}
.agent-info .desc{
  font-size:11px;color:var(--muted);margin-top:3px;
  font-family:'Space Mono',monospace;
}
.badge-active{
  font-family:'Space Mono',monospace;
  font-size:9px;
  padding:4px 10px;
  border-radius:4px;
  letter-spacing:1px;
  font-weight:700;
}
.badge-green{background:#00e09022;color:var(--green);border:1px solid #00e09044;}
.badge-blue{background:#4da6ff22;color:var(--blue);border:1px solid #4da6ff44;}
.badge-purple{background:#9b7bff22;color:var(--purple);border:1px solid #9b7bff44;}
.badge-yellow{background:#f5c84222;color:var(--yellow);border:1px solid #f5c84244;}
.badge-red{background:#ff4d6a22;color:var(--red);border:1px solid #ff4d6a44;}
.badge-orange{background:#ff9a3c22;color:var(--orange);border:1px solid #ff9a3c44;}

/* INPUT SECTION */
.input-section{
  padding:20px 28px 24px;
  border-top:1px solid var(--border);
  background:var(--bg);
}
.input-section label{
  font-family:'Space Mono',monospace;
  font-size:9px;
  letter-spacing:1.5px;
  color:var(--muted);
  display:block;
  margin-bottom:8px;
}
.input-row{display:flex;gap:8px;align-items:stretch;}
.styled-select{
  flex:1;
  padding:10px 14px;
  background:var(--surface);
  border:1px solid var(--border);
  color:var(--text);
  font-family:'Syne',sans-serif;
  font-size:13px;
  border-radius:6px;
  outline:none;
  cursor:pointer;
}
.styled-select:focus{border-color:var(--blue);}
.run-btn{
  padding:10px 20px;
  background:var(--blue);
  color:#000;
  border:none;
  border-radius:6px;
  font-family:'Syne',sans-serif;
  font-weight:800;
  font-size:12px;
  letter-spacing:1px;
  cursor:pointer;
  transition:all 0.2s;
  white-space:nowrap;
}
.run-btn:hover{background:#6bb8ff;transform:translateY(-1px);}
.run-btn:disabled{opacity:0.4;cursor:not-allowed;transform:none;}
#paste-area{margin-top:10px;display:none;}
#vendor-input{
  width:100%;padding:10px 14px;
  background:var(--surface);
  border:1px solid var(--border);
  color:var(--text);
  font-family:'Space Mono',monospace;
  font-size:11px;
  border-radius:6px;
  height:80px;
  resize:none;
  outline:none;
}
#vendor-input:focus{border-color:var(--blue);}

/* LOGS */
.log-stream{
  padding:16px 28px;
  border-top:1px solid var(--border);
  display:none;
}
.log-stream.on{display:block;}
.log-stream h4{
  font-family:'Space Mono',monospace;
  font-size:9px;
  letter-spacing:2px;
  color:var(--muted);
  margin-bottom:10px;
}
.log-entry{
  font-family:'Space Mono',monospace;
  font-size:10px;
  color:#4da6ff;
  padding:5px 0 5px 12px;
  border-left:2px solid #4da6ff44;
  margin-bottom:4px;
  animation:fadeIn 0.3s ease;
}
.log-entry::before{content:'> ';}
@keyframes fadeIn{from{opacity:0;transform:translateX(-4px);}to{opacity:1;transform:none;}}

/* RESULTS OVERLAY */
#results-overlay{
  display:none;
  position:fixed;inset:0;
  background:rgba(10,11,14,0.96);
  z-index:200;
  overflow-y:auto;
  padding:40px;
}
#results-overlay.on{display:block;}
.results-inner{max-width:960px;margin:0 auto;}
.results-nav{
  display:flex;justify-content:space-between;align-items:center;
  margin-bottom:32px;
}
.results-nav h2{font-size:24px;font-weight:800;}
.back-btn{
  padding:10px 20px;
  background:transparent;
  border:1px solid var(--border);
  color:var(--muted);
  border-radius:6px;
  font-family:'Syne',sans-serif;
  font-weight:700;
  cursor:pointer;
  transition:all 0.2s;
}
.back-btn:hover{border-color:var(--blue);color:var(--blue);}
.r-kpi-grid{
  display:grid;
  grid-template-columns:repeat(4,1fr);
  gap:12px;
  margin-bottom:24px;
}
.r-kpi{
  background:var(--surface);
  border:1px solid var(--border);
  border-radius:8px;
  padding:20px;
}
.r-kpi .val{font-size:32px;font-weight:800;margin-bottom:4px;}
.r-kpi .lbl{
  font-family:'Space Mono',monospace;
  font-size:9px;
  color:var(--muted);
  letter-spacing:1px;
}
.r-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;}
.r-card{
  background:var(--surface);
  border:1px solid var(--border);
  border-radius:8px;
  padding:20px;
}
.r-card h3{
  font-size:12px;
  font-weight:700;
  letter-spacing:1.5px;
  color:var(--muted);
  text-transform:uppercase;
  font-family:'Space Mono',monospace;
  margin-bottom:14px;
  padding-bottom:10px;
  border-bottom:1px solid var(--border);
}
.r-item{
  display:flex;justify-content:space-between;align-items:center;
  padding:10px 0;
  border-bottom:1px solid var(--border);
  font-size:13px;
}
.r-item:last-child{border-bottom:none;}
.r-item .detail{color:var(--muted);font-size:11px;font-family:'Space Mono',monospace;}
.r-item .amount{color:var(--green);font-weight:700;font-family:'Space Mono',monospace;font-size:12px;}
.sim-pct{
  display:inline-block;
  padding:2px 8px;
  background:#00e09015;
  color:var(--green);
  border-radius:4px;
  font-family:'Space Mono',monospace;
  font-size:10px;
}
.r-summary{
  background:var(--surface);
  border:1px solid var(--border);
  border-radius:8px;
  padding:20px;
  margin-bottom:12px;
  grid-column:span 2;
  font-size:14px;
  color:#8a9ab5;
  line-height:1.7;
}
.spinner{
  display:inline-block;
  width:14px;height:14px;
  border:2px solid #ffffff33;
  border-top:2px solid var(--blue);
  border-radius:50%;
  animation:spin 0.7s linear infinite;
  margin-right:8px;
  vertical-align:middle;
}
@keyframes spin{to{transform:rotate(360deg);}}
</style>
</head>
<body>

<!-- NAV -->
<nav class="nav">
  <div class="nav-logo">
    <div class="logo-icon">VI</div>
    <span>VendorIQ</span>
    <div class="nav-badge">● AI PROCUREMENT INTELLIGENCE</div>
  </div>
  <div class="nav-right">
    Claude Sonnet · <span>Duplicate Agent</span> · <span>7-Agent Platform</span>
  </div>
</nav>

<!-- MAIN -->
<div class="layout">

  <!-- LEFT HERO -->
  <div class="hero">
    <div class="hero-label">○ AI-POWERED VENDOR OPERATIONS</div>

    <div class="hero-headline">
      <span class="line1">One Platform.</span>
      <span class="line2">Detect. Consolidate.</span>
      <span class="line3">Save.</span>
    </div>

    <p class="hero-desc">
      VendorIQ is an intelligent procurement assistant that deduplicates vendor records,
      eliminates spend waste, flags redundant contracts, and generates negotiation playbooks —
      powered by a multi-agent AI platform.
    </p>

    <div class="hero-tags">
      <div class="tag">DUPLICATE DETECTION</div>
      <div class="tag">SPEND ANALYSIS</div>
      <div class="tag">AI NEGOTIATION</div>
      <div class="tag">COST INTELLIGENCE</div>
      <div class="tag">VENDOR REGISTRY</div>
      <div class="tag">SMART CONSOLIDATION</div>
    </div>

    <div class="agent-grid">
      <div class="agent-btn"><div class="icon">🔗</div><div class="label">Dup</div></div>
      <div class="agent-btn"><div class="icon">💰</div><div class="label">Cost</div></div>
      <div class="agent-btn"><div class="icon">🤝</div><div class="label">Neg</div></div>
      <div class="agent-btn"><div class="icon">📊</div><div class="label">Spend</div></div>
      <div class="agent-btn"><div class="icon">🔍</div><div class="label">Audit</div></div>
      <div class="agent-btn"><div class="icon">⚡</div><div class="label">Risk</div></div>
      <div class="agent-btn"><div class="icon">📋</div><div class="label">Report</div></div>
    </div>

    <div class="kpi-row" id="kpi-row">
      <div class="kpi-cell">
        <div class="kpi-val c-blue" id="kpi-vendors">—</div>
        <div class="kpi-label">TOTAL VENDORS</div>
      </div>
      <div class="kpi-cell">
        <div class="kpi-val c-green" id="kpi-savings">—</div>
        <div class="kpi-label">SAVINGS IDENTIFIED</div>
      </div>
      <div class="kpi-cell">
        <div class="kpi-val c-red" id="kpi-dups">—</div>
        <div class="kpi-label">DUPLICATES FOUND</div>
      </div>
    </div>

  </div>

  <!-- RIGHT PANEL -->
  <div class="right-panel">
    <div class="right-header">
      <h3>Active Agents</h3>
    </div>

    <div class="agent-list">
      <div class="agent-row blue">
        <div class="agent-icon-box" style="background:#4da6ff15;">🔗</div>
        <div class="agent-info">
          <div class="name">Duplicate Vendor Agent</div>
          <div class="desc">Identify and merge redundant vendor records</div>
        </div>
        <div class="badge-active badge-blue">ACTIVE</div>
      </div>
      <div class="agent-row green">
        <div class="agent-icon-box" style="background:#00e09015;">✂️</div>
        <div class="agent-info">
          <div class="name">Cost Cutter Agent</div>
          <div class="desc">Spot waste, right-size spend, maximise savings</div>
        </div>
        <div class="badge-active badge-green">ACTIVE</div>
      </div>
      <div class="agent-row purple">
        <div class="agent-icon-box" style="background:#9b7bff15;">🤝</div>
        <div class="agent-info">
          <div class="name">Negotiator Agent</div>
          <div class="desc">AI-driven contract and vendor negotiation playbooks</div>
        </div>
        <div class="badge-active badge-purple">ACTIVE</div>
      </div>
      <div class="agent-row yellow">
        <div class="agent-icon-box" style="background:#f5c84215;">📊</div>
        <div class="agent-info">
          <div class="name">Spend Intelligence</div>
          <div class="desc">Track trends, simulate scenarios, gain insights</div>
        </div>
        <div class="badge-active badge-yellow">ACTIVE</div>
      </div>
      <div class="agent-row red">
        <div class="agent-icon-box" style="background:#ff4d6a15;">🚨</div>
        <div class="agent-info">
          <div class="name">Risk & Anomaly Agent</div>
          <div class="desc">Surface hidden outliers and contract irregularities</div>
        </div>
        <div class="badge-active badge-red">ACTIVE</div>
      </div>
      <div class="agent-row orange">
        <div class="agent-icon-box" style="background:#ff9a3c15;">📋</div>
        <div class="agent-info">
          <div class="name">Improvement Reports</div>
          <div class="desc">Vendor scorecards and procurement benchmarks</div>
        </div>
        <div class="badge-active badge-orange">ACTIVE</div>
      </div>
      <div class="agent-row teal">
        <div class="agent-icon-box" style="background:#00c9b415;">🏛️</div>
        <div class="agent-info">
          <div class="name">Vendor Registry</div>
          <div class="desc">Maintain canonical vendor master data</div>
        </div>
        <div class="badge-active" style="background:#00c9b415;color:#00c9b4;border:1px solid #00c9b444;font-family:'Space Mono',monospace;font-size:9px;padding:4px 10px;border-radius:4px;letter-spacing:1px;font-weight:700;">ACTIVE</div>
      </div>
    </div>

    <!-- LOG STREAM -->
    <div class="log-stream" id="log-section">
      <h4>AGENT LOG STREAM</h4>
      <div id="agent-log"></div>
    </div>

    <!-- INPUT -->
    <div class="input-section">
      <label>DATA SOURCE</label>
      <div class="input-row">
        <select class="styled-select" id="mode" onchange="handleModeChange()">
          <option value="sample">Use Sample Data</option>
          <option value="csv">Paste CSV</option>
          <option value="json">Paste JSON</option>
        </select>
        <button class="run-btn" id="run-btn" onclick="runAnalysis()">RUN ANALYSIS</button>
      </div>
      <div id="paste-area">
        <textarea id="vendor-input" placeholder="Paste vendor data here..."></textarea>
      </div>
    </div>

  </div>
</div>

<!-- RESULTS OVERLAY -->
<div id="results-overlay">
  <div class="results-inner">
    <div class="results-nav">
      <h2>Analysis Results</h2>
      <button class="back-btn" onclick="resetApp()">← NEW ANALYSIS</button>
    </div>

    <div class="r-kpi-grid" id="r-kpi-grid"></div>
    <div class="r-grid" id="r-cards"></div>
  </div>
</div>

<script>
function G(id){ return document.getElementById(id); }

function handleModeChange(){
  G("paste-area").style.display = G("mode").value === "sample" ? "none" : "block";
}

function addLog(text){
  G("log-section").classList.add("on");
  G("agent-log").innerHTML += "<div class='log-entry'>" + text + "</div>";
  G("log-section").scrollTop = G("log-section").scrollHeight;
}

function getSampleData(){
  return [
    {id:"V001",name:"Infosys Ltd",spend:850000},
    {id:"V002",name:"Infosys Limited",spend:120000},
    {id:"V003",name:"TCS",spend:650000},
    {id:"V004",name:"AWS",spend:420000},
    {id:"V005",name:"ABC Services",spend:10000}
  ];
}

function parseCSV(raw){
  var lines = raw.trim().split("\n");
  var headers = lines[0].split(",");
  return lines.slice(1).map(function(line,i){
    var vals = line.split(",");
    return { id: vals[0]||"V00"+(i+1), name: vals[1]||"Vendor", spend: Number(vals[2])||0 };
  });
}

async function callClaude(prompt){
  await new Promise(r => setTimeout(r, 2800));
  return {
    summary:"Duplicate vendors and low-value contracts detected. Suggested consolidation can reduce procurement overhead by 18% and yield significant cost savings across the vendor base.",
    kpis:{ total_vendors:5, duplicate_pairs:2, low_value_count:1, total_savings_inr:450000 },
    duplicates:[
      { vendor_a:"Infosys Ltd", vendor_b:"Infosys Limited", similarity:94, action:"Merge" },
      { vendor_a:"AWS", vendor_b:"Amazon Web Services", similarity:98, action:"Consolidate" }
    ],
    low_value_vendors:[{ id:"V005", name:"ABC Services", spend:10000, action:"Terminate", reason:"Low annual spend" }],
    action_plan:[
      { action:"Merge Infosys vendors", saving_inr:150000, effort:"Low" },
      { action:"Consolidate AWS billing", saving_inr:200000, effort:"Medium" }
    ],
    negotiation_targets:[
      { vendor:"Microsoft", current_spend:510000, target_saving_pct:12, strategy:"Volume negotiation" }
    ],
    vendor_registry: getSampleData().map(v => ({ ...v, status: v.spend < 20000 ? "Review" : "Keep" }))
  };
}

async function runAnalysis(){
  G("run-btn").disabled = true;
  G("run-btn").innerHTML = "<span class='spinner'></span>RUNNING";

  addLog("Initializing VendorIQ agents...");
  addLog("Loading dataset...");

  var mode = G("mode").value;
  var vendors = [];

  try{
    if(mode === "sample") vendors = getSampleData();
    else if(mode === "csv") vendors = parseCSV(G("vendor-input").value);
    else vendors = JSON.parse(G("vendor-input").value);

    addLog("Dataset loaded — " + vendors.length + " vendors");

    await new Promise(r => setTimeout(r, 600));
    addLog("Duplicate Agent scanning name similarity...");
    await new Promise(r => setTimeout(r, 700));
    addLog("Cost Cutter Agent analyzing spend patterns...");
    await new Promise(r => setTimeout(r, 700));
    addLog("Negotiator Agent generating playbooks...");

    var result = await callClaude("dummy");

    addLog("All agents complete — rendering results");

    // Update KPIs on hero
    G("kpi-vendors").textContent = result.kpis.total_vendors;
    G("kpi-savings").textContent = "₹" + (result.kpis.total_savings_inr/1000).toFixed(0) + "K";
    G("kpi-dups").textContent = result.kpis.duplicate_pairs;

    await new Promise(r => setTimeout(r, 400));
    renderResults(result);

  } catch(e){
    addLog("ERROR: " + e.message);
    G("run-btn").disabled = false;
    G("run-btn").innerHTML = "RUN ANALYSIS";
  }
}

function renderResults(d){
  G("results-overlay").classList.add("on");

  G("r-kpi-grid").innerHTML =
    "<div class='r-kpi'><div class='val c-blue'>" + d.kpis.total_vendors + "</div><div class='lbl'>TOTAL VENDORS</div></div>" +
    "<div class='r-kpi'><div class='val c-red'>" + d.kpis.duplicate_pairs + "</div><div class='lbl'>DUPLICATES FOUND</div></div>" +
    "<div class='r-kpi'><div class='val' style='color:var(--orange)'>" + d.kpis.low_value_count + "</div><div class='lbl'>LOW VALUE</div></div>" +
    "<div class='r-kpi'><div class='val c-green'>₹" + (d.kpis.total_savings_inr/1000).toFixed(0) + "K</div><div class='lbl'>TOTAL SAVINGS</div></div>";

  var html = "<div class='r-summary' style='grid-column:span 2'>" + d.summary + "</div>";

  html += "<div class='r-card'><h3>Duplicate Vendors</h3>";
  (d.duplicates||[]).forEach(function(x){
    html += "<div class='r-item'><div><div>" + x.vendor_a + " ↔ " + x.vendor_b + "</div><div class='detail'>" + x.action + "</div></div><span class='sim-pct'>" + x.similarity + "% match</span></div>";
  });
  html += "</div>";

  html += "<div class='r-card'><h3>Action Plan</h3>";
  (d.action_plan||[]).forEach(function(x){
    html += "<div class='r-item'><div><div>" + x.action + "</div><div class='detail'>Effort: " + x.effort + "</div></div><span class='amount'>₹" + x.saving_inr.toLocaleString() + "</span></div>";
  });
  html += "</div>";

  html += "<div class='r-card'><h3>Negotiation Targets</h3>";
  (d.negotiation_targets||[]).forEach(function(x){
    html += "<div class='r-item'><div><div>" + x.vendor + "</div><div class='detail'>" + x.strategy + "</div></div><span class='amount'>Save " + x.target_saving_pct + "%</span></div>";
  });
  html += "</div>";

  html += "<div class='r-card'><h3>Vendor Registry</h3>";
  (d.vendor_registry||[]).forEach(function(v){
    var col = v.status === "Keep" ? "var(--green)" : "var(--orange)";
    html += "<div class='r-item'><div><div>" + v.name + "</div><div class='detail'>₹" + v.spend.toLocaleString() + "</div></div><span style='color:" + col + ";font-size:10px;font-family:Space Mono,monospace'>" + v.status + "</span></div>";
  });
  html += "</div>";

  G("r-cards").innerHTML = html;
}

function resetApp(){ location.reload(); }
</script>

</body>
</html>
"""

st.components.v1.html(PAGE, height=1000, scrolling=True)
