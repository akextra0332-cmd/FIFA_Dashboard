"""
filters.py — Data loading and filtering functions
FIFA Men's International Football Results Dashboard
"""

import pandas as pd
import numpy as np


def load_data(filepath: str = "data/results.csv") -> pd.DataFrame:
    """Load and preprocess the FIFA results dataset."""
    df = pd.read_csv(filepath)

    # Parse dates
    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].dt.year
    df["decade"] = (df["year"] // 10 * 10).astype(str) + "s"

    # Scores to int
    df["home_score"] = pd.to_numeric(df["home_score"], errors="coerce").fillna(0).astype(int)
    df["away_score"] = pd.to_numeric(df["away_score"], errors="coerce").fillna(0).astype(int)

    # Derived columns
    df["total_goals"] = df["home_score"] + df["away_score"]
    df["goal_diff"] = abs(df["home_score"] - df["away_score"])

    df["result"] = df.apply(
        lambda r: "Home Win" if r["home_score"] > r["away_score"]
        else ("Away Win" if r["home_score"] < r["away_score"] else "Draw"),
        axis=1,
    )

    df["is_draw"] = df["result"] == "Draw"
    df["neutral"] = df["neutral"].map({"TRUE": True, "FALSE": False, True: True, False: False}).fillna(False)

    return df


def apply_filters(
    df: pd.DataFrame,
    year_range: tuple = None,
    tournaments: list = None,
    teams: list = None,
    search_text: str = "",
    result_filter: list = None,
) -> pd.DataFrame:
    """Apply all sidebar filters and return filtered DataFrame."""
    filtered = df.copy()

    # Year range filter
    if year_range:
        filtered = filtered[
            (filtered["year"] >= year_range[0]) & (filtered["year"] <= year_range[1])
        ]

    # Tournament multi-select
    if tournaments:
        filtered = filtered[filtered["tournament"].isin(tournaments)]

    # Team multi-select (home OR away)
    if teams:
        filtered = filtered[
            filtered["home_team"].isin(teams) | filtered["away_team"].isin(teams)
        ]

    # Text search across team names, city, country
    if search_text.strip():
        q = search_text.strip().lower()
        mask = (
            filtered["home_team"].str.lower().str.contains(q, na=False)
            | filtered["away_team"].str.lower().str.contains(q, na=False)
            | filtered["city"].str.lower().str.contains(q, na=False)
            | filtered["country"].str.lower().str.contains(q, na=False)
        )
        filtered = filtered[mask]

    # Result filter
    if result_filter:
        filtered = filtered[filtered["result"].isin(result_filter)]

    return filtered.reset_index(drop=True)


def get_team_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate per-team stats: played, won, drawn, lost, goals for/against."""
    records = []
    teams = sorted(set(df["home_team"].tolist() + df["away_team"].tolist()))

    for team in teams:
        home = df[df["home_team"] == team]
        away = df[df["away_team"] == team]

        played = len(home) + len(away)
        if played == 0:
            continue

        won = (home["result"] == "Home Win").sum() + (away["result"] == "Away Win").sum()
        drawn = (home["result"] == "Draw").sum() + (away["result"] == "Draw").sum()
        lost = (home["result"] == "Away Win").sum() + (away["result"] == "Home Win").sum()
        gf = home["home_score"].sum() + away["away_score"].sum()
        ga = home["away_score"].sum() + away["home_score"].sum()
        win_pct = round(won / played * 100, 1) if played > 0 else 0

        records.append({
            "Team": team,
            "Played": played,
            "Won": won,
            "Drawn": drawn,
            "Lost": lost,
            "Goals For": gf,
            "Goals Against": ga,
            "Goal Diff": gf - ga,
            "Win %": win_pct,
        })

    return pd.DataFrame(records).sort_values("Won", ascending=False).reset_index(drop=True)
