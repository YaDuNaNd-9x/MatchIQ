from collections import defaultdict, deque

import pandas as pd


WINDOW = 5


def get_team_form(history):
    """Summarise a team's previous matches only."""
    if not history:
        return {
            "avg_points": 0.0,
            "avg_goals_for": 0.0,
            "avg_goals_against": 0.0,
            "win_rate": 0.0,
            "matches_available": 0,
        }

    return {
        "avg_points": sum(x["points"] for x in history) / len(history),
        "avg_goals_for": sum(x["goals_for"] for x in history) / len(history),
        "avg_goals_against": sum(x["goals_against"] for x in history) / len(history),
        "win_rate": sum(x["won"] for x in history) / len(history),
        "matches_available": len(history),
    }


def build_features(csv_path):
    df = pd.read_csv(csv_path)
    df["match_date"] = pd.to_datetime(df["match_date"])
    df = df.sort_values(["match_date", "match_id"]).reset_index(drop=True)

    required = {
        "match_date", "match_id", "home_team", "away_team",
        "home_goals", "away_goals", "home_points", "away_points", "result",
    }
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    history = defaultdict(lambda: deque(maxlen=WINDOW))
    feature_rows = []

    # Process each date as a group. No match on a date can use another
    # match's result from that same date.
    for _, date_group in df.groupby("match_date", sort=True):
        pending_updates = []

        for row in date_group.itertuples(index=False):
            home_form = get_team_form(history[row.home_team])
            away_form = get_team_form(history[row.away_team])

            features = {}

            for key, value in home_form.items():
                features[f"home_{key}"] = value

            for key, value in away_form.items():
                features[f"away_{key}"] = value

            for key in [
                "avg_points",
                "avg_goals_for",
                "avg_goals_against",
                "win_rate",
                "matches_available",
            ]:
                features[f"{key}_difference"] = (
                    home_form[key] - away_form[key]
                )

            features["home_advantage"] = 1

            feature_rows.append({
                "match_id": row.match_id,
                "match_date": row.match_date,
                "result": row.result,
                **features,
            })

            # Queue results for updating only after every match on this
            # date has had its pre-match features calculated.
            pending_updates.append((
                row.home_team,
                {
                    "points": float(row.home_points),
                    "goals_for": float(row.home_goals),
                    "goals_against": float(row.away_goals),
                    "won": int(row.result == "H"),
                },
                row.away_team,
                {
                    "points": float(row.away_points),
                    "goals_for": float(row.away_goals),
                    "goals_against": float(row.home_goals),
                    "won": int(row.result == "A"),
                },
            ))

        for home_team, home_record, away_team, away_record in pending_updates:
            history[home_team].append(home_record)
            history[away_team].append(away_record)

    return pd.DataFrame(feature_rows)