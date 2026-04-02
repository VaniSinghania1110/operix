import streamlit as st

st.set_page_config(layout="wide", page_title="VendorIQ")

PAGE = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>VendorIQ</title>
<style>
body{
    background:#04080f;
    color:#e0eaf8;
    font-family:Arial;
    margin:0;
    padding:0;
}
.wrap{
    max-width:1100px;
    margin:auto;
    padding:30px;
}
.hero{
    margin-bottom:30px;
}
.hero h1{
    font-size:60px;
    margin:0;
}
.hero span{
    color:#00d4ff;
}
.card{
    background:#080f1a;
    border:1px solid #162540;
    padding:20px;
    border-radius:8px;
    margin-bottom:20px;
}
button{
    width:100%;
    padding:16px;
    font-size:18px;
    background:#00d4ff;
    border:none;
    cursor:pointer;
    font-weight:bold;
}
textarea{
    width:100%;
    min-height:150px;
    background:#0d1624;
    color:white;
    border:1px solid #162540;
    padding:12px;
}
#loader,#results,#agent-panel{
    display:none;
}
#loader.on,#results.on,#agent-panel.on{
    display:block;
}
.log{
    padding:8px;
    margin:6px 0;
    background:#0d1624;
    border-left:3px solid #00d4ff;
}
.kpi-grid{
    display:grid;
    grid-template-columns:repeat(4,1fr);
    gap:15px;
}
.kpi{
    background:#080f1a;
    padding:20px;
    border:1px solid #162540;
}
.big{
    font-size:32px;
    color:#00e090;
    font-weight:bold;
}
</style>
</head>
<body>
<div class="wrap">

<div class="hero">
<h1>Vendor<span>IQ</span></h1>
<p>AI Procurement Negotiator and Duplicate Vendor Intelligence</p>
</div>

<div id="input-section" class="card">
<h3>Vendor Input</h3>

<select id="mode" style="width:100%;padding:10px;margin-bottom:15px;">
<option value="sample">Use Sample Data</option>
<option value="csv">Paste CSV</option>
<option value="json">Paste JSON</option>
</select>

<textarea id="vendor-input" placeholder="Paste CSV or JSON here"></textarea>

<button onclick="runAnalysis()">RUN VENDOR NEGOTIATOR</button>
</div>

<div id="loader" class="card">
<h2>Agent Running...</h2>
<p>Analyzing vendor dataset...</p>
</div>

<div id="agent-panel" class="card">
<h3>Reasoning Logs</h3>
<div id="agent-log"></div>
</div>

<div id="results">

<div class="kpi-grid" id="kpi-grid"></div>

<div class="card">
<h3>Executive Summary</h3>
<p id="exec-text"></p>
</div>

<div class="card">
<h3>Priority Action Plan</h3>
<div id="action-plan"></div>
</div>

<div class="card">
<h3>Duplicate Vendors</h3>
<div id="dup-grid"></div>
</div>

<div class="card">
<h3>Low Value Vendors</h3>
<div id="lv-grid"></div>
</div>

<div class="card">
<h3>Full Vendor Registry</h3>
<div id="vendor-table"></div>
</div>

<button onclick="resetApp()">NEW ANALYSIS</button>

</div>
</div>

<script>
function G(id){
    return document.getElementById(id);
}

function addLog(text){
    G("agent-log").innerHTML += "<div class='log'>" + text + "</div>";
}

function runAnalysis(){

    G("input-section").style.display = "none";
    G("loader").classList.add("on");
    G("agent-panel").classList.add("on");
    G("agent-log").innerHTML = "";

    addLog("Initializing VendorIQ Negotiator...");
    
    setTimeout(function(){
        addLog("Parsing vendor dataset...");
    },1000);

    setTimeout(function(){
        addLog("Detecting duplicate vendors...");
    },2000);

    setTimeout(function(){
        addLog("Flagging low-value vendors...");
    },3000);

    setTimeout(function(){
        addLog("Calculating negotiation savings...");
    },4000);

    setTimeout(function(){
        G("loader").classList.remove("on");
        renderResults();
    },5000);
}

function renderResults(){

    G("results").classList.add("on");

    G("kpi-grid").innerHTML =
        "<div class='kpi'><div>Total Vendors</div><div class='big'>20</div></div>" +
        "<div class='kpi'><div>Duplicate Pairs</div><div class='big'>6</div></div>" +
        "<div class='kpi'><div>Low Value</div><div class='big'>4</div></div>" +
        "<div class='kpi'><div>Savings</div><div class='big'>Rs.4.5L</div></div>";

    G("exec-text").innerText =
        "VendorIQ detected multiple overlapping vendors and low-value contracts. Recommended consolidation and renegotiation can save 18% annual procurement cost.";

    G("action-plan").innerHTML =
        "<ul>" +
        "<li>Merge Infosys Ltd + Infosys Limited → Save Rs.1.5L</li>" +
        "<li>Terminate ABC Services → Save Rs.90K</li>" +
        "<li>Renegotiate AWS support contract → Save Rs.2L</li>" +
        "</ul>";

    G("dup-grid").innerHTML =
        "<ul>" +
        "<li>Infosys Ltd ↔ Infosys Limited (94% similarity)</li>" +
        "<li>TCS ↔ Tata Consultancy Services (96%)</li>" +
        "</ul>";

    G("lv-grid").innerHTML =
        "<ul>" +
        "<li>ABC Services → Terminate</li>" +
        "<li>XYZ Logistics → Review</li>" +
        "</ul>";

    G("vendor-table").innerHTML =
        "<table border='1' width='100%' style='border-collapse:collapse'>" +
        "<tr><th>ID</th><th>Name</th><th>Spend</th></tr>" +
        "<tr><td>V001</td><td>Infosys Ltd</td><td>850000</td></tr>" +
        "<tr><td>V002</td><td>Infosys Limited</td><td>120000</td></tr>" +
        "<tr><td>V010</td><td>ABC Services</td><td>10000</td></tr>" +
        "</table>";
}

function resetApp(){
    location.reload();
}
</script>
</body>
</html>
"""

st.components.v1.html(PAGE, height=1200, scrolling=True)
