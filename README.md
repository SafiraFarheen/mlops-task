# MLOps Pipeline — Technical Assessment

A miniature MLOps batch pipeline that ingests cryptocurrency OHLCV data,
computes rolling-mean-based trading signals, and emits structured JSON metrics.

The project demonstrates configuration-driven execution, structured logging,
containerized reproducibility, and CI-validated Docker builds.

---

## Project Structure

```
mlops-task/
├── run.py # Main pipeline script
├── config.yaml # Configuration (seed, window, version)
├── data.csv # Input OHLCV dataset (10,000 rows)
├── requirements.txt # Python dependencies
├── Dockerfile # Container definition
├── metrics.json # Example output (generated after a run)
├── run.log # Example log file (generated after a run)
├── .github/
│ └── workflows/
│ └── docker-test.yml # CI workflow for Docker validation
└── README.md # This file
```

---

## How It Works

1. **Config Loading**  
   Reads `seed`, `window`, and `version` from `config.yaml`.

2. **Data Ingestion**  
   Loads and validates `data.csv`; confirms required `close` column exists.

3. **Rolling Mean Computation**  
   Computes a sliding-window average over the `close` column using pandas.

4. **Signal Generation**  
   Assigns `1` where `close > rolling_mean`, otherwise `0`.

5. **Metrics Calculation**  
   Computes:
   - `rows_processed`
   - `signal_rate`
   - `latency_ms`

6. **Logging**  
   Each stage is logged with timestamps to the specified log file.

7. **JSON Output**  
   Writes structured metrics to `metrics.json`.
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
  "value": 0.4971,
  "latency_ms": 13,
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
| pandas    | 2.1.0   | CSV loading and rolling window |
| numpy     | 1.26.0  | Signal generation, seed        |
| pyyaml    | 6.0     | YAML config file parsing       |

All dependencies are available on PyPI and installable via `pip`.

---

## Reproducibility

The pipeline is fully deterministic. Running it multiple times with the same
`config.yaml` will always produce identical `signal_rate` values because:
- `numpy.random.seed(seed)` is set from config before any computation
- `pandas.rolling()` is a pure deterministic function
- Configuration values are externalized

## Design Considerations
- Configuration-driven execution (no hardcoded parameters)
- Explicit input validation and error handling
- Structured JSON outputs for downstream compatibility
- Deterministic computation via seeded randomness
- Containerized execution for environment reproducibility
- Clear logging for observability

  ## CI Validation
  Docker build and container execution are automatically validated via GitHub Actions.
  
  Workflow file:
  .github/workflows/docker-test.yml
  
  - Each push to main:
      - Builds the Docker image
      - Runs the container
      - Verifies successful execution
      - Confirms correct JSON output
