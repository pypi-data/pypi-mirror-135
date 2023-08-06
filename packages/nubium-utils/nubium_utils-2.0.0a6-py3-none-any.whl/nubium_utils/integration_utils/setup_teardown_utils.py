import json
import logging
import subprocess
from os import environ, remove
from time import sleep
from unittest.mock import patch

import psutil
import pytest

LOGGER = logging.getLogger(__name__)


@pytest.fixture()
def setup_teardown_env_vars(env_vars):
    LOGGER.info("Patching environment variables...")
    env_patch = patch.dict('os.environ', env_vars)
    env_patch.start()
    yield None
    LOGGER.info("Unpatching environment variables...")
    env_patch.stop()


@pytest.fixture()
def setup_teardown_app():
    LOGGER.info("Initializing app...")
    parent = subprocess.Popen("dude app run", shell=True)
    sleep(30)  # wait for app to launch
    yield None
    LOGGER.info("Terminating app...")
    children = psutil.Process(parent.pid)
    for child in children.children(recursive=True):
        child.terminate()


@pytest.fixture()
def setup_teardown_test_data(map_integration_input):
    LOGGER.info("Creating test data input file...")
    with open(environ['TEST_DATA_IN'], 'w') as f:
        json.dump(map_integration_input, f, indent=4, sort_keys=True)
    yield None
    # LOGGER.info("Deleting test data files...")
    remove(environ['TEST_DATA_IN'])
    remove(environ['TEST_DATA_OUT'])
