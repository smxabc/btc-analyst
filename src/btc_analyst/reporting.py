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


def write_backtest_metrics(metrics: dict, output_path: Path) -> None:
    output_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")


def write_executive_summary(
    metrics: dict, backtest_metrics: dict, feature_importance: pd.DataFrame, output_path: Path
) -> None:
    top_features = feature_importance.head(5)
    lines = [
        "# Executive Summary",
        "",
        "## Objective",
        "Evaluate whether historical Bitcoin price and volume features can support daily Bitcoin decision-making.",
        "",
        "## Model Performance",
        f"- Accuracy: {metrics['accuracy']:.3f}",
        f"- Precision: {metrics['precision']:.3f}",
        f"- Recall: {metrics['recall']:.3f}",
        f"- F1 Score: {metrics['f1_score']:.3f}",
        f"- Train Rows: {metrics['train_rows']}",
        f"- Test Rows: {metrics['test_rows']}",
        "",
        "## Decision Intelligence Layer",
        f"- Strategy Return: {backtest_metrics['strategy_total_return']:.3%}",
        f"- Buy and Hold Return: {backtest_metrics['benchmark_total_return']:.3%}",
        f"- Alpha vs Buy and Hold: {backtest_metrics['alpha_vs_benchmark']:.3%}",
        f"- Strategy Max Drawdown: {backtest_metrics['strategy_max_drawdown']:.3%}",
        f"- Strategy Sharpe: {backtest_metrics['strategy_sharpe']:.3f}",
        f"- Average Risk Score: {backtest_metrics['avg_risk_score']:.1f}/100",
        f"- Average Confidence Score: {backtest_metrics['avg_confidence_score']:.3f}",
        "",
        "## Top Drivers",
    ]

    for _, row in top_features.iterrows():
        lines.append(f"- {row['feature']}: {row['importance']:.4f}")

    lines.extend(
        [
            "",
            "## Interpretation",
            "The project now goes beyond next-day classification and converts probabilities into actionable signals, risk scoring, and backtested decisions.",
            "It should still be treated as a research and decision-support tool, not as fully automated financial advice.",
        ]
    )

    output_path.write_text("\n".join(lines), encoding="utf-8")
