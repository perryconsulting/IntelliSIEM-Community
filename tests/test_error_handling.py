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
from src.error_handling import APIError, ConfigError, DataError, log_error
import logging


def test_api_error():
    """
    Test that the APIError exception can be raised and caught correctly.
    """
    with pytest.raises(APIError, match="API issue occurred"):
        raise APIError("API issue occurred.")


def test_config_error():
    """
    Test that the ConfigError exception can be raised and caught correctly.
    """
    with pytest.raises(ConfigError, match="Configuration issue occurred"):
        raise ConfigError("Configuration issue occurred.")


def test_data_error():
    """
    Test that the DataError exception can be raised and caught correctly.
    """
    with pytest.raises(DataError, match="Data issue occurred"):
        raise DataError("Data issue occurred.")


def test_log_error(mocker):
    """
    Test that the log_error function logs an error message correctly.
    """
    mocker.patch('logging.error')
    log_error("Test error message.")
    logging.error.assert_called_once_with("Test error message.")


def test_log_warning(mocker):
    """
    Test that the log_error function logs a warning message correctly.
    """
    mocker.patch('logging.warning')
    log_error("Test warning message.", level="WARNING")
    logging.warning.assert_called_once_with("Test warning message.")


def test_log_info(mocker):
    """
    Test that the log_error function logs an informational message correctly.
    """
    mocker.patch('logging.info')
    log_error("Test info message.", level="INFO")
    logging.info.assert_called_once_with("Test info message.")
