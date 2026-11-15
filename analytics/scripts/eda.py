
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# --------------------------------------------------
# PATHS
# --------------------------------------------------

ROOT = Path(__file__).resolve().parents[2]

DATA_FILE = ROOT / "data/processed/epl_matches_cleaned.csv"
OUTPUT_DIR = ROOT / "analytics/visualizations"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

df = pd.read_csv(DATA_FILE)
df["match_date"] = pd.to_datetime(df["match_date"])

print("=" * 60)
print("MATCHIQ - EXPLORATORY DATA ANALYSIS")
print("=" * 60)

print("\nDataset shape:", df.shape)
print("\nColumns:", list(df.columns))
print("\nData types:\n", df.dtypes)

# --------------------------------------------------
# 1. MATCH OUTCOME DISTRIBUTION
# --------------------------------------------------

outcomes = df["result"].value_counts().reindex(
    ["H", "D", "A"], fill_value=0
)

plt.figure(figsize=(9, 5))
outcomes.plot(kind="bar")
plt.title("EPL Match Outcome Distribution")
plt.xlabel("Match Result")
plt.ylabel("Number of Matches")
plt.xticks(
    range(3),
    ["Home Wins", "Draws", "Away Wins"],
    rotation=0
)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "match_outcomes.png", dpi=150)
plt.close()

# --------------------------------------------------
# 2. AVERAGE GOALS BY SEASON
# --------------------------------------------------

season_goals = df.groupby("season")["total_goals"].mean()

plt.figure(figsize=(10, 5))
season_goals.plot(marker="o", linewidth=2)
plt.title("Average Goals Per Match by Season")
plt.xlabel("Season")
plt.ylabel("Average Goals")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "average_goals_by_season.png", dpi=150)
plt.close()

# --------------------------------------------------
# 3. TOP 10 ATTACKING TEAMS
# --------------------------------------------------

home_goals = df.groupby("home_team")["home_goals"].sum()
away_goals = df.groupby("away_team")["away_goals"].sum()

team_goals = home_goals.add(away_goals, fill_value=0)
top_attacking = team_goals.sort_values(ascending=False).head(10)

plt.figure(figsize=(11, 6))
top_attacking.sort_values().plot(kind="barh")
plt.title("Top 10 EPL Teams by Goals Scored")
plt.xlabel("Total Goals")
plt.ylabel("Team")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "top_attacking_teams.png", dpi=150)
plt.close()

# --------------------------------------------------
# 4. MATCH GOAL DISTRIBUTION
# --------------------------------------------------

plt.figure(figsize=(9, 5))
plt.hist(df["total_goals"], bins=range(
    0, int(df["total_goals"].max()) + 2
), edgecolor="black")

plt.title("Distribution of Goals Per Match")
plt.xlabel("Total Goals in Match")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "goal_distribution.png", dpi=150)
plt.close()

# --------------------------------------------------
# 5. HOME VS AWAY GOALS
# --------------------------------------------------

home_average = df["home_goals"].mean()
away_average = df["away_goals"].mean()

plt.figure(figsize=(8, 5))
plt.bar(
    ["Home Goals", "Away Goals"],
    [home_average, away_average]
)
plt.title("Average Home vs Away Goals")
plt.ylabel("Average Goals Per Match")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "home_vs_away_goals.png", dpi=150)
plt.close()

# --------------------------------------------------
# 6. MATCH OUTCOMES BY SEASON
# --------------------------------------------------

season_outcomes = pd.crosstab(
    df["season"],
    df["result"]
).reindex(columns=["H", "D", "A"], fill_value=0)

season_outcomes.columns = [
    "Home Wins", "Draws", "Away Wins"
]

season_outcomes.plot(
    kind="bar",
    figsize=(11, 6),
    width=0.8
)

plt.title("Match Outcomes Across EPL Seasons")
plt.xlabel("Season")
plt.ylabel("Number of Matches")
plt.xticks(rotation=0)
plt.legend(title="Result")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "season_outcomes.png", dpi=150)
plt.close()

# --------------------------------------------------
# STATISTICAL REPORT
# --------------------------------------------------

report = []

report.append("MATCHIQ - EDA STATISTICAL REPORT")
report.append("=" * 50)

report.append(f"\nTotal matches: {len(df)}")
report.append(
    f"Unique teams: {len(set(df.home_team) | set(df.away_team))}"
)

report.append(
    f"\nDate range: {df.match_date.min()} to {df.match_date.max()}"
)

report.append(
    f"\nAverage goals per match: {df.total_goals.mean():.2f}"
)

report.append(
    f"Average home goals: {home_average:.2f}"
)

report.append(
    f"Average away goals: {away_average:.2f}"
)

report.append("\nMatch outcome distribution:")
report.append(outcomes.to_string())

report.append("\nAverage goals by season:")
report.append(season_goals.to_string())

report.append("\nTop 10 attacking teams:")
report.append(top_attacking.to_string())

report_text = "\n".join(report)

report_file = OUTPUT_DIR / "eda_report.txt"
report_file.write_text(report_text, encoding="utf-8")

print("\n" + report_text)

print("\nEDA COMPLETED SUCCESSFULLY")
print("Visualizations saved to:", OUTPUT_DIR)
