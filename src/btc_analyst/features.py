from __future__ import annotations

import numpy as np
import pandas as pd


FEATURE_COLUMNS = [
    "return_1d",
    "return_7d",
    "return_30d",
    "volatility_7d",
    "volatility_30d",
    "trend_strength_30d",
    "volume_change_1d",
    "volume_zscore_30d",
    "sma_7_ratio",
    "sma_30_ratio",
    "distance_to_52w_high",
    "momentum_14d",
    "momentum_30d",
    "rsi_14",
    "intraday_range",
]


def _relative_strength_index(close: pd.Series, window: int = 14) -> pd.Series:
    delta = close.diff()
    gains = delta.clip(lower=0)
    losses = -delta.clip(upper=0)

    avg_gain = gains.rolling(window=window).mean()
    avg_loss = losses.rolling(window=window).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    rsi = 100 - (100 / (1 + rs))
    return rsi.fillna(50)


def build_features(dataset: pd.DataFrame) -> pd.DataFrame:
    frame = dataset.copy()
    frame["Date"] = pd.to_datetime(frame["Date"])
    frame["return_1d"] = frame["Close"].pct_change(1)
    frame["return_7d"] = frame["Close"].pct_change(7)
    frame["return_30d"] = frame["Close"].pct_change(30)
    frame["volatility_7d"] = frame["return_1d"].rolling(7).std()
    frame["volatility_30d"] = frame["return_1d"].rolling(30).std()
    frame["trend_strength_30d"] = frame["Close"].rolling(30).mean() / frame["Close"].rolling(90).mean()
    frame["volume_change_1d"] = frame["Volume"].pct_change(1).replace([np.inf, -np.inf], np.nan)
    volume_mean = frame["Volume"].rolling(30).mean()
    volume_std = frame["Volume"].rolling(30).std()
    frame["volume_zscore_30d"] = (frame["Volume"] - volume_mean) / volume_std.replace(0, np.nan)
    frame["sma_7_ratio"] = frame["Close"] / frame["Close"].rolling(7).mean()
    frame["sma_30_ratio"] = frame["Close"] / frame["Close"].rolling(30).mean()
    frame["distance_to_52w_high"] = frame["Close"] / frame["Close"].rolling(365, min_periods=60).max()
    frame["momentum_14d"] = frame["Close"] - frame["Close"].shift(14)
    frame["momentum_30d"] = frame["Close"] - frame["Close"].shift(30)
    frame["rsi_14"] = _relative_strength_index(frame["Close"], window=14)
    frame["intraday_range"] = (frame["High"] - frame["Low"]) / frame["Open"]

    frame["next_close"] = frame["Close"].shift(-1)
    frame["next_return"] = frame["next_close"] / frame["Close"] - 1
    frame["target"] = (frame["next_close"] > frame["Close"]).astype(int)
    features = frame.dropna(subset=FEATURE_COLUMNS + ["next_close"]).copy()
    features = features.drop(columns=["next_close"])
    return features.reset_index(drop=True)
