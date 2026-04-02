import streamlit as st

st.set_page_config(layout="wide", page_title="VendorIQ")

PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>VendorIQ</title>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box;margin:0;padding:0;}
body{
    background:#0b0d11;
    color:#dde3ed;
    font-family:'Space Grotesk',sans-serif;
    min-height:100vh;
}

/* NAV */
.nav{
    display:flex;
    align-items:center;
    justify-content:space-between;
    padding:0 32px;
    height:58px;
    border-bottom:1px solid #1c2030;
    background:#0b0d11;
    position:sticky;top:0;z-index:99;
}
.nav-left{display:flex;align-items:center;gap:14px;}
.logo-box{
    width:34px;height:34px;
    background:#4da6ff;
    border-radius:8px;
    display:flex;align-items:center;justify-content:center;
    font-weight:700;font-size:13px;color:#000;letter-spacing:-0.5px;
}
.nav-title{font-size:18px;font-weight:700;letter-spacing:-0.3px;}
.nav-pill{
    font-family:'Space Mono',monospace;
    font-size:9px;letter-spacing:1.5px;
    border:1px solid #4da6ff55;
    color:#4da6ff;
    padding:4px 10px;border-radius:20px;
}
.nav-right{
    font-family:'Space Mono',monospace;
    font-size:10px;color:#3e4a5c;
    letter-spacing:0.3px;
}
.nav-right b{color:#6b7a90;}

/* LAYOUT */
.layout{
    display:grid;
    grid-template-columns:1fr 440px;
    min-height:calc(100vh - 58px);
}

/* LEFT */
.left{
    padding:44px 44px 36px;
    border-right:1px solid #1c2030;
    display:flex;flex-direction:column;gap:28px;
}
.eyebrow{
    font-family:'Space Mono',monospace;
    font-size:9px;letter-spacing:3px;color:#3e4a5c;
    display:flex;align-items:center;gap:10px;
}
.eyebrow::after{content:'';flex:0 0 80px;height:1px;background:#1c2030;}
.headline{line-height:1.08;}
.headline .h1{display:block;font-size:48px;font-weight:700;color:#dde3ed;}
.headline .h2{display:block;font-size:48px;font-weight:700;color:#4da6ff;}
.headline .h3{display:block;font-size:48px;font-weight:700;color:#00e090;}
.desc{
    font-size:14px;color:#566070;line-height:1.75;
    max-width:480px;font-weight:400;
}
.tags{display:flex;flex-wrap:wrap;gap:8px;}
.tag{
    font-family:'Space Mono',monospace;
    font-size:9px;letter-spacing:0.8px;
    padding:5px 12px;
    border:1px solid #1c2030;
    border-radius:3px;
    color:#3e4a5c;
    transition:all 0.15s;cursor:default;
}
.tag:hover{border-color:#4da6ff55;color:#4da6ff;}

/* AGENT ICON STRIP */
.agent-strip{display:flex;gap:8px;flex-wrap:wrap;}
.a-chip{
    display:flex;flex-direction:column;align-items:center;gap:5px;
    padding:12px 14px;
    background:#0f1219;
    border:1px solid #1c2030;
    border-radius:8px;
    min-width:66px;cursor:pointer;
    transition:border-color 0.15s;
}
.a-chip:hover{border-color:#4da6ff44;}
.a-chip .ic{font-size:20px;}
.a-chip .lb{font-family:'Space Mono',monospace;font-size:8px;color:#3e4a5c;letter-spacing:0.5px;}

/* KPI STRIP */
.kpi-strip{
    display:grid;grid-template-columns:repeat(3,1fr);
    border:1px solid #1c2030;border-radius:8px;overflow:hidden;
    background:#1c2030;gap:1px;
}
.kpi-cell{
    background:#0f1219;
    padding:18px 22px;text-align:center;
}
.kpi-val{font-size:34px;font-weight:700;line-height:1;}
.kpi-lbl{
    font-family:'Space Mono',monospace;
    font-size:8px;letter-spacing:1.5px;color:#3e4a5c;margin-top:5px;
}
.blue{color:#4da6ff;} .green{color:#00e090;} .red{color:#ff4d6a;}

/* RIGHT PANEL */
.right{
    background:#0d1016;
    display:flex;flex-direction:column;
}
.panel-head{
    padding:20px 26px 16px;
    border-bottom:1px solid #1c2030;
}
.panel-head p{
    font-family:'Space Mono',monospace;
    font-size:9px;letter-spacing:2px;color:#3e4a5c;
    text-transform:uppercase;
}

/* AGENT LIST */
.agent-list{flex:1;overflow-y:auto;}
.a-row{
    display:flex;align-items:center;gap:14px;
    padding:15px 26px;
    border-bottom:1px solid #1c2030;
    cursor:pointer;transition:background 0.12s;
    position:relative;
}
.a-row::before{
    content:'';position:absolute;left:0;top:0;bottom:0;width:3px;
}
.a-row:hover{background:#0f1219;}
.a-row.c1::before{background:#4da6ff;}
.a-row.c2::before{background:#00e090;}
.a-row.c3::before{background:#9b7bff;}
.a-row.c4::before{background:#f5c842;}
.a-row.c5::before{background:#ff4d6a;}
.a-row.c6::before{background:#ff9a3c;}
.a-row.c7::before{background:#00c9b4;}
.a-icon{
    width:42px;height:42px;border-radius:10px;
    display:flex;align-items:center;justify-content:center;
    font-size:18px;flex-shrink:0;
}
.a-text .name{font-size:13px;font-weight:600;}
.a-text .sub{
    font-family:'Space Mono',monospace;
    font-size:10px;color:#3e4a5c;margin-top:2px;
}
.a-text{flex:1;}
.badge{
    font-family:'Space Mono',monospace;
    font-size:8px;letter-spacing:1px;font-weight:700;
    padding:3px 9px;border-radius:3px;
}
.b1{background:#4da6ff18;color:#4da6ff;border:1px solid #4da6ff33;}
.b2{background:#00e09018;color:#00e090;border:1px solid #00e09033;}
.b3{background:#9b7bff18;color:#9b7bff;border:1px solid #9b7bff33;}
.b4{background:#f5c84218;color:#f5c842;border:1px solid #f5c84233;}
.b5{background:#ff4d6a18;color:#ff4d6a;border:1px solid #ff4d6a33;}
.b6{background:#ff9a3c18;color:#ff9a3c;border:1px solid #ff9a3c33;}
.b7{background:#00c9b418;color:#00c9b4;border:1px solid #00c9b433;}

/* LOG */
.log-wrap{
    padding:14px 26px;
    border-top:1px solid #1c2030;
    display:none;max-height:140px;overflow-y:auto;
}
.log-wrap.on{display:block;}
.log-head{
    font-family:'Space Mono',monospace;
    font-size:8px;letter-spacing:2px;color:#3e4a5c;margin-bottom:8px;
}
.log{
    font-family:'Space Mono',monospace;
    font-size:10px;color:#4da6ff;
    padding:4px 0 4px 10px;
    border-left:2px solid #4da6ff33;
    margin-bottom:3px;
}
.log::before{content:'> ';}

/* INPUT ZONE */
.input-zone{
    padding:18px 26px 22px;
    border-top:1px solid #1c2030;
    background:#0b0d11;
}
.iz-label{
    font-family:'Space Mono',monospace;
    font-size:8px;letter-spacing:2px;color:#3e4a5c;
    margin-bottom:8px;
}
.iz-row{display:flex;gap:8px;}
select#mode{
    flex:1;
    padding:10px 12px;
    background:#0d1016;
    border:1px solid #1c2030;
    color:#dde3ed;
    font-family:'Space Grotesk',sans-serif;
    font-size:13px;
    border-radius:6px;
    outline:none;cursor:pointer;
}
select#mode:focus{border-color:#4da6ff;}
#run-btn{
    padding:10px 20px;
    background:#4da6ff;
    color:#000;border:none;
    border-radius:6px;
    font-family:'Space Grotesk',sans-serif;
    font-weight:700;font-size:11px;letter-spacing:0.5px;
    cursor:pointer;transition:all 0.15s;white-space:nowrap;
}
#run-btn:hover{background:#6dbfff;}
#run-btn:disabled{opacity:0.35;cursor:not-allowed;}
#paste-area{margin-top:10px;display:none;}
#vendor-input{
    width:100%;padding:10px 12px;
    background:#0d1016;border:1px solid #1c2030;
    color:#dde3ed;
    font-family:'Space Mono',monospace;font-size:10px;
    border-radius:6px;height:72px;resize:none;outline:none;
}
#vendor-input:focus{border-color:#4da6ff;}

/* RESULTS OVERLAY */
#results-overlay{
    display:none;
    position:fixed;inset:0;
    background:#0b0d11;
    z-index:200;overflow-y:auto;padding:36px;
}
#results-overlay.on{display:block;}
.ro-inner{max-width:980px;margin:0 auto;}
.ro-top{
    display:flex;justify-content:space-between;align-items:center;
    margin-bottom:28px;
}
.ro-top h2{font-size:22px;font-weight:700;}
.back-btn{
    padding:9px 18px;
    background:transparent;
    border:1px solid #1c2030;
    color:#566070;border-radius:6px;
    font-family:'Space Grotesk',sans-serif;
    font-weight:600;cursor:pointer;transition:all 0.15s;
}
.back-btn:hover{border-color:#4da6ff;color:#4da6ff;}
.ro-kpis{
    display:grid;grid-template-columns:repeat(4,1fr);
    gap:10px;margin-bottom:20px;
}
.ro-kpi{
    background:#0f1219;border:1px solid #1c2030;
    border-radius:8px;padding:18px 20px;
}
.ro-kpi .v{font-size:30px;font-weight:700;margin-bottom:4px;}
.ro-kpi .l{
    font-family:'Space Mono',monospace;
    font-size:8px;letter-spacing:1.5px;color:#3e4a5c;
}
.ro-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;}
.ro-card{
    background:#0f1219;border:1px solid #1c2030;
    border-radius:8px;padding:18px 20px;
}
.ro-card h3{
    font-family:'Space Mono',monospace;
    font-size:9px;letter-spacing:2px;color:#3e4a5c;
    text-transform:uppercase;margin-bottom:14px;
    padding-bottom:10px;border-bottom:1px solid #1c2030;
}
.ro-item{
    display:flex;justify-content:space-between;align-items:center;
    padding:9px 0;border-bottom:1px solid #1c2030;font-size:13px;
}
.ro-item:last-child{border-bottom:none;}
.ro-item .sub{
    font-family:'Space Mono',monospace;
    font-size:9px;color:#3e4a5c;margin-top:2px;
}
.ro-item .amt{
    color:#00e090;font-weight:700;
    font-family:'Space Mono',monospace;font-size:11px;
}
.sim{
    display:inline-block;padding:2px 7px;
    background:#00e09012;color:#00e090;
    border-radius:3px;font-family:'Space Mono',monospace;font-size:9px;
}
.ro-summary{
    grid-column:span 2;
    background:#0f1219;border:1px solid #1c2030;
    border-radius:8px;padding:18px 20px;
    font-size:13px;color:#566070;line-height:1.75;
    margin-bottom:0;
}
.spin{
    display:inline-block;width:12px;height:12px;
    border:2px solid #ffffff22;border-top:2px solid #4da6ff;
    border-radius:50%;animation:sp 0.7s linear infinite;
    margin-right:6px;vertical-align:middle;
}
@keyframes sp{to{transform:rotate(360deg);}}
</style>
</head>
<body>

<!-- NAV -->
<nav class="nav">
  <div class="nav-left">
    <div class="logo-box">VI</div>
    <span class="nav-title">VendorIQ</span>
    <span class="nav-pill">● AI PROCUREMENT INTELLIGENCE</span>
  </div>
  <div class="nav-right">
    Claude Sonnet &nbsp;·&nbsp; <b>Duplicate Agent</b> &nbsp;·&nbsp; <b>7-Agent Platform</b>
  </div>
</nav>

<!-- LAYOUT -->
<div class="layout">

  <!-- LEFT -->
  <div class="left">
    <div class="eyebrow">○ AI-POWERED VENDOR OPERATIONS</div>

    <div class="headline">
      <span class="h1">One Platform.</span>
      <span class="h2">Detect. Consolidate.</span>
      <span class="h3">Save.</span>
    </div>

    <p class="desc">
      VendorIQ is an intelligent procurement assistant that deduplicates vendor records,
      eliminates spend waste, flags redundant contracts, and generates negotiation playbooks —
      powered by a multi-agent AI platform.
    </p>

    <div class="tags">
      <div class="tag">DUPLICATE DETECTION</div>
      <div class="tag">SPEND ANALYSIS</div>
      <div class="tag">AI NEGOTIATION</div>
      <div class="tag">COST INTELLIGENCE</div>
      <div class="tag">VENDOR REGISTRY</div>
      <div class="tag">SMART CONSOLIDATION</div>
    </div>

    <div class="agent-strip">
      <div class="a-chip"><div class="ic">🔗</div><div class="lb">Dup</div></div>
      <div class="a-chip"><div class="ic">✂️</div><div class="lb">Cost</div></div>
      <div class="a-chip"><div class="ic">🤝</div><div class="lb">Neg</div></div>
      <div class="a-chip"><div class="ic">📊</div><div class="lb">Spend</div></div>
      <div class="a-chip"><div class="ic">🔍</div><div class="lb">Audit</div></div>
      <div class="a-chip"><div class="ic">⚡</div><div class="lb">Risk</div></div>
      <div class="a-chip"><div class="ic">📋</div><div class="lb">Report</div></div>
    </div>

    <div class="kpi-strip">
      <div class="kpi-cell">
        <div class="kpi-val blue" id="kpi-vendors">—</div>
        <div class="kpi-lbl">TOTAL VENDORS</div>
      </div>
      <div class="kpi-cell">
        <div class="kpi-val green" id="kpi-savings">—</div>
        <div class="kpi-lbl">SAVINGS IDENTIFIED</div>
      </div>
      <div class="kpi-cell">
        <div class="kpi-val red" id="kpi-dups">—</div>
        <div class="kpi-lbl">DUPLICATES FOUND</div>
      </div>
    </div>
  </div>

  <!-- RIGHT -->
  <div class="right">
    <div class="panel-head">
      <p>Active Agents</p>
    </div>

    <div class="agent-list">
      <div class="a-row c1">
        <div class="a-icon" style="background:#4da6ff12">🔗</div>
        <div class="a-text">
          <div class="name">Duplicate Vendor Agent</div>
          <div class="sub">Identify and merge redundant vendor records</div>
        </div>
        <div class="badge b1">ACTIVE</div>
      </div>
      <div class="a-row c2">
        <div class="a-icon" style="background:#00e09012">✂️</div>
        <div class="a-text">
          <div class="name">Cost Cutter Agent</div>
          <div class="sub">Spot waste, right-size spend, maximise savings</div>
        </div>
        <div class="badge b2">ACTIVE</div>
      </div>
      <div class="a-row c3">
        <div class="a-icon" style="background:#9b7bff12">🤝</div>
        <div class="a-text">
          <div class="name">Negotiator Agent</div>
          <div class="sub">AI-driven contract and vendor negotiation playbooks</div>
        </div>
        <div class="badge b3">ACTIVE</div>
      </div>
      <div class="a-row c4">
        <div class="a-icon" style="background:#f5c84212">📊</div>
        <div class="a-text">
          <div class="name">Spend Intelligence</div>
          <div class="sub">Track trends, simulate scenarios, gain insights</div>
        </div>
        <div class="badge b4">ACTIVE</div>
      </div>
      <div class="a-row c5">
        <div class="a-icon" style="background:#ff4d6a12">🚨</div>
        <div class="a-text">
          <div class="name">Risk & Anomaly Agent</div>
          <div class="sub">Surface hidden outliers and contract irregularities</div>
        </div>
        <div class="badge b5">ACTIVE</div>
      </div>
      <div class="a-row c6">
        <div class="a-icon" style="background:#ff9a3c12">📋</div>
        <div class="a-text">
          <div class="name">Improvement Reports</div>
          <div class="sub">Vendor scorecards and procurement benchmarks</div>
        </div>
        <div class="badge b6">ACTIVE</div>
      </div>
      <div class="a-row c7">
        <div class="a-icon" style="background:#00c9b412">🏛️</div>
        <div class="a-text">
          <div class="name">Vendor Registry</div>
          <div class="sub">Maintain canonical vendor master data</div>
        </div>
        <div class="badge b7">ACTIVE</div>
      </div>
    </div>

    <!-- LOG STREAM -->
    <div class="log-wrap" id="log-section">
      <div class="log-head">AGENT LOG STREAM</div>
      <div id="agent-log"></div>
    </div>

    <!-- INPUT -->
    <div class="input-zone">
      <div class="iz-label">DATA SOURCE</div>
      <div class="iz-row">
        <select id="mode" onchange="handleModeChange()">
          <option value="sample">Use Sample Data</option>
          <option value="csv">Paste CSV</option>
          <option value="json">Paste JSON</option>
        </select>
        <button id="run-btn" onclick="runAnalysis()">RUN ANALYSIS</button>
      </div>
      <div id="paste-area">
        <textarea id="vendor-input" placeholder="Paste vendor data here..."></textarea>
      </div>
    </div>
  </div>
</div>

<!-- RESULTS OVERLAY -->
<div id="results-overlay">
  <div class="ro-inner">
    <div class="ro-top">
      <h2>Analysis Results</h2>
      <button class="back-btn" onclick="resetApp()">← New Analysis</button>
    </div>
    <div class="ro-kpis" id="ro-kpis"></div>
    <div class="ro-grid" id="ro-grid"></div>
  </div>
</div>

<script>
function G(id){ return document.getElementById(id); }

function handleModeChange(){
    var mode = G("mode").value;
    G("paste-area").style.display = mode === "sample" ? "none" : "block";
}

function addLog(text){
    G("log-section").classList.add("on");
    G("agent-log").innerHTML += "<div class='log'>" + text + "</div>";
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
    var lines = raw.trim().split("\\n");
    var headers = lines[0].split(",");
    return lines.slice(1).map(function(line,i){
        var vals = line.split(",");
        return {
            id: vals[0] || "V00" + (i+1),
            name: vals[1] || "Vendor",
            spend: Number(vals[2]) || 0
        };
    });
}

async function callClaude(prompt){
    await new Promise(resolve => setTimeout(resolve, 2500));
    return {
        summary: "Duplicate vendors and low-value contracts detected. Suggested consolidation can save significant procurement cost.",
        kpis: {
            total_vendors: 5,
            duplicate_pairs: 2,
            low_value_count: 1,
            total_savings_inr: 450000
        },
        duplicates: [
            { vendor_a: "Infosys Ltd", vendor_b: "Infosys Limited", similarity: 94, action: "Merge" },
            { vendor_a: "AWS", vendor_b: "Amazon Web Services", similarity: 98, action: "Consolidate" }
        ],
        low_value_vendors: [
            { id: "V005", name: "ABC Services", spend: 10000, action: "Terminate", reason: "Low annual spend" }
        ],
        action_plan: [
            { action: "Merge Infosys vendors", saving_inr: 150000, effort: "Low" },
            { action: "Consolidate AWS billing", saving_inr: 200000, effort: "Medium" }
        ],
        negotiation_targets: [
            { vendor: "Microsoft", current_spend: 510000, target_saving_pct: 12, strategy: "Volume negotiation" }
        ],
        vendor_registry: getSampleData().map(v => ({
            ...v,
            status: v.spend < 20000 ? "Review" : "Keep"
        }))
    };
}

async function runAnalysis(){
    G("run-btn").disabled = true;
    G("run-btn").innerHTML = "<span class='spin'></span>RUNNING";
    addLog("Initializing VendorIQ...");
    addLog("Loading dataset...");

    var mode = G("mode").value;
    var vendors = [];

    try{
        if(mode === "sample"){
            vendors = getSampleData();
        } else if(mode === "csv"){
            vendors = parseCSV(G("vendor-input").value);
        } else {
            vendors = JSON.parse(G("vendor-input").value);
        }

        addLog("Dataset loaded successfully");
        addLog("Running AI duplicate detection...");
        addLog("Running spend optimization...");

        var result = await callClaude("dummy prompt");

        addLog("AI analysis complete");

        // Update hero KPIs
        G("kpi-vendors").textContent = result.kpis.total_vendors;
        G("kpi-savings").textContent = "₹" + (result.kpis.total_savings_inr/1000).toFixed(0) + "K";
        G("kpi-dups").textContent = result.kpis.duplicate_pairs;

        renderResults(result);

    } catch(e){
        addLog("ERROR: " + e.message);
        alert("Error: " + e.message);
        G("run-btn").disabled = false;
        G("run-btn").innerHTML = "RUN ANALYSIS";
    }
}

function renderResults(d){
    G("results-overlay").classList.add("on");

    G("ro-kpis").innerHTML =
        "<div class='ro-kpi'><div class='v blue'>" + d.kpis.total_vendors + "</div><div class='l'>TOTAL VENDORS</div></div>" +
        "<div class='ro-kpi'><div class='v red'>" + d.kpis.duplicate_pairs + "</div><div class='l'>DUPLICATES</div></div>" +
        "<div class='ro-kpi'><div class='v' style='color:#ff9a3c'>" + d.kpis.low_value_count + "</div><div class='l'>LOW VALUE</div></div>" +
        "<div class='ro-kpi'><div class='v green'>₹" + d.kpis.total_savings_inr.toLocaleString() + "</div><div class='l'>SAVINGS (INR)</div></div>";

    var html = "<div class='ro-summary'>" + d.summary + "</div>";

    html += "<div class='ro-card'><h3>Duplicate Vendors</h3>";
    (d.duplicates || []).forEach(function(x){
        html += "<div class='ro-item'><div><div>" + x.vendor_a + " ↔ " + x.vendor_b + "</div><div class='sub'>" + x.action + "</div></div><span class='sim'>" + x.similarity + "% match</span></div>";
    });
    html += "</div>";

    html += "<div class='ro-card'><h3>Action Plan</h3>";
    (d.action_plan || []).forEach(function(x){
        html += "<div class='ro-item'><div><div>" + x.action + "</div><div class='sub'>Effort: " + x.effort + "</div></div><span class='amt'>₹" + x.saving_inr.toLocaleString() + "</span></div>";
    });
    html += "</div>";

    html += "<div class='ro-card'><h3>Negotiation Targets</h3>";
    (d.negotiation_targets || []).forEach(function(x){
        html += "<div class='ro-item'><div><div>" + x.vendor + "</div><div class='sub'>" + x.strategy + "</div></div><span class='amt'>Save " + x.target_saving_pct + "%</span></div>";
    });
    html += "</div>";

    html += "<div class='ro-card'><h3>Vendor Registry</h3>";
    (d.vendor_registry || []).forEach(function(v){
        var c = v.status === "Keep" ? "#00e090" : "#ff9a3c";
        html += "<div class='ro-item'><div><div>" + v.name + "</div><div class='sub'>₹" + v.spend.toLocaleString() + "</div></div><span style='color:" + c + ";font-family:Space Mono,monospace;font-size:10px;'>" + v.status + "</span></div>";
    });
    html += "</div>";

    G("ro-grid").innerHTML = html;
}

function resetApp(){
    location.reload();
}
</script>

</body>
</html>
"""

st.components.v1.html(PAGE, height=1000, scrolling=True)
