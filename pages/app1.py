import streamlit as st
from groq import Groq
from PIL import Image
import io, base64, re

st.set_page_config(page_title="Productly AI", layout="wide", initial_sidebar_state="collapsed")

# ───────── OPERIX-STYLE CSS ─────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;700;800&display=swap');

/* ── Reset & Base ── */
html, body, [class*="css"] {
    font-family: 'Syne', sans-serif !important;
    background-color: #0a0a0f !important;
    color: #e8e8f0 !important;
}

.stApp {
    background: #0a0a0f !important;
    background-image:
        radial-gradient(ellipse 80% 50% at 20% 10%, rgba(0, 180, 255, 0.04) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 80%, rgba(0, 255, 140, 0.03) 0%, transparent 60%);
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden !important; }
.block-container { padding: 2rem 3rem 4rem !important; max-width: 1200px !important; }

/* ── TOP NAV BAR ── */
.nav-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem 0 2.5rem;
    border-bottom: 0.5px solid rgba(255,255,255,0.08);
    margin-bottom: 3rem;
}
.nav-logo {
    font-family: 'Space Mono', monospace;
    font-size: 13px;
    letter-spacing: 0.25em;
    color: rgba(255,255,255,0.4);
    text-transform: uppercase;
}
.nav-logo span { color: #00d4ff; }
.nav-badge {
    font-family: 'Space Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.2em;
    color: rgba(255,255,255,0.3);
    border: 0.5px solid rgba(255,255,255,0.1);
    padding: 4px 12px;
    border-radius: 20px;
}

/* ── HERO HEADLINE ── */
.hero-block { margin-bottom: 2.5rem; }
.hero-block h1 {
    font-size: clamp(2.2rem, 5vw, 3.6rem);
    font-weight: 800;
    line-height: 1.1;
    margin: 0 0 0.25rem;
    color: #fff;
    letter-spacing: -0.02em;
}
.hero-block h1 .c1 { color: #00d4ff; }
.hero-block h1 .c2 { color: #00ff8c; }
.hero-block h1 .c3 { color: #ff6b4a; }
.hero-sub {
    font-size: 0.95rem;
    line-height: 1.65;
    color: rgba(255,255,255,0.45);
    max-width: 560px;
    margin-top: 1rem;
}

/* ── FEATURE TAGS ── */
.tag-row { display: flex; flex-wrap: wrap; gap: 8px; margin: 1.5rem 0 2rem; }
.tag {
    font-family: 'Space Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.12em;
    color: rgba(255,255,255,0.5);
    border: 0.5px solid rgba(255,255,255,0.12);
    padding: 5px 14px;
    border-radius: 20px;
    background: rgba(255,255,255,0.03);
    text-transform: uppercase;
}

/* ── STEP INDICATOR ── */
.step-indicator {
    display: flex;
    gap: 8px;
    align-items: center;
    margin-bottom: 2.5rem;
}
.step-dot {
    font-family: 'Space Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.1em;
    padding: 4px 14px;
    border-radius: 20px;
    border: 0.5px solid rgba(255,255,255,0.1);
    color: rgba(255,255,255,0.25);
    background: transparent;
}
.step-dot.active {
    background: rgba(0, 212, 255, 0.08);
    border-color: rgba(0, 212, 255, 0.4);
    color: #00d4ff;
}
.step-dot.done {
    background: rgba(0, 255, 140, 0.06);
    border-color: rgba(0, 255, 140, 0.3);
    color: #00ff8c;
}

/* ── AGENT CARD (result block) ── */
.agent-card {
    display: flex;
    align-items: flex-start;
    gap: 1rem;
    background: rgba(255,255,255,0.03);
    border: 0.5px solid rgba(255,255,255,0.08);
    border-left: 3px solid #00d4ff;
    border-radius: 0 10px 10px 0;
    padding: 1.1rem 1.4rem;
    margin-bottom: 10px;
    transition: background 0.2s;
}
.agent-card:hover { background: rgba(255,255,255,0.05); }
.agent-icon {
    width: 40px; height: 40px;
    border-radius: 10px;
    background: rgba(0, 212, 255, 0.1);
    display: flex; align-items: center; justify-content: center;
    font-size: 18px;
    flex-shrink: 0;
}
.agent-info { flex: 1; }
.agent-name {
    font-size: 0.95rem;
    font-weight: 700;
    color: #fff;
    margin: 0 0 2px;
}
.agent-desc {
    font-size: 0.8rem;
    color: rgba(255,255,255,0.4);
    font-family: 'Space Mono', monospace;
    margin: 0;
}
.active-badge {
    font-family: 'Space Mono', monospace;
    font-size: 9px;
    letter-spacing: 0.15em;
    color: #00ff8c;
    border: 0.5px solid rgba(0, 255, 140, 0.35);
    background: rgba(0, 255, 140, 0.07);
    padding: 3px 10px;
    border-radius: 20px;
    align-self: center;
    white-space: nowrap;
}

/* ── RESULT BLOCK ── */
.result-panel {
    background: rgba(255,255,255,0.02);
    border: 0.5px solid rgba(255,255,255,0.08);
    border-left: 3px solid #ff6b4a;
    border-radius: 0 12px 12px 0;
    padding: 1.5rem 1.75rem;
    margin-top: 1.5rem;
    font-size: 0.9rem;
    line-height: 1.75;
    color: rgba(255,255,255,0.75);
}
.result-label {
    font-family: 'Space Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.2em;
    color: #ff6b4a;
    text-transform: uppercase;
    margin-bottom: 0.75rem;
}

/* ── CHAT BUBBLE ── */
.chat-user {
    background: rgba(0, 212, 255, 0.07);
    border: 0.5px solid rgba(0, 212, 255, 0.2);
    border-radius: 10px 10px 2px 10px;
    padding: 0.75rem 1rem;
    margin-bottom: 8px;
    font-size: 0.88rem;
    color: #e0f7ff;
}
.chat-assistant {
    background: rgba(255,255,255,0.03);
    border: 0.5px solid rgba(255,255,255,0.08);
    border-radius: 10px 10px 10px 2px;
    padding: 0.75rem 1rem;
    margin-bottom: 8px;
    font-size: 0.88rem;
    color: rgba(255,255,255,0.7);
}
.chat-label {
    font-family: 'Space Mono', monospace;
    font-size: 9px;
    letter-spacing: 0.15em;
    margin-bottom: 4px;
    text-transform: uppercase;
}
.chat-label.u { color: #00d4ff; }
.chat-label.a { color: rgba(255,255,255,0.3); }

/* ── STREAMLIT WIDGETS ── */
div[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.02) !important;
    border: 1px dashed rgba(0, 212, 255, 0.25) !important;
    border-radius: 12px !important;
    padding: 1.5rem !important;
}
div[data-testid="stFileUploader"] label {
    color: rgba(255,255,255,0.4) !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 12px !important;
    letter-spacing: 0.1em !important;
}

.stSelectbox label, .stTextInput label {
    font-family: 'Space Mono', monospace !important;
    font-size: 10px !important;
    letter-spacing: 0.2em !important;
    text-transform: uppercase !important;
    color: rgba(255,255,255,0.35) !important;
}
.stSelectbox > div > div, .stTextInput > div > div > input {
    background: rgba(255,255,255,0.04) !important;
    border: 0.5px solid rgba(255,255,255,0.1) !important;
    border-radius: 8px !important;
    color: #e8e8f0 !important;
    font-family: 'Syne', sans-serif !important;
}
.stSelectbox > div > div:hover, .stTextInput > div > div > input:focus {
    border-color: rgba(0, 212, 255, 0.4) !important;
}

.stButton > button {
    background: transparent !important;
    border: 0.5px solid rgba(0, 212, 255, 0.4) !important;
    color: #00d4ff !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: 0.2em !important;
    text-transform: uppercase !important;
    padding: 0.65rem 2rem !important;
    border-radius: 6px !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: rgba(0, 212, 255, 0.08) !important;
    border-color: rgba(0, 212, 255, 0.7) !important;
}

.stImage img {
    border-radius: 12px !important;
    border: 0.5px solid rgba(255,255,255,0.1) !important;
}

/* ── SPINNER ── */
.stSpinner > div { border-top-color: #00d4ff !important; }

/* ── DIVIDER ── */
hr { border-color: rgba(255,255,255,0.06) !important; }
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
    "chat_history": []
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
        img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        return img
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
            messages=[{
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}},
                    {"type": "text", "text": "Describe this product briefly."}
                ]
            }],
            max_tokens=150
        )
        return r.choices[0].message.content.strip()
    except:
        return "Vision unavailable."

def analyze_product(data):
    r = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{
            "role": "user",
            "content": f"""Product: {data}\nGive strengths, risks, pricing, improvements."""
        }],
        max_tokens=500
    )
    return r.choices[0].message.content

