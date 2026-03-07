from __future__ import annotations

from pathlib import Path

import pandas as pd


def load_market_data(start_date: str, ticker: str = "BTC-USD") -> pd.DataFrame:
    try:
        import yfinance as yf
    except ImportError as exc:
        raise ImportError(
            "yfinance ist nicht installiert. Bitte zuerst `pip install -r requirements.txt` ausfuehren."
        ) from exc

    dataset = yf.download(ticker, start=start_date, auto_adjust=False, progress=False)
    if dataset.empty:
        raise ValueError(f"Keine Marktdaten fuer {ticker} ab {start_date} erhalten.")

    dataset = dataset.reset_index()
    if isinstance(dataset.columns, pd.MultiIndex):
        dataset.columns = [
            first if first not in ("", None) else second for first, second in dataset.columns.to_flat_index()
        ]
    else:
        dataset.columns = [str(column) for column in dataset.columns]

    if "Adj Close" not in dataset.columns and "Close" in dataset.columns:
        dataset["Adj Close"] = dataset["Close"]

    required_columns = ["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]
    dataset = dataset[required_columns]
    return dataset.sort_values("Date").reset_index(drop=True)


def load_from_csv(csv_path: Path) -> pd.DataFrame:
    dataset = pd.read_csv(csv_path, parse_dates=["Date"])
    required_columns = {"Date", "Open", "High", "Low", "Close", "Volume"}
    missing = required_columns.difference(dataset.columns)
    if missing:
        missing_text = ", ".join(sorted(missing))
        raise ValueError(f"CSV-Datei enthaelt nicht alle benoetigten Spalten: {missing_text}")
    return dataset.sort_values("Date").reset_index(drop=True)


def save_dataframe(dataset: pd.DataFrame, output_path: Path) -> None:
    dataset.to_csv(output_path, index=False)
