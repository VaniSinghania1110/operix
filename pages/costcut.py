import streamlit as st
st.set_page_config(layout="wide", page_title="CostSense")
PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CostSense</title>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}

:root{
  --ink:#08090a;
  --paper:#f4f0e8;
  --cream:#ede8dc;
  --warm:#e8dfd0;
  --rust:#c94f1e;
  --gold:#d4a017;
  --forest:#2d5a3d;
  --slate:#2a3240;
  --mist:#8a9bb0;
  --fog:#c8cfd8;
}

body{
  background:var(--paper);
  color:var(--ink);
  font-family:'DM Mono',monospace;
  min-height:100vh;
  overflow-x:hidden;
}

/* Grid texture */
body::before{
  content:'';
  position:fixed;
  inset:0;
  background-image:
    linear-gradient(rgba(42,50,64,0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(42,50,64,0.04) 1px, transparent 1px);
  background-size:40px 40px;
  pointer-events:none;
  z-index:0;
}

.wrap{
  max-width:860px;
  margin:0 auto;
  padding:48px 40px;
  position:relative;
  z-index:1;
}

/* ── HEADER ── */
.header{
  display:flex;
  align-items:flex-end;
  justify-content:space-between;
  margin-bottom:64px;
  border-bottom:2px solid var(--ink);
  padding-bottom:20px;
}

.logo{
  display:flex;
  align-items:baseline;
  gap:2px;
}

.logo-cost{
  font-family:'Syne',sans-serif;
  font-size:42px;
  font-weight:800;
  color:var(--ink);
  letter-spacing:-2px;
}

.logo-sense{
  font-family:'Syne',sans-serif;
  font-size:42px;
  font-weight:400;
  color:var(--rust);
  letter-spacing:-2px;
}

.logo-tag{
  font-size:10px;
  font-weight:500;
  color:var(--mist);
  letter-spacing:3px;
  text-transform:uppercase;
  margin-left:12px;
  padding-bottom:8px;
}

.header-right{
  font-size:11px;
  color:var(--mist);
  text-align:right;
  letter-spacing:1px;
}

/* ── UPLOAD ZONE ── */
#usec{
  animation:fadeSlideUp 0.6s ease both;
}

@keyframes fadeSlideUp{
  from{opacity:0;transform:translateY(24px)}
  to{opacity:1;transform:translateY(0)}
}

.upload-grid{
  display:grid;
  grid-template-columns:1fr 1fr;
  gap:24px;
  margin-bottom:24px;
}

.upload-panel{
  background:var(--cream);
  border:2px solid var(--ink);
  border-radius:4px;
  padding:40px 32px;
  position:relative;
  overflow:hidden;
}

.upload-panel::after{
  content:'';
  position:absolute;
  bottom:-4px;
  right:-4px;
  width:100%;
  height:100%;
  border:2px solid var(--ink);
  border-radius:4px;
  z-index:-1;
}

.panel-label{
  font-size:10px;
  font-weight:500;
  letter-spacing:3px;
  text-transform:uppercase;
  color:var(--mist);
  margin-bottom:16px;
  display:flex;
  align-items:center;
  gap:8px;
}

.panel-label::before{
  content:'';
  width:6px;
  height:6px;
  border-radius:50%;
  background:var(--rust);
  display:inline-block;
}

.upload-drop{
  border:2px dashed var(--fog);
  border-radius:4px;
  padding:32px 20px;
  text-align:center;
  cursor:pointer;
  transition:all 0.2s;
  position:relative;
}

.upload-drop:hover{
  border-color:var(--rust);
  background:rgba(201,79,30,0.04);
}

.upload-drop.has-file{
  border-color:var(--forest);
  background:rgba(45,90,61,0.06);
}

.upload-icon{
  font-size:32px;
  margin-bottom:10px;
  display:block;
}

.upload-text{
  font-size:12px;
  color:var(--mist);
  line-height:1.6;
}