def parse_to_flashcards(text):
    """Parse markdown AI output into a list of {title, items, body} dicts."""
    cards = []
    current_title = None
    current_items = []
    current_body  = []

    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue

        # Section heading: ### Strengths  or  **Strengths**
        heading_match = re.match(r'^#{1,3}\s+(.+)', line) or re.match(r'^\*\*([^*]+)\*\*\s*$', line)
        if heading_match:
            if current_title:
                cards.append({"title": current_title, "items": current_items, "body": " ".join(current_body)})
            current_title = heading_match.group(1).strip(": ")
            current_items = []
            current_body  = []
            continue

        # Numbered / bullet item
        item_match = re.match(r'^[\d\-\*•]+[.\)]\s*(.+)', line) or re.match(r'^[-*•]\s+(.+)', line)
        if item_match and current_title:
            # clean inner **bold**
            clean = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', item_match.group(1))
            current_items.append(clean)
        elif current_title and line:
            clean = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', line)
            current_body.append(clean)

    if current_title:
        cards.append({"title": current_title, "items": current_items, "body": " ".join(current_body)})

    return cards

def render_flashcards(cards):
    """Render parsed cards as styled HTML flashcards."""
    CARD_META = {
        "strengths":    ("✦", "#00ff8c", "rgba(0,255,140,0.08)",  "rgba(0,255,140,0.25)"),
        "risks":        ("⚠", "#ff6b4a", "rgba(255,107,74,0.08)", "rgba(255,107,74,0.25)"),
        "pricing":      ("◈", "#00d4ff", "rgba(0,212,255,0.08)",  "rgba(0,212,255,0.25)"),
        "improvements": ("◎", "#c97aff", "rgba(201,122,255,0.08)","rgba(201,122,255,0.25)"),
        "default":      ("○", "#888",    "rgba(255,255,255,0.04)", "rgba(255,255,255,0.12)"),
    }

    html = '<div style="display:flex; flex-direction:column; gap:12px;">'

    for card in cards:
        key = card["title"].lower().split()[0] if card["title"] else "default"
        icon, accent, bg, border_color = CARD_META.get(key, CARD_META["default"])

        items_html = ""
        if card["items"]:
            items_html = "<ul style='margin:8px 0 0; padding-left:0; list-style:none;'>"
            for item in card["items"]:
                items_html += f"""
                <li style='display:flex; gap:8px; align-items:flex-start;
                            font-size:0.83rem; line-height:1.6;
                            color:rgba(255,255,255,0.65); margin-bottom:6px;'>
                    <span style='color:{accent}; margin-top:3px; flex-shrink:0;'>›</span>
                    <span>{item}</span>
                </li>"""
            items_html += "</ul>"
        elif card["body"]:
            items_html = f"<p style='font-size:0.83rem; line-height:1.65; color:rgba(255,255,255,0.6); margin:8px 0 0;'>{card['body']}</p>"

        html += f"""
        <div style="background:{bg}; border:0.5px solid {border_color};
                    border-left:3px solid {accent}; border-radius:0 10px 10px 0;
                    padding:1rem 1.25rem;">
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:2px;">
                <span style="color:{accent}; font-size:14px;">{icon}</span>
                <span style="font-family:'Space Mono',monospace; font-size:10px;
                             letter-spacing:0.18em; text-transform:uppercase;
                             color:{accent}; font-weight:700;">{card['title']}</span>
            </div>
            {items_html}
        </div>"""

    html += "</div>"
    return html

