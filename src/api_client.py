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

import requests
from src.error_handling import APIError, log_error


class APIClient:
    """
    A client for interacting with various threat intelligence APIs.
    """

    def __init__(self, base_url, headers):
        """
        Initialize the API client with the base URL and headers.

        :param base_url: (str) The base URL of the API.
        :param headers: (dict) Headers required for API requests.
        """
        self.base_url = base_url
        self.headers = headers

    def get_data(self, endpoint, params=None):
        """
        Fetch data from the specified endpoint.

        :param endpoint: (str) The API endpoint to fetch data from.
        :param params: (dict) Optional query parameters.
        :return: (dict) JSON response from the API.
        :raises APIError: If there is an error with the API request.
        """
        url = f"{self.base_url}/{endpoint}"
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            if response.status_code == 429:
                retry_after = response.headers.get("Retry-After", "unknown time")
                log_error(f"Rate limit exceeded. Retry after: {retry_after}")
                raise APIError("Rate limit exceeded.")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            log_error("API request timed out")
            raise APIError("API request timed out")
        except requests.exceptions.RequestException as e:
            log_error(f"API request failed: {e}")
            raise APIError(f"API request failed: {e}")
        except ValueError:
            log_error("Invalid JSON response format from API")
            raise APIError("Invalid response format.")  # New error for invalid JSON responses
