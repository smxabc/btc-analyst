import pandas as pd

from btc_analyst.features import FEATURE_COLUMNS, build_features


def test_build_features_returns_expected_columns() -> None:
    rows = 420
    dataset = pd.DataFrame(
        {
            "Date": pd.date_range("2024-01-01", periods=rows, freq="D"),
            "Open": [100 + index for index in range(rows)],
            "High": [101 + index for index in range(rows)],
            "Low": [99 + index for index in range(rows)],
            "Close": [100 + index for index in range(rows)],
            "Adj Close": [100 + index for index in range(rows)],
            "Volume": [1000 + index * 10 for index in range(rows)],
        }
    )

    features = build_features(dataset)

    for column in FEATURE_COLUMNS + ["target"]:
        assert column in features.columns
    assert "next_return" in features.columns
    assert not features.empty
