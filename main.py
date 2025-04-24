# main.py
import os
import csv
import json
import sys
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

def load_data(path: str) -> pd.DataFrame:
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    ext = os.path.splitext(path)[1].lower()
    if ext == ".csv":
        return pd.read_csv(path, encoding="utf-8")
    elif ext == ".json":
        data = json.loads(open(path, encoding="utf-8").read())
        return pd.DataFrame(data)
    elif ext in (".xlsx", ".xls"):
        return pd.read_excel(path)
    else:
        raise ValueError(f"Unsupported extension: {ext}")

def save_result(data, path: str, dry_run: bool = False) -> None:
    if dry_run:
        return
    # Если пришёл DataFrame — преобразуем в список словарей
    if isinstance(data, pd.DataFrame):
        records = data.to_dict(orient="records")
    else:
        records = data
    if not records:
        return

    ext = os.path.splitext(path)[1].lower()
    if ext == ".csv":
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(records[0].keys()))
            writer.writeheader()
            writer.writerows(records)
    elif ext == ".json":
        with open(path, "w", encoding="utf-8") as f:
            json.dump(records, f, ensure_ascii=False, indent=2)
    elif ext in (".xlsx", ".xls"):
        df = pd.DataFrame(records)
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
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--config", "-c", required=True)
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    inp, outp, thr = load_config(args.config)
    df = load_data(inp)
    filtered = process_data(df.to_dict(orient="records"), threshold=thr)
    save_result(filtered, outp, dry_run=args.dry_run)

if __name__ == "__main__":
    main()
