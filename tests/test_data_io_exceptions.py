import json
import pytest
import pandas as pd
import logging
from main import load_data, save_result

def test_load_data_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_data(str(tmp_path / "nofile.csv"))

def test_load_data_bad_extension(tmp_path):
    bad = tmp_path / "in.txt"
    bad.write_text("foo", encoding="utf-8")
    with pytest.raises(ValueError):
        load_data(str(bad))

def test_save_result_dry_run(tmp_path, caplog):
    caplog.set_level(logging.INFO)
    save_result([{"a": 1}], str(tmp_path / "out.csv"), dry_run=True)
    assert "Dry run" in caplog.text

def test_save_result_empty(tmp_path):
    out = tmp_path / "empty.csv"
    save_result([], str(out))
    assert out.exists()
    assert open(out).read().startswith("id,value")

def test_save_csv_and_json(tmp_path):
    data = [{"id": "1", "value": "100"}]
    out_csv = tmp_path / "out.csv"
    save_result(data, str(out_csv))
    assert open(out_csv).read().startswith("id,value")
    out_json = tmp_path / "out.json"
    save_result(data, str(out_json))
    assert json.loads(open(out_json).read()) == data

def test_save_excel(tmp_path):
    data = [{"id": "1", "value": "100"}]
    out_xlsx = tmp_path / "out.xlsx"
    save_result(data, str(out_xlsx))
    df = pd.read_excel(str(out_xlsx))
    assert df.to_dict(orient="records") == data