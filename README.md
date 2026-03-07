# Bitcoin Market Analyst Portfolio Project

Dieses Repository ist als Portfolio-Projekt fuer Bewerbungen im Bereich Business Analysis, Data Analysis und Analytics aufgebaut. Es zeigt einen vollstaendigen Analyse-Workflow fuer Bitcoin-Marktdaten: Datenbeschaffung, Feature Engineering, Modelltraining, Evaluierung und Management-taugliche Ergebnisaufbereitung.

## Projektziel

Ziel ist es, historische Bitcoin-Daten zu analysieren und ein einfaches, nachvollziehbares Modell zur Vorhersage der naechsten Tagesbewegung aufzubauen. Im Vordergrund stehen nicht "perfekte" Prognosen, sondern:

- strukturierte Analyse eines realen Marktdatensatzes
- saubere und reproduzierbare Datenpipeline
- nachvollziehbare KPIs und Interpretation
- GitHub-taugliche Projektdokumentation fuer Bewerbungen

## Business-Frage

**Kann man aus historischen Marktindikatoren ein Modell bauen, das die Richtung der Bitcoin-Preisbewegung am naechsten Handelstag besser als Zufall abschaetzt?**

## Projektumfang

- Abruf historischer `BTC-USD`-Marktdaten via `yfinance`
- Berechnung technischer und statistischer Features
- Training eines Klassifikationsmodells fuer Up/Down-Prognosen
- Zeitbasierter Train/Test-Split
- Export von Metriken, Feature Importances und Markdown-Report

## Verzeichnisstruktur

```text
.
├── data/
│   ├── processed/
│   └── raw/
├── models/
├── reports/
│   └── generated/
├── scripts/
│   └── run_pipeline.py
├── src/
│   └── btc_analyst/
│       ├── config.py
│       ├── data.py
│       ├── features.py
│       ├── model.py
│       ├── pipeline.py
│       └── reporting.py
├── tests/
└── README.md
```

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Pipeline ausfuehren

```bash
python scripts/run_pipeline.py --start-date 2018-01-01 --test-size 0.25
```

Optional mit lokaler CSV-Datei:

```bash
python scripts/run_pipeline.py --input-csv data/raw/btc_usd.csv
```

## Outputs

Nach einem Lauf werden folgende Artefakte erzeugt:

- `data/raw/btc_usd.csv`: Rohdaten
- `data/processed/btc_features.csv`: modellierte Features
- `models/random_forest_direction.pkl`: trainiertes Modell
- `reports/generated/metrics.json`: Kennzahlen
- `reports/generated/feature_importance.csv`: wichtigste Einflussfaktoren
- `reports/generated/executive_summary.md`: Management Summary

## Beispielergebnis

Ein Beispiel-Lauf mit echten `BTC-USD`-Daten wurde am **7. Maerz 2026** ausgefuehrt.

- Accuracy: `0.516`
- Precision: `0.513`
- Recall: `0.549`
- F1 Score: `0.530`
- Train Rows: `2217`
- Test Rows: `740`

Die wichtigsten Features in diesem Lauf waren:

- `return_1d`
- `sma_7_ratio`
- `sma_30_ratio`
- `rsi_14`
- `return_7d`

Die erzeugten Beispiel-Outputs liegen in `reports/generated/` und koennen direkt im Repository eingesehen werden.

## Warum dieses Projekt fuer Bewerbungen sinnvoll ist

Dieses Projekt zeigt, dass du:

- ein Analyseproblem fachlich strukturieren kannst
- Datenquellen in eine reproduzierbare Pipeline ueberfuehrst
- KPIs definierst und Ergebnisse sauber interpretierst
- technische Ergebnisse in Business-Sprache uebersetzt
- ein komplettes GitHub-Repository mit sinnvoller Dokumentation aufsetzt

## Weiterer Ausbau

Moegliche naechste Schritte fuer Version 2:

- Benchmark gegen Buy-and-Hold oder naive Baselines
- Backtesting fuer einfache Handelsregeln
- Dashboard in Power BI oder Streamlit
- erweiterte Feature-Sets mit Makro- oder On-Chain-Daten
- automatisierte Reports per GitHub Actions

## Hinweis

Das Modell ist ein Demonstrationsprojekt fuer Analytics- und Business-Portfolio-Zwecke. Es ist **keine** Finanzberatung.

