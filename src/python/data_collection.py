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

from src.python.api_client import APIClient
from src.python.config import load_config
from src.python.error_handling import APIError, DataError, log_error

config = load_config()


def fetch_threat_data():
    """
    Fetch threat data from various sources and return the combined result.

    :return: (list) A list of threat intelligence data.
    :raises DataError: If there is an error with data integrity or structure.
    """
    try:
        alien_vault = APIClient("https://otx.alienvault.com/api/v1",
                                {"X-OTX-API-KEY": config['api_keys']['alien_vault']})
        vt = APIClient("https://www.virustotal.com/api/v3", {"x-apikey": config['api_keys']['virus_total']})

        alien_vault_data = alien_vault.get_data("indicators/export")
        vt_data = vt.get_data("files", params={"limit": 10})

        # Validate that the data is a list
        if not isinstance(alien_vault_data, list) or not isinstance(vt_data, list):
            log_error(f"Invalid data type received: {type(alien_vault_data)} or {type(vt_data)}.")
            raise DataError("Unexpected data type received.")

        # Define the required keys for validation
        required_keys = ['id']

        # Validate data and raise DataError if required keys are missing or if data is corrupt
        valid_data = []
        for entry in alien_vault_data + vt_data:
            if not isinstance(entry, dict):
                log_error(f"Unexpected data type in entry: {entry}")
                raise DataError("Unexpected data type received.")
            # Check if the 'id' key is present and its value is of expected type
            if 'id' in entry and not isinstance(entry['id'], (str, int)):
                log_error(f"Corrupt data in entry: {entry}. 'id' key has invalid type.")
                raise DataError("Corrupt data received.")
            if any(key not in entry for key in required_keys):
                log_error(f"Missing required data keys in entry: {entry}.")
                raise DataError("Missing required data keys.")
            valid_data.append(entry)

        return valid_data

    except APIError as e:
        log_error(f"Failed to fetch threat data: {e}")
        return []
    except (KeyError, TypeError, ValueError) as e:
        log_error(f"Data error occurred: {e}")
        raise DataError("Corrupt data received.")
