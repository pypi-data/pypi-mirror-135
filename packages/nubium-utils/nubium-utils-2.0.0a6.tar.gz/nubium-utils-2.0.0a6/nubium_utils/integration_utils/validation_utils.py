import json
import logging
from os import environ

import pytest

LOGGER = logging.getLogger(__name__)


@pytest.fixture()
def actual_results():
    LOGGER.info('Preparing actual results...')
    with open(environ['TEST_DATA_OUT'], 'r') as f:
        results = json.load(f)
    return [{k: v for k, v in result.items() if k in ['key', 'value']} for result in results]


@pytest.fixture()
def expected_results(map_expected_output):
    LOGGER.info('Preparing expected results...')
    return [{k: v for k, v in message.items() if k in ['key', 'value']} for message in map_expected_output]


def validate_results(actual_results, expected_results):
    LOGGER.info('Validating results...')
    try:
        for expected, actual in zip(expected_results, actual_results):
            for k, v in expected['value'].items():
                assert expected['value'][k] == actual['value'][k]
        LOGGER.info('TEST SUCCESS!')
    except AssertionError:
        LOGGER.info(
            f"TEST FAILURE =(\n\nEXPECTED=\n{json.dumps(expected_results, indent=4)}\n\nACTUAL:\n{json.dumps(actual_results, indent=4)}")
        raise
