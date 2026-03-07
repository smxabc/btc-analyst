from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from btc_analyst.config import ProjectPaths
from btc_analyst.data import load_from_csv, load_market_data, save_dataframe
from btc_analyst.features import build_features
from btc_analyst.model import save_model, train_direction_model
from btc_analyst.reporting import (
    write_backtest_metrics,
    write_executive_summary,
    write_feature_importance,
    write_metrics,
    write_predictions,
)
from btc_analyst.strategy import backtest_strategy


@dataclass
class PipelineArgs:
    start_date: str
    test_size: float
    ticker: str
    input_csv: str | None = None


def run_pipeline(project_root: Path, args: PipelineArgs) -> dict:
    paths = ProjectPaths.from_root(project_root)
    paths.ensure()

    if args.input_csv:
        raw_data = load_from_csv(Path(args.input_csv))
    else:
        raw_data = load_market_data(start_date=args.start_date, ticker=args.ticker)

    features = build_features(raw_data)
    result = train_direction_model(features, test_size=args.test_size)
    strategy_result = backtest_strategy(result.predictions)

    save_dataframe(raw_data, paths.data_raw / "btc_usd.csv")
    save_dataframe(features, paths.data_processed / "btc_features.csv")
    save_model(result.model, paths.models / "random_forest_direction.pkl")
    write_metrics(result.metrics, paths.reports / "metrics.json")
    write_backtest_metrics(strategy_result.backtest_metrics, paths.reports / "backtest_metrics.json")
    write_feature_importance(result.feature_importance, paths.reports / "feature_importance.csv")
    write_predictions(strategy_result.enriched_predictions, paths.reports / "predictions.csv")
    write_executive_summary(
        result.metrics,
        strategy_result.backtest_metrics,
        result.feature_importance,
        paths.reports / "executive_summary.md",
    )

    combined_metrics = {
        "model_metrics": result.metrics,
        "strategy_metrics": strategy_result.backtest_metrics,
    }
    return combined_metrics
