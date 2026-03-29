import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

# =========================
# SAFE HTML (FIXED VERSION)
# =========================

PAGE = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>SpendGuard Demo</title>

<style>
body {
    background: #0b1220;
    color: white;
    font-family: Arial;
    text-align: center;
}
h1 {
    color: #00d4ff;
}
button {
    background: #00d4ff;
    border: none;
    padding: 12px 20px;
    margin: 10px;
    cursor: pointer;
    font-weight: bold;
}
.card {
    background: #111d2e;
    padding: 20px;
    margin: 20px;
    border-radius: 10px;
}
</style>

</head>

<body>

<h1>🚀 SpendGuard AI — Anomaly Detection</h1>

<div class="card">
    <h2>Step 1: Configure</h2>
    <input id="org" placeholder="Enter Organisation" style="padding:10px;width:200px">
    <br>
    <button onclick="goNext()">Next</button>
</div>

<div id="step2" style="display:none" class="card">
    <h2>Step 2: Add Data</h2>
    <p>Sample data loaded automatically</p>
    <button onclick="runAI()">Run AI Agents</button>
</div>

<div id="result" style="display:none" class="card">
    <h2>🤖 AI Analysis Result</h2>
    <div id="output"></div>
</div>

<script>

function goNext() {
    document.querySelector('.card').style.display = "none";
    document.getElementById("step2").style.display = "block";
}

// 🔥 FULL FIXED AI FUNCTION (NO ERRORS)
async function callLLM() {

    // 👇 FAKE AI RESPONSE (NO API NEEDED)
    return {
        total_spike_pct: 35,
        anomaly_count: 2,
        anomalous_services: [
            {
                name: "EC2 Web Cluster",
                spike_pct: 52,
                severity: "HIGH",
                wasted_spend: 50000,
                cause: "Auto-scaling misconfiguration"
            },
            {
                name: "Azure AI Service",
                spike_pct: 40,
                severity: "MEDIUM",
                wasted_spend: 30000,
                cause: "New deployment spike"
            }
        ]
    };
}

async function runAI() {

    document.getElementById("step2").innerHTML = "<h2>⚡ Running AI Agents...</h2>";

    await new Promise(r => setTimeout(r, 1500));

    let data = await callLLM();

    let html = "";

    html += "<h3>Total Spike: +" + data.total_spike_pct + "%</h3>";
    html += "<h3>Anomalies Found: " + data.anomaly_count + "</h3>";

    data.anomalous_services.forEach(s => {
        html += `
        <div style="margin:10px;padding:10px;background:#1e3050;border-radius:8px">
            <b>${s.name}</b><br>
            Spike: +${s.spike_pct}%<br>
            Severity: ${s.severity}<br>
            Wasted Spend: ₹${s.wasted_spend}<br>
            Cause: ${s.cause}
        </div>
        `;
    });

    document.getElementById("result").style.display = "block";
    document.getElementById("output").innerHTML = html;
}

</script>

</body>
</html>
"""

components.html(PAGE, height=800, scrolling=True)
