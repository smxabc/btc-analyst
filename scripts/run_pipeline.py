from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from btc_analyst.pipeline import PipelineArgs, run_pipeline


def parse_args() -> PipelineArgs:
    parser = argparse.ArgumentParser(description="Run the Bitcoin analytics portfolio pipeline.")
    parser.add_argument("--start-date", default="2018-01-01", help="Start date for market data download.")
    parser.add_argument("--test-size", type=float, default=0.25, help="Share of rows reserved for testing.")
    parser.add_argument("--ticker", default="BTC-USD", help="Ticker symbol for market data.")
    parser.add_argument("--input-csv", default=None, help="Optional path to a local CSV file.")
    namespace = parser.parse_args()
    return PipelineArgs(
        start_date=namespace.start_date,
        test_size=namespace.test_size,
        ticker=namespace.ticker,
        input_csv=namespace.input_csv,
    )


def main() -> None:
    metrics = run_pipeline(project_root=PROJECT_ROOT, args=parse_args())
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
