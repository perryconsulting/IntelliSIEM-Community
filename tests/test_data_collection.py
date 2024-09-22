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

from src.data_collection import fetch_threat_data, APIError


def test_fetch_threat_data_success(mocker):
    """
    Test fetching threat data with valid API keys.
    """
    mocker.patch('src.api_client.APIClient.get_data', return_value=[{'id': 'test'}])
    threats = fetch_threat_data()
    assert len(threats) > 0


def test_fetch_threat_data_failure(mocker):
    """
    Test fetching threat data with invalid API keys.
    """
    # Mock API client responses to raise an error
    mocker.patch('src.api_client.APIClient.get_data', side_effect=APIError("API Error"))

    # Expect the APIError exception to be raised and handle it in the function
    threats = fetch_threat_data()
    assert threats == []  # Expecting an empty list as a fallback
