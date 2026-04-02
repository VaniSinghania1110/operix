import streamlit as st
st.set_page_config(layout="wide", page_title="CostSense")
PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CostSense</title>
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
  overflow-x:hidden;
}

/* subtle grid */
body::before{
  content:'';
  position:fixed;
  inset:0;
  background-image:
    linear-gradient(rgba(255,255,255,0.018) 1px,transparent 1px),
    linear-gradient(90deg,rgba(255,255,255,0.018) 1px,transparent 1px);
  background-size:48px 48px;
  pointer-events:none;
  z-index:0;
}

/* ── NAV ── */
nav{
  display:flex;
  align-items:center;
  justify-content:space-between;
  padding:18px 40px;
  border-bottom:1px solid var(--b1);
  position:relative;
  z-index:10;
  backdrop-filter:blur(8px);
}

.nav-left{
  display:flex;
  align-items:center;
  gap:16px;
}

.nav-logo-box{
  width:36px;height:36px;
  background:linear-gradient(135deg,var(--blue),#2060cc);
  border-radius:8px;
  display:flex;align-items:center;justify-content:center;
  font-family:'IBM Plex Mono',monospace;
  font-weight:700;font-size:14px;
  color:#fff;
}

.nav-brand{
  font-family:'IBM Plex Sans',sans-serif;
  font-size:22px;
  font-weight:600;
  letter-spacing:-0.5px;
}

.nav-brand span{
  color:var(--blue);
}

.nav-badge{
  display:flex;align-items:center;gap:6px;
  border:1px solid var(--b2);
  border-radius:20px;
  padding:5px 12px;
  font-family:'IBM Plex Mono',monospace;
  font-size:10px;
  font-weight:500;
  letter-spacing:1.5px;
  color:var(--tx);
}

.nav-badge::before{
  content:'';
  width:6px;height:6px;
  border-radius:50%;
  background:var(--blue);
  box-shadow:0 0 8px var(--blue);
}

.nav-right{
  font-family:'IBM Plex Mono',monospace;
  font-size:11px;
  color:var(--mu);
  letter-spacing:0.5px;
}

.nav-right span{
  color:var(--dim);
}

/* ── MAIN SPLIT ── */
.main{
  display:grid;
  grid-template-columns:1fr 1fr;
  min-height:calc(100vh - 73px);
  position:relative;
  z-index:1;
}

/* LEFT HERO */
.hero{
  padding:60px 40px 60px 40px;
  display:flex;
  flex-direction:column;
  justify-content:center;
  border-right:1px solid var(--b1);
}

.hero-eyebrow{
  display:flex;
  align-items:center;
  gap:12px;
  margin-bottom:32px;
  font-family:'IBM Plex Mono',monospace;
  font-size:10px;
  font-weight:500;
  letter-spacing:3px;
  color:var(--mu);
  text-transform:uppercase;
}

.hero-eyebrow::before{
  content:'○';
  font-size:12px;
  color:var(--mu);
}

.hero-eyebrow::after{
  content:'';
  flex:1;
  height:1px;
  background:var(--b2);
  max-width:60px;
}

.hero-heading{
  font-family:'IBM Plex Sans',sans-serif;
  font-size:52px;
  font-weight:700;
  line-height:1.1;
  letter-spacing:-1.5px;
  margin-bottom:28px;
}

.hero-heading .line1{color:var(--tx)}
.hero-heading .line2{color:var(--blue)}
.hero-heading .line3{color:var(--green)}
.hero-heading .line4{color:var(--orange)}

.hero-desc{
  font-size:14px;
  color:var(--mu);
  line-height:1.75;
  max-width:420px;
  margin-bottom:32px;
}

.tag-row{
  display:flex;
  flex-wrap:wrap;
  gap:8px;
  margin-bottom:40px;
}

.tag{
  border:1px solid var(--b2);
  border-radius:4px;
  padding:5px 12px;
  font-family:'IBM Plex Mono',monospace;
  font-size:10px;
  font-weight:400;
  color:var(--mu);
  letter-spacing:0.5px;
  transition:border-color 0.2s,color 0.2s;
}

.tag:hover{border-color:var(--blue);color:var(--blue)}

/* ── UPLOAD FORM (left panel) ── */
.upload-section{
  display:flex;
  flex-direction:column;
  gap:12px;
}

.field-label{
  font-family:'IBM Plex Mono',monospace;
  font-size:9px;
  font-weight:500;
  letter-spacing:2.5px;
  text-transform:uppercase;
  color:var(--mu);
  margin-bottom:6px;
  display:flex;
  align-items:center;
  gap:8px;
}

.field-label::before{
  content:'';
  width:4px;height:4px;
  border-radius:50%;
  background:var(--blue);
}

.drop-zone{
  border:1px solid var(--b2);
  border-radius:6px;
  background:var(--sf);
  padding:28px 20px;
  text-align:center;
  cursor:pointer;
  position:relative;
  transition:all 0.2s;
}

.drop-zone:hover{
  border-color:var(--blue);
  background:rgba(77,166,255,0.05);
}

.drop-zone.has-file{
  border-color:var(--green);
  background:rgba(0,224,144,0.05);
}

#finput{
  position:absolute;inset:0;opacity:0;cursor:pointer;width:100%;height:100%;
}

