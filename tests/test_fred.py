import pytest
from unittest.mock import patch, MagicMock
from ingestion.sources.fred import fetch_fred_data  


def test_fetch_fred_data_success():

    mock_response = MagicMock()
    mock_response.json.return_value = {
        'observations': [
            {'date': '2023-01-01', 'value': '100.5'},
            {'date': '2023-01-02', 'value': '101.2'}
        ]
    }
    
    with patch('ingestion.sources.fred.requests.get', return_value=mock_response):
        result = fetch_fred_data('TEST_SERIES')
        assert result is not None
        assert len(result) == 2


def test_fetch_fred_data_api_key_missing():
    with patch.dict('os.environ', {}, clear=True):
        with pytest.raises(ValueError):
            fetch_fred_data('TEST_SERIES')


def test_fetch_fred_data_invalid_series():
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = Exception("Not found")
    
    with patch('ingestion.sources.fred.requests.get', return_value=mock_response):
        with pytest.raises(Exception):
            fetch_fred_data('INVALID_SERIES')
