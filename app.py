import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import random
from datetime import datetime
from pathlib import Path
from supabase import create_client

# ─── Supabase Connection ─────────────────────────────────────────────────────
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ─── Page Config ─────────────────────────────────────────────────────────────
# Kept year-agnostic since set_page_config must run before we can read the
# year selector value (it has to be the first Streamlit call in the script).
st.set_page_config(
    page_title="Flow of Tides",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ──────────────────────────────────────────────────────────────
css = Path("assets/styles.css").read_text()
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

# ─── Plotly theme ────────────────────────────────────────────────────────────
BG = PAPER_BG = "#ffffff"
GRID    = "#f0e8e2"
TEXT    = "#373F51"
SUBTEXT = "#D0ADA7"

def base_layout(title="", h=340):
    return dict(
        title=dict(text=title, font=dict(family="Lora", size=14, color="#0B3954")),
        plot_bgcolor=BG, paper_bgcolor=PAPER_BG,
        font=dict(color=TEXT, size=11, family="DM Sans"),
        legend=dict(orientation="h", y=1.12, font=dict(size=11)),
        margin=dict(l=10, r=10, t=50, b=10),
        height=h,
    )

# ═══════════════════════════════════════════════════════════════════════════════
# STATIC CONFIG (year-independent)
# ═══════════════════════════════════════════════════════════════════════════════

MONTHS      = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
MONTH_INDEX = {m: i for i, m in enumerate(MONTHS)}

SAVINGS_FLOOR = 2000

# Annual PERA contribution cap for employed contributors (₱). OFWs get a
# higher cap — adjust this if that ever applies to you.
PERA_CONTRIBUTION_CAP = 200000

VERSES = [
    ("Proverbs 21:20 (KJV)", "There is treasure to be desired and oil in the dwelling of the wise; but a foolish man spendeth it up."),
    ("Proverbs 6:6–8 (KJV)", "Go to the ant, thou sluggard; consider her ways, and be wise: Which having no guide, overseer, or ruler, provideth her meat in the summer, and gathereth her food in the harvest."),
    ("Luke 14:28 (KJV)", "For which of you, intending to build a tower, sitteth not down first, and counteth the cost, whether he have sufficient to finish it?"),
    ("Proverbs 22:7 (KJV)", "The rich ruleth over the poor, and the borrower is servant to the lender."),
    ("Proverbs 13:11 (KJV)", "Wealth gotten by vanity shall be diminished: but he that gathereth by labour shall increase."),
    ("1 Corinthians 4:2 (KJV)", "Moreover it is required in stewards, that a man be found faithful."),
    ("Ecclesiastes 11:1 (KJV)", "Cast thy bread upon the waters: for thou shalt find it after many days."),
    ("Galatians 6:9 (KJV)", "And let us not be weary in well doing: for in due season we shall reap, if we faint not."),
    ("Proverbs 10:4 (KJV)", "He becometh poor that dealeth with a slack hand: but the hand of the diligent maketh rich."),
    ("1 Timothy 6:6 (KJV)", "But godliness with contentment is great gain."),
    ("Hebrews 13:5 (KJV)", "Let your conversation be without covetousness; and be content with such things as ye have…"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# YEARLY CONFIG — everything that's specific to a given year lives here.
# Adding a new year going forward means adding a new dict entry, not
# rewriting app logic. Numbers you haven't finalized yet can stay at 0 —
# the app degrades gracefully to "Pending" / dashes rather than breaking.
# ═══════════════════════════════════════════════════════════════════════════════

YEARLY_CONFIG = {
    2026: {
        "carryover": {
            "total":      25400,
            "investment": 20000,
            "insurance":  5400,
            "note":       "Seed capital from 2025 savings",
            "year":       2025,
        },
        "fixed_insurance":   [0, 0, 0, 10800, 0, 0, 0, 0, 0, 5400, 0, 0],
        "fixed_investments": [0, 0, 0, 0, 0, 15000, 0, 0, 0, 0, 0, 0],
        "notes": [
            "Controller purchase • Insurance paid from 2025", "", "",
            "Insurance month paid early so ×2", "Stabilization",
            "End of 1H 2026 & Reinvest", "Mid-year insurance already paid back in April",
            "", "", "Insurance month", "", "Year-end surplus",
        ],
        "goals_config": [
            {"label": "PS5 Genshin Impact",  "desc": "Limited Edition Dual Sense Controller",      "target": 4900,  "icon": "🎮"},
            {"label": "Insurance Fund",       "desc": "₱21,600 for 4 months of insurance coverage", "target": 21600, "icon": "🛡️"},
            {"label": "Investment Target",    "desc": "₱60,000 across both BPI funds by Dec 2026",  "target": 60000, "icon": "📈"},
            {"label": "P.E.R.A",              "desc": "Retirement Fund",                             "target": 5000,  "icon": "🏦"},
        ],
        "milestones": [
            {"date": "Jan 2026",  "label": "Started 2026 with ₱25,400 carryover",      "icon": "🌱", "past": True},
            {"date": "Feb 2026",  "label": "First official portfolio snapshot recorded", "icon": "📸", "past": True},
            {"date": "May 2026",  "label": "Portfolio crossed ₱20,000 mark",            "icon": "🌿", "past": True},
            {"date": "Jun 2026",  "label": "First major reinvestment — ₱15,000",        "icon": "🚀", "past": True},
            {"date": "Sep 2026",  "label": "Turning 21 — credit card eligibility",      "icon": "🎂", "past": False},
            {"date": "Oct 2026",  "label": "Insurance month — plan ahead",              "icon": "🛡️", "past": False},
            {"date": "Dec 2026",  "label": "Year-end reinvestment + PERA planning",     "icon": "🏦", "past": False},
        ],
        "planned_investment_path": {
            "Jan": {"equity": 8000,  "bond": 12000},
            "Jun": {"equity": 20000, "bond": 15000},
        },
        "initial_snapshots": [
            {"date": "Feb", "us_equity": 8039.98, "bond_fund": 11952.97, "bond_income": 58.86, "pera_balance": 0.0, "pera_contributions": 0.0, "official": True,  "planned": False},
            {"date": "Mar", "us_equity": 7840.03, "bond_fund": 11809.68, "bond_income": 58.02, "pera_balance": 0.0, "pera_contributions": 0.0, "official": True,  "planned": False},
            {"date": "Apr", "us_equity": 7746.09, "bond_fund": 11921.25, "bond_income": 60.20, "pera_balance": 0.0, "pera_contributions": 0.0, "official": True,  "planned": False},
            {"date": "May", "us_equity": 8668.67, "bond_fund": 12185.95, "bond_income": 61.22, "pera_balance": 0.0, "pera_contributions": 0.0, "official": True,  "planned": False},
            {"date": "Jun", "us_equity": 0.0,     "bond_fund": 0.0,      "bond_income": 0.0,   "pera_balance": 0.0, "pera_contributions": 0.0, "official": False, "planned": True},
            {"date": "Jul", "us_equity": 0.0,     "bond_fund": 0.0,      "bond_income": 0.0,   "pera_balance": 0.0, "pera_contributions": 0.0, "official": False, "planned": False},
            {"date": "Aug", "us_equity": 0.0,     "bond_fund": 0.0,      "bond_income": 0.0,   "pera_balance": 0.0, "pera_contributions": 0.0, "official": False, "planned": False},
            {"date": "Sep", "us_equity": 0.0,     "bond_fund": 0.0,      "bond_income": 0.0,   "pera_balance": 0.0, "pera_contributions": 0.0, "official": False, "planned": False},
            {"date": "Oct", "us_equity": 0.0,     "bond_fund": 0.0,      "bond_income": 0.0,   "pera_balance": 0.0, "pera_contributions": 0.0, "official": False, "planned": False},
            {"date": "Nov", "us_equity": 0.0,     "bond_fund": 0.0,      "bond_income": 0.0,   "pera_balance": 0.0, "pera_contributions": 0.0, "official": False, "planned": False},
            {"date": "Dec", "us_equity": 0.0,     "bond_fund": 0.0,      "bond_income": 0.0,   "pera_balance": 0.0, "pera_contributions": 0.0, "official": False, "planned": True},
        ],
    },
    2027: {
        # Stub — fill this in properly once 2026 closes out. carryover.investment
        # and .insurance should be pulled from your actual Dec 2026 net worth.
        "carryover": {
            "total": 0, "investment": 0, "insurance": 0,
            "note": "Update after 2026 year-end close", "year": 2026,
        },
        "fixed_insurance":   [0] * 12,
        "fixed_investments": [0] * 12,
        "notes": [""] * 12,
        "goals_config": [
            {"label": "Emergency Fund", "desc": "Liquid reserve, phase-2 focus", "target": 30000, "icon": "🧯"},
            {"label": "P.E.R.A",        "desc": "Retirement Fund",              "target": 20000, "icon": "🏦"},
        ],
        "milestones": [],
        "planned_investment_path": {},
        "initial_snapshots": [],
    },
}

CURRENT_YEAR    = datetime.now().year
AVAILABLE_YEARS = sorted(YEARLY_CONFIG.keys())

# ── Year selector — placed in its own sidebar block so it renders first,
#    and so `selected_year` exists before any data is loaded below. ──
with st.sidebar:
    selected_year = st.selectbox(
        "📅 Viewing Year",
        AVAILABLE_YEARS,
        index=AVAILABLE_YEARS.index(CURRENT_YEAR) if CURRENT_YEAR in AVAILABLE_YEARS else len(AVAILABLE_YEARS) - 1,
    )

# ── Editor auth — anyone can view the dashboard, but the sidebar's edit
#    forms only unlock after the correct password is entered. The password
#    lives in st.secrets, never in code. ──
if "is_editor" not in st.session_state:
    st.session_state.is_editor = False

with st.sidebar:
    if st.session_state.is_editor:
        st.success("🔐 Administrator Access")
        if st.button("Lock edit mode", use_container_width=True):
            st.session_state.is_editor = False
            st.rerun()
    else:
        with st.expander("🔐 Administrator Access"):
            pw_attempt = st.text_input(
                "Password",
                type="password",
                key="edit_pw_attempt"
            )

        if st.button("Unlock", use_container_width=True):
            if pw_attempt == st.secrets["EDIT_PASSWORD"]:
                st.session_state.is_editor = True
                st.rerun()
            else:
                st.session_state.edit_pw_attempt = ""
                st.error("Incorrect password.")

cfg = YEARLY_CONFIG[selected_year]
CARRYOVER                = cfg["carryover"]
COST_BASIS                = CARRYOVER["investment"]   # derived, not hardcoded
FIXED_INSURANCE           = cfg["fixed_insurance"]
FIXED_INVESTMENTS         = cfg["fixed_investments"]
NOTES                     = cfg["notes"]
GOALS_CONFIG              = cfg["goals_config"]
MILESTONES                = cfg["milestones"]
PLANNED_INVESTMENT_PATH   = cfg["planned_investment_path"]
INITIAL_SNAPSHOTS         = cfg["initial_snapshots"]

# ═══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════════════════════

def fmt_value(val, prefix="₱", decimals=2):
    """Format a value, showing a clean empty state for zero."""
    if val == 0:
        return '<span class="empty-val">Pending</span>'
    fmt = f"{val:,.{decimals}f}"
    return f"{prefix}{fmt}"

def goal_status_label(pct):
    if pct == 0:
        return "not-started", "Your next step"
    elif pct < 50:
        return "inprogress", "In progress — keep going"
    elif pct < 100:
        return "almosthere", "Almost there — don't stop now"
    else:
        return "complete", "Goal achieved 🎉"

# ═══════════════════════════════════════════════════════════════════════════════
# SUPABASE — Load & Save (all year-scoped now)
# ═══════════════════════════════════════════════════════════════════════════════

def load_monthly_finance(year):
    try:
        rows = supabase.table("monthly_finance").select("*").eq("year", year).execute().data or []
    except Exception as e:
        st.error(f"Supabase load failed: {e}")
        rows = []

    income = {m: 0.0 for m in MONTHS}
    expenses = {m: 0.0 for m in MONTHS}

    for row in rows:
        month = row.get("month")
        if month in MONTHS:
            income[month] = float(row.get("income") or 0)
            expenses[month] = float(row.get("expenses") or 0)

    return {"income": income, "expenses": expenses}


finance = load_monthly_finance(selected_year)
income_map = finance["income"]
expenses_map = finance["expenses"]


def build_df():
    rows = []
    cum = 0

    for i, m in enumerate(MONTHS):
        inc = income_map.get(m, 0)
        exp = expenses_map.get(m, 0)

        ins = FIXED_INSURANCE[i]
        inv = FIXED_INVESTMENTS[i]

        net = inc - exp - inv - ins
        cum += net

        rows.append({
            "Month": m,
            "Insurance": ins,
            "Investments": inv,
            "Savings Deposited": inc,
            "Money Spent": exp,
            "Kept for Future": net,
            "Cumulative": cum,
        })

    return pd.DataFrame(rows)


def load_goals(year):
    try:
        rows = supabase.table("goals").select("*").eq("year", year).execute().data or []
    except Exception as e:
        st.error(f"Supabase load failed: {e}")
        rows = []

    data = {r["label"]: float(r["current_value"] or 0) for r in rows}

    for g in GOALS_CONFIG:
        if g["label"] not in data:
            data[g["label"]] = 0.0

    return data

goals = load_goals(selected_year)


def get_snap_date(x):
    return x.get("snapshot_date")


def load_snapshots(year):
    try:
        rows = supabase.table("investment_snapshots").select("*").eq("year", year).execute().data or []
    except Exception as e:
        st.error(f"Supabase load failed: {e}")
        rows = []

    return sorted(rows, key=lambda x: MONTH_INDEX.get(get_snap_date(x), 999))

goals_map = goals


def save_monthly(year, month, income, expenses):
    try:
        supabase.table("monthly_finance").upsert(
            {"year": year, "month": month, "income": income, "expenses": expenses},
            on_conflict="year,month"
        ).execute()
    except Exception as e:
        st.error(f"Save failed for {month} {year}: {e}")

snapshots = load_snapshots(selected_year)


def save_goal(year, label, current_value):
    try:
        g_cfg = next((g for g in GOALS_CONFIG if g["label"] == label), {})
        supabase.table("goals").upsert(
            {
                "year":          year,
                "label":         label,
                "current_value": current_value,
                "target_value":  g_cfg.get("target", 0),
                "description":   g_cfg.get("desc", ""),
                "icon":          g_cfg.get("icon", ""),
            },
            on_conflict="year,label"
        ).execute()
    except Exception as e:
        st.error(f"Save failed for goal {label}: {e}")


def save_snapshot(year, snap):
    try:
        supabase.table("investment_snapshots").upsert(
            {
                "year":                year,
                "snapshot_date":       snap["date"],
                "us_equity":           snap["us_equity"],
                "bond_fund":           snap["bond_fund"],
                "bond_income":         snap["bond_income"],
                "pera_balance":        snap.get("pera_balance", 0.0),
                "pera_contributions":  snap.get("pera_contributions", 0.0),
                "official":            snap["official"],
                "planned":             snap["planned"],
            },
            on_conflict="year,snapshot_date"
        ).execute()
    except Exception as e:
        st.error(f"Save failed for snapshot {snap['date']} {year}: {e}")


def delete_snapshot(year, date_label):
    try:
        supabase.table("investment_snapshots").delete().eq("year", year).eq("snapshot_date", date_label).execute()
    except Exception as e:
        st.error(f"Delete failed for {date_label}: {e}")


def reset_snapshots_in_db(year):
    try:
        supabase.table("investment_snapshots").delete().eq("year", year).execute()

        for s in INITIAL_SNAPSHOTS:
            supabase.table("investment_snapshots").insert({
                "year":               year,
                "snapshot_date":      get_snap_date(s),
                "us_equity":          s["us_equity"],
                "bond_fund":          s["bond_fund"],
                "bond_income":        s["bond_income"],
                "pera_balance":       s.get("pera_balance", 0.0),
                "pera_contributions": s.get("pera_contributions", 0.0),
                "official":           s["official"],
                "planned":            s["planned"],
            }).execute()

    except Exception as e:
        st.error(f"Reset failed: {e}")

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR (rest of it — year selector already rendered above)
# ═══════════════════════════════════════════════════════════════════════════════
if "verse" not in st.session_state:
    st.session_state.verse = random.choice(VERSES)

verse_data = st.session_state.verse
with st.sidebar:
    st.markdown("# This is for my future self")
    st.markdown(
        "<hr style='margin:6px 0;border:0;height:1px;background-color:#373F51;opacity:0.6;'>",
        unsafe_allow_html=True,
    )
    st.caption(f"📱 Scroll down for full dashboard on mobile · Viewing {selected_year}")

    # ── Goals ──
    st.markdown("### 🎯 Goals")
    with st.expander("Update Goals", expanded=False):
        with st.form(f"goals_form_{selected_year}"):
            for g in GOALS_CONFIG:
                label = g["label"]
                step  = 5400.0 if label == "Insurance Fund" else 1000.0 if label == "Investment Target" else 100.0
                st.number_input(
                    f"{g['icon']} {label}",
                    min_value=0.0, max_value=float(g["target"] * 2),
                    value=goals.get(label, 0.0), step=step, format="%.0f",
                    key=f"goal_{label}_{selected_year}",
                    help=g["desc"],
                    disabled=not st.session_state.is_editor,
                )
            if not st.session_state.is_editor:
                st.caption("🔒 Unlock edit mode to save changes")
            if st.form_submit_button("Save Goals", use_container_width=True, disabled=not st.session_state.is_editor):
                for g in GOALS_CONFIG:
                    new_val = st.session_state[f"goal_{g['label']}_{selected_year}"]
                    if new_val != goals[g["label"]]:
                        goals[g["label"]] = new_val
                        save_goal(selected_year, g["label"], new_val)
                st.success("Goals saved!")
                st.rerun()

    # ── Income ──
    st.markdown("### 🏦 Savings Deposited")
    with st.expander("Monthly Deposits", expanded=False):
        with st.form(f"income_form_{selected_year}"):
            for m in MONTHS:
                st.number_input(m, 0.0, 50000.0, income_map[m], 500.0,
                                key=f"income_{m}_{selected_year}",
                                help=f"Total cash you set aside in {m} {selected_year}",
                                disabled=not st.session_state.is_editor)
            if not st.session_state.is_editor:
                st.caption("🔒 Unlock edit mode to save changes")
            if st.form_submit_button("Save Deposits", use_container_width=True, disabled=not st.session_state.is_editor):
                for m in MONTHS:
                    new_inc = st.session_state[f"income_{m}_{selected_year}"]
                    if new_inc != income_map[m]:
                        income_map[m] = new_inc
                        save_monthly(selected_year, m, new_inc, expenses_map[m])
                st.success("Deposits saved!")
                st.rerun()

    # ── Expenses ──
    st.markdown("### 💸 Money Spent")
    with st.expander("Monthly Expenses", expanded=False):
        with st.form(f"expenses_form_{selected_year}"):
            for m in MONTHS:
                st.number_input(m, 0.0, 50000.0, expenses_map[m], 500.0,
                                key=f"expense_{m}_{selected_year}",
                                help=f"Total spent in {m} {selected_year} (excluding insurance & investments)",
                                disabled=not st.session_state.is_editor)
            if not st.session_state.is_editor:
                st.caption("🔒 Unlock edit mode to save changes")
            if st.form_submit_button("Save Expenses", use_container_width=True, disabled=not st.session_state.is_editor):
                for m in MONTHS:
                    new_exp = st.session_state[f"expense_{m}_{selected_year}"]
                    if new_exp != expenses_map[m]:
                        expenses_map[m] = new_exp
                        save_monthly(selected_year, m, income_map[m], new_exp)
                st.success("Expenses saved!")
                st.rerun()

    # ── Investment Snapshots ──
    st.markdown("### 📸 Portfolio Snapshots")
    with st.expander("Add Snapshot", expanded=False):
        with st.form(f"add_snap_form_{selected_year}"):
            snap_date    = st.text_input("Month label (e.g. Jun)", key=f"snap_date_{selected_year}",
                                         help="Use the 3-letter month abbreviation",
                                         disabled=not st.session_state.is_editor)
            snap_equity  = st.number_input("US Equity Feeder (₱)",  0.0, value=0.0, step=10.0, format="%.2f", key=f"snap_eq_{selected_year}", disabled=not st.session_state.is_editor)
            snap_bond    = st.number_input("Global Bond Fund (₱)",   0.0, value=0.0, step=10.0, format="%.2f", key=f"snap_bond_{selected_year}", disabled=not st.session_state.is_editor)
            snap_bincome = st.number_input("Bond Income received (₱)", 0.0, value=0.0, step=1.0, format="%.2f", key=f"snap_bi_{selected_year}", disabled=not st.session_state.is_editor)
            snap_pera_bal = st.number_input("PERA Balance (₱)", 0.0, value=0.0, step=10.0, format="%.2f", key=f"snap_pera_bal_{selected_year}",
                                            help="Total PERA account value as of this snapshot",
                                            disabled=not st.session_state.is_editor)
            snap_pera_ctr = st.number_input("PERA Contribution this snapshot (₱)", 0.0, value=0.0, step=100.0, format="%.2f", key=f"snap_pera_ctr_{selected_year}",
                                            help="New money put into PERA since your last snapshot",
                                            disabled=not st.session_state.is_editor)
            snap_official = st.checkbox("✦ Mark as Official (verified from BPI app)", key=f"snap_official_{selected_year}", disabled=not st.session_state.is_editor)
            snap_planned  = st.checkbox("⏳ Mark as Planned (future projection)",     key=f"snap_planned_{selected_year}", disabled=not st.session_state.is_editor)
            if not st.session_state.is_editor:
                st.caption("🔒 Unlock edit mode to save changes")
            if st.form_submit_button("Add Snapshot", use_container_width=True, disabled=not st.session_state.is_editor):
                if snap_date:
                    new_snap = {
                        "date": snap_date, "us_equity": snap_equity,
                        "bond_fund": snap_bond, "bond_income": snap_bincome,
                        "pera_balance": snap_pera_bal, "pera_contributions": snap_pera_ctr,
                        "official": snap_official, "planned": snap_planned,
                    }
                    existing_dates = [get_snap_date(s) for s in snapshots]
                    if snap_date in existing_dates:
                        snapshots[existing_dates.index(snap_date)] = new_snap
                    else:
                        snapshots.append(new_snap)
                    snapshots.sort(key=lambda x: MONTH_INDEX.get(get_snap_date(x), 999))
                    save_snapshot(selected_year, new_snap)
                    st.success(f"Snapshot saved: {snap_date}")
                    st.rerun()

    with st.expander("Edit / Delete Snapshot", expanded=False):
        if snapshots:
            snap_labels = [get_snap_date(s) for s in snapshots]
            edit_date   = st.selectbox("Select snapshot to edit", snap_labels, key=f"edit_select_{selected_year}")
            edit_idx    = snap_labels.index(edit_date)
            s           = snapshots[edit_idx]
            with st.form(f"edit_snap_form_{selected_year}"):
                e_eq  = st.number_input("US Equity (₱)",    value=float(s["us_equity"]),   step=10.0, format="%.2f", key=f"e_eq_{selected_year}", disabled=not st.session_state.is_editor)
                e_bf  = st.number_input("Bond Fund (₱)",    value=float(s["bond_fund"]),   step=10.0, format="%.2f", key=f"e_bf_{selected_year}", disabled=not st.session_state.is_editor)
                e_bi  = st.number_input("Bond Income (₱)",  value=float(s["bond_income"]), step=1.0,  format="%.2f", key=f"e_bi_{selected_year}", disabled=not st.session_state.is_editor)
                e_pb  = st.number_input("PERA Balance (₱)", value=float(s.get("pera_balance", 0.0)), step=10.0, format="%.2f", key=f"e_pb_{selected_year}", disabled=not st.session_state.is_editor)
                e_pc  = st.number_input("PERA Contribution (₱)", value=float(s.get("pera_contributions", 0.0)), step=100.0, format="%.2f", key=f"e_pc_{selected_year}", disabled=not st.session_state.is_editor)
                e_off = st.checkbox("✦ Official", value=s["official"], key=f"e_official_{selected_year}", disabled=not st.session_state.is_editor)
                e_pln = st.checkbox("⏳ Planned",  value=s["planned"],  key=f"e_planned_{selected_year}", disabled=not st.session_state.is_editor)
                if not st.session_state.is_editor:
                    st.caption("🔒 Unlock edit mode to save changes")
                col1, col2 = st.columns(2)
                with col1:
                    save_btn = st.form_submit_button("Save", use_container_width=True, disabled=not st.session_state.is_editor)
                with col2:
                    del_btn = st.form_submit_button("Delete", use_container_width=True, disabled=not st.session_state.is_editor)

            if save_btn:
                updated = {"date": edit_date, "us_equity": e_eq, "bond_fund": e_bf,
                           "bond_income": e_bi, "pera_balance": e_pb, "pera_contributions": e_pc,
                           "official": e_off, "planned": e_pln}
                snapshots[edit_idx] = updated
                save_snapshot(selected_year, updated)
                st.success("Saved!")
                st.rerun()

            if del_btn:
                delete_snapshot(selected_year, edit_date)
                snapshots.pop(edit_idx)
                st.success(f"Deleted: {edit_date}")
                st.rerun()

        if not st.session_state.is_editor:
            st.caption("🔒 Unlock edit mode to reset snapshots")
        if st.button("↺ Reset All Snapshots to Defaults", use_container_width=True, key=f"reset_snaps_{selected_year}", disabled=not st.session_state.is_editor):
            reset_snapshots_in_db(selected_year)
            snapshots = [s.copy() for s in INITIAL_SNAPSHOTS]
            snapshots.sort(key=lambda x: MONTH_INDEX.get(get_snap_date(x), 999))
            st.success("Snapshots reset.")
            st.rerun()

    # ── Verse ──
    st.markdown("---")
    ref, verse = st.session_state.verse
    st.caption(f"**{ref}**  \n*{verse}*")
    st.caption(
        "Earn wisely. Give faithfully. Your money is a tool, not a treasure. "
        "Use it to build the life you want and to bless others along the way. "
        "May you be guided by Jesus Christ. God will provide, and He will always provide more than enough."
    )


# fix if anything weird gets stored
if not isinstance(verse_data, (list, tuple)) or len(verse_data) != 2:
    verse_data = random.choice(VERSES)
    st.session_state.verse = verse_data

ref, verse = verse_data

# ═══════════════════════════════════════════════════════════════════════════════
# BUILD DATA
# ═══════════════════════════════════════════════════════════════════════════════

baseline_df = build_df()

total_income      = baseline_df["Savings Deposited"].sum()
total_investments = baseline_df["Investments"].sum()
total_expenses    = baseline_df["Money Spent"].sum()
end_cumulative    = baseline_df["Cumulative"].iloc[-1]
best_month        = baseline_df.loc[baseline_df["Kept for Future"].idxmax(), "Month"]
worst_month       = baseline_df.loc[baseline_df["Kept for Future"].idxmin(), "Month"]
neg_months        = baseline_df[baseline_df["Kept for Future"] < 0]["Month"].tolist()
floor_months      = [
    m for m in MONTHS
    if income_map[m] - expenses_map[m] < SAVINGS_FLOOR and income_map[m] > 0
]

bond_income_ytd  = sum(s["bond_income"] for s in snapshots)
invest_vs_save   = (total_investments / total_income * 100) if total_income else 0
savings_rate_ytd = ((total_income - total_expenses) / total_income * 100) if total_income else 0

# ── Investment P&L ──
actual_snaps = sorted(
    [s for s in snapshots if s["official"] and s["us_equity"] > 0],
    key=lambda x: MONTH_INDEX.get(get_snap_date(x), 999),
)
latest_snap   = actual_snaps[-1] if actual_snaps else None
latest_equity = latest_snap["us_equity"] if latest_snap else 0
latest_bond   = latest_snap["bond_fund"]  if latest_snap else 0
portfolio_val = latest_equity + latest_bond

# Cost basis split: prior-year carryover + this year's lump sum
cost_basis_prior  = CARRYOVER["investment"]
cost_basis_thisyr = total_investments
total_cost_basis  = cost_basis_prior + cost_basis_thisyr

unrealized_pnl = portfolio_val - total_cost_basis
realized_pnl   = bond_income_ytd
net_pnl        = unrealized_pnl + realized_pnl

# Portfolio allocation %
equity_pct = (latest_equity / portfolio_val * 100) if portfolio_val else 0
bond_pct   = (latest_bond   / portfolio_val * 100) if portfolio_val else 0

# Simple net worth estimate (PERA excluded — it's locked/retirement money,
# tracked separately below rather than folded into liquid net worth)
net_worth = portfolio_val + bond_income_ytd + end_cumulative

# ── PERA ──
latest_pera_balance   = latest_snap.get("pera_balance", 0.0) if latest_snap else 0.0
pera_contributions_ytd = sum(s.get("pera_contributions", 0.0) for s in snapshots)
pera_cap_pct = min(pera_contributions_ytd / PERA_CONTRIBUTION_CAP * 100, 100) if PERA_CONTRIBUTION_CAP else 0

# ── Wealth Growth Metrics ──────────────────────────────────────────

STARTING_WEALTH = CARRYOVER["investment"]

wealth_growth_rate = (
    (net_worth - STARTING_WEALTH) / STARTING_WEALTH * 100
    if STARTING_WEALTH else 0
)

investment_growth_rate = (
    (portfolio_val - total_cost_basis) / total_cost_basis * 100
    if total_cost_basis else 0
)

net_worth_growth_rate = (
    (net_worth - CARRYOVER["total"]) / CARRYOVER["total"] * 100
    if CARRYOVER["total"] else 0
)

growth_label = "kpi-pos" if wealth_growth_rate >= 0 else "kpi-neg"

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE HEADER
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown(
    f'<div style="text-align:center;padding:16px 0 4px 0;">'
    f'<span style="font-family:Lora,serif;color:#0B3954;font-size:24px;font-weight:600;">'
    f'{selected_year} Financial Overview</span></div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div style="text-align:center;color:#D0ADA7;font-size:11px;letter-spacing:2.5px;'
    'text-transform:uppercase;margin-bottom:24px;">Blessed to give, not hoard.</div>',
    unsafe_allow_html=True,
)

# ═══════════════════════════════════════════════════════════════════════════════
# KPI ROW — TIER 1: Operational
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown('<div class="section-header">📋 This Year So Far</div>', unsafe_allow_html=True)

c1, c2, c3, c4, c5 = st.columns(5)
kpis_t1 = [
    (c1, "Savings Deposited",  f"₱{total_income:,.0f}",      "Total set aside",            False),
    (c2, "Money Spent",        f"₱{total_expenses:,.0f}",     "All personal outflows",      False),
    (c3, "Savings Rate",       f"{savings_rate_ytd:.1f}%",    "Income kept after expenses", False),
    (c4, "Kept for Future",    f"₱{end_cumulative:,.0f}",     "Year-end running total",     end_cumulative < 0),
    (c5, "Passive Provision",  f"₱{bond_income_ytd:,.2f}",   "Bond income received",       False),
]
for col, label, val, sub, is_neg in kpis_t1:
    with col:
        st.markdown(f"""
        <div class="kpi-card">
          <div class="kpi-label">{label}</div>
          <div class="kpi-value {'kpi-neg' if is_neg else 'kpi-pos'}">{val}</div>
          <div class="kpi-sub">{sub}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# KPI ROW — TIER 2: Wealth
c6, c7, c8, c9, c10 = st.columns(5)
kpis_t2 = [
    (c6, "Portfolio Value",    f"₱{portfolio_val:,.2f}"  if portfolio_val else "—",  "US Equity + Bond Fund",     False),
    (c7, "Unrealized G/L",    f"{'+'if unrealized_pnl>=0 else ''}₱{unrealized_pnl:,.2f}", "vs total cost basis", unrealized_pnl < 0),
    (c8, "Net P&L",           f"{'+'if net_pnl>=0 else ''}₱{net_pnl:,.2f}",         "incl. bond income",         net_pnl < 0),
    (c9, "Est. Net Worth",    f"₱{net_worth:,.0f}",                                  "Portfolio + savings",       False),
    (c10, "Wealth Growth Rate",  f"{investment_growth_rate:.1f}%",  "Realized + unrealized portfolio growth", investment_growth_rate < 0)
]
for col, label, val, sub, is_neg in kpis_t2:
    with col:
        st.markdown(f"""
        <div class="kpi-card">
          <div class="kpi-label">{label}</div>
          <div class="kpi-value {'kpi-neg' if is_neg else 'kpi-pos'}">{val}</div>
          <div class="kpi-sub">{sub}</div>
        </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PERA — RETIREMENT TRACKING
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown('<div class="section-header">🏦 P.E.R.A — Retirement Tracking</div>', unsafe_allow_html=True)
p1, p2, p3 = st.columns(3)
with p1:
    st.markdown(f"""
    <div class="kpi-card">
      <div class="kpi-label">PERA Balance</div>
      <div class="kpi-value kpi-pos">{fmt_value(latest_pera_balance)}</div>
      <div class="kpi-sub">Locked until retirement — tracked separately from net worth</div>
    </div>""", unsafe_allow_html=True)
with p2:
    st.markdown(f"""
    <div class="kpi-card">
      <div class="kpi-label">Contributions This Year</div>
      <div class="kpi-value kpi-pos">{fmt_value(pera_contributions_ytd)}</div>
      <div class="kpi-sub">{pera_cap_pct:.0f}% of ₱{PERA_CONTRIBUTION_CAP:,} annual cap</div>
    </div>""", unsafe_allow_html=True)
with p3:
    st.markdown(f"""
    <div class="kpi-card" style="text-align:left;">
      <div class="kpi-label" style="text-align:center;">Cap Progress</div>
      <div class="goal-bar-bg" style="margin-top:10px;"><div class="goal-bar-fill" style="width:{pera_cap_pct:.1f}%;"></div></div>
      <div class="goal-numbers"><span>₱{pera_contributions_ytd:,.0f}</span><span>₱{PERA_CONTRIBUTION_CAP:,.0f}</span></div>
    </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# CAPITAL ORIGIN + MILESTONE STRIP
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown('<div class="section-header">🌱 Capital Origin & Milestones</div>', unsafe_allow_html=True)
col_orig, col_ms = st.columns([1, 2])

with col_orig:
    alloc_pct_prior  = (cost_basis_prior / total_cost_basis * 100) if total_cost_basis else 0
    alloc_pct_thisyr = (cost_basis_thisyr / total_cost_basis * 100) if total_cost_basis else 0
    st.markdown(f"""
    <div class="capital-card">
      <div class="kpi-label" style="margin-bottom:12px;">Where your investments came from</div>

      <div class="capital-row">
        <div>
          <div style="color:#373F51;font-size:13px;font-weight:500;">{CARRYOVER['year']} Carryover</div>
          <div class="capital-note">{CARRYOVER['note']}</div>
        </div>
        <div style="text-align:right;">
          <div class="capital-amount">₱{cost_basis_prior:,.0f}</div>
          <div class="capital-source">{alloc_pct_prior:.0f}% of basis</div>
        </div>
      </div>

      <div class="capital-row">
        <div>
          <div style="color:#373F51;font-size:13px;font-weight:500;">{CARRYOVER['year']} → Insurance Reserve</div>
          <div class="capital-note">Carried into early-year coverage</div>
        </div>
        <div style="text-align:right;">
          <div class="capital-amount">₱{CARRYOVER['insurance']:,.0f}</div>
          <div class="capital-source">Separate from investments</div>
        </div>
      </div>

      <div class="capital-row">
        <div>
          <div style="color:#373F51;font-size:13px;font-weight:500;">{selected_year} Operating Investments</div>
          <div class="capital-note">From this year's income</div>
        </div>
        <div style="text-align:right;">
          <div class="capital-amount">₱{cost_basis_thisyr:,.0f}</div>
          <div class="capital-source">{alloc_pct_thisyr:.0f}% of basis</div>
        </div>
      </div>

      <div class="capital-row" style="margin-top:4px;">
        <div style="color:#0B3954;font-size:13px;font-weight:600;">Total Cost Basis</div>
        <div class="capital-amount">₱{total_cost_basis:,.0f}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

with col_ms:
    if MILESTONES:
        ms_cards = ""
        for m in MILESTONES:
            cls = "milestone-past" if m["past"] else "milestone-future"
            ms_cards += f"""
            <div class="milestone-card {cls}">
              <div class="milestone-icon">{m['icon']}</div>
              <div class="milestone-date">{m['date']}</div>
              <div class="milestone-label">{m['label']}</div>
            </div>"""
        st.markdown(f'<div class="milestone-strip">{ms_cards}</div>', unsafe_allow_html=True)
    else:
        st.info(f"No milestones logged for {selected_year} yet — add them to YEARLY_CONFIG as the year unfolds.")

# ═══════════════════════════════════════════════════════════════════════════════
# GOALS
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown('<div class="section-header">🎯 Goals</div>', unsafe_allow_html=True)
goal_cols = st.columns(len(GOALS_CONFIG)) if GOALS_CONFIG else []
for idx, g in enumerate(GOALS_CONFIG):
    current_val = goals_map.get(g["label"], 0)
    target_val  = g["target"]
    pct         = min(current_val / target_val * 100, 100) if target_val else 0
    status_key, status_text = goal_status_label(pct)
    with goal_cols[idx]:
        st.markdown(f"""
        <div class="goal-card">
          <div class="goal-title">{g['icon']} {g['label']}</div>
          <div class="goal-meta">{g['desc']}</div>
          <span class="goal-pct">{pct:.0f}%</span>
          <div class="goal-bar-bg"><div class="goal-bar-fill" style="width:{pct:.1f}%;"></div></div>
          <div class="goal-numbers"><span>₱{current_val:,.0f}</span><span>₱{target_val:,.0f}</span></div>
          <div class="goal-status goal-status-{status_key}">{status_text}</div>
        </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# CASH FLOW CHARTS
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown('<div class="section-header">📊 Cash Flow</div>', unsafe_allow_html=True)
col_a, col_b = st.columns([3, 2])

with col_a:
    fig = go.Figure()
    fig.add_bar(x=baseline_df["Month"], y=baseline_df["Savings Deposited"],
                name="Savings Deposited", marker_color="#6EA4BF", opacity=0.85)
    fig.add_bar(x=baseline_df["Month"],
                y=baseline_df["Insurance"] + baseline_df["Investments"] + baseline_df["Money Spent"],
                name="Total Outflow", marker_color="#D0ADA7", opacity=0.80)
    fig.add_scatter(x=baseline_df["Month"], y=baseline_df["Kept for Future"],
                    name="Kept for Future", mode="lines+markers",
                    line=dict(color="#0B3954", width=2.5),
                    marker=dict(size=8, color=["#b05555" if v < 0 else "#0B3954"
                                               for v in baseline_df["Kept for Future"]]))
    layout = base_layout("Monthly Deposits vs Outflow vs Net", 340)
    layout["barmode"] = "group"
    fig.update_layout(**layout)
    fig.update_xaxes(showgrid=False, color=TEXT)
    fig.update_yaxes(showgrid=True, gridcolor=GRID, color=SUBTEXT, tickprefix="₱", tickformat=",")
    st.plotly_chart(fig, use_container_width=True)

with col_b:
    fig2 = go.Figure(go.Pie(
        labels=["Savings Deposited", "Total Insurance Coverage", "Invested", "Money Spent"],
        values=[
            total_income,
            sum(FIXED_INSURANCE) + CARRYOVER["insurance"],
            total_investments,
            total_expenses
        ],
        hole=0.55,
        marker_colors=["#6EA4BF", "#D0ADA7", "#0B3954", "#E8D6CB"],
        textinfo="label+percent",
        textfont_size=11,
    ))

    fig2.update_layout(**base_layout("Annual Allocation Breakdown", 340))
    fig2.update_layout(showlegend=False)

    st.plotly_chart(fig2, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SAVINGS & INVESTMENT GROWTH
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown('<div class="section-header">📈 Savings & Investment Growth</div>', unsafe_allow_html=True)
col_c, col_d = st.columns([3, 2])

with col_c:
    fig3 = go.Figure()
    fig3.add_scatter(x=baseline_df["Month"], y=baseline_df["Cumulative"],
                     name="Cumulative", mode="lines+markers",
                     line=dict(color="#0B3954", width=2.5),
                     marker=dict(size=8, color="#6EA4BF"),
                     fill="tozeroy", fillcolor="rgba(110,164,191,0.10)")
    fig3.add_hline(y=0, line_color="#D0ADA7", line_dash="dot", line_width=1.5)
    fig3.update_layout(**base_layout("Cumulative Savings Growth", 320))
    fig3.update_xaxes(showgrid=False, color=TEXT)
    fig3.update_yaxes(showgrid=True, gridcolor=GRID, color=SUBTEXT, tickprefix="₱", tickformat=",")
    st.plotly_chart(fig3, use_container_width=True)

with col_d:
    snap_sorted   = sorted(snapshots, key=lambda x: MONTH_INDEX.get(get_snap_date(x), 999))
    actual_months = [get_snap_date(s)     for s in snap_sorted if s["us_equity"] > 0]
    actual_eq     = [s["us_equity"] for s in snap_sorted if s["us_equity"] > 0]
    actual_bd     = [s["bond_fund"] for s in snap_sorted if s["us_equity"] > 0]

    fig4 = go.Figure()
    fig4.add_bar(x=MONTHS,
                 y=[PLANNED_INVESTMENT_PATH.get(m, {}).get("equity", 0) for m in MONTHS],
                 name="Planned Equity", marker_color="#6EA4BF", opacity=0.35)
    fig4.add_bar(x=MONTHS,
                 y=[PLANNED_INVESTMENT_PATH.get(m, {}).get("bond", 0) for m in MONTHS],
                 name="Planned Bond", marker_color="#0B3954", opacity=0.25)
    fig4.add_scatter(x=actual_months,
                     y=[e + b for e, b in zip(actual_eq, actual_bd)],
                     name="Actual Total", mode="lines+markers",
                     line=dict(width=2, color="#D0ADA7"), marker=dict(size=7))
    fig4.update_layout(**base_layout("Planned vs Actual Portfolio", 320))
    fig4.update_xaxes(showgrid=False, color=TEXT)
    fig4.update_yaxes(showgrid=True, gridcolor=GRID, color=SUBTEXT, tickprefix="₱", tickformat=",")
    st.plotly_chart(fig4, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# INVESTMENT TRACKER
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown('<div class="section-header">📸 Portfolio Snapshots</div>', unsafe_allow_html=True)
col_e, col_f = st.columns([3, 2])

with col_e:
    total_snap_income = sum(s["bond_income"] for s in snapshots)
    rows_html = ""
    for s in snapshots:
        row_total  = s["us_equity"] + s["bond_fund"]
        unreal     = row_total - total_cost_basis if row_total > 0 else 0
        unreal_cls = "val-pos" if unreal > 0 else ("val-neg" if unreal < 0 else "val-zero")
        unreal_str = (f"+₱{unreal:,.2f}" if unreal > 0 else f"₱{unreal:,.2f}") if row_total > 0 else '<span class="empty-val">Pending</span>'
        badge      = '<span class="badge-official">✦ Official</span>' if s["official"] else ('<span class="badge-planned">⏳ Planned</span>' if s["planned"] else "")
        row_cls    = "snap-official" if s["official"] else ("snap-planned" if s["planned"] else "")
        eq_str  = fmt_value(s["us_equity"])
        bf_str  = fmt_value(s["bond_fund"])
        tt_str  = fmt_value(row_total) if row_total > 0 else '<span class="empty-val">Pending</span>'
        bi_str  = fmt_value(s["bond_income"])
        pb_str  = fmt_value(s.get("pera_balance", 0.0))
        rows_html += (
            f"<tr class='{row_cls}'><td>{get_snap_date(s)}{badge}</td><td>{eq_str}</td>"
            f"<td>{bf_str}</td><td>{tt_str}</td><td class='{unreal_cls}'>{unreal_str}</td>"
            f"<td>{bi_str}</td><td>{pb_str}</td></tr>"
        )

    rows_html += f"<tr class='snap-total-row'><td>TOTAL BOND INCOME / LATEST PERA</td><td>—</td><td>—</td><td>—</td><td>—</td><td>₱{total_snap_income:.2f}</td><td>{fmt_value(latest_pera_balance)}</td></tr>"
    st.markdown(f"""
    <div style="background:#fff;border:1px solid #E8D6CB;border-radius:14px;overflow:hidden;box-shadow:0 2px 8px rgba(55,63,81,0.05);">
      <table class="snap-table">
        <thead><tr>
          <th>Date</th><th>US Equity Feeder</th><th>Global Bond</th>
          <th>Total</th><th>Unrealized G/L</th><th>Bond Income</th><th>PERA Balance</th>
        </tr></thead>
        <tbody>{rows_html}</tbody>
      </table>
    </div>""", unsafe_allow_html=True)

    st.caption("✦ Official = verified from BPI app   ⏳ Planned = future projection   G/L uses total cost basis (carryover + this year's investments). PERA tracked separately since it's locked until retirement.")

with col_f:
    if actual_snaps:
        dates_a = [get_snap_date(s)      for s in actual_snaps]
        eq_a    = [s["us_equity"]  for s in actual_snaps]
        bf_a    = [s["bond_fund"]  for s in actual_snaps]
        tot_a   = [e + b for e, b in zip(eq_a, bf_a)]

        fig_snap = go.Figure()
        fig_snap.add_bar(x=dates_a, y=eq_a, name="US Equity", marker_color="#6EA4BF", opacity=0.9)
        fig_snap.add_bar(x=dates_a, y=bf_a, name="Bond Fund", marker_color="#0B3954", opacity=0.9)
        fig_snap.add_scatter(x=dates_a, y=tot_a, name="Total", mode="lines+markers",
                             line=dict(color="#D0ADA7", width=2, dash="dot"),
                             marker=dict(size=7, color="#D0ADA7"))
        layout_snap = base_layout("Actual Portfolio Snapshots", 240)
        layout_snap["barmode"] = "stack"
        fig_snap.update_layout(**layout_snap)
        fig_snap.update_xaxes(showgrid=False, color=TEXT)
        fig_snap.update_yaxes(showgrid=True, gridcolor=GRID, color=SUBTEXT, tickprefix="₱", tickformat=",")
        st.plotly_chart(fig_snap, use_container_width=True)
    else:
        st.info("Add official snapshots to see the portfolio chart.")

    # Portfolio allocation
    if portfolio_val > 0:
        fig_alloc = go.Figure(go.Pie(
            labels=["US Equity Feeder", "Global Bond Fund"],
            values=[latest_equity, latest_bond],
            hole=0.6,
            marker_colors=["#6EA4BF", "#0B3954"],
            textinfo="label+percent", textfont_size=10,
        ))
        fig_alloc.update_layout(**base_layout("Portfolio Allocation", 200))
        fig_alloc.update_layout(showlegend=False, margin=dict(l=10,r=10,t=40,b=10))
        st.plotly_chart(fig_alloc, use_container_width=True)

    st.markdown(f"""
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:8px;">
      <div class="kpi-card" style="padding:14px 12px;">
        <div class="kpi-label">Unrealized G/L</div>
        <div class="kpi-value {'kpi-neg' if unrealized_pnl < 0 else 'kpi-pos'}" style="font-size:20px;">
          {'+'if unrealized_pnl>=0 else ''}₱{unrealized_pnl:,.2f}</div>
        <div class="kpi-sub">vs ₱{total_cost_basis:,} basis</div>
      </div>
      <div class="kpi-card" style="padding:14px 12px;">
        <div class="kpi-label">Net P&L</div>
        <div class="kpi-value {'kpi-neg' if net_pnl < 0 else 'kpi-pos'}" style="font-size:20px;">
          {'+'if net_pnl>=0 else ''}₱{net_pnl:,.2f}</div>
        <div class="kpi-sub">unrealized + bond income</div>
      </div>
    </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# MONTHLY TRACKER TABLE
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown('<div class="section-header">📋 Monthly Tracker</div>', unsafe_allow_html=True)
tracker_df = pd.DataFrame([
    {
        "Month": m,
        "Insurance": FIXED_INSURANCE[i],
        "Investments": FIXED_INVESTMENTS[i],
        "Savings Deposited": income_map[m],
        "Money Spent": expenses_map[m],
        "Kept for Future": income_map[m] - expenses_map[m] - FIXED_INVESTMENTS[i]
                           - FIXED_INSURANCE[i],
        "Notes": NOTES[i],
    }
    for i, m in enumerate(MONTHS)
])
tracker_df["Cumulative"] = tracker_df["Kept for Future"].cumsum()
for col in ["Insurance","Investments","Savings Deposited","Money Spent","Kept for Future","Cumulative"]:
    tracker_df[col] = tracker_df[col].apply(lambda x: f"₱{x:,.0f}")

def highlight_negative(row):
    net_val = int(row["Kept for Future"].replace("₱","").replace(",",""))
    return (["background-color:#fdf3f0;color:#8c3a3a"] * len(row)) if net_val < 0 else ([""] * len(row))

st.dataframe(
    tracker_df.style.apply(highlight_negative, axis=1),
    use_container_width=True, hide_index=True, height=460,
)

# ═══════════════════════════════════════════════════════════════════════════════
# INSIGHTS
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown('<div class="section-header">🔍 Insights</div>', unsafe_allow_html=True)
col_g, col_h = st.columns(2)

with col_g:
    st.markdown("**Cash Flow**")
    st.markdown(f'<div class="insight-pos">🏆 Best month: <b>{best_month}</b></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="insight-neg">⚠️ Toughest month: <b>{worst_month}</b></div>', unsafe_allow_html=True)
    if neg_months:
        st.markdown(f'<div class="insight-neg">🔴 Months in the red: <b>{", ".join(neg_months)}</b></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="insight-pos">✅ No negative months this year</div>', unsafe_allow_html=True)
    if floor_months:
        st.markdown(f'<div class="insight-neg">⚡ Below ₱{SAVINGS_FLOOR:,} floor: <b>{", ".join(floor_months)}</b></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="insight-neu">📊 Savings rate: <b>{savings_rate_ytd:.1f}%</b> of income kept</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="insight-neu">💹 Investment ratio: <b>{invest_vs_save:.1f}%</b> of deposits</div>', unsafe_allow_html=True)

with col_h:
    st.markdown("**Investments & Passive Income**")
    st.markdown(f'<div class="insight-pos">💸 Passive provision so far: <b>₱{bond_income_ytd:,.2f}</b></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="insight-neu">📈 {selected_year} investments deployed: <b>₱{total_investments:,.0f}</b></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="insight-neu">🌱 {CARRYOVER["year"]} carryover invested: <b>₱{cost_basis_prior:,.0f}</b></div>', unsafe_allow_html=True)
    if portfolio_val > 0:
        st.markdown(f'<div class="insight-neu">🥧 Allocation: <b>{equity_pct:.0f}% equity / {bond_pct:.0f}% bond</b></div>', unsafe_allow_html=True)
        months_of_expenses = (bond_income_ytd / (total_expenses / 12)) if total_expenses > 0 else 0
        st.markdown(f'<div class="insight-pos">📅 Bond income covers ~<b>{months_of_expenses:.1f} months</b> of avg expenses</div>', unsafe_allow_html=True)
    if pera_contributions_ytd > 0:
        st.markdown(f'<div class="insight-neu">🏦 PERA contributions: <b>₱{pera_contributions_ytd:,.0f}</b> ({pera_cap_pct:.0f}% of cap)</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="insight-neu">💰 Net P&L: <b>{"+" if net_pnl >= 0 else ""}₱{net_pnl:,.2f}</b></div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("---")
st.markdown(f"""
> *"Keiza, this year you're building on ₱{CARRYOVER['total']:,.0f} carried over from {CARRYOVER['year']} —
> money you earned while studying, serving, and trusting God for provision. Every peso here is a testimony.
> Keep building. Keep giving. Keep the faith."*
""")
st.caption(
    "Remember Keiza: you're saving up for your future. It'll be hard, there will be times "
    "when you want to spend your hard-earned money — but think about your future self. "
    "You want to provide for your family, give generously, and enjoy the fruits of your labor "
    "without worry. Stay disciplined. Stay focused. Keep your eyes on the prize. "
    "But never forget that money is replaceable — prioritize your present self when worse comes to worst. "
    "God will provide, and He will always provide more than enough."
)
st.markdown(
    f'<div style="text-align:center;color:#D0ADA7;font-size:11px;letter-spacing:1px;">'
    f'Built by Kei · {selected_year} Financial Overview · Streamlit + Plotly + Supabase</div>',
    unsafe_allow_html=True,
)

st.caption(
    f"Last updated: {datetime.now().strftime('%B %d, %Y • %I:%M %p')}"
)