.drop-icon{
  font-size:24px;
  margin-bottom:8px;
  display:block;
}

.drop-main{
  font-size:13px;
  font-weight:500;
  color:var(--tx);
  margin-bottom:4px;
}

.drop-sub{
  font-size:11px;
  color:var(--mu);
  font-family:'IBM Plex Mono',monospace;
}

#preview{
  display:none;
  width:100%;
  max-height:120px;
  object-fit:cover;
  border-radius:4px;
  margin-top:10px;
  border:1px solid var(--b2);
}

#preview.on{display:block}

.price-row{
  display:flex;
  align-items:stretch;
  border:1px solid var(--b2);
  border-radius:6px;
  overflow:hidden;
  background:var(--sf);
  transition:border-color 0.2s;
}

.price-row:focus-within{
  border-color:var(--blue);
}

.price-pre{
  padding:13px 16px;
  background:var(--b1);
  font-family:'IBM Plex Mono',monospace;
  font-size:16px;
  font-weight:600;
  color:var(--tx);
  border-right:1px solid var(--b2);
  display:flex;align-items:center;
}

#priceinput{
  border:none;outline:none;
  background:transparent;
  padding:13px 16px;
  font-family:'IBM Plex Mono',monospace;
  font-size:16px;
  font-weight:500;
  color:var(--tx);
  width:100%;
}

#priceinput::placeholder{color:var(--dim)}

.abtn{
  width:100%;
  padding:16px 24px;
  background:var(--blue);
  border:none;
  border-radius:6px;
  font-family:'IBM Plex Mono',monospace;
  font-size:12px;
  font-weight:600;
  letter-spacing:2px;
  text-transform:uppercase;
  color:#fff;
  cursor:pointer;
  transition:all 0.2s;
  display:flex;
  align-items:center;
  justify-content:center;
  gap:10px;
}

.abtn:hover{
  background:#5db5ff;
  box-shadow:0 0 24px rgba(77,166,255,0.35);
  transform:translateY(-1px);
}

/* ── RIGHT PANEL — AGENT CARDS ── */
.right-panel{
  padding:40px 32px;
  display:flex;
  flex-direction:column;
  gap:0;
  overflow-y:auto;
}

.right-header{
  font-family:'IBM Plex Mono',monospace;
  font-size:10px;
  font-weight:500;
  letter-spacing:3px;
  color:var(--mu);
  text-transform:uppercase;
  margin-bottom:20px;
  padding-bottom:16px;
  border-bottom:1px solid var(--b1);
}

.agent-card{
  display:flex;
  align-items:center;
  gap:16px;
  padding:18px 16px;
  border-bottom:1px solid var(--b1);
  position:relative;
  cursor:default;
  transition:background 0.15s;
}

.agent-card::before{
  content:'';
  position:absolute;
  left:0;top:0;bottom:0;
  width:3px;
  border-radius:0 2px 2px 0;
}

.agent-card:hover{
  background:var(--sf);
}

.ac-red::before{background:var(--red)}
.ac-green::before{background:var(--green)}
.ac-blue::before{background:var(--blue)}
.ac-yellow::before{background:var(--yellow)}
.ac-teal::before{background:var(--teal)}
.ac-purple::before{background:var(--purple)}
.ac-orange::before{background:var(--orange)}

.agent-icon{
  width:44px;height:44px;
  border-radius:8px;
  display:flex;align-items:center;justify-content:center;
  font-size:20px;
  flex-shrink:0;
  background:var(--sf);
  border:1px solid var(--b2);
}