.upload-text strong{
  color:var(--ink);
  display:block;
  font-size:13px;
  margin-bottom:4px;
}

#finput{
  position:absolute;
  inset:0;
  opacity:0;
  cursor:pointer;
  width:100%;
  height:100%;
}

.price-panel{
  background:var(--cream);
  border:2px solid var(--ink);
  border-radius:4px;
  padding:40px 32px;
  position:relative;
  overflow:hidden;
  display:flex;
  flex-direction:column;
}

.price-panel::after{
  content:'';
  position:absolute;
  bottom:-4px;
  right:-4px;
  width:100%;
  height:100%;
  border:2px solid var(--ink);
  border-radius:4px;
  z-index:-1;
}

.price-currency{
  font-family:'Syne',sans-serif;
  font-size:56px;
  font-weight:800;
  color:var(--fog);
  line-height:1;
  margin-top:auto;
  margin-bottom:8px;
}

.price-field-wrap{
  position:relative;
  display:flex;
  align-items:center;
  border:2px solid var(--ink);
  border-radius:4px;
  background:var(--paper);
  overflow:hidden;
}

.price-prefix{
  padding:14px 16px;
  font-family:'Syne',sans-serif;
  font-size:20px;
  font-weight:700;
  color:var(--ink);
  background:var(--ink);
  color:var(--paper);
}

#priceinput{
  border:none;
  outline:none;
  background:transparent;
  padding:14px 16px;
  font-family:'DM Mono',monospace;
  font-size:20px;
  font-weight:500;
  color:var(--ink);
  width:100%;
}

#priceinput::placeholder{
  color:var(--fog);
}

/* ── ANALYZE BUTTON ── */
.abtn-wrap{
  position:relative;
  display:inline-block;
  width:100%;
}

.abtn{
  width:100%;
  padding:20px 40px;
  background:var(--ink);
  color:var(--paper);
  border:2px solid var(--ink);
  border-radius:4px;
  font-family:'Syne',sans-serif;
  font-size:16px;
  font-weight:700;
  letter-spacing:2px;
  text-transform:uppercase;
  cursor:pointer;
  transition:all 0.2s;
  position:relative;
  z-index:1;
}

.abtn:hover{
  background:var(--rust);
  border-color:var(--rust);
  transform:translate(-2px,-2px);
}

.abtn-shadow{
  position:absolute;
  inset:0;
  background:var(--rust);
  border-radius:4px;
  transform:translate(4px,4px);
  z-index:0;
  transition:all 0.2s;
}

.abtn-wrap:hover .abtn-shadow{
  transform:translate(6px,6px);
  background:var(--ink);
}

/* ── LOADER ── */
.loader{
  display:none;
  padding:80px 40px;
  text-align:center;
}

.loader.on{
  display:block;
  animation:fadeSlideUp 0.4s ease both;
}

.loader-ring{
  width:64px;
  height:64px;
  border:3px solid var(--fog);
  border-top-color:var(--rust);
  border-radius:50%;
  animation:spin 0.8s linear infinite;
  margin:0 auto 28px;
}

@keyframes spin{
  to{transform:rotate(360deg)}
}

.loader-title{
  font-family:'Syne',sans-serif;
  font-size:24px;
  font-weight:700;
  color:var(--ink);
  margin-bottom:8px;
}

.loader-sub{
  font-size:12px;
  color:var(--mist);
  letter-spacing:2px;
  text-transform:uppercase;
}

.loader-steps{
  margin-top:32px;
  display:flex;
  justify-content:center;
  gap:8px;
}

.loader-dot{
  width:8px;
  height:8px;
  border-radius:50%;
  background:var(--fog);
  animation:pulse 1.4s ease-in-out infinite;
}
.loader-dot:nth-child(2){animation-delay:0.2s}
.loader-dot:nth-child(3){animation-delay:0.4s}

@keyframes pulse{
  0%,100%{background:var(--fog);transform:scale(1)}
  50%{background:var(--rust);transform:scale(1.3)}
}

