import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="2026 Financial Overview",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Palette ─────────────────────────────────────────────────────────────────
# E8D6CB  warm linen (lightest bg)
# D0ADA7  dusty rose (muted accent)
# 373F51  slate navy (text / dark elements)
# 0B3954  deep ocean (primary accent)
# 6EA4BF  soft sky blue (charts / highlights)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;1,400&family=DM+Sans:wght@300;400;500&display=swap');

  html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #f5ede8;
  }

  .main { background: #f5ede8; }

  /* ── KPI cards ── */
  .kpi-card {
    background: #ffffff;
    border: 1px solid #E8D6CB;
    border-radius: 14px;
    padding: 20px 22px;
    text-align: center;
    box-shadow: 0 2px 12px rgba(55,63,81,0.06);
  }
  .kpi-label {
    color: #D0ADA7;
    font-size: 10px;
    font-weight: 500;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 6px;
  }
  .kpi-value {
    color: #373F51;
    font-family: 'Lora', serif;
    font-size: 26px;
    font-weight: 600;
  }
  .kpi-sub   { color: #6EA4BF; font-size: 11px; margin-top: 4px; }
  .kpi-neg   { color: #b05555; }
  .kpi-pos   { color: #0B3954; }

  /* ── Section headers ── */
  .section-header {
    color: #0B3954;
    font-family: 'Lora', serif;
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    border-bottom: 1.5px solid #E8D6CB;
    padding-bottom: 8px;
    margin: 28px 0 16px 0;
  }

  /* ── Insight pills ── */
  .insight-pos {
    background: #f0f7fb;
    color: #0B3954;
    border: 1px solid #6EA4BF;
    border-radius: 8px;
    padding: 10px 16px;
    margin: 6px 0;
    font-size: 13px;
  }
  .insight-neg {
    background: #fdf3f0;
    color: #8c3a3a;
    border: 1px solid #D0ADA7;
    border-radius: 8px;
    padding: 10px 16px;
    margin: 6px 0;
    font-size: 13px;
  }
  .insight-neu {
    background: #f7f4f1;
    color: #373F51;
    border: 1px solid #E8D6CB;
    border-radius: 8px;
    padding: 10px 16px;
    margin: 6px 0;
    font-size: 13px;
  }

  /* ── Goal progress card ── */
  .goal-card {
    background: #ffffff;
    border: 1px solid #E8D6CB;
    border-radius: 14px;
    padding: 18px 22px;
    margin-bottom: 12px;
    box-shadow: 0 2px 8px rgba(55,63,81,0.05);
  }
  .goal-title { color: #373F51; font-family: 'Lora', serif; font-size: 14px; font-weight: 600; }
  .goal-meta  { color: #D0ADA7; font-size: 11px; margin-top: 2px; margin-bottom: 10px; }
  .goal-bar-bg {
    background: #E8D6CB;
    border-radius: 99px;
    height: 10px;
    width: 100%;
    overflow: hidden;
  }
  .goal-bar-fill {
    height: 10px;
    border-radius: 99px;
    background: linear-gradient(90deg, #6EA4BF, #0B3954);
    transition: width 0.5s ease;
  }
  .goal-numbers { display: flex; justify-content: space-between; margin-top: 6px; font-size: 11px; color: #D0ADA7; }
  .goal-pct { color: #0B3954; font-weight: 600; font-size: 13px; float: right; margin-top: -6px; }

  /* ── Sidebar ── */
  [data-testid="stSidebar"] {
    background: linear-gradient(135deg, #efe5df 0%, #E8D6CB 50%, #dcc9c2 100%);
    border-right: 2px solid #D0ADA7;
    box-shadow: -2px 0 8px rgba(55,63,81,0.08);
  }
  [data-testid="stSidebar"] > div {
    padding-top: 8px;
  }
  [data-testid="stSidebar"] label {
    color: #373F51 !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    letter-spacing: 0.5px !important;
  }
  [data-testid="stSidebar"] .stSlider > div { accent-color: #0B3954; }
  [data-testid="stSidebar"] .stSelectbox > div,
  [data-testid="stSidebar"] .stNumberInput > div,
  [data-testid="stSidebar"] .stTextInput > div {
    border: 1.5px solid #E8D6CB !important;
    border-radius: 8px !important;
  }
  [data-testid="stSidebar"] .stSelectbox > div > div,
  [data-testid="stSidebar"] .stNumberInput > div > input,
  [data-testid="stSidebar"] .stTextInput > div > input {
    background: rgba(255, 255, 255, 0.6) !important;
    color: #373F51 !important;
    border-radius: 6px !important;
  }
  [data-testid="stSidebar"] .stButton > button {
    background: linear-gradient(135deg, #6EA4BF, #0B3954) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 2px 6px rgba(11,57,84,0.2) !important;
  }
  [data-testid="stSidebar"] .stButton > button:hover {
    box-shadow: 0 4px 12px rgba(11,57,84,0.3) !important;
    transform: translateY(-2px) !important;
  }
  [data-testid="stSidebar"] .stCheckbox,
  [data-testid="stSidebar"] .stRadio {
    padding: 8px 0 !important;
  }
  [data-testid="stSidebar"] .stCheckbox > label > div,
  [data-testid="stSidebar"] .stRadio > label > div {
    color: #373F51 !important;
  }

  /* ── DataFrame tweaks ── */
  .stDataFrame { border-radius: 12px; overflow: hidden; }

  /* ── Plotly border radius ── */
  .js-plotly-plot { border-radius: 14px; overflow: hidden; }

  /* ── Investment Snapshot Table ── */
  .snap-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 12px;
    font-family: 'DM Sans', sans-serif;
  }
  .snap-table th {
    background: #f0e8e2;
    color: #0B3954;
    font-size: 10px;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    padding: 10px 12px;
    text-align: left;
    border-bottom: 1.5px solid #E8D6CB;
  }
  .snap-table td {
    padding: 9px 12px;
    border-bottom: 1px solid #f0e8e2;
    color: #373F51;
    vertical-align: middle;
  }
  .snap-table tr:last-child td { border-bottom: none; }
  .snap-table tr:hover td { background: #faf5f2; }
  .badge-planned {
    background: rgba(110,164,191,0.18);
    color: #0B3954;
    font-size: 9px;
    font-weight: 600;
    letter-spacing: 0.8px;
    padding: 2px 7px;
    border-radius: 99px;
    text-transform: uppercase;
    margin-left: 5px;
  }
  .badge-official {
    background: rgba(245,197,66,0.18);
    color: #9a7d0a;
    font-size: 9px;
    font-weight: 600;
    letter-spacing: 0.8px;
    padding: 2px 7px;
    border-radius: 99px;
    text-transform: uppercase;
    margin-left: 5px;
  }
  .val-pos { color: #2a7a5a; font-weight: 500; }
  .val-neg { color: #b05555; font-weight: 500; }
  .val-zero { color: #ccc; }
  .snap-total-row td {
    background: #f7f4f1;
    font-weight: 600;
    color: #0B3954;
    border-top: 1.5px solid #E8D6CB;
  }

  /* ── Highlight Text ── */
  .highlight-text {
    background: rgba(110,164,191,0.12);
    color: #0B3954;
    padding: 2px 6px;
    border-radius: 6px;
    font-weight: 500;
    display: inline-block;
    margin: 2px 0;
  }
</style>
""", unsafe_allow_html=True)

# ─── Plotly shared theme ──────────────────────────────────────────────────────
BG       = "#ffffff"
PAPER_BG = "#ffffff"
GRID     = "#f0e8e2"
TEXT     = "#373F51"
SUBTEXT  = "#D0ADA7"

def base_layout(title="", h=340):
    return dict(
        title=dict(text=title, font=dict(family="Lora", size=14, color="#0B3954")),
        plot_bgcolor=BG, paper_bgcolor=PAPER_BG,
        font=dict(color=TEXT, size=11, family="DM Sans"),
        legend=dict(orientation="h", y=1.12, font=dict(size=11)),
        margin=dict(l=10, r=10, t=50, b=10),
        height=h,
    )

# ─── Data ────────────────────────────────────────────────────────────────────
MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

FIXED_INSURANCE   = [5400, 0, 0, 10800, 0, 0, 0, 0, 0, 5400, 0, 0]
FIXED_INVESTMENTS = [0, 0, 0, 0, 0, 16000, 0, 0, 0, 0, 0, 24000]
FIXED_SAVINGS     = [5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000]
FIXED_EXPENSES    = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
FIXED_INCOME      = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
NOTES = [
    "Controller purchase • Insurance paid from 2025",
    "", "",
    "Insurance month paid early so ×2",
    "Stabilization",
    "End of 1H 2026 & Reinvest",
    "Mid-year insurance already paid back in April",
    "", "",
    "Insurance month",
    "",
    "Year-end surplus",
]

PORTFOLIO = {
    "BPI US Equity Feeder Fund PHP": {
        "principal": 8000,  "p_date": "Jan 2026",
        "reinvest1": 9000,  "r1_date": "Jun 2026",
        "reinvest2": 13000, "r2_date": "Dec 2026",
        "total": 30000
    },
    "BPI Global Income Bond": {
        "principal": 12000, "p_date": "Jan 2026",
        "reinvest1": 7000,  "r1_date": "Jun 2026",
        "reinvest2": 11000, "r2_date": "Dec 2026",
        "total": 30000
    }
}

# ─── Default Investment Snapshots ─────────────────────────────────────────────
DEFAULT_SNAPSHOTS = [
    {"date": "Feb",          "us_equity": 0.0,       "bond_fund": 0.0,      "bond_income": 0.0,    "official": False, "planned": False},
    {"date": "Mar",          "us_equity": 0.0,       "bond_fund": 0.0,      "bond_income": 0.0,    "official": False, "planned": False},
    {"date": "Apr",          "us_equity": 0.0,       "bond_fund": 0.0,      "bond_income": 0.0,    "official": False, "planned": False},
    {"date": "May",          "us_equity": 0.0,       "bond_fund": 0.0,      "bond_income": 0.0,    "official": False, "planned": False},
    {"date": "Jun",          "us_equity": 0.0,       "bond_fund": 0.0,      "bond_income": 0.0,    "official": False, "planned": True},
    {"date": "Jul",          "us_equity": 0.0,       "bond_fund": 0.0,      "bond_income": 0.0,    "official": False, "planned": False},
    {"date": "Aug",          "us_equity": 0.0,       "bond_fund": 0.0,      "bond_income": 0.0,    "official": False, "planned": False},
    {"date": "Sep",          "us_equity": 0.0,       "bond_fund": 0.0,      "bond_income": 0.0,    "official": False, "planned": False},
    {"date": "Oct",          "us_equity": 0.0,       "bond_fund": 0.0,      "bond_income": 0.0,    "official": False, "planned": False},
    {"date": "Nov",          "us_equity": 0.0,       "bond_fund": 0.0,      "bond_income": 0.0,    "official": False, "planned": False},
    {"date": "Dec",          "us_equity": 0.0,       "bond_fund": 0.0,      "bond_income": 0.0,    "official": False, "planned": True},
]

COST_BASIS = 20000

# ─── Goals Config ─────────────────────────────────────────────────────────────
GOALS = [
    {
        "label": "PS5 Genshin Impact",
        "desc": " Limited Edition Dual Sense Controller",
        "current": 0,
        "target": 4900,
        "unit": "₱",
        "icon": "🎮",
    },
    {
        "label": "Insurance Fund",
        "desc": "₱21,600 for 4 months of insurance coverage",
        "current": 0,
        "target": 21600,
        "unit": "₱",
        "icon": "🛡️",
    },
    {
        "label": "Investment Target",
        "desc": "₱60,000 across both BPI funds by Dec 2026",
        "current": 0,
        "target": 60000,
        "unit": "₱",
        "icon": "📈",
    },
    {
        "label": "P.E.R.A",
        "desc": "Retirement Fund",
        "current": 0,
        "target": 5000,
        "unit": "₱",
        "icon": "📈",
    },
]

# ─── Session State ────────────────────────────────────────────────────────────
if "snapshots" not in st.session_state:
    st.session_state.snapshots = [s.copy() for s in DEFAULT_SNAPSHOTS]

# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:

    import random
    import streamlit as st

    # ───────────────────────── HEADER ─────────────────────────
    st.markdown("# This is for my future self")

    st.markdown(
        "<hr style='margin:6px 0; border:0; height:1px; background-color:#373F51; opacity:0.6;'>",
        unsafe_allow_html=True
    )

    # ───────────────────────── GOALS ─────────────────────────
    st.markdown("### 🎯 Goals")

    goal_current = {}

    with st.expander("View Goals", expanded=False):

        for g in GOALS:
            key = f"goal_{g['label']}"

            if key not in st.session_state:
                st.session_state[key] = float(g["current"])

            if g["label"] == "Insurance Fund":
                step_size = 5400.0
            elif g["label"] == "Investment Target":
                step_size = 1000.0
            else:
                step_size = 100.0

            goal_current[g["label"]] = st.number_input(
                f"{g['icon']} {g['label']}",
                0.0,
                float(g["target"] * 2),
                st.session_state[key],
                step_size,
                format="%.0f",
                key=key
            )

    # ───────────────────────── INCOME ─────────────────────────
    st.markdown("### 🏦 Savings In")

    income_inputs = {}
    default_income = [5000] * 12

    with st.expander("Monthly Income", expanded=False):
        for i, m in enumerate(MONTHS):
            income_inputs[m] = st.number_input(
                f"{m}",
                0,
                50000,
                default_income[i],
                500,
                key=f"income_{m}"
            )

    # ───────────────────────── EXPENSES ─────────────────────────
    st.markdown("### 💸 Expenses")

    expense_inputs = {}

    with st.expander("Active Months", expanded=False):
        for i, m in enumerate(MONTHS):
            if FIXED_EXPENSES[i] > 0:
                expense_inputs[m] = st.number_input(
                    f"{m}",
                    0,
                    50000,
                    FIXED_EXPENSES[i],
                    500,
                    key=f"exp_active_{m}"
                )
            else:
                expense_inputs[m] = 0

    with st.expander("Inactive Months", expanded=False):
        for i, m in enumerate(MONTHS):
            if FIXED_EXPENSES[i] == 0:
                expense_inputs[m] = st.number_input(
                    f"{m}",
                    0,
                    50000,
                    0,
                    500,
                    key=f"exp_future_{m}"
                )

    # ───────────────────────── SNAPSHOTS ─────────────────────────
    st.markdown("### 📸 Investments")

    with st.expander("Add Snapshots", expanded=False):

        snap_date     = st.text_input("Date", key="snap_date")
        snap_equity   = st.number_input("US Equity", 0.0, value=0.0, step=10.0, format="%.2f", key="snap_eq")
        snap_bond     = st.number_input("Bond Fund", 0.0, value=0.0, step=10.0, format="%.2f", key="snap_bond")
        snap_bincome  = st.number_input("Bond Income", 0.0, value=0.0, step=1.0, format="%.2f", key="snap_bi")
        snap_official = st.checkbox("Official", key="snap_official")
        snap_planned  = st.checkbox("Planned", key="snap_planned")

        if st.button("Add Snapshot", use_container_width=True):
            if snap_date:
                st.session_state.snapshots.append({
                    "date": snap_date,
                    "us_equity": snap_equity,
                    "bond_fund": snap_bond,
                    "bond_income": snap_bincome,
                    "official": snap_official,
                    "planned": snap_planned,
                })
                st.success(f"Added: {snap_date}")

        st.divider()

        edit_idx = st.number_input("Edit index", 0,
                                   max(0, len(st.session_state.snapshots) - 1),
                                   0, key="edit_idx")

        if st.session_state.snapshots:
            s = st.session_state.snapshots[edit_idx]

            e_eq = st.number_input("Equity", value=float(s["us_equity"]), step=10.0, format="%.2f", key="e_eq")
            e_bf = st.number_input("Bond Fund", value=float(s["bond_fund"]), step=10.0, format="%.2f", key="e_bf")
            e_bi = st.number_input("Bond Income", value=float(s["bond_income"]), step=1.0, format="%.2f", key="e_bi")

            if st.button("Save"):
                s["us_equity"] = e_eq
                s["bond_fund"] = e_bf
                s["bond_income"] = e_bi

    # ───────────────────────── VERSE ─────────────────────────
    verses = [ ("Proverbs 21:20 (KJV)", "There is treasure to be desired and oil in the dwelling  of the wise; but a foolish man spendeth it up."), 
              ("Proverbs 6:6–8 (KJV)", "Go to the ant, thou sluggard; consider her ways, and be wise: Which having no guide, overseer, or ruler, provideth her meat in the summer, and gathereth her food in the harvest."), 
              ("Luke 14:28 (KJV)", "For which of you, intending to build a tower, sitteth not down first, and counteth the cost, whether he have sufficient to finish it?"), ("Proverbs 22:7 (KJV)", "The rich ruleth over the poor, and the borrower is servant to the lender."), 
              ("Proverbs 13:11 (KJV)", "Wealth gotten by vanity shall be diminished: but he that gathereth by labour shall increase."), 
              ("1 Corinthians 4:2 (KJV)", "Moreover it is required in stewards, that a man be found faithful."), 
              ("Ecclesiastes 11:1 (KJV)", "Cast thy bread upon the waters: for thou shalt find it after many days."), 
              ("Galatians 6:9 (KJV)", "And let us not be weary in well doing: for in due season we shall reap, if we faint not."), 
              ("Proverbs 10:4 (KJV)", "He becometh poor that dealeth with a slack hand: but the hand of the diligent maketh rich."), 
              ("1 Timothy 6:6 (KJV)", "But godliness with contentment is great gain."), 
              ("Hebrews 13:5 (KJV)", "Let your conversation be without covetousness; and be content with such things as ye have…") ]

    ref, verse = random.choice(verses)

    st.caption(f"**{ref}**  \n*{verse}*")
    
    st.caption("Earn wisely. Give faithfully. Your money is a tool, not a treasure. Use it to build the life you want and to bless others along the way. May you be guided by Jesus Christ. May you be a good steward of the resources God has entrusted to you. Remember that true wealth is found not in money, but in a life well lived. God will provide, and He will always provide more than enough.")

# ─── Build DataFrame ──────────────────────────────────────────────────────────
def build_df(income_map, expense_map):
    rows = []
    cum = 0
    for i, m in enumerate(MONTHS):
        inc = income_map[m]
        ins = FIXED_INSURANCE[i]
        inv = FIXED_INVESTMENTS[i]
        exp = expense_map[m]
        net = inc - exp - inv - (ins if m != "Jan" else 0)
        cum += net
        rows.append({
                "Month": m, "Insurance": ins,
                "Investments": inv,"Savings In": inc, "Expenses": exp,
                "Monthly Net": net, "Cumulative": cum
        })
    return pd.DataFrame(rows)

baseline_df = build_df(income_inputs, expense_inputs)

# ─── KPIs ─────────────────────────────────────────────────────────────────────
total_income = baseline_df["Savings In"].sum()
total_savings_flow = baseline_df["Savings In"].sum()
total_investments  = baseline_df["Investments"].sum()
total_expenses     = baseline_df["Expenses"].sum()
end_cumulative     = baseline_df["Cumulative"].iloc[-1]
savings_rate       = (total_savings_flow / total_income * 100) if total_income else 0
best_month         = baseline_df.loc[baseline_df["Monthly Net"].idxmax(), "Month"]
worst_month        = baseline_df.loc[baseline_df["Monthly Net"].idxmin(), "Month"]
neg_months         = baseline_df[baseline_df["Monthly Net"] < 0]["Month"].tolist()

bond_income_ytd = sum(s["bond_income"] for s in st.session_state.snapshots if "2026" in s["date"])

# ─── Header ──────────────────────────────────────────────────────────────────
st.markdown(
    '<div style="text-align:center;padding:16px 0 4px 0;">'
    '<span style="font-family:Lora,serif;color:#0B3954;font-size:24px;font-weight:600;">'
    '2026 Financial Overview</span></div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div style="text-align:center;color:#D0ADA7;font-size:11px;letter-spacing:2.5px;'
    'text-transform:uppercase;margin-bottom:24px;">Blessed to give, not hoard.</div>',
    unsafe_allow_html=True
)

# ─── KPI Row ──────────────────────────────────────────────────────────────────
c1, c2, c3, c4, c5 = st.columns(5)
kpis = [
    (c1, "Total Savings In",        f"₱{total_income:,.0f}",       "Annual Total in",                          False),
    (c2, "Savings Deposited",   f"₱{total_savings_flow:,.0f}", f"{savings_rate:.1f}% rate", False),
    (c3, "Total Invested",      f"₱{total_investments:,.0f}",  "Scheduled",                 False),
    (c4, "Year-end Cumulative", f"₱{end_cumulative:,.0f}",     "Money left",                          end_cumulative < 0),
    (c5, "Bond Income YTD",     f"₱{bond_income_ytd:,.2f}", "Passive",            False),
]
for col, label, val, sub, is_neg in kpis:
    with col:
        st.markdown(f"""
        <div class="kpi-card">
          <div class="kpi-label">{label}</div>
          <div class="kpi-value {'kpi-neg' if is_neg else 'kpi-pos'}">{val}</div>
          <div class="kpi-sub">{sub}</div>
        </div>""", unsafe_allow_html=True)

# ─── Goals Section ────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">🎯 Goals</div>', unsafe_allow_html=True)

goal_cols = st.columns(4)
for idx, g in enumerate(GOALS):
    current_val = goal_current[g["label"]]
    target_val  = g["target"]
    pct         = min(current_val / target_val * 100, 100) if target_val else 0
    fill_w      = f"{pct:.1f}%"

    with goal_cols[idx]:
        st.markdown(f"""
        <div class="goal-card">
          <div class="goal-title">{g['icon']} {g['label']}</div>
          <div class="goal-meta">{g['desc']}</div>
          <span class="goal-pct">{pct:.0f}%</span>
          <div class="goal-bar-bg">
            <div class="goal-bar-fill" style="width:{fill_w};"></div>
          </div>
          <div class="goal-numbers">
            <span>{g['unit']}{current_val:,.0f}</span>
            <span>{g['unit']}{target_val:,.0f}</span>
          </div>
        </div>""", unsafe_allow_html=True)

# ─── Charts Row 1 ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">📊 Cash Flow</div>', unsafe_allow_html=True)

col_a, col_b = st.columns([3, 2])

with col_a:
    fig = go.Figure()
    fig.add_bar(x=baseline_df["Month"], y=baseline_df["Savings In"],
                name="Savings In", marker_color="#6EA4BF", opacity=0.85)
    fig.add_bar(
        x=baseline_df["Month"],
        y=baseline_df["Insurance"] + baseline_df["Investments"] + baseline_df["Expenses"],
        name="Total Outflow", marker_color="#D0ADA7", opacity=0.80
    )
    fig.add_scatter(
        x=baseline_df["Month"], y=baseline_df["Monthly Net"],
        name="Net", mode="lines+markers",
        line=dict(color="#0B3954", width=2.5),
        marker=dict(size=8, color=[
            "#b05555" if v < 0 else "#0B3954"
            for v in baseline_df["Monthly Net"]
        ])
    )
    layout = base_layout("Monthly Income vs Outflow vs Net", 340)
    st.caption("\n")
    layout["barmode"] = "group"
    fig.update_layout(**layout)
    fig.update_xaxes(showgrid=False, color=TEXT)
    fig.update_yaxes(showgrid=True, gridcolor=GRID, color=SUBTEXT,
                     tickprefix="₱", tickformat=",")
    st.plotly_chart(fig, use_container_width=True)

with col_b:
    labels = ["Savings Deposits", "Insurance", "Investments", "Expenses"]
    values = [total_savings_flow, sum(FIXED_INSURANCE), total_investments, total_expenses]
    colors = ["#6EA4BF", "#D0ADA7", "#0B3954", "#E8D6CB"]
    fig2 = go.Figure(go.Pie(
        labels=labels, values=values,
        hole=0.55, marker_colors=colors,
        textinfo="label+percent", textfont_size=11,
    ))
    fig2.update_layout(**base_layout("Annual Outflow Breakdown", 340))
    fig2.update_layout(showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)

# ─── Charts Row 2 ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">📈 Savings Growth</div>', unsafe_allow_html=True)

col_c, col_d = st.columns([3, 2])

with col_c:
    fig3 = go.Figure()
    fig3.add_scatter(
        x=baseline_df["Month"], y=baseline_df["Cumulative"],
        name="Cumulative", mode="lines+markers",
        line=dict(color="#0B3954", width=2.5),
        marker=dict(size=8, color="#6EA4BF"),
        fill="tozeroy", fillcolor="rgba(110,164,191,0.10)"
    )
    fig3.add_hline(y=0, line_color="#D0ADA7", line_dash="dot", line_width=1.5)
    fig3.update_layout(**base_layout("Cumulative Savings Growth", 320))
    fig3.update_xaxes(showgrid=False, color=TEXT)
    fig3.update_yaxes(showgrid=True, gridcolor=GRID, color=SUBTEXT,
                      tickprefix="₱", tickformat=",")
    st.plotly_chart(fig3, use_container_width=True)

with col_d:
    inv_months   = ["Jan", "Jun", "Dec"]
    us_eq_values = [8000, 8000+9000, 8000+9000+13000]
    bond_values  = [12000, 12000+7000, 12000+7000+11000]

    fig4 = go.Figure()
    fig4.add_bar(x=inv_months, y=us_eq_values, name="US Equity Feeder", marker_color="#6EA4BF")
    fig4.add_bar(x=inv_months, y=bond_values,  name="Global Bond",       marker_color="#0B3954")
    layout4 = base_layout("Investment Portfolio Growth", 320)
    layout4["barmode"] = "group"
    fig4.update_layout(**layout4)
    fig4.update_xaxes(showgrid=False, color=TEXT)
    fig4.update_yaxes(showgrid=True, gridcolor=GRID, color=SUBTEXT,
                      tickprefix="₱", tickformat=",")
    st.plotly_chart(fig4, use_container_width=True)

# ─── Investment Tracker (replaces Bond Dividends) ────────────────────────────
st.markdown('<div class="section-header">📸 Investment Tracker</div>', unsafe_allow_html=True)

snaps = st.session_state.snapshots
actual_snaps  = [s for s in snaps if not s["planned"] and s["us_equity"] > 0]
latest_snap   = actual_snaps[-1] if actual_snaps else None
latest_equity = latest_snap["us_equity"] if latest_snap else 8000
latest_bond   = latest_snap["bond_fund"] if latest_snap else 12000
latest_total  = latest_equity + latest_bond
unrealized    = latest_total - COST_BASIS
total_snap_income = sum(s["bond_income"] for s in snaps)
net_pnl       = unrealized + total_snap_income

col_e, col_f = st.columns([3, 2])

with col_e:
    # Build HTML table rows
    rows_html = ""
    for s in snaps:
        row_total  = s["us_equity"] + s["bond_fund"]
        unreal     = row_total - COST_BASIS if row_total > 0 else 0
        unreal_cls = "val-pos" if unreal > 0 else ("val-neg" if unreal < 0 else "val-zero")
        unreal_str = (f"+₱{unreal:,.2f}" if unreal > 0 else f"₱{unreal:,.2f}") if row_total > 0 else '<span class="val-zero">—</span>'

        # Badges
        badge = ""
        if s["official"]:
            badge = '<span class="badge-official">✦ Official</span>'
        elif s["planned"]:
            badge = '<span class="badge-planned">⏳ Planned</span>'

        eq_str = f"₱{s['us_equity']:,.2f}" if s["us_equity"] > 0 else '<span class="val-zero">—</span>'
        bf_str = f"₱{s['bond_fund']:,.2f}"  if s["bond_fund"]  > 0 else '<span class="val-zero">—</span>'
        tt_str = f"₱{row_total:,.2f}"        if row_total       > 0 else '<span class="val-zero">—</span>'
        bi_str = f"₱{s['bond_income']:.2f}"  if s["bond_income"] > 0 else '<span class="val-zero">—</span>'

        rows_html += f"""
        <tr>
          <td>{s['date']}{badge}</td>
          <td>{eq_str}</td>
          <td>{bf_str}</td>
          <td>{tt_str}</td>
          <td class="{unreal_cls}">{unreal_str}</td>
          <td>{bi_str}</td>
        </tr>"""

    # Totals row
    rows_html += f"""
    <tr class="snap-total-row">
      <td>TOTAL</td>
      <td>—</td>
      <td>—</td>
      <td>—</td>
      <td>—</td>
      <td>₱{total_snap_income:.2f}</td>
    </tr>"""

    st.markdown(f"""
    <div style="background:#fff;border:1px solid #E8D6CB;border-radius:14px;
                overflow:hidden;box-shadow:0 2px 8px rgba(55,63,81,0.05);">
      <table class="snap-table">
        <thead>
          <tr>
            <th>Date</th>
            <th>US Equity Feeder</th>
            <th>Global Bond</th>
            <th>Total</th>
            <th>Unrealized G/L</th>
            <th>Bond Income</th>
          </tr>
        </thead>
        <tbody>{rows_html}</tbody>
      </table>
    </div>
    """, unsafe_allow_html=True)

with col_f:
    # Stacked bar chart — actual snapshots only
    if actual_snaps:
        dates_a = [s["date"] for s in actual_snaps]
        eq_a    = [s["us_equity"] for s in actual_snaps]
        bf_a    = [s["bond_fund"] for s in actual_snaps]
        tot_a   = [s["us_equity"] + s["bond_fund"] for s in actual_snaps]

        fig_snap = go.Figure()
        fig_snap.add_bar(x=dates_a, y=eq_a, name="US Equity",  marker_color="#6EA4BF", opacity=0.9)
        fig_snap.add_bar(x=dates_a, y=bf_a, name="Bond Fund",  marker_color="#0B3954", opacity=0.9)
        fig_snap.add_scatter(
            x=dates_a, y=tot_a, name="Total",
            mode="lines+markers",
            line=dict(color="#D0ADA7", width=2, dash="dot"),
            marker=dict(size=7, color="#D0ADA7")
        )
        layout_snap        = base_layout("Actual Portfolio Snapshots", 280)
        layout_snap["barmode"] = "stack"
        fig_snap.update_layout(**layout_snap)
        fig_snap.update_xaxes(showgrid=False, color=TEXT)
        fig_snap.update_yaxes(showgrid=True, gridcolor=GRID, color=SUBTEXT,
                              tickprefix="₱", tickformat=",")
        st.plotly_chart(fig_snap, use_container_width=True)

    # Two mini P&L cards
    st.markdown(f"""
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:8px;">
      <div class="kpi-card" style="padding:14px 12px;">
        <div class="kpi-label">Unrealized G/L</div>
        <div class="kpi-value {'kpi-neg' if unrealized < 0 else 'kpi-pos'}" style="font-size:20px;">
          {'+'if unrealized >= 0 else ''}₱{unrealized:,.2f}
        </div>
        <div class="kpi-sub">vs ₱{COST_BASIS:,} cost</div>
      </div>
      <div class="kpi-card" style="padding:14px 12px;">
        <div class="kpi-label">Net P&L</div>
        <div class="kpi-value {'kpi-neg' if net_pnl < 0 else 'kpi-pos'}" style="font-size:20px;">
          {'+'if net_pnl >= 0 else ''}₱{net_pnl:,.2f}
        </div>
        <div class="kpi-sub">incl. bond income</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ─── Monthly Tracker Table ────────────────────────────────────────────────────
st.markdown('<div class="section-header">📋 Monthly Tracker</div>', unsafe_allow_html=True)

tracker_df = pd.DataFrame([
    {
        "Month": m,
        "Insurance": FIXED_INSURANCE[i],
        "Investments": FIXED_INVESTMENTS[i],
        "Savings In": income_inputs[m],
        "Expenses": expense_inputs[m],
        "Monthly Net": (
            income_inputs[m] - expense_inputs[m] - FIXED_INVESTMENTS[i] -
            (FIXED_INSURANCE[i] if m != "Jan" else 0)
        ),
        "Notes": NOTES[i],
    }
    for i, m in enumerate(MONTHS)
])
tracker_df["Cumulative Savings"] = tracker_df["Monthly Net"].cumsum()

for col in ["Insurance", "Investments","Savings In", "Expenses", "Monthly Net", "Cumulative Savings"]:
    tracker_df[col] = tracker_df[col].apply(lambda x: f"₱{x:,.0f}")

def highlight_negative(row):
    net_val = int(row["Monthly Net"].replace("₱", "").replace(",", ""))
    if net_val < 0:
        return ["background-color: #fdf3f0; color: #8c3a3a"] * len(row)
    return [""] * len(row)

st.dataframe(
    tracker_df.style.apply(highlight_negative, axis=1),
    use_container_width=True,
    hide_index=True,
    height=460
)

# ─── Insights ─────────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">🔍 Insights</div>', unsafe_allow_html=True)

col_g, col_h = st.columns(2)

with col_g:
    st.markdown("**Cash Flow**")
    st.markdown(f'<div class="insight-pos">🏆 Best month: <b>{best_month}</b></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="insight-neg">⚠️ Toughest month: <b>{worst_month}</b></div>', unsafe_allow_html=True)
    if neg_months:
        st.markdown(f'<div class="insight-neg">🔴 Negative net months: <b>{", ".join(neg_months)}</b></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="insight-pos">✅ No negative net months this year</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="insight-neu">📊 Annual savings rate: <b>{savings_rate:.1f}%</b></div>', unsafe_allow_html=True)

with col_h:
    st.markdown("**Investments & Passive Income**")
    total_bond_income = bond_income_ytd
    invest_vs_save = (total_investments / total_savings_flow * 100) if total_savings_flow else 0
    st.markdown(f'<div class="insight-pos">💸 Bond income so far: <b>₱{total_bond_income:,.2f}</b></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="insight-neu">📈 Total invested this year: <b>₱{total_investments:,.0f}</b></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="insight-neu">⚖️ Invest vs savings ratio: <b>{invest_vs_save:.1f}%</b></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="insight-neu">🎯 Investment target: <b>₱60,000</b> (₱30k per fund)</div>', unsafe_allow_html=True)

st.markdown("---")

st.caption("Remember Keiza, you're saving up for your future. It'll be hard, there will be times when you want to spend your hard earned money but remember. You have to think about your future self. You want to be able to provide for your family, to be able to give generously, and to be able to enjoy the fruits of your labor without worry. So stay disciplined, stay focused, and keep your eyes on the prize. Your future self will thank you for it. But never forget that money is replacable, prioritize your present self when worse comes to worst. God will provide, and He will always provide more than enough.")

st.markdown(
    '<div style="text-align:center;color:#D0ADA7;font-size:11px;letter-spacing:1px;">'
    'Built for Kei · 2026 Financial Overview · Streamlit + Plotly</div>',
    unsafe_allow_html=True
)