# 🌊 TIDES

A personal financial flow system built with **Python**, **Streamlit**, **Plotly**, **Pandas**, and **Supabase**.

TIDES is a multi-year personal finance dashboard designed to help visualize the movement of savings, investments, expenses, and long-term wealth over time.

Rather than treating finance as static numbers in a spreadsheet, TIDES focuses on patterns, flow, stewardship, and intentional decision-making through an interactive web application that can be accessed anywhere.

Built for continuous financial tracking across multiple years and deployed using Streamlit Community Cloud.

---

# ✨ Features

## 🗓 Multi-Year Financial Tracking

Organize your finances by year while keeping historical records separate.

Track independently for every year:

* monthly savings
* expenses
* investments
* portfolio snapshots
* financial goals
* yearly milestones

Switch between years instantly without affecting historical data.

---

## 🌊 Cash Flow Tracking

Monitor the movement of your finances through:

* savings tracking
* monthly cash inflow and outflow
* insurance payment schedules
* investment contributions
* cumulative balance monitoring
* yearly net cash flow

---

## 📈 Investment Portfolio

Track long-term investment performance with support for:

* portfolio allocation
* unrealized gain/loss
* realized investment income
* net P&L
* bond income tracking
* investment snapshots
* cost basis calculations

---

## 🏦 Retirement Tracking

Monitor retirement progress through Personal Equity and Retirement Account (P.E.R.A.) tracking.

Includes:

* retirement balance
* annual contributions
* contribution progress
* retirement savings separate from liquid net worth

---

## 🎯 Financial Goals

Track progress toward long-term milestones including:

* emergency funds
* insurance reserves
* retirement savings
* investment targets
* personal purchases
* custom yearly goals

---

## 📊 Interactive Analytics

Powered by Plotly for dynamic visualizations including:

* yearly cash flow
* cumulative savings
* portfolio growth
* asset allocation
* financial trends
* historical comparisons

---

## ☁️ Cloud Database

Persistent financial records are stored using Supabase PostgreSQL.

Features include:

* cloud synchronization
* year-isolated records
* investment history
* goal persistence
* portfolio snapshots

---

## 🌿 Personalized Dashboard

Designed to provide a calm, reflective financial experience through:

* responsive layout
* custom KPI cards
* personalized styling
* yearly milestones
* motivational reminders
* faith-inspired stewardship verses

---

# 🛠 Tech Stack

* Python 3.13
* Streamlit
* Plotly Graph Objects
* Pandas
* Supabase PostgreSQL

---

# 🚀 Running Locally

## 1. Clone the repository

```bash
git clone https://github.com/kzaroen/tides.git
cd tides
```

---

## 2. Create a virtual environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Streamlit Secrets

Create:

```text
.streamlit/secrets.toml
```

Add your Supabase credentials:

```toml
SUPABASE_URL="..."
SUPABASE_KEY="..."
```

---

## 5. Run the application

```bash
streamlit run app.py
```

The application will be available at:

```text
http://localhost:8501
```

---

# ☁️ Deployment

TIDES is designed for deployment using:

* Streamlit Community Cloud
* GitHub
* Supabase PostgreSQL

Accessible across:

* Desktop
* Laptop
* Tablet
* Mobile devices

---

# 📁 Project Structure

```text
tides-flow/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── assets/
│   └── styles.css
│
└── .streamlit/
    └── secrets.toml
```

> `.venv/` and `.streamlit/secrets.toml` are excluded from version control for security and local development.

---

# 🔮 Roadmap

Future improvements include:

* user authentication
* enhanced mobile experience
* AI-powered financial insights
* cash flow forecasting
* dividend forecasting
* multi-year wealth projections
* historical trend comparisons
* portfolio allocation intelligence
* exportable yearly financial reports

---

# 🏗 Architecture

TIDES uses a year-isolated architecture built on Supabase.

Financial records are separated by year while sharing a common application interface.

This allows:

* scalable multi-year tracking
* historical preservation
* reusable yearly configurations
* isolated financial goals
* year-specific investment snapshots

As each year begins, only configuration values need to be updated—no application logic has to be rewritten.

---

# 🌊 Philosophy

TIDES was built as more than a financial tracker.

It is a system for observing financial patterns, building discipline, and making intentional decisions over time.

Rather than pursuing perfectly linear growth, TIDES embraces the reality that personal finance moves in seasons.

Money is viewed as a resource to be stewarded wisely—supporting stability, generosity, freedom, future opportunities, and long-term peace of mind.

---

# 🌊 Why "TIDES"?

Financial progress comes in waves.

Some months emphasize saving.

Others focus on investing, spending, or preparing for future obligations.

Like the tides, progress is rarely perfectly linear—but with consistency and wise stewardship, every wave moves you forward.

---

## 📜 License

This project is intended for personal learning and portfolio purposes.

Feel free to explore the code and ideas for educational use.

---

🌊 **Built by Kei**

**TIDES © 2026**

*Powered by Streamlit • Plotly • Pandas • Supabase*
