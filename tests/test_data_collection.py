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
# tests/test_data_collection.py

import pytest
from src.data_collection import fetch_threat_data, DataError


def test_fetch_threat_data_success(mocker):
    """
    Test successful fetching of threat data.
    This ensures that data is correctly collected from the APIs and returned.
    """
    mock_data_alien = [{'id': 'test1'}]
    mock_data_virus = [{'id': 'test2'}]

    # Create separate mock instances for each APIClient
    mock_alien_vault_client = mocker.Mock()
    mock_alien_vault_client.get_data.return_value = mock_data_alien

    mock_virus_total_client = mocker.Mock()
    mock_virus_total_client.get_data.return_value = mock_data_virus

    # Patch the APIClient constructor to return the respective mock instances
    mocker.patch('src.data_collection.APIClient', side_effect=[mock_alien_vault_client, mock_virus_total_client])

    threats = fetch_threat_data()

    # Verify that the mock was called only once per client
    mock_alien_vault_client.get_data.assert_called_once()
    mock_virus_total_client.get_data.assert_called_once()

    assert len(threats) == 2  # Expecting two entries: one from each mock data list
    assert threats == [{'id': 'test1'}, {'id': 'test2'}]


def test_fetch_threat_data_missing_keys(mocker):
    """
    Test data collection handling of missing required data keys.
    This ensures that missing keys in the data trigger the appropriate exception.
    """
    # Mock get_data to return an entry missing the required 'id' key
    mocker.patch('src.api_client.APIClient.get_data', return_value=[{'missing_key': 'value'}])
    with pytest.raises(DataError, match="Missing required data keys."):
        fetch_threat_data()


def test_fetch_threat_data_corrupt_data(mocker):
    """
    Test data collection handling of corrupt data.
    This ensures that corrupt data is caught and triggers the DataError exception.
    """
    # Mock get_data to return structurally corrupt data with an unexpected type for 'id'
    mocker.patch('src.api_client.APIClient.get_data',
                 return_value=[{'id': {'unexpected': 'dict'}, 'nested_data': ['unexpected_list']}])

    # Expect DataError to be raised for corrupt data
    with pytest.raises(DataError, match="Corrupt data received."):
        fetch_threat_data()


def test_fetch_threat_data_empty_response(mocker):
    """
    Test fetching threat data with an empty response.
    This ensures that the function handles empty responses gracefully.
    """
    mocker.patch('src.api_client.APIClient.get_data', return_value=[])
    threats = fetch_threat_data()
    assert threats == []  # Expecting an empty list when no data is returned


def test_fetch_threat_data_invalid_data_type(mocker):
    """
    Test data collection handling of invalid data type.
    This simulates an unexpected data type from the API response.
    """
    # Mock get_data to return a non-list data type, such as a string
    mocker.patch('src.api_client.APIClient.get_data', return_value="invalid_data")
    with pytest.raises(DataError, match="Unexpected data type received."):
        fetch_threat_data()
