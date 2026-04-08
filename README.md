# Analytics Automation Agent (CareerOS Lite)

A modular Python analytics automation agent that reads a CSV dataset, runs basic EDA, detects anomalies, calculates KPIs, and generates a structured report with text and charts.

## Features

- **Input:** CSV dataset
- **Processing:**
  - Basic EDA (shape, missingness, numeric/categorical summaries)
  - KPI calculation (row count, missingness, cardinality, numeric moments)
  - Anomaly detection (robust z-score with row-level anomaly scoring)
- **Output:**
  - Markdown report with insights and recommendations
  - JSON artifacts for KPIs and anomaly rows
  - Charts (histograms and anomaly score distribution)

## Project Structure

```text
analytics_agent/
  __init__.py
  agent.py
  io_utils.py
  eda.py
  kpi.py
  anomalies.py
  insights.py
  visualization.py
  report.py
run_agent.py
requirements.txt
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
python run_agent.py --input path/to/data.csv --output-dir outputs
```

Optional threshold tuning:

```bash
python run_agent.py --input data.csv --output-dir outputs --anomaly-threshold 3.5
```

## Outputs

Inside `--output-dir`, the agent creates:

- `report.md` - structured narrative report
- `kpis.json` - machine-readable KPI results
- `anomalies.csv` - anomalous rows with score
- `charts/` - generated visual assets

