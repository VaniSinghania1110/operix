import streamlit as st
from groq import Groq
from PIL import Image
import io, base64, re

st.set_page_config(page_title="Productly AI", layout="wide")

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

# ───────── SAFE IMAGE LOADER ─────────
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

# ───────── IMAGE DESCRIPTION ─────────
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
                    {"type": "image_url",
                     "image_url": {"url": f"data:image/jpeg;base64,{b64}"}},
                    {"type": "text",
                     "text": "Describe this product briefly."}
                ]
            }],
            max_tokens=150
        )
        return r.choices[0].message.content.strip()
    except:
        return "Vision unavailable."

# ───────── PRODUCT ANALYSIS ─────────
def analyze_product(data):
    r = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{
            "role": "user",
            "content": f"""
Product: {data}
Give strengths, risks, pricing, improvements.
"""
        }],
        max_tokens=500
    )
    return r.choices[0].message.content

# ───────── STEP 0 ─────────
if st.session_state.step == 0:

    st.title("🚀 Productly AI")

    f = st.file_uploader(
        "Upload product image",
        type=["jpg", "jpeg", "png", "webp"]
    )

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
        st.session_state.uploaded_file_name = f.name
        st.session_state.uploaded_file_size = f.size
        st.session_state.step = 1
        st.rerun()

# ───────── STEP 1 ─────────
elif st.session_state.step == 1:

    img_bytes = st.session_state.uploaded_file_bytes
    img = load_safe_image(img_bytes)

    if img is None:
        st.error("Image corrupted. Re-upload.")
        st.session_state.step = 0
        st.stop()

    st.image(img, width=300)

    st.session_state.category = st.selectbox(
        "Category",
        ["Footwear", "Apparel", "Electronics"]
    )

    st.session_state.audience = st.selectbox(
        "Audience",
        ["Gen Z", "Professionals", "Families"]
    )

    st.session_state.price_range = st.selectbox(
        "Price",
        ["Budget", "Mid", "Premium"]
    )

    if st.button("Analyze"):
        st.session_state.image_desc = describe_image(img_bytes)
        st.session_state.result = analyze_product({
            "category": st.session_state.category,
            "audience": st.session_state.audience,
            "price": st.session_state.price_range,
            "image_desc": st.session_state.image_desc
        })
        st.session_state.step = 2
        st.rerun()

# ───────── STEP 2 ─────────
elif st.session_state.step == 2:

    img = load_safe_image(st.session_state.uploaded_file_bytes)

    if img:
        st.image(img, width=250)

    st.subheader("AI Insights")
    st.write(st.session_state.result)

    if st.button("Chat"):
        st.session_state.step = 3
        st.rerun()

# ───────── STEP 3 ─────────
elif st.session_state.step == 3:

    st.subheader("💬 Chat with AI")

    for msg in st.session_state.chat_history:
        st.write(f"**{msg['role']}**: {msg['content']}")

    user = st.text_input("Ask something")

    if user:
        st.session_state.chat_history.append({"role": "user", "content": user})

        r = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=st.session_state.chat_history,
            max_tokens=200
        )

        reply = r.choices[0].message.content
        st.session_state.chat_history.append(
            {"role": "assistant", "content": reply}
        )

        st.rerun()