.ac-red .agent-icon{background:rgba(255,71,87,0.12);border-color:rgba(255,71,87,0.25)}
.ac-green .agent-icon{background:rgba(0,224,144,0.1);border-color:rgba(0,224,144,0.2)}
.ac-blue .agent-icon{background:rgba(77,166,255,0.1);border-color:rgba(77,166,255,0.2)}
.ac-yellow .agent-icon{background:rgba(255,201,71,0.1);border-color:rgba(255,201,71,0.2)}
.ac-teal .agent-icon{background:rgba(0,207,200,0.1);border-color:rgba(0,207,200,0.2)}
.ac-purple .agent-icon{background:rgba(176,107,255,0.1);border-color:rgba(176,107,255,0.2)}
.ac-orange .agent-icon{background:rgba(255,107,53,0.1);border-color:rgba(255,107,53,0.2)}

.agent-info{flex:1;min-width:0}

.agent-name{
  font-size:14px;
  font-weight:600;
  color:var(--tx);
  margin-bottom:3px;
  white-space:nowrap;
  overflow:hidden;
  text-overflow:ellipsis;
}

.agent-desc{
  font-size:11px;
  color:var(--mu);
  font-family:'IBM Plex Mono',monospace;
  white-space:nowrap;
  overflow:hidden;
  text-overflow:ellipsis;
}

.agent-status{
  padding:4px 10px;
  border-radius:3px;
  font-family:'IBM Plex Mono',monospace;
  font-size:9px;
  font-weight:600;
  letter-spacing:1.5px;
  text-transform:uppercase;
  flex-shrink:0;
}

.status-active{background:rgba(0,224,144,0.15);color:var(--green);border:1px solid rgba(0,224,144,0.3)}
.status-idle{background:rgba(90,101,120,0.2);color:var(--mu);border:1px solid var(--b2)}

/* ── LOADER ── */
#ldr{
  display:none;
  position:fixed;inset:0;
  background:rgba(11,13,15,0.92);
  z-index:100;
  align-items:center;
  justify-content:center;
  flex-direction:column;
  gap:20px;
  backdrop-filter:blur(4px);
}

#ldr.on{display:flex}

.ldr-ring{
  width:56px;height:56px;
  border:2px solid var(--b2);
  border-top-color:var(--blue);
  border-radius:50%;
  animation:spin 0.75s linear infinite;
}

@keyframes spin{to{transform:rotate(360deg)}}

.ldr-text{
  font-family:'IBM Plex Mono',monospace;
  font-size:11px;
  letter-spacing:3px;
  text-transform:uppercase;
  color:var(--mu);
}

.ldr-dots{display:flex;gap:6px;margin-top:4px}

.ldr-dot{
  width:6px;height:6px;
  border-radius:50%;
  background:var(--b2);
  animation:dp 1.4s ease-in-out infinite;
}

.ldr-dot:nth-child(2){animation-delay:.2s}
.ldr-dot:nth-child(3){animation-delay:.4s}

@keyframes dp{
  0%,100%{background:var(--b2)}
  50%{background:var(--blue);box-shadow:0 0 8px var(--blue)}
}

/* ── RESULTS OVERLAY (replaces right panel) ── */
#results{display:none;flex-direction:column;gap:0}
#results.on{display:flex;animation:fadeIn 0.5s ease}

@keyframes fadeIn{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}

.res-header{
  padding:20px 0 16px;
  margin-bottom:4px;
  border-bottom:1px solid var(--b1);
  display:flex;
  align-items:center;
  justify-content:space-between;
}

.res-title{
  font-size:18px;
  font-weight:700;
  letter-spacing:-0.5px;
}

.res-badge{
  padding:5px 12px;
  background:rgba(0,224,144,0.12);
  border:1px solid rgba(0,224,144,0.3);
  border-radius:3px;
  font-family:'IBM Plex Mono',monospace;
  font-size:9px;
  font-weight:600;
  letter-spacing:2px;
  text-transform:uppercase;
  color:var(--green);
}

.rcard{
  display:flex;align-items:flex-start;gap:14px;
  padding:16px;
  border-bottom:1px solid var(--b1);
  position:relative;
  transition:background 0.15s;
}

.rcard:hover{background:var(--sf)}

.rcard::before{
  content:'';
  position:absolute;
  left:0;top:0;bottom:0;
  width:3px;
  border-radius:0 2px 2px 0;
}

.rcard-issue::before{background:var(--red)}
.rcard-comp::before{background:var(--blue)}
.rcard-sol::before{background:var(--green)}
.rcard-price::before{background:var(--orange)}

.rcard-icon{
  width:40px;height:40px;
  border-radius:8px;
  display:flex;align-items:center;justify-content:center;
  font-size:18px;
  flex-shrink:0;
  border:1px solid var(--b2);
}