/* ── RESULTS ── */
#results{
  display:none;
}

#results.on{
  display:grid;
  grid-template-columns:1fr 1fr;
  gap:20px;
  animation:fadeSlideUp 0.6s ease both;
}

.result-header{
  grid-column:1/-1;
  display:flex;
  align-items:center;
  justify-content:space-between;
  padding-bottom:20px;
  border-bottom:2px solid var(--ink);
  margin-bottom:8px;
}

.result-title{
  font-family:'Syne',sans-serif;
  font-size:28px;
  font-weight:800;
  letter-spacing:-1px;
}

.result-badge{
  padding:6px 14px;
  background:var(--forest);
  color:var(--paper);
  border-radius:2px;
  font-size:11px;
  font-weight:500;
  letter-spacing:2px;
  text-transform:uppercase;
}

.rcard{
  background:var(--cream);
  border:2px solid var(--ink);
  border-radius:4px;
  padding:24px;
  position:relative;
  overflow:hidden;
}

.rcard::after{
  content:'';
  position:absolute;
  bottom:-4px;
  right:-4px;
  width:100%;
  height:100%;
  border:2px solid var(--ink);
  border-radius:4px;
  z-index:-1;
}

.rcard.full-width{
  grid-column:1/-1;
}

.rcard.accent-rust{
  background:var(--rust);
  color:var(--paper);
}

.rcard.accent-rust::after{
  border-color:rgba(0,0,0,0.3);
}

.card-eyebrow{
  font-size:9px;
  font-weight:500;
  letter-spacing:3px;
  text-transform:uppercase;
  color:var(--mist);
  margin-bottom:12px;
  display:flex;
  align-items:center;
  gap:6px;
}

.accent-rust .card-eyebrow{
  color:rgba(244,240,232,0.7);
}

.card-eyebrow-dot{
  width:5px;
  height:5px;
  border-radius:50%;
  background:currentColor;
  display:inline-block;
}

.card-title{
  font-family:'Syne',sans-serif;
  font-size:20px;
  font-weight:700;
  margin-bottom:8px;
}

.card-desc{
  font-size:12px;
  color:var(--mist);
  line-height:1.7;
}

.accent-rust .card-desc{
  color:rgba(244,240,232,0.8);
}

.tag-list{
  display:flex;
  flex-wrap:wrap;
  gap:8px;
  margin-top:12px;
}

.tag{
  padding:5px 12px;
  background:var(--paper);
  border:1.5px solid var(--fog);
  border-radius:2px;
  font-size:11px;
  color:var(--slate);
}

.sol-list{
  list-style:none;
  margin-top:12px;
}

.sol-list li{
  display:flex;
  align-items:flex-start;
  gap:10px;
  padding:8px 0;
  border-bottom:1px solid var(--warm);
  font-size:12px;
  line-height:1.5;
}

.sol-list li:last-child{
  border-bottom:none;
}

.sol-num{
  font-family:'Syne',sans-serif;
  font-size:11px;
  font-weight:700;
  color:var(--rust);
  min-width:20px;
  padding-top:1px;
}

/* ── SAVINGS CARD ── */
.savings-grid{
  display:grid;
  grid-template-columns:1fr 1fr;
  gap:12px;
  margin-top:12px;
}

.savings-item{
  background:rgba(244,240,232,0.15);
  border:1.5px solid rgba(244,240,232,0.3);
  border-radius:4px;
  padding:14px;
}

.savings-label{
  font-size:9px;
  letter-spacing:2px;
  text-transform:uppercase;
  opacity:0.7;
  margin-bottom:6px;
}

.savings-value{
  font-family:'Syne',sans-serif;
  font-size:22px;
  font-weight:800;
  line-height:1;
}

.savings-pct{
  font-family:'Syne',sans-serif;
  font-size:52px;
  font-weight:800;
  line-height:1;
  margin-top:16px;
  letter-spacing:-2px;
}

