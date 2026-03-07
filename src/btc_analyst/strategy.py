from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass
class StrategyResult:
    enriched_predictions: pd.DataFrame
    backtest_metrics: dict


def classify_market_regime(row: pd.Series) -> str:
    if row["volatility_30d"] >= 0.05:
        return "high_volatility"
    if row["trend_strength_30d"] >= 1.03 and row["sma_30_ratio"] >= 1.0:
        return "bull_trend"
    if row["trend_strength_30d"] <= 0.98 and row["sma_30_ratio"] <= 1.0:
        return "bear_trend"
    return "range_bound"


def compute_risk_score(row: pd.Series) -> int:
    score = 50
    score += min(20, max(0, int(row["volatility_30d"] * 800)))
    score += 10 if row["intraday_range"] > 0.05 else 0
    score += 10 if row["distance_to_52w_high"] < 0.85 else 0
    score -= 10 if row["trend_strength_30d"] > 1.03 else 0
    return int(max(0, min(100, score)))


def compute_signal(row: pd.Series) -> str:
    probability = row["prob_up"]
    regime = row["market_regime"]
    risk_score = row["risk_score"]

    if probability >= 0.58 and risk_score <= 60 and regime in {"bull_trend", "range_bound"}:
        return "BUY"
    if probability <= 0.42 or risk_score >= 75 or regime == "bear_trend":
        return "REDUCE_RISK"
    return "HOLD"


def compute_position_size(row: pd.Series) -> float:
    if row["signal"] == "BUY":
        base_size = 1.0 if row["confidence_score"] >= 0.2 else 0.6
        if row["risk_score"] > 55:
            base_size *= 0.6
        return round(base_size, 2)
    if row["signal"] == "HOLD":
        return 0.35
    return 0.0


def enrich_predictions(predictions: pd.DataFrame) -> pd.DataFrame:
    enriched = predictions.copy()
    enriched["market_regime"] = enriched.apply(classify_market_regime, axis=1)
    enriched["risk_score"] = enriched.apply(compute_risk_score, axis=1)
    enriched["confidence_score"] = (enriched["prob_up"] - 0.5).abs() * 2
    enriched["signal"] = enriched.apply(compute_signal, axis=1)
    enriched["position_size"] = enriched.apply(compute_position_size, axis=1)
    enriched["benchmark_position"] = 1.0
    enriched["strategy_return"] = enriched["position_size"] * enriched["next_return"]
    enriched["benchmark_return"] = enriched["benchmark_position"] * enriched["next_return"]
    enriched["strategy_equity_curve"] = (1 + enriched["strategy_return"]).cumprod()
    enriched["benchmark_equity_curve"] = (1 + enriched["benchmark_return"]).cumprod()
    return enriched


def _max_drawdown(equity_curve: pd.Series) -> float:
    running_max = equity_curve.cummax()
    drawdown = equity_curve / running_max - 1
    return float(drawdown.min())


def _annualized_sharpe(returns: pd.Series) -> float:
    volatility = returns.std()
    if volatility == 0 or np.isnan(volatility):
        return 0.0
    return float((returns.mean() / volatility) * np.sqrt(365))


def backtest_strategy(predictions: pd.DataFrame) -> StrategyResult:
    enriched = enrich_predictions(predictions)

    strategy_total_return = float(enriched["strategy_equity_curve"].iloc[-1] - 1)
    benchmark_total_return = float(enriched["benchmark_equity_curve"].iloc[-1] - 1)
    signal_counts = enriched["signal"].value_counts().to_dict()

    metrics = {
        "strategy_total_return": strategy_total_return,
        "benchmark_total_return": benchmark_total_return,
        "alpha_vs_benchmark": float(strategy_total_return - benchmark_total_return),
        "strategy_max_drawdown": _max_drawdown(enriched["strategy_equity_curve"]),
        "benchmark_max_drawdown": _max_drawdown(enriched["benchmark_equity_curve"]),
        "strategy_sharpe": _annualized_sharpe(enriched["strategy_return"]),
        "benchmark_sharpe": _annualized_sharpe(enriched["benchmark_return"]),
        "signal_distribution": signal_counts,
        "avg_risk_score": float(enriched["risk_score"].mean()),
        "avg_confidence_score": float(enriched["confidence_score"].mean()),
        "buy_signal_precision": float(
            (
                enriched.loc[enriched["signal"] == "BUY", "next_return"] > 0
            ).mean()
            if (enriched["signal"] == "BUY").any()
            else 0.0
        ),
    }
    return StrategyResult(enriched_predictions=enriched, backtest_metrics=metrics)
