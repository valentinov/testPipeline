import pytest
from unittest.mock import patch, MagicMock
from requests.exceptions import Timeout, HTTPError, ConnectionError
from logic.requests_helper import make_request


@patch("logic.requests_helper.requests.request")
def test_make_request_success(mock_request):
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"data": "ok"}
    mock_request.return_value = mock_response

    response = make_request("GET", "https://example.com")
    assert response.json() == {"data": "ok"}
    mock_request.assert_called_once()


@patch("logic.requests_helper.requests.request")
def test_make_request_http_error(mock_request):
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = HTTPError("500 Server Error")
    mock_request.return_value = mock_response

    with pytest.raises(RuntimeError) as excinfo:
        make_request("GET", "https://example.com", max_retries=2)

    assert "HTTPError" in str(excinfo.value)
    assert mock_request.call_count == 2  # Retries once before failing


@patch("logic.requests_helper.requests.request")
def test_make_request_timeout(mock_request):
    mock_request.side_effect = Timeout("Request timed out")

    with pytest.raises(RuntimeError) as excinfo:
        make_request("POST", "https://example.com", json={}, max_retries=3)

    assert "Timeout" in str(excinfo.value)
    assert mock_request.call_count == 3  # Retries twice before failing


@patch("logic.requests_helper.requests.request")
def test_make_request_recovers_after_retry(mock_request):
    # First call fails, second succeeds
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_request.side_effect = [ConnectionError("Connection failed"), mock_response]

    response = make_request("GET", "https://example.com", max_retries=2)
    assert response == mock_response
    assert mock_request.call_count == 2
