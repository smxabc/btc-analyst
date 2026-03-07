from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


def write_metrics(metrics: dict, output_path: Path) -> None:
    output_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")


def write_feature_importance(feature_importance: pd.DataFrame, output_path: Path) -> None:
    feature_importance.to_csv(output_path, index=False)


def write_predictions(predictions: pd.DataFrame, output_path: Path) -> None:
    predictions.to_csv(output_path, index=False)


def write_executive_summary(metrics: dict, feature_importance: pd.DataFrame, output_path: Path) -> None:
    top_features = feature_importance.head(5)
    lines = [
        "# Executive Summary",
        "",
        "## Objective",
        "Evaluate whether historical Bitcoin price and volume features can help classify the next day's market direction.",
        "",
        "## Model Performance",
        f"- Accuracy: {metrics['accuracy']:.3f}",
        f"- Precision: {metrics['precision']:.3f}",
        f"- Recall: {metrics['recall']:.3f}",
        f"- F1 Score: {metrics['f1_score']:.3f}",
        f"- Train Rows: {metrics['train_rows']}",
        f"- Test Rows: {metrics['test_rows']}",
        "",
        "## Top Drivers",
    ]

    for _, row in top_features.iterrows():
        lines.append(f"- {row['feature']}: {row['importance']:.4f}")

    lines.extend(
        [
            "",
            "## Interpretation",
            "The model should be treated as an analytics demonstration rather than a trading system.",
            "Its value for a portfolio lies in the full workflow: sourcing data, designing features, testing a hypothesis, and translating outputs into business-facing insights.",
        ]
    )

    output_path.write_text("\n".join(lines), encoding="utf-8")

