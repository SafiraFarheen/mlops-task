import argparse
import yaml
import numpy as np
import os
import time
import pandas as pd
import json
import logging
import sys


def load_config(config_path):
    if not os.path.exists(config_path):
        raise FileNotFoundError("Configuration file not found.")

    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    # Validate structure
    required_keys = ["seed", "window", "version"]
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Missing required config field: {key}")

    return config

def load_data(input_path):
    # 1️⃣ Check file existence
    if not os.path.exists(input_path):
        raise FileNotFoundError("Input CSV file not found.")

    # 2️⃣ Try loading CSV
    try:
        df = pd.read_csv(input_path)
    except Exception:
        raise ValueError("Invalid CSV file format.")

    # 3️⃣ Check if empty
    if df.empty:
        raise ValueError("Input CSV file is empty.")

    # 4️⃣ Validate required column
    if "close" not in df.columns:
        raise ValueError("Required column 'close' is missing.")

    return df

def setup_logging(log_file):
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--input", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--log-file", required=True)

    args = parser.parse_args()

    start_time = time.time()
    setup_logging(args.log_file)
    logging.info("Job started")

    try:
        # 1️⃣ Load configuration
        config = load_config(args.config)

        seed = config["seed"]
        window = config["window"]
        version = config["version"]

        np.random.seed(seed)

        logging.info(f"Config loaded: seed={seed}, window={window}, version={version}")

        # 2️⃣ Load data
        df = load_data(args.input)
        logging.info(f"Data loaded: {len(df)} rows")

        # 3️⃣ Rolling mean
        df["rolling_mean"] = df["close"].rolling(window=window).mean()
        logging.info(f"Rolling mean calculated with window={window}")

        # 4️⃣ Signal generation
        df["signal"] = np.where(df["close"] > df["rolling_mean"], 1, 0)
        logging.info("Signals generated")

        # 5️⃣ Metrics
        rows_processed = len(df)
        signal_rate = float(df["signal"].mean())
        latency_ms = int((time.time() - start_time) * 1000)

        metrics = {
            "version": version,
            "rows_processed": rows_processed,
            "metric": "signal_rate",
            "value": round(signal_rate, 4),
            "latency_ms": latency_ms,
            "seed": seed,
            "status": "success"
        }

        with open(args.output, "w") as f:
            json.dump(metrics, f, indent=4)

        logging.info(
            f"Metrics: signal_rate={round(signal_rate,4)}, rows_processed={rows_processed}"
        )
        logging.info(f"Job completed successfully in {latency_ms}ms")

        # REQUIRED: print final metrics to stdout
        print(json.dumps(metrics, indent=4))

        sys.exit(0)

    except Exception as e:
        error_output = {
            "version": "v1",
            "status": "error",
            "error_message": str(e)
        }

        with open(args.output, "w") as f:
            json.dump(error_output, f, indent=4)

        logging.error(f"Error occurred: {str(e)}")

        print(json.dumps(error_output, indent=4))

        sys.exit(1)
   


if __name__ == "__main__":
    main()