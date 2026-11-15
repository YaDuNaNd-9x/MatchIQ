import json
from pathlib import Path

import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from features import build_features


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CSV_PATH = PROJECT_ROOT / "data" / "processed" / "epl_matches_cleaned.csv"
MODEL_DIR = PROJECT_ROOT / "machine-learning" / "match_prediction" / "models"

MODEL_DIR.mkdir(parents=True, exist_ok=True)


def main():
    print("Building pre-match features...")
    data = build_features(CSV_PATH)

    feature_columns = [
        column for column in data.columns
        if column not in ["match_id", "match_date", "result"]
    ]

    X = data[feature_columns]
    y = data["result"]

    # Chronological split: older matches train, newer matches test.
    split_index = int(len(data) * 0.80)

    X_train = X.iloc[:split_index]
    X_test = X.iloc[split_index:]
    y_train = y.iloc[:split_index]
    y_test = y.iloc[split_index:]

    if y_train.nunique() < 2 or y_test.nunique() < 2:
        raise ValueError("Training or test data does not contain enough result classes.")

    print(f"Total matches: {len(data)}")
    print(f"Training matches: {len(X_train)}")
    print(f"Testing matches: {len(X_test)}")
    print(f"Training period: {data.iloc[0]['match_date'].date()} to "
          f"{data.iloc[split_index - 1]['match_date'].date()}")
    print(f"Testing period: {data.iloc[split_index]['match_date'].date()} to "
          f"{data.iloc[-1]['match_date'].date()}")

    models = {
        "logistic_regression": Pipeline([
            ("scaler", StandardScaler()),
            ("classifier", LogisticRegression(
                max_iter=2000,
                class_weight="balanced",
                random_state=42,
            )),
        ]),
        "random_forest": RandomForestClassifier(
            n_estimators=400,
            max_depth=8,
            min_samples_leaf=5,
            class_weight="balanced",
            random_state=42,
            n_jobs=-1,
        ),
    }

    results = {}
    best_model = None
    best_name = None
    best_score = -1

    for name, model in models.items():
        print(f"\nTraining {name}...")
        model.fit(X_train, y_train)

        predictions = model.predict(X_test)

        accuracy = accuracy_score(y_test, predictions)
        balanced_accuracy = balanced_accuracy_score(y_test, predictions)
        macro_f1 = f1_score(
            y_test, predictions, average="macro", zero_division=0
        )

        results[name] = {
            "accuracy": float(accuracy),
            "balanced_accuracy": float(balanced_accuracy),
            "macro_f1": float(macro_f1),
        }

        print(f"Accuracy:          {accuracy:.4f}")
        print(f"Balanced accuracy: {balanced_accuracy:.4f}")
        print(f"Macro F1:          {macro_f1:.4f}")

        if balanced_accuracy > best_score:
            best_score = balanced_accuracy
            best_model = model
            best_name = name
            best_predictions = predictions

    print(f"\nBest model: {best_name}")
    print("\nClassification report:")
    print(classification_report(
        y_test,
        best_predictions,
        labels=["H", "D", "A"],
        target_names=["Home Win", "Draw", "Away Win"],
        zero_division=0,
    ))

    print("Confusion matrix (rows = actual, columns = predicted):")
    print(confusion_matrix(y_test, best_predictions, labels=["H", "D", "A"]))

    model_path = MODEL_DIR / "matchiq_model.joblib"
    metadata_path = MODEL_DIR / "model_metadata.json"

    joblib.dump(best_model, model_path)

    metadata = {
        "model_name": best_name,
        "features": feature_columns,
        "classes": ["H", "D", "A"],
        "test_start_date": str(data.iloc[split_index]["match_date"].date()),
        "test_end_date": str(data.iloc[-1]["match_date"].date()),
        "training_matches": len(X_train),
        "testing_matches": len(X_test),
        "metrics": results,
    }

    metadata_path.write_text(json.dumps(metadata, indent=4))

    print("\nMODEL TRAINING COMPLETED")
    print(f"Saved model: {model_path}")
    print(f"Saved metadata: {metadata_path}")


if __name__ == "__main__":
    main()