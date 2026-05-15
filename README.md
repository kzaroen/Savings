venv\Scripts\activate
streamlit run app.py

# 💹 2026 Financial Command Center

A fully interactive financial dashboard built with Streamlit + Plotly, based on your 2026 Money Monthly Tracker.

---

## 🚀 How to Run Locally

### 1. Prerequisites
Make sure you have **Python 3.9+** installed.

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv

# Activate it:
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
streamlit run app.py
```

The app will open automatically at **http://localhost:8501**

---

## 🎛️ Features

### Sidebar Controls
- **Income sliders** — All monthly income values are fully adjustable
- **Expense inputs** — Override any month's expenses
- **Bond income inputs** — Update your monthly bond income directly

### Dashboard
- **KPI cards** — Total income, savings, investments, cumulative balance, passive income
- **Cash flow chart** — Income vs outflow vs monthly net (negative months highlighted red)
- **Outflow breakdown** — Donut chart of where money goes
- **Cumulative savings** — Baseline savings growth
- **Investment portfolio** — Growth across Jan/Jun/Dec reinvestment milestones
- **Bond dividend tracker** — Monthly bond income table + bar chart
- **Monthly tracker table** — Full editable view with red highlighting for negative months
- **Smart insights** — Best/worst months, savings rate, investment ratios

---

## 📁 File Structure
```
dashboard/
├── app.py            ← Main Streamlit app
├── requirements.txt  ← Python dependencies
└── README.md         ← This file
```

---

## 🔧 Customization Tips

- To update bond income defaults, edit the `DEFAULT_BOND_INCOME` mapping inside `app.py`
- To change the default income values, update the `default_income` list inside the sidebar section
- To add new funds, extend the `PORTFOLIO` dict and the investment chart section

---

Built for Kei · 2026 · Streamlit + Plotly + Pandas