.rcard-issue .rcard-icon{background:rgba(255,71,87,0.12);border-color:rgba(255,71,87,0.25)}
.rcard-comp .rcard-icon{background:rgba(77,166,255,0.1);border-color:rgba(77,166,255,0.2)}
.rcard-sol .rcard-icon{background:rgba(0,224,144,0.1);border-color:rgba(0,224,144,0.2)}
.rcard-price .rcard-icon{background:rgba(255,107,53,0.1);border-color:rgba(255,107,53,0.2)}

.rcard-body{flex:1}

.rcard-label{
  font-family:'IBM Plex Mono',monospace;
  font-size:9px;
  font-weight:500;
  letter-spacing:2px;
  text-transform:uppercase;
  color:var(--mu);
  margin-bottom:5px;
}

.rcard-title{
  font-size:14px;
  font-weight:600;
  margin-bottom:4px;
}

.rcard-desc{
  font-size:11px;
  color:var(--mu);
  font-family:'IBM Plex Mono',monospace;
  line-height:1.6;
}

.chip-row{
  display:flex;flex-wrap:wrap;gap:6px;margin-top:8px;
}

.chip{
  padding:3px 10px;
  background:rgba(77,166,255,0.08);
  border:1px solid rgba(77,166,255,0.2);
  border-radius:3px;
  font-family:'IBM Plex Mono',monospace;
  font-size:10px;
  color:var(--blue);
}

.sol-list{list-style:none;margin-top:8px;}
.sol-list li{
  display:flex;align-items:flex-start;gap:8px;
  padding:5px 0;
  font-size:11px;
  font-family:'IBM Plex Mono',monospace;
  color:var(--mu);
  border-bottom:1px solid var(--b1);
  line-height:1.5;
}
.sol-list li:last-child{border-bottom:none}
.sol-n{color:var(--green);font-weight:600;min-width:18px;font-size:10px;padding-top:1px}

/* savings card */
.savings-card{
  margin:12px 0 0;
  background:var(--sf);
  border:1px solid var(--b1);
  border-radius:6px;
  padding:16px;
}

.savings-row{
  display:grid;grid-template-columns:1fr 1fr 1fr;
  gap:12px;
}

.sav-item-label{
  font-family:'IBM Plex Mono',monospace;
  font-size:9px;
  letter-spacing:2px;
  text-transform:uppercase;
  color:var(--mu);
  margin-bottom:6px;
}

.sav-item-val{
  font-size:20px;
  font-weight:700;
  letter-spacing:-0.5px;
}

.sav-item-val.green{color:var(--green)}
.sav-item-val.orange{color:var(--orange)}

.reset-btn{
  margin-top:16px;
  padding:12px 20px;
  background:transparent;
  border:1px solid var(--b2);
  border-radius:6px;
  font-family:'IBM Plex Mono',monospace;
  font-size:10px;
  font-weight:500;
  letter-spacing:2px;
  text-transform:uppercase;
  color:var(--mu);
  cursor:pointer;
  transition:all 0.2s;
  width:100%;
}

.reset-btn:hover{border-color:var(--blue);color:var(--blue)}

/* stagger animations */
.agent-card{animation:fadeInRow 0.4s ease both}
.agent-card:nth-child(1){animation-delay:.05s}
.agent-card:nth-child(2){animation-delay:.1s}
.agent-card:nth-child(3){animation-delay:.15s}
.agent-card:nth-child(4){animation-delay:.2s}
.agent-card:nth-child(5){animation-delay:.25s}
.agent-card:nth-child(6){animation-delay:.3s}
.agent-card:nth-child(7){animation-delay:.35s}

@keyframes fadeInRow{
  from{opacity:0;transform:translateX(12px)}
  to{opacity:1;transform:translateX(0)}
}

</style>
</head>
<body>

<!-- NAV -->
<nav>
  <div class="nav-left">
    <div class="nav-logo-box">C</div>
    <div class="nav-brand">Cost<span>Sense</span></div>
    <div class="nav-badge">AI COST INTELLIGENCE</div>
  </div>
  <div class="nav-right">
    Claude AI &nbsp;<span>·</span>&nbsp; Vision Analysis &nbsp;<span>·</span>&nbsp; Cost Optimizer
  </div>
</nav>

