
import json
import pandas as pd
from pathlib import Path

# --------------------------------------------------
# PATH CONFIGURATION
# --------------------------------------------------

ROOT_DIR = Path(__file__).resolve().parents[2]

RAW_DIR = ROOT_DIR / "data" / "raw" / "football_json"
PROCESSED_DIR = ROOT_DIR / "data" / "processed"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# LOAD RAW DATA
# --------------------------------------------------

def load_matches():

    all_matches = []

    files = sorted(RAW_DIR.glob("epl_*.json"))

    if not files:
        raise FileNotFoundError("No EPL JSON files found.")

    for file in files:

        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)

        season = file.stem.replace("epl_", "")

        for match in data.get("matches", []):

            score = match.get("score") or {}
            full_time = score.get("ft")
            half_time = score.get("ht")

            # Exclude matches without valid full-time scores
            if (
                not isinstance(full_time, list)
                or len(full_time) != 2
                or any(x is None for x in full_time)
            ):
                continue

            home_goals, away_goals = full_time

            if not isinstance(home_goals, int) or not isinstance(away_goals, int):
                continue

            home_team = str(match.get("team1", "")).strip()
            away_team = str(match.get("team2", "")).strip()

            if not home_team or not away_team:
                continue

            ht_home = None
            ht_away = None

            if (
                isinstance(half_time, list)
                and len(half_time) == 2
                and all(isinstance(x, int) for x in half_time)
            ):
                ht_home, ht_away = half_time

            # Determine match outcome
            if home_goals > away_goals:
                result = "H"
                home_points, away_points = 3, 0

            elif home_goals < away_goals:
                result = "A"
                home_points, away_points = 0, 3

            else:
                result = "D"
                home_points, away_points = 1, 1

            all_matches.append({
                "season": season,
                "round": match.get("round"),
                "match_date": match.get("date"),
                "home_team": home_team,
                "away_team": away_team,
                "half_time_home_goals": ht_home,
                "half_time_away_goals": ht_away,
                "home_goals": home_goals,
                "away_goals": away_goals,
                "total_goals": home_goals + away_goals,
                "goal_difference": home_goals - away_goals,
                "result": result,
                "home_points": home_points,
                "away_points": away_points
            })

    return pd.DataFrame(all_matches)


# --------------------------------------------------
# DATA CLEANING
# --------------------------------------------------

def clean_data(df):

    print("\nStarting data cleaning...")

    initial_count = len(df)

    # Convert dates
    df["match_date"] = pd.to_datetime(
        df["match_date"], errors="coerce"
    )

    # Remove invalid dates
    df = df.dropna(subset=["match_date"])

    # Remove duplicate matches
    df = df.drop_duplicates(
        subset=[
            "season",
            "match_date",
            "home_team",
            "away_team"
        ]
    )

    # Remove invalid scores
    df = df[
        (df["home_goals"] >= 0)
        & (df["away_goals"] >= 0)
    ]

    # Standardize text fields
    for column in ["home_team", "away_team", "season"]:
        df[column] = df[column].str.strip()

    # Sort chronologically
    df = df.sort_values(
        by=["match_date", "home_team"]
    ).reset_index(drop=True)

    # Generate unique match identifier
    df.insert(
        0,
        "match_id",
        [f"MATCH_{i:05d}" for i in range(1, len(df) + 1)]
    )

    print("Initial records:", initial_count)
    print("Final records:", len(df))
    print("Duplicates / invalid records removed:", initial_count - len(df))

    return df


# --------------------------------------------------
# DATA QUALITY REPORT
# --------------------------------------------------

def generate_report(df):

    print("\n" + "=" * 60)
    print("MATCHIQ - DATA QUALITY REPORT")
    print("=" * 60)

    print("\nDataset shape:", df.shape)

    print("\nSeason distribution:")
    print(df["season"].value_counts().sort_index())

    print("\nMissing values:")
    print(df.isnull().sum())

    print("\nMatch outcome distribution:")
    print(df["result"].value_counts())

    print("\nTotal goals:", df["total_goals"].sum())

    print("\nAverage goals per match:",
          round(df["total_goals"].mean(), 2))

    print("\nUnique teams:",
          len(set(df["home_team"]) | set(df["away_team"])))

    print("\nDate range:")
    print(df["match_date"].min(), "to", df["match_date"].max())


# --------------------------------------------------
# SAVE PROCESSED DATA
# --------------------------------------------------

def main():

    print("=" * 60)
    print("MATCHIQ - FOOTBALL DATA PREPROCESSING")
    print("=" * 60)

    df = load_matches()

    print("\nLoaded records:", len(df))

    df = clean_data(df)

    generate_report(df)

    output_file = PROCESSED_DIR / "epl_matches_cleaned.csv"

    df.to_csv(output_file, index=False)

    print("\nProcessed dataset saved successfully!")
    print("Location:", output_file)

    print("\nFirst five records:")
    print(df.head().to_string(index=False))


if __name__ == "__main__":
    main()
