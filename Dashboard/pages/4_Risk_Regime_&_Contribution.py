import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

DATA_DIR = os.path.join(BASE_DIR, "Data")


# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Risk Intelligence Terminal",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# GLOBAL BLOOMBERG-STYLE THEME (SYNCHRONIZED)
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
}

/* ================= METRIC CARD ================= */
.metric-card {
    background:linear-gradient(145deg, #0d1117, #161b22);
    border:1px solid rgba(255,165,0,0.35);
    border-radius:18px;
    padding:22px;
    transition:all .35s ease;
}

.metric-label {
    font-family:'IBM Plex Mono', monospace;
    font-size:11px;
    letter-spacing:1.4px;
    color:#8b8d91;
    margin-bottom:10px;
}

.metric-value {
    font-size:32px;
    font-weight:900;
    background:linear-gradient(135deg, #ffa500, #00ff88);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}

/* ================= SECTION HEADER ================= */
.section-header {
    margin:34px 0 18px;
    padding:16px 26px;
    background:linear-gradient(135deg, #0d1117, #161b22);
    border:1px solid rgba(255,165,0,0.35);
    border-left:6px solid #ffa500;
    border-radius:16px;
}

.section-title {
    font-size:18px;
    font-weight:800;
    color:#ffa500;
    letter-spacing:1px;
    text-transform:uppercase;
}

.explain-box {
    background:rgba(255,165,0,0.08);
    border-left:5px solid #ffa500;
    padding:16px 20px;
    border-radius:12px;
    font-size:12px;
    color:#c9d1d9;
    line-height:1.8;
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
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# LOAD DATA
# ============================================================
@st.cache_data
def load_data():
    weights = pd.read_csv(
        os.path.join(DATA_DIR, "portfolio_weights_percentage.csv")
    )

    corr = pd.read_csv(
        os.path.join(DATA_DIR, "stock_return_correlation_matrix.csv"),
        index_col=0
    )

    port_vol = pd.read_csv(
        os.path.join(DATA_DIR, "portfolio_volatility_all_stocks.csv")
    )

    port_vol["Date"] = pd.to_datetime(port_vol["Date"])

    return weights, corr, port_vol


weights_df, corr_df, port_vol_df = load_data()

# =========================================================
# TERMINAL HEADER
# =========================================================
st.markdown("""
<div class="terminal-header">
    <div class="terminal-title">RISK INTELLIGENCE TERMINAL</div>
    <div class="terminal-subtitle">
        Decision-layer analytics • Regime Detection • Risk Attribution • Institutional-grade Diagnostics
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR
# ============================================================
st.sidebar.markdown("""
<div class="sidebar-box">
<div style="color:#ffa500; font-weight:800; font-size:14px; letter-spacing:1px;">CONTROL PANEL</div>
</div>
""", unsafe_allow_html=True)

mode = st.sidebar.radio(
    "Select Analysis Dimension",
    ["Market Risk Regime Detection", "Portfolio Risk Contribution"],
    label_visibility="collapsed"
)

st.sidebar.markdown("""
<div class="sidebar-box">
<div style="font-size:11px; color:#8b8d91;">
LAYER 3: ADAPTIVE RISK<br>
Used to identify WHEN market risk shifts and WHO drives volatility.
</div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# PART 1: RISK REGIME DETECTION
# ============================================================
if mode == "Market Risk Regime Detection":

    # --- Calculations ---
    vol_series = port_vol_df.copy()
    vol_values = vol_series["Portfolio_All_20d_Volatility"]
    low_q = vol_values.quantile(0.33)
    high_q = vol_values.quantile(0.66)

    def classify_regime(v):
        if v <= low_q: return "Low Risk"
        elif v <= high_q: return "Medium Risk"
        else: return "High Risk"

    vol_series["Risk_Regime"] = vol_values.apply(classify_regime)
    current = vol_series.iloc[-1]

    # --- Metrics ---
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown(f"""<div class="metric-card"><div class="metric-label">PORTFOLIO VOLATILITY</div>
        <div class="metric-value">{current['Portfolio_All_20d_Volatility']*100:.2f}%</div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="metric-card"><div class="metric-label">CURRENT REGIME</div>
        <div class="metric-value">{current['Risk_Regime']}</div></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="metric-card"><div class="metric-label">AS OF DATE</div>
        <div class="metric-value" style="font-size:24px; padding-top:10px;">{current['Date'].strftime('%Y-%m-%d')}</div></div>""", unsafe_allow_html=True)

    # --- Timeline ---
    st.markdown('<div class="section-header"><div class="section-title">Volatility Regime Timeline</div></div>', unsafe_allow_html=True)
    
    line_fig = px.line(
        vol_series, x="Date", y="Portfolio_All_20d_Volatility",
        template="plotly_dark", color_discrete_sequence=["#ffa500"]
    )
    line_fig.add_hline(y=low_q, line_dash="dash", line_color="#00ff88", annotation_text="Low Threshold")
    line_fig.add_hline(y=high_q, line_dash="dash", line_color="#ff4444", annotation_text="High Threshold")
    line_fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=500)
    st.plotly_chart(line_fig, width='stretch')

    # --- Distribution ---
    st.markdown('<div class="section-header"><div class="section-title">Historical Regime Distribution</div></div>', unsafe_allow_html=True)
    regime_dist = vol_series.groupby("Risk_Regime").size().reset_index(name="Count")
    
    pie_fig = px.pie(
        regime_dist, names="Risk_Regime", values="Count",
        color="Risk_Regime",
        color_discrete_map={"Low Risk": "#00FF9C", "Medium Risk": "#FFD166", "High Risk": "#EF476F"},
        template="plotly_dark", hole=0.4
    )
    pie_fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(pie_fig, width='stretch')

    st.markdown("""<div class="explain-box">⭐ <b>Analyst Note:</b> Risk regimes are adaptive. Thresholds shift based on historical volatility quantiles rather than fixed numbers.</div>""", unsafe_allow_html=True)

# ============================================================
# PART 2: RISK CONTRIBUTION BREAKDOWN
# ============================================================
else:
    # --- Math Prep ---
    df = weights_df.copy()
    df["Weight"] = df["Portfolio_Weight_Percent"] / 100
    vols = df.set_index("Stock")["Avg_20D_Volatility"]
    corr = corr_df.loc[vols.index, vols.index]
    cov_matrix = np.outer(vols, vols) * corr.values
    weights = df.set_index("Stock")["Weight"].values
    
    portfolio_vol = np.sqrt(weights.T @ cov_matrix @ weights)
    marginal_contrib = (cov_matrix @ weights) / portfolio_vol
    total_contrib = weights * marginal_contrib

    contrib_df = pd.DataFrame({
        "Stock": vols.index,
        "Weight (%)": weights * 100,
        "Volatility": vols.values,
        "Risk Contribution %": total_contrib / total_contrib.sum() * 100
    }).sort_values("Risk Contribution %", ascending=False)

    # --- Metrics ---
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""<div class="metric-card"><div class="metric-label">PORTFOLIO VOLATILITY</div>
        <div class="metric-value">{portfolio_vol*100:.2f}%</div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="metric-card"><div class="metric-label">TOP RISK DRIVER</div>
        <div class="metric-value" style="font-size:24px; padding-top:10px;">{contrib_df.iloc[0]['Stock']}</div></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="metric-card"><div class="metric-label">CONCENTRATION</div>
        <div class="metric-value">{contrib_df.iloc[0]['Risk Contribution %']:.2f}%</div></div>""", unsafe_allow_html=True)

    # --- Bar Chart ---
    st.markdown('<div class="section-header"><div class="section-title">Top 15 Risk Contributors</div></div>', unsafe_allow_html=True)
    bar_fig = px.bar(
        contrib_df.head(15), x="Risk Contribution %", y="Stock",
        orientation="h", color="Risk Contribution %",
        color_continuous_scale="Oranges", template="plotly_dark"
    )
    bar_fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", yaxis=dict(autorange="reversed"))
    st.plotly_chart(bar_fig, width='stretch')

    # --- Table ---
    st.markdown('<div class="section-header"><div class="section-title">Full Attribution Table</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="dataframe-box">', unsafe_allow_html=True)
    st.dataframe(contrib_df.style.format({"Weight (%)": "{:.2f}", "Volatility": "{:.4f}", "Risk Contribution %": "{:.2f}"}), width='stretch')
    st.markdown('</div>', unsafe_allow_html=True)

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