<!-- MAIN SPLIT -->
<div class="main">

  <!-- LEFT HERO -->
  <div class="hero">
    <div class="hero-eyebrow">AI-Powered Cost Operations</div>
    <div class="hero-heading">
      <div class="line1">One Image.</div>
      <div class="line2">Detect.</div>
      <div class="line3">Analyse.</div>
      <div class="line4">Reduce.</div>
    </div>
    <p class="hero-desc">
      CostSense uses AI to scan your product image, identify cost inefficiencies across components, and instantly generate actionable reduction strategies — powered by computer vision and cost intelligence models.
    </p>

    <div class="tag-row">
      <span class="tag">Component Detection</span>
      <span class="tag">Price Benchmarking</span>
      <span class="tag">Supplier Alternatives</span>
      <span class="tag">Margin Analysis</span>
      <span class="tag">Cost Modelling</span>
      <span class="tag">Savings Report</span>
    </div>

    <!-- UPLOAD FORM -->
    <div id="usec" class="upload-section">

      <div>
        <div class="field-label">Product Image</div>
        <div class="drop-zone" id="dropzone">
          <input type="file" accept="image/*" id="finput">
          <span class="drop-icon" id="dicon">📁</span>
          <div class="drop-main" id="dmain">Drop image or click to browse</div>
          <div class="drop-sub">JPG · PNG · WEBP · max 10MB</div>
        </div>
        <img id="preview" src="" alt="">
      </div>

      <div>
        <div class="field-label">Current Price (₹)</div>
        <div class="price-row">
          <span class="price-pre">₹</span>
          <input type="number" id="priceinput" placeholder="Enter amount...">
        </div>
      </div>

      <button class="abtn" id="abtn">
        <span>→</span> Run Cost Analysis
      </button>

    </div>
  </div>

  <!-- RIGHT PANEL -->
  <div class="right-panel" id="rpanel">

    <!-- Default agent list -->
    <div id="agentList">
      <div class="right-header">Analysis Modules — 7 Active</div>

      <div class="agent-card ac-red">
        <div class="agent-icon">🔍</div>
        <div class="agent-info">
          <div class="agent-name">Component Detector</div>
          <div class="agent-desc">Identify parts, materials and assemblies from image</div>
        </div>
        <div class="agent-status status-active">ACTIVE</div>
      </div>

      <div class="agent-card ac-green">
        <div class="agent-icon">⚖️</div>
        <div class="agent-info">
          <div class="agent-name">Price Benchmarker</div>
          <div class="agent-desc">Compare against market and supplier databases</div>
        </div>
        <div class="agent-status status-active">ACTIVE</div>
      </div>

      <div class="agent-card ac-blue">
        <div class="agent-icon">📊</div>
        <div class="agent-info">
          <div class="agent-name">Cost Modeller</div>
          <div class="agent-desc">Build BOM cost trees and simulate reduction paths</div>
        </div>
        <div class="agent-status status-active">ACTIVE</div>
      </div>

      <div class="agent-card ac-yellow">
        <div class="agent-icon">🏭</div>
        <div class="agent-info">
          <div class="agent-name">Supplier Intelligence</div>
          <div class="agent-desc">Surface alternate vendors and regional sourcing</div>
        </div>
        <div class="agent-status status-active">ACTIVE</div>
      </div>

      <div class="agent-card ac-teal">
        <div class="agent-icon">📦</div>
        <div class="agent-info">
          <div class="agent-name">Packaging Analyser</div>
          <div class="agent-desc">Detect over-packaging and optimise material usage</div>
        </div>
        <div class="agent-status status-active">ACTIVE</div>
      </div>

      <div class="agent-card ac-purple">
        <div class="agent-icon">📉</div>
        <div class="agent-info">
          <div class="agent-name">Margin Optimizer</div>
          <div class="agent-desc">Compute max savings while protecting quality targets</div>
        </div>
        <div class="agent-status status-active">ACTIVE</div>
      </div>

      <div class="agent-card ac-orange">
        <div class="agent-icon">📋</div>
        <div class="agent-info">
          <div class="agent-name">Report Generator</div>
          <div class="agent-desc">Compile findings into actionable reduction playbook</div>
        </div>
        <div class="agent-status status-active">ACTIVE</div>
      </div>
    </div>

    <!-- Results (injected here) -->
    <div id="results">
      <div class="res-header">
        <div class="res-title" id="rprod">—</div>
        <div class="res-badge">✓ Complete</div>
      </div>

      <div class="rcard rcard-issue">
        <div class="rcard-icon">⚠️</div>
        <div class="rcard-body">
          <div class="rcard-label">Issue Detected</div>
          <div class="rcard-title">Cost Inefficiency</div>
          <div class="rcard-desc" id="rissue">—</div>
        </div>
      </div>

      <div class="rcard rcard-comp">
        <div class="rcard-icon">🔩</div>
        <div class="rcard-body">
          <div class="rcard-label">Cost Components</div>
          <div class="rcard-title">Identified Parts</div>
          <div id="rcomp"></div>
        </div>
      </div>

      <div class="rcard rcard-sol">
        <div class="rcard-icon">✅</div>
        <div class="rcard-body">
          <div class="rcard-label">Optimisation Steps</div>
          <div class="rcard-title">Recommended Actions</div>
          <div id="rsol"></div>
        </div>
      </div>

      <div class="rcard rcard-price">
        <div class="rcard-icon">💰</div>
        <div class="rcard-body">
          <div class="rcard-label">Price Reduction</div>
          <div class="rcard-title">Savings Summary</div>
          <div class="savings-card">
            <div class="savings-row">
              <div>
                <div class="sav-item-label">Original</div>
                <div class="sav-item-val" id="rbefore">—</div>
              </div>
              <div>
                <div class="sav-item-label">Optimised</div>
                <div class="sav-item-val orange" id="rafter">—</div>
              </div>
              <div>
                <div class="sav-item-label">Saved</div>
                <div class="sav-item-val green" id="rpct">—</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <button class="reset-btn" onclick="resetApp()">← New Analysis</button>
    </div>

  </div>