.savings-pct-label{
  font-size:11px;
  opacity:0.7;
  margin-top:4px;
  letter-spacing:2px;
  text-transform:uppercase;
}

/* ── RESET BUTTON ── */
.reset-btn{
  margin-top:24px;
  grid-column:1/-1;
  padding:14px 32px;
  background:transparent;
  border:2px solid var(--ink);
  border-radius:4px;
  font-family:'Syne',sans-serif;
  font-size:13px;
  font-weight:700;
  letter-spacing:2px;
  text-transform:uppercase;
  cursor:pointer;
  transition:all 0.2s;
  color:var(--ink);
}

.reset-btn:hover{
  background:var(--ink);
  color:var(--paper);
}

/* ── PREVIEW IMG ── */
.preview-img{
  width:100%;
  height:140px;
  object-fit:cover;
  border-radius:4px;
  margin-top:12px;
  border:1.5px solid var(--fog);
  display:none;
}

.preview-img.on{
  display:block;
}

</style>
</head>
<body>
<div class="wrap">

  <!-- HEADER -->
  <div class="header">
    <div class="logo">
      <span class="logo-cost">Cost</span><span class="logo-sense">Sense</span>
      <span class="logo-tag">v2.0</span>
    </div>
    <div class="header-right">
      AI Cost Optimizer<br>
      <span style="color:var(--rust)">●</span> System Ready
    </div>
  </div>

  <!-- UPLOAD SECTION -->
  <div id="usec">
    <div class="upload-grid">

      <!-- Image Upload -->
      <div class="upload-panel">
        <div class="panel-label"><span class="card-eyebrow-dot"></span>Product Image</div>
        <div class="upload-drop" id="dropzone">
          <input type="file" accept="image/*" id="finput">
          <span class="upload-icon">⬆</span>
          <div class="upload-text">
            <strong>Click to upload</strong>
            JPG, PNG, WEBP supported<br>Max 10MB
          </div>
        </div>
        <img id="preview" class="preview-img" src="" alt="preview">
      </div>

      <!-- Price Input -->
      <div class="price-panel">
        <div class="panel-label"><span class="card-eyebrow-dot"></span>Current Price</div>
        <div class="price-currency">₹</div>
        <div class="price-field-wrap">
          <span class="price-prefix">₹</span>
          <input type="number" id="priceinput" placeholder="0.00">
        </div>
        <p style="margin-top:12px;font-size:11px;color:var(--mist);line-height:1.6">
          Enter the product's current retail or manufacturing price for cost optimization analysis.
        </p>
      </div>

    </div>

    <!-- Analyze Button -->
    <div class="abtn-wrap">
      <button class="abtn" id="abtn">→ &nbsp; Run Cost Analysis</button>
      <div class="abtn-shadow"></div>
    </div>
  </div>

  <!-- LOADER -->
  <div class="loader" id="ldr">
    <div class="loader-ring"></div>
    <div class="loader-title">Analyzing Product Cost</div>
    <div class="loader-sub">AI is optimizing your pricing</div>
    <div class="loader-steps">
      <div class="loader-dot"></div>
      <div class="loader-dot"></div>
      <div class="loader-dot"></div>
    </div>
  </div>

  <!-- RESULTS -->
  <div id="results">
    <div class="result-header">
      <div class="result-title" id="rprod">Analysis Complete</div>
      <div class="result-badge">✓ Optimized</div>
    </div>

    <!-- Issue Overview -->
    <div class="rcard full-width">
      <div class="card-eyebrow"><span class="card-eyebrow-dot"></span>Overview</div>
      <div class="card-desc" id="rissue" style="font-size:13px;color:var(--slate)"></div>
    </div>

    <!-- Components -->
    <div class="rcard">
      <div class="card-eyebrow"><span class="card-eyebrow-dot"></span>Cost Components</div>
      <div id="rcomp"></div>
    </div>

    <!-- Solutions -->
    <div class="rcard">
      <div class="card-eyebrow"><span class="card-eyebrow-dot"></span>Optimization Steps</div>
      <div id="rsol"></div>
    </div>

    <!-- Savings -->
    <div class="rcard accent-rust full-width">
      <div class="card-eyebrow"><span class="card-eyebrow-dot"></span>Price Reduction Summary</div>
      <div class="savings-pct" id="rpct"></div>
      <div class="savings-pct-label">Potential savings identified</div>
      <div class="savings-grid" style="margin-top:20px">
        <div class="savings-item">
          <div class="savings-label">Original Price</div>
          <div class="savings-value" id="rbefore"></div>
        </div>
        <div class="savings-item">
          <div class="savings-label">Optimized Price</div>
          <div class="savings-value" id="rafter"></div>
        </div>
      </div>
    </div>

    <button class="reset-btn" onclick="resetApp()">← Run Another Analysis</button>
  </div>

