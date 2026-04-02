
import streamlit as st
from groq import Groq
from PIL import Image
import io, re, base64

st.set_page_config(page_title="Productly AI", layout="wide", initial_sidebar_state="collapsed")

for key, default in {
    "step": 0, "category": None, "audience": None,
    "image_desc": "", "result": "", "price_range": None,
    "chat_history": [],
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');
:root {
  --bg:#08090f;--bg2:#0e101a;--bg3:#141720;--bg4:#1a1e2e;
  --lime:#b8ff00;--coral:#ff5c5c;--purple:#a78bfa;--amber:#fbbf24;--teal:#2dd4bf;
  --text:#eef2ff;--text2:#c4c9e0;--muted:#4a5270;
  --border:rgba(255,255,255,0.06);--border2:rgba(255,255,255,0.1);
}
*,*::before,*::after{box-sizing:border-box;}
html,body,[data-testid="stAppViewContainer"],[data-testid="stMain"]{
  background:var(--bg)!important;font-family:'Plus Jakarta Sans',sans-serif!important;color:var(--text)!important;
}
[data-testid="stAppViewContainer"]::before{content:'';position:fixed;width:700px;height:700px;background:radial-gradient(circle,rgba(184,255,0,0.04) 0%,transparent 65%);top:-250px;left:-200px;pointer-events:none;z-index:0;}
[data-testid="stAppViewContainer"]::after{content:'';position:fixed;width:600px;height:600px;background:radial-gradient(circle,rgba(167,139,250,0.05) 0%,transparent 65%);bottom:-200px;right:-150px;pointer-events:none;z-index:0;}
#MainMenu,footer,header,[data-testid="stDecoration"],[data-testid="stToolbar"],[data-testid="stStatusWidget"]{display:none!important;}
[data-testid="stMainBlockContainer"]{max-width:1100px!important;padding:0 2.5rem 5rem!important;margin:0 auto!important;position:relative;z-index:1;}
[data-testid="stVerticalBlock"]{gap:0!important;}
::-webkit-scrollbar{width:4px;}::-webkit-scrollbar-thumb{background:rgba(184,255,0,0.2);border-radius:10px;}

@keyframes fadeUp{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:translateY(0)}}
@keyframes scalePop{0%{transform:scale(0.94);opacity:0}100%{transform:scale(1);opacity:1}}
@keyframes blink{0%,100%{opacity:1}50%{opacity:0.15}}
@keyframes barGrow{from{width:0!important}}
@keyframes bounceIn{0%{transform:scale(0.85);opacity:0}60%{transform:scale(1.04)}100%{transform:scale(1);opacity:1}}
.anim-up{animation:fadeUp 0.5s ease both;}.anim-pop{animation:scalePop 0.4s ease both;}
.d1{animation-delay:0.08s}.d2{animation-delay:0.16s}.d3{animation-delay:0.24s}.d4{animation-delay:0.32s}

/* WIZARD */
.wizard-progress{display:flex;align-items:center;justify-content:center;gap:0;padding:2.5rem 0 0;margin-bottom:2.5rem;}
.wp-step{display:flex;flex-direction:column;align-items:center;gap:6px;}
.wp-dot{width:36px;height:36px;border-radius:50%;border:2px solid var(--border);display:flex;align-items:center;justify-content:center;font-family:'JetBrains Mono',monospace;font-size:13px;font-weight:600;color:var(--muted);background:var(--bg2);transition:all 0.3s;}
.wp-dot.active{border-color:var(--lime);color:var(--bg);background:var(--lime);box-shadow:0 0 22px rgba(184,255,0,0.5);}
.wp-dot.done{border-color:var(--lime);color:var(--lime);background:rgba(184,255,0,0.1);}
.wp-label{font-size:10px;letter-spacing:1.5px;text-transform:uppercase;color:var(--muted);font-weight:600;white-space:nowrap;}
.wp-label.active{color:var(--lime);}
.wp-line{width:70px;height:1px;background:var(--border);margin:0 4px;margin-bottom:22px;flex-shrink:0;}
.wp-line.done{background:rgba(184,255,0,0.35);}

