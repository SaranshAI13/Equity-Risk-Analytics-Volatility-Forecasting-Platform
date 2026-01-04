import streamlit as st

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Equity Risk Analytics Terminal",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# STOCK UNIVERSE
# ============================================================
STOCKS = {
    "AAPL": "Apple Inc.", "ABBV": "AbbVie Inc.", "ACN": "Accenture plc",
    "ADBE": "Adobe Inc.", "ADI": "Analog Devices", "ADP": "Automatic Data Processing",
    "AMD": "Advanced Micro Devices", "AMGN": "Amgen Inc.", "AMT": "American Tower",
    "AMZN": "Amazon.com Inc.", "APD": "Air Products & Chemicals", "AXP": "American Express",
    "BA": "Boeing Co.", "BDX": "Becton Dickinson", "BKNG": "Booking Holdings",
    "BLK": "BlackRock Inc.", "BMY": "Bristol Myers Squibb", "BRK-B": "Berkshire Hathaway",
    "C": "Citigroup Inc.", "CAT": "Caterpillar Inc.", "CB": "Chubb Ltd.",
    "CI": "Cigna Group", "CL": "Colgate-Palmolive", "COP": "ConocoPhillips",
    "CRM": "Salesforce Inc.", "CSCO": "Cisco Systems", "CSX": "CSX Corp.",
    "CVS": "CVS Health", "CVX": "Chevron Corp.", "DE": "Deere & Co.",
    "DHR": "Danaher Corp.", "DUK": "Duke Energy", "ELV": "Elevance Health",
    "EQIX": "Equinix Inc.", "ETN": "Eaton Corp.", "GE": "General Electric",
    "GILD": "Gilead Sciences", "GM": "General Motors", "GOOG": "Alphabet Inc. (C)",
    "GOOGL": "Alphabet Inc. (A)", "GS": "Goldman Sachs", "HD": "Home Depot",
    "HON": "Honeywell", "IBM": "IBM Corp.", "INTC": "Intel Corp.",
    "INTU": "Intuit Inc.", "ISRG": "Intuitive Surgical", "JNJ": "Johnson & Johnson",
    "JPM": "JPMorgan Chase", "KO": "Coca-Cola", "LIN": "Linde plc",
    "LMT": "Lockheed Martin", "LOW": "Lowe's Companies", "MCD": "McDonald's",
    "MDLZ": "Mondelez Intl.", "MDT": "Medtronic", "META": "Meta Platforms",
    "MMC": "Marsh & McLennan", "MO": "Altria Group", "MRK": "Merck & Co.",
    "MS": "Morgan Stanley", "MSFT": "Microsoft Corp.", "MU": "Micron Technology",
    "NEE": "NextEra Energy", "NFLX": "Netflix Inc.", "NOW": "ServiceNow",
    "NVDA": "NVIDIA Corp.", "PEP": "PepsiCo", "PG": "Procter & Gamble",
    "PLD": "Prologis", "PM": "Philip Morris", "PNC": "PNC Financial",
    "PYPL": "PayPal Holdings", "QCOM": "Qualcomm", "REGN": "Regeneron Pharma",
    "RTX": "RTX Corp.", "SCHW": "Charles Schwab", "SHW": "Sherwin-Williams",
    "SO": "Southern Co.", "SPGI": "S&P Global", "SYK": "Stryker Corp.",
    "T": "AT&T", "TGT": "Target Corp.", "TMO": "Thermo Fisher",
    "TSLA": "Tesla Inc.", "TXN": "Texas Instruments", "UNH": "UnitedHealth Group",
    "UNP": "Union Pacific", "USB": "U.S. Bancorp", "V": "Visa Inc.",
    "VRTX": "Vertex Pharma", "VZ": "Verizon", "WFC": "Wells Fargo",
    "WMT": "Walmart", "XOM": "Exxon Mobil", "ZTS": "Zoetis Inc."
}
OPTIONS = [f"{k} – {v}" for k, v in STOCKS.items()]

# ============================================================
# ADVANCED TERMINAL STYLES
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700;800;900&display=swap');

