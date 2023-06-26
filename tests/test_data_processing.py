from unittest.mock import patch, mock_open
from modules.data_processing import load_tickers, process_data, load_processed_data

def test_load_tickers():
    mock_open_file = mock_open(read_data='TICKER1\nTICKER2\nTICKER3')
    with patch('builtins.open', mock_open_file):
        result = load_tickers('mock_file_path')
    assert result == ['TICKER1', 'TICKER2', 'TICKER3']

@patch('modules.data_processing.load_tickers')
@patch('json.load')
@patch('builtins.open')
def test_process_data(mock_open_file, mock_json_load, mock_load_tickers):
    mock_json_load.return_value = [
        {
            'body': 'test body',
            'comments': [
                {
                    'body': 'comment body',
                    'tickers': []
                }
            ]
        }
    ]  # replace with your actual test data structure
    mock_load_tickers.return_value = ['TICKER1', 'TICKER2']
    process_data('mock_file_path', 'mock_ticker_file_path')
    assert mock_open_file.call_count == 2  # Assert that the open was called twice
    assert mock_json_load.call_count == 1  # Assert that json.load was called once
    assert mock_load_tickers.call_count == 1  # Assert that load_tickers was called once

@patch('json.load')
@patch('builtins.open')
def test_load_processed_data(mock_open_file, mock_json_load):
    mock_json_load.return_value = [
        {
            'body': 'test body',
            'comments': [
                {
                    'body': 'comment body',
                    'tickers': ['TICKER1']
                }
            ]
        }
    ]  # replace with your actual test data structure
    load_processed_data('mock_file_path')
    mock_open_file.assert_called_once_with('mock_file_path', 'r')
    mock_json_load.assert_called_once()

