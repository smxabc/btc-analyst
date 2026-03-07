# Bitcoin Decision Intelligence Platform

Dieses Repository ist als starkes Portfolio-Projekt fuer Bewerbungen im Bereich Business Analysis, Data Analysis und Analytics aufgebaut. Es zeigt nicht nur eine Preisprognose, sondern eine vollstaendige Decision-Intelligence-Pipeline fuer Bitcoin: Datenbeschaffung, Feature Engineering, Modelltraining, Signal-Generierung, Risiko-Scoring, Backtesting und Management-taugliche Ergebnisaufbereitung.

## Projektziel

Ziel ist es, historische Bitcoin-Daten so auszuwerten, dass daraus taegliche Entscheidungsunterstuetzung fuer Marktbeobachtung und Trading entsteht. Im Vordergrund stehen nicht "perfekte" Prognosen, sondern:

- strukturierte Analyse eines realen Marktdatensatzes
- saubere und reproduzierbare Datenpipeline
- nachvollziehbare KPIs und Interpretation
- konkrete Handlungssignale statt nur Modell-Outputs
- Backtesting und Benchmarking gegen Buy-and-Hold
- GitHub-taugliche Projektdokumentation fuer Bewerbungen

## Business-Frage

**Kann man aus historischen Marktindikatoren ein System bauen, das taeglich Chancen, Risiken und sinnvolle Bitcoin-Handlungsoptionen strukturiert bewertet?**

## Projektumfang

- Abruf historischer `BTC-USD`-Marktdaten via `yfinance`
- Berechnung technischer, trendbezogener und risiko-orientierter Features
- Training eines Klassifikationsmodells mit Wahrscheinlichkeits-Output
- Zeitbasierter Train/Test-Split
- Uebersetzung der Modellwahrscheinlichkeit in `BUY`, `HOLD`, `REDUCE_RISK`
- Marktregime-Erkennung wie `bull_trend`, `bear_trend` und `high_volatility`
- Risiko-Score und Position-Sizing als Decision Layer
- Backtesting der Signale mit Benchmark gegen Buy-and-Hold
- Export von Reports, Kennzahlen und Management Summary

## Die 9 Mehrwert-Bausteine

Dieses Projekt wurde bewusst um neun Punkte erweitert, damit es fachlich deutlich mehr hergibt als ein simples Modell:

1. Modellwahrscheinlichkeiten statt nur binarer Vorhersage
2. konkrete Trading-Signale (`BUY`, `HOLD`, `REDUCE_RISK`)
3. Konfidenz-Score pro Entscheidung
4. Marktregime-Erkennung
5. Risiko-Score fuer das aktuelle Setup
6. Position-Sizing als Handlungsempfehlung
7. Backtesting der Strategie
8. Benchmark gegen Buy-and-Hold
9. Executive Summary mit Business- und Trading-Perspektive

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
│       ├── reporting.py
│       └── strategy.py
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
- `reports/generated/metrics.json`: Modell-Kennzahlen
- `reports/generated/backtest_metrics.json`: Strategie- und Benchmark-Kennzahlen
- `reports/generated/feature_importance.csv`: wichtigste Einflussfaktoren
- `reports/generated/predictions.csv`: Signale, Risiko, Konfidenz und Equity Curves
- `reports/generated/executive_summary.md`: Management- und Trading Summary

## Beispielergebnis

Ein Beispiel-Lauf mit echten `BTC-USD`-Daten wurde am **7. Maerz 2026** ausgefuehrt.

Die genauen Zahlen werden bei jedem Lauf neu erzeugt. Im Repository liegen Beispiel-Outputs in `reports/generated/`, damit Recruiter und Interviewer direkt sehen koennen, wie das System Ergebnisse dokumentiert.

Typische Output-Fragen, die dieses Projekt beantwortet:

- Wie hoch ist die Wahrscheinlichkeit fuer einen positiven naechsten Tag?
- Befindet sich Bitcoin in einem Bullen-, Baeren- oder Hochrisiko-Regime?
- Ist die aktuelle Situation eher fuer `BUY`, `HOLD` oder `REDUCE_RISK` geeignet?
- Wie haette sich diese Signallogik historisch gegen Buy-and-Hold geschlagen?

## Warum dieses Projekt fuer Bewerbungen sinnvoll ist

Dieses Projekt zeigt, dass du:

- ein Analyseproblem fachlich strukturieren kannst
- Datenquellen in eine reproduzierbare Pipeline ueberfuehrst
- KPIs fuer Modell, Risiko und Strategie definierst
- technische Ergebnisse in Business-Sprache uebersetzt
- aus Daten konkrete Handlungsoptionen ableitest
- ein komplettes GitHub-Repository mit sinnvoller Dokumentation aufsetzt

## Weiterer Ausbau

Moegliche naechste Schritte fuer Version 2:

- Dashboard in Power BI oder Streamlit
- erweiterte Feature-Sets mit Makro-, ETF-, Sentiment- oder On-Chain-Daten
- taegliche automatische Report-Generierung
- Walk-Forward-Validation statt nur eines Splits
- Alerting fuer neue Hochrisiko- oder High-Conviction-Signale
- automatisierte Reports per GitHub Actions

## Hinweis

Das Projekt ist als Research-, Analytics- und Decision-Support-System gedacht. Es ist **keine** Finanzberatung und kein fertig produktives Handelssystem.
