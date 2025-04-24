import pytest
import json
import yaml
import os
from main import load_config

@pytest.fixture
def tmp_yaml(tmp_path):
    data = {'input': 'in.csv', 'output': 'out.csv', 'threshold': 5}
    path = tmp_path / 'cfg.yml'
    path.write_text(yaml.safe_dump(data), encoding='utf-8')
    return path

@pytest.fixture
def tmp_json(tmp_path):
    data = {'input': 'in.json', 'output': 'out.json'}
    path = tmp_path / 'cfg.json'
    path.write_text(json.dumps(data), encoding='utf-8')
    return path

def test_load_config_yaml(tmp_yaml):
    inp, outp, thr = load_config(str(tmp_yaml))
    assert inp == 'in.csv'
    assert outp == 'out.csv'
    assert thr == 5

def test_load_config_json_defaults(tmp_json):
    inp, outp, thr = load_config(str(tmp_json))
    # threshold берётся по умолчанию
    assert inp == 'in.json'
    assert outp == 'out.json'
    assert thr == 10

def test_load_config_missing_file():
    with pytest.raises(FileNotFoundError):
        load_config('no-such-file.yaml')

def test_load_config_bad_format(tmp_path):
    # файл с неподдерживаемым расширением
    bad = tmp_path / 'cfg.txt'
    bad.write_text('foo: bar', encoding='utf-8')
    with pytest.raises(ValueError):
        load_config(str(bad))

def test_load_config_missing_keys(tmp_path):
    # нет ключа output
    bad = tmp_path / 'cfg2.json'
    bad.write_text(json.dumps({'input': 'a.csv'}), encoding='utf-8')
    with pytest.raises(KeyError):
        load_config(str(bad))

def test_load_config_invalid_threshold(tmp_yaml, tmp_path):
    # порог не число
    data = {'input': 'in.csv', 'output': 'out.csv', 'threshold': 'abc'}
    f = tmp_path / 'bad.yml'
    f.write_text(yaml.safe_dump(data), encoding='utf-8')
    with pytest.raises(ValueError):
        load_config(str(f))
