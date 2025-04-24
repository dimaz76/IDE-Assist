import sys
import os
import csv
import pytest
from main import main

@pytest.fixture
def project_tree(tmp_path, monkeypatch):
    # создаём структуру проекта в tmp
    project_dir = tmp_path
    data_dir = project_dir / "data"
    data_dir.mkdir()
    # пишем свой input.csv с числами
    input_csv = data_dir / "input.csv"
    input_csv.write_text(
        "id,value\n"
        "1,5\n"
        "2,15\n"
        "3,30\n",
        encoding="utf-8"
    )
    # конфиг
    cfg = project_dir / "config.yaml"
    cfg.write_text(
        "input: data/input.csv\n"
        "output: data/out.csv\n"
        "threshold: 10\n",
        encoding="utf-8"
    )
    # переключаем cwd
    monkeypatch.chdir(project_dir)
    return project_dir, cfg

def test_cli_creates_output(project_tree, capsys):
    project_dir, cfg = project_tree
    sys.argv = ["main.py", "--config", str(cfg)]
    main()
    out = project_dir / "data" / "out.csv"
    assert out.exists()
    rows = list(csv.DictReader(open(out, newline="", encoding="utf-8")))
    # остались только с value > 10: обе записи 15 и 30
    assert rows == [{"id": "2", "value": "15"}, {"id": "3", "value": "30"}]

def test_cli_dry_run(project_tree, capsys):
    project_dir, cfg = project_tree
    sys.argv = [
        "main.py",
        "--config", str(cfg),
        "--dry-run"
    ]
    main()
    out = project_dir / "data" / "out.csv"
    assert not out.exists()
