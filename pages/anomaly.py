import streamlit as st

st.set_page_config(layout="wide", page_title="SpendGuard")

PAGE = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>SpendGuard</title>
<style>
body{
    background:#04080f;
    color:#e0eaf8;
    font-family:Arial,sans-serif;
    margin:0;
    padding:0;
}
.wrap{
    max-width:1200px;
    margin:auto;
    padding:30px;
}
.hero h1{
    font-size:60px;
    margin:0;
}
.hero span{
    color:#ff4040;
}
.card{
    background:#080f1a;
    border:1px solid #162540;
    padding:20px;
    border-radius:10px;
    margin-bottom:20px;
}
button{
    width:100%;
    padding:16px;
    font-size:18px;
    background:#ff4040;
    color:white;
    border:none;
    cursor:pointer;
    font-weight:bold;
}
table{
    width:100%;
    border-collapse:collapse;
}
th,td{
    border:1px solid #162540;
    padding:10px;
    text-align:left;
}
.log{
    padding:10px;
    margin:8px 0;
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
    font-size:30px;
    color:#ff4040;
    font-weight:bold;
}
#results,#running{
    display:none;
}
#results.on,#running.on{
    display:block;
}
</style>
</head>
<body>
<div class="wrap">

<div class="hero">
<h1>Spend<span>Guard</span></h1>
<p>Cloud Spend Anomaly Detection AI Agent</p>
</div>

<div id="input-section" class="card">
<h3>Cloud Services Spend Data</h3>

<table>
<tr>
<th>Service</th>
<th>Previous Cost</th>
<th>Current Cost</th>
</tr>
<tr>
<td>EC2 Web Cluster</td>
<td>280000</td>
<td>420000</td>
</tr>
<tr>
<td>Azure Kubernetes</td>
<td>210000</td>
<td>310000</td>
</tr>
<tr>
<td>GCP BigQuery</td>
<td>88000</td>
<td>95000</td>
</tr>
</table>

<br>
<button onclick="runAnalysis()">RUN ANOMALY AGENT</button>
</div>

<div id="running" class="card">
<h3>Agent Running...</h3>
<div id="agent-log"></div>
</div>

<div id="results">
<div class="kpi-grid" id="kpi-grid"></div>

<div class="card">
<h3>Anomalies Detected</h3>
<div id="anomaly-list"></div>
</div>

<div class="card">
<h3>Recommended Actions</h3>
<div id="action-list"></div>
</div>

<button onclick="resetApp()">NEW ANALYSIS</button>
</div>

</div>

<script>
function G(id){
    return document.getElementById(id);
}

function addLog(text){
    G("agent-log").innerHTML +=
        "<div class='log'>" + text + "</div>";
}

function runAnalysis(){

    G("input-section").style.display = "none";
    G("running").classList.add("on");
    G("agent-log").innerHTML = "";

    addLog("Initializing anomaly detection agent...");

    setTimeout(function(){
        addLog("Scanning cloud spend services...");
    },1000);

    setTimeout(function(){
        addLog("Comparing with previous billing cycle...");
    },2000);

    setTimeout(function(){
        addLog("Root cause diagnosis in progress...");
    },3000);

    setTimeout(function(){
        addLog("Generating autonomous action plan...");
    },4000);

    setTimeout(function(){
        renderResults();
    },5000);
}

function renderResults(){

    G("running").classList.remove("on");
    G("results").classList.add("on");

    var anomalies = [
        {
            service:"EC2 Web Cluster",
            spike:50,
            wasted:50000,
            cause:"Auto Scaling Misconfiguration"
        },
        {
            service:"Azure Kubernetes",
            spike:47,
            wasted:30000,
            cause:"Unexpected Node Pool Scaling"
        }
    ];

    var actions = [
        "Reduce EC2 instances by 10 nodes",
        "Pause unused Azure node pool",
        "Enable budget alerts",
        "Activate auto shutdown policies"
    ];

    G("kpi-grid").innerHTML =
        "<div class='kpi'><div>Total Services</div><div class='big'>3</div></div>" +
        "<div class='kpi'><div>Anomalies</div><div class='big'>2</div></div>" +
        "<div class='kpi'><div>Spike</div><div class='big'>35%</div></div>" +
        "<div class='kpi'><div>Wasted</div><div class='big'>₹80K</div></div>";

    var html1 = "<ul>";
    anomalies.forEach(function(x){
        html1 += "<li><b>" + x.service + "</b> → +" + x.spike +
                 "% | Cause: " + x.cause +
                 " | Wasted: ₹" + x.wasted + "</li>";
    });
    html1 += "</ul>";

    var html2 = "<ul>";
    actions.forEach(function(x){
        html2 += "<li>" + x + "</li>";
    });
    html2 += "</ul>";

    G("anomaly-list").innerHTML = html1;
    G("action-list").innerHTML = html2;
}

function resetApp(){
    location.reload();
}
</script>

</body>
</html>
"""

st.components.v1.html(PAGE, height=1100, scrolling=True)
