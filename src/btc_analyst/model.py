from __future__ import annotations

from dataclasses import dataclass

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, f1_score, precision_score, recall_score

from btc_analyst.features import FEATURE_COLUMNS


@dataclass
class TrainResult:
    model: RandomForestClassifier
    metrics: dict
    feature_importance: pd.DataFrame
    predictions: pd.DataFrame


def train_direction_model(features: pd.DataFrame, test_size: float = 0.25) -> TrainResult:
    if not 0.0 < test_size < 1.0:
        raise ValueError("test_size muss zwischen 0 und 1 liegen.")

    split_index = int(len(features) * (1 - test_size))
    if split_index <= 0 or split_index >= len(features):
        raise ValueError("Train/Test-Split nicht moeglich. Bitte mehr Daten oder anderes test_size verwenden.")

    train = features.iloc[:split_index].copy()
    test = features.iloc[split_index:].copy()

    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=6,
        min_samples_leaf=5,
        random_state=42,
    )
    model.fit(train[FEATURE_COLUMNS], train["target"])

    predicted = model.predict(test[FEATURE_COLUMNS])
    probability_up = model.predict_proba(test[FEATURE_COLUMNS])[:, 1]
    metrics = {
        "train_rows": int(len(train)),
        "test_rows": int(len(test)),
        "accuracy": float(accuracy_score(test["target"], predicted)),
        "precision": float(precision_score(test["target"], predicted, zero_division=0)),
        "recall": float(recall_score(test["target"], predicted, zero_division=0)),
        "f1_score": float(f1_score(test["target"], predicted, zero_division=0)),
        "classification_report": classification_report(test["target"], predicted, zero_division=0),
    }

    importance = pd.DataFrame(
        {
            "feature": FEATURE_COLUMNS,
            "importance": model.feature_importances_,
        }
    ).sort_values("importance", ascending=False)

    predictions = test[
        [
            "Date",
            "Close",
            "target",
            "next_return",
            "volatility_30d",
            "trend_strength_30d",
            "sma_30_ratio",
            "intraday_range",
            "distance_to_52w_high",
        ]
    ].copy()
    predictions["prediction"] = predicted
    predictions["prob_up"] = probability_up
    return TrainResult(model=model, metrics=metrics, feature_importance=importance, predictions=predictions)


def save_model(model: RandomForestClassifier, output_path) -> None:
    joblib.dump(model, output_path)
