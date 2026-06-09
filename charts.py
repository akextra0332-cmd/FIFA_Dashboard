"""
charts.py — Chart and visualization functions
FIFA Men's International Football Results Dashboard
All charts use Matplotlib + Seaborn as required.
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns

# ── Consistent color palette ──────────────────────────────────────────────────
PALETTE = {
    "primary":   "#1a3a5c",
    "secondary": "#e63946",
    "accent":    "#f4a261",
    "green":     "#2a9d8f",
    "light":     "#457b9d",
    "bg":        "#f8f9fa",
    "text":      "#212529",
}

RESULT_COLORS = {
    "Home Win": PALETTE["primary"],
    "Draw":     PALETTE["accent"],
    "Away Win": PALETTE["secondary"],
}

sns.set_theme(style="whitegrid", font_scale=1.0)
plt.rcParams.update({
    "figure.facecolor": PALETTE["bg"],
    "axes.facecolor":   PALETTE["bg"],
    "axes.edgecolor":   "#cccccc",
    "axes.labelcolor":  PALETTE["text"],
    "xtick.color":      PALETTE["text"],
    "ytick.color":      PALETTE["text"],
    "text.color":       PALETTE["text"],
    "grid.color":       "#e0e0e0",
    "font.family":      "DejaVu Sans",
})


def _save(fig, path):
    fig.tight_layout()
    fig.savefig(path, dpi=120, bbox_inches="tight", facecolor=PALETTE["bg"])
    plt.close(fig)


# ── 1. Pie Chart ─────────────────────────────────────────────────────────────
def chart_result_pie(df: pd.DataFrame, save_path: str):
    counts = df["result"].value_counts()
    colors = [RESULT_COLORS.get(r, "#aaaaaa") for r in counts.index]
    fig, ax = plt.subplots(figsize=(6, 5))
    wedges, texts, autotexts = ax.pie(
        counts, labels=counts.index, autopct="%1.1f%%",
        colors=colors, startangle=140,
        wedgeprops={"edgecolor": "white", "linewidth": 2},
    )
    for t in autotexts:
        t.set_fontsize(10)
        t.set_color("white")
    ax.set_title("Match Result Distribution", fontsize=14, fontweight="bold", pad=15)
    _save(fig, save_path)


# ── 2. Histogram ─────────────────────────────────────────────────────────────
def chart_goals_histogram(df: pd.DataFrame, save_path: str):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(
        df["total_goals"], bins=range(0, df["total_goals"].max() + 2),
        color=PALETTE["primary"], edgecolor="white", linewidth=0.8, rwidth=0.85,
    )
    ax.set_title("Distribution of Total Goals Per Match", fontsize=14, fontweight="bold")
    ax.set_xlabel("Total Goals in Match", fontsize=12)
    ax.set_ylabel("Number of Matches", fontsize=12)
    mean_goals = df["total_goals"].mean()
    ax.axvline(mean_goals, color=PALETTE["secondary"], linestyle="--", linewidth=1.8, label=f"Mean = {mean_goals:.2f}")
    ax.legend(fontsize=10)
    _save(fig, save_path)


# ── 3. Line Chart ─────────────────────────────────────────────────────────────
def chart_goals_over_time(df: pd.DataFrame, save_path: str):
    yearly = df.groupby("year").agg(
        matches=("total_goals", "count"),
        avg_goals=("total_goals", "mean"),
    ).reset_index()
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(yearly["year"], yearly["avg_goals"], color=PALETTE["primary"],
            linewidth=2.2, marker="o", markersize=4, label="Avg Goals/Match")
    ax.fill_between(yearly["year"], yearly["avg_goals"], alpha=0.15, color=PALETTE["primary"])
    ax.set_title("Average Goals Per Match Over the Years", fontsize=14, fontweight="bold")
    ax.set_xlabel("Year", fontsize=12)
    ax.set_ylabel("Avg Goals per Match", fontsize=12)
    ax.legend(fontsize=10)
    _save(fig, save_path)


# ── 4. Bar Chart ─────────────────────────────────────────────────────────────
def chart_top_teams_bar(df: pd.DataFrame, save_path: str, n: int = 15):
    from filters import get_team_stats
    stats = get_team_stats(df).head(n)
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(stats["Team"][::-1], stats["Won"][::-1], color=PALETTE["primary"], edgecolor="white")
    for bar, val in zip(bars, stats["Won"][::-1]):
        ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height() / 2,
                str(val), va="center", fontsize=9, color=PALETTE["text"])
    ax.set_title(f"Top {n} Teams by Matches Won", fontsize=14, fontweight="bold")
    ax.set_xlabel("Matches Won", fontsize=12)
    ax.set_ylabel("Team", fontsize=12)
    _save(fig, save_path)


# ── 5. Scatter Plot ──────────────────────────────────────────────────────────
def chart_home_away_scatter(df: pd.DataFrame, save_path: str):
    color_map = {k: v for k, v in RESULT_COLORS.items()}
    colors = df["result"].map(color_map)
    fig, ax = plt.subplots(figsize=(8, 7))
    scatter = ax.scatter(
        df["home_score"], df["away_score"],
        c=colors, alpha=0.55, s=45, edgecolors="white", linewidth=0.4,
    )
    ax.set_title("Home Score vs Away Score (by Result)", fontsize=14, fontweight="bold")
    ax.set_xlabel("Home Score", fontsize=12)
    ax.set_ylabel("Away Score", fontsize=12)
    legend_patches = [mpatches.Patch(color=v, label=k) for k, v in RESULT_COLORS.items()]
    ax.legend(handles=legend_patches, fontsize=10)
    ax.plot([0, df["home_score"].max()], [0, df["home_score"].max()],
            "k--", linewidth=1, alpha=0.4, label="Equal score line")
    _save(fig, save_path)


# ── 6. Box Plot ──────────────────────────────────────────────────────────────
def chart_goals_boxplot(df: pd.DataFrame, save_path: str):
    top_tournaments = df["tournament"].value_counts().head(5).index.tolist()
    sub = df[df["tournament"].isin(top_tournaments)]
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(
        data=sub, x="tournament", y="total_goals", ax=ax,
        palette=[PALETTE["primary"], PALETTE["secondary"], PALETTE["accent"],
                 PALETTE["green"], PALETTE["light"]],
        width=0.5, flierprops={"marker": "o", "markersize": 4, "alpha": 0.5},
    )
    ax.set_title("Goals Distribution by Tournament", fontsize=14, fontweight="bold")
    ax.set_xlabel("Tournament", fontsize=12)
    ax.set_ylabel("Total Goals", fontsize=12)
    ax.tick_params(axis="x", rotation=20)
    _save(fig, save_path)


# ── 7. Heatmap ───────────────────────────────────────────────────────────────
def chart_correlation_heatmap(df: pd.DataFrame, save_path: str):
    cols = ["home_score", "away_score", "total_goals", "goal_diff", "year"]
    corr = df[cols].corr()
    fig, ax = plt.subplots(figsize=(7, 6))
    sns.heatmap(
        corr, annot=True, fmt=".2f", ax=ax,
        cmap=sns.diverging_palette(220, 20, as_cmap=True),
        linewidths=0.5, square=True,
        annot_kws={"size": 10},
    )
    ax.set_title("Feature Correlation Heatmap", fontsize=14, fontweight="bold")
    _save(fig, save_path)


# ── 8. Area Chart ────────────────────────────────────────────────────────────
def chart_matches_area(df: pd.DataFrame, save_path: str):
    yearly = df.groupby(["year", "result"]).size().unstack(fill_value=0).reset_index()
    for col in ["Home Win", "Draw", "Away Win"]:
        if col not in yearly.columns:
            yearly[col] = 0
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.stackplot(
        yearly["year"],
        yearly["Home Win"], yearly["Draw"], yearly["Away Win"],
        labels=["Home Win", "Draw", "Away Win"],
        colors=[PALETTE["primary"], PALETTE["accent"], PALETTE["secondary"]],
        alpha=0.85,
    )
    ax.set_title("Match Results Over Time (Stacked Area)", fontsize=14, fontweight="bold")
    ax.set_xlabel("Year", fontsize=12)
    ax.set_ylabel("Number of Matches", fontsize=12)
    ax.legend(loc="upper left", fontsize=10)
    _save(fig, save_path)


# ── 9. Count Plot ────────────────────────────────────────────────────────────
def chart_tournament_countplot(df: pd.DataFrame, save_path: str):
    top = df["tournament"].value_counts().head(8)
    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(top.index, top.values,
                  color=[PALETTE["primary"], PALETTE["secondary"], PALETTE["accent"],
                         PALETTE["green"], PALETTE["light"],
                         "#9c6644", "#6a4c93", "#52796f"],
                  edgecolor="white")
    for bar, val in zip(bars, top.values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                str(val), ha="center", va="bottom", fontsize=10)
    ax.set_title("Match Count by Tournament", fontsize=14, fontweight="bold")
    ax.set_xlabel("Tournament", fontsize=12)
    ax.set_ylabel("Number of Matches", fontsize=12)
    ax.tick_params(axis="x", rotation=25)
    _save(fig, save_path)


# ── 10. Violin Plot ──────────────────────────────────────────────────────────
def chart_goals_violin(df: pd.DataFrame, save_path: str):
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.violinplot(
        data=df, x="result", y="total_goals", ax=ax,
        palette=RESULT_COLORS, inner="box", cut=0,
    )
    ax.set_title("Goals Distribution by Match Result (Violin)", fontsize=14, fontweight="bold")
    ax.set_xlabel("Match Result", fontsize=12)
    ax.set_ylabel("Total Goals", fontsize=12)
    _save(fig, save_path)


# ── BONUS: Pair Plot ─────────────────────────────────────────────────────────
def chart_pair_plot(df: pd.DataFrame, save_path: str):
    cols = ["home_score", "away_score", "total_goals", "goal_diff"]
    sub = df[cols + ["result"]].dropna()
    g = sns.pairplot(
        sub, hue="result",
        palette=RESULT_COLORS,
        plot_kws={"alpha": 0.5, "s": 20},
        diag_kind="kde",
    )
    g.fig.suptitle("Pair Plot: Score & Goal Features", y=1.02, fontsize=13, fontweight="bold")
    g.fig.tight_layout()
    g.fig.savefig(save_path, dpi=110, bbox_inches="tight", facecolor=PALETTE["bg"])
    plt.close(g.fig)