/* HERO */
.hero{text-align:center;padding:0.5rem 0 2.5rem;}
.hero-badge{display:inline-flex;align-items:center;gap:8px;background:rgba(184,255,0,0.06);border:1px solid rgba(184,255,0,0.2);padding:7px 20px;border-radius:50px;font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:1.5px;color:var(--lime);margin-bottom:24px;text-transform:uppercase;}
.hero-badge-dot{width:6px;height:6px;background:var(--lime);border-radius:50%;animation:blink 1.8s infinite;}
.hero-h1{font-family:'Sora',sans-serif!important;font-size:clamp(2.8rem,6vw,4.8rem)!important;font-weight:800!important;line-height:1.0!important;letter-spacing:-2px!important;color:var(--text)!important;margin-bottom:18px!important;}
.hero-h1 .acc{background:linear-gradient(135deg,var(--lime),#78e000);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
.hero-sub{font-size:1rem;color:var(--muted);line-height:1.7;max-width:440px;margin:0 auto 30px;}

/* FILE UPLOADER */
[data-testid="stFileUploaderDropzone"]{background:var(--bg2)!important;border:2px dashed rgba(184,255,0,0.2)!important;border-radius:22px!important;min-height:175px!important;transition:all 0.25s!important;}
[data-testid="stFileUploaderDropzone"]:hover{border-color:var(--lime)!important;box-shadow:0 0 40px rgba(184,255,0,0.1)!important;}
[data-testid="stFileUploaderDropzoneInstructions"] span{font-size:14px!important;color:var(--muted)!important;}
[data-testid="stFileUploaderDropzoneInstructions"] small{color:#2a3050!important;}

/* BUTTONS */
.stButton>button{background:var(--bg3)!important;border:1.5px solid var(--border2)!important;color:#6070a0!important;font-family:'Plus Jakarta Sans',sans-serif!important;font-size:13px!important;font-weight:600!important;border-radius:10px!important;height:2.7em!important;width:100%!important;transition:all 0.18s!important;}
.stButton>button:hover{border-color:rgba(184,255,0,0.4)!important;color:var(--lime)!important;background:rgba(184,255,0,0.05)!important;transform:translateY(-1px)!important;}
[data-testid="stBaseButton-primary"]>button{background:rgba(184,255,0,0.1)!important;border-color:var(--lime)!important;color:var(--lime)!important;box-shadow:0 4px 14px rgba(184,255,0,0.15)!important;}
.cta-wrap .stButton>button{background:linear-gradient(135deg,var(--lime),#78e000)!important;border:none!important;color:#060a00!important;font-family:'Sora',sans-serif!important;font-weight:800!important;font-size:15px!important;border-radius:14px!important;height:3.8em!important;box-shadow:0 0 36px rgba(184,255,0,0.28),0 8px 20px rgba(184,255,0,0.18)!important;transition:all 0.2s!important;}
.cta-wrap .stButton>button:hover{transform:translateY(-3px)!important;box-shadow:0 0 55px rgba(184,255,0,0.4),0 14px 32px rgba(184,255,0,0.22)!important;}
.ghost-wrap .stButton>button{background:transparent!important;border:1.5px solid var(--border2)!important;color:var(--muted)!important;font-size:13px!important;border-radius:11px!important;height:2.8em!important;}
.ghost-wrap .stButton>button:hover{border-color:rgba(184,255,0,0.3)!important;color:var(--lime)!important;}

/* TEXT INPUT */
.stTextInput>div>div>input{background:var(--bg)!important;border:1.5px solid var(--border2)!important;border-radius:10px!important;font-family:'Plus Jakarta Sans',sans-serif!important;font-size:14px!important;color:var(--text)!important;padding:10px 14px!important;}
.stTextInput>div>div>input:focus{border-color:rgba(184,255,0,0.5)!important;box-shadow:0 0 0 3px rgba(184,255,0,0.06)!important;}
.stTextInput label{font-size:10px!important;font-weight:700!important;letter-spacing:2px!important;text-transform:uppercase!important;color:var(--muted)!important;}
.stTextInput label span{color:transparent!important;}

/* IMG PREVIEW */
.img-preview{background:var(--bg2);border:1px solid var(--border2);border-radius:18px;overflow:hidden;box-shadow:0 16px 48px rgba(0,0,0,0.45);position:sticky;top:20px;}
.img-caption{padding:9px 13px;display:flex;gap:7px;flex-wrap:wrap;border-top:1px solid var(--border);}
.img-tag{font-family:'JetBrains Mono',monospace;font-size:10px;color:var(--muted);background:var(--bg);padding:2px 9px;border-radius:5px;border:1px solid var(--border);}

/* DASHBOARD */
.d-img-wrap{background:var(--bg2);border:1px solid var(--border2);border-radius:16px;overflow:hidden;box-shadow:0 14px 40px rgba(0,0,0,0.4);margin-bottom:10px;}
.d-img-foot{padding:8px 12px;display:flex;gap:7px;flex-wrap:wrap;border-top:1px solid var(--border);}
.d-tag{font-family:'JetBrains Mono',monospace;font-size:10px;color:var(--muted);background:var(--bg);padding:2px 9px;border-radius:5px;border:1px solid var(--border);}
.d-score-row{display:flex;align-items:center;gap:14px;background:linear-gradient(135deg,#070e05,#0b1808);border:1px solid rgba(184,255,0,0.15);border-radius:14px;padding:14px 16px;margin-bottom:10px;}
.d-ring-wrap{position:relative;flex-shrink:0;}
.d-ring-val{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:'Sora',sans-serif;font-size:1.35rem;font-weight:800;}
.d-verdict{font-family:'Sora',sans-serif;font-size:0.85rem;font-weight:700;}
.d-score-meta{font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:1.5px;text-transform:uppercase;color:var(--muted);margin:3px 0 6px;}
.d-vision{background:rgba(45,212,191,0.04);border:1px solid rgba(45,212,191,0.15);border-radius:11px;padding:10px 13px;margin-bottom:10px;}
.d-vision-lbl{font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:2px;text-transform:uppercase;color:var(--teal);margin-bottom:4px;display:block;}
.d-vision-tx{font-size:12px;line-height:1.6;color:#3a7a74;}

/* INSIGHT CARDS */
.ins-section{background:var(--bg2);border-radius:14px;border:1px solid var(--border2);padding:14px;margin-bottom:12px;transition:box-shadow 0.2s;}
.ins-section:hover{box-shadow:0 6px 28px rgba(0,0,0,0.3);}
.ins-sec-hdr{display:flex;align-items:center;gap:9px;padding-bottom:10px;border-bottom:1px solid var(--border);margin-bottom:10px;}
.ins-sec-dot{width:8px;height:8px;border-radius:50%;flex-shrink:0;}
.ins-sec-title{font-family:'Sora',sans-serif;font-size:11px;font-weight:700;letter-spacing:0.5px;flex:1;text-transform:uppercase;}
.ins-sec-badge{font-family:'JetBrains Mono',monospace;font-size:9px;font-weight:600;padding:2px 9px;border-radius:20px;letter-spacing:1px;}
.ins-row{display:flex;align-items:flex-start;gap:10px;padding:9px 10px;margin-bottom:6px;border-radius:9px;border:1px solid rgba(255,255,255,0.04);background:rgba(255,255,255,0.02);transition:all 0.18s;cursor:default;animation:fadeUp 0.4s ease both;}
.ins-row:last-child{margin-bottom:0;}
.ins-row:hover{background:rgba(255,255,255,0.05);transform:translateX(4px);}
.ins-row-icon{width:24px;height:24px;border-radius:7px;display:flex;align-items:center;justify-content:center;font-size:11px;flex-shrink:0;margin-top:1px;}
.ins-row-body{flex:1;min-width:0;}
.ins-row-head{font-family:'Sora',sans-serif;font-size:12.5px;font-weight:700;line-height:1.3;margin-bottom:3px;}
.ins-row-detail{font-size:11.5px;line-height:1.55;color:#4a5878;}
.ins-row-bar{height:2px;border-radius:2px;margin-top:6px;animation:barGrow 0.9s ease both;}

/* CHATBOT */
.chat-hero{background:linear-gradient(135deg,#0a081a,#100d25);border:1px solid rgba(167,139,250,0.2);border-radius:18px;padding:20px 24px;margin-bottom:14px;position:relative;overflow:hidden;}
.chat-hero::before{content:'';position:absolute;right:-50px;top:-50px;width:180px;height:180px;background:radial-gradient(circle,rgba(167,139,250,0.1) 0%,transparent 65%);pointer-events:none;}
.chat-hero-row{display:flex;align-items:center;gap:16px;}
.chat-avatar{width:48px;height:48px;border-radius:13px;background:linear-gradient(135deg,rgba(167,139,250,0.18),rgba(167,139,250,0.06));border:1px solid rgba(167,139,250,0.3);display:flex;align-items:center;justify-content:center;font-size:24px;flex-shrink:0;}
.chat-name{font-family:'Sora',sans-serif;font-size:1rem;font-weight:800;color:var(--text);margin-bottom:2px;}
.chat-tagline{font-size:11.5px;color:#6050a0;line-height:1.35;}
.chat-status{margin-left:auto;display:flex;align-items:center;gap:6px;font-family:'JetBrains Mono',monospace;font-size:10px;color:#5040a0;letter-spacing:1px;}
.chat-status-dot{width:7px;height:7px;border-radius:50%;background:#a78bfa;animation:blink 2s infinite;box-shadow:0 0 7px #a78bfa;}
.chat-lang-row{display:flex;gap:6px;flex-wrap:wrap;margin-top:12px;padding-top:12px;border-top:1px solid rgba(167,139,250,0.1);}
.chat-lang-chip{font-family:'JetBrains Mono',monospace;font-size:9.5px;font-weight:600;padding:3px 10px;border-radius:20px;background:rgba(167,139,250,0.07);border:1px solid rgba(167,139,250,0.16);color:rgba(167,139,250,0.55);}
.ctx-pill{display:flex;align-items:center;gap:10px;background:rgba(45,212,191,0.04);border:1px solid rgba(45,212,191,0.14);border-radius:11px;padding:9px 14px;margin-bottom:12px;}
.ctx-icon{font-size:15px;}
.ctx-label{font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:2px;text-transform:uppercase;color:var(--teal);display:block;margin-bottom:1px;}
.ctx-txt{font-size:12px;color:#2a8880;line-height:1.4;}

/* CHAT WINDOW — all bubbles rendered in one HTML block for correct flex alignment */
.chat-window{
  background:var(--bg2);border:1px solid var(--border2);
  border-radius:16px;padding:16px;min-height:280px;max-height:420px;
  overflow-y:auto;margin-bottom:12px;
  display:flex;flex-direction:column;gap:10px;
}
.chat-window::-webkit-scrollbar{width:3px;}
.chat-window::-webkit-scrollbar-thumb{background:rgba(167,139,250,0.2);border-radius:10px;}

/* Alignment wrappers */
.msg-row-user{display:flex;justify-content:flex-end;width:100%;}
.msg-row-bot{display:flex;justify-content:flex-start;width:100%;}

.chat-bubble{max-width:78%;padding:11px 15px;border-radius:16px;font-size:13.5px;line-height:1.65;word-break:break-word;animation:bounceIn 0.3s ease both;}
.user-bubble{background:linear-gradient(135deg,rgba(184,255,0,0.1),rgba(184,255,0,0.06));border:1px solid rgba(184,255,0,0.22);color:var(--text);border-bottom-right-radius:4px;}
.bot-bubble{background:linear-gradient(135deg,rgba(167,139,250,0.1),rgba(167,139,250,0.05));border:1px solid rgba(167,139,250,0.2);border-bottom-left-radius:4px;}
.bot-bubble-hdr{display:flex;align-items:center;gap:7px;margin-bottom:7px;padding-bottom:7px;border-bottom:1px solid rgba(167,139,250,0.1);}
.bot-mini-av{width:20px;height:20px;border-radius:6px;background:rgba(167,139,250,0.14);border:1px solid rgba(167,139,250,0.28);display:flex;align-items:center;justify-content:center;font-size:10px;flex-shrink:0;}
.bot-name-tag{font-family:'JetBrains Mono',monospace;font-size:9px;font-weight:600;color:rgba(167,139,250,0.65);letter-spacing:1px;text-transform:uppercase;}
.bot-bubble-txt{font-size:13px;line-height:1.65;color:#c0b8e0;}
.chat-empty{display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;height:100%;min-height:200px;gap:10px;}
.chat-empty-icon{font-size:34px;opacity:0.35;}
.chat-empty-txt{font-size:12.5px;color:var(--muted);line-height:1.5;max-width:260px;}

/* SUG BUTTONS */
.sug-btn-wrap .stButton>button{background:rgba(167,139,250,0.06)!important;border:1px solid rgba(167,139,250,0.2)!important;color:#9878e8!important;font-size:12px!important;border-radius:9px!important;height:auto!important;padding:8px 11px!important;white-space:normal!important;text-align:left!important;line-height:1.4!important;}
.sug-btn-wrap .stButton>button:hover{background:rgba(167,139,250,0.13)!important;border-color:rgba(167,139,250,0.42)!important;transform:translateY(-2px)!important;}

/* CHAT INPUT */
[data-testid="stChatInput"] textarea{background:var(--bg3)!important;border:1.5px solid rgba(167,139,250,0.22)!important;border-radius:13px!important;color:var(--text)!important;font-family:'Plus Jakarta Sans',sans-serif!important;font-size:14px!important;}
[data-testid="stChatInput"] textarea:focus{border-color:rgba(167,139,250,0.5)!important;box-shadow:0 0 0 3px rgba(167,139,250,0.06)!important;}
[data-testid="stChatInput"] textarea::placeholder{color:#2e2850!important;}
[data-testid="stHorizontalBlock"]{gap:10px!important;}
[data-testid="stAlert"]{border-radius:12px!important;}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────
# API
# ─────────────────────────────────────────────────────
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def describe_image(img_bytes):
    if not img_bytes:
        return "No image uploaded."

    try:
        pil = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        pil.thumbnail((1024, 1024), Image.LANCZOS)

        buf = io.BytesIO()
        pil.save(buf, format="JPEG", quality=85)

        b64 = base64.b64encode(buf.getvalue()).decode()

    except Exception as e:
        return f"Invalid image file: {e}"

    for model in [
        "meta-llama/llama-4-scout-17b-16e-instruct",
        "meta-llama/llama-4-maverick-17b-128e-instruct",
        "llava-v1.5-7b-4096-preview"
    ]:
        try:
            r = client.chat.completions.create(
                model=model,
                messages=[{
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{b64}"
                            }
                        },
                        {
                            "type": "text",
                            "text": "Describe this product in 60 words: what it is, packaging quality, design, colours, branding, target audience."
                        }
                    ]
                }],
                max_tokens=200
            )

            t = r.choices[0].message.content.strip()

            if len(t) > 15:
                return t

        except Exception:
            continue

    return "Vision unavailable."

def analyze_product(data):
    r = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role":"user","content":f"""
Senior product strategist. Analyse briefly.
Product: {data.get('category','')} | Audience: {data.get('audience','')} | Price: {data.get('price','')} | Vision: {data.get('image_desc','')} | Extra: {data.get('extra','')}

Rules: Each bullet = SHORT HEADLINE (3-4 words) :: one crisp sentence. No markdown. 3 bullets each.

GOOD:
- headline :: explanation
- headline :: explanation
- headline :: explanation

BAD:
- headline :: explanation
- headline :: explanation
- headline :: explanation

PRICE:
- headline :: explanation
- headline :: explanation
- headline :: explanation

IMPROVEMENTS:
- headline :: explanation
- headline :: explanation
- headline :: explanation
"""}], temperature=0.5, max_tokens=800)
    return r.choices[0].message.content.strip()

def parse_section(result, key):
    try:
        after = result.split(f"{key}:")[1]
        chunk = re.split(r"\n(?=(?:GOOD|BAD|PRICE|IMPROVEMENTS):)", after)[0].strip()
        return chunk or "Insufficient data."
    except: return "Insufficient data."

def get_parts(text):
    lines = [l.strip().lstrip("-").strip() for l in text.splitlines() if l.strip().lstrip("-").strip()]
    out = []
    for line in lines:
        if "::" in line:
            h, d = line.split("::", 1); out.append((h.strip(), d.strip()))
        else:
            w = line.split(); out.append((" ".join(w[:5]), " ".join(w[5:])))
    return out

def show_progress(active):
    steps = ["Upload","Details","Insights","Chat"]
    html = ""
    for i, label in enumerate(steps):
        dc = "active" if i==active else ("done" if i<active else "")
        lc = "active" if i==active else ""
        num = "✓" if i<active else str(i+1)
        html += f'<div class="wp-step"><div class="wp-dot {dc}">{num}</div><div class="wp-label {lc}">{label}</div></div>'
        if i < len(steps)-1:
            html += f'<div class="wp-line {"done" if i<active else ""}"></div>'
    st.markdown(f'<div class="wizard-progress">{html}</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════
# STEP 0 — UPLOAD
# ══════════════════════════════════════════════
if st.session_state.step == 0:
    show_progress(0)
    st.markdown("""
    <div class="hero anim-up">
      <div class="hero-badge"><span class="hero-badge-dot"></span>AI Product Intelligence · Live</div>
      <h1 class="hero-h1">Drop your product.<br><span class="acc">Get the edge.</span></h1>
      <p class="hero-sub">Upload any product image — instant analysis on strengths, risks, pricing & growth powered by Groq AI.</p>
    </div>""", unsafe_allow_html=True)
    _, mid, _ = st.columns([1,2.5,1])
    with mid:
        f = st.file_uploader("upload", type=["jpg","jpeg","png","webp"], label_visibility="collapsed", key="uploader_main")
        if f:
            st.session_state.uploaded_file_bytes = f.read()
            st.session_state.uploaded_file_name  = f.name
            st.session_state.uploaded_file_size  = f.size
            st.session_state.step = 1; st.rerun()
        st.markdown('<div style="text-align:center;margin-top:12px;color:#1e2240;font-size:11px;font-family:JetBrains Mono,monospace;">JPG · PNG · WEBP</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════
# STEP 1 — INTERACTIVE DETAILS
# ══════════════════════════════════════════════
elif st.session_state.step == 1:
    show_progress(1)

    img_bytes = st.session_state.get("uploaded_file_bytes", b"")
    img_name  = st.session_state.get("uploaded_file_name","product")
    img_size  = st.session_state.get("uploaded_file_size",0)
    pil_img   = Image.open(io.BytesIO(img_bytes))
    w, h      = pil_img.size

    st.markdown("""<div class="anim-up" style="margin-bottom:20px;">
      <div style="font-family:'Sora',sans-serif;font-size:1.7rem;font-weight:800;color:var(--text);letter-spacing:-0.5px;margin-bottom:5px;">Tell us about your product</div>
      <div style="font-size:13px;color:var(--muted);">Tap to select — minimal typing needed.</div>
    </div>""", unsafe_allow_html=True)

    col_img, col_form = st.columns([1, 1.65], gap="large")

    with col_img:
        st.markdown('<div class="img-preview anim-pop">', unsafe_allow_html=True)
        st.image(pil_img, use_container_width=True)
        st.markdown(
            f'<div class="img-caption"><span class="img-tag">{img_name[:18]}</span>'
            f'<span class="img-tag">{w}×{h}</span>'
            f'<span class="img-tag">{round(img_size/1024,1)} KB</span></div></div>',
            unsafe_allow_html=True)
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        if st.button("← Different image", key="back_btn"):
            for k in ["uploaded_file_bytes","uploaded_file_name","uploaded_file_size","category","audience","image_desc","result","price_range"]:
                st.session_state[k] = None
            st.session_state.step = 0; st.rerun()

    with col_form:
        st.markdown("""<div style="background:var(--bg2);border:1px solid var(--border2);
                        border-radius:18px;padding:22px 22px 20px;">""", unsafe_allow_html=True)

        # 01 — CATEGORY
        st.markdown("""<div style="font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:2px;
                        text-transform:uppercase;color:var(--lime);margin-bottom:12px;">
                        01 &nbsp;·&nbsp; What type of product?</div>""", unsafe_allow_html=True)
        cats = [("👟","Footwear"),("👕","Apparel"),("📱","Electronics"),("🍔","Food & Bev"),("🏠","Home"),("💄","Beauty"),("📦","Other")]
        r1 = st.columns(4)
        for i,(icon,name) in enumerate(cats[:4]):
            full = f"{icon} {name}"
            with r1[i]:
                t = "primary" if st.session_state.category==full else "secondary"
                if st.button(full, key=f"cat_{i}", use_container_width=True, type=t):
                    st.session_state.category=full; st.rerun()
        r2 = st.columns(4)
        for i,(icon,name) in enumerate(cats[4:]):
            full = f"{icon} {name}"
            with r2[i]:
                t = "primary" if st.session_state.category==full else "secondary"
                if st.button(full, key=f"cat_{i+4}", use_container_width=True, type=t):
                    st.session_state.category=full; st.rerun()

        # 02 — AUDIENCE — visual persona tiles
        st.markdown("""<div style="margin-top:18px;border-top:1px solid var(--border);padding-top:16px;">
          <div style="font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:2px;
                      text-transform:uppercase;color:var(--lime);margin-bottom:12px;">
            02 &nbsp;·&nbsp; Who's your buyer?</div>""", unsafe_allow_html=True)
        auds = [("🎓","Gen Z","16–24"),("💼","Professionals","25–40"),("👨‍👩‍👧","Families","30–50"),("💎","Luxury","All ages"),("🏋️","Wellness","20–45")]
        ac = st.columns(5)
        for i,(icon,name,sub) in enumerate(auds):
            full = f"{icon} {name}"
            with ac[i]:
                is_sel = st.session_state.audience==full
                bc2 = "rgba(184,255,0,0.5)" if is_sel else "rgba(255,255,255,0.07)"
                bg  = "rgba(184,255,0,0.08)" if is_sel else "var(--bg3)"
                fc  = "var(--lime)" if is_sel else "#4a5680"
                st.markdown(f"""<div style="background:{bg};border:1.5px solid {bc2};border-radius:12px;
                  padding:11px 6px;text-align:center;margin-bottom:7px;">
                  <div style="font-size:20px;margin-bottom:4px;">{icon}</div>
                  <div style="font-family:'Sora',sans-serif;font-size:11.5px;font-weight:700;color:{fc};">{name}</div>
                  <div style="font-size:9.5px;color:var(--muted);margin-top:2px;">{sub}</div>
                </div>""", unsafe_allow_html=True)
                t = "primary" if is_sel else "secondary"
                if st.button("✓ Picked" if is_sel else "Select", key=f"aud_{i}", use_container_width=True, type=t):
                    st.session_state.audience=full; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

        # 03 — PRICE RANGE — visual chips
        st.markdown("""<div style="margin-top:18px;border-top:1px solid var(--border);padding-top:16px;">
          <div style="font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:2px;
                      text-transform:uppercase;color:var(--lime);margin-bottom:12px;">
            03 &nbsp;·&nbsp; Expected price range</div>""", unsafe_allow_html=True)
        price_opts = [("₹","Budget","< ₹500"),("₹₹","Mid","₹500–2k"),("₹₹₹","Premium","₹2k–6k"),("💎","Luxury","₹6k+")]
        pc = st.columns(4)
        for i,(sym,label,rtxt) in enumerate(price_opts):
            pv = f"{sym} {label}"
            with pc[i]:
                is_sel = st.session_state.price_range==pv
                bc2 = "rgba(251,191,36,0.5)" if is_sel else "rgba(255,255,255,0.07)"
                bg  = "rgba(251,191,36,0.08)" if is_sel else "var(--bg3)"
                fc  = "#fbbf24" if is_sel else "#4a5680"
                st.markdown(f"""<div style="background:{bg};border:1.5px solid {bc2};border-radius:12px;
                  padding:11px 6px;text-align:center;margin-bottom:7px;">
                  <div style="font-family:'Sora',sans-serif;font-size:16px;font-weight:800;color:{fc};">{sym}</div>
                  <div style="font-size:12px;font-weight:700;color:{fc};margin:2px 0;">{label}</div>
                  <div style="font-size:9.5px;color:var(--muted);">{rtxt}</div>
                </div>""", unsafe_allow_html=True)
                t = "primary" if is_sel else "secondary"
                if st.button("✓" if is_sel else "Pick", key=f"pr_{i}", use_container_width=True, type=t):
                    st.session_state.price_range=pv; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

        # 04 — OPTIONAL EXTRA
        st.markdown("""<div style="margin-top:18px;border-top:1px solid var(--border);padding-top:14px;">
          <div style="font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:2px;
                      text-transform:uppercase;color:var(--lime);margin-bottom:10px;">
            04 &nbsp;·&nbsp; Anything extra? <span style="color:var(--muted);font-size:9px;">(optional)</span></div>
        """, unsafe_allow_html=True)
        extra = st.text_input("", placeholder="e.g. eco-friendly, competing with Pringles, D2C brand…", key="inp_extra")
        st.markdown("</div></div>", unsafe_allow_html=True)

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    _, cta_col, _ = st.columns([1,2,1])
    with cta_col:
        st.markdown('<div class="cta-wrap">', unsafe_allow_html=True)
        if st.button("✦  Generate AI Insights →", key="analyze_main", use_container_width=True):
            if not st.session_state.category: st.warning("⚡ Pick a category first.")
            elif not st.session_state.audience: st.warning("⚡ Pick a target audience.")
            elif not st.session_state.price_range: st.warning("⚡ Pick a price range.")
            else:
                with st.spinner("🔍 Vision AI scanning…"):
                    image_desc = describe_image(img_bytes); st.session_state.image_desc = image_desc
                with st.spinner("🧠 Crafting your insights…"):
                    result = analyze_product({"category":st.session_state.category,"audience":st.session_state.audience,"price":st.session_state.price_range,"extra":st.session_state.get("inp_extra",""),"image_desc":image_desc})
                    st.session_state.result = result
                st.session_state.step = 2; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# STEP 2 — CRISP INSIGHTS DASHBOARD
# ══════════════════════════════════════════════
elif st.session_state.step == 2:
    show_progress(2)

    result     = st.session_state.result
    image_desc = st.session_state.image_desc
    img_bytes  = st.session_state.get("uploaded_file_bytes", b"")
    pil_img    = Image.open(io.BytesIO(img_bytes))
    cat = st.session_state.get("category",""); aud = st.session_state.get("audience",""); pr = st.session_state.get("price_range","")

    gl = get_parts(parse_section(result,"GOOD")); bl = get_parts(parse_section(result,"BAD"))
    pl = get_parts(parse_section(result,"PRICE")); il = get_parts(parse_section(result,"IMPROVEMENTS"))

    gc=len(gl); bc=len(bl)
    score = round(min(9.8, max(5.0, 5.0+gc*1.1-bc*0.4)), 1)
    sp = int((score/10)*100)
    sc = "#b8ff00" if score>=7.5 else ("#fbbf24" if score>=6.0 else "#ff5c5c")
    vd = "Strong Market Fit" if score>=7.5 else ("Moderate Potential" if score>=6.0 else "Needs Work")
    vision_ok = bool(image_desc) and "unavailable" not in image_desc.lower()

    lc, rc = st.columns([1, 1.85], gap="large")

    with lc:
        st.markdown('<div class="d-img-wrap anim-pop">', unsafe_allow_html=True)
        iw, ih = pil_img.size
        thumb = pil_img.resize((int(iw*260/ih), 260), Image.LANCZOS)
        st.image(thumb, use_container_width=True)
        st.markdown(f'<div class="d-img-foot"><span class="d-tag">{cat}</span><span class="d-tag">{aud}</span><span class="d-tag">{pr}</span></div></div>', unsafe_allow_html=True)

        arc = int(sp*2.073)
        st.markdown(
            f'<div class="d-score-row anim-up d1"><div class="d-ring-wrap">'
            f'<svg viewBox="0 0 80 80" style="width:68px;height:68px">'
            f'<circle cx="40" cy="40" r="33" fill="none" stroke="rgba(255,255,255,0.06)" stroke-width="6"/>'
            f'<circle cx="40" cy="40" r="33" fill="none" stroke="{sc}" stroke-width="6"'
            f' stroke-linecap="round" stroke-dasharray="{arc} 207" transform="rotate(-90 40 40)"'
            f' style="filter:drop-shadow(0 0 6px {sc})"/></svg>'
            f'<div class="d-ring-val" style="color:{sc}">{score}<span style="font-size:10px;color:var(--muted)">/10</span></div></div>'
            f'<div><div class="d-verdict" style="color:{sc}">{vd}</div>'
            f'<div class="d-score-meta">Market Readiness</div>'
            f'<div style="display:flex;gap:8px;margin-top:3px">'
            f'<span style="font-family:JetBrains Mono,monospace;font-size:10px;color:#b8ff00">+{gc} strengths</span>'
            f'<span style="font-family:JetBrains Mono,monospace;font-size:10px;color:#ff5c5c">−{bc} risks</span>'
            f'</div></div></div>', unsafe_allow_html=True)

        if vision_ok:
            short_v = " ".join(image_desc.split()[:26])+("…" if len(image_desc.split())>26 else "")
            st.markdown(f'<div class="d-vision anim-up d2"><span class="d-vision-lbl">🔍 Vision Read</span><div class="d-vision-tx">{short_v}</div></div>', unsafe_allow_html=True)

    with rc:
        def render_sec(bullets, accent, bg, border, icon, label, icons, delay):
            rows = ""
            for j,(head,detail) in enumerate(bullets):
                bw = max(35, 95-j*20)
                rows += (f'<div class="ins-row" style="animation-delay:{55+j*50}ms">'
                         f'<div class="ins-row-icon" style="background:{bg}"><span style="color:{accent};font-weight:700">{icons[j%len(icons)]}</span></div>'
                         f'<div class="ins-row-body">'
                         f'<div class="ins-row-head" style="color:{accent}">{head}</div>'
                         f'<div class="ins-row-detail">{detail}</div>'
                         f'<div class="ins-row-bar" style="width:{bw}%;background:{accent};opacity:0.4"></div>'
                         f'</div></div>')
            return (f'<div class="ins-section anim-up {delay}" style="border-color:{border}">'
                    f'<div class="ins-sec-hdr">'
                    f'<div class="ins-sec-dot" style="background:{accent};box-shadow:0 0 8px {accent}"></div>'
                    f'<span class="ins-sec-title" style="color:{accent}">{icon} {label}</span>'
                    f'<span class="ins-sec-badge" style="color:{accent};background:{bg};border:1px solid {border}">{len(bullets)}</span>'
                    f'</div>{rows}</div>')

        t1, t2 = st.columns(2, gap="small")
        with t1:
            st.markdown(render_sec(gl,"#b8ff00","rgba(184,255,0,0.07)","rgba(184,255,0,0.17)","✦","STRENGTHS",["✦","★","◆"],"d1"), unsafe_allow_html=True)
            st.markdown(render_sec(pl,"#fbbf24","rgba(251,191,36,0.07)","rgba(251,191,36,0.17)","💰","PRICING",["$","₹","€"],"d3"), unsafe_allow_html=True)
        with t2:
            st.markdown(render_sec(bl,"#ff5c5c","rgba(255,92,92,0.07)","rgba(255,92,92,0.17)","⚠","RISKS",["!","✗","△"],"d2"), unsafe_allow_html=True)
            st.markdown(render_sec(il,"#a78bfa","rgba(167,139,250,0.07)","rgba(167,139,250,0.17)","🚀","GROWTH",["→","+","◎"],"d4"), unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    ba, bb, _ = st.columns([1.6,1.4,1])
    with ba:
        st.markdown('<div class="cta-wrap">', unsafe_allow_html=True)
        if st.button("💬  Chat with your Marketing AI  →", key="goto_chat", use_container_width=True):
            st.session_state.chat_history=[]; st.session_state.step=3; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    with bb:
        st.markdown('<div class="ghost-wrap">', unsafe_allow_html=True)
        if st.button("↺  Analyse Another", key="restart2", use_container_width=True):
            for k in ["uploaded_file_bytes","uploaded_file_name","uploaded_file_size","category","audience","image_desc","result","price_range","chat_history"]:
                st.session_state[k]=[] if k=="chat_history" else None
            st.session_state.step=0; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# STEP 3 — CHATBOT (bubbles properly aligned)
# ══════════════════════════════════════════════
elif st.session_state.step == 3:
    show_progress(3)
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    result     = st.session_state.get("result","")
    image_desc = st.session_state.get("image_desc","")
    cat        = st.session_state.get("category","")
    aud        = st.session_state.get("audience","")
    pr         = st.session_state.get("price_range","")

    SYSTEM = (
        "You are Productly AI, a friendly expert marketing advisor — warm, witty, practical. "
        f"You analysed: Category={cat}, Audience={aud}, Price={pr}. "
        f"Vision: {image_desc}. Analysis: {result}\n"
        "Rules: Reply in SAME language as user. Start with short energetic hook. "
        "Use 1-2 emojis. Under 120 words unless asked more. Reference the product analysis. Never be generic."
    )

    # Header
    st.markdown("""
    <div class="chat-hero anim-up">
      <div class="chat-hero-row">
        <div class="chat-avatar">🤖</div>
        <div>
          <div class="chat-name">Productly AI — Your Marketing Brain</div>
          <div class="chat-tagline">Pricing · Growth · Strategy · Campaigns — I already know your product 😎</div>
        </div>
        <div class="chat-status"><div class="chat-status-dot"></div>Online</div>
      </div>
      <div class="chat-lang-row">
        <span class="chat-lang-chip">🇬🇧 English</span>
        <span class="chat-lang-chip">🇮🇳 हिन्दी</span>
        <span class="chat-lang-chip">🇮🇳 Hinglish</span>
        <span class="chat-lang-chip">🇪🇸 Español</span>
        <span class="chat-lang-chip">🇫🇷 Français</span>
        <span class="chat-lang-chip">🇸🇦 عربي</span>
        <span class="chat-lang-chip">🇨🇳 中文</span>
      </div>
    </div>""", unsafe_allow_html=True)

    st.markdown(
        f'<div class="ctx-pill anim-up d1"><span class="ctx-icon">🎯</span>'
        f'<div><span class="ctx-label">Context Loaded</span>'
        f'<span class="ctx-txt">Analysed your <strong style="color:var(--teal)">{cat}</strong> '
        f'for <strong style="color:var(--teal)">{aud}</strong> at <strong style="color:var(--teal)">{pr}</strong>. '
        f'Answers are product-specific, not generic.</span></div></div>',
        unsafe_allow_html=True)

    # Suggestions
    if not st.session_state.chat_history:
        st.markdown("""<div style="font-family:'JetBrains Mono',monospace;font-size:9.5px;letter-spacing:2px;
                        text-transform:uppercase;color:#252840;margin-bottom:8px;">💡 Quick starters</div>""", unsafe_allow_html=True)
        suggestions = [
            ("💸","How should I price for Gen Z?"),
            ("📣","Best marketing channels for this?"),
            ("🤔","इसे कैसे improve करूं?"),
            ("🏆","Top 3 competitors & how to beat them?"),
            ("📦","How to improve packaging appeal?"),
            ("🌍","Which market to expand to first?"),
        ]
        cols = st.columns(3)
        for i,(icon,sug) in enumerate(suggestions):
            with cols[i%3]:
                st.markdown('<div class="sug-btn-wrap">', unsafe_allow_html=True)
                if st.button(f"{icon} {sug}", key=f"sug_{i}", use_container_width=True):
                    st.session_state.chat_history.append({"role":"user","content":sug})
                    with st.spinner(""):
                        msgs=[{"role":"system","content":SYSTEM}]+st.session_state.chat_history
                        resp=client.chat.completions.create(model="llama-3.3-70b-versatile",messages=msgs,max_tokens=300,temperature=0.75)
                        st.session_state.chat_history.append({"role":"assistant","content":resp.choices[0].message.content.strip()})
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── ALL BUBBLES RENDERED IN ONE HTML BLOCK ──
    # This is the key fix: flex alignment only works correctly when all bubbles
    # are inside the same flex container element, rendered as one st.markdown call.
    bubbles_html = ""
    if not st.session_state.chat_history:
        bubbles_html = """<div class="chat-empty">
          <div class="chat-empty-icon">💬</div>
          <div class="chat-empty-txt">Ask anything about pricing, marketing, improvements, or campaign ideas.</div>
        </div>"""
    else:
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                bubbles_html += (
                    f'<div class="msg-row-user">'
                    f'<div class="chat-bubble user-bubble">{msg["content"]}</div>'
                    f'</div>'
                )
            else:
                bubbles_html += (
                    f'<div class="msg-row-bot">'
                    f'<div class="chat-bubble bot-bubble">'
                    f'<div class="bot-bubble-hdr"><div class="bot-mini-av">🤖</div>'
                    f'<span class="bot-name-tag">Productly AI</span></div>'
                    f'<div class="bot-bubble-txt">{msg["content"]}</div>'
                    f'</div></div>'
                )

    st.markdown(f'<div class="chat-window">{bubbles_html}</div>', unsafe_allow_html=True)

    # Input
    user_input = st.chat_input("Ask about your product in any language…")
    if user_input:
        st.session_state.chat_history.append({"role":"user","content":user_input})
        with st.spinner(""):
            msgs=[{"role":"system","content":SYSTEM}]+st.session_state.chat_history
            resp=client.chat.completions.create(model="llama-3.3-70b-versatile",messages=msgs,max_tokens=300,temperature=0.75)
            st.session_state.chat_history.append({"role":"assistant","content":resp.choices[0].message.content.strip()})
        st.rerun()

    # Controls
    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
    bc_col, cl_col, _ = st.columns([1.2,1.2,2.6])
    with bc_col:
        st.markdown('<div class="ghost-wrap">', unsafe_allow_html=True)
        if st.button("← Back to Insights", key="back_to_results", use_container_width=True):
            st.session_state.step=2; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    with cl_col:
        st.markdown('<div class="ghost-wrap">', unsafe_allow_html=True)
        if st.button("🗑  Clear Chat", key="clear_chat", use_container_width=True):
            st.session_state.chat_history=[]; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""<div style="text-align:center;padding:3rem 0 1rem;border-top:1px solid rgba(255,255,255,0.04);
              margin-top:3rem;font-family:'JetBrains Mono',monospace;font-size:11px;color:#1e2238;letter-spacing:0.5px;">
  Productly · Groq Vision · LLaMA 3.3 70B · Streamlit</div>""", unsafe_allow_html=True)
