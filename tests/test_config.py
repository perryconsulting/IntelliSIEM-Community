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
from src.config import load_config, ConfigError


def test_load_config_success(mocker):
    """
    Test successful loading of the configuration file.
    This ensures that a valid configuration is loaded and returned correctly.
    """
    mock_config = """
    api_keys:
        alien_vault: "VALID_ALIEN_VAULT_API_KEY"
        virus_total: "VALID_VIRUS_TOTAL_API_KEY"
    """
    mocker.patch('builtins.open', mocker.mock_open(read_data=mock_config))
    config = load_config()
    assert config['api_keys']['alien_vault'] == "VALID_ALIEN_VAULT_API_KEY"
    assert config['api_keys']['virus_total'] == "VALID_VIRUS_TOTAL_API_KEY"


def test_load_config_missing_file():
    """
    Test configuration loading with a missing file.
    This ensures that a FileNotFoundError is raised when the config file does not exist.
    """
    with pytest.raises(FileNotFoundError):
        load_config('config/non_existent_config.yaml')


def test_load_config_invalid_format(mocker):
    """
    Test configuration loading with an invalid format.
    This simulates an invalid YAML format and expects a ConfigError.
    """
    invalid_yaml = """
    api_keys:
        alien_vault: !!invalid
    """
    mocker.patch('builtins.open', mocker.mock_open(read_data=invalid_yaml))
    with pytest.raises(ConfigError, match="Configuration file error."):
        load_config()


def test_load_config_permission_error(mocker):
    """
    Test configuration loading with a permission error.
    This simulates a PermissionError when accessing the config file.
    """
    mock_open = mocker.patch('builtins.open', mocker.mock_open())
    mock_open.side_effect = PermissionError
    with pytest.raises(ConfigError, match="Permission denied for config file."):
        load_config()


def test_load_config_disk_space_error(mocker):
    """
    Test configuration loading with a disk space error.
    This simulates an OSError due to lack of disk space.
    """
    mock_open = mocker.patch('builtins.open', mocker.mock_open())
    mock_open.side_effect = OSError("No space left on device")
    with pytest.raises(ConfigError, match="Disk space issue while loading configuration."):
        load_config()
