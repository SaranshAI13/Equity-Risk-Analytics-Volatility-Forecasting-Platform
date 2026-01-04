# =========================================================
# ELITE WALL STREET RISK TERMINAL
# LAYER 1 – PORTFOLIO RISK ANALYTICS
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
    page_title="Portfolio Risk Terminal",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# GLOBAL BLOOMBERG-STYLE THEME
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

.sidebar-note {
    font-size:11px;
    color:#8b8d91;
    line-height:1.6;
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

    stock_risk = pd.read_csv(
        os.path.join(DATA_DIR, "stock_risk_summary.csv")
    )

    return weights, corr, port_vol, stock_risk

weights_df, corr_df, port_vol_df, stock_risk_df = load_data()

# =========================================================
# TERMINAL HEADER
# =========================================================
st.markdown("""
<div class="terminal-header">
    <div class="terminal-title">PORTFOLIO RISK TERMINAL</div>
    <div class="terminal-subtitle">
        Layer 1 • Institutional portfolio risk aggregation •
        Diversification diagnostics • Correlation exposure •
        Volatility regime analysis
    </div>
    <div class="status-bar">
        <div class="status-left">
            <span class="status-dot"></span>
            SYSTEM STATUS : OPERATIONAL
        </div>
        <div class="status-pill">LIVE ANALYTICS</div>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR – CONTROL CENTER
# =========================================================
st.sidebar.markdown("""
<div class="sidebar-box">
    <div class="sidebar-title">PORTFOLIO CONTROL PANEL</div>
    <div class="sidebar-note">
        Select analytical dimension to explore portfolio-wide
        risk behavior under different lenses.
    </div>
</div>
""", unsafe_allow_html=True)

analysis_view = st.sidebar.radio(
    label="Portfolio Risk Dimension",
    options=[
        "Portfolio Overview",
        "Allocation Analysis",
        "Correlation Risk",
        "Volatility Trend",
        "Risk Contribution",
        "Stress Scenarios"
    ],
    label_visibility="collapsed"
)

st.sidebar.markdown("""
<div class="sidebar-box">
    <div class="sidebar-title">MODEL LAYER</div>
    <div class="sidebar-note">
        Layer 1 focuses on descriptive and aggregated
        portfolio risk derived from historical returns.
    </div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# PORTFOLIO-LEVEL AGGREGATED METRICS
# =========================================================

# Latest portfolio volatility
portfolio_vol_latest = port_vol_df["Portfolio_All_20d_Volatility"].iloc[-1]

# Weighted return & volatility
weighted_return = np.sum(
    weights_df["Avg_Daily_Return"] *
    (weights_df["Portfolio_Weight_Percent"] / 100)
)

weighted_vol = np.sum(
    weights_df["Avg_20D_Volatility"] *
    (weights_df["Portfolio_Weight_Percent"] / 100)
)

diversification_ratio = weighted_vol / portfolio_vol_latest

# =========================================================
# TOP METRIC DASHBOARD
# =========================================================
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">PORTFOLIO DAILY RETURN</div>
        <div class="metric-value">{weighted_return*100:.2f}%</div>
        <div class="metric-sub">Weighted average of constituents</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">PORTFOLIO VOLATILITY (20D)</div>
        <div class="metric-value">{portfolio_vol_latest*100:.2f}%</div>
        <div class="metric-sub">Correlation-adjusted risk</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">WEIGHTED AVG VOLATILITY</div>
        <div class="metric-value">{weighted_vol*100:.2f}%</div>
        <div class="metric-sub">No correlation assumption</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">DIVERSIFICATION RATIO</div>
        <div class="metric-value">{diversification_ratio:.2f}x</div>
        <div class="metric-sub">
            {'Healthy diversification' if diversification_ratio > 1 else 'Concentration risk'}
        </div>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# SECTION: PORTFOLIO OVERVIEW
# =========================================================
if analysis_view == "Portfolio Overview":

    st.markdown("""
    <div class="section-header">
        <div class="section-title">PORTFOLIO RISK COMPOSITION</div>
    </div>
    """, unsafe_allow_html=True)

    fig = px.bar(
        weights_df.sort_values("Portfolio_Weight_Percent", ascending=False),
        x="Stock",
        y="Portfolio_Weight_Percent",
        color="Avg_20D_Volatility",
        color_continuous_scale="Viridis",
        height=520
    )

    fig.update_layout(
        template="plotly_dark",
        xaxis_title="Stock",
        yaxis_title="Portfolio Weight (%)",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        coloraxis_colorbar=dict(title="Volatility")
    )

    st.plotly_chart(fig, width="stretch")

    st.markdown("""
    <div class="explain-box">
        ⭐ <b>How to Read This:</b><br>
        Each bar represents a stock's allocation in the portfolio.<br>
        • <b>Height</b> → portfolio weight contribution<br>
        • <b>Color intensity</b> → stock volatility<br><br>
        Large dark bars indicate positions that are both <b>heavy in weight</b>
        and <b>high in volatility</b> — these dominate portfolio risk.
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# SECTION: ALLOCATION ANALYSIS
# =========================================================
elif analysis_view == "Allocation Analysis":

    st.markdown("""
    <div class="section-header">
        <div class="section-title">RISK–RETURN ALLOCATION MAP</div>
    </div>
    """, unsafe_allow_html=True)

    fig = px.scatter(
        weights_df,
        x="Avg_20D_Volatility",
        y="Avg_Daily_Return",
        size="Portfolio_Weight_Percent",
        color="Portfolio_Weight_Percent",
        hover_name="Stock",
        color_continuous_scale="Turbo",
        size_max=60
    )

    fig.update_layout(
        template="plotly_dark",
        height=600,
        xaxis_title="Volatility",
        yaxis_title="Average Daily Return",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(fig, width="stretch")

    st.markdown("""
    <div class="explain-box">
        ⭐ <b>How to Read This:</b><br>
        • X-axis → risk (volatility)<br>
        • Y-axis → return<br>
        • Bubble size → portfolio weight<br><br>
        Ideal assets lie in the <b>upper-left</b> (high return, low risk).<br>
        Large bubbles on the <b>right side</b> signal potential
        risk concentration without proportional return.
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# SECTION: CORRELATION RISK
# =========================================================
elif analysis_view == "Correlation Risk":

    st.markdown("""
    <div class="section-header">
        <div class="section-title">SYSTEMIC CORRELATION RISK MATRIX</div>
    </div>
    """, unsafe_allow_html=True)

    fig = go.Figure(
        data=go.Heatmap(
            z=corr_df.values,
            x=corr_df.columns,
            y=corr_df.index,
            colorscale="RdBu",
            zmin=-1,
            zmax=1,
            colorbar=dict(title="Correlation")
        )
    )

    fig.update_layout(
        template="plotly_dark",
        height=720,
        paper_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(fig, width="stretch")

    st.markdown("""
    <div class="explain-box">
        ⭐ <b>How to Read This:</b><br>
        • Red → strong positive correlation<br>
        • Blue → negative correlation<br>
        • White → low / neutral relationship<br><br>
        Highly red clusters indicate <b>systemic risk</b> —
        during stress events, these stocks tend to move together,
        reducing diversification benefits.
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# SECTION: VOLATILITY TREND
# =========================================================
elif analysis_view == "Volatility Trend":

    st.markdown("""
    <div class="section-header">
        <div class="section-title">PORTFOLIO VOLATILITY REGIME</div>
    </div>
    """, unsafe_allow_html=True)

    fig = px.line(
        port_vol_df,
        x="Date",
        y="Portfolio_All_20d_Volatility"
    )

    fig.update_layout(
        template="plotly_dark",
        height=480,
        yaxis_tickformat=".2%",
        xaxis_title="Date",
        yaxis_title="Volatility",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(fig, width="stretch")

    st.markdown("""
    <div class="explain-box">
        ⭐ <b>How to Read This:</b><br>
        Rising volatility signals increasing uncertainty and risk.<br>
        Flat or declining regimes indicate stable market conditions.<br><br>
        Sharp spikes often coincide with <b>macro events</b> or
        <b>earnings shocks</b> across correlated assets.
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# SECTION: RISK CONTRIBUTION ANALYSIS
# =========================================================
elif analysis_view == "Risk Contribution":

    st.markdown("""
    <div class="section-header">
        <div class="section-title">MARGINAL & PERCENTAGE RISK CONTRIBUTION</div>
    </div>
    """, unsafe_allow_html=True)

    # --- Risk contribution math ---
    weights = weights_df["Portfolio_Weight_Percent"].values / 100
    vols = weights_df["Avg_20D_Volatility"].values
    corr = corr_df.values

    cov_matrix = corr * np.outer(vols, vols)
    portfolio_variance = weights @ cov_matrix @ weights
    portfolio_vol = np.sqrt(portfolio_variance)

    marginal_risk = (cov_matrix @ weights) / portfolio_vol
    risk_contribution = weights * marginal_risk
    risk_contribution_pct = (risk_contribution / risk_contribution.sum()) * 100

    rc_df = weights_df.copy()
    rc_df["Risk_Contribution_%"] = risk_contribution_pct
    rc_df = rc_df.sort_values("Risk_Contribution_%", ascending=False)

    # --- Bar Chart ---
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=rc_df["Stock"],
        y=rc_df["Risk_Contribution_%"],
        marker_color="#ff4444",
        name="Risk Contribution (%)"
    ))

    fig.add_trace(go.Scatter(
        x=rc_df["Stock"],
        y=rc_df["Portfolio_Weight_Percent"],
        mode="lines+markers",
        marker_color="#ffa500",
        name="Portfolio Weight (%)",
        yaxis="y2"
    ))

    fig.update_layout(
        template="plotly_dark",
        height=620,
        yaxis=dict(title="Risk Contribution (%)"),
        yaxis2=dict(
            title="Portfolio Weight (%)",
            overlaying="y",
            side="right"
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", y=1.1)
    )

    st.plotly_chart(fig, width="stretch")

    st.markdown("""
    <div class="explain-box">
        ⭐ <b>How to Read This:</b><br>
        • Red bars show how much each stock contributes to total portfolio risk.<br>
        • Orange line shows portfolio allocation weight.<br><br>
        If a stock's <b>risk contribution is much higher than its weight</b>,
        it is a hidden risk driver and may require rebalancing.
    </div>
    """, unsafe_allow_html=True)

    # --- Risk Contribution Table ---
    st.markdown('<div class="dataframe-box">', unsafe_allow_html=True)

    table = rc_df[[
        "Stock",
        "Portfolio_Weight_Percent",
        "Risk_Contribution_%",
        "Avg_20D_Volatility",
        "Avg_Daily_Return"
    ]].copy()

    table["Avg_20D_Volatility"] *= 100
    table["Avg_Daily_Return"] *= 100

    st.dataframe(
        table.rename(columns={
            "Portfolio_Weight_Percent": "Weight (%)",
            "Risk_Contribution_%": "Risk Contribution (%)",
            "Avg_20D_Volatility": "Volatility (%)",
            "Avg_Daily_Return": "Return (%)"
        }),
        width="stretch",
        height=420
    )

    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# SECTION: STRESS SCENARIO ANALYSIS
# =========================================================
elif analysis_view == "Stress Scenarios":

    st.markdown("""
    <div class="section-header">
        <div class="section-title">PORTFOLIO STRESS SCENARIO SIMULATION</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="explain-box">
        Simulates extreme market shocks applied uniformly to the portfolio.
        Used to understand downside exposure during crisis events.
    </div>
    """, unsafe_allow_html=True)

    scenarios = {
        "Mild Correction (-10%)": -0.10,
        "Market Selloff (-20%)": -0.20,
        "Financial Crisis (-30%)": -0.30,
        "Black Swan (-40%)": -0.40
    }

    base_value = 1_000_000
    stress_results = []

    for name, shock in scenarios.items():
        stressed_value = base_value * (1 + shock)
        stress_results.append({
            "Scenario": name,
            "Shock": f"{shock*100:.0f}%",
            "Portfolio Value ($)": stressed_value,
            "Loss ($)": base_value - stressed_value
        })

    stress_df = pd.DataFrame(stress_results)

    # --- Waterfall chart ---
    fig = go.Figure(go.Waterfall(
        x=stress_df["Scenario"],
        y=stress_df["Portfolio Value ($)"] - base_value,
        decreasing={"marker": {"color": "#ff4444"}},
        increasing={"marker": {"color": "#00ff88"}},
        connector={"line": {"color": "#ffa500"}}
    ))

    fig.update_layout(
        template="plotly_dark",
        height=520,
        title="Stress Impact on Portfolio Value",
        paper_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(fig, width="stretch")

    st.markdown("""
    <div class="explain-box">
        ⭐ <b>How to Read This:</b><br>
        Each bar represents portfolio value change under a stress scenario.<br>
        Larger drops indicate higher vulnerability to tail-risk events.<br><br>
        This helps define <b>capital buffers</b> and
        <b>maximum acceptable drawdowns</b>.
    </div>
    """, unsafe_allow_html=True)

    # --- Stress Table ---
    st.markdown('<div class="dataframe-box">', unsafe_allow_html=True)

    st.dataframe(
        stress_df.style.format({
            "Portfolio Value ($)": "${:,.0f}",
            "Loss ($)": "${:,.0f}"
        }),
        width="stretch",
        height=260
    )

    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# SECTION: CORRELATION DIAGNOSTICS SUMMARY
# =========================================================
elif analysis_view == "Correlation Diagnostics":

    st.markdown("""
    <div class="section-header">
        <div class="section-title">CORRELATION STRUCTURE DIAGNOSTICS</div>
    </div>
    """, unsafe_allow_html=True)

    avg_corr = corr_df.where(~np.eye(corr_df.shape[0], dtype=bool)).mean().mean()
    max_corr = corr_df.where(~np.eye(corr_df.shape[0], dtype=bool)).max().max()
    min_corr = corr_df.where(~np.eye(corr_df.shape[0], dtype=bool)).min().min()

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">AVERAGE CORRELATION</div>
            <div class="metric-value">{avg_corr:.2f}</div>
            <div class="metric-sub">System-wide dependency</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">MAX CORRELATION</div>
            <div class="metric-value">{max_corr:.2f}</div>
            <div class="metric-sub">Strongest pair linkage</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">MIN CORRELATION</div>
            <div class="metric-value">{min_corr:.2f}</div>
            <div class="metric-sub">Diversification anchor</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="explain-box">
        ⭐ <b>How to Read This:</b><br>
        • High average correlation → portfolio behaves like a single asset<br>
        • Extreme max correlation → contagion risk during stress<br>
        • Very low / negative correlations → diversification backbone<br><br>
        Healthy portfolios maintain <b>moderate average correlation</b>
        with limited extreme pair dependencies.
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# MASTER PORTFOLIO RISK TABLE
# =========================================================
st.markdown("""
<div class="section-header">
    <div class="section-title">MASTER PORTFOLIO RISK TABLE</div>
</div>
""", unsafe_allow_html=True)

master_df = weights_df.copy()

master_df["Weight (%)"] = master_df["Portfolio_Weight_Percent"]
master_df["Return (%)"] = master_df["Avg_Daily_Return"] * 100
master_df["Volatility (%)"] = master_df["Avg_20D_Volatility"] * 100

# recompute risk contribution for table safety
weights = master_df["Weight (%)"].values / 100
vols = master_df["Volatility (%)"].values / 100
cov = corr_df.values * np.outer(vols, vols)

port_var = weights @ cov @ weights
port_vol = np.sqrt(port_var)
marginal = (cov @ weights) / port_vol
master_df["Risk Contribution (%)"] = (weights * marginal) / np.sum(weights * marginal) * 100

display_master = master_df[[
    "Stock",
    "Weight (%)",
    "Return (%)",
    "Volatility (%)",
    "Risk Contribution (%)",
    "Risk_Adjusted_Score"
]].sort_values("Risk Contribution (%)", ascending=False)

st.markdown('<div class="dataframe-box">', unsafe_allow_html=True)

st.dataframe(
    display_master.style.format({
        "Weight (%)": "{:.2f}",
        "Return (%)": "{:.2f}",
        "Volatility (%)": "{:.2f}",
        "Risk Contribution (%)": "{:.2f}",
        "Risk_Adjusted_Score": "{:.2f}"
    }),
    width="stretch",
    height=520
)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div class="explain-box">
    ⭐ <b>How to Read This:</b><br>
    This is the <b>single source of truth</b> for portfolio risk.<br><br>
    • Sort by <b>Risk Contribution</b> to find dominant risk drivers<br>
    • Compare <b>Weight vs Risk Contribution</b> to detect imbalance<br>
    • Use <b>Risk-Adjusted Score</b> to evaluate efficiency of exposure
</div>
""", unsafe_allow_html=True)

# =========================================================
# FINAL DIAGNOSTIC SUMMARY
# =========================================================
st.markdown("""
<div class="section-header">
    <div class="section-title">LAYER 1 – DIAGNOSTIC SUMMARY</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="explain-box">
<b>What Layer 1 Covers:</b><br>
• Portfolio-level aggregation of stock risk<br>
• Correlation-adjusted volatility computation<br>
• Diversification diagnostics<br>
• Risk contribution decomposition<br>
• Stress scenario impact estimation<br><br>

<b>What Layer 1 Does NOT Do:</b><br>
• No forecasting<br>
• No ML prediction<br>
• No forward-looking regime classification<br><br>

This ensures a <b>clean separation</b> between descriptive risk
(Layer 1) and predictive analytics (Layer 2).
</div>
""", unsafe_allow_html=True)

# =========================================================
# FOOTER
# =========================================================
st.markdown("""
<hr style="border:none;height:1px;background:linear-gradient(to right,transparent,#ffa500,transparent);margin:40px 0;">
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center;color:#8b8d91;font-size:12px;line-height:1.8;">
<b>ELITE PORTFOLIO RISK TERMINAL</b><br>
Layer 1 – Descriptive & Aggregated Risk Analytics<br><br>

Methodology based on historical daily returns,
rolling volatility, correlation matrices,
and portfolio-weighted aggregation.<br><br>

Designed for institutional-style
risk interpretation & capital awareness.
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