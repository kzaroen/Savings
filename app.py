import random
import textwrap
from datetime import datetime
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from supabase import create_client


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP
# ═══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Flow of Tides",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded",
)

supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"],
)

css = Path("assets/styles.css").read_text()
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# THEME
# ═══════════════════════════════════════════════════════════════════════════════

BG = "#ffffff"
PAPER_BG = "#ffffff"
GRID = "#f0e8e2"
TEXT = "#373F51"
SUBTEXT = "#D0ADA7"

MONTHS = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
]

MONTH_INDEX = {month: index for index, month in enumerate(MONTHS)}

SAVINGS_FLOOR = 2000
PERA_CONTRIBUTION_CAP = 200000


def base_layout(title="", height=340):
    return {
        "title": {
            "text": title,
            "font": {
                "family": "Lora",
                "size": 14,
                "color": "#0B3954",
            },
        },
        "plot_bgcolor": BG,
        "paper_bgcolor": PAPER_BG,
        "font": {
            "color": TEXT,
            "size": 11,
            "family": "DM Sans",
        },
        "legend": {
            "orientation": "h",
            "y": 1.12,
            "font": {"size": 11},
        },
        "margin": {
            "l": 10,
            "r": 10,
            "t": 50,
            "b": 10,
        },
        "height": height,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# STATIC CONTENT
# ═══════════════════════════════════════════════════════════════════════════════

VERSES = [
    (
        "Proverbs 21:20 (KJV)",
        "There is treasure to be desired and oil in the dwelling of the wise; "
        "but a foolish man spendeth it up.",
    ),
    (
        "Proverbs 6:6–8 (KJV)",
        "Go to the ant, thou sluggard; consider her ways, and be wise: "
        "Which having no guide, overseer, or ruler, provideth her meat in the "
        "summer, and gathereth her food in the harvest.",
    ),
    (
        "Luke 14:28 (KJV)",
        "For which of you, intending to build a tower, sitteth not down first, "
        "and counteth the cost, whether he have sufficient to finish it?",
    ),
    (
        "Proverbs 22:7 (KJV)",
        "The rich ruleth over the poor, and the borrower is servant to the lender.",
    ),
    (
        "Proverbs 13:11 (KJV)",
        "Wealth gotten by vanity shall be diminished: but he that gathereth by "
        "labour shall increase.",
    ),
    (
        "1 Corinthians 4:2 (KJV)",
        "Moreover it is required in stewards, that a man be found faithful.",
    ),
    (
        "Ecclesiastes 11:1 (KJV)",
        "Cast thy bread upon the waters: for thou shalt find it after many days.",
    ),
    (
        "Galatians 6:9 (KJV)",
        "And let us not be weary in well doing: for in due season we shall reap, "
        "if we faint not.",
    ),
    (
        "Proverbs 10:4 (KJV)",
        "He becometh poor that dealeth with a slack hand: but the hand of the "
        "diligent maketh rich.",
    ),
    (
        "1 Timothy 6:6 (KJV)",
        "But godliness with contentment is great gain.",
    ),
    (
        "Hebrews 13:5 (KJV)",
        "Let your conversation be without covetousness; and be content with "
        "such things as ye have…",
    ),
]


# ═══════════════════════════════════════════════════════════════════════════════
# YEARLY CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

YEARLY_CONFIG = {
    2026: {
        "carryover": {
            "total": 25400,
            "investment": 20000,
            "insurance": 5400,
            "note": "Seed capital from 2025 savings",
            "year": 2025,
        },

        "fixed_insurance": [
            0, 0, 0, 10800, 0, 0,
            0, 0, 0, 5400, 0, 0,
        ],

        "fixed_investments": [
            0, 0, 0, 0, 0, 15000,
            0, 0, 0, 0, 0, 0,
        ],

        "notes": [
            "Controller purchase • Insurance paid from 2025",
            "",
            "",
            "Insurance month paid early so ×2",
            "Stabilization",
            "End of 1H 2026 & Reinvest",
            "Mid-year insurance already paid back in April",
            "",
            "",
            "Insurance month",
            "",
            "Year-end surplus",
        ],

        "goals_config": [
            {
                "label": "PS5 Genshin Impact",
                "desc": "Limited Edition Dual Sense Controller",
                "target": 4900,
                "icon": "🎮",
            },
            {
                "label": "Insurance Fund",
                "desc": "₱21,600 for 4 months of insurance coverage",
                "target": 21600,
                "icon": "🛡️",
            },
            {
                "label": "Investment Target",
                "desc": "₱60,000 across both BPI funds by Dec 2026",
                "target": 60000,
                "icon": "📈",
            },
            {
                "label": "P.E.R.A",
                "desc": "Retirement Fund",
                "target": 5000,
                "icon": "🏦",
            },
        ],

        "milestones": [
            {
                "date": "Jan 2026",
                "label": "Started 2026 with ₱25,400 carryover",
                "icon": "🌱",
                "past": True,
            },
            {
                "date": "Feb 2026",
                "label": "First official portfolio snapshot recorded",
                "icon": "📸",
                "past": True,
            },
            {
                "date": "May 2026",
                "label": "Portfolio crossed ₱20,000 mark",
                "icon": "🌿",
                "past": True,
            },
            {
                "date": "Jun 2026",
                "label": "First major reinvestment — ₱15,000",
                "icon": "🚀",
                "past": True,
            },
            {
                "date": "Sep 2026",
                "label": "Turning 21 — credit card eligibility",
                "icon": "🎂",
                "past": False,
            },
            {
                "date": "Oct 2026",
                "label": "Insurance month — plan ahead",
                "icon": "🛡️",
                "past": False,
            },
            {
                "date": "Dec 2026",
                "label": "Year-end reinvestment + PERA planning",
                "icon": "🏦",
                "past": False,
            },
        ],

        "planned_investment_path": {
            "Jan": {"equity": 8000, "bond": 12000},
            "Jun": {"equity": 20000, "bond": 15000},
        },

        "initial_snapshots": [
            {
                "date": "Feb",
                "us_equity": 8039.98,
                "bond_fund": 11952.97,
                "bond_income": 58.86,
                "pera_balance": 0.0,
                "pera_contributions": 0.0,
                "official": True,
                "planned": False,
            },
            {
                "date": "Mar",
                "us_equity": 7840.03,
                "bond_fund": 11809.68,
                "bond_income": 58.02,
                "pera_balance": 0.0,
                "pera_contributions": 0.0,
                "official": True,
                "planned": False,
            },
            {
                "date": "Apr",
                "us_equity": 7746.09,
                "bond_fund": 11921.25,
                "bond_income": 60.20,
                "pera_balance": 0.0,
                "pera_contributions": 0.0,
                "official": True,
                "planned": False,
            },
            {
                "date": "May",
                "us_equity": 8668.67,
                "bond_fund": 12185.95,
                "bond_income": 61.22,
                "pera_balance": 0.0,
                "pera_contributions": 0.0,
                "official": True,
                "planned": False,
            },
            {
                "date": "Jun",
                "us_equity": 0.0,
                "bond_fund": 0.0,
                "bond_income": 0.0,
                "pera_balance": 0.0,
                "pera_contributions": 0.0,
                "official": False,
                "planned": True,
            },
            {
                "date": "Jul",
                "us_equity": 0.0,
                "bond_fund": 0.0,
                "bond_income": 0.0,
                "pera_balance": 0.0,
                "pera_contributions": 0.0,
                "official": False,
                "planned": False,
            },
            {
                "date": "Aug",
                "us_equity": 0.0,
                "bond_fund": 0.0,
                "bond_income": 0.0,
                "pera_balance": 0.0,
                "pera_contributions": 0.0,
                "official": False,
                "planned": False,
            },
            {
                "date": "Sep",
                "us_equity": 0.0,
                "bond_fund": 0.0,
                "bond_income": 0.0,
                "pera_balance": 0.0,
                "pera_contributions": 0.0,
                "official": False,
                "planned": False,
            },
            {
                "date": "Oct",
                "us_equity": 0.0,
                "bond_fund": 0.0,
                "bond_income": 0.0,
                "pera_balance": 0.0,
                "pera_contributions": 0.0,
                "official": False,
                "planned": False,
            },
            {
                "date": "Nov",
                "us_equity": 0.0,
                "bond_fund": 0.0,
                "bond_income": 0.0,
                "pera_balance": 0.0,
                "pera_contributions": 0.0,
                "official": False,
                "planned": False,
            },
            {
                "date": "Dec",
                "us_equity": 0.0,
                "bond_fund": 0.0,
                "bond_income": 0.0,
                "pera_balance": 0.0,
                "pera_contributions": 0.0,
                "official": False,
                "planned": True,
            },
        ],
    },

    2027: {
        "carryover": {
            "total": 0,
            "investment": 0,
            "insurance": 0,
            "note": "Update after 2026 year-end close",
            "year": 2026,
        },

        "fixed_insurance": [0] * 12,
        "fixed_investments": [0] * 12,
        "notes": [""] * 12,

        "goals_config": [
            {
                "label": "Emergency Fund",
                "desc": "Liquid reserve, phase-2 focus",
                "target": 30000,
                "icon": "🧯",
            },
            {
                "label": "P.E.R.A",
                "desc": "Retirement Fund",
                "target": 20000,
                "icon": "🏦",
            },
        ],

        "milestones": [],
        "planned_investment_path": {},
        "initial_snapshots": [],
    },
}


# ═══════════════════════════════════════════════════════════════════════════════
# YEAR SELECTION
# ═══════════════════════════════════════════════════════════════════════════════

current_year = datetime.now().year
available_years = sorted(YEARLY_CONFIG)

with st.sidebar:
    selected_year = st.selectbox(
        "📅 Viewing Year",
        available_years,
        index=(
            available_years.index(current_year)
            if current_year in available_years
            else len(available_years) - 1
        ),
    )

cfg = YEARLY_CONFIG[selected_year]

CARRYOVER = cfg["carryover"]
FIXED_INSURANCE = cfg["fixed_insurance"]
FIXED_INVESTMENTS = cfg["fixed_investments"]
NOTES = cfg["notes"]
GOALS_CONFIG = cfg["goals_config"]
MILESTONES = cfg["milestones"]
PLANNED_INVESTMENT_PATH = cfg["planned_investment_path"]
INITIAL_SNAPSHOTS = cfg["initial_snapshots"]


# ═══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════════════════════

def fmt_value(value, prefix="₱", decimals=2):
    if value == 0:
        return '<span class="empty-val">Pending</span>'

    return f"{prefix}{value:,.{decimals}f}"


def render_html(html: str):
    st.markdown(
        textwrap.dedent(html),
        unsafe_allow_html=True,
    )


def goal_status_label(percent):
    if percent == 0:
        return "not-started", "Your next step"
    if percent < 50:
        return "inprogress", "In progress — keep going"
    if percent < 100:
        return "almosthere", "Almost there — don't stop now"

    return "complete", "Goal achieved 🎉"


def get_snap_date(snapshot):
    return snapshot.get("snapshot_date", snapshot.get("date"))


# ═══════════════════════════════════════════════════════════════════════════════
# SUPABASE — LOAD
# ═══════════════════════════════════════════════════════════════════════════════

def load_monthly_finance(year):
    try:
        rows = (
            supabase
            .table("monthly_finance")
            .select("*")
            .eq("year", year)
            .execute()
            .data
            or []
        )
    except Exception as error:
        st.error(f"Supabase load failed: {error}")
        rows = []

    income = {month: 0.0 for month in MONTHS}
    expenses = {month: 0.0 for month in MONTHS}

    for row in rows:
        month = row.get("month")

        if month in MONTHS:
            income[month] = float(row.get("income") or 0)
            expenses[month] = float(row.get("expenses") or 0)

    return income, expenses


def load_goals(year):
    try:
        rows = (
            supabase
            .table("goals")
            .select("*")
            .eq("year", year)
            .execute()
            .data
            or []
        )
    except Exception as error:
        st.error(f"Supabase load failed: {error}")
        rows = []

    goals = {
        row["label"]: float(row["current_value"] or 0)
        for row in rows
    }

    for goal in GOALS_CONFIG:
        goals.setdefault(goal["label"], 0.0)

    return goals


def load_snapshots(year):
    try:
        rows = (
            supabase
            .table("investment_snapshots")
            .select("*")
            .eq("year", year)
            .execute()
            .data
            or []
        )
    except Exception as error:
        st.error(f"Supabase load failed: {error}")
        rows = []

    return sorted(
        rows,
        key=lambda snapshot: MONTH_INDEX.get(
            get_snap_date(snapshot),
            999,
        ),
    )


income_map, expenses_map = load_monthly_finance(selected_year)
goals = load_goals(selected_year)
snapshots = load_snapshots(selected_year)


# ═══════════════════════════════════════════════════════════════════════════════
# SUPABASE — SAVE
# ═══════════════════════════════════════════════════════════════════════════════

def save_monthly(year, month, income, expenses):
    try:
        (
            supabase
            .table("monthly_finance")
            .upsert(
                {
                    "year": year,
                    "month": month,
                    "income": income,
                    "expenses": expenses,
                },
                on_conflict="year,month",
            )
            .execute()
        )
    except Exception as error:
        st.error(f"Save failed for {month} {year}: {error}")


def save_goal(year, label, current_value):
    try:
        config = next(
            (goal for goal in GOALS_CONFIG if goal["label"] == label),
            {},
        )

        (
            supabase
            .table("goals")
            .upsert(
                {
                    "year": year,
                    "label": label,
                    "current_value": current_value,
                    "target_value": config.get("target", 0),
                    "description": config.get("desc", ""),
                    "icon": config.get("icon", ""),
                },
                on_conflict="year,label",
            )
            .execute()
        )
    except Exception as error:
        st.error(f"Save failed for goal {label}: {error}")


def save_snapshot(year, snapshot):
    try:
        (
            supabase
            .table("investment_snapshots")
            .upsert(
                {
                    "year": year,
                    "snapshot_date": snapshot["date"],
                    "us_equity": snapshot["us_equity"],
                    "bond_fund": snapshot["bond_fund"],
                    "bond_income": snapshot["bond_income"],
                    "pera_balance": snapshot.get("pera_balance", 0.0),
                    "pera_contributions": snapshot.get(
                        "pera_contributions",
                        0.0,
                    ),
                    "official": snapshot["official"],
                    "planned": snapshot["planned"],
                },
                on_conflict="year,snapshot_date",
            )
            .execute()
        )
    except Exception as error:
        st.error(
            f"Save failed for snapshot {snapshot['date']} {year}: {error}"
        )


def delete_snapshot(year, date_label):
    try:
        (
            supabase
            .table("investment_snapshots")
            .delete()
            .eq("year", year)
            .eq("snapshot_date", date_label)
            .execute()
        )
    except Exception as error:
        st.error(f"Delete failed for {date_label}: {error}")


def reset_snapshots_in_db(year):
    try:
        (
            supabase
            .table("investment_snapshots")
            .delete()
            .eq("year", year)
            .execute()
        )

        for snapshot in INITIAL_SNAPSHOTS:
            (
                supabase
                .table("investment_snapshots")
                .insert(
                    {
                        "year": year,
                        "snapshot_date": snapshot["date"],
                        "us_equity": snapshot["us_equity"],
                        "bond_fund": snapshot["bond_fund"],
                        "bond_income": snapshot["bond_income"],
                        "pera_balance": snapshot.get(
                            "pera_balance",
                            0.0,
                        ),
                        "pera_contributions": snapshot.get(
                            "pera_contributions",
                            0.0,
                        ),
                        "official": snapshot["official"],
                        "planned": snapshot["planned"],
                    }
                )
                .execute()
            )

    except Exception as error:
        st.error(f"Reset failed: {error}")


# ═══════════════════════════════════════════════════════════════════════════════
# BUILD DATA
# ═══════════════════════════════════════════════════════════════════════════════

def build_df():
    rows = []
    cumulative = 0

    for index, month in enumerate(MONTHS):
        income = income_map[month]
        expenses = expenses_map[month]
        insurance = FIXED_INSURANCE[index]
        investments = FIXED_INVESTMENTS[index]

        net = income - expenses - investments - insurance
        cumulative += net

        rows.append(
            {
                "Month": month,
                "Insurance": insurance,
                "Investments": investments,
                "Savings Deposited": income,
                "Money Spent": expenses,
                "Kept for Future": net,
                "Cumulative": cumulative,
            }
        )

    return pd.DataFrame(rows)


baseline_df = build_df()

total_income = baseline_df["Savings Deposited"].sum()
total_investments = baseline_df["Investments"].sum()
total_expenses = baseline_df["Money Spent"].sum()
end_cumulative = baseline_df["Cumulative"].iloc[-1]

best_month = baseline_df.loc[
    baseline_df["Kept for Future"].idxmax(),
    "Month",
]

worst_month = baseline_df.loc[
    baseline_df["Kept for Future"].idxmin(),
    "Month",
]

negative_months = baseline_df[
    baseline_df["Kept for Future"] < 0
]["Month"].tolist()

floor_months = [
    month
    for month in MONTHS
    if (
        income_map[month] - expenses_map[month] < SAVINGS_FLOOR
        and income_map[month] > 0
    )
]

bond_income_ytd = sum(
    snapshot["bond_income"]
    for snapshot in snapshots
)

invest_vs_save = (
    total_investments / total_income * 100
    if total_income
    else 0
)

savings_rate_ytd = (
    (total_income - total_expenses) / total_income * 100
    if total_income
    else 0
)


# ═══════════════════════════════════════════════════════════════════════════════
# INVESTMENT DATA
# ═══════════════════════════════════════════════════════════════════════════════

actual_snapshots = sorted(
    [
        snapshot
        for snapshot in snapshots
        if snapshot["official"] and snapshot["us_equity"] > 0
    ],
    key=lambda snapshot: MONTH_INDEX.get(
        get_snap_date(snapshot),
        999,
    ),
)

latest_snapshot = actual_snapshots[-1] if actual_snapshots else None

latest_equity = (
    latest_snapshot["us_equity"]
    if latest_snapshot
    else 0
)

latest_bond = (
    latest_snapshot["bond_fund"]
    if latest_snapshot
    else 0
)

portfolio_value = latest_equity + latest_bond

cost_basis_prior = CARRYOVER["investment"]
cost_basis_this_year = total_investments
total_cost_basis = cost_basis_prior + cost_basis_this_year

unrealized_pnl = portfolio_value - total_cost_basis
realized_pnl = bond_income_ytd
net_pnl = unrealized_pnl + realized_pnl

equity_pct = (
    latest_equity / portfolio_value * 100
    if portfolio_value
    else 0
)

bond_pct = (
    latest_bond / portfolio_value * 100
    if portfolio_value
    else 0
)

net_worth = (
    portfolio_value
    + bond_income_ytd
    + end_cumulative
)


# ═══════════════════════════════════════════════════════════════════════════════
# PERA
# ═══════════════════════════════════════════════════════════════════════════════

latest_pera_balance = (
    latest_snapshot.get("pera_balance", 0.0)
    if latest_snapshot
    else 0.0
)

pera_contributions_ytd = sum(
    snapshot.get("pera_contributions", 0.0)
    for snapshot in snapshots
)

pera_cap_pct = (
    min(
        pera_contributions_ytd / PERA_CONTRIBUTION_CAP * 100,
        100,
    )
    if PERA_CONTRIBUTION_CAP
    else 0
)

investment_growth_rate = (
    (portfolio_value - total_cost_basis)
    / total_cost_basis
    * 100
    if total_cost_basis
    else 0
)


# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════

if "verse" not in st.session_state:
    st.session_state.verse = random.choice(VERSES)

verse_data = st.session_state.verse

if (
    not isinstance(verse_data, (list, tuple))
    or len(verse_data) != 2
):
    verse_data = random.choice(VERSES)
    st.session_state.verse = verse_data

with st.sidebar:
    st.markdown("# This is for my future self")

    st.markdown(
        "<hr style='margin:6px 0;border:0;height:1px;"
        "background-color:#373F51;opacity:0.6;'>",
        unsafe_allow_html=True,
    )

    st.caption(
        f"📱 Scroll down for full dashboard on mobile · "
        f"Viewing {selected_year}"
    )

    # ── Goals ────────────────────────────────────────────────────────────────

    st.markdown("### 🎯 Goals")

    with st.expander("Update Goals"):
        with st.form(f"goals_form_{selected_year}"):

            for goal in GOALS_CONFIG:
                label = goal["label"]

                if label == "Insurance Fund":
                    step = 5400.0
                elif label == "Investment Target":
                    step = 1000.0
                else:
                    step = 100.0

                st.number_input(
                    f"{goal['icon']} {label}",
                    min_value=0.0,
                    max_value=float(goal["target"] * 2),
                    value=goals.get(label, 0.0),
                    step=step,
                    format="%.0f",
                    key=f"goal_{label}_{selected_year}",
                    help=goal["desc"],
                )

            if st.form_submit_button(
                "Save Goals",
                use_container_width=True,
            ):
                for goal in GOALS_CONFIG:
                    label = goal["label"]
                    new_value = st.session_state[
                        f"goal_{label}_{selected_year}"
                    ]

                    if new_value != goals[label]:
                        goals[label] = new_value
                        save_goal(
                            selected_year,
                            label,
                            new_value,
                        )

                st.success("Goals saved!")
                st.rerun()

    # ── Savings Deposited ───────────────────────────────────────────────────

    st.markdown("### 🏦 Savings Deposited")

    with st.expander("Monthly Deposits"):
        with st.form(f"income_form_{selected_year}"):

            for month in MONTHS:
                st.number_input(
                    month,
                    0.0,
                    50000.0,
                    income_map[month],
                    500.0,
                    key=f"income_{month}_{selected_year}",
                    help=(
                        f"Total cash you set aside in "
                        f"{month} {selected_year}"
                    ),
                )

            if st.form_submit_button(
                "Save Deposits",
                use_container_width=True,
            ):
                for month in MONTHS:
                    new_income = st.session_state[
                        f"income_{month}_{selected_year}"
                    ]

                    if new_income != income_map[month]:
                        income_map[month] = new_income

                        save_monthly(
                            selected_year,
                            month,
                            new_income,
                            expenses_map[month],
                        )

                st.success("Deposits saved!")
                st.rerun()

    # ── Expenses ────────────────────────────────────────────────────────────

    st.markdown("### 💸 Money Spent")

    with st.expander("Monthly Expenses"):
        with st.form(f"expenses_form_{selected_year}"):

            for month in MONTHS:
                st.number_input(
                    month,
                    0.0,
                    50000.0,
                    expenses_map[month],
                    500.0,
                    key=f"expense_{month}_{selected_year}",
                    help=(
                        f"Total spent in {month} {selected_year} "
                        "(excluding insurance & investments)"
                    ),
                )

            if st.form_submit_button(
                "Save Expenses",
                use_container_width=True,
            ):
                for month in MONTHS:
                    new_expenses = st.session_state[
                        f"expense_{month}_{selected_year}"
                    ]

                    if new_expenses != expenses_map[month]:
                        expenses_map[month] = new_expenses

                        save_monthly(
                            selected_year,
                            month,
                            income_map[month],
                            new_expenses,
                        )

                st.success("Expenses saved!")
                st.rerun()

    # ── Add Portfolio Snapshot ──────────────────────────────────────────────

    st.markdown("### 📸 Portfolio Snapshots")

    with st.expander("Add Snapshot"):
        with st.form(f"add_snap_form_{selected_year}"):

            snap_date = st.text_input(
                "Month label (e.g. Jun)",
                key=f"snap_date_{selected_year}",
                help="Use the 3-letter month abbreviation",
            )

            snap_equity = st.number_input(
                "US Equity Feeder (₱)",
                0.0,
                value=0.0,
                step=10.0,
                format="%.2f",
                key=f"snap_eq_{selected_year}",
            )

            snap_bond = st.number_input(
                "Global Bond Fund (₱)",
                0.0,
                value=0.0,
                step=10.0,
                format="%.2f",
                key=f"snap_bond_{selected_year}",
            )

            snap_bond_income = st.number_input(
                "Bond Income received (₱)",
                0.0,
                value=0.0,
                step=1.0,
                format="%.2f",
                key=f"snap_bi_{selected_year}",
            )

            snap_pera_balance = st.number_input(
                "PERA Balance (₱)",
                0.0,
                value=0.0,
                step=10.0,
                format="%.2f",
                key=f"snap_pera_bal_{selected_year}",
                help="Total PERA account value as of this snapshot",
            )

            snap_pera_contribution = st.number_input(
                "PERA Contribution this snapshot (₱)",
                0.0,
                value=0.0,
                step=100.0,
                format="%.2f",
                key=f"snap_pera_ctr_{selected_year}",
                help="New money put into PERA since your last snapshot",
            )

            snap_official = st.checkbox(
                "✦ Mark as Official (verified from BPI app)",
                key=f"snap_official_{selected_year}",
            )

            snap_planned = st.checkbox(
                "⏳ Mark as Planned (future projection)",
                key=f"snap_planned_{selected_year}",
            )

            if st.form_submit_button(
                "Add Snapshot",
                use_container_width=True,
            ):
                if snap_date:
                    new_snapshot = {
                        "date": snap_date,
                        "us_equity": snap_equity,
                        "bond_fund": snap_bond,
                        "bond_income": snap_bond_income,
                        "pera_balance": snap_pera_balance,
                        "pera_contributions": snap_pera_contribution,
                        "official": snap_official,
                        "planned": snap_planned,
                    }

                    existing_dates = [
                        get_snap_date(snapshot)
                        for snapshot in snapshots
                    ]

                    if snap_date in existing_dates:
                        snapshots[
                            existing_dates.index(snap_date)
                        ] = new_snapshot
                    else:
                        snapshots.append(new_snapshot)

                    snapshots.sort(
                        key=lambda snapshot: MONTH_INDEX.get(
                            get_snap_date(snapshot),
                            999,
                        )
                    )

                    save_snapshot(
                        selected_year,
                        new_snapshot,
                    )

                    st.success(
                        f"Snapshot saved: {snap_date}"
                    )
                    st.rerun()

    # ── Edit / Delete Snapshot ──────────────────────────────────────────────

    with st.expander("Edit / Delete Snapshot"):

        if snapshots:
            snapshot_labels = [
                get_snap_date(snapshot)
                for snapshot in snapshots
            ]

            edit_date = st.selectbox(
                "Select snapshot to edit",
                snapshot_labels,
                key=f"edit_select_{selected_year}",
            )

            edit_index = snapshot_labels.index(edit_date)
            snapshot = snapshots[edit_index]

            with st.form(f"edit_snap_form_{selected_year}"):

                edit_equity = st.number_input(
                    "US Equity (₱)",
                    value=float(snapshot["us_equity"]),
                    step=10.0,
                    format="%.2f",
                    key=f"e_eq_{selected_year}",
                )

                edit_bond = st.number_input(
                    "Bond Fund (₱)",
                    value=float(snapshot["bond_fund"]),
                    step=10.0,
                    format="%.2f",
                    key=f"e_bf_{selected_year}",
                )

                edit_bond_income = st.number_input(
                    "Bond Income (₱)",
                    value=float(snapshot["bond_income"]),
                    step=1.0,
                    format="%.2f",
                    key=f"e_bi_{selected_year}",
                )

                edit_pera_balance = st.number_input(
                    "PERA Balance (₱)",
                    value=float(
                        snapshot.get("pera_balance", 0.0)
                    ),
                    step=10.0,
                    format="%.2f",
                    key=f"e_pb_{selected_year}",
                )

                edit_pera_contribution = st.number_input(
                    "PERA Contribution (₱)",
                    value=float(
                        snapshot.get(
                            "pera_contributions",
                            0.0,
                        )
                    ),
                    step=100.0,
                    format="%.2f",
                    key=f"e_pc_{selected_year}",
                )

                edit_official = st.checkbox(
                    "✦ Official",
                    value=snapshot["official"],
                    key=f"e_official_{selected_year}",
                )

                edit_planned = st.checkbox(
                    "⏳ Planned",
                    value=snapshot["planned"],
                    key=f"e_planned_{selected_year}",
                )

                col1, col2 = st.columns(2)

                with col1:
                    save_button = st.form_submit_button(
                        "Save",
                        use_container_width=True,
                    )

                with col2:
                    delete_button = st.form_submit_button(
                        "Delete",
                        use_container_width=True,
                    )

            if save_button:
                updated_snapshot = {
                    "date": edit_date,
                    "us_equity": edit_equity,
                    "bond_fund": edit_bond,
                    "bond_income": edit_bond_income,
                    "pera_balance": edit_pera_balance,
                    "pera_contributions": edit_pera_contribution,
                    "official": edit_official,
                    "planned": edit_planned,
                }

                snapshots[edit_index] = updated_snapshot
                save_snapshot(
                    selected_year,
                    updated_snapshot,
                )

                st.success("Saved!")
                st.rerun()

            if delete_button:
                delete_snapshot(
                    selected_year,
                    edit_date,
                )

                snapshots.pop(edit_index)

                st.success(f"Deleted: {edit_date}")
                st.rerun()

        if st.button(
            "↺ Reset All Snapshots to Defaults",
            use_container_width=True,
            key=f"reset_snaps_{selected_year}",
        ):
            reset_snapshots_in_db(selected_year)

            snapshots = [
                snapshot.copy()
                for snapshot in INITIAL_SNAPSHOTS
            ]

            snapshots.sort(
                key=lambda snapshot: MONTH_INDEX.get(
                    get_snap_date(snapshot),
                    999,
                )
            )

            st.success("Snapshots reset.")
            st.rerun()

    # ── Verse ───────────────────────────────────────────────────────────────

    st.markdown("---")

    ref, verse = verse_data

    st.caption(
        f"**{ref}**  \n*{verse}*"
    )

    st.caption(
        "Earn wisely. Give faithfully. Your money is a tool, not a treasure. "
        "Use it to build the life you want and to bless others along the way. "
        "May you be guided by Jesus Christ. God will provide, and He will "
        "always provide more than enough."
    )


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE HEADER
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown(
    f"""
    <div style="text-align:center;padding:16px 0 4px 0;">
        <span style="
            font-family:Lora,serif;
            color:#0B3954;
            font-size:24px;
            font-weight:600;
        ">
            {selected_year} Financial Overview
        </span>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div style="
        text-align:center;
        color:#D0ADA7;
        font-size:11px;
        letter-spacing:2.5px;
        text-transform:uppercase;
        margin-bottom:24px;
    ">
        Blessed to give, not hoard.
    </div>
    """,
    unsafe_allow_html=True,
)


# ═══════════════════════════════════════════════════════════════════════════════
# KPI — THIS YEAR
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown(
    '<div class="section-header">📋 This Year So Far</div>',
    unsafe_allow_html=True,
)

c1, c2, c3, c4, c5 = st.columns(5)

kpis = [
    (
        c1,
        "Savings Deposited",
        f"₱{total_income:,.0f}",
        "Total set aside",
        False,
    ),
    (
        c2,
        "Money Spent",
        f"₱{total_expenses:,.0f}",
        "All personal outflows",
        False,
    ),
    (
        c3,
        "Savings Rate",
        f"{savings_rate_ytd:.1f}%",
        "Income kept after expenses",
        False,
    ),
    (
        c4,
        "Kept for Future",
        f"₱{end_cumulative:,.0f}",
        "Year-end running total",
        end_cumulative < 0,
    ),
    (
        c5,
        "Passive Provision",
        f"₱{bond_income_ytd:,.2f}",
        "Bond income received",
        False,
    ),
]

for column, label, value, subtitle, is_negative in kpis:
    with column:
        render_html(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value {'kpi-neg' if is_negative else 'kpi-pos'}">
                    {value}
                </div>
                <div class="kpi-sub">{subtitle}</div>
            </div>
            """
        )

# ═══════════════════════════════════════════════════════════════════════════════
# KPI — WEALTH
# ═══════════════════════════════════════════════════════════════════════════════

c6, c7, c8, c9, c10 = st.columns(5)

wealth_kpis = [
    (
        c6,
        "Portfolio Value",
        f"₱{portfolio_value:,.2f}"
        if portfolio_value
        else "—",
        "US Equity + Bond Fund",
        False,
    ),
    (
        c7,
        "Unrealized G/L",
        f"{'+' if unrealized_pnl >= 0 else ''}"
        f"₱{unrealized_pnl:,.2f}",
        "vs total cost basis",
        unrealized_pnl < 0,
    ),
    (
        c8,
        "Net P&L",
        f"{'+' if net_pnl >= 0 else ''}"
        f"₱{net_pnl:,.2f}",
        "incl. bond income",
        net_pnl < 0,
    ),
    (
        c9,
        "Est. Net Worth",
        f"₱{net_worth:,.0f}",
        "Portfolio + savings",
        False,
    ),
    (
        c10,
        "Wealth Growth Rate",
        f"{investment_growth_rate:.1f}%",
        "Realized + unrealized portfolio growth",
        investment_growth_rate < 0,
    ),
]

for column, label, value, subtitle, is_negative in wealth_kpis:
    with column:
        render_html(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value {'kpi-neg' if is_negative else 'kpi-pos'}">
                    {value}
                </div>
                <div class="kpi-sub">{subtitle}</div>
            </div>
            """
        )


# ═══════════════════════════════════════════════════════════════════════════════
# PERA
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown(
    '<div class="section-header">🏦 P.E.R.A — Retirement Tracking</div>',
    unsafe_allow_html=True,
)

p1, p2, p3 = st.columns(3)

with p1:
    render_html(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">PERA Balance</div>
            <div class="kpi-value kpi-pos">
                {fmt_value(latest_pera_balance)}
            </div>
            <div class="kpi-sub">
                Locked until retirement — tracked separately from net worth
            </div>
        </div>
        """
    )

with p2:
    render_html(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Contributions This Year</div>
            <div class="kpi-value kpi-pos">
                {fmt_value(pera_contributions_ytd)}
            </div>
            <div class="kpi-sub">
                {pera_cap_pct:.0f}% of ₱{PERA_CONTRIBUTION_CAP:,} annual cap
            </div>
        </div>
        """
    )

with p3:
    render_html(
        f"""
        <div class="kpi-card" style="text-align:left;">
            <div class="kpi-label" style="text-align:center;">
                Cap Progress
            </div>

            <div class="goal-bar-bg" style="margin-top:10px;">
                <div class="goal-bar-fill"
                    style="width:{pera_cap_pct:.1f}%;"></div>
            </div>

            <div class="goal-numbers">
                <span>₱{pera_contributions_ytd:,.0f}</span>
                <span>₱{PERA_CONTRIBUTION_CAP:,.0f}</span>
            </div>
        </div>
        """
    )


# ═══════════════════════════════════════════════════════════════════════════════
# CAPITAL ORIGIN + MILESTONES
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown(
    '<div class="section-header">🌱 Capital Origin & Milestones</div>',
    unsafe_allow_html=True,
)

col_origin, col_milestones = st.columns([1, 2])

with col_origin:
    prior_pct = (
        cost_basis_prior / total_cost_basis * 100
        if total_cost_basis
        else 0
    )

    this_year_pct = (
        cost_basis_this_year / total_cost_basis * 100
        if total_cost_basis
        else 0
    )

    render_html(
        f"""
        <div class="capital-card">
            <div class="kpi-label" style="margin-bottom:12px;">
                Where your investments came from
            </div>

            <div class="capital-row">
                <div>
                    <div style="
                        color:#373F51;
                        font-size:13px;
                        font-weight:500;
                    ">
                        {CARRYOVER['year']} Carryover
                    </div>
                    <div class="capital-note">
                        {CARRYOVER['note']}
                    </div>
                </div>

                <div style="text-align:right;">
                    <div class="capital-amount">
                        ₱{cost_basis_prior:,.0f}
                    </div>
                    <div class="capital-source">
                        {prior_pct:.0f}% of basis
                    </div>
                </div>
            </div>

            <div class="capital-row">
                <div>
                    <div style="
                        color:#373F51;
                        font-size:13px;
                        font-weight:500;
                    ">
                        {CARRYOVER['year']} → Insurance Reserve
                    </div>
                    <div class="capital-note">
                        Carried into early-year coverage
                    </div>
                </div>

                <div style="text-align:right;">
                    <div class="capital-amount">
                        ₱{CARRYOVER['insurance']:,.0f}
                    </div>
                    <div class="capital-source">
                        Separate from investments
                    </div>
                </div>
            </div>

            <div class="capital-row">
                <div>
                    <div style="
                        color:#373F51;
                        font-size:13px;
                        font-weight:500;
                    ">
                        {selected_year} Operating Investments
                    </div>
                    <div class="capital-note">
                        From this year's income
                    </div>
                </div>

                <div style="text-align:right;">
                    <div class="capital-amount">
                        ₱{cost_basis_this_year:,.0f}
                    </div>
                    <div class="capital-source">
                        {this_year_pct:.0f}% of basis
                    </div>
                </div>
            </div>

            <div class="capital-row" style="margin-top:4px;">
                <div style="
                    color:#0B3954;
                    font-size:13px;
                    font-weight:600;
                ">
                    Total Cost Basis
                </div>

                <div class="capital-amount">
                    ₱{total_cost_basis:,.0f}
                </div>
            </div>
        </div>
        """
    )
    

with col_milestones:
    if MILESTONES:
        cards = ""

        for milestone in MILESTONES:
            status_class = (
                "milestone-past"
                if milestone["past"]
                else "milestone-future"
            )

            cards += f"""
            <div class="milestone-card {status_class}">
                <div class="milestone-icon">
                    {milestone['icon']}
                </div>
                <div class="milestone-date">
                    {milestone['date']}
                </div>
                <div class="milestone-label">
                    {milestone['label']}
                </div>
            </div>
            """

        st.markdown(
            f'<div class="milestone-strip">{cards}</div>',
            unsafe_allow_html=True
        )
    else:
        st.info(
            f"No milestones logged for {selected_year} yet."
        )


# ═══════════════════════════════════════════════════════════════════════════════
# GOALS
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown(
    '<div class="section-header">🎯 Goals</div>',
    unsafe_allow_html=True,
)

goal_columns = st.columns(len(GOALS_CONFIG))

for index, goal in enumerate(GOALS_CONFIG):
    current_value = goals.get(goal["label"], 0)
    target_value = goal["target"]

    percent = (
        min(current_value / target_value * 100, 100)
        if target_value
        else 0
    )

    status_key, status_text = goal_status_label(percent)

    with goal_columns[index]:
        render_html(
            f"""
            <div class="goal-card">
                <div class="goal-title">
                    {goal['icon']} {goal['label']}
                </div>

                <div class="goal-meta">
                    {goal['desc']}
                </div>

                <span class="goal-pct">
                    {percent:.0f}%
                </span>

                <div class="goal-bar-bg">
                    <div class="goal-bar-fill"
                        style="width:{percent:.1f}%;"></div>
                </div>

                <div class="goal-numbers">
                    <span>₱{current_value:,.0f}</span>
                    <span>₱{target_value:,.0f}</span>
                </div>

                <div class="goal-status goal-status-{status_key}">
                    {status_text}
                </div>
            </div>
            """
        )


# ═══════════════════════════════════════════════════════════════════════════════
# CASH FLOW
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown(
    '<div class="section-header">📊 Cash Flow</div>',
    unsafe_allow_html=True,
)

col_a, col_b = st.columns([3, 2])

with col_a:
    fig = go.Figure()

    fig.add_bar(
        x=baseline_df["Month"],
        y=baseline_df["Savings Deposited"],
        name="Savings Deposited",
        marker_color="#6EA4BF",
        opacity=0.85,
    )

    fig.add_bar(
        x=baseline_df["Month"],
        y=(
            baseline_df["Insurance"]
            + baseline_df["Investments"]
            + baseline_df["Money Spent"]
        ),
        name="Total Outflow",
        marker_color="#D0ADA7",
        opacity=0.80,
    )

    fig.add_scatter(
        x=baseline_df["Month"],
        y=baseline_df["Kept for Future"],
        name="Kept for Future",
        mode="lines+markers",
        line=dict(
            color="#0B3954",
            width=2.5,
        ),
        marker=dict(
            size=8,
            color=[
                "#b05555" if value < 0 else "#0B3954"
                for value in baseline_df["Kept for Future"]
            ],
        ),
    )

    layout = base_layout(
        "Monthly Deposits vs Outflow vs Net",
        340,
    )

    layout["barmode"] = "group"

    fig.update_layout(**layout)

    fig.update_xaxes(
        showgrid=False,
        color=TEXT,
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor=GRID,
        color=SUBTEXT,
        tickprefix="₱",
        tickformat=",",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )


with col_b:
    fig = go.Figure(
        go.Pie(
            labels=[
                "Savings Deposited",
                "Total Insurance Coverage",
                "Invested",
                "Money Spent",
            ],
            values=[
                total_income,
                sum(FIXED_INSURANCE) + CARRYOVER["insurance"],
                total_investments,
                total_expenses,
            ],
            hole=0.55,
            marker_colors=[
                "#6EA4BF",
                "#D0ADA7",
                "#0B3954",
                "#E8D6CB",
            ],
            textinfo="label+percent",
            textfont_size=11,
        )
    )

    fig.update_layout(
        **base_layout(
            "Annual Allocation Breakdown",
            340,
        )
    )

    fig.update_layout(showlegend=False)

    st.plotly_chart(
        fig,
        use_container_width=True,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# SAVINGS & INVESTMENT GROWTH
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown(
    '<div class="section-header">📈 Savings & Investment Growth</div>',
    unsafe_allow_html=True,
)

col_c, col_d = st.columns([3, 2])

with col_c:
    fig = go.Figure()

    fig.add_scatter(
        x=baseline_df["Month"],
        y=baseline_df["Cumulative"],
        name="Cumulative",
        mode="lines+markers",
        line=dict(
            color="#0B3954",
            width=2.5,
        ),
        marker=dict(
            size=8,
            color="#6EA4BF",
        ),
        fill="tozeroy",
        fillcolor="rgba(110,164,191,0.10)",
    )

    fig.add_hline(
        y=0,
        line_color="#D0ADA7",
        line_dash="dot",
        line_width=1.5,
    )

    fig.update_layout(
        **base_layout(
            "Cumulative Savings Growth",
            320,
        )
    )

    fig.update_xaxes(
        showgrid=False,
        color=TEXT,
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor=GRID,
        color=SUBTEXT,
        tickprefix="₱",
        tickformat=",",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )


with col_d:
    sorted_snapshots = sorted(
        snapshots,
        key=lambda snapshot: MONTH_INDEX.get(
            get_snap_date(snapshot),
            999,
        ),
    )

    actual_months = [
        get_snap_date(snapshot)
        for snapshot in sorted_snapshots
        if snapshot["us_equity"] > 0
    ]

    actual_equity = [
        snapshot["us_equity"]
        for snapshot in sorted_snapshots
        if snapshot["us_equity"] > 0
    ]

    actual_bond = [
        snapshot["bond_fund"]
        for snapshot in sorted_snapshots
        if snapshot["us_equity"] > 0
    ]

    fig = go.Figure()

    fig.add_bar(
        x=MONTHS,
        y=[
            PLANNED_INVESTMENT_PATH
            .get(month, {})
            .get("equity", 0)
            for month in MONTHS
        ],
        name="Planned Equity",
        marker_color="#6EA4BF",
        opacity=0.35,
    )

    fig.add_bar(
        x=MONTHS,
        y=[
            PLANNED_INVESTMENT_PATH
            .get(month, {})
            .get("bond", 0)
            for month in MONTHS
        ],
        name="Planned Bond",
        marker_color="#0B3954",
        opacity=0.25,
    )

    fig.add_scatter(
        x=actual_months,
        y=[
            equity + bond
            for equity, bond in zip(
                actual_equity,
                actual_bond,
            )
        ],
        name="Actual Total",
        mode="lines+markers",
        line=dict(
            width=2,
            color="#D0ADA7",
        ),
        marker=dict(size=7),
    )

    fig.update_layout(
        **base_layout(
            "Planned vs Actual Portfolio",
            320,
        )
    )

    fig.update_xaxes(
        showgrid=False,
        color=TEXT,
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor=GRID,
        color=SUBTEXT,
        tickprefix="₱",
        tickformat=",",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# PORTFOLIO SNAPSHOTS
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown(
    '<div class="section-header">📸 Portfolio Snapshots</div>',
    unsafe_allow_html=True,
)

col_e, col_f = st.columns([3, 2])

with col_e:
    total_snapshot_income = sum(
        snapshot["bond_income"]
        for snapshot in snapshots
    )

    rows_html = ""

    for snapshot in snapshots:
        row_total = (
            snapshot["us_equity"]
            + snapshot["bond_fund"]
        )

        unrealized = (
            row_total - total_cost_basis
            if row_total > 0
            else 0
        )

        unrealized_class = (
            "val-pos"
            if unrealized > 0
            else "val-neg"
            if unrealized < 0
            else "val-zero"
        )

        if row_total > 0:
            unrealized_text = (
                f"+₱{unrealized:,.2f}"
                if unrealized > 0
                else f"₱{unrealized:,.2f}"
            )
        else:
            unrealized_text = (
                '<span class="empty-val">Pending</span>'
            )

        if snapshot["official"]:
            badge = (
                '<span class="badge-official">'
                "✦ Official"
                "</span>"
            )
            row_class = "snap-official"
        elif snapshot["planned"]:
            badge = (
                '<span class="badge-planned">'
                "⏳ Planned"
                "</span>"
            )
            row_class = "snap-planned"
        else:
            badge = ""
            row_class = ""

        equity_text = fmt_value(
            snapshot["us_equity"]
        )

        bond_text = fmt_value(
            snapshot["bond_fund"]
        )

        total_text = (
            fmt_value(row_total)
            if row_total > 0
            else '<span class="empty-val">Pending</span>'
        )

        income_text = fmt_value(
            snapshot["bond_income"]
        )

        pera_text = fmt_value(
            snapshot.get("pera_balance", 0.0)
        )

        rows_html += (
            f"<tr class='{row_class}'>"
            f"<td>{get_snap_date(snapshot)}{badge}</td>"
            f"<td>{equity_text}</td>"
            f"<td>{bond_text}</td>"
            f"<td>{total_text}</td>"
            f"<td class='{unrealized_class}'>"
            f"{unrealized_text}"
            f"</td>"
            f"<td>{income_text}</td>"
            f"<td>{pera_text}</td>"
            "</tr>"
        )

    rows_html += f"""
    <tr class='snap-total-row'>
        <td>TOTAL BOND INCOME / LATEST PERA</td>
        <td>—</td>
        <td>—</td>
        <td>—</td>
        <td>—</td>
        <td>₱{total_snapshot_income:.2f}</td>
        <td>{fmt_value(latest_pera_balance)}</td>
    </tr>
    """

    st.markdown(
        f"""
        <div style="
            background:#fff;
            border:1px solid #E8D6CB;
            border-radius:14px;
            overflow:hidden;
            box-shadow:0 2px 8px rgba(55,63,81,0.05);
        ">
            <table class="snap-table">
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>US Equity Feeder</th>
                        <th>Global Bond</th>
                        <th>Total</th>
                        <th>Unrealized G/L</th>
                        <th>Bond Income</th>
                        <th>PERA Balance</th>
                    </tr>
                </thead>

                <tbody>
                    {rows_html}
                </tbody>
            </table>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.caption(
        "✦ Official = verified from BPI app   "
        "⏳ Planned = future projection   "
        "G/L uses total cost basis (carryover + this year's investments). "
        "PERA tracked separately since it's locked until retirement."
    )


with col_f:
    if actual_snapshots:
        dates = [
            get_snap_date(snapshot)
            for snapshot in actual_snapshots
        ]

        equities = [
            snapshot["us_equity"]
            for snapshot in actual_snapshots
        ]

        bonds = [
            snapshot["bond_fund"]
            for snapshot in actual_snapshots
        ]

        totals = [
            equity + bond
            for equity, bond in zip(
                equities,
                bonds,
            )
        ]

        fig = go.Figure()

        fig.add_bar(
            x=dates,
            y=equities,
            name="US Equity",
            marker_color="#6EA4BF",
            opacity=0.9,
        )

        fig.add_bar(
            x=dates,
            y=bonds,
            name="Bond Fund",
            marker_color="#0B3954",
            opacity=0.9,
        )

        fig.add_scatter(
            x=dates,
            y=totals,
            name="Total",
            mode="lines+markers",
            line=dict(
                color="#D0ADA7",
                width=2,
                dash="dot",
            ),
            marker=dict(
                size=7,
                color="#D0ADA7",
            ),
        )

        layout = base_layout(
            "Actual Portfolio Snapshots",
            240,
        )

        layout["barmode"] = "stack"

        fig.update_layout(**layout)

        fig.update_xaxes(
            showgrid=False,
            color=TEXT,
        )

        fig.update_yaxes(
            showgrid=True,
            gridcolor=GRID,
            color=SUBTEXT,
            tickprefix="₱",
            tickformat=",",
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    else:
        st.info(
            "Add official snapshots to see the portfolio chart."
        )

    if portfolio_value > 0:
        fig = go.Figure(
            go.Pie(
                labels=[
                    "US Equity Feeder",
                    "Global Bond Fund",
                ],
                values=[
                    latest_equity,
                    latest_bond,
                ],
                hole=0.6,
                marker_colors=[
                    "#6EA4BF",
                    "#0B3954",
                ],
                textinfo="label+percent",
                textfont_size=10,
            )
        )

        fig.update_layout(
            **base_layout(
                "Portfolio Allocation",
                200,
            )
        )

        fig.update_layout(
            showlegend=False,
            margin=dict(
                l=10,
                r=10,
                t=40,
                b=10,
            ),
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    st.markdown(
        f"""
        <div style="
            display:grid;
            grid-template-columns:1fr 1fr;
            gap:10px;
            margin-top:8px;
        ">
            <div class="kpi-card" style="padding:14px 12px;">
                <div class="kpi-label">
                    Unrealized G/L
                </div>

                <div class="kpi-value {
                    'kpi-neg'
                    if unrealized_pnl < 0
                    else 'kpi-pos'
                }" style="font-size:20px;">
                    {
                        '+' if unrealized_pnl >= 0 else ''
                    }₱{unrealized_pnl:,.2f}
                </div>

                <div class="kpi-sub">
                    vs ₱{total_cost_basis:,} basis
                </div>
            </div>

            <div class="kpi-card" style="padding:14px 12px;">
                <div class="kpi-label">
                    Net P&L
                </div>

                <div class="kpi-value {
                    'kpi-neg'
                    if net_pnl < 0
                    else 'kpi-pos'
                }" style="font-size:20px;">
                    {
                        '+' if net_pnl >= 0 else ''
                    }₱{net_pnl:,.2f}
                </div>

                <div class="kpi-sub">
                    unrealized + bond income
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# MONTHLY TRACKER
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown(
    '<div class="section-header">📋 Monthly Tracker</div>',
    unsafe_allow_html=True,
)

tracker_df = pd.DataFrame(
    [
        {
            "Month": month,
            "Insurance": FIXED_INSURANCE[index],
            "Investments": FIXED_INVESTMENTS[index],
            "Savings Deposited": income_map[month],
            "Money Spent": expenses_map[month],
            "Kept for Future": (
                income_map[month]
                - expenses_map[month]
                - FIXED_INVESTMENTS[index]
                - FIXED_INSURANCE[index]
            ),
            "Notes": NOTES[index],
        }
        for index, month in enumerate(MONTHS)
    ]
)

tracker_df["Cumulative"] = (
    tracker_df["Kept for Future"].cumsum()
)


for column in [
    "Insurance",
    "Investments",
    "Savings Deposited",
    "Money Spent",
    "Kept for Future",
    "Cumulative",
]:
    tracker_df[column] = tracker_df[column].apply(
        lambda value: f"₱{value:,.0f}"
    )


def highlight_negative(row):
    value = int(
        row["Kept for Future"]
        .replace("₱", "")
        .replace(",", "")
    )

    if value < 0:
        return [
            "background-color:#fdf3f0;color:#8c3a3a"
        ] * len(row)

    return [""] * len(row)


st.dataframe(
    tracker_df.style.apply(
        highlight_negative,
        axis=1,
    ),
    use_container_width=True,
    hide_index=True,
    height=460,
)


# ═══════════════════════════════════════════════════════════════════════════════
# INSIGHTS
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown(
    '<div class="section-header">🔍 Insights</div>',
    unsafe_allow_html=True,
)

col_g, col_h = st.columns(2)

with col_g:
    st.markdown("**Cash Flow**")

    st.markdown(
        f'<div class="insight-pos">🏆 Best month: '
        f'<b>{best_month}</b></div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div class="insight-neg">⚠️ Toughest month: '
        f'<b>{worst_month}</b></div>',
        unsafe_allow_html=True,
    )

    if negative_months:
        st.markdown(
            f'<div class="insight-neg">🔴 Months in the red: '
            f'<b>{", ".join(negative_months)}</b></div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="insight-pos">✅ No negative months this year</div>',
            unsafe_allow_html=True,
        )

    if floor_months:
        st.markdown(
            f'<div class="insight-neg">⚡ Below ₱{SAVINGS_FLOOR:,} '
            f'floor: <b>{", ".join(floor_months)}</b></div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        f'<div class="insight-neu">📊 Savings rate: '
        f'<b>{savings_rate_ytd:.1f}%</b> of income kept</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div class="insight-neu">💹 Investment ratio: '
        f'<b>{invest_vs_save:.1f}%</b> of deposits</div>',
        unsafe_allow_html=True,
    )


with col_h:
    st.markdown("**Investments & Passive Income**")

    st.markdown(
        f'<div class="insight-pos">💸 Passive provision so far: '
        f'<b>₱{bond_income_ytd:,.2f}</b></div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div class="insight-neu">📈 {selected_year} investments deployed: '
        f'<b>₱{total_investments:,.0f}</b></div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div class="insight-neu">🌱 {CARRYOVER["year"]} carryover invested: '
        f'<b>₱{cost_basis_prior:,.0f}</b></div>',
        unsafe_allow_html=True,
    )

    if portfolio_value > 0:
        st.markdown(
            f'<div class="insight-neu">🥧 Allocation: '
            f'<b>{equity_pct:.0f}% equity / '
            f'{bond_pct:.0f}% bond</b></div>',
            unsafe_allow_html=True,
        )

        months_of_expenses = (
            bond_income_ytd
            / (total_expenses / 12)
            if total_expenses > 0
            else 0
        )

        st.markdown(
            f'<div class="insight-pos">📅 Bond income covers ~'
            f'<b>{months_of_expenses:.1f} months</b> '
            f'of avg expenses</div>',
            unsafe_allow_html=True,
        )

    if pera_contributions_ytd > 0:
        st.markdown(
            f'<div class="insight-neu">🏦 PERA contributions: '
            f'<b>₱{pera_contributions_ytd:,.0f}</b> '
            f'({pera_cap_pct:.0f}% of cap)</div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        f'<div class="insight-neu">💰 Net P&L: '
        f'<b>{"+" if net_pnl >= 0 else ""}'
        f'₱{net_pnl:,.2f}</b></div>',
        unsafe_allow_html=True,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("---")

st.markdown(
    f"""
    > *"Keiza, this year you're building on ₱{CARRYOVER['total']:,.0f}
    > carried over from {CARRYOVER['year']} — money you earned while
    > studying, serving, and trusting God for provision. Every peso here
    > is a testimony. Keep building. Keep giving. Keep the faith."*
    """
)

st.caption(
    "Remember Keiza: you're saving up for your future. It'll be hard, "
    "there will be times when you want to spend your hard-earned money — "
    "but think about your future self. You want to provide for your family, "
    "give generously, and enjoy the fruits of your labor without worry. "
    "Stay disciplined. Stay focused. Keep your eyes on the prize. "
    "But never forget that money is replaceable — prioritize your present "
    "self when worse comes to worst. God will provide, and He will always "
    "provide more than enough."
)

st.markdown(
    f"""
    <div style="
        text-align:center;
        color:#D0ADA7;
        font-size:11px;
        letter-spacing:1px;
    ">
        Built by Kei · {selected_year} Financial Overview ·
        Streamlit + Plotly + Supabase
    </div>
    """,
    unsafe_allow_html=True,
)

st.caption(
    f"Last updated: {datetime.now().strftime('%B %d, %Y • %I:%M %p')}"
)
