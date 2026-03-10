import pandas as pd

from btc_analyst.strategy import backtest_strategy


def test_backtest_strategy_creates_decision_columns() -> None:
    predictions = pd.DataFrame(
        {
            "Date": pd.date_range("2024-01-01", periods=4, freq="D"),
            "Close": [100, 102, 101, 105],
            "target": [1, 0, 1, 1],
            "next_return": [0.02, -0.01, 0.04, 0.01],
            "volatility_30d": [0.02, 0.03, 0.06, 0.02],
            "trend_strength_30d": [1.04, 1.01, 0.97, 1.05],
            "sma_30_ratio": [1.02, 1.0, 0.98, 1.03],
            "intraday_range": [0.03, 0.02, 0.07, 0.02],
            "distance_to_52w_high": [0.97, 0.95, 0.8, 0.99],
            "prediction": [1, 0, 1, 1],
            "prob_up": [0.66, 0.51, 0.35, 0.72],
        }
    )

    result = backtest_strategy(predictions)

    assert "signal" in result.enriched_predictions.columns
    assert "signal_reason" in result.enriched_predictions.columns
    assert "decision_score" in result.enriched_predictions.columns
    assert "risk_score" in result.enriched_predictions.columns
    assert "strategy_equity_curve" in result.enriched_predictions.columns
    assert "strategy_total_return" in result.backtest_metrics