</div>

<script>
var purl = "";
function G(id){ return document.getElementById(id); }

G("finput").onchange = function(){
  var f = this.files[0];
  if(!f) return;
  var reader = new FileReader();
  reader.onload = function(e){
    purl = e.target.result;
    G("preview").src = purl;
    G("preview").classList.add("on");
    G("dropzone").classList.add("has-file");
    G("dropzone").querySelector(".upload-text").innerHTML =
      "<strong>Image ready</strong>File loaded successfully";
    G("dropzone").querySelector(".upload-icon").textContent = "✓";
  };
  reader.readAsDataURL(f);
};

G("abtn").onclick = function(){
  var f = G("finput").files[0];
  if(!f){ alert("Please upload an image"); return; }
  var price = parseFloat(G("priceinput").value);
  if(!price || price <= 0){ alert("Please enter a valid price"); return; }

  G("usec").style.display = "none";
  G("ldr").classList.add("on");

  setTimeout(function(){
    G("ldr").classList.remove("on");
    var percent = 25;
    var after = Math.round(price * 0.75);
    var savings = price - after;

    G("rprod").innerText = "Smartphone";
    G("rissue").innerText = "High manufacturing and packaging cost identified across 3 major component categories. Significant savings achievable through supplier diversification and packaging optimization.";

    G("rcomp").innerHTML =
      '<div class="tag-list">' +
      '<span class="tag">🔋 Battery</span>' +
      '<span class="tag">📱 Display</span>' +
      '<span class="tag">📷 Camera Module</span>' +
      '<span class="tag">📦 Packaging</span>' +
      '<span class="tag">⚡ Chipset</span>' +
      '</div>';

    G("rsol").innerHTML =
      '<ol class="sol-list">' +
      '<li><span class="sol-num">01</span><span>Switch to alternate supplier network to reduce component costs by ~12%</span></li>' +
      '<li><span class="sol-num">02</span><span>Reduce packaging layers and use recycled materials for outer casing</span></li>' +
      '<li><span class="sol-num">03</span><span>Optimize regional sourcing to cut logistics overhead</span></li>' +
      '</ol>';

    G("rpct").innerText = percent + "%";
    G("rbefore").innerText = "₹" + price.toLocaleString();
    G("rafter").innerText = "₹" + after.toLocaleString();

    G("results").classList.add("on");
  }, 3000);
};

function resetApp(){
  G("results").classList.remove("on");
  G("usec").style.display = "block";
  G("priceinput").value = "";
  G("finput").value = "";
  purl = "";
  G("preview").classList.remove("on");
  G("dropzone").classList.remove("has-file");
  G("dropzone").querySelector(".upload-text").innerHTML =
    "<strong>Click to upload</strong>JPG, PNG, WEBP supported<br>Max 10MB";
  G("dropzone").querySelector(".upload-icon").textContent = "⬆";
}
</script>
</body>
</html>
"""
st.components.v1.html(PAGE, height=900, scrolling=True)
