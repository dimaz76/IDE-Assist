from main import process_data

def test_process_data_default_threshold():
    data = [{"id":"1","value":"5"},{"id":"2","value":"15"}]
    result = process_data(data, threshold=10)
    assert result == [{"id":"2","value":"15"}]

def test_process_data_custom_threshold():
    data = [{"id":"1","value":"5"},{"id":"2","value":"15"},{"id":"3","value":"20"}]
    result = process_data(data, threshold=15)
    assert result == [{"id":"3","value":"20"}]

def test_process_data_non_numeric():
    data = [{"id":"1","value":"abc"},{"id":"2","value":"20"}]
    result = process_data(data, threshold=10)
    assert result == [{"id":"2","value":"20"}]