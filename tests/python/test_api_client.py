#  IntelliSIEM Copyright 2024, Rob Perry
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import pytest
import requests

from src.python.api_client import APIClient, APIError


def test_api_client_success(mocker):
    """
    Test API client handling a successful request.
    This ensures that valid data is returned when the API call is successful.
    """
    mock_response = [{'id': 'test_data'}]
    mocker.patch('requests.get',
                 return_value=mocker.Mock(status_code=200, json=mocker.Mock(return_value=mock_response)))
    client = APIClient("https://example.com/api", {"Authorization": "Bearer token"})
    result = client.get_data("endpoint")
    assert result == mock_response  # Expecting mock response data


def test_api_client_timeout(mocker):
    """
    Test API client handling of a timeout error.
    This ensures that the appropriate exception and message are raised and logged.
    """
    mocker.patch('requests.get', side_effect=requests.exceptions.Timeout)
    client = APIClient("https://example.com/api", {"Authorization": "Bearer token"})
    with pytest.raises(APIError, match="API request timed out."):
        client.get_data("endpoint")


def test_api_client_rate_limit(mocker):
    """
    Test API client handling of rate limiting.
    This ensures that the APIError exception is raised when the rate limit is exceeded.
    """
    mock_response = mocker.Mock(status_code=429, headers={"Retry-After": "5"})
    mocker.patch('requests.get', return_value=mock_response)
    client = APIClient("https://example.com/api", {"Authorization": "Bearer token"})
    with pytest.raises(APIError, match="Rate limit exceeded."):
        client.get_data("endpoint")


def test_api_client_invalid_json(mocker):
    """
    Test API client handling of invalid JSON response.
    This test simulates a ValueError when the JSON response is not valid.
    """
    mock_response = mocker.Mock(status_code=200, json=mocker.Mock(side_effect=ValueError))
    mocker.patch('requests.get', return_value=mock_response)
    client = APIClient("https://example.com/api", {"Authorization": "Bearer token"})
    with pytest.raises(APIError, match="Invalid response format."):
        client.get_data("endpoint")


def test_api_client_connection_error(mocker):
    """
    Test API client handling of a connection error.
    This ensures that connection issues are properly caught and logged.
    """
    mocker.patch('requests.get', side_effect=requests.ConnectionError)
    client = APIClient("https://example.com/api", {"Authorization": "Bearer token"})
    with pytest.raises(APIError, match="Connection error occurred."):
        client.get_data("endpoint")


def test_api_client_authentication_error(mocker):
    """
    Test API client handling of an authentication error.
    This simulates an authentication failure with a 401 status code.
    """
    mock_response = mocker.Mock(status_code=401)
    mocker.patch('requests.get', return_value=mock_response)
    client = APIClient("https://example.com/api", {"Authorization": "Invalid token"})
    with pytest.raises(APIError, match="Authentication failed."):
        client.get_data("endpoint")


def test_api_client_permission_error(mocker):
    """
    Test API client handling of a permission error.
    This simulates a permission failure with a 403 status code.
    """
    mock_response = mocker.Mock(status_code=403)
    mocker.patch('requests.get', return_value=mock_response)
    client = APIClient("https://example.com/api", {"Authorization": "Bearer token"})
    with pytest.raises(APIError, match="Permission denied."):
        client.get_data("endpoint")
