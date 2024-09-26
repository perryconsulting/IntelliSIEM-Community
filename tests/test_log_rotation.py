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
import os
from logging.handlers import RotatingFileHandler
import pytest


@pytest.fixture
def setup_rotating_log():
    """
    Set up a rotating log handler for testing.
    """
    # Define the log file path and cleanup if exists
    log_file = 'data/test_error.log'
    for i in range(6):
        try:
            os.remove(f"{log_file}.{i}")
        except FileNotFoundError:
            pass
    try:
        os.remove(log_file)
    except FileNotFoundError:
        pass

    # Set up rotating file handler
    handler = RotatingFileHandler(log_file, maxBytes=200, backupCount=5)
    handler.setLevel(logging.ERROR)
    handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
    logger = logging.getLogger('test_logger')
    logger.setLevel(logging.ERROR)
    logger.addHandler(handler)
    return logger


def test_log_rotation(setup_rotating_log):
    """
    Test log rotation by generating log entries to exceed maxBytes limit.
    """
    logger = setup_rotating_log
    log_message = "This is a test log message to fill up the log file and trigger rotation."
    log_file = 'data/test_error.log'

    # Write multiple log entries to exceed the maxBytes limit
    for _ in range(50):  # Increase number of entries if needed
        logger.error(log_message)

    # Ensure the main log file and at least one backup exist
    assert os.path.exists(log_file), f"Log file {log_file} does not exist."
    assert os.path.exists(f"{log_file}.1"), f"Backup log file {log_file}.1 does not exist."
