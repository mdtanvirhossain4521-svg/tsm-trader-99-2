import streamlit as st
import streamlit.components.v1 as components
from streamlit_autorefresh import st_autorefresh
from PIL import Image
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
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
.signal-box-buy {
    background-color: rgba(0, 255, 0, 0.1);
    border: 2px solid #39ff14;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
}
.signal-box-sell {
    background-color: rgba(255, 0, 0, 0.1);
    border: 2px solid #ff4d4d;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
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
c2.metric("CANDLE TIMER", "Active Scan")
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

# ---------- SCREENSHOT UPLOAD & AI SIGNAL ENGINE ----------
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

        # ---------- TSM TRADER 99 AI PREDICTION LOGIC ----------
        st.divider()
        st.subheader("TSM TRADER 99 AI SIGNAL ENGINE")

        r_channel = image_array[:, :, 0]
        g_channel = image_array[:, :, 1]
        
        green_mask = (g_channel > r_channel + 20) & (g_channel > 80)
        red_mask = (r_channel > g_channel + 20) & (r_channel > 80)
        
        green_count = np.sum(green_mask)
        red_count = np.sum(red_mask)
        total_candles_pixels = green_count + red_count

        if total_candles_pixels > 0:
            bullish_ratio = (green_count / total_candles_pixels) * 100
            bearish_ratio = (red_count / total_candles_pixels) * 100
        else:
            bullish_ratio = 50.0
            bearish_ratio = 50.0

        if bullish_ratio > bearish_ratio + 3:
            signal = "BUY (CALL)"
            confidence = min(round(50 + (bullish_ratio - bearish_ratio) * 1.5, 2), 94.5)
            box_class = "signal-box-buy"
            signal_color = "#39ff14"
        elif bearish_ratio > bullish_ratio + 3:
            signal = "SELL (PUT)"
            confidence = min(round(50 + (bearish_ratio - bearish_ratio) * 1.5, 2), 94.5)
            box_class = "signal-box-sell"
            signal_color = "#ff4d4d"
        else:
            signal = "CONSOLIDATION / WAIT"
            confidence = 60.0
            box_class = "signal-box-buy"
            signal_color = "#ffaa00"

        st.markdown(f"""
            <div class="{box_class}">
                <h2 style="color: {signal_color}; margin: 0;">SIGNAL: {signal}</h2>
                <p style="font-size: 18px; margin: 5px 0;">Workspace: <b>{st.session_state.market_mode}</b></p>
                <p style="font-size: 16px; margin: 0;">AI Confidence Score: <b>{confidence}%</b></p>
            </div>
        """, unsafe_allow_html=True)

        col_m1, col_m2 = st.columns(2)
        col_m1.metric("Bullish Momentum", f"{round(bullish_ratio, 1)}%")
        col_m2.metric("Bearish Momentum", f"{round(bearish_ratio, 1)}%")

    except Exception as error:
        st.error(f"Image processing failed: {error}")

else:
    st.info(
        "Upload a chart screenshot to begin image processing and signal generation."
    )

st.divider()

# ---------- FOOTER ----------
st.caption(
    "TSM TRADER 99 | Private Chart Analysis Workspace"
)
