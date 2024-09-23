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
from src.api_client import APIClient, APIError


def test_api_client_timeout(mocker):
    """
    Test API client handling of a timeout error.
    """
    mocker.patch('requests.get', side_effect=requests.exceptions.Timeout)
    client = APIClient("https://example.com/api", {"Authorization": "Bearer token"})
    # Match a more general pattern, ignoring the specific exception message.
    with pytest.raises(APIError, match="API request timed out"):
        client.get_data("endpoint")


def test_api_client_invalid_response(mocker):
    """
    Test API client handling of invalid JSON response.
    """
    mocker.patch('requests.get', return_value=mocker.Mock(status_code=200, json=mocker.Mock(side_effect=ValueError)))
    client = APIClient("https://example.com/api", {"Authorization": "Bearer token"})
    with pytest.raises(APIError, match="Invalid response format."):
        client.get_data("endpoint")


def test_api_client_rate_limit(mocker):
    """
    Test API client handling of rate limiting.
    """
    mock_response = mocker.Mock(status_code=429, headers={"Retry-After": "5"})
    mocker.patch('requests.get', return_value=mock_response)
    client = APIClient("https://example.com/api", {"Authorization": "Bearer token"})
    with pytest.raises(APIError, match="Rate limit exceeded."):
        client.get_data("endpoint")
