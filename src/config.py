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


def load_config(config_file='config/config.yaml'):
    """
    Load configuration from the specified YAML file.

    :param config_file: The path to the YAML configuration file.
    :return: dict: Configuration data.
    """

    with open(config_file, 'r') as file:
        return yaml.safe_load(file)
