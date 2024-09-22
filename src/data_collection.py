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

from src.api_client import APIClient
from src.error_handling import APIError, log_error
from src.config import load_config

config = load_config()


def fetch_threat_data():
    """
    Fetch threat data from various sources and return the combined result.

    :return: (list) A list of threat intelligence data.
    """
    try:
        alien_vault = APIClient("https://otx.alienvault.com/api/v1",
                                {"X-OTX-API-KEY": config['api_keys']['alien_vault']})
        vt = APIClient("https://www.virustotal.com/api/v3", {"x-apikey": config['api_keys']['virus_total']})

        alien_vault_data = alien_vault.get_data("indicators/export")
        vt_data = vt.get_data("files", params={"limit": 10})

        return alien_vault_data + vt_data
    except APIError as e:
        log_error(f"Failed to fetch threat data: {e}")
        return []