</div>

<!-- LOADER OVERLAY -->
<div id="ldr">
  <div class="ldr-ring"></div>
  <div class="ldr-text">Analysing Cost Structure</div>
  <div class="ldr-dots">
    <div class="ldr-dot"></div>
    <div class="ldr-dot"></div>
    <div class="ldr-dot"></div>
  </div>
</div>

<script>
var purl = "";
function G(id){return document.getElementById(id)}

G("finput").onchange = function(){
  var f = this.files[0];
  if(!f) return;
  var reader = new FileReader();
  reader.onload = function(e){
    purl = e.target.result;
    G("preview").src = purl;
    G("preview").classList.add("on");
    G("dropzone").classList.add("has-file");
    G("dicon").textContent = "✓";
    G("dmain").textContent = f.name;
  };
  reader.readAsDataURL(f);
};

G("abtn").onclick = function(){
  var f = G("finput").files[0];
  if(!f){alert("Please upload a product image"); return;}
  var price = parseFloat(G("priceinput").value);
  if(!price || price <= 0){alert("Please enter a valid price"); return;}

  G("ldr").classList.add("on");

  setTimeout(function(){
    G("ldr").classList.remove("on");

    var percent = 25;
    var after = Math.round(price * 0.75);
    var savings = price - after;

    G("rprod").innerText = "Smartphone";
    G("rissue").innerText = "High manufacturing and packaging cost across 3 key component categories. Alternate sourcing and packaging simplification can unlock significant margin.";

    G("rcomp").innerHTML =
      '<div class="chip-row">' +
      '<span class="chip">🔋 Battery</span>' +
      '<span class="chip">📱 Display</span>' +
      '<span class="chip">📷 Camera</span>' +
      '<span class="chip">📦 Packaging</span>' +
      '<span class="chip">⚡ Chipset</span>' +
      '</div>';

    G("rsol").innerHTML =
      '<ol class="sol-list">' +
      '<li><span class="sol-n">01</span>Switch to alternate supplier network — estimated 12% component cost reduction</li>' +
      '<li><span class="sol-n">02</span>Reduce packaging layers, use recycled outer casing material</li>' +
      '<li><span class="sol-n">03</span>Optimise regional sourcing to cut logistics overhead by ~8%</li>' +
      '</ol>';

    G("rbefore").innerText = "₹" + price.toLocaleString();
    G("rafter").innerText = "₹" + after.toLocaleString();
    G("rpct").innerText = percent + "% · ₹" + savings.toLocaleString();

    G("agentList").style.display = "none";
    G("results").classList.add("on");
  }, 3000);
};

function resetApp(){
  G("results").classList.remove("on");
  G("agentList").style.display = "block";
  G("priceinput").value = "";
  G("finput").value = "";
  purl = "";
  G("preview").classList.remove("on");
  G("dropzone").classList.remove("has-file");
  G("dicon").textContent = "📁";
  G("dmain").textContent = "Drop image or click to browse";
}
</script>
</body>
</html>
"""
st.components.v1.html(PAGE, height=900, scrolling=True)
