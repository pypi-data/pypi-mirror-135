import logging
import json
from nubium_utils import parse_headers
from nubium_utils.custom_exceptions import ProduceHeadersException
from nubium_utils.metrics import MetricsManager
from .message_utils import confirm_produce
from .confluent_runtime_vars import env_vars
from .confluent_configs import init_producer_configs, get_kafka_configs
from confluent_kafka import SerializingProducer
from confluent_kafka.schema_registry.avro import AvroSerializer


LOGGER = logging.getLogger(__name__)


def producer_serializers(schema_dict, schema_registry):
    return {topic: AvroSerializer(schema_registry, json.dumps(schema)) for topic, schema in schema_dict.items() if
            schema}


def get_producers(topic_schema_dict, cluster_name, schema_registry, return_as_singular=True, transactional=False):
    producer_topic_dict = {}
    LOGGER.debug('Setting up Kafka Producer')
    for topic, schema in topic_schema_dict.items():
        temp_schema_dict = {topic: schema}
        producer = SerializingProducer(init_producer_configs(temp_schema_dict, schema_registry, get_kafka_configs(cluster_name)[0], cluster_name))
        setattr(producer, 'topic', topic)
        setattr(producer, 'schema_dict', producer_serializers(temp_schema_dict, schema_registry))
        LOGGER.debug(f'Producer configuration for topic {topic} complete.')
        producer_topic_dict[topic] = producer
    LOGGER.debug('Producer setup complete.')
    if return_as_singular:
        if len(topic_dict) == 1:
            return list(producer_topic_dict.values())[0]
    return producer_topic_dict


def produce_message(producer, producer_kwargs: dict, metrics_manager: MetricsManager = None,
                    consumed_msg_headers_passthrough: tuple = ()):
    """
    Helper for producing a message with confluent_kafka producers; primarily handles headers passthrough and enforcing
    all required headers fields exist before producing.
    You can pass in the previous message headers via 'consumed_msg_headers_passthrough', which extracts the headers.
    Then, if you wish to overwrite any of them, you can provide your own "headers" keyword in 'producer_kwargs'
    which will take that dict and overwrite any matching key in the 'consumed_msg_headers_passthrough' argument.
    You can also provide a None value for a key to remove it entirely.
    :param producer: A confluent_kafka producer
    :type: confluent_kafka.Producer or confluent_kafka.avro.AvroProducer
    :param producer_kwargs: the kwargs to pass into the producer instance
    :type producer_kwargs: dict
    :param metrics_manager: a MetricsManager object instance
    :type metrics_manager: MetricsManager
    :param consumed_msg_headers_passthrough: confluent_kafka Message.headers() from a consumed msg; will add all to new message
    :type consumed_msg_headers_passthrough: tuple
    """
    required_fields = ['guid', 'last_updated_by']

    if 'header' in producer_kwargs:
        raise KeyError('"header" is not the appropriate key for producing message headers; use "headers" instead')

    headers_out = parse_headers(consumed_msg_headers_passthrough)
    headers_out.update(producer_kwargs.get('headers', {}))
    headers_out = {key: value for key, value in headers_out.items() if value is not None}
    missing_required_keys = [key for key in required_fields if key not in headers_out]
    if missing_required_keys:
        raise ProduceHeadersException(f'Message headers are missing the required key(s): {missing_required_keys}')
    producer_kwargs['headers'] = headers_out

    LOGGER.debug('Polling for previous successful produce callbacks before adding additional produces to queue...')
    producer.poll(0)

    # multi-producer management
    if "topic" not in producer_kwargs and hasattr(producer, 'topic'):
        producer_kwargs.update({'topic': producer.topic})
    
    producer._value_serializer = producer.schema_dict[producer_kwargs['topic']]

    LOGGER.debug(f'Adding a message to the produce queue for topic {producer_kwargs["topic"]} for key {repr(producer_kwargs["key"])}')
    producer.produce(**producer_kwargs)
    if metrics_manager:
        metrics_manager.inc_messages_produced(1, producer_kwargs['topic'])
    LOGGER.info(f'Message added to the produce queue; GUID {headers_out.get("guid")}')
