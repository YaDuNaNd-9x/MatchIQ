
import pandas as pd
from pathlib import Path

# --------------------------------------------------
# PATHS
# --------------------------------------------------

ROOT = Path(__file__).resolve().parents[2]

DATA_FILE = ROOT / "data/processed/epl_matches_cleaned.csv"
OUTPUT_DIR = ROOT / "data/processed"

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

df = pd.read_csv(DATA_FILE)

team_records = []

# --------------------------------------------------
# CALCULATE TEAM PERFORMANCE
# --------------------------------------------------

seasons = sorted(df["season"].unique())

for season in seasons:

    season_df = df[df["season"] == season]

    teams = sorted(
        set(season_df["home_team"]) |
        set(season_df["away_team"])
    )

    for team in teams:

        home = season_df[
            season_df["home_team"] == team
        ]

        away = season_df[
            season_df["away_team"] == team
        ]

        played = len(home) + len(away)

        wins = (
            (home["result"] == "H").sum()
            + (away["result"] == "A").sum()
        )

        draws = (
            (home["result"] == "D").sum()
            + (away["result"] == "D").sum()
        )

        losses = (
            (home["result"] == "A").sum()
            + (away["result"] == "H").sum()
        )

        goals_for = (
            home["home_goals"].sum()
            + away["away_goals"].sum()
        )

        goals_against = (
            home["away_goals"].sum()
            + away["home_goals"].sum()
        )

        goal_difference = goals_for - goals_against

        points = wins * 3 + draws

        home_wins = (home["result"] == "H").sum()
        away_wins = (away["result"] == "A").sum()

        home_draws = (home["result"] == "D").sum()
        away_draws = (away["result"] == "D").sum()

        home_losses = (home["result"] == "A").sum()
        away_losses = (away["result"] == "H").sum()

        win_percentage = (
            (wins / played) * 100 if played else 0
        )

        team_records.append({

            "season": season,
            "team": team,

            "matches_played": played,
            "wins": wins,
            "draws": draws,
            "losses": losses,

            "goals_for": goals_for,
            "goals_against": goals_against,
            "goal_difference": goal_difference,

            "points": points,
            "win_percentage": round(win_percentage, 2),

            "home_wins": home_wins,
            "home_draws": home_draws,
            "home_losses": home_losses,

            "away_wins": away_wins,
            "away_draws": away_draws,
            "away_losses": away_losses,

            "home_goals_scored": home["home_goals"].sum(),
            "away_goals_scored": away["away_goals"].sum(),

        })

# --------------------------------------------------
# CREATE STANDINGS DATAFRAME
# --------------------------------------------------

standings = pd.DataFrame(team_records)

standings = standings.sort_values(
    by=[
        "season",
        "points",
        "goal_difference",
        "goals_for"
    ],
    ascending=[True, False, False, False]
)

standings["position"] = (
    standings.groupby("season").cumcount() + 1
)

# --------------------------------------------------
# EXPORT SEASON-WISE STANDINGS
# --------------------------------------------------

standings_file = OUTPUT_DIR / "team_season_standings.csv"

standings.to_csv(standings_file, index=False)

# --------------------------------------------------
# OVERALL TEAM PERFORMANCE
# --------------------------------------------------

overall = (
    standings.groupby("team", as_index=False)
    .agg({
        "matches_played": "sum",
        "wins": "sum",
        "draws": "sum",
        "losses": "sum",
        "goals_for": "sum",
        "goals_against": "sum",
        "goal_difference": "sum",
        "points": "sum"
    })
)

overall["win_percentage"] = (
    overall["wins"] / overall["matches_played"] * 100
).round(2)

overall = overall.sort_values(
    by=["points", "goal_difference", "goals_for"],
    ascending=False
)

overall_file = OUTPUT_DIR / "team_overall_statistics.csv"

overall.to_csv(overall_file, index=False)

# --------------------------------------------------
# DISPLAY RESULTS
# --------------------------------------------------

print("=" * 65)
print("MATCHIQ - TEAM ANALYTICS")
print("=" * 65)

for season in seasons:

    print(f"\nSEASON: {season}")

    print(
        standings[standings["season"] == season][
            [
                "position",
                "team",
                "matches_played",
                "wins",
                "draws",
                "losses",
                "goal_difference",
                "points"
            ]
        ].head(10).to_string(index=False)
    )

print("\nTOP 10 OVERALL TEAMS")
print(
    overall.head(10).to_string(index=False)
)

print("\nTEAM ANALYTICS COMPLETED")
print("Season standings:", standings_file)
print("Overall statistics:", overall_file)
