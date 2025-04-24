import os
import sys
import json
import csv
import logging
import argparse
from typing import Tuple, List, Dict, Any
import yaml
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def load_config(path: str) -> Tuple[str, str, int]:
    """Загрузка конфигурации из YAML или JSON файла."""
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Config file '{path}' not found")

    ext = os.path.splitext(path)[1].lower()
    try:
        with open(path, "r", encoding="utf-8") as f:
            if ext in (".yaml", ".yml"):
                cfg = yaml.safe_load(f)
            elif ext == ".json":
                cfg = json.load(f)
            else:
                raise ValueError(f"Unsupported config format '{ext}'")
    except Exception as e:
        raise e

    # Проверяем обязательные ключи
    if "input" not in cfg or "output" not in cfg:
        raise KeyError("Config missing 'input' or 'output' keys")

    inp = cfg["input"]
    outp = cfg["output"]
    thr = cfg.get("threshold", 0)
    try:
        thr = int(thr)
    except Exception:
        logging.warning("Invalid threshold '%s', using 0.", cfg.get("threshold"))
        thr = 0

    return inp, outp, thr


def load_data(path: str) -> List[Dict[str, Any]]:
    """Загрузка данных из CSV, JSON или Excel файлов."""
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Data file '{path}' not found")

    ext = os.path.splitext(path)[1].lower()
    if ext == ".csv":
        return list(csv.DictReader(open(path, newline="", encoding="utf-8")))
    elif ext == ".json":
        try:
            df = pd.read_json(path)  # type: ignore
        except ValueError:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return list(data)  # type: ignore
        return df.to_dict(orient="records")  # type: ignore
    elif ext in (".xls", ".xlsx"):
        df = pd.read_excel(path)
        return df.to_dict(orient="records")  # type: ignore
    else:
        raise ValueError(f"Unsupported data format '{ext}'")


def process_data(
    data: List[Dict[str, Any]], threshold: int = 0
) -> List[Dict[str, Any]]:
    """Фильтрация записей, где value > threshold."""
    result: List[Dict[str, Any]] = []
    for row in data:
        try:
            val = int(row.get("value", 0))
        except Exception:
            continue
        if val > threshold:
            result.append({"id": row.get("id", ""), "value": str(val)})
    return result


def save_result(data: List[Dict[str, Any]], path: str, dry_run: bool = False) -> None:
    """Сохранение результата в CSV, JSON или Excel файл."""
    if dry_run:
        logging.info("Dry run: would save %d rows to %s", len(data), path)
        return

    # Создаем папку, если не существует
    os.makedirs(os.path.dirname(path), exist_ok=True)

    ext = os.path.splitext(path)[1].lower()
    if ext == ".csv":
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["id", "value"])
            writer.writeheader()
            writer.writerows(data)
    elif ext == ".json":
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    elif ext in (".xls", ".xlsx"):
        from openpyxl import Workbook  # type: ignore

        wb = Workbook()
        ws = wb.active
        ws.append(["id", "value"])
        for row in data:
            ws.append([row.get("id", ""), row.get("value", "")])
        wb.save(path)
    else:
        raise ValueError(f"Unsupported output format '{ext}'")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="IDE-Assist script")
    parser.add_argument("-c", "--config", default="config.yaml", help="Path to config file")
    parser.add_argument("-v", "--version", action="store_true", help="Show version")
    parser.add_argument("--dry-run", action="store_true", help="Dry run mode")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.version:
        print("IDE-Assist version 1.0")
        return

    inp, outp, thr = load_config(args.config)
    data = load_data(inp)
    processed = process_data(data, threshold=thr)
    save_result(processed, outp, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
