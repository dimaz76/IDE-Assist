import json
import csv
import pandas as pd
import pytest
from main import load_data, save_result

def test_csv_to_csv(tmp_path):
    in_csv = tmp_path / "in.csv"
    in_csv.write_text("id,value\n1,5\n2,15\n", encoding="utf-8")
    out_csv = tmp_path / "out.csv"
    data = load_data(str(in_csv))
    save_result(data, str(out_csv))
    assert csv.DictReader(open(out_csv)).fieldnames == ["id", "value"]

def test_json_to_json(tmp_path):
    sample = [{"id":"1","value":"5"},{"id":"2","value":"15"}]
    in_json = tmp_path / "in.json"
    in_json.write_text(json.dumps(sample), encoding="utf-8")
    out_json = tmp_path / "out.json"
    data = load_data(str(in_json))
    save_result(data, str(out_json))
    assert json.loads(open(out_json).read()) == sample

def test_excel_to_excel(tmp_path):
    sample = [{"id":"1","value":"5"},{"id":"2","value":"15"}]
    df = pd.DataFrame(sample)
    in_xlsx = tmp_path / "in.xlsx"
    df.to_excel(str(in_xlsx), index=False)
    out_xlsx = tmp_path / "out.xlsx"
    data = load_data(str(in_xlsx))
    save_result(data, str(out_xlsx))
    df2 = pd.read_excel(str(out_xlsx))
    assert df2.to_dict(orient="records") == sample