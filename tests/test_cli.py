import sys
import csv
import pytest
import logging
from main import main

@pytest.fixture
def project_tree(tmp_path):
    proj = tmp_path
    cfg = proj / "config.yaml"
    cfg.write_text("input: data/in.csv\noutput: data/out.csv\nthreshold: 10\n", encoding="utf-8")
    d = proj / "data"
    d.mkdir()
    f = d / "in.csv"
    f.write_text("id,value\n1,5\n2,15\n3,30\n", encoding="utf-8")
    return proj, cfg

def test_cli_creates_output(project_tree, monkeypatch):
    proj, cfg = project_tree
    monkeypatch.chdir(proj)
    sys.argv = ["main.py", "--config", str(cfg)]
    main()
    out = proj / "data" / "out.csv"
    assert out.exists()
    rows = list(csv.DictReader(open(out, newline="", encoding="utf-8")))
    assert rows == [{"id": "2", "value": "15"}, {"id": "3", "value": "30"}]

def test_cli_dry_run(project_tree, caplog, monkeypatch):
    proj, cfg = project_tree
    monkeypatch.chdir(proj)
    caplog.set_level(logging.INFO)
    sys.argv = ["main.py", "--config", str(cfg), "--dry-run"]
    main()
    assert "Dry run" in caplog.text