/* CORE TERMINAL STYLING */
html, body, [class*="css"] {
    background: #000000;
    color: #e8eaed;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

.block-container {
    padding-top: 0rem;
    padding-bottom: 2rem;
    max-width: 100%;
}

/* Remove Streamlit's default padding and margins */
.main > div {
    padding-top: 0rem;
}

header {
    background: transparent !important;
}

.main .block-container {
    padding-left: 2rem;
    padding-right: 2rem;
}

/* HEADER SECTION */
.main-header {
    background: linear-gradient(180deg, #0a0e13 0%, #000000 100%);
    border-bottom: 1px solid rgba(255, 165, 0, 0.15);
    padding: 20px 28px;
    margin: 0rem -2rem 2rem -2rem;
    box-shadow: 0 8px 32px rgba(255, 165, 0, 0.08);
    position: relative;
    z-index: 10;
}

.terminal-title {
    font-size: 26px;
    font-weight: 800;
    letter-spacing: -0.5px;
    background: linear-gradient(135deg, #ffa500 0%, #ff8c00 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 4px;
    text-transform: uppercase;
    line-height: 1.2;
}

.terminal-subtitle {
    font-size: 12px;
    color: #8b8d91;
    font-weight: 500;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    line-height: 1.3;
}

/* STATUS BAR - WALL STREET STYLE */
.status-bar {
    background: linear-gradient(135deg, #0d1117 0%, #161b22 100%);
    border: 1px solid rgba(255, 165, 0, 0.2);
    border-radius: 12px;
    padding: 16px 24px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
    box-shadow: 
        0 4px 20px rgba(255, 165, 0, 0.1),
        inset 0 1px 0 rgba(255, 255, 255, 0.05);
}

.status-left {
    display: flex;
    align-items: center;
    gap: 12px;
}

.status-indicator {
    width: 10px;
    height: 10px;
    background: #00ff88;
    border-radius: 50%;
    box-shadow: 0 0 12px rgba(0, 255, 136, 0.6);
    animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.7; transform: scale(1.1); }
}

.status-text {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 13px;
    font-weight: 600;
    color: #00ff88;
    letter-spacing: 0.5px;
}

.live-pill {
    background: linear-gradient(135deg, rgba(255, 165, 0, 0.15), rgba(255, 140, 0, 0.2));
    border: 1px solid rgba(255, 165, 0, 0.4);
    color: #ffa500;
    padding: 8px 20px;
    border-radius: 20px;
    font-family: 'IBM Plex Mono', monospace;
    font-weight: 700;
    font-size: 11px;
    letter-spacing: 1.2px;
    box-shadow: 0 0 20px rgba(255, 165, 0, 0.2);
}

/* METRIC CARDS - BLOOMBERG INSPIRED */
.metric-card {
    background: linear-gradient(145deg, #0d1117 0%, #161b22 100%);
    border: 1px solid rgba(255, 165, 0, 0.15);
    border-radius: 14px;
    padding: 20px;
    position: relative;
    overflow: hidden;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.metric-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, #ffa500, transparent);
    opacity: 0;
    transition: opacity 0.3s ease;
}

.metric-card:hover {
    border-color: rgba(255, 165, 0, 0.4);
    box-shadow: 0 8px 32px rgba(255, 165, 0, 0.15);
    transform: translateY(-2px);
}

.metric-card:hover::before {
    opacity: 1;
}

.metric-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    color: #8b8d91;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 8px;
    font-weight: 600;
}

.metric-value {
    font-size: 32px;
    font-weight: 900;
    background: linear-gradient(135deg, #ffa500 0%, #00ff88 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -1px;
}

/* TERMINAL INFO BOX */
.terminal-box {
    background: linear-gradient(145deg, #0a0e13 0%, #0d1117 100%);
    border: 1px solid rgba(255, 165, 0, 0.2);
    border-radius: 16px;
    padding: 28px;
    margin-top: 28px;
    box-shadow: 
        0 12px 48px rgba(0, 0, 0, 0.8),
        inset 0 1px 0 rgba(255, 255, 255, 0.05);
    position: relative;
}

.terminal-box::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, #ffa500, transparent);
    opacity: 0.3;
}

.terminal-box b {
    color: #ffa500;
    font-weight: 700;
    font-size: 16px;
    letter-spacing: 0.3px;
}

.terminal-box ul {
    list-style: none;
    padding-left: 0;
}

.terminal-box li {
    padding: 8px 0;
    color: #c9d1d9;
    line-height: 1.6;
    position: relative;
    padding-left: 20px;
}

.terminal-box li::before {
    content: '▸';
    position: absolute;
    left: 0;
    color: #ffa500;
    font-weight: bold;
}

/* NAV GUIDE BOX - ENHANCED */
.nav-guide {
    position: relative;
    background: linear-gradient(145deg, #0d1117, #0a0e13);
    border: 1px solid rgba(255, 165, 0, 0.25);
    border-radius: 14px;
    padding: 20px;
    margin: 20px 0;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6);
    overflow: hidden;
}

.nav-guide::after {
    content: '';
    position: absolute;
    top: -50%;
    right: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(255, 165, 0, 0.03) 0%, transparent 70%);
    animation: rotate 20s linear infinite;
}

@keyframes rotate {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.nav-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    letter-spacing: 1.5px;
    color: #ffa500;
    margin-bottom: 12px;
    font-weight: 700;
    position: relative;
    z-index: 1;
}

.nav-text {
    font-size: 13px;
    line-height: 1.7;
    color: #c9d1d9;
    position: relative;
    z-index: 1;
}

.nav-text span {
    color: #00ff88;
    font-weight: 700;
}

/* SIDEBAR STYLING */
.sidebar-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    color: #8b8d91;
    letter-spacing: 1px;
    margin-top: 20px;
    margin-bottom: 8px;
    font-weight: 600;
    text-transform: uppercase;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a0e13 0%, #000000 100%);
    border-right: 1px solid rgba(255, 165, 0, 0.15);
}

section[data-testid="stSidebar"] > div {
    background: transparent;
}

/* SELECTED SECURITY SECTION */
.security-display {
    background: linear-gradient(135deg, #0d1117 0%, #161b22 100%);
    border: 1px solid rgba(255, 165, 0, 0.25);
    border-left: 4px solid #ffa500;
    border-radius: 12px;
    padding: 20px 24px;
    margin-top: 24px;
    box-shadow: 0 4px 24px rgba(255, 165, 0, 0.1);
}

.security-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    color: #8b8d91;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 8px;
}

.security-name {
    font-size: 24px;
    font-weight: 800;
    color: #ffa500;
    letter-spacing: -0.5px;
}

/* DEVELOPER CREDITS */
.dev-credits {
    background: linear-gradient(135deg, rgba(13, 17, 23, 0.6), rgba(22, 27, 34, 0.4));
    border: 1px solid rgba(255, 165, 0, 0.15);
    border-radius: 12px;
    padding: 20px;
    margin-top: 24px;
    text-align: center;
}

.dev-credits a {
    color: #ffa500;
    text-decoration: none;
    font-weight: 600;
    transition: all 0.2s ease;
}

.dev-credits a:hover {
    color: #ff8c00;
    text-shadow: 0 0 8px rgba(255, 165, 0, 0.4);
}

/* SCROLLBAR STYLING */
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

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(180deg, #ff8c00, #ffa500);
}

/* SELECTBOX STYLING */
div[data-baseweb="select"] {
    background: #0d1117 !important;
    border: 1px solid rgba(255, 165, 0, 0.2) !important;
    border-radius: 8px !important;
}

div[data-baseweb="select"]:hover {
    border-color: rgba(255, 165, 0, 0.4) !important;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# HEADER
# ============================================================
st.markdown("""
<div class="main-header">
    <div class="terminal-title">⚡ EQUITY RISK ANALYTICS TERMINAL</div>
    <div class="terminal-subtitle">Institutional Equity Risk & Volatility Monitoring System</div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# STATUS BAR
# ============================================================
st.markdown("""
<div class="status-bar">
    <div class="status-left">
        <div class="status-indicator"></div>
        <div class="status-text">SYSTEM STATUS: OPERATIONAL</div>
    </div>
    <div class="live-pill">● LIVE ANALYTICS</div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# METRICS
# ============================================================
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown("<div class='metric-card'><div class='metric-title'>MARKET UNIVERSE</div><div class='metric-value'>S&P 100</div></div>", unsafe_allow_html=True)
with c2:
    st.markdown("<div class='metric-card'><div class='metric-title'>SECURITIES</div><div class='metric-value'>100</div></div>", unsafe_allow_html=True)
with c3:
    st.markdown("<div class='metric-card'><div class='metric-title'>RISK ENGINE</div><div class='metric-value'>ACTIVE</div></div>", unsafe_allow_html=True)
with c4:
    st.markdown("<div class='metric-card'><div class='metric-title'>ML FORECASTING</div><div class='metric-value'>ENABLED</div></div>", unsafe_allow_html=True)

# ============================================================
# SIDEBAR
# ============================================================
st.sidebar.markdown("### 📊 RISK TERMINAL")

st.sidebar.markdown("<div class='sidebar-label'>MARKET UNIVERSE</div>", unsafe_allow_html=True)
st.sidebar.selectbox("Market", ["S&P 100"], label_visibility="collapsed")

st.sidebar.markdown("<div class='sidebar-label'>SECURITY SELECTION</div>", unsafe_allow_html=True)
selected = st.sidebar.selectbox("Security", OPTIONS, label_visibility="collapsed")

ticker = selected.split(" – ")[0]
company = STOCKS[ticker]

# NAVIGATION GUIDE BOX
st.sidebar.markdown("""
<div class="nav-guide">
    <div class="nav-title">⚡ NAVIGATION GUIDE</div>
    <div class="nav-text">
        Navigate through <span>stock-level risk analytics</span>,
        <span>portfolio optimization</span>, and
        <span>ML-powered volatility forecasts</span>.
        <br><br>
        Each module represents a specialized
        <span>institutional trading desk</span> terminal.
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# MAIN TERMINAL INFO
# ============================================================
st.markdown("""
<div class="terminal-box">
<b>🎯 TERMINAL OVERVIEW</b><br><br>

<b>📈 Stock Risk Analytics</b><br>
<ul>
<li>Real-time stock-level risk profiling using historical volatility metrics</li>
<li>Cross-sectional risk comparison across S&P 100 universe</li>
<li>Identify high-beta opportunities and defensive positions</li>
</ul><br>

<b>💼 Portfolio Risk Management</b><br>
<ul>
<li>Comprehensive portfolio volatility measurement with correlation analysis</li>
<li>Diversification efficiency scoring and concentration risk detection</li>
<li>Marginal contribution to total portfolio risk (MCTR)</li>
</ul><br>

<b>🤖 ML Volatility Forecasting</b><br>
<ul>
<li>Machine learning models for 5-day forward volatility prediction</li>
<li>Uncertainty quantification and confidence intervals</li>
<li>Real-time model performance metrics (RMSE, MAE)</li>
</ul><br>

<b>🎲 Risk Regime Detection</b><br>
<ul>
<li>Dynamic market regime identification using volatility clustering</li>
<li>Component risk contribution analysis</li>
<li>Tail risk and extreme event probability assessment</li>
</ul>
</div>
""", unsafe_allow_html=True)

# ============================================================
# SELECTED SECURITY
# ============================================================
st.markdown(f"""
<div class="security-display">
    <div class="security-label">SELECTED SECURITY</div>
    <div class="security-name">{ticker} – {company}</div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

# ============================================================
# DEVELOPER CREDITS
# ============================================================
st.sidebar.markdown("""
<div class="dev-credits">
    <div style="font-size:11px; color:#8b8d91; letter-spacing:1px; margin-bottom:8px;">DEVELOPED BY</div>
    <div style="font-size:16px; color:#ffa500; font-weight:700; margin-bottom:12px;">Saransh Nijhawan</div>
    <div style="font-size:13px;">
        <a href="https://www.linkedin.com/in/saransh-nijhawan8142" target="_blank">🔗 LinkedIn</a>
        &nbsp;•&nbsp;
        <a href="https://github.com/SaranshAI13" target="_blank">💻 GitHub</a>
        <br>
        <a href="mailto:saranshnijhawan2005@gmail.com">📧 Gmail</a>
    </div>
</div>
""", unsafe_allow_html=True)