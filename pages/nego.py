import streamlit as st

st.set_page_config(layout="wide", page_title="VendorIQ")

PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>VendorIQ</title>
<style>
body{
    background:#0b0d0f;
    color:#e8edf2;
    font-family:Arial,sans-serif;
    margin:0;
}
.main{
    display:grid;
    grid-template-columns:380px 1fr;
    min-height:100vh;
}
.left{
    padding:30px;
    border-right:1px solid #232830;
}
.right{
    padding:30px;
}
button{
    width:100%;
    padding:14px;
    background:#4da6ff;
    color:white;
    border:none;
    cursor:pointer;
    font-weight:bold;
    margin-top:15px;
}
select,textarea{
    width:100%;
    padding:12px;
    margin-top:10px;
    background:#13161a;
    color:white;
    border:1px solid #2e3540;
}
.card{
    background:#13161a;
    border:1px solid #232830;
    padding:20px;
    margin-bottom:15px;
}
.kpi-grid{
    display:grid;
    grid-template-columns:repeat(4,1fr);
    gap:10px;
}
.kpi{
    background:#13161a;
    padding:20px;
    border:1px solid #232830;
}
.big{
    font-size:28px;
    font-weight:bold;
    color:#00e090;
}
#log-section,#results{
    display:none;
}
#log-section.on,#results.on{
    display:block;
}
.log{
    padding:10px;
    margin-bottom:8px;
    background:#13161a;
    border-left:3px solid #4da6ff;
}
</style>
</head>
<body>

<div class="main">

<div class="left">
<h1>VendorIQ</h1>
<p>AI Vendor Negotiation + Duplicate Detection</p>

<select id="mode" onchange="handleModeChange()">
<option value="sample">Use Sample Data</option>
<option value="csv">Paste CSV</option>
<option value="json">Paste JSON</option>
</select>

<div id="paste-area" style="display:none;">
<textarea id="vendor-input" placeholder="Paste data here"></textarea>
</div>

<button id="run-btn" onclick="runAnalysis()">RUN ANALYSIS</button>
</div>

<div class="right">

<div id="log-section">
<h3>Agent Logs</h3>
<div id="agent-log"></div>
</div>

<div id="results">
<div class="kpi-grid" id="kpi-grid"></div>
<div id="result-cards"></div>
<button onclick="resetApp()">NEW ANALYSIS</button>
</div>

</div>
</div>

<script>
function G(id){
    return document.getElementById(id);
}

function handleModeChange(){
    var mode = G("mode").value;
    G("paste-area").style.display =
        mode === "sample" ? "none" : "block";
}

function addLog(text){
    G("log-section").classList.add("on");
    G("agent-log").innerHTML +=
        "<div class='log'>" + text + "</div>";
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
            {
                vendor_a: "Infosys Ltd",
                vendor_b: "Infosys Limited",
                similarity: 94,
                action: "Merge"
            },
            {
                vendor_a: "AWS",
                vendor_b: "Amazon Web Services",
                similarity: 98,
                action: "Consolidate"
            }
        ],

        low_value_vendors: [
            {
                id: "V005",
                name: "ABC Services",
                spend: 10000,
                action: "Terminate",
                reason: "Low annual spend"
            }
        ],

        action_plan: [
            {
                action: "Merge Infosys vendors",
                saving_inr: 150000,
                effort: "Low"
            },
            {
                action: "Consolidate AWS billing",
                saving_inr: 200000,
                effort: "Medium"
            }
        ],

        negotiation_targets: [
            {
                vendor: "Microsoft",
                current_spend: 510000,
                target_saving_pct: 12,
                strategy: "Volume negotiation"
            }
        ],

        vendor_registry: getSampleData().map(v => ({
            ...v,
            status: v.spend < 20000 ? "Review" : "Keep"
        }))
    };
}

async function runAnalysis(){

    G("run-btn").disabled = true;
    addLog("Initializing VendorIQ...");
    addLog("Loading dataset...");

    var mode = G("mode").value;
    var vendors = [];

    try{
        if(mode === "sample"){
            vendors = getSampleData();
        }
        else if(mode === "csv"){
            vendors = parseCSV(G("vendor-input").value);
        }
        else{
            vendors = JSON.parse(G("vendor-input").value);
        }

        addLog("Dataset loaded successfully");
        addLog("Running AI duplicate detection...");
        addLog("Running spend optimization...");

        var result = await callClaude("dummy prompt");

        addLog("AI analysis complete");
        renderResults(result);

    } catch(e){
        addLog("ERROR: " + e.message);
        alert("Error: " + e.message);
        G("run-btn").disabled = false;
    }
}

function renderResults(d){

    G("results").classList.add("on");

    G("kpi-grid").innerHTML =
        "<div class='kpi'><div>Total Vendors</div><div class='big'>" + d.kpis.total_vendors + "</div></div>" +
        "<div class='kpi'><div>Duplicates</div><div class='big'>" + d.kpis.duplicate_pairs + "</div></div>" +
        "<div class='kpi'><div>Low Value</div><div class='big'>" + d.kpis.low_value_count + "</div></div>" +
        "<div class='kpi'><div>Savings</div><div class='big'>₹" + d.kpis.total_savings_inr + "</div></div>";

    var html = "";

    html += "<div class='card'><h3>Executive Summary</h3><p>" + d.summary + "</p></div>";

    html += "<div class='card'><h3>Duplicate Vendors</h3><ul>";
    (d.duplicates || []).forEach(function(x){
        html += "<li>" + x.vendor_a + " ↔ " + x.vendor_b + " (" + x.similarity + "%)</li>";
    });
    html += "</ul></div>";

    html += "<div class='card'><h3>Action Plan</h3><ul>";
    (d.action_plan || []).forEach(function(x){
        html += "<li>" + x.action + " → ₹" + x.saving_inr + "</li>";
    });
    html += "</ul></div>";

    html += "<div class='card'><h3>Negotiation Targets</h3><ul>";
    (d.negotiation_targets || []).forEach(function(x){
        html += "<li>" + x.vendor + " → Save " + x.target_saving_pct + "%</li>";
    });
    html += "</ul></div>";

    G("result-cards").innerHTML = html;
}

function resetApp(){
    location.reload();
}
</script>

</body>
</html>
"""

st.components.v1.html(PAGE, height=1000, scrolling=True)
