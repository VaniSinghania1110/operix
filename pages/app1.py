import streamlit as st
from groq import Groq
from PIL import Image
import io, base64, re

st.set_page_config(page_title="Productly AI", layout="wide", initial_sidebar_state="collapsed")

# ───────── CSS ─────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif !important;
    background-color: #0a0a0f !important;
    color: #e8e8f0 !important;
}
.stApp {
    background: #0a0a0f !important;
    background-image:
        radial-gradient(ellipse 80% 50% at 20% 10%, rgba(0,180,255,0.04) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 80%, rgba(0,255,140,0.03) 0%, transparent 60%);
}
#MainMenu, footer, header { visibility: hidden !important; }
.block-container { padding: 2rem 3rem 4rem !important; max-width: 1200px !important; }

/* NAV */
.nav-bar {
    display:flex; align-items:center; justify-content:space-between;
    padding:1rem 0 2.5rem;
    border-bottom:0.5px solid rgba(255,255,255,0.08);
    margin-bottom:3rem;
}
.nav-logo { font-family:'Space Mono',monospace; font-size:13px; letter-spacing:0.25em; color:rgba(255,255,255,0.4); text-transform:uppercase; }
.nav-logo span { color:#00d4ff; }
.nav-badge { font-family:'Space Mono',monospace; font-size:10px; letter-spacing:0.2em; color:rgba(255,255,255,0.3); border:0.5px solid rgba(255,255,255,0.1); padding:4px 12px; border-radius:20px; }

/* STEPS */
.step-indicator { display:flex; gap:8px; align-items:center; margin-bottom:2.5rem; }
.step-dot { font-family:'Space Mono',monospace; font-size:10px; letter-spacing:0.1em; padding:4px 14px; border-radius:20px; border:0.5px solid rgba(255,255,255,0.1); color:rgba(255,255,255,0.25); background:transparent; }
.step-dot.active { background:rgba(0,212,255,0.08); border-color:rgba(0,212,255,0.4); color:#00d4ff; }
.step-dot.done   { background:rgba(0,255,140,0.06); border-color:rgba(0,255,140,0.3); color:#00ff8c; }

/* HERO */
.hero-block h1 { font-size:clamp(2.2rem,5vw,3.6rem); font-weight:800; line-height:1.1; margin:0 0 0.25rem; color:#fff; letter-spacing:-0.02em; }
.c1{color:#00d4ff;} .c2{color:#00ff8c;} .c3{color:#ff6b4a;}
.hero-sub { font-size:0.95rem; line-height:1.65; color:rgba(255,255,255,0.45); max-width:560px; margin-top:1rem; }

/* TAGS */
.tag-row { display:flex; flex-wrap:wrap; gap:8px; margin:1.5rem 0 2rem; }
.tag { font-family:'Space Mono',monospace; font-size:10px; letter-spacing:0.12em; color:rgba(255,255,255,0.5); border:0.5px solid rgba(255,255,255,0.12); padding:5px 14px; border-radius:20px; background:rgba(255,255,255,0.03); text-transform:uppercase; }

/* AGENT CARDS */
.agent-card { display:flex; align-items:flex-start; gap:1rem; background:rgba(255,255,255,0.03); border:0.5px solid rgba(255,255,255,0.08); border-left:3px solid #00d4ff; border-radius:0 10px 10px 0; padding:1.1rem 1.4rem; margin-bottom:10px; }
.agent-card:hover { background:rgba(255,255,255,0.05); }
.agent-icon { width:40px; height:40px; border-radius:10px; background:rgba(0,212,255,0.1); display:flex; align-items:center; justify-content:center; font-size:18px; flex-shrink:0; }
.agent-info { flex:1; }
.agent-name { font-size:0.95rem; font-weight:700; color:#fff; margin:0 0 2px; }
.agent-desc { font-size:0.8rem; color:rgba(255,255,255,0.4); font-family:'Space Mono',monospace; margin:0; }
.active-badge { font-family:'Space Mono',monospace; font-size:9px; letter-spacing:0.15em; color:#00ff8c; border:0.5px solid rgba(0,255,140,0.35); background:rgba(0,255,140,0.07); padding:3px 10px; border-radius:20px; align-self:center; white-space:nowrap; }

/* FLASHCARD GRID */
.fc-grid { display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-top:4px; }
.fc-card {
    background:rgba(255,255,255,0.03);
    border:0.5px solid rgba(255,255,255,0.1);
    border-radius:12px;
    padding:1.1rem 1.25rem;
    position:relative;
    overflow:hidden;
}
.fc-card::before {
    content:'';
    position:absolute; top:0; left:0; right:0; height:3px;
    border-radius:12px 12px 0 0;
}
.fc-card.green  { border-color:rgba(0,255,140,0.18); }
.fc-card.green::before  { background:#00ff8c; }
.fc-card.red    { border-color:rgba(255,107,74,0.18); }
.fc-card.red::before    { background:#ff6b4a; }
.fc-card.blue   { border-color:rgba(0,212,255,0.18); }
.fc-card.blue::before   { background:#00d4ff; }
.fc-card.purple { border-color:rgba(201,122,255,0.18); }
.fc-card.purple::before { background:#c97aff; }

.fc-head { display:flex; align-items:center; gap:7px; margin-bottom:10px; }
.fc-icon { font-size:13px; }
.fc-title { font-family:'Space Mono',monospace; font-size:9px; letter-spacing:0.2em; text-transform:uppercase; font-weight:700; }
.fc-card.green  .fc-title, .fc-card.green  .fc-icon { color:#00ff8c; }
.fc-card.red    .fc-title, .fc-card.red    .fc-icon { color:#ff6b4a; }
.fc-card.blue   .fc-title, .fc-card.blue   .fc-icon { color:#00d4ff; }
.fc-card.purple .fc-title, .fc-card.purple .fc-icon { color:#c97aff; }

.fc-list { list-style:none; padding:0; margin:0; }
.fc-item { display:flex; gap:7px; align-items:flex-start; font-size:0.8rem; line-height:1.6; color:rgba(255,255,255,0.62); margin-bottom:7px; }
.fc-bullet { font-size:10px; margin-top:4px; flex-shrink:0; }
.fc-card.green  .fc-bullet { color:#00ff8c; }
.fc-card.red    .fc-bullet { color:#ff6b4a; }
.fc-card.blue   .fc-bullet { color:#00d4ff; }
.fc-card.purple .fc-bullet { color:#c97aff; }

/* CHAT — override Streamlit chat components */
[data-testid="stChatMessage"] {
    background:rgba(255,255,255,0.02) !important;
    border:0.5px solid rgba(255,255,255,0.07) !important;
    border-radius:10px !important;
    padding:0.75rem 1rem !important;
    margin-bottom:8px !important;
}
[data-testid="stChatMessageContent"] p {
    font-size:0.88rem !important;
    color:rgba(255,255,255,0.8) !important;
    line-height:1.65 !important;
}
[data-testid="stChatInput"] textarea {
    background:rgba(255,255,255,0.04) !important;
    border:0.5px solid rgba(255,255,255,0.12) !important;
    border-radius:10px !important;
    color:#e8e8f0 !important;
    font-family:'Syne',sans-serif !important;
    font-size:0.9rem !important;
}
[data-testid="stChatInput"] textarea:focus {
    border-color:rgba(0,212,255,0.4) !important;
}

/* WIDGETS */
div[data-testid="stFileUploader"] {
    background:rgba(255,255,255,0.02) !important;
    border:1px dashed rgba(0,212,255,0.25) !important;
    border-radius:12px !important;
    padding:1.5rem !important;
}
.stSelectbox label {
    font-family:'Space Mono',monospace !important;
    font-size:10px !important; letter-spacing:0.2em !important;
    text-transform:uppercase !important; color:rgba(255,255,255,0.35) !important;
}
.stSelectbox > div > div {
    background:rgba(255,255,255,0.04) !important;
    border:0.5px solid rgba(255,255,255,0.1) !important;
    border-radius:8px !important; color:#e8e8f0 !important;
}
.stSelectbox > div > div:hover { border-color:rgba(0,212,255,0.4) !important; }
.stButton > button {
    background:transparent !important;
    border:0.5px solid rgba(0,212,255,0.4) !important;
    color:#00d4ff !important;
    font-family:'Space Mono',monospace !important;
    font-size:11px !important; letter-spacing:0.2em !important;
    text-transform:uppercase !important;
    padding:0.65rem 2rem !important; border-radius:6px !important;
    transition:all 0.15s !important;
}
.stButton > button:hover {
    background:rgba(0,212,255,0.08) !important;
    border-color:rgba(0,212,255,0.7) !important;
}
/* Suggestion buttons smaller */
button[kind="secondary"] {
    padding:0.4rem 1rem !important;
    font-size:10px !important;
}
.stImage img { border-radius:12px !important; border:0.5px solid rgba(255,255,255,0.1) !important; }
.stSpinner > div { border-top-color:#00d4ff !important; }
hr { border-color:rgba(255,255,255,0.06) !important; }
</style>
""", unsafe_allow_html=True)

# ───────── STATE ─────────
for key, default in {
    "step": 0,
    "uploaded_file_bytes": None,
    "uploaded_file_name": None,
    "uploaded_file_size": None,
    "category": None,
    "audience": None,
    "price_range": None,
    "image_desc": "",
    "result": "",
    "chat_history": [],
    "pending_question": None,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ───────── API ─────────
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ───────── HELPERS ─────────
def load_safe_image(img_bytes):
    if not img_bytes:
        return None
    try:
        img = Image.open(io.BytesIO(img_bytes))
        img.verify()
        return Image.open(io.BytesIO(img_bytes)).convert("RGB")
    except Exception:
        return None

def describe_image(img_bytes):
    img = load_safe_image(img_bytes)
    if img is None:
        return "Invalid image."
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    b64 = base64.b64encode(buf.getvalue()).decode()
    try:
        r = client.chat.completions.create(
            model="llava-v1.5-7b-4096-preview",
            messages=[{"role":"user","content":[
                {"type":"image_url","image_url":{"url":f"data:image/jpeg;base64,{b64}"}},
                {"type":"text","text":"Describe this product briefly."}
            ]}],
            max_tokens=150
        )
        return r.choices[0].message.content.strip()
    except:
        return "Vision unavailable."

def analyze_product(data):
    r = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role":"user","content":f"""
You are a product analyst. Analyze this product and respond using EXACTLY these four section headers on their own lines (no other text before them):

### Strengths
### Risks
### Pricing
### Improvements

Under each header, provide exactly 3 numbered points. Format each point as:
1. **Title**: explanation sentence.

Product data: {data}
"""}],
        max_tokens=700
    )
    return r.choices[0].message.content

# ───────── FLASHCARD PARSER ─────────
def parse_flashcards(text):
    cards, current_title, current_items = [], None, []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        h = re.match(r'^#{1,3}\s+(.+)', line)
        if h:
            if current_title:
                cards.append({"title": current_title, "items": current_items})
            current_title = h.group(1).strip()
            current_items = []
            continue
        m = re.match(r'^\d+[.)]\s+(.+)', line) or re.match(r'^[-*]\s+(.+)', line)
        if m and current_title:
            clean = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', m.group(1))
            current_items.append(clean)
    if current_title:
        cards.append({"title": current_title, "items": current_items})
    return cards

def render_flashcards(cards):
    META = {
        "strengths":    ("green",  "✦"),
        "risks":        ("red",    "⚠"),
        "pricing":      ("blue",   "◈"),
        "improvements": ("purple", "◎"),
    }
    html = '<div class="fc-grid">'
    for card in cards:
        key = card["title"].lower().split()[0]
        cls, icon = META.get(key, ("blue", "○"))
        items_html = '<ul class="fc-list">'
        for item in card["items"]:
            items_html += f'<li class="fc-item"><span class="fc-bullet">›</span><span>{item}</span></li>'
        items_html += "</ul>"
        html += f"""
        <div class="fc-card {cls}">
            <div class="fc-head">
                <span class="fc-icon">{icon}</span>
                <span class="fc-title">{card["title"]}</span>
            </div>
            {items_html}
        </div>"""
    html += "</div>"
    return html

# ───────── CHAT REPLY ─────────
def get_chat_reply(user_msg):
    system = f"""You are Productly AI, a sharp product strategist. Keep answers concise (3-5 sentences max).
Product context:
- Category: {st.session_state.category}
- Audience: {st.session_state.audience}
- Price tier: {st.session_state.price_range}
- Image description: {st.session_state.image_desc}
- Full analysis: {st.session_state.result}

Answer specifically about this product. Be direct, insightful, and actionable."""
    messages = [{"role":"system","content":system}] + [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.chat_history
    ]
    r = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        max_tokens=300
    )
    return r.choices[0].message.content.strip()

# ───────── NAV ─────────
st.markdown("""
<div class="nav-bar">
    <div class="nav-logo">○ &nbsp;<span>Productly</span> AI</div>
    <div class="nav-badge">AI-POWERED PRODUCT ANALYSIS</div>
</div>
""", unsafe_allow_html=True)

# ───────── STEP INDICATOR ─────────
steps = ["Upload", "Configure", "Insights", "Chat"]
dots = ""
for i, label in enumerate(steps):
    cls = "done" if i < st.session_state.step else ("active" if i == st.session_state.step else "")
    dots += f'<span class="step-dot {cls}">{label}</span>'
st.markdown(f'<div class="step-indicator">{dots}</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════
# STEP 0 — UPLOAD
# ═══════════════════════════════════════════════
if st.session_state.step == 0:

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown("""
        <div class="hero-block">
            <h1>One Upload.<br>
            <span class="c1">Analyse.</span>
            <span class="c2"> Optimise.</span><br>
            <span class="c3">Decide.</span></h1>
            <p class="hero-sub">Drop a product image and let Productly's AI engine surface
            strengths, risks, pricing signals, and improvement vectors — in seconds.</p>
        </div>
        <div class="tag-row">
            <span class="tag">Vision Analysis</span>
            <span class="tag">Risk Detection</span>
            <span class="tag">Pricing Intel</span>
            <span class="tag">Audience Fit</span>
            <span class="tag">Improvement Plans</span>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        for icon, name, desc, color in [
            ("🔍", "Vision Agent",   "Reads product image context",     "#00d4ff"),
            ("📊", "Analysis Agent", "Surfaces strengths & risks",      "#00ff8c"),
            ("💡", "Strategy Agent", "Pricing & improvement playbooks", "#ff6b4a"),
            ("💬", "Chat Agent",     "Follow-up Q&A on any insight",    "#c97aff"),
        ]:
            st.markdown(f"""
            <div class="agent-card" style="border-left-color:{color}">
                <div class="agent-icon" style="background:{color}18;">{icon}</div>
                <div class="agent-info">
                    <p class="agent-name">{name}</p>
                    <p class="agent-desc">{desc}</p>
                </div>
                <span class="active-badge">ACTIVE</span>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    f = st.file_uploader("Upload product image", type=["jpg","jpeg","png","webp"])
    if f:
        if f.type not in ["image/jpeg","image/png","image/webp"]:
            st.error("Upload only image files"); st.stop()
        file_bytes = f.read()
        if load_safe_image(file_bytes) is None:
            st.error("Invalid image file"); st.stop()
        st.session_state.uploaded_file_bytes = file_bytes
        st.session_state.uploaded_file_name  = f.name
        st.session_state.uploaded_file_size  = f.size
        st.session_state.step = 1
        st.rerun()

# ═══════════════════════════════════════════════
# STEP 1 — CONFIGURE
# ═══════════════════════════════════════════════
elif st.session_state.step == 1:

    img = load_safe_image(st.session_state.uploaded_file_bytes)
    if img is None:
        st.error("Image corrupted. Re-upload.")
        st.session_state.step = 0; st.stop()

    col1, col2 = st.columns([1, 1.4], gap="large")
    with col1:
        st.markdown('<p style="font-family:\'Space Mono\',monospace;font-size:10px;letter-spacing:0.2em;color:rgba(255,255,255,0.3);text-transform:uppercase;margin-bottom:0.5rem;">Product Preview</p>', unsafe_allow_html=True)
        st.image(img, use_container_width=True)

    with col2:
        st.markdown("""
        <p style="font-size:1.5rem;font-weight:700;color:#fff;margin:0;">Configure Analysis</p>
        <p style="font-size:0.85rem;color:rgba(255,255,255,0.4);margin-top:6px;margin-bottom:1.5rem;">
            Set the context — agents will adapt their analysis accordingly.</p>
        """, unsafe_allow_html=True)

        st.session_state.category    = st.selectbox("Category",   ["Footwear","Apparel","Electronics"])
        st.session_state.audience    = st.selectbox("Audience",   ["Gen Z","Professionals","Families"])
        st.session_state.price_range = st.selectbox("Price Tier", ["Budget","Mid","Premium"])
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("▶  Run Analysis"):
            with st.spinner("Agents running…"):
                st.session_state.image_desc = describe_image(st.session_state.uploaded_file_bytes)
                st.session_state.result = analyze_product({
                    "category":   st.session_state.category,
                    "audience":   st.session_state.audience,
                    "price":      st.session_state.price_range,
                    "image_desc": st.session_state.image_desc,
                })
            st.session_state.step = 2
            st.rerun()

# ═══════════════════════════════════════════════
# STEP 2 — INSIGHTS (FLASHCARDS)
# ═══════════════════════════════════════════════
elif st.session_state.step == 2:

    col1, col2 = st.columns([1, 1.8], gap="large")

    with col1:
        img = load_safe_image(st.session_state.uploaded_file_bytes)
        if img:
            st.image(img, use_container_width=True)
        st.markdown(f"""
        <div style="margin-top:1rem;">
            <div class="agent-card" style="border-left-color:#00d4ff">
                <div class="agent-icon">📦</div>
                <div class="agent-info">
                    <p class="agent-name">{st.session_state.category}</p>
                    <p class="agent-desc">{st.session_state.audience} · {st.session_state.price_range}</p>
                </div>
                <span class="active-badge">DONE</span>
            </div>
        </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <p style="font-size:1.4rem;font-weight:700;color:#fff;margin-bottom:0.25rem;">AI Insights</p>
        <p style="font-size:0.82rem;color:rgba(255,255,255,0.35);font-family:'Space Mono',monospace;
           letter-spacing:0.08em;margin-bottom:1.25rem;">ANALYSIS COMPLETE — 4 AGENTS</p>
        """, unsafe_allow_html=True)

        cards = parse_flashcards(st.session_state.result)

        if cards:
            st.markdown(render_flashcards(cards), unsafe_allow_html=True)
        else:
            # Fallback with formatting
            cleaned = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', st.session_state.result)
            cleaned = cleaned.replace('\n', '<br>')
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.02);border:0.5px solid rgba(255,255,255,0.08);
                        border-left:3px solid #ff6b4a;border-radius:0 12px 12px 0;
                        padding:1.5rem 1.75rem;font-size:0.88rem;line-height:1.75;
                        color:rgba(255,255,255,0.72);">
                <p style="font-family:'Space Mono',monospace;font-size:10px;letter-spacing:0.2em;
                           color:#ff6b4a;text-transform:uppercase;margin-bottom:0.75rem;">○ Analysis Output</p>
                {cleaned}
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("💬  Chat with AI about this product"):
            st.session_state.chat_history = []
            st.session_state.step = 3
            st.rerun()

# ═══════════════════════════════════════════════
# STEP 3 — INTERACTIVE CHAT
# ═══════════════════════════════════════════════
elif st.session_state.step == 3:

    chat_col, side_col = st.columns([1.8, 1], gap="large")

    with side_col:
        img = load_safe_image(st.session_state.uploaded_file_bytes)
        if img:
            st.image(img, use_container_width=True)

        st.markdown(f"""
        <div style="margin-top:1rem;">
            <div class="agent-card" style="border-left-color:#c97aff">
                <div class="agent-icon" style="background:rgba(201,122,255,0.1);">💬</div>
                <div class="agent-info">
                    <p class="agent-name">Chat Agent</p>
                    <p class="agent-desc">{st.session_state.category} · {st.session_state.audience}</p>
                </div>
                <span class="active-badge">LIVE</span>
            </div>
        </div>
        <p style="font-family:'Space Mono',monospace;font-size:9px;letter-spacing:0.2em;
           color:rgba(255,255,255,0.3);text-transform:uppercase;margin:1.5rem 0 0.75rem;">
           Suggested questions</p>
        """, unsafe_allow_html=True)

        suggestions = [
            "What's the biggest risk?",
            "How should I price this?",
            "Who's the ideal buyer?",
            "Top 3 improvements?",
            "How to market to Gen Z?",
            "Compare vs competitors",
        ]
        for q in suggestions:
            if st.button(q, key=f"sq_{q}"):
                st.session_state.pending_question = q
                st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("← Back to Insights"):
            st.session_state.step = 2
            st.rerun()

    with chat_col:
        st.markdown("""
        <p style="font-size:1.4rem;font-weight:700;color:#fff;margin-bottom:0.25rem;">Chat with AI</p>
        <p style="font-family:'Space Mono',monospace;font-size:10px;letter-spacing:0.15em;
           color:rgba(255,255,255,0.3);text-transform:uppercase;margin-bottom:1.5rem;">
           ASK ANYTHING ABOUT YOUR PRODUCT</p>
        """, unsafe_allow_html=True)

        # Render chat history
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"], avatar="🧑" if msg["role"] == "user" else "🤖"):
                st.markdown(msg["content"])

        # Handle sidebar suggestion button clicks
        if st.session_state.pending_question:
            q = st.session_state.pending_question
            st.session_state.pending_question = None
            st.session_state.chat_history.append({"role":"user","content":q})
            with st.chat_message("user", avatar="🧑"):
                st.markdown(q)
            with st.chat_message("assistant", avatar="🤖"):
                with st.spinner(""):
                    reply = get_chat_reply(q)
                st.markdown(reply)
            st.session_state.chat_history.append({"role":"assistant","content":reply})
            st.rerun()

        # Native Streamlit chat input — sticks to bottom, clears after submit
        if prompt := st.chat_input("Ask something about this product…"):
            st.session_state.chat_history.append({"role":"user","content":prompt})
            with st.chat_message("user", avatar="🧑"):
                st.markdown(prompt)
            with st.chat_message("assistant", avatar="🤖"):
                with st.spinner(""):
                    reply = get_chat_reply(prompt)
                st.markdown(reply)
            st.session_state.chat_history.append({"role":"assistant","content":reply})
