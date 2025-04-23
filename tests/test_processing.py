import pytest
from main import process_data

# Старые тесты: уберём их или адаптируем
# def test_process_data_empty():
#     ...
# def test_process_data_identity():
#     ...

def test_process_data_default_threshold():
    data = [
        {"id": "1", "value": "5"},
        {"id": "2", "value": "15"},
    ]
    # при threshold=10 останется только вторая запись
    result = process_data(data, threshold=10)
    assert result == [{"id": "2", "value": "15"}]

def test_process_data_custom_threshold():
    data = [
        {"id": "1", "value": "5"},
        {"id": "2", "value": "15"},
        {"id": "3", "value": "20"},
    ]
    # при threshold=15 останется только запись с value>15
    result = process_data(data, threshold=15)
    assert result == [{"id": "3", "value": "20"}]

def test_process_data_non_numeric():
    data = [
        {"id": "1", "value": "abc"},
        {"id": "2", "value": "20"},
    ]
    # некорректные строки пропускаются
    result = process_data(data, threshold=10)
    assert result == [{"id": "2", "value": "20"}]
