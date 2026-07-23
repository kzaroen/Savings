# 🌊 TIDES

A personal flow system built with Python, Streamlit, Plotly, and Pandas.

TIDES is a reflective financial dashboard designed to visualize the movement of savings, investments, spending, and long-term financial growth over time.

Rather than treating finance as static numbers on a spreadsheet, TIDES focuses on patterns, flow, balance, and intentional decision-making through an interactive and accessible web application.

Designed for cross-device accessibility through deployment on Streamlit Community Cloud.

---

# ✨ Features

## 🌊 Flow Tracking

Monitor the movement of your finances through:

* savings tracking
* cash inflow and outflow analysis
* monthly balance monitoring
* insurance payment records
* cumulative yearly progress
* net flow visualization

---

## 📈 Investment Overview

Track portfolio activity and long-term growth through:

* portfolio allocation monitoring
* investment performance visualization
* unrealized gain/loss tracking
* net P&L calculations
* bond income monitoring
* investment snapshot logging

---

## 🎯 Long-Term Goals

Track progress toward personal financial milestones including:

* emergency reserves
* insurance preparation
* retirement contributions (P.E.R.A.)
* investment targets
* personal growth goals

---

## 📊 Interactive Analytics

Powered by Plotly for dynamic visualizations including:

* flow analytics
* portfolio growth charts
* balance trends
* investment breakdowns
* long-term pattern insights

---

## 🌿 Personalized Experience

* responsive dashboard layout
* dynamic KPI cards
* custom visual styling
* reflective dashboard experience
* motivational and faith-informed reminders

---

## 🗓️ Multi-Year Architecture

* year selector drives every table, chart, and form
* `YEARLY_CONFIG` holds year-specific schedules, goals, and milestones so a new year is a config entry, not a rewrite
* Supabase tables scoped by `(year, ...)` unique keys so historical data is never overwritten

---

# 🛠️ Tech Stack

* Python 3.13
* Streamlit
* Plotly Graph Objects
* Pandas
* Supabase PostgreSQL

---

# 🔒 Security Notes & Known Limitations

TIDES currently uses a **session-based password gate** to separate viewing from editing:

* Anyone with the deployed link can **view** the full dashboard — no account needed.
* **Editing** (deposits, expenses, goals, snapshots) is locked behind a password stored in `st.secrets["EDIT_PASSWORD"]`, unlocked per-browser-session via a sidebar expander.

**This is a soft deterrent, not real security.** It's important to be precise about this:

* The gate controls what renders in the Streamlit UI (`disabled=` on widgets, conditional rendering) — it does **not** enforce anything at the data layer.
* There is no per-request identity check against Supabase, and no Row Level Security on the `monthly_finance`, `goals`, or `investment_snapshots` tables. Anything that reaches the save functions directly, bypassing the rendered UI, is not blocked by this gate.
* The password itself lives only in `st.secrets` (never committed to the repo), which is correct practice — but the *mechanism* using it is UI-only, so a correctly-stored secret doesn't make the enforcement any stronger.

**Why it's deferred rather than fixed now:** TIDES is currently a single-person tool with no public sign-up flow and no high-value target, so the cost of building proper authorization exceeds the risk today. This was a deliberate trade-off to prioritize finishing the multi-year architecture, not an oversight.

**The real fix, planned for later:** Supabase Auth + Row Level Security, so authorization is enforced by the database itself rather than by what the Streamlit UI happens to render. This is expected to land alongside the broader TIDES 3.0 rebuild (see Planned Features), when multi-user support is on the table anyway and RLS becomes necessary rather than optional.

Until then: treat the password as a way to stop casual poking-around, not as protection for sensitive data against a motivated actor.

---

# 🚀 Running Locally

## 1. Clone Repository

```bash
git clone https://github.com/kzaroen/tides.git
cd tides
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Run Streamlit App

```bash
streamlit run app.py
```

The application will open at:

```text
http://localhost:8501
```

---

### 5. Configure Streamlit Secrets

Create:

.streamlit/secrets.toml

and add your Supabase credentials, plus an edit-mode password, before running the application:

```toml
SUPABASE_URL = "..."
SUPABASE_KEY = "..."
EDIT_PASSWORD = "..."
```

---

# ☁️ Deployment

TIDES is designed for deployment using:

* Streamlit Community Cloud
* GitHub integration
* Supabase backend services

Accessible across:

* desktop
* laptop
* tablet
* mobile devices

---

## 📁 Project Structure

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

> **Note:** `.venv/` and `.streamlit/secrets.toml` are used for local development and are intentionally excluded from version control.

---

# 🔮 Planned Features

* proper authentication system — Supabase Auth + Row Level Security (see Security Notes above)
* enhanced mobile responsiveness
* AI-generated financial insights
* automated savings analytics
* dividend forecasting
* multi-year flow projections
* historical trend analysis
* portfolio allocation intelligence
* long-term: navigation-based product architecture (TIDES 3.0 vision — React/Next.js frontend on the same Supabase backend)

---

# 🌊 Philosophy

TIDES was built as more than a financial tracker.

It is a system for observing patterns, maintaining clarity, and building intentional financial habits over time.

The project reflects the idea that financial growth is not only about accumulation, but also about awareness, discipline, stability, and stewardship.

Money is treated as a tool to support:

* stability
* generosity
* freedom
* future opportunities
* long-term peace of mind

---

# 🌊 Why "TIDES"?

Financial progress comes in waves.

Some months are focused on saving, others on investing or spending. Rather than aiming for perfectly linear growth, TIDES embraces the natural rhythm of personal finance while encouraging consistent, intentional progress over time.

Like the tides, financial progress is never perfectly linear—but with consistency, every wave moves forward.

---

## 📜 License

This project is intended for personal learning and portfolio purposes.

Feel free to explore the code and ideas for educational use.

---

🌊 Built by Kei

TIDES © 2026

Powered by Streamlit • Plotly • Pandas • Supabase