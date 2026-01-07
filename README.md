# ⚡ Equity Risk Analytics & Volatility Forecasting Platform

An **institutional-grade, multi-page equity risk analytics terminal** built using **Python, Streamlit, and Machine Learning**, inspired by Bloomberg-style risk desks.

This platform provides **stock-level risk analytics, portfolio risk decomposition, ML-based volatility forecasting, and regime detection** across the **S&P 100 universe** — fully deployed on **Streamlit Cloud**.

---

## 🚀 Live Application

🔗 **Live Demo:** [https://equity-risk-analytics-volatility-forecasting-platform-atn7umcj.streamlit.app](https://equity-risk-analytics-volatility-forecasting-platform-atn7umcj.streamlit.app)

---

## 🧠 Key Features

### 📈 Stock Risk Analytics

* Historical & annualized volatility analysis
* Cross-sectional risk comparison across S&P 100
* Identification of high-beta and defensive stocks
* Risk ranking and summary dashboards

### 💼 Portfolio Risk Management

* Portfolio-level volatility computation
* Correlation matrix & diversification analysis
* Marginal Contribution to Risk (MCTR)
* Weight-based risk decomposition

### 🤖 ML Volatility Forecasting

* Supervised ML models for **5-day forward volatility**
* Prediction uncertainty & confidence intervals
* Model evaluation metrics (RMSE, MAE)
* Forecast vs realized volatility comparison

### 🎲 Risk Regime & Contribution Analysis

* Volatility regime detection (low / medium / high risk)
* Component-wise risk contribution
* Tail-risk awareness & regime shifts

---

## 🏗️ Project Architecture

```text
Equity-Risk-Analytics-Volatility-Forecasting-Platform/
│
├── Dashboard/
│   ├── app.py                  # Main Streamlit entry point
│   ├── requirements.txt
│   ├── pages/
│   │   ├── 1_Stock_Risk.py
│   │   ├── 2_Portfolio_Risk.py
│   │   ├── 3_ML_Volatility_Forecast.py
│   │   └── 4_Risk_Regime_&_Contribution.py
│
├── Data/
│   ├── clean_sp100_data.csv
│   ├── sp100_stocks_data.csv
│   ├── stock_risk_summary.csv
│   ├── stock_return_correlation_matrix.csv
│   ├── portfolio_weights_percentage.csv
│   ├── portfolio_volatility_all_stocks.csv
│   └── layer2_ml_results.csv
│
├── Notebooks/                  # Research & experimentation
└── README.md
```

---

## 🛠️ Tech Stack

* **Python 3.11**
* **Streamlit** – Interactive dashboards & deployment
* **Pandas / NumPy** – Data processing
* **Plotly** – Interactive financial visualizations
* **Scikit-Learn** – Machine learning models
* **Statsmodels** – Statistical & time-series analysis

---

## ☁️ Deployment

The application is deployed using **Streamlit Cloud** with:

* Multi-page architecture (`pages/`)
* Cloud-safe relative data paths
* Cached data loading for performance

To deploy manually:

```bash
streamlit run Dashboard/app.py
```

---

## 🎯 Use Cases

* Equity research & sell-side risk analysis
* Portfolio risk monitoring
* Quant & ML finance projects
* Institutional-style financial dashboards
* Resume / portfolio showcase

---

## 👨‍💻 Developer

**Saransh Nijhawan**

* 🔗 LinkedIn: [https://www.linkedin.com/in/saransh-nijhawan8142](https://www.linkedin.com/in/saransh-nijhawan8142)
* 💻 GitHub: [https://github.com/SaranshAI13](https://github.com/SaranshAI13)
* 📧 Email: [saranshnijhawan2005@gmail.com](mailto:saranshnijhawan2005@gmail.com)

---

## ⭐ Highlights

* End-to-end financial risk platform
* Clean modular architecture
* Production-ready Streamlit deployment
* Resume-grade quantitative finance project

---

> ⚠️ **Disclaimer:** This project is for educational & analytical purposes only. It does not constitute financial or investment advice.
