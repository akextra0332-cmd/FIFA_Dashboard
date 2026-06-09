"""
app.py — Main Streamlit Dashboard Application
FIFA Men's International Football Results Dashboard
EDA Project — Exploratory Data Analysis Course

Run:  streamlit run app.py
"""

import os
import sys
import tempfile

import pandas as pd
import numpy as np
import streamlit as st

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FIFA Results Dashboard",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Main background */
    .stApp { background-color: #f0f4f8; }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(160deg, #1a3a5c 0%, #0d2035 100%);
    }
    section[data-testid="stSidebar"] * { color: #e0eaf4 !important; }
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stMultiSelect label,
    section[data-testid="stSidebar"] .stSlider label,
    section[data-testid="stSidebar"] .stTextInput label { color: #a8c8e8 !important; }

    /* KPI cards */
    .kpi-card {
        background: white;
        border-radius: 12px;
        padding: 18px 22px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border-left: 4px solid #1a3a5c;
    }
    .kpi-value { font-size: 2rem; font-weight: 700; color: #1a3a5c; }
    .kpi-label { font-size: 0.82rem; color: #6c757d; margin-top: 2px; }

    /* Section headers */
    .section-title {
        font-size: 1.1rem; font-weight: 600; color: #1a3a5c;
        border-bottom: 2px solid #e63946; padding-bottom: 4px; margin-bottom: 12px;
    }

    /* Reset button */
    .stButton button {
        background: #e63946; color: white; border-radius: 8px;
        border: none; width: 100%; font-weight: 600;
    }
    .stButton button:hover { background: #c1121f; }
</style>
""", unsafe_allow_html=True)

# ── Load data & modules ───────────────────────────────────────────────────────
sys.path.insert(0, os.path.dirname(__file__))
from filters import load_data, apply_filters, get_team_stats
import charts as ch

@st.cache_data
def get_data():
    return load_data("data/results.csv")

df_raw = get_data()

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚽ FIFA Dashboard")
    st.markdown("*International Football Results*")
    st.markdown("---")

    # 1. Year range slider
    st.markdown("### 📅 Year Range")
    min_yr, max_yr = int(df_raw["year"].min()), int(df_raw["year"].max())
    year_range = st.slider("Select Year Range", min_yr, max_yr, (1990, max_yr))

    # 2. Tournament multi-select
    st.markdown("### 🏆 Tournament")
    all_tournaments = sorted(df_raw["tournament"].unique().tolist())
    selected_tournaments = st.multiselect(
        "Select Tournament(s)",
        options=all_tournaments,
        default=[],
        placeholder="All tournaments",
    )

    # 3. Team multi-select
    st.markdown("### 🌍 Team Filter")
    all_teams = sorted(set(df_raw["home_team"].tolist() + df_raw["away_team"].tolist()))
    selected_teams = st.multiselect(
        "Select Team(s)",
        options=all_teams,
        default=[],
        placeholder="All teams",
    )

    # 4. Result filter
    st.markdown("### 🎯 Match Result")
    result_options = ["Home Win", "Draw", "Away Win"]
    selected_results = st.multiselect(
        "Select Result(s)",
        options=result_options,
        default=[],
        placeholder="All results",
    )

    # 5. Text search
    st.markdown("### 🔍 Search")
    search_text = st.text_input("Search by team, city or country", placeholder="e.g. Brazil")

    # 6. Reset button
    st.markdown("---")
    if st.button("🔄 Reset All Filters"):
        st.rerun()

# ── Apply filters ─────────────────────────────────────────────────────────────
df = apply_filters(
    df_raw,
    year_range=year_range,
    tournaments=selected_tournaments if selected_tournaments else None,
    teams=selected_teams if selected_teams else None,
    search_text=search_text,
    result_filter=selected_results if selected_results else None,
)

# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown("""
<h1 style='text-align:center; color:#1a3a5c; font-size:2.2rem; margin-bottom:0;'>
    ⚽ FIFA Men's International Football Results
</h1>
<p style='text-align:center; color:#6c757d; font-size:1rem; margin-top:4px;'>
    Exploratory Data Analysis Dashboard &nbsp;|&nbsp; International Matches 1872 – 2023
</p>
<hr style='border:1px solid #dee2e6; margin:12px 0 20px;'>
""", unsafe_allow_html=True)

# ── KPI CARDS ─────────────────────────────────────────────────────────────────
k1, k2, k3, k4, k5, k6 = st.columns(6)

total_matches   = len(df)
total_goals     = int(df["total_goals"].sum())
avg_goals       = round(df["total_goals"].mean(), 2) if total_matches > 0 else 0
highest_score   = int(df["total_goals"].max()) if total_matches > 0 else 0
home_wins_pct   = round((df["result"] == "Home Win").mean() * 100, 1) if total_matches > 0 else 0
unique_teams    = len(set(df["home_team"].tolist() + df["away_team"].tolist()))

def kpi(col, value, label):
    col.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">{value}</div>
        <div class="kpi-label">{label}</div>
    </div>""", unsafe_allow_html=True)

kpi(k1, f"{total_matches:,}", "Total Matches")
kpi(k2, f"{total_goals:,}", "Total Goals")
kpi(k3, f"{avg_goals}", "Avg Goals/Match")
kpi(k4, f"{highest_score}", "Highest Scoring Match")
kpi(k5, f"{home_wins_pct}%", "Home Win Rate")
kpi(k6, f"{unique_teams}", "Teams Represented")

st.markdown("<br>", unsafe_allow_html=True)

# ── CHARTS — Row 1 ────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">📊 Distribution & Composition</div>', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with tempfile.TemporaryDirectory() as tmpdir:

    # ── Chart 1: Pie Chart ────────────────────────────────────────────────────
    p_pie = os.path.join(tmpdir, "pie.png")
    ch.chart_result_pie(df, p_pie)
    with col1:
        st.image(p_pie, use_container_width=True)

    # ── Chart 2: Histogram ────────────────────────────────────────────────────
    p_hist = os.path.join(tmpdir, "hist.png")
    ch.chart_goals_histogram(df, p_hist)
    with col2:
        st.image(p_hist, use_container_width=True)

    # ── Chart 9: Count Plot ───────────────────────────────────────────────────
    p_count = os.path.join(tmpdir, "count.png")
    ch.chart_tournament_countplot(df, p_count)
    with col3:
        st.image(p_count, use_container_width=True)

    st.markdown('<div class="section-title">📈 Trends & Time Series</div>', unsafe_allow_html=True)
    col4, col5 = st.columns(2)

    # ── Chart 3: Line Chart ───────────────────────────────────────────────────
    p_line = os.path.join(tmpdir, "line.png")
    ch.chart_goals_over_time(df, p_line)
    with col4:
        st.image(p_line, use_container_width=True)

    # ── Chart 8: Area Chart ───────────────────────────────────────────────────
    p_area = os.path.join(tmpdir, "area.png")
    ch.chart_matches_area(df, p_area)
    with col5:
        st.image(p_area, use_container_width=True)

    st.markdown('<div class="section-title">🏅 Team & Match Analysis</div>', unsafe_allow_html=True)
    col6, col7 = st.columns([1.2, 0.8])

    # ── Chart 4: Bar Chart ────────────────────────────────────────────────────
    p_bar = os.path.join(tmpdir, "bar.png")
    ch.chart_top_teams_bar(df, p_bar)
    with col6:
        st.image(p_bar, use_container_width=True)

    # ── Chart 5: Scatter Plot ─────────────────────────────────────────────────
    p_scatter = os.path.join(tmpdir, "scatter.png")
    ch.chart_home_away_scatter(df, p_scatter)
    with col7:
        st.image(p_scatter, use_container_width=True)

    st.markdown('<div class="section-title">📦 Statistical Distributions</div>', unsafe_allow_html=True)
    col8, col9, col10 = st.columns(3)

    # ── Chart 6: Box Plot ─────────────────────────────────────────────────────
    p_box = os.path.join(tmpdir, "box.png")
    ch.chart_goals_boxplot(df, p_box)
    with col8:
        st.image(p_box, use_container_width=True)

    # ── Chart 10: Violin Plot ─────────────────────────────────────────────────
    p_violin = os.path.join(tmpdir, "violin.png")
    ch.chart_goals_violin(df, p_violin)
    with col9:
        st.image(p_violin, use_container_width=True)

    # ── Chart 7: Heatmap ──────────────────────────────────────────────────────
    p_heatmap = os.path.join(tmpdir, "heatmap.png")
    ch.chart_correlation_heatmap(df, p_heatmap)
    with col10:
        st.image(p_heatmap, use_container_width=True)

    st.markdown('<div class="section-title">🔬 Bonus: Pair Plot</div>', unsafe_allow_html=True)
    p_pair = os.path.join(tmpdir, "pair.png")
    ch.chart_pair_plot(df, p_pair)
    st.image(p_pair, use_container_width=True)

# ── TEAM STATS TABLE ──────────────────────────────────────────────────────────
st.markdown('<div class="section-title">📋 Team Performance Summary</div>', unsafe_allow_html=True)
stats_df = get_team_stats(df)
st.dataframe(
    stats_df,
    use_container_width=True,
    height=320,
    hide_index=True,
)

# ── RAW DATA ──────────────────────────────────────────────────────────────────
with st.expander("🗂️ View Filtered Raw Data"):
    st.dataframe(df, use_container_width=True, height=300, hide_index=True)
    st.caption(f"Showing {len(df):,} of {len(df_raw):,} records after filters.")

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<hr style='border:1px solid #dee2e6; margin-top:30px;'>
<p style='text-align:center; color:#adb5bd; font-size:0.8rem;'>
    ⚽ FIFA Men's International Football Results Dashboard &nbsp;|&nbsp;
    Built with Python · Pandas · Matplotlib · Seaborn · Streamlit
</p>
""", unsafe_allow_html=True)
