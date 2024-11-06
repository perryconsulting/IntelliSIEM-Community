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

import yaml

from src.python.error_handling import log_error, ConfigError


def load_config(config_file='config/config.yaml'):
    """
    Load configuration from the specified YAML file.

    :param config_file: (str) The path to the YAML configuration file.
    :return: dict: Configuration data.
    :raises ConfigError: If there is an error with the configuration file.
    """
    try:
        with open(config_file, 'r') as file:
            return yaml.safe_load(file)
    except yaml.YAMLError as e:
        log_error(f"YAML parsing error while loading configuration: {e}.")
        raise ConfigError(f"Configuration file error: {e}.")
    except FileNotFoundError:
        log_error(f"Configuration file not found: {config_file}.")
        raise FileNotFoundError(f"Configuration file not found: {config_file}.")
    except PermissionError:
        log_error(f"Permission denied for config file: {config_file}.")
        raise ConfigError("Permission denied for config file.")
    except OSError as e:
        log_error(f"Disk space issue while loading configuration: {e}.")
        raise ConfigError("Disk space issue while loading configuration.")
