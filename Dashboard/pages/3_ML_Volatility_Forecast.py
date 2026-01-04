# =========================================================
# ELITE WALL STREET RISK TERMINAL
# LAYER 2 – ML VOLATILITY FORECASTING ENGINE
# Institutional-Grade / Bloomberg-Inspired
# =========================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import os 

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

DATA_DIR = os.path.join(BASE_DIR, "Data")


# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="ML Volatility Forecast",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# GLOBAL THEME (Synchronized with Layer 1)
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@300;400;600;700&family=Inter:wght@300;400;600;700;800;900&display=swap');

html, body, [class*="css"] {
    background:#000000;
    color:#e8eaed;
    font-family:'Inter', sans-serif;
}

.block-container {
    padding-top:0.8rem;
    max-width:100%;
}

/* ================= TERMINAL HEADER ================= */
.terminal-header {
    background: linear-gradient(135deg, #0a0e13 0%, #000000 100%);
    border:1px solid rgba(255,165,0,0.35);
    border-left:6px solid #ffa500;
    border-radius:18px;
    padding:28px 36px;
    margin-bottom:28px;
    box-shadow:0 14px 48px rgba(255,165,0,0.25);
    position:relative;
    overflow:hidden;
}

.terminal-header::after {
    content:'';
    position:absolute;
    top:-40%;
    right:-20%;
    width:400px;
    height:400px;
    background:radial-gradient(circle, rgba(255,165,0,0.15), transparent 70%);
    pointer-events:none;
}

.terminal-title {
    font-size:36px;
    font-weight:900;
    letter-spacing:1.2px;
    background:linear-gradient(135deg, #ffa500, #ff8c00, #ffcc00);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}

.terminal-subtitle {
    font-size:13px;
    color:#8b8d91;
    margin-top:8px;
    line-height:1.8;
}

/* ================= STATUS BAR ================= */
.status-bar {
    margin-top:18px;
    display:flex;
    align-items:center;
    justify-content:space-between;
}

.status-left {
    font-family:'IBM Plex Mono', monospace;
    font-size:12px;
    color:#c9d1d9;
}

.status-dot {
    display:inline-block;
    width:8px;
    height:8px;
    background:#00ff88;
    border-radius:50%;
    margin-right:8px;
    box-shadow:0 0 8px rgba(0,255,136,0.9);
}

.status-pill {
    background:rgba(0,255,136,0.15);
    color:#00ff88;
    padding:6px 16px;
    border-radius:999px;
    font-size:12px;
    font-weight:700;
    letter-spacing:0.6px;
}

/* ================= SIDEBAR ================= */
section[data-testid="stSidebar"] {
    background:linear-gradient(180deg, #0a0e13 0%, #000000 100%);
    border-right:1px solid rgba(255,165,0,0.25);
}

.sidebar-box {
    background:linear-gradient(145deg, #0d1117, #0a0e13);
    border:1px solid rgba(255,165,0,0.3);
    border-radius:16px;
    padding:18px;
    margin:16px 0;
    box-shadow:0 6px 20px rgba(0,0,0,0.4);
}

.sidebar-title {
    font-size:13px;
    font-weight:800;
    color:#ffa500;
    letter-spacing:1px;
    margin-bottom:12px;
}

/* ================= METRIC CARD ================= */
.metric-card {
    background:linear-gradient(145deg, #0d1117, #161b22);
    border:1px solid rgba(255,165,0,0.35);
    border-radius:18px;
    padding:22px;
    position:relative;
    overflow:hidden;
    transition:all .35s ease;
}

.metric-card:hover {
    transform:translateY(-6px) scale(1.02);
    box-shadow:0 18px 60px rgba(255,165,0,0.3);
}

.metric-label {
    font-family:'IBM Plex Mono', monospace;
    font-size:11px;
    letter-spacing:1.4px;
    color:#8b8d91;
    margin-bottom:10px;
}

.metric-value {
    font-size:38px;
    font-weight:900;
    background:linear-gradient(135deg, #ffa500, #00ff88);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}

.metric-sub {
    font-size:11px;
    color:#8b8d91;
    margin-top:6px;
}

/* ================= SECTION HEADER ================= */
.section-header {
    margin:34px 0 18px;
    padding:16px 26px;
    background:linear-gradient(135deg, #0d1117, #161b22);
    border:1px solid rgba(255,165,0,0.35);
    border-left:6px solid #ffa500;
    border-radius:16px;
    box-shadow:0 6px 20px rgba(255,165,0,0.15);
}

.section-title {
    font-size:18px;
    font-weight:800;
    color:#ffa500;
    letter-spacing:1px;
    text-transform:uppercase;
}

/* ================= EXPLANATION ================= */
.explain-box {
    background:rgba(255,165,0,0.08);
    border-left:5px solid #ffa500;
    padding:16px 20px;
    border-radius:12px;
    font-size:12px;
    color:#c9d1d9;
    line-height:1.8;
    margin-bottom:20px;
}

/* ================= TABLE ================= */
.dataframe-box {
    background:linear-gradient(145deg, #0d1117, #161b22);
    border:1px solid rgba(255,165,0,0.25);
    border-radius:16px;
    padding:16px;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# DATA LOADING
# =========================================================
@st.cache_data
def load_ml_data():
    return pd.read_csv(
        os.path.join(DATA_DIR, "layer2_ml_results.csv")
    )


df = load_ml_data()

# =========================================================
# HEADER
# =========================================================
st.markdown("""
<div class="terminal-header">
    <div class="terminal-title">ML VOLATILITY FORECAST TERMINAL</div>
    <div class="terminal-subtitle">
        Layer 2 • Supervised ML volatility forecasts •
        5-Day forward risk • Model uncertainty • Accuracy diagnostics
    </div>
    <div class="status-bar">
        <div class="status-left">
            <span class="status-dot"></span>
            SYSTEM STATUS : OPERATIONAL
        </div>
        <div class="status-pill">LIVE ML SIGNALS</div>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================
st.sidebar.markdown("""
<div class="sidebar-box">
<div class="sidebar-title">ML ANALYTICS CONTROL</div>
<div style="font-size:11px; color:#8b8d91; line-height:1.6;">
Select forecasting lens & diagnostics to explore predictive risk regimes.
</div>
</div>
""", unsafe_allow_html=True)

selected_stock = st.sidebar.selectbox(
    "Stock Selection",
    sorted(df["Ticker"].unique())
)

view_mode = st.sidebar.radio(
    "Analysis Mode",
    [
        "Single Stock Forecast",
        "Cross-Stock Risk Map",
        "Model Accuracy Diagnostics",
        "Uncertainty Decomposition"
    ]
)

# =========================================================
# DATA SLICE
# =========================================================
row = df[df["Ticker"] == selected_stock].iloc[0]

pred_vol = row["Predicted_5D_Vol"]
rmse = row["RMSE"]
latest_price = row["Latest_Price"]
lower_68 = row["Price_Lower_68"]
upper_68 = row["Price_Upper_68"]

# =========================================================
# TOP METRICS DASHBOARD
# =========================================================
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">PREDICTED 5D VOL</div>
        <div class="metric-value">{pred_vol*100:.2f}%</div>
        <div class="metric-sub">ML Forecast Output</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">MODEL RMSE</div>
        <div class="metric-value">{rmse:.4f}</div>
        <div class="metric-sub">Hist. Prediction Error</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">LATEST PRICE</div>
        <div class="metric-value">${latest_price:.2f}</div>
        <div class="metric-sub">Current Market Spot</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    band = (upper_68 - lower_68) / latest_price * 100
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">UNCERTAINTY BAND</div>
        <div class="metric-value">{band:.2f}%</div>
        <div class="metric-sub">68% Confidence Width</div>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# VIEW 1: SINGLE STOCK FORECAST
# =========================================================
if view_mode == "Single Stock Forecast":

    st.markdown("""
    <div class="section-header">
        <div class="section-title">PRICE FORECAST RANGE</div>
    </div>
    """, unsafe_allow_html=True)

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=[selected_stock],
        y=[upper_68 - lower_68],
        base=[lower_68],
        marker_color="#ffa500",
        opacity=0.6,
        name="68% Confidence Band"
    ))

    fig.add_trace(go.Scatter(
        x=[selected_stock],
        y=[latest_price],
        mode="markers",
        marker=dict(size=14, color="#ff4444", symbol="diamond"),
        name="Current Price"
    ))

    fig.update_layout(
        template="plotly_dark",
        height=420,
        yaxis_title="Price ($)",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(fig, width='stretch')

    st.markdown("""
    <div class="explain-box">
    ⭐ <b>How to Read:</b><br>
    The orange bar shows the expected price range over the next 5 trading days based on ML volatility forecasts.<br>
    The red diamond marks the current market price.<br><br>
    Wider bars imply higher uncertainty and elevated short-term risk regimes.
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# VIEW 2: CROSS-STOCK MAP
# =========================================================
elif view_mode == "Cross-Stock Risk Map":

    st.markdown("""
    <div class="section-header">
        <div class="section-title">CROSS-STOCK ML RISK LANDSCAPE</div>
    </div>
    """, unsafe_allow_html=True)

    df["Bubble"] = (df["Predicted_5D_Vol"] * 1000).clip(lower=8)

    fig = px.scatter(
        df,
        x="Predicted_5D_Vol",
        y="RMSE",
        size="Bubble",
        color="Predicted_5D_Vol",
        hover_name="Ticker",
        color_continuous_scale="Turbo",
        height=520,
        template="plotly_dark"
    )

    fig.add_trace(go.Scatter(
        x=[pred_vol],
        y=[rmse],
        mode="markers",
        marker=dict(size=18, color="#ffffff", line=dict(width=2, color="#ffa500")),
        name=selected_stock
    ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(fig, width='stretch')

    st.markdown("""
    <div class="explain-box">
    ⭐ <b>How to Read:</b><br>
    Right → higher expected volatility<br>
    Down → better model accuracy (lower historical error)<br><br>
    High-confidence risk plays cluster in the bottom-right region.
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# VIEW 3: MODEL ACCURACY
# =========================================================
elif view_mode == "Model Accuracy Diagnostics":

    st.markdown("""
    <div class="section-header">
        <div class="section-title">MODEL ACCURACY DISTRIBUTION</div>
    </div>
    """, unsafe_allow_html=True)

    fig = px.histogram(
        df,
        x="RMSE",
        nbins=40,
        color_discrete_sequence=["#ffa500"],
        template="plotly_dark",
        height=420
    )

    fig.add_vline(x=rmse, line_color="#ff4444", line_dash="dash", line_width=3)

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(fig, width='stretch')

    st.markdown("""
    <div class="explain-box">
    ⭐ <b>How to Read:</b><br>
    Distribution shows forecasting error (RMSE) across the entire universe.<br>
    The red dashed line marks the selected stock’s error position.<br><br>
    Lower RMSE indicates higher model reliability and tighter forecast confidence.
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# VIEW 4: UNCERTAINTY
# =========================================================
else:

    st.markdown("""
    <div class="section-header">
        <div class="section-title">UNCERTAINTY DECOMPOSITION</div>
    </div>
    """, unsafe_allow_html=True)

    df["Uncertainty_%"] = (
        (df["Price_Upper_68"] - df["Price_Lower_68"]) /
        df["Latest_Price"]
    ) * 100

    fig = px.bar(
        df.sort_values("Uncertainty_%", ascending=False).head(15),
        x="Ticker",
        y="Uncertainty_%",
        color="Uncertainty_%",
        color_continuous_scale="Viridis",
        template="plotly_dark",
        height=480
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(fig, width='stretch')

    st.markdown("""
    <div class="explain-box">
    ⭐ <b>How to Read:</b><br>
    Taller bars indicate stocks with the widest forecast price ranges.<br>
    These names carry the highest short-term prediction uncertainty in the current regime.
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# RANKING TABLE
# =========================================================
st.markdown("""
<div class="section-header">
    <div class="section-title">ML FORECAST RANKING TABLE</div>
</div>
""", unsafe_allow_html=True)

rank_df = df.sort_values("Predicted_5D_Vol", ascending=False)

st.markdown('<div class="dataframe-box">', unsafe_allow_html=True)

st.dataframe(
    rank_df,
    width='stretch',
    height=520
)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div class="explain-box">
⭐ <b>How to Read:</b><br>
Sort by predicted volatility to identify near-term risk leaders.<br>
Cross-reference RMSE to avoid unreliable ML signals in low-confidence names.
</div>
""", unsafe_allow_html=True)

# =========================================================
# FOOTER
# =========================================================
st.markdown("""
<hr style="border:none;height:1px;background:linear-gradient(to right,transparent,#ffa500,transparent);margin:40px 0;">
<div style="text-align:center;color:#8b8d91;font-size:12px;line-height:1.8;">
<b>ELITE PORTFOLIO RISK TERMINAL</b><br>
Layer 2 – Predictive ML Volatility Engine<br><br>
Supervised ML models • Feature-engineered returns & volatility •
Short-horizon (5-Day) forward risk estimation
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# SIDEBAR FOOTER
# -------------------------------------------------
st.sidebar.markdown("---")
st.sidebar.markdown("""
<div class="sidebar-section" style="text-align:center;">
    <div style="font-size:11px; color:#8b8d91; letter-spacing:1px; margin-bottom:8px;">DEVELOPED BY</div>
    <div style="font-size:16px; color:#ffa500; font-weight:700; margin-bottom:12px;">Saransh Nijhawan</div>
    <div style="font-size:13px;">
        <a href="https://www.linkedin.com/in/saransh-nijhawan8142" target="_blank" 
           style="color:#ffa500; text-decoration:none;">🔗 LinkedIn</a>
        &nbsp;•&nbsp;
        <a href="https://github.com/SaranshAI13" target="_blank" 
           style="color:#ffa500; text-decoration:none;">💻 GitHub</a>
        <br>
        <a href="mailto:saranshnijhawan2005@gmail.com" 
           style="color:#ffa500; text-decoration:none;">📧 Gmail</a>
    </div>
</div>
""", unsafe_allow_html=True)