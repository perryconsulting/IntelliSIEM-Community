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

import logging
from logging.handlers import RotatingFileHandler

# Set up rotating file handler
handler = RotatingFileHandler('data/error.log', maxBytes=1000000, backupCount=5)
handler.setLevel(logging.ERROR)
handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))

# Add the handler to the root logger
logging.basicConfig(level=logging.ERROR, handlers=[handler])


class APIError(Exception):
    """Custom exception for API-related errors."""
    pass


class ConfigError(Exception):
    """Custom exception for configuration-related errors."""
    pass


class DataError(Exception):
    """Custom exception for data processing errors."""
    pass


def log_error(message, level="ERROR"):
    """
    Log error messages to a file with severity level.

    :param message: (str) The error message to log.
    :param level: (str) The severity level (default is "ERROR").
    """
    if level == "WARNING":
        logging.warning(message)
    elif level == "INFO":
        logging.info(message)
    else:
        logging.error(message)
