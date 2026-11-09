import streamlit as st
import streamlit.components.v1 as components
from streamlit_autorefresh import st_autorefresh
from PIL import Image
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import cv2
import numpy as np
import hmac

st.set_page_config(
    page_title="TSM TRADER 99",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------- SECURITY ----------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown(
        "<h1 style='text-align:center;color:#39ff14'>"
        "TSM TRADER 99</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='text-align:center'>PRIVATE ACCESS</p>",
        unsafe_allow_html=True
    )

    try:
        password = st.secrets["APP_PASSWORD"]
    except Exception:
        st.error(
            "APP_PASSWORD is not configured. "
            "Set it in Streamlit Secrets."
        )
        st.stop()

    entered = st.text_input(
        "Enter Access Password",
        type="password"
    )

    if st.button("UNLOCK ANALYZER", use_container_width=True):
        if hmac.compare_digest(entered, password):
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Incorrect password")

    st.stop()

# ---------- AUTO REFRESH ----------
st_autorefresh(interval=1000, key="clock_refresh")

# ---------- CUSTOM STYLE ----------
st.markdown("""
<style>
.stApp {
    background: #070b09;
    color: white;
}
h1, h2, h3 {
    color: #39ff14 !important;
}
div.stButton > button {
    background: #102719;
    color: #39ff14;
    border: 1px solid #39ff14;
    border-radius: 12px;
    min-height: 48px;
    font-weight: bold;
}
div.stButton > button:hover {
    background: #174426;
    color: white;
    border-color: #39ff14;
}
[data-testid="stFileUploader"] {
    border: 1px dashed #39ff14;
    border-radius: 14px;
    padding: 15px;
}
</style>
""", unsafe_allow_html=True)

# ---------- LOGO ----------
try:
    logo = Image.open("tsm_logo.png")
    st.image(logo, width=180)
except Exception:
    st.warning("Logo file not found.")

st.markdown(
    "<h1 style='text-align:center'>TSM TRADER 99</h1>",
    unsafe_allow_html=True
)
st.caption("UNIVERSAL CHART IMAGE ANALYSIS WORKSPACE")

st.divider()

# ---------- CLOCKS ----------
utc_now = datetime.now(timezone.utc)
bd_now = utc_now.astimezone(ZoneInfo("Asia/Dhaka"))

c1, c2, c3 = st.columns(3)

c1.metric("QUOTEX UTC", utc_now.strftime("%H:%M:%S"))
c2.metric("CANDLE TIMER", "Awaiting recognition")
c3.metric("BANGLADESH", bd_now.strftime("%H:%M:%S"))

st.caption(
    "System UTC clock is displayed; it is not independently "
    "verified against Quotex server time."
)

st.divider()

# ---------- MARKET MODE ----------
st.subheader("SELECT MARKET MODE")

if "market_mode" not in st.session_state:
    st.session_state.market_mode = "OTC"

col1, col2 = st.columns(2)

with col1:
    if st.button("OTC MARKET", use_container_width=True):
        st.session_state.market_mode = "OTC"

with col2:
    if st.button("REAL MARKET", use_container_width=True):
        st.session_state.market_mode = "REAL"

st.success(
    f"Selected Workspace: {st.session_state.market_mode}"
)

st.divider()

# ---------- SCREENSHOT UPLOAD ----------
st.subheader("UPLOAD CHART SCREENSHOT")

uploaded = st.file_uploader(
    "Choose a chart screenshot",
    type=["png", "jpg", "jpeg", "webp"],
    help="Upload a readable chart screenshot."
)

if uploaded is not None:

    try:
        image = Image.open(uploaded).convert("RGB")
        image_array = np.array(image)

        st.image(
            image,
            caption="Uploaded Chart Screenshot",
            use_container_width=True
        )

        # OpenCV image processing
        gray = cv2.cvtColor(
            image_array,
            cv2.COLOR_RGB2GRAY
        )

        height, width = gray.shape

        edges = cv2.Canny(gray, 50, 150)

        edge_pixels = int(np.count_nonzero(edges))

        st.divider()
        st.subheader("IMAGE PROCESSING RESULTS")

        a, b, c = st.columns(3)

        a.metric("Image Width", f"{width}px")
        b.metric("Image Height", f"{height}px")
        c.metric("Edge Pixels", edge_pixels)

        st.success("Image loaded and OpenCV processing completed.")

        st.info(
            "This stage validates and processes the image only. "
            "It does not yet identify candles or generate predictions."
        )

    except Exception as error:
        st.error(f"Image processing failed: {error}")

else:
    st.info(
        "Upload a chart screenshot to begin image processing."
    )

st.divider()

# ---------- FOOTER ----------
st.caption(
    "TSM TRADER 99 | Private Chart Analysis Workspace"
)
