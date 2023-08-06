"""
confluent-kafka runtime environment variables
"""

from os import environ
from nubium_utils import general_runtime_vars
from nubium_utils.env_var_generator import env_vars_creator


def default_env_vars():
    """
    Environment variables that have defaults if not specified.
    """
    return {
        'NU_CONSUMER_POLL_TIMEOUT': environ.get('NU_CONSUMER_POLL_TIMEOUT', '5'),
        'NU_CONSUMER_TIMEOUT_LIMIT_MINUTES': environ.get('NU_CONSUMER_TIMEOUT_LIMIT_MINUTES', '2'),
        'NU_CONSUMER_AUTO_OFFSET_RESET': environ.get('NU_CONSUMER_AUTO_OFFSET_RESET', 'latest'),
        'NU_CONSUMER_TIMESTAMP_OFFSET_MINUTES': environ.get('NU_CONSUMER_TIMESTAMP_OFFSET_MINUTES', '0'), # for retry layers
        'NU_CONSUMER_DEFAULT_BATCH_CONSUME_MAX_COUNT': environ.get('NU_CONSUMER_DEFAULT_BATCH_CONSUME_MAX_COUNT', 1),

        # Performance
        'NU_CONSUMER_AUTO_COMMIT_INTERVAL_SECONDS': str(int(environ.get('NU_CONSUMER_AUTO_COMMIT_INTERVAL_SECONDS', '20'))*1000),
        'NU_CONSUMER_HEARTBEAT_TIMEOUT_SECONDS': str(environ.get('NU_CONSUMER_HEARTBEAT_TIMEOUT_SECONDS', '90')),
        'NU_CONSUMER_MESSAGE_BATCH_MAX_MB': str(int(float(environ.get('NU_CONSUMER_MESSAGE_BATCH_MAX_MB', '2')) * 2 ** 20)),
        'NU_CONSUMER_MESSAGE_TOTAL_MAX_MB': str(int(float(environ.get('NU_CONSUMER_MESSAGE_TOTAL_MAX_MB', '3')) * 2 ** 20)),
        'NU_CONSUMER_MESSAGE_QUEUE_MAX_MB': str(int(float(environ.get('NU_CONSUMER_MESSAGE_QUEUE_MAX_MB', '10')) * 2 ** 10)),
}


def required_env_vars():
    """
    Environment variables that require a value (aka no default specified).
    """
    return {}


def all_env_vars():
    return {
        **general_runtime_vars.all_env_vars(),
        **default_env_vars(),
        **required_env_vars()
    }


env_vars = env_vars_creator(all_env_vars)
