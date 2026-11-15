import json
from collections import defaultdict
from functools import lru_cache
from pathlib import Path

import joblib
import pandas as pd

from django.db.models import Q

from matches.models import Match


PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODEL_DIR = PROJECT_ROOT / "machine-learning" / "match_prediction" / "models"
MODEL_PATH = MODEL_DIR / "matchiq_model.joblib"
METADATA_PATH = MODEL_DIR / "model_metadata.json"


@lru_cache(maxsize=1)
def load_model():
    if not MODEL_PATH.exists() or not METADATA_PATH.exists():
        raise FileNotFoundError(
            "Trained model not found. Run the ML training script first."
        )

    model = joblib.load(MODEL_PATH)

    with open(METADATA_PATH, "r", encoding="utf-8") as file:
        metadata = json.load(file)

    return model, metadata


def get_team_history(team):
    matches = Match.objects.filter(
        Q(home_team=team) | Q(away_team=team)
    ).select_related(
        "home_team", "away_team"
    ).order_by("-match_date", "-id")[:5]

    history = []

    for match in matches:
        if match.home_team_id == team.id:
            history.append({
                "points": float(match.home_points),
                "goals_for": float(match.home_goals),
                "goals_against": float(match.away_goals),
                "won": int(match.result == "H"),
            })
        else:
            history.append({
                "points": float(match.away_points),
                "goals_for": float(match.away_goals),
                "goals_against": float(match.home_goals),
                "won": int(match.result == "A"),
            })

    return history


def calculate_form(history):
    if not history:
        return {
            "avg_points": 0.0,
            "avg_goals_for": 0.0,
            "avg_goals_against": 0.0,
            "win_rate": 0.0,
            "matches_available": 0,
        }

    count = len(history)

    return {
        "avg_points": sum(x["points"] for x in history) / count,
        "avg_goals_for": sum(x["goals_for"] for x in history) / count,
        "avg_goals_against": sum(x["goals_against"] for x in history) / count,
        "win_rate": sum(x["won"] for x in history) / count,
        "matches_available": count,
    }


def predict_match(home_team, away_team):
    model, metadata = load_model()

    home_history = get_team_history(home_team)
    away_history = get_team_history(away_team)

    home_form = calculate_form(home_history)
    away_form = calculate_form(away_history)

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

    # Preserve exactly the feature order used during training.
    feature_columns = metadata["features"]
    input_data = pd.DataFrame(
        [[features[column] for column in feature_columns]],
        columns=feature_columns,
    )

    probabilities = model.predict_proba(input_data)[0]

    probability_map = {
        str(label): round(float(probability) * 100, 2)
        for label, probability in zip(model.classes_, probabilities)
    }

    predicted_result = str(model.predict(input_data)[0])

    result_labels = {
        "H": "Home Win",
        "D": "Draw",
        "A": "Away Win",
    }

    return {
        "home_team": home_team.name,
        "away_team": away_team.name,
        "predicted_result": predicted_result,
        "predicted_outcome": result_labels[predicted_result],
        "probabilities": {
            "home_win": probability_map.get("H", 0.0),
            "draw": probability_map.get("D", 0.0),
            "away_win": probability_map.get("A", 0.0),
        },
        "recent_form": {
            "home_matches_available": len(home_history),
            "away_matches_available": len(away_history),
        },
        "model": metadata["model_name"],
    }