import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

import os

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

DATA_DIR = os.path.join(BASE_DIR, "Data")


# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(page_title="Stock Risk Analytics", layout="wide")

# -------------------------------------------------
# ADVANCED STYLING
# -------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700;800;900&display=swap');

html, body, [class*="css"] {
    background: #000000;
    color: #e8eaed;
    font-family: 'Inter', sans-serif;
}

.block-container {
    padding-top: 1rem;
    max-width: 100%;
}

/* HEADER STYLING */
.page-header {
    background: linear-gradient(135deg, #0a0e13 0%, #000000 100%);
    border: 1px solid rgba(255, 165, 0, 0.2);
    border-left: 4px solid #ffa500;
    border-radius: 12px;
    padding: 20px 28px;
    margin-bottom: 28px;
    box-shadow: 0 8px 32px rgba(255, 165, 0, 0.1);
}

.page-title {
    font-size: 28px;
    font-weight: 900;
    background: linear-gradient(135deg, #ffa500 0%, #ff8c00 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 6px;
}

.page-subtitle {
    font-size: 13px;
    color: #8b8d91;
    line-height: 1.5;
}

/* METRIC CARDS */
.metric-card-advanced {
    background: linear-gradient(145deg, #0d1117, #161b22);
    border: 1px solid rgba(255, 165, 0, 0.2);
    border-radius: 12px;
    padding: 18px;
    text-align: center;
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
}

.metric-card-advanced::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, transparent, #ffa500, transparent);
    opacity: 0;
    transition: opacity 0.3s ease;
}

.metric-card-advanced:hover {
    border-color: rgba(255, 165, 0, 0.5);
    transform: translateY(-4px);
    box-shadow: 0 12px 40px rgba(255, 165, 0, 0.2);
}

.metric-card-advanced:hover::before {
    opacity: 1;
}

.metric-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    color: #8b8d91;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    margin-bottom: 6px;
}

.metric-value-large {
    font-size: 32px;
    font-weight: 900;
    background: linear-gradient(135deg, #ffa500, #00ff88);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1;
}

.metric-delta {
    font-size: 12px;
    color: #8b8d91;
    margin-top: 4px;
}

/* SECTION HEADERS */
.section-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 28px 0 12px 0;
    padding: 14px 18px;
    background: linear-gradient(135deg, #0d1117, #161b22);
    border: 1px solid rgba(255, 165, 0, 0.25);
    border-left: 4px solid #ffa500;
    border-radius: 10px;
    box-shadow: 0 4px 16px rgba(255, 165, 0, 0.1);
}

.section-icon {
    font-size: 20px;
    flex-shrink: 0;
}

.section-title {
    font-size: 16px;
    font-weight: 700;
    color: #ffa500;
    letter-spacing: -0.2px;
    text-transform: uppercase;
    line-height: 1.2;
}

/* RISK POSITIONING BAR */
.risk-container {
    background: linear-gradient(145deg, #0d1117, #161b22);
    border: 1px solid rgba(255, 165, 0, 0.2);
    border-radius: 14px;
    padding: 24px;
    margin: 20px 0;
}

.risk-bar-container {
    position: relative;
    height: 40px;
    background: #0a0e13;
    border-radius: 20px;
    overflow: hidden;
    border: 1px solid rgba(255, 165, 0, 0.3);
}

.risk-bar-fill {
    height: 100%;
    background: linear-gradient(90deg, #00ff88, #ffa500, #ff4444);
    border-radius: 20px;
    display: flex;
    align-items: center;
    justify-content: flex-end;
    padding-right: 16px;
    font-weight: 700;
    font-size: 14px;
    color: #000;
}

.risk-labels {
    display: flex;
    justify-content: space-between;
    margin-top: 12px;
    font-size: 12px;
    color: #8b8d91;
}

/* CHART CONTAINER */
.chart-container {
    background: linear-gradient(145deg, #0d1117, #161b22);
    border: 1px solid rgba(255, 165, 0, 0.15);
    border-radius: 12px;
    padding: 20px;
    margin: 12px 0;
    box-shadow: 0 4px 24px rgba(0, 0, 0, 0.4);
}

/* CHART EXPLANATION */
.chart-explanation {
    background: rgba(255, 165, 0, 0.05);
    border-left: 3px solid #ffa500;
    padding: 10px 14px;
    margin-bottom: 16px;
    border-radius: 6px;
    font-size: 12px;
    color: #c9d1d9;
    line-height: 1.5;
}

.chart-explanation strong {
    color: #ffa500;
    font-size: 12px;
}

/* SIDEBAR STYLING */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a0e13 0%, #000000 100%);
    border-right: 1px solid rgba(255, 165, 0, 0.15);
}

.sidebar-section {
    background: linear-gradient(145deg, #0d1117, #0a0e13);
    border: 1px solid rgba(255, 165, 0, 0.2);
    border-radius: 12px;
    padding: 16px;
    margin: 16px 0;
}

/* DATAFRAME STYLING */
.dataframe-container {
    background: linear-gradient(145deg, #0d1117, #161b22);
    border: 1px solid rgba(255, 165, 0, 0.15);
    border-radius: 14px;
    padding: 16px;
    margin: 16px 0;
}

/* STATS GRID */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 16px;
    margin: 20px 0;
}

.stat-box {
    background: linear-gradient(145deg, #0d1117, #161b22);
    border: 1px solid rgba(255, 165, 0, 0.15);
    border-radius: 12px;
    padding: 16px;
    text-align: center;
}

.stat-box-label {
    font-size: 11px;
    color: #8b8d91;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 8px;
}

.stat-box-value {
    font-size: 24px;
    font-weight: 700;
    color: #ffa500;
}

/* SCROLLBAR */
::-webkit-scrollbar {
    width: 10px;
    height: 10px;
}

::-webkit-scrollbar-track {
    background: #0a0e13;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #ffa500, #ff8c00);
    border-radius: 5px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------
@st.cache_data
def load_stock_risk_data():
    return pd.read_csv(
        os.path.join(DATA_DIR, "stock_risk_summary.csv")
    )


df = load_stock_risk_data()

# -------------------------------------------------
# PAGE HEADER
# -------------------------------------------------
st.markdown("""
<div class="page-header">
    <div class="page-title">📈 STOCK-LEVEL RISK ANALYTICS</div>
    <div class="page-subtitle">
        Comprehensive risk profiling using historical returns and volatility metrics. 
        All calculations derived from daily log returns with 20-day rolling windows.
    </div>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# SIDEBAR CONTROLS
# -------------------------------------------------
st.sidebar.markdown("""
<div class="sidebar-section">
    <div style="font-size:14px; font-weight:700; color:#ffa500; margin-bottom:12px;">
        📊 RISK TERMINAL CONTROLS
    </div>
</div>
""", unsafe_allow_html=True)

selected_stock = st.sidebar.selectbox(
    label="🎯 Select Security",
    options=sorted(df["Stock"].unique()),
    label_visibility="visible"
)

st.sidebar.markdown("---")

view_mode = st.sidebar.radio(
    "📊 Analysis Mode",
    ["Single Stock Deep Dive", "Cross-Sectional Comparison", "Advanced Analytics"]
)

st.sidebar.markdown("---")

# Risk filter
risk_filter = st.sidebar.multiselect(
    "🎚️ Volatility Filter",
    ["Low Risk (0-25%)", "Medium Risk (25-75%)", "High Risk (75-100%)"],
    default=["Low Risk (0-25%)", "Medium Risk (25-75%)", "High Risk (75-100%)"]
)

# -------------------------------------------------
# FILTER DATA
# -------------------------------------------------
stock_row = df[df["Stock"] == selected_stock].iloc[0]
avg_return = stock_row["Avg_Daily_Return"]
volatility = stock_row["Avg_20D_Volatility"]

# Calculate percentile
percentile = (df["Avg_20D_Volatility"].rank(pct=True)[df["Stock"] == selected_stock].values[0])

# Risk rank
risk_rank = int(df["Avg_20D_Volatility"].rank(ascending=False)[df["Stock"] == selected_stock].values[0])

# -------------------------------------------------
# TOP METRICS ROW
# -------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card-advanced">
        <div class="metric-label">AVG DAILY RETURN</div>
        <div class="metric-value-large">{avg_return*100:.3f}%</div>
        <div class="metric-delta">Historical Mean</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card-advanced">
        <div class="metric-label">20D VOLATILITY</div>
        <div class="metric-value-large">{volatility*100:.3f}%</div>
        <div class="metric-delta">Rolling StdDev</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card-advanced">
        <div class="metric-label">VOLATILITY RANK</div>
        <div class="metric-value-large">{risk_rank}/{len(df)}</div>
        <div class="metric-delta">Descending Order</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    percentile_display = percentile * 100
    st.markdown(f"""
    <div class="metric-card-advanced">
        <div class="metric-label">RISK PERCENTILE</div>
        <div class="metric-value-large">{percentile_display:.1f}%</div>
        <div class="metric-delta">Universe Position</div>
    </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------
# SINGLE STOCK VIEW
# -------------------------------------------------
if view_mode == "Single Stock Deep Dive":
    
    # Risk Positioning
    st.markdown("""
    <div class="section-header">
        <div class="section-icon">🎯</div>
        <div class="section-title">RISK POSITIONING MATRIX</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="risk-container">
        <div class="risk-bar-container">
            <div class="risk-bar-fill" style="width: {percentile*100}%;">
                {percentile*100:.1f}%
            </div>
        </div>
        <div class="risk-labels">
            <span>LOW RISK</span>
            <span>MEDIUM RISK</span>
            <span>HIGH RISK</span>
        </div>
        <div style="margin-top:16px; color:#c9d1d9; text-align:center;">
            <b>{selected_stock}</b> is more volatile than <b style="color:#ffa500;">{percentile*100:.1f}%</b> of stocks in the S&P 100 universe
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Additional Stats Grid
    st.markdown("""
    <div class="section-header">
        <div class="section-icon">📊</div>
        <div class="section-title">RISK STATISTICS DASHBOARD</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Calculate additional metrics
    sharpe_proxy = avg_return / volatility if volatility != 0 else 0
    ann_return = avg_return * 252
    ann_vol = volatility * np.sqrt(252)
    
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-box-label">Sharpe Proxy</div>
            <div class="stat-box-value">{sharpe_proxy:.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with c2:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-box-label">Ann. Return</div>
            <div class="stat-box-value">{ann_return*100:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with c3:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-box-label">Ann. Volatility</div>
            <div class="stat-box-value">{ann_vol*100:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with c4:
        risk_category = "HIGH" if percentile > 0.75 else "MEDIUM" if percentile > 0.25 else "LOW"
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-box-label">Risk Category</div>
            <div class="stat-box-value">{risk_category}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Distribution Analysis
    st.markdown("""
    <div class="section-header">
        <div class="section-icon">📉</div>
        <div class="section-title">VOLATILITY DISTRIBUTION ANALYSIS</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="chart-explanation">
        <strong>📖 How to Read:</strong> This histogram shows how volatility is distributed across all stocks. 
        The red dashed line marks the selected stock's position. Stocks to the right are more volatile (riskier), 
        while stocks to the left are more stable. Most stocks cluster around 1.5-2.5% daily volatility.
    </div>
    """, unsafe_allow_html=True)
    
    hist_fig = go.Figure()
    
    hist_fig.add_trace(go.Histogram(
        x=df["Avg_20D_Volatility"]*100,
        nbinsx=40,
        name="Distribution",
        marker=dict(
            color=df["Avg_20D_Volatility"]*100,
            colorscale='Viridis',
            line=dict(color='#ffa500', width=1)
        ),
        opacity=0.8
    ))
    
    hist_fig.add_vline(
        x=volatility*100,
        line_width=3,
        line_dash="dash",
        line_color="#ff4444",
        annotation_text=f"{selected_stock}",
        annotation_position="top"
    )
    
    hist_fig.update_layout(
        template="plotly_dark",
        height=400,
        showlegend=False,
        xaxis_title="Volatility (%)",
        yaxis_title="Frequency",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter", size=12, color="#e8eaed")
    )
    
    st.plotly_chart(hist_fig, width="stretch")

# -------------------------------------------------
# CROSS-SECTIONAL VIEW
# -------------------------------------------------
elif view_mode == "Cross-Sectional Comparison":
    
    st.markdown("""
    <div class="section-header">
        <div class="section-icon">🌐</div>
        <div class="section-title">RISK-RETURN LANDSCAPE</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="chart-explanation">
        <strong>📖 How to Read:</strong> Each dot represents a stock plotted by its volatility (X-axis) vs return (Y-axis). 
        Top-right stocks = high risk, high return. Bottom-left = low risk, low return. The red star highlights your selected stock. 
        Ideal positions are top-left (high return, low risk), but these are rare. Color intensity shows volatility level.
    </div>
    """, unsafe_allow_html=True)
    
    # Create scatter plot
    fig = go.Figure()
    
    # Add all stocks
    fig.add_trace(go.Scatter(
        x=df["Avg_20D_Volatility"]*100,
        y=df["Avg_Daily_Return"]*100,
        mode='markers',
        name='Universe',
        marker=dict(
            size=10,
            color=df["Avg_20D_Volatility"]*100,
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="Volatility %"),
            line=dict(width=1, color='rgba(255,255,255,0.3)')
        ),
        text=df["Stock"],
        hovertemplate='<b>%{text}</b><br>Volatility: %{x:.2f}%<br>Return: %{y:.3f}%<extra></extra>'
    ))
    
    # Highlight selected stock
    fig.add_trace(go.Scatter(
        x=[volatility*100],
        y=[avg_return*100],
        mode='markers+text',
        name=selected_stock,
        marker=dict(size=20, color='#ff4444', symbol='star', line=dict(width=2, color='#ffa500')),
        text=[selected_stock],
        textposition="top center",
        textfont=dict(size=14, color='#ffa500', family='IBM Plex Mono'),
        hovertemplate='<b>%{text}</b><br>Volatility: %{x:.2f}%<br>Return: %{y:.3f}%<extra></extra>'
    ))
    
    fig.update_layout(
        template="plotly_dark",
        height=600,
        xaxis_title="Volatility (%)",
        yaxis_title="Avg Daily Return (%)",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter", size=12, color="#e8eaed"),
        hovermode='closest'
    )
    
    st.plotly_chart(fig, width="stretch")
    
    # Top/Bottom performers
    st.markdown("""
    <div class="section-header">
        <div class="section-icon">🏆</div>
        <div class="section-title">RISK EXTREMES</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🔴 Highest Volatility (Top 10)")
        top_10 = df.nlargest(10, "Avg_20D_Volatility")[["Stock", "Avg_20D_Volatility", "Avg_Daily_Return"]]
        top_10["Avg_20D_Volatility"] = (top_10["Avg_20D_Volatility"] * 100).round(3)
        top_10["Avg_Daily_Return"] = (top_10["Avg_Daily_Return"] * 100).round(3)
        st.dataframe(top_10, width="stretch", height=400)
    
    with col2:
        st.markdown("#### 🟢 Lowest Volatility (Bottom 10)")
        bottom_10 = df.nsmallest(10, "Avg_20D_Volatility")[["Stock", "Avg_20D_Volatility", "Avg_Daily_Return"]]
        bottom_10["Avg_20D_Volatility"] = (bottom_10["Avg_20D_Volatility"] * 100).round(3)
        bottom_10["Avg_Daily_Return"] = (bottom_10["Avg_Daily_Return"] * 100).round(3)
        st.dataframe(bottom_10, width="stretch", height=400)

# -------------------------------------------------
# ADVANCED ANALYTICS VIEW
# -------------------------------------------------
else:
    st.markdown("""
    <div class="section-header">
        <div class="section-icon">🔬</div>
        <div class="section-title">ADVANCED MULTI-DIMENSIONAL ANALYSIS</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="chart-explanation">
        <strong>📖 How to Read:</strong> Four synchronized views: <strong>(1) Top-left:</strong> Volatility distribution shows risk spread. 
        <strong>(2) Top-right:</strong> Return distribution shows performance spread. <strong>(3) Bottom-left:</strong> Risk-return scatter combines both metrics. 
        <strong>(4) Bottom-right:</strong> Top 10 most volatile stocks ranked. Together, these reveal market structure and risk patterns.
    </div>
    """, unsafe_allow_html=True)
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Volatility Distribution', 'Return Distribution', 
                       'Risk-Return Scatter', 'Correlation Heatmap Proxy'),
        specs=[[{"type": "histogram"}, {"type": "histogram"}],
               [{"type": "scatter"}, {"type": "bar"}]]
    )
    
    # Volatility histogram
    fig.add_trace(
        go.Histogram(x=df["Avg_20D_Volatility"]*100, name="Volatility", 
                    marker_color='#ffa500', nbinsx=30),
        row=1, col=1
    )
    
    # Return histogram
    fig.add_trace(
        go.Histogram(x=df["Avg_Daily_Return"]*100, name="Returns", 
                    marker_color='#00ff88', nbinsx=30),
        row=1, col=2
    )
    
    # Risk-return scatter
    fig.add_trace(
        go.Scatter(x=df["Avg_20D_Volatility"]*100, y=df["Avg_Daily_Return"]*100,
                  mode='markers', name='Stocks',
                  marker=dict(size=8, color=df["Avg_20D_Volatility"]*100, 
                            colorscale='Viridis', showscale=False)),
        row=2, col=1
    )
    
    # Top 10 volatility bar
    top_10_vol = df.nlargest(10, "Avg_20D_Volatility")
    fig.add_trace(
        go.Bar(x=top_10_vol["Stock"], y=top_10_vol["Avg_20D_Volatility"]*100,
              name="Top 10 Vol", marker_color='#ff4444'),
        row=2, col=2
    )
    
    fig.update_layout(
        height=800,
        showlegend=False,
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter", size=11, color="#e8eaed")
    )
    
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.plotly_chart(fig, width="stretch")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Statistical Summary
    st.markdown("""
    <div class="section-header">
        <div class="section-icon">📊</div>
        <div class="section-title">UNIVERSE STATISTICAL SUMMARY</div>
    </div>
    """, unsafe_allow_html=True)
    
    summary_stats = pd.DataFrame({
        'Metric': ['Mean', 'Median', 'Std Dev', 'Min', 'Max', 'Q1', 'Q3'],
        'Volatility (%)': [
            df["Avg_20D_Volatility"].mean()*100,
            df["Avg_20D_Volatility"].median()*100,
            df["Avg_20D_Volatility"].std()*100,
            df["Avg_20D_Volatility"].min()*100,
            df["Avg_20D_Volatility"].max()*100,
            df["Avg_20D_Volatility"].quantile(0.25)*100,
            df["Avg_20D_Volatility"].quantile(0.75)*100
        ],
        'Return (%)': [
            df["Avg_Daily_Return"].mean()*100,
            df["Avg_Daily_Return"].median()*100,
            df["Avg_Daily_Return"].std()*100,
            df["Avg_Daily_Return"].min()*100,
            df["Avg_Daily_Return"].max()*100,
            df["Avg_Daily_Return"].quantile(0.25)*100,
            df["Avg_Daily_Return"].quantile(0.75)*100
        ]
    })
    
    summary_stats['Volatility (%)'] = summary_stats['Volatility (%)'].round(3)
    summary_stats['Return (%)'] = summary_stats['Return (%)'].round(4)
    
    st.dataframe(summary_stats, width="stretch", height=300)

# -------------------------------------------------
# FULL RISK TABLE
# -------------------------------------------------
st.markdown("""
<div class="section-header">
    <div class="section-icon">📋</div>
    <div class="section-title">COMPLETE RISK UNIVERSE TABLE</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)

styled_df = df.sort_values("Avg_20D_Volatility", ascending=False).reset_index(drop=True)
styled_df["Avg_20D_Volatility"] = (styled_df["Avg_20D_Volatility"] * 100).round(3)
styled_df["Avg_Daily_Return"] = (styled_df["Avg_Daily_Return"] * 100).round(4)
styled_df.columns = ["Stock", "Volatility (%)", "Return (%)"]

st.dataframe(styled_df, width="stretch", height=420)
st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------
# FOOTER
# -------------------------------------------------
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#8b8d91; font-size:12px; padding:20px;">
    <b>Layer 1: Descriptive Risk Analytics</b><br>
    Returns & Volatility computed from historical daily log returns • Rolling 20-day windows
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
