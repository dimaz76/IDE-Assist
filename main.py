# main.py
import os
import csv
import json
import sys
import argparse
import yaml
import pandas as pd


def load_config(path: str) -> tuple[str, str, int]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Config file not found: {path}")
    ext = os.path.splitext(path)[1].lower()
    if ext in (".yaml", ".yml"):
        cfg = yaml.safe_load(open(path, encoding="utf-8"))
    elif ext == ".json":
        cfg = json.loads(open(path, encoding="utf-8").read())
    else:
        raise ValueError(f"Unsupported config format: {ext}")
    inp = cfg["input"]
    outp = cfg["output"]
    thr = cfg.get("threshold", 10)
    if not isinstance(thr, int):
        raise ValueError("Threshold must be an integer")
    return inp, outp, thr


def load_data(path: str) -> list[dict]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    ext = os.path.splitext(path)[1].lower()
    if ext == ".csv":
        with open(path, newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))
    elif ext == ".json":
        return json.loads(open(path, encoding="utf-8").read())
    elif ext in (".xlsx", ".xls"):
        df = pd.read_excel(path)
        return df.to_dict(orient="records")
    else:
        raise ValueError(f"Unsupported extension: {ext}")


def save_result(data: list[dict], path: str, dry_run: bool = False) -> None:
    if dry_run or not data:
        return
    ext = os.path.splitext(path)[1].lower()
    if ext == ".csv":
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(data[0].keys()))
            writer.writeheader()
            writer.writerows(data)
    elif ext == ".json":
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    elif ext in (".xlsx", ".xls"):
        df = pd.DataFrame(data)
        df.to_excel(path, index=False)
    else:
        raise ValueError(f"Unsupported extension for saving: {ext}")


def process_data(data: list[dict], threshold: int = 10) -> list[dict]:
    out = []
    for row in data:
        try:
            if int(row["value"]) > threshold:
                out.append(row)
        except (KeyError, ValueError):
            continue
    return out


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--config", "-c", required=True)
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    inp, outp, thr = load_config(args.config)
    data = load_data(inp)
    filtered = process_data(data, threshold=thr)
    save_result(filtered, outp, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
