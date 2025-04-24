import os
import csv
import json
import pytest
import pandas as pd
from main import load_data, save_result

def test_load_data_missing_file(tmp_path):
    missing = tmp_path / "nofile.csv"
    with pytest.raises(FileNotFoundError):
        load_data(str(missing))

def test_load_data_bad_extension(tmp_path):
    bad = tmp_path / "in.txt"
    bad.write_text("foo", encoding="utf-8")
    with pytest.raises(ValueError):
        load_data(str(bad))

def test_save_result_dry_run(tmp_path):
    out = tmp_path / "out.csv"
    save_result([{"a": 1}], str(out), dry_run=True)
    assert not out.exists()

def test_save_result_empty(tmp_path):
    out = tmp_path / "empty.csv"
    save_result([], str(out))
    assert not out.exists()

def test_save_csv_and_json(tmp_path):
    data = [{"id": "1", "value": "100"}]
    # CSV
    out_csv = tmp_path / "out.csv"
    save_result(data, str(out_csv))
    rows = list(csv.DictReader(open(out_csv, newline="", encoding="utf-8")))
    assert rows == data

    # JSON
    out_json = tmp_path / "out.json"
    save_result(data, str(out_json))
    loaded = json.loads(out_json.read_text(encoding="utf-8"))
    assert loaded == data

def test_save_excel(tmp_path):
    data = [{"id": "1", "value": "100"}]
    out_xlsx = tmp_path / "out.xlsx"
    save_result(data, str(out_xlsx))

    # читаем обратно
    df2 = pd.read_excel(str(out_xlsx))
    records = df2.to_dict(orient="records")

    # приводим всё к строкам
    normalized = [
        {k: str(v) for k, v in row.items()}
        for row in records
    ]

    assert normalized == data