# ───────── NAV BAR (all steps) ─────────
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
    if i < st.session_state.step:
        cls = "done"
    elif i == st.session_state.step:
        cls = "active"
    else:
        cls = ""
    dots += f'<span class="step-dot {cls}">{label}</span>'
st.markdown(f'<div class="step-indicator">{dots}</div>', unsafe_allow_html=True)

# ───────── STEP 0 — UPLOAD ─────────
if st.session_state.step == 0:

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown("""
        <div class="hero-block">
            <h1>One Upload.<br>
            <span class="c1">Analyse.</span>
            <span class="c2"> Optimise.</span><br>
            <span class="c3">Decide.</span></h1>
            <p class="hero-sub">
                Drop a product image and let Productly's AI engine surface
                strengths, risks, pricing signals, and improvement vectors — in seconds.
            </p>
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
        # Agent preview cards
        agents = [
            ("🔍", "Vision Agent",      "Reads product image context",      "#00d4ff"),
            ("📊", "Analysis Agent",    "Surfaces strengths & risks",       "#00ff8c"),
            ("💡", "Strategy Agent",    "Pricing & improvement playbooks",  "#ff6b4a"),
            ("💬", "Chat Agent",        "Follow-up Q&A on any insight",     "#c97aff"),
        ]
        for icon, name, desc, color in agents:
            st.markdown(f"""
            <div class="agent-card" style="border-left-color: {color}">
                <div class="agent-icon" style="background: {color}18;">{icon}</div>
                <div class="agent-info">
                    <p class="agent-name">{name}</p>
                    <p class="agent-desc">{desc}</p>
                </div>
                <span class="active-badge">ACTIVE</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    f = st.file_uploader("Upload product image", type=["jpg", "jpeg", "png", "webp"])

    if f:
        if f.type not in ["image/jpeg", "image/png", "image/webp"]:
            st.error("Upload only image files")
            st.stop()

        file_bytes = f.read()
        img = load_safe_image(file_bytes)

        if img is None:
            st.error("Invalid image file")
            st.stop()

        st.session_state.uploaded_file_bytes = file_bytes
        st.session_state.uploaded_file_name  = f.name
        st.session_state.uploaded_file_size  = f.size
        st.session_state.step = 1
        st.rerun()

# ───────── STEP 1 — CONFIGURE ─────────
elif st.session_state.step == 1:

    img_bytes = st.session_state.uploaded_file_bytes
    img = load_safe_image(img_bytes)

    if img is None:
        st.error("Image corrupted. Re-upload.")
        st.session_state.step = 0
        st.stop()

    col1, col2 = st.columns([1, 1.4], gap="large")

    with col1:
        st.markdown("""
        <div style="margin-bottom: 1rem;">
            <p style="font-family:'Space Mono',monospace; font-size:10px;
               letter-spacing:0.2em; color:rgba(255,255,255,0.3); text-transform:uppercase;
               margin-bottom:0.5rem;">Product Preview</p>
        </div>
        """, unsafe_allow_html=True)
        st.image(img, use_container_width=True)

    with col2:
        st.markdown("""
        <div style="margin-bottom: 1.5rem;">
            <p style="font-size:1.5rem; font-weight:700; color:#fff; margin:0;">
                Configure Analysis
            </p>
            <p style="font-size:0.85rem; color:rgba(255,255,255,0.4); margin-top:6px;">
                Set the context — the AI agents will adapt their analysis accordingly.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.session_state.category   = st.selectbox("Category",  ["Footwear", "Apparel", "Electronics"])
        st.session_state.audience   = st.selectbox("Audience",  ["Gen Z", "Professionals", "Families"])
        st.session_state.price_range = st.selectbox("Price Tier", ["Budget", "Mid", "Premium"])

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("▶  Run Analysis"):
            with st.spinner("Agents running…"):
                st.session_state.image_desc = describe_image(img_bytes)
                st.session_state.result = analyze_product({
                    "category":   st.session_state.category,
                    "audience":   st.session_state.audience,
                    "price":      st.session_state.price_range,
                    "image_desc": st.session_state.image_desc,
                })
            st.session_state.step = 2
            st.rerun()

# ───────── STEP 2 — INSIGHTS ─────────
elif st.session_state.step == 2:

    col1, col2 = st.columns([1, 1.6], gap="large")

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
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <p style="font-size:1.4rem; font-weight:700; color:#fff; margin-bottom:0.25rem;">
            AI Insights
        </p>
        <p style="font-size:0.82rem; color:rgba(255,255,255,0.35); font-family:'Space Mono',monospace;
           letter-spacing:0.08em; margin-bottom:1.5rem;">
            ANALYSIS COMPLETE — 4 AGENTS
        </p>
        """, unsafe_allow_html=True)

        cards = parse_to_flashcards(st.session_state.result)
        if cards:
            st.markdown(render_flashcards(cards), unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="result-panel">
                <p class="result-label">○ Analysis Output</p>
                {st.session_state.result.replace(chr(10), '<br>')}
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("💬  Open Chat"):
            st.session_state.step = 3
            st.rerun()

# ───────── STEP 3 — CHAT ─────────
elif st.session_state.step == 3:

    st.markdown("""
    <p style="font-size:1.4rem; font-weight:700; color:#fff; margin-bottom:0.25rem;">
        Chat with AI
    </p>
    <p style="font-size:0.82rem; color:rgba(255,255,255,0.35); font-family:'Space Mono',monospace;
       letter-spacing:0.08em; margin-bottom:1.5rem;">
        ASK ANYTHING ABOUT YOUR PRODUCT
    </p>
    """, unsafe_allow_html=True)

    chat_col, _ = st.columns([2, 1])
    with chat_col:
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(f"""
                <div class="chat-user">
                    <div class="chat-label u">You</div>
                    {msg['content']}
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-assistant">
                    <div class="chat-label a">Productly AI</div>
                    {msg['content']}
                </div>""", unsafe_allow_html=True)

        user = st.text_input("Ask something about this product…", label_visibility="collapsed",
                             placeholder="Ask something about this product…")

        if user:
            st.session_state.chat_history.append({"role": "user", "content": user})
            with st.spinner("Thinking…"):
                r = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=st.session_state.chat_history,
                    max_tokens=200
                )
            reply = r.choices[0].message.content
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            st.rerun()
