
import streamlit as st

# Page config
st.set_page_config(layout="wide")

# =========================
# YOUR ORIGINAL HTML UI
# =========================
PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>NegotiatorAI</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,800;0,900;1,700&family=Manrope:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/@emailjs/browser@4/dist/email.min.js"></script>
<style>
*,::before,::after{box-sizing:border-box;margin:0;padding:0;}
html{scroll-behavior:smooth;}
:root{
  --void:#040507;--deep:#080b12;--layer1:#0d1018;--layer2:#111520;--layer3:#161b28;
  --edge:#1d2333;--edge2:#242d42;--fade:#3a4560;--muted:#5a6785;--body:#8b97b8;
  --text:#c8d3ee;--bright:#e8eeff;--white:#f4f6ff;
  --gold:#e8b84b;--gold2:#c49b2e;--gold-soft:rgba(232,184,75,0.12);--gold-rim:rgba(232,184,75,0.25);
  --emerald:#10d48a;--emerald-soft:rgba(16,212,138,0.1);--emerald-rim:rgba(16,212,138,0.22);
  --sapphire:#4d9ef7;--sapphire-soft:rgba(77,158,247,0.1);
  --ruby:#f74d6d;--ruby-soft:rgba(247,77,109,0.1);--ruby-rim:rgba(247,77,109,0.25);
  --amber:#f0a040;--amber-soft:rgba(240,160,64,0.1);--r:12px;
}
body{font-family:'Manrope',sans-serif;background:var(--void);color:var(--text);min-height:100vh;overflow-x:hidden;}
body::before{
  content:'';position:fixed;inset:0;z-index:0;pointer-events:none;opacity:0.035;
  background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
  background-size:180px 180px;
}
.ambiance{position:fixed;inset:0;z-index:0;pointer-events:none;overflow:hidden;}
.ambiance::before{content:'';position:absolute;width:900px;height:900px;border-radius:50%;background:radial-gradient(circle,rgba(232,184,75,0.055) 0%,transparent 65%);top:-400px;right:-300px;}
.ambiance::after{content:'';position:absolute;width:700px;height:700px;border-radius:50%;background:radial-gradient(circle,rgba(16,212,138,0.04) 0%,transparent 65%);bottom:-300px;left:-250px;}
nav{position:sticky;top:0;z-index:100;height:62px;display:flex;align-items:center;justify-content:space-between;padding:0 40px;background:rgba(4,5,7,0.85);border-bottom:1px solid var(--edge);backdrop-filter:blur(24px);}
.logo{display:flex;align-items:center;gap:11px;}
.logo-mark{width:36px;height:36px;border-radius:9px;background:linear-gradient(135deg,var(--gold),var(--gold2));display:grid;place-items:center;font-size:17px;box-shadow:0 0 20px rgba(232,184,75,0.3);position:relative;}
.logo-name{font-family:'Playfair Display',serif;font-size:18px;font-weight:700;color:var(--white);letter-spacing:-0.3px;}
.logo-name em{font-style:normal;color:var(--gold);}
.nav-tags{display:flex;gap:8px;align-items:center;}
.nt{font-size:10px;font-weight:700;letter-spacing:0.8px;padding:4px 11px;border-radius:20px;text-transform:uppercase;}
.nt-gold{background:var(--gold-soft);color:var(--gold);border:1px solid var(--gold-rim);}
.nt-em{background:var(--emerald-soft);color:var(--emerald);border:1px solid var(--emerald-rim);}
.nt-sap{background:var(--sapphire-soft);color:var(--sapphire);border:1px solid rgba(77,158,247,0.25);}
.pulse{display:inline-block;width:6px;height:6px;border-radius:50%;background:var(--emerald);margin-right:4px;animation:pulse 2s infinite;}
@keyframes pulse{0%,100%{opacity:1;box-shadow:0 0 0 rgba(16,212,138,0)}50%{opacity:0.5;box-shadow:0 0 8px rgba(16,212,138,0.5)}}
.canvas{position:relative;z-index:1;max-width:1000px;margin:0 auto;padding:52px 28px 120px;}
.hero{margin-bottom:56px;position:relative;}
.hero-sup{font-size:10px;font-weight:700;letter-spacing:3px;color:var(--muted);text-transform:uppercase;margin-bottom:20px;display:flex;align-items:center;gap:10px;}
.hero-sup::before{content:'';display:block;width:28px;height:1px;background:var(--gold);}
.hero h1{font-family:'Playfair Display',serif;font-size:clamp(38px,6vw,64px);font-weight:900;line-height:1.05;color:var(--white);letter-spacing:-1px;margin-bottom:18px;}
.hero h1 .accent{background:linear-gradient(90deg,var(--gold),var(--amber));-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-style:italic;}
.hero-desc{font-size:16px;color:var(--body);line-height:1.8;max-width:520px;margin-bottom:32px;}
.hero-flow{display:flex;align-items:center;gap:0;flex-wrap:wrap;row-gap:12px;}
.hf-step{display:flex;align-items:center;gap:8px;}
.hf-num{width:28px;height:28px;border-radius:50%;background:var(--layer2);border:1px solid var(--edge2);display:grid;place-items:center;font-size:11px;font-weight:700;color:var(--gold);font-family:'JetBrains Mono',monospace;flex-shrink:0;}
.hf-label{font-size:12px;color:var(--muted);font-weight:500;white-space:nowrap;}
.hf-arr{color:var(--edge2);margin:0 10px;font-size:14px;}
.wizard{display:flex;gap:0;margin-bottom:40px;background:var(--layer1);border:1px solid var(--edge);border-radius:14px;overflow:hidden;padding:4px;}
.wz-tab{flex:1;padding:12px 8px;text-align:center;cursor:pointer;border-radius:10px;transition:all 0.25s;font-size:12px;font-weight:600;color:var(--muted);display:flex;flex-direction:column;align-items:center;gap:4px;}
.wz-tab .wt-ico{font-size:18px;}
.wz-tab .wt-num{font-size:9px;font-weight:700;letter-spacing:1px;color:var(--edge2);text-transform:uppercase;margin-bottom:1px;}
.wz-tab.active{background:var(--layer3);color:var(--white);}
.wz-tab.active .wt-num{color:var(--gold);}
.wz-tab.done{color:var(--emerald);}
.wz-tab.done .wt-num{color:var(--emerald);}
.panel{display:none;animation:fadeUp 0.35s ease both;}
.panel.active{display:block;}
@keyframes fadeUp{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:translateY(0)}}
.srule{display:flex;align-items:center;gap:12px;margin-bottom:20px;}
.srule h2{font-size:13px;font-weight:700;color:var(--bright);white-space:nowrap;letter-spacing:0.3px;}
.srule-line{flex:1;height:1px;background:var(--edge);}
.gcard{background:var(--layer1);border:1px solid var(--edge);border-radius:16px;padding:28px 30px;margin-bottom:20px;position:relative;overflow:hidden;}
.gcard::before{content:'';position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,var(--edge2),transparent);}
.fg{display:grid;gap:16px;margin-bottom:16px;}
.fg-3{grid-template-columns:1fr 1fr 1fr;}
.fg-2{grid-template-columns:1fr 1fr;}
.fg-1{grid-template-columns:1fr;}
@media(max-width:640px){.fg-3,.fg-2{grid-template-columns:1fr;}}
.field{}
.field label{display:flex;align-items:center;gap:6px;font-size:11px;font-weight:700;letter-spacing:0.8px;color:var(--muted);text-transform:uppercase;margin-bottom:8px;}
.field label .req{color:var(--ruby);font-size:10px;}
.field label .opt{font-size:9px;color:var(--edge2);letter-spacing:1px;background:var(--layer2);padding:1px 6px;border-radius:20px;font-weight:600;}
.field input,.field select,.field textarea{width:100%;background:var(--layer2);border:1.5px solid var(--edge);border-radius:10px;color:var(--bright);font-family:'Manrope',sans-serif;font-size:14px;font-weight:500;padding:13px 16px;outline:none;transition:border-color 0.2s,box-shadow 0.2s;appearance:none;-webkit-appearance:none;}
.field input:focus,.field select:focus,.field textarea:focus{border-color:var(--gold);box-shadow:0 0 0 3px rgba(232,184,75,0.1);}
.field input::placeholder,.field textarea::placeholder{color:var(--fade);}
.field select{background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='8' fill='none'%3E%3Cpath d='M1 1l5 5 5-5' stroke='%235a6785' stroke-width='1.5' stroke-linecap='round'/%3E%3C/svg%3E");background-repeat:no-repeat;background-position:right 14px center;padding-right:38px;cursor:pointer;}
.field select option{background:var(--layer2);}
.field textarea{resize:vertical;min-height:96px;line-height:1.65;}
.field-hint{font-size:11px;color:var(--fade);margin-top:6px;line-height:1.5;}
.tip-box{background:var(--gold-soft);border:1px solid var(--gold-rim);border-radius:10px;padding:13px 16px;margin-bottom:16px;display:flex;gap:10px;font-size:12px;color:#c9a84c;line-height:1.6;}
.tip-box .ti{font-size:16px;flex-shrink:0;}
.strat-grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin-bottom:20px;}
@media(max-width:640px){.strat-grid{grid-template-columns:1fr 1fr;}}
.sg{border:1.5px solid var(--edge);border-radius:10px;padding:12px 14px;cursor:pointer;transition:all 0.2s;background:var(--layer2);}
.sg:hover{border-color:var(--gold);background:var(--gold-soft);}
.sg.on{background:var(--gold-soft);border-color:var(--gold);}
.sg-ico{font-size:20px;margin-bottom:6px;}
.sg-name{font-size:12px;font-weight:600;color:var(--text);margin-bottom:2px;}
.sg.on .sg-name{color:var(--gold);}
.sg-desc{font-size:10px;color:var(--muted);}
.power-wrap{margin-bottom:24px;}
.power-head{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;}
.power-lbl{font-size:11px;font-weight:700;letter-spacing:0.8px;color:var(--muted);text-transform:uppercase;}
.power-val{font-size:13px;font-weight:700;font-family:'JetBrains Mono',monospace;}
.power-track{height:6px;background:var(--edge);border-radius:99px;overflow:hidden;}
.power-fill{height:100%;border-radius:99px;transition:width 0.5s ease;background:linear-gradient(90deg,var(--ruby),var(--amber),var(--gold),var(--emerald));}
.nav-row{display:flex;gap:12px;margin-top:24px;}
.btn-next{flex:1;padding:15px;border:none;border-radius:11px;font-size:14px;font-weight:700;cursor:pointer;font-family:'Manrope',sans-serif;transition:all 0.2s;display:flex;align-items:center;justify-content:center;gap:8px;background:linear-gradient(135deg,var(--gold),var(--gold2));color:#0d0e10;box-shadow:0 4px 20px rgba(232,184,75,0.25);letter-spacing:0.3px;}
.btn-next:hover:not(:disabled){transform:translateY(-2px);box-shadow:0 8px 30px rgba(232,184,75,0.4);}
.btn-next:disabled{opacity:0.45;cursor:not-allowed;transform:none!important;}
.btn-back{padding:15px 20px;border:1.5px solid var(--edge2);border-radius:11px;font-size:13px;font-weight:600;cursor:pointer;font-family:'Manrope',sans-serif;transition:all 0.2s;background:transparent;color:var(--body);}
.btn-back:hover{color:var(--white);border-color:var(--fade);}
.term{background:#030508;border:1px solid var(--edge);border-radius:14px;overflow:hidden;}
.term-bar{background:#060810;padding:12px 18px;display:flex;align-items:center;gap:7px;border-bottom:1px solid var(--edge);}
.td{width:11px;height:11px;border-radius:50%;}
.td.r{background:#ff5f56;}.td.y{background:#febc2e;}.td.g{background:#28c840;}
.term-lbl{font-size:11px;color:var(--muted);margin-left:8px;font-family:'JetBrains Mono',monospace;}
.term-body{padding:18px 20px;min-height:220px;max-height:320px;overflow-y:auto;font-family:'JetBrains Mono',monospace;font-size:12px;line-height:1.9;}
.term-body::-webkit-scrollbar{width:4px;}
.term-body::-webkit-scrollbar-thumb{background:var(--edge2);border-radius:2px;}
.t-idle{color:var(--fade);text-align:center;padding:40px 0;font-size:12px;}
.t-row{display:flex;gap:10px;padding:2px 0;border-bottom:1px solid rgba(255,255,255,0.025);animation:tr 0.2s ease both;}
@keyframes tr{from{opacity:0;transform:translateX(-3px)}to{opacity:1}}
.t-ts{color:var(--fade);min-width:68px;font-size:10px;padding-top:2px;flex-shrink:0;}
.t-msg{flex:1;word-break:break-word;}
.ci{color:#58a6ff;}.cd{color:#484f58;font-style:italic;}.cok{color:#3fb950;}.cw{color:#d29922;}.ce{color:#f85149;}.cai{color:#bc8cff;}
.spin-row{display:flex;align-items:center;gap:9px;padding:6px 0;color:var(--gold);font-size:12px;}
.sdots{display:flex;gap:3px;}
.sd{width:5px;height:5px;border-radius:50%;background:var(--gold);animation:sb 1s infinite;}
.sd:nth-child(2){animation-delay:.15s;}.sd:nth-child(3){animation-delay:.3s;}
@keyframes sb{0%,80%,100%{transform:translateY(0);opacity:0.3}40%{transform:translateY(-6px);opacity:1}}
.ep{background:var(--layer2);border:1px solid var(--edge);border-radius:12px;overflow:hidden;margin-top:16px;display:none;}
.ep.show{display:block;animation:fadeUp 0.3s ease both;}
.ep-head{background:var(--layer3);border-bottom:1px solid var(--edge);padding:14px 18px;}
.ep-row{display:flex;gap:10px;font-size:12px;margin-bottom:5px;}
.ep-row:last-child{margin-bottom:0;}
.ep-k{color:var(--muted);font-weight:700;min-width:60px;font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:0.5px;}
.ep-v{color:var(--text);}
.ep-body{padding:20px;font-size:12.5px;color:var(--body);line-height:1.85;white-space:pre-wrap;font-family:'JetBrains Mono',monospace;}
.deals-stack{display:flex;flex-direction:column;gap:14px;}
.deal{background:var(--layer1);border:1px solid var(--edge);border-radius:16px;overflow:hidden;transition:border-color 0.2s;}
.deal:hover{border-color:var(--edge2);}
.deal-top{padding:20px 22px;display:flex;gap:14px;align-items:flex-start;}
.deal-ico{font-size:32px;flex-shrink:0;line-height:1;}
.deal-info{flex:1;}
.deal-vendor{font-size:15px;font-weight:700;color:var(--white);margin-bottom:2px;}
.deal-product{font-size:12px;color:var(--body);margin-bottom:8px;}
.deal-subject{font-size:11px;color:var(--muted);font-style:italic;margin-bottom:10px;}
.deal-chips{display:flex;gap:7px;flex-wrap:wrap;}
.dc{font-size:10px;font-weight:700;padding:3px 10px;border-radius:20px;letter-spacing:0.3px;}
.dc-sent{background:var(--sapphire-soft);color:var(--sapphire);border:1px solid rgba(77,158,247,0.25);}
.dc-neg{background:rgba(240,160,64,0.1);color:var(--amber);border:1px solid rgba(240,160,64,0.2);}
.dc-done{background:var(--emerald-soft);color:var(--emerald);border:1px solid var(--emerald-rim);}
.dc-demo{background:var(--gold-soft);color:var(--gold);border:1px solid var(--gold-rim);}
.deal-prices{text-align:right;flex-shrink:0;}
.dp-orig{font-size:11px;color:var(--muted);text-decoration:line-through;margin-bottom:3px;}
.dp-current{font-size:22px;font-weight:800;color:var(--emerald);font-family:'JetBrains Mono',monospace;line-height:1;}
.dp-save{font-size:10px;color:var(--emerald);margin-top:3px;font-weight:600;}
.deal-bar{padding:12px 22px;background:var(--layer2);border-top:1px solid var(--edge);display:flex;gap:9px;flex-wrap:wrap;align-items:center;}
.da{padding:7px 15px;border-radius:8px;font-size:12px;font-weight:600;cursor:pointer;font-family:'Manrope',sans-serif;border:1.5px solid;transition:all 0.15s;display:flex;align-items:center;gap:5px;}
.da:hover{filter:brightness(1.15);}
.da-gold{background:var(--gold-soft);color:var(--gold);border-color:var(--gold-rim);}
.da-em{background:var(--emerald-soft);color:var(--emerald);border-color:var(--emerald-rim);}
.da-sap{background:var(--sapphire-soft);color:var(--sapphire);border-color:rgba(77,158,247,0.25);}
.da-ruby{background:var(--ruby-soft);color:var(--ruby);border-color:var(--ruby-rim);}
.deal-time{font-size:10px;color:var(--fade);margin-left:auto;font-family:'JetBrains Mono',monospace;}
.empty-state{text-align:center;padding:60px 24px;border:1.5px dashed var(--edge);border-radius:16px;color:var(--fade);}
.empty-state .ei{font-size:48px;margin-bottom:14px;opacity:0.6;}
.empty-state h3{font-size:15px;font-weight:600;color:var(--muted);margin-bottom:6px;}
.empty-state p{font-size:13px;}
.modal-bg{display:none;position:fixed;inset:0;z-index:500;background:rgba(0,0,0,0.8);align-items:center;justify-content:center;backdrop-filter:blur(12px);}
.modal-bg.show{display:flex;}
.modal{background:var(--layer1);border:1px solid var(--edge2);border-radius:22px;padding:40px;max-width:500px;width:94%;position:relative;overflow:hidden;animation:mIn 0.3s cubic-bezier(0.34,1.56,0.64,1) both;box-shadow:0 30px 80px rgba(0,0,0,0.6);}
@keyframes mIn{from{opacity:0;transform:scale(0.88)}to{opacity:1;transform:scale(1)}}
.modal-glow{position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,var(--gold),var(--emerald),var(--sapphire));}
.modal-icon{font-size:50px;text-align:center;margin-bottom:14px;}
.modal h3{font-family:'Playfair Display',serif;font-size:26px;font-weight:800;color:var(--white);text-align:center;margin-bottom:8px;}
.modal-sub{font-size:13px;color:var(--body);text-align:center;margin-bottom:24px;line-height:1.65;}
.pricebox{background:var(--layer2);border:1px solid var(--edge2);border-radius:14px;padding:22px;margin-bottom:18px;text-align:center;}
.pb-lbl{font-size:10px;font-weight:700;letter-spacing:2px;color:var(--muted);text-transform:uppercase;margin-bottom:8px;}
.pb-val{font-family:'Playfair Display',serif;font-size:48px;font-weight:900;color:var(--gold);line-height:1;}
.pb-sub{font-size:12px;color:var(--muted);margin-top:6px;}
.modal-info{background:var(--emerald-soft);border:1px solid var(--emerald-rim);border-radius:10px;padding:13px 16px;font-size:12px;color:#6ee7b7;margin-bottom:20px;line-height:1.65;}
.modal-info strong{color:var(--emerald);}
.mbtn-row{display:flex;gap:10px;}
.mbtn-primary{flex:1;background:linear-gradient(135deg,var(--gold),var(--gold2));color:#0d0e10;border:none;border-radius:11px;padding:14px;font-size:14px;font-weight:700;cursor:pointer;font-family:'Manrope',sans-serif;transition:all 0.2s;letter-spacing:0.2px;}
.mbtn-primary:hover{filter:brightness(1.08);transform:translateY(-1px);}
.mbtn-ghost{background:var(--layer2);color:var(--body);border:1.5px solid var(--edge2);border-radius:11px;padding:14px 20px;font-size:13px;font-weight:600;cursor:pointer;font-family:'Manrope',sans-serif;transition:all 0.2s;}
.mbtn-ghost:hover{color:var(--white);}
footer{position:relative;z-index:1;text-align:center;padding:20px;border-top:1px solid var(--edge);font-size:11px;color:var(--muted);letter-spacing:0.3px;}
footer span{color:var(--body);}
</style>
</head>
<body>
<div class="ambiance"></div>

<nav>
  <div class="logo">
    <div class="logo-mark">🤝</div>
    <div class="logo-name">Negotiator<em>AI</em></div>
  </div>

</nav>

<div class="canvas">

  <div class="hero">
    <div class="hero-sup">Autonomous Deal Negotiation</div>
    <h1>Your AI Agent That<br><span class="accent">Fights For Best Price</span></h1>
    <p class="hero-desc">Enter your deal. The AI crafts a killer negotiation email, sends it to your vendor, and keeps replying until you get the price you want.</p>
    <div class="hero-flow">
      <div class="hf-step"><div class="hf-num">1</div><span class="hf-label">Fill deal details</span></div>
      <div class="hf-arr">→</div>
      <div class="hf-step"><div class="hf-num">2</div><span class="hf-label">AI writes email</span></div>
      <div class="hf-arr">→</div>
      <div class="hf-step"><div class="hf-num">3</div><span class="hf-label">Sent to vendor</span></div>
      <div class="hf-arr">→</div>
      <div class="hf-step"><div class="hf-num">4</div><span class="hf-label">AI handles replies</span></div>
      <div class="hf-arr">→</div>
      <div class="hf-step"><div class="hf-num">5</div><span class="hf-label">Deal closed 🏆</span></div>
    </div>
  </div>

  <div class="wizard" id="wizard">
    <div class="wz-tab active" id="tab1" onclick="goTab(1)">
      <span class="wt-num">Step 01</span><span class="wt-ico">🔧</span><span>Setup</span>
    </div>
    <div class="wz-tab" id="tab2" onclick="goTab(2)">
      <span class="wt-num">Step 02</span><span class="wt-ico">📋</span><span>Deal Info</span>
    </div>
    <div class="wz-tab" id="tab3" onclick="goTab(3)">
      <span class="wt-num">Step 03</span><span class="wt-ico">⚔️</span><span>Strategy</span>
    </div>
    <div class="wz-tab" id="tab4" onclick="goTab(4)">
      <span class="wt-num">Step 04</span><span class="wt-ico">🚀</span><span>Send &amp; Track</span>
    </div>
  </div>

  <!-- PANEL 1: SETUP -->
  <div class="panel active" id="panel1">
    <div class="srule"><h2>EmailJS Configuration</h2><div class="srule-line"></div></div>
    <div class="tip-box">
      <span class="ti">💡</span>
      <div><strong style="color:var(--gold);">Demo Mode:</strong> Preview your negotiation email without sending real emails. Add EmailJS keys above to send actual emails.</div>
    </div>
    <div class="gcard">
      <div class="fg fg-3" style="margin-bottom:16px;">
        <div class="field">
          <label>Service ID <span class="opt">optional</span></label>
          <input type="text" id="cfg_svc" placeholder="service_xxxxxxx">
        </div>
        <div class="field">
          <label>Template ID <span class="opt">optional</span></label>
          <input type="text" id="cfg_tpl" placeholder="template_xxxxxxx">
        </div>
        <div class="field">
          <label>Public Key <span class="opt">optional</span></label>
          <input type="text" id="cfg_key" placeholder="your_public_key">
        </div>
      </div>
      <div class="fg fg-2">
        <div class="field">
          <label>Your Name / Company <span class="req">*</span></label>
          <input type="text" id="cfg_name" placeholder="Rahul Sharma / TechCorp India" value="Your Company">
        </div>
        <div class="field">
          <label>Your Email <span class="req">*</span></label>
          <input type="email" id="cfg_email" placeholder="you@company.com" value="procurement@yourcompany.com">
          <div class="field-hint">📬 Vendor replies land here</div>
        </div>
      </div>
    </div>
    <div class="nav-row">
      <button class="btn-next" onclick="goTab(2)">Continue to Deal Details →</button>
    </div>
  </div>

  <!-- PANEL 2: DEAL -->
  <div class="panel" id="panel2">
    <div class="srule"><h2>Procurement Information</h2><div class="srule-line"></div></div>
    <div class="gcard">
      <div class="fg fg-2" style="margin-bottom:16px;">
        <div class="field">
          <label>Vendor / Supplier <span class="req">*</span></label>
          <input type="text" id="n_vendor" placeholder="Samsung India, Infosys, Reliance...">
        </div>
        <div class="field">
          <label>Vendor Email <span class="req">*</span></label>
          <input type="email" id="n_email" placeholder="sales@vendor.com">
        </div>
      </div>
      <div class="fg fg-3" style="margin-bottom:16px;">
        <div class="field">
          <label>Product / Service <span class="req">*</span></label>
          <input type="text" id="n_product" placeholder="Laptops, Raw Materials...">
        </div>
        <div class="field">
          <label>Quantity <span class="opt">optional</span></label>
          <input type="text" id="n_qty" placeholder="50 units, 500 kg...">
        </div>
        <div class="field">
          <label>Delivery Needed</label>
          <select id="n_delivery">
            <option value="immediately / ASAP">Immediately / ASAP</option>
            <option value="within 2 weeks">Within 2 weeks</option>
            <option value="within 1 month" selected>Within 1 month</option>
            <option value="within 3 months">Within 3 months</option>
            <option value="flexible">Flexible</option>
          </select>
        </div>
      </div>
      <div class="fg fg-3" style="margin-bottom:16px;">
        <div class="field">
          <label>Vendor's Quoted Price <span class="req">*</span></label>
          <input type="text" id="n_quoted" placeholder="₹5,00,000 or $10,000">
        </div>
        <div class="field">
          <label>Your Target Price <span class="req">*</span></label>
          <input type="text" id="n_target" placeholder="₹3,50,000 or $7,000">
          <div class="field-hint">🎯 AI fights hard to reach this</div>
        </div>
        <div class="field">
          <label>Max Budget <span class="opt">private</span></label>
          <input type="text" id="n_budget" placeholder="₹4,00,000 or $8,500">
          <div class="field-hint">🔒 Never revealed to vendor</div>
        </div>
      </div>
      <div class="fg fg-2">
        <div class="field">
          <label>Payment Terms</label>
          <select id="n_payment">
            <option value="100% payment upfront">100% Upfront — Best Leverage</option>
            <option value="50% upfront 50% on delivery">50/50 Split</option>
            <option value="Net 30 days">Net 30 Days</option>
            <option value="Net 60 days">Net 60 Days</option>
            <option value="Milestone-based">Milestone-Based</option>
          </select>
        </div>
        <div class="field">
          <label>Negotiation Tone</label>
          <select id="n_tone">
            <option value="firm and professional">Firm &amp; Professional</option>
            <option value="highly aggressive">Highly Aggressive</option>
            <option value="collaborative partner-focused">Collaborative Partner</option>
            <option value="urgent with hard deadline">Urgent — Hard Deadline</option>
          </select>
        </div>
      </div>
    </div>
    <div class="nav-row">
      <button class="btn-back" onclick="goTab(1)">← Back</button>
      <button class="btn-next" onclick="goTab(3)">Continue to Strategy →</button>
    </div>
  </div>

  <!-- PANEL 3: STRATEGY -->
  <div class="panel" id="panel3">
    <div class="srule"><h2>Negotiation Strategy</h2><div class="srule-line"></div></div>
    <div class="gcard" style="margin-bottom:16px;">
      <div style="font-size:11px;font-weight:700;letter-spacing:0.8px;color:var(--muted);text-transform:uppercase;margin-bottom:14px;">Choose Your Primary Strategy</div>
      <div class="strat-grid">
        <div class="sg on" onclick="pickStrat(this,'bulk volume discount')" id="sg0">
          <div class="sg-ico">📦</div><div class="sg-name">Bulk Discount</div><div class="sg-desc">Use quantity as leverage</div>
        </div>
        <div class="sg" onclick="pickStrat(this,'full upfront payment for discount')" id="sg1">
          <div class="sg-ico">💰</div><div class="sg-name">Pay Upfront</div><div class="sg-desc">Offer instant full payment</div>
        </div>
        <div class="sg" onclick="pickStrat(this,'long-term partnership and repeat business')" id="sg2">
          <div class="sg-ico">🤝</div><div class="sg-name">Long-term Partnership</div><div class="sg-desc">Promise repeat business</div>
        </div>
        <div class="sg" onclick="pickStrat(this,'competitor price matching — we have better quotes')" id="sg3">
          <div class="sg-ico">⚔️</div><div class="sg-name">Beat Competitor</div><div class="sg-desc">Mention rival quotes</div>
        </div>
        <div class="sg" onclick="pickStrat(this,'strict budget constraint — cannot exceed')" id="sg4">
          <div class="sg-ico">📊</div><div class="sg-name">Budget Cap</div><div class="sg-desc">Hard limit approach</div>
        </div>
        <div class="sg" onclick="pickStrat(this,'bundle multiple products for total deal')" id="sg5">
          <div class="sg-ico">🎁</div><div class="sg-name">Bundle Deal</div><div class="sg-desc">Package multiple items</div>
        </div>
      </div>
    </div>
    <div class="gcard">
      <div class="fg fg-1" style="margin-bottom:16px;">
        <div class="field">
          <label>Your Leverage Points <span class="req">*</span></label>
          <textarea id="n_leverage" placeholder="List everything you have. More = stronger AI. e.g:&#10;• Buying in bulk (50 units)&#10;• Can pay 100% upfront today&#10;• Loyal customer for 3 years&#10;• Comparing 3 vendor quotes right now&#10;• Can refer 5 new clients"></textarea>
          <div class="field-hint">💪 This is the most important field — every point becomes a weapon for the AI</div>
        </div>
      </div>
      <div class="fg fg-1" style="margin-bottom:16px;">
        <div class="field">
          <label>Competitor Quotes <span class="opt">very powerful</span></label>
          <input type="text" id="n_comp" placeholder="e.g. Competitor A quoted ₹3,80,000 · Vendor B at ₹4,00,000 for identical product">
          <div class="field-hint">⚔️ The single strongest leverage you can have</div>
        </div>
      </div>
      <div class="fg fg-1">
        <div class="field">
          <label>Additional Context <span class="opt">optional</span></label>
          <textarea id="n_context" style="min-height:68px;" placeholder="Past relationship, previous orders, project urgency, specific requirements..."></textarea>
        </div>
      </div>
    </div>
    <div class="gcard">
      <div class="power-wrap" style="margin-bottom:0;">
        <div class="power-head">
          <span class="power-lbl">Negotiation Power</span>
          <span class="power-val" id="powerVal" style="color:var(--muted)">—</span>
        </div>
        <div class="power-track"><div class="power-fill" id="powerFill" style="width:0%"></div></div>
        <div style="font-size:11px;color:var(--muted);margin-top:8px;" id="powerHint">Fill in the fields above to build your negotiation strength.</div>
      </div>
    </div>
    <div class="nav-row">
      <button class="btn-back" onclick="goTab(2)">← Back</button>
      <button class="btn-next" id="sendBtn" onclick="runAgent()">🚀 Generate &amp; Send Email</button>
    </div>
  </div>

  <!-- PANEL 4: TRACK -->
  <div class="panel" id="panel4">
    <div id="agentWrap" style="display:none;margin-bottom:24px;">
      <div class="srule"><h2>AI Agent Live</h2><div class="srule-line"></div></div>
      <div class="gcard" style="padding:0;overflow:hidden;">
        <div class="term">
          <div class="term-bar">
            <div class="td r"></div><div class="td y"></div><div class="td g"></div>
            <span class="term-lbl">negotiator-agent ~ deal processing</span>
            <span style="margin-left:auto;font-size:10px;font-family:'JetBrains Mono',monospace;color:var(--fade);" id="modelLbl">Llama 3.3 70B · Groq</span>
          </div>
          <div class="term-body" id="logBox"><div class="t-idle">Starting agent...</div></div>
        </div>
        <div class="ep" id="epWrap">
          <div class="ep-head">
            <div class="ep-row"><span class="ep-k">FROM</span><span class="ep-v" id="ep_from"></span></div>
            <div class="ep-row"><span class="ep-k">TO</span><span class="ep-v" id="ep_to"></span></div>
            <div class="ep-row"><span class="ep-k">SUBJECT</span><span class="ep-v" id="ep_subj"></span></div>
          </div>
          <div class="ep-body" id="ep_body"></div>
        </div>
      </div>
    </div>
    <div class="srule"><h2>Deal Tracker</h2><div class="srule-line"></div></div>
    <div id="dealTracker">
      <div class="empty-state">
        <div class="ei">📁</div>
        <h3>No deals yet</h3>
        <p>Complete the form and send your first negotiation email to see deals here.</p>
      </div>
    </div>
    <div class="nav-row">
      <button class="btn-back" onclick="goTab(3)">← New Negotiation</button>
    </div>
  </div>

</div>

<!-- SENT MODAL -->
<div class="modal-bg" id="sentModal">
  <div class="modal">
    <div class="modal-glow"></div>
    <div class="modal-icon">📧</div>
    <h3>Email Fired Off!</h3>
    <div class="modal-sub">Your AI negotiation email has been sent to <strong id="sm_vendor" style="color:var(--white)"></strong>. The agent is actively fighting for your target price.</div>
    <div class="pricebox">
      <div class="pb-lbl">Target Price</div>
      <div class="pb-val" id="sm_target"></div>
      <div class="pb-sub">AI will keep pushing until this is achieved</div>
    </div>
    <div class="modal-info">
      <strong>What's next?</strong> When the vendor replies, go to your <strong>Deal Tracker</strong> and click <strong>"Handle Reply"</strong>. The AI reads their response and fires back a perfect counter-offer automatically.
    </div>
    <div class="mbtn-row">
      <button class="mbtn-primary" onclick="closeSent()">Track This Deal →</button>
      <button class="mbtn-ghost" onclick="closeSent()">Close</button>
    </div>
  </div>
</div>

<!-- RESULT MODAL -->
<div class="modal-bg" id="resultModal">
  <div class="modal">
    <div class="modal-glow"></div>
    <div class="modal-icon" id="rm_ico">🔄</div>
    <h3 id="rm_title">Counter-Offer Sent</h3>
    <div class="modal-sub" id="rm_sub"></div>
    <div class="pricebox">
      <div class="pb-lbl" id="rm_lbl">Negotiated Price</div>
      <div class="pb-val" id="rm_price"></div>
      <div class="pb-sub" id="rm_sub2"></div>
    </div>
    <div class="modal-info" id="rm_info"></div>
    <div class="mbtn-row">
      <button class="mbtn-primary" onclick="closeResult()">✓ Got It</button>
    </div>
  </div>
</div>

<footer>NegotiatorAI &bull; Powered by Llama 3.3 70B · Groq &bull; <span id="tokenInfo">—</span></footer>

<script>
var GROQ_KEY = "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";
var GROQ_URL = "https://api.groq.com/openai/v1/chat/completions";
var MODEL    = "llama-3.3-70b-versatile";
var strategy = "bulk volume discount";
var deals    = [];
var curTab   = 1;

function $(id){ return document.getElementById(id); }
function val(id){ return $(id)?$(id).value.trim():''; }

function goTab(n){
  for(var i=1;i<=4;i++){
    $('panel'+i).classList.toggle('active', i===n);
    $('tab'+i).classList.remove('active','done');
    if(i===n) $('tab'+i).classList.add('active');
    else if(i<n) $('tab'+i).classList.add('done');
  }
  curTab=n;
  window.scrollTo({top:0,behavior:'smooth'});
}

function pickStrat(el, s){
  document.querySelectorAll('.sg').forEach(function(g){g.classList.remove('on');});
  el.classList.add('on');
  strategy=s;
  calcPower();
}

function calcPower(){
  var s=0;
  if(val('n_vendor'))   s+=10;
  if(val('n_email'))    s+=10;
  if(val('n_product'))  s+=10;
  if(val('n_quoted'))   s+=10;
  if(val('n_target'))   s+=10;
  if(val('n_leverage') && val('n_leverage').length>30) s+=25;
  if(val('n_comp'))     s+=15;
  if(val('n_budget'))   s+=5;
  if(val('n_context'))  s+=5;
  $('powerFill').style.width=s+'%';
  var pv=$('powerVal'), ph=$('powerHint');
  if(s<25){pv.textContent=s+'% Weak';pv.style.color='#f85149';ph.textContent='Add vendor info and leverage points to increase power.';}
  else if(s<50){pv.textContent=s+'% Building';pv.style.color='#f0a040';ph.textContent='Add leverage points and competitor quotes for more power.';}
  else if(s<75){pv.textContent=s+'% Strong 💪';pv.style.color='#e8b84b';ph.textContent='Good! Add competitor quotes to reach maximum power.';}
  else{pv.textContent=s+'% Maximum Power 🔥';pv.style.color='#3fb950';ph.textContent='Excellent! Your AI agent will negotiate at full strength.';}
}

document.addEventListener('DOMContentLoaded',function(){
  document.querySelectorAll('input,select,textarea').forEach(function(el){
    el.addEventListener('input',calcPower);el.addEventListener('change',calcPower);
  });
});

function L(step,msg,cls){
  var b=$('logBox'),r=document.createElement('div');r.className='t-row';
  var s=document.createElement('span');s.className='t-ts';s.textContent='['+step+']';
  var m=document.createElement('span');m.className='t-msg '+(cls||'ci');m.textContent=msg;
  r.appendChild(s);r.appendChild(m);b.appendChild(r);b.scrollTop=b.scrollHeight;
}
function showSpin(lbl){
  var b=$('logBox'),d=document.createElement('div');
  d.className='spin-row';d.id='spinner';
  d.innerHTML='<div class="sdots"><div class="sd"></div><div class="sd"></div><div class="sd"></div></div><span>'+(lbl||'Thinking...')+'</span>';
  b.appendChild(d);b.scrollTop=b.scrollHeight;
}
function rmSpin(){var s=$('spinner');if(s)s.remove();}

function groq(msgs,onOk,onErr){
  fetch(GROQ_URL,{method:'POST',headers:{'Content-Type':'application/json','Authorization':'Bearer '+GROQ_KEY},
    body:JSON.stringify({model:MODEL,temperature:0.65,max_tokens:1800,messages:msgs})})
  .then(function(r){return r.json();})
  .then(function(d){
    if(d.error) throw new Error(d.error.message||'Groq error');
    var t=((d.choices||[])[0]||{}).message?d.choices[0].message.content:'';
    var u=d.usage||{};
    $('tokenInfo').textContent='Tokens in:'+(u.prompt_tokens||0)+' out:'+(u.completion_tokens||0);
    onOk(t);
  }).catch(onErr);
}

function parseJ(t){
  try{return JSON.parse(t.replace(/```json/g,'').replace(/```/g,'').trim());}
  catch(e){var m=t.match(/\{[\s\S]*\}/);try{return JSON.parse(m[0]);}catch(e2){return null;}}
}

function showEP(from,to,subj,body){
  $('ep_from').textContent=from;$('ep_to').textContent=to;
  $('ep_subj').textContent=subj;$('ep_body').textContent=body;
  $('epWrap').classList.add('show');
}

function sendEmail(to,subj,body,fromName,fromEmail,cb){
  var svc=val('cfg_svc'),tpl=val('cfg_tpl'),key=val('cfg_key');
  if(!svc||!tpl||!key){
    L('DEMO','No EmailJS keys — Demo Mode: preview shown, email not sent','cw');
    setTimeout(function(){cb(true);},900);return;
  }
  emailjs.init(key);
  emailjs.send(svc,tpl,{to_email:to,subject:subj,message:body,from_name:fromName,reply_to:fromEmail})
  .then(function(){cb(false);})
  .catch(function(err){L('WARN','EmailJS: '+(err.text||'failed')+' — Demo Mode','cw');cb(true);});
}

function runAgent(){
  var vendor=val('n_vendor'),vemail=val('n_email'),product=val('n_product');
  var qty=val('n_qty'),delivery=val('n_delivery');
  var quoted=val('n_quoted'),target=val('n_target'),budget=val('n_budget');
  var payment=val('n_payment'),tone=val('n_tone');
  var leverage=val('n_leverage'),comp=val('n_comp'),context=val('n_context');
  var myName=val('cfg_name')||'Procurement Team',myEmail=val('cfg_email')||'procurement@company.com';

  if(!vendor||!product||!quoted||!target){
    alert('Please fill in: Vendor Name, Product, Quoted Price, and Target Price (Steps 1 & 2).');return;
  }
  if(!leverage){
    alert('Please add at least one leverage point in Step 3 — this is how the AI negotiates for you!');return;
  }

  var btn=$('sendBtn');
  btn.disabled=true;btn.textContent='🤖 Agent Working...';

  goTab(4);
  $('agentWrap').style.display='block';
  $('logBox').innerHTML='';
  $('epWrap').classList.remove('show');

  var pct=0;
  try{var q=parseFloat(quoted.replace(/[^0-9.]/g,'')),t=parseFloat(target.replace(/[^0-9.]/g,''));if(q>0)pct=Math.round((q-t)/q*100);}catch(e){}

  [{s:'INIT',m:'NegotiatorAI agent activated for procurement deal',c:'ci'},
   {s:'DEAL',m:'Vendor: '+vendor+' | Product: '+product+(qty?' ('+qty+')':''),c:'ci'},
   {s:'PRICE',m:'Quoted: '+quoted+' → Target: '+target+(pct?' ('+pct+'% reduction needed)':''),c:'cw'},
   {s:'STRAT',m:'Strategy: '+strategy+' | Tone: '+tone,c:'cd'},
   {s:'LEVERAGE',m:(leverage.split('\n').filter(Boolean).length||1)+' leverage points loaded — full power mode',c:'cd'},
   {s:'AI',m:'Sending to Llama 3.3 70B to craft negotiation email...',c:'cai'}
  ].forEach(function(x,i){setTimeout(function(){L(x.s,x.m,x.c);},i*380);});
  setTimeout(function(){showSpin('Llama 3.3 70B writing your negotiation email...');},6*380+100);

  var SYS="You are an elite procurement negotiation AI agent. Write devastatingly effective negotiation emails.\nRules:\n- Use EVERY leverage point — never waste a single one\n- Be firm and authoritative, never desperate or weak\n- Make a SPECIFIC counter-offer with crystal-clear reasoning\n- Use competitor quotes as hard leverage if provided\n- Create urgency: mention a decision deadline (end of week)\n- Never reveal the maximum budget\n- Sign professionally as the buyer\nReturn ONLY valid JSON (no markdown):\n{\"subject\":\"subject\",\"email\":\"full email\",\"reasoning\":\"why this will work (2 sentences)\",\"confidence\":85,\"predicted_response\":\"vendor will likely say...\"}";

  var USR="Write procurement negotiation email:\nFrom: "+myName+" ("+myEmail+")\nTo: "+vendor+"\nProduct: "+product+(qty?" | Qty: "+qty:"")+"\nDelivery: "+delivery+"\nQuoted: "+quoted+"\nTarget: "+target+(budget?"\nMax budget (NEVER reveal): "+budget:"")+"\nPayment offer: "+payment+"\nTone: "+tone+"\nStrategy: "+strategy+"\nLeverage:\n"+leverage+(comp?"\nCompetitor quotes (use hard): "+comp:"")+(context?"\nContext: "+context:"")+"\n\nCraft the most powerful email to get us to "+target+". Sign as "+myName+".";

  groq([{role:'system',content:SYS},{role:'user',content:USR}],
    function(text){
      rmSpin();
      var r=parseJ(text);
      if(!r){r={subject:"Re: "+product+" — Pricing Discussion",email:text,reasoning:"Direct leverage approach.",confidence:72,predicted_response:"Vendor will offer partial reduction."};}
      L('DRAFT','Email crafted — "'+r.subject+'"','cok');
      L('WHY',r.reasoning,'cd');
      L('CONF','Success confidence: '+r.confidence+'%','cw');
      L('EXPECT','Predicted: '+r.predicted_response,'ci');
      showEP(myName+' <'+myEmail+'>',vendor+' <'+(vemail||'vendor@email.com')+'>',r.subject,r.email);
      L('SEND','Dispatching to '+vendor+'...','cai');
      showSpin('Sending via EmailJS...');
      sendEmail(vemail||'demo@vendor.com',r.subject,r.email,myName,myEmail,function(isDemo){
        rmSpin();
        L(isDemo?'DEMO':'SENT',isDemo?'📧 Demo Mode — email preview shown (add EmailJS keys to send real emails)':'📧 Email successfully sent to '+vendor+'!',isDemo?'cw':'cok');
        L('TRACK','Deal saved to tracker below — waiting for vendor reply...','cok');
        var deal={id:Date.now(),vendor:vendor,vendorEmail:vemail,product:product,qty:qty,quoted:quoted,target:target,myName:myName,myEmail:myEmail,subject:r.subject,emailBody:r.email,confidence:r.confidence,status:'sent',isDemo:isDemo,timestamp:new Date().toLocaleString('en-IN'),rounds:0};
        deals.unshift(deal);renderDeals();
        $('sm_vendor').textContent=vendor;$('sm_target').textContent=target;
        $('sentModal').classList.add('show');
        btn.disabled=false;btn.innerHTML='🚀 Generate &amp; Send Email';
      });
    },
    function(err){rmSpin();L('ERROR',err.message,'ce');btn.disabled=false;btn.innerHTML='🚀 Generate &amp; Send Email';}
  );
}

function handleReply(id){
  var deal=deals.find(function(d){return d.id===id;});if(!deal)return;
  var reply=prompt("Paste the vendor's reply email here:\n(Copy and paste their full response)");
  if(!reply||!reply.trim())return;
  goTab(4);$('agentWrap').style.display='block';$('logBox').innerHTML='';$('epWrap').classList.remove('show');
  L('REPLY','Vendor reply received for: '+deal.vendor,'ci');
  L('READ','AI analyzing their response...','cd');
  showSpin('Reading vendor reply and crafting counter-offer...');
  var SYS2="You are an elite procurement negotiation AI. Vendor has replied. Craft the strongest counter-response.\nRules:\n- Acknowledge them professionally\n- Identify and dismantle weak excuses\n- Push firmly toward target price\n- Use any new info as additional leverage\n- Be polite but non-negotiable on key points\nReturn ONLY valid JSON:\n{\"subject\":\"subject\",\"email\":\"full counter-email\",\"analysis\":\"what their reply reveals\",\"new_predicted_price\":\"achievable price\",\"confidence\":80,\"recommendation\":\"push more | accept | close deal\"}";
  var USR2="Context: Vendor="+deal.vendor+" | Product="+deal.product+" | Quote="+deal.quoted+" | Target="+deal.target+"\n\nVendor's reply:\n"+reply+"\n\nWrite strongest counter-response toward "+deal.target+". Sign as "+deal.myName+".";
  groq([{role:'system',content:SYS2},{role:'user',content:USR2}],
    function(text){
      rmSpin();var r=parseJ(text);
      if(!r){r={subject:"Re: "+deal.product,email:text,analysis:"Vendor is open to negotiation.",new_predicted_price:deal.target,confidence:70,recommendation:"push more"};}
      L('ANALYSIS',r.analysis,'cd');L('COUNTER','Counter ready — Predicted: '+r.new_predicted_price,'cok');L('ADVICE','Recommendation: '+r.recommendation,'cw');
      showEP(deal.myName+' <'+deal.myEmail+'>',deal.vendor+' <'+(deal.vendorEmail||'vendor@email.com')+'>',r.subject,r.email);
      showSpin('Sending counter-offer...');
      sendEmail(deal.vendorEmail||'demo@vendor.com',r.subject,r.email,deal.myName,deal.myEmail,function(isDemo){
        rmSpin();L(isDemo?'DEMO':'SENT',isDemo?'Counter-offer simulated (Demo Mode)':'Counter-offer sent to '+deal.vendor+'!',isDemo?'cw':'cok');
        deal.status='negotiating';deal.predicted=r.new_predicted_price;deal.rounds=(deal.rounds||0)+1;
        renderDeals();
        $('rm_ico').textContent='🔄';$('rm_title').textContent='Counter-Offer Sent!';
        $('rm_sub').textContent='AI counter-offer sent to '+deal.vendor+'. Round '+deal.rounds+' of negotiation complete.';
        $('rm_lbl').textContent='Predicted Price';$('rm_price').textContent=r.new_predicted_price;
        $('rm_sub2').textContent='Original quote: '+deal.quoted;
        $('rm_info').innerHTML='<strong>Recommendation:</strong> '+r.recommendation+'. When they reply again, click Handle Reply to continue automatically.';
        $('resultModal').classList.add('show');
      });
    },
    function(err){rmSpin();L('ERROR',err.message,'ce');}
  );
}

function closeDeal(id){
  var deal=deals.find(function(d){return d.id===id;});if(!deal)return;
  var final=prompt("Enter the final agreed price to lock this deal:",deal.predicted||deal.target);
  if(!final)return;
  deal.status='closed';deal.finalPrice=final;
  $('rm_ico').textContent='🏆';$('rm_title').textContent='Deal Closed!';
  $('rm_sub').textContent='Congratulations! You closed a deal with '+deal.vendor+'.';
  $('rm_lbl').textContent='Final Price Locked';$('rm_price').textContent=final;
  $('rm_sub2').textContent='Started: '+deal.quoted+' → Closed: '+final;
  $('rm_info').innerHTML='<strong>🎉 Well done!</strong> Your AI agent successfully negotiated this procurement deal to the final price.';
  $('resultModal').classList.add('show');renderDeals();
}

function viewEmail(id){
  var deal=deals.find(function(d){return d.id===id;});if(!deal)return;
  goTab(4);$('agentWrap').style.display='block';
  showEP(deal.myName+' <'+deal.myEmail+'>',deal.vendor+' <'+(deal.vendorEmail||'vendor@email.com')+'>',deal.subject,deal.emailBody);
  window.scrollTo({top:0,behavior:'smooth'});
}

function renderDeals(){
  var el=$('dealTracker');
  if(!deals.length){
    el.innerHTML='<div class="empty-state"><div class="ei">📁</div><h3>No deals yet</h3><p>Complete the form and send your first negotiation email to see deals here.</p></div>';return;
  }
  var html='<div class="deals-stack">';
  deals.forEach(function(d){
    var ico='📤',stTag='';
    if(d.status==='sent'){ico='📤';stTag='<span class="dc dc-sent">Email Sent</span>';}
    if(d.status==='negotiating'){ico='🔄';stTag='<span class="dc dc-neg">Negotiating · Round '+d.rounds+'</span>';}
    if(d.status==='closed'){ico='🏆';stTag='<span class="dc dc-done">Deal Closed</span>';}
    var demoTag=d.isDemo?'<span class="dc dc-demo">Demo Mode</span>':'';
    var display=d.finalPrice||d.predicted||d.target;
    var qn=parseFloat((d.quoted||'').replace(/[^0-9.]/g,''))||0;
    var fn=parseFloat((display||'').replace(/[^0-9.]/g,''))||0;
    var sp=qn>0&&fn>0?Math.round((qn-fn)/qn*100):0;
    html+='<div class="deal">'
      +'<div class="deal-top">'
      +'<div class="deal-ico">'+ico+'</div>'
      +'<div class="deal-info">'
      +'<div class="deal-vendor">'+d.vendor+'</div>'
      +'<div class="deal-product">'+d.product+(d.qty?' &mdash; '+d.qty:'')+'</div>'
      +'<div class="deal-subject">'+d.subject+'</div>'
      +'<div class="deal-chips">'+stTag+demoTag+'</div>'
      +'</div>'
      +'<div class="deal-prices">'
      +'<div class="dp-orig">'+d.quoted+'</div>'
      +'<div class="dp-current">'+display+'</div>'
      +(sp>0?'<div class="dp-save">↓ '+sp+'% off</div>':'')
      +'</div>'
      +'</div>'
      +'<div class="deal-bar">';
    if(d.status!=='closed'){
      html+='<button class="da da-gold" onclick="handleReply('+d.id+')"><span>🔄</span> Handle Reply</button>';
      html+='<button class="da da-em" onclick="closeDeal('+d.id+')"><span>✅</span> Close Deal</button>';
    }
    html+='<button class="da da-sap" onclick="viewEmail('+d.id+')"><span>👁</span> View Email</button>';
    html+='<span class="deal-time">'+d.timestamp+'</span>';
    html+='</div></div>';
  });
  html+='</div>';el.innerHTML=html;
}

function closeSent(){$('sentModal').classList.remove('show');}
function closeResult(){$('resultModal').classList.remove('show');renderDeals();}
</script>
</body>
</html>"""

# =========================
# STREAMLIT UI WRAPPER
# =========================
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🤝 Negotiator AI")

# Render full HTML UI
st.components.v1.html(PAGE, height=900, scrolling=True)
