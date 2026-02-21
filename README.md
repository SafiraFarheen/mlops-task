# MLOps Pipeline — Technical Assessment

A miniature MLOps batch pipeline that ingests cryptocurrency OHLCV data,
computes rolling-mean-based trading signals, and emits structured JSON metrics.

---

## Project Structure

```
mlops-task/
├── run.py            # Main pipeline script
├── config.yaml       # Configuration (seed, window, version)
├── data.csv          # Input OHLCV dataset (10,000 rows)
├── requirements.txt  # Python dependencies
├── Dockerfile        # Container definition
├── metrics.json      # Example output (generated after a run)
├── run.log           # Example log file (generated after a run)
└── README.md         # This file
```

---

## How It Works

1. **Config Loading** — Reads `seed`, `window`, and `version` from `config.yaml`
2. **Data Ingestion** — Loads and validates `data.csv`; confirms `close` column exists
3. **Rolling Mean** — Computes a sliding-window average over the `close` column
4. **Signal Generation** — Assigns `1` where `close > rolling_mean`, else `0`
5. **Metrics Output** — Writes JSON with `signal_rate`, `rows_processed`, `latency_ms`
6. **Logging** — Every step is logged with timestamps to the specified log file

---

## Setup Instructions

```bash
# Install dependencies
pip install -r requirements.txt
```

---

## Local Execution

```bash
# Run locally
python run.py --input data.csv --config config.yaml \
              --output metrics.json --log-file run.log
```

---

## Docker Instructions

```bash
# Build the Docker image
docker build -t mlops-task .

# Run the container
docker run --rm mlops-task
```

---

## Expected Output

After a successful run, `metrics.json` will contain:

```json
{
  "version": "v1",
  "rows_processed": 10000,
  "metric": "signal_rate",
  "value": 0.4974,
  "latency_ms": 21,
  "seed": 42,
  "status": "success"
}
```

On error, the output will be:

```json
{
  "version": "v1",
  "status": "error",
  "error_message": "Description of what went wrong"
}
```

---

## Dependencies

| Package   | Version | Purpose                        |
|-----------|---------|--------------------------------|
| pandas    | 2.0.3   | CSV loading and rolling window |
| numpy     | 1.24.4  | Signal generation, seed        |
| pyyaml    | 6.0.1   | YAML config file parsing       |

All dependencies are available on PyPI and installable via `pip`.

---

## Reproducibility

The pipeline is fully deterministic. Running it multiple times with the same
`config.yaml` will always produce identical `signal_rate` values because:
- `numpy.random.seed(seed)` is set from config before any computation
- `pandas.rolling()` is a pure deterministic function