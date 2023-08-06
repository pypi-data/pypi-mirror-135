import itertools
import json
import logging
from time import sleep
from copy import deepcopy
from confluent_kafka import KafkaException, TopicPartition
from confluent_kafka.error import KafkaError
from confluent_kafka.admin import AdminClient, NewTopic
from fastavro.validation import validate
from unittest.mock import MagicMock
from nubium_utils import log_and_raise_error
from nubium_utils.confluent_utils import get_producers, produce_message, shutdown_cleanup, handle_no_messages
from nubium_utils.confluent_utils.confluent_runtime_vars import env_vars
from nubium_utils.confluent_utils.confluent_configs import init_schema_registry_configs
from nubium_utils.custom_exceptions import NoMessageError, SignalRaise
from .transaction_utils import GtfoBatchApp


LOGGER = logging.getLogger(__name__)


class DudeConsumer(GtfoBatchApp):
    def seek_consumer_to_beginning(self):
        LOGGER.info('Setting up consumer to pull from the beginning of the topics...')
        self.consumer.poll(5)
        partitions = self.consumer.assignment()
        LOGGER.debug('Seeking all partitions to 0...')
        for partition in partitions:
            offset = self.consumer.get_watermark_offsets(partition)[0]
            topic = partition.topic
            p = partition.partition
            LOGGER.debug(f'Seeking {topic} p{p} to offset {offset}')
            self.consumer.seek(TopicPartition(topic=topic, partition=p, offset=offset))

    def _app_run_loop(self, *args, **kwargs):
        self.seek_consumer_to_beginning()
        self.all_messages = [] # allows you to do batches still, and return transformed versions of the messages
        LOGGER.debug('Beginning consumption loop...')
        consuming = True
        try:
            while consuming:
                try:
                    messages = []
                    self.consume(*args, **kwargs)
                    if self.app_function:
                        messages = self.app_function(self.transaction) # allows you to transform msgs to desired result if you'd like
                    if not messages: # if app_function does not return anything (maybe they passed a placeholder function or something)
                        messages = self.transaction.messages()
                    self.all_messages += messages
                    if not self.transaction._committed:
                        self.transaction.commit()
                except NoMessageError:
                    producer.poll(0)
                    LOGGER.debug('All messages pulled!')
                    consuming = False
                except Exception as e:
                    LOGGER.error(e)
                    raise
        finally:
            raise Exception(f'DudeConsumer operations complete: total messages: {len(self.all_messages)}')

    def run(self):
        super().run()
        return self.all_messages


class KafkaToolbox:
    """
    Helpful functions for interacting with Kafka (mainly RHOSAK).
    Allows you to interface with multiple clusters at once by default assuming they are defined via your environment
    variables NUBIUM_CLUSTER_{N}. Actions include:

    Topics (multiple): create, delete, list.

    Messages (multiple): produce, consume
    """

    def __init__(self, cluster_configs=None, topic_configs=None, auto_configure=True):
        self.admin_clients = {}
        self.producers = {}
        self.consumer = {}
        self.schema_registry = None

        if not cluster_configs:
            cluster_configs = json.loads(env_vars()['NU_KAFKA_CLUSTERS_CONFIGS_JSON'])
        self.cluster_configs = cluster_configs
        if not topic_configs:
            topic_configs = json.loads(env_vars()['NU_TOPIC_CONFIGS_JSON'])
        self.topic_configs = topic_configs
        if self.cluster_configs and auto_configure:
            self.add_admin_cluster_clients(self.cluster_configs)

    def add_admin_cluster_clients(self, configs):
        """
        Add a new client connection for a given cluster.
        Added to 'self.admin_clients', where k:v is cluster_bootstrap_url: cluster_client_instance.

        By default, uses your environment to establish the client aside from the cluster URLS.

        You can provide configs in the following ways:
            {cluster1_confluent_config_dict}
            'cluster1_bootstrap_url'
        or lists of either.
        """
        if isinstance(configs, str):
            if self.cluster_configs: # "config" passed was just a cluster name
                configs = {configs: self.cluster_configs[configs]}
            else:
                raise Exception(f'Cant create admin client for {configs}; no cluster config metadata was provided for that name.')
        for cluster_name, cluster_config in configs.items():
            if cluster_name not in self.admin_clients:
                sleep(.2)
                apply_config = {
                    "bootstrap.servers": cluster_config['url']
                }
                if 'localhost' not in cluster_config['url']:
                    apply_config.update({
                        "sasl.username": cluster_config['username'],
                        "sasl.password": cluster_config['password'],
                        "security.protocol": "sasl_ssl",
                        "sasl.mechanisms": "PLAIN",
                    })
                client = AdminClient(apply_config)
                self.admin_clients[cluster_name] = client

    def create_all_topics(self):
        """Creates all the topics by passing the whole topic map to create_topics."""
        self.create_topics(self.topic_configs)

    def create_topics(self, topic_cluster_dict, num_partitions=None, replication_factor=None, topic_config=None,
                      ignore_topic_configs=False):
        """
        Accepts a "topic_cluster_dict" like: {'topic_a': 'cluster_x', 'topic_b': 'cluster_y', 'topic_c': ''}
        If cluster name is provided, will default to that; else, will attempt to derive using nubium_schemas
        if "use_nubium_topic_cluster_maps" is True.
        Otherwise, if "ignore_nubium_topic_cluster_maps" is False, creates topic with predefined nubium_schemas configs.
        Else, will use the args "num_partitions", "replication_factor", "topic_config".
        """
        if isinstance(topic_cluster_dict, list):
            topic_cluster_dict = {k: self.topic_configs[k] for k in topic_cluster_dict}
        topic_cluster_dict = {k: {'cluster': v} if isinstance(v, str) else v for k,v in topic_cluster_dict.items()}
        topic_dict = {}
        for topic, configuration in topic_cluster_dict.items():
            if not configuration.get('cluster'):
                configuration['cluster'] = self.topic_configs[topic]['cluster']
            if not configuration.get('configs'):
                configuration['configs'] = self.topic_configs.get(topic, {}).get('configs', {})
            partitions = num_partitions if num_partitions else configuration.get('configs', {}).get('num_partitions', 3)
            rep_factor = replication_factor if replication_factor else configuration.get('configs', {}).get('replication_factor', 3)
            config = topic_config if topic_config else configuration.get('configs', {}).get('config', {})
            topic_dict[configuration['cluster']] = topic_dict.get(configuration['cluster'], []) + [
                NewTopic(
                topic=topic,
                num_partitions=partitions,
                replication_factor=rep_factor,
                config=config)]
        for cluster, topic_creates in topic_dict.items():
            self.add_admin_cluster_clients(cluster)
            for topic in topic_creates:
                try:
                    _wait_on_futures_map(self.admin_clients[cluster].create_topics([topic]))
                    print(f"Topic created: {topic}")
                except KafkaException as e:
                    if e.args[0].code() == KafkaError.TOPIC_ALREADY_EXISTS:
                        print(f"Topic already exists: {topic}")
                        pass
                    else:
                        raise

    def delete_topics(self, topic_cluster_dict, ignore_nubium_topic_cluster_maps=False):
        """
        Accepts a "topic_cluster_dict" like: {'topic_a': 'cluster_url_x', 'topic_b': 'cluster_url_y', 'topic_c': ''}
        If cluster url is provided, will default to that; else, will attempt to derive using nubium_schemas
        if "ignore_nubium_topic_cluster_maps" is False.
        """
        if isinstance(topic_cluster_dict, list):
            topic_cluster_dict = {k: self.topic_configs[k] for k in topic_cluster_dict}
        topic_cluster_dict = {k: {'cluster': v} if isinstance(v, str) else v for k, v in topic_cluster_dict.items()}
        for topic, configuration in topic_cluster_dict.items():
            cluster = configuration['cluster']
            self.add_admin_cluster_clients(cluster)
            try:
                _wait_on_futures_map(self.admin_clients[cluster].delete_topics([topic]))
                print(f"Topic deleted: {topic}")
            except KafkaException as e:
                if e.args[0].code() == KafkaError.UNKNOWN_TOPIC_OR_PART:
                    print(f"Topic deletion failed (likely because it didn't exist): {topic}")
                    pass

    def list_topics(self, by_topic=False, mirrors=False, cluster_name=None):
        """
        Allows you to list all topics across all cluster instances.

        If you want to return the output in a format that is used by the other toolbox functions, then
        you can change "by_topic"=True; the default format makes it easier to read.

        Will not include the mirrored topics by default, but can toggle with "mirrors".
        """
        def _mirror_include(topic):
            if topic.startswith('nubium_'):
                return mirrors
            return True

        def _valid(topic):
            return not topic.startswith('__') and 'schema' not in topic

        if cluster_name:
            self.add_admin_cluster_clients(cluster_name)
        else:
            self.add_admin_cluster_clients(self.cluster_configs)
        by_cluster = {clust: [topic for topic in list(client.list_topics().topics) if _valid(topic) and _mirror_include(topic)]
                      for clust, client in self.admin_clients.items()}
        if by_topic:
            topics = {topic: clust for clust, topics in by_cluster.items() for topic in topics}
            return {k: topics[k] for k in sorted(topics.keys())}
        return {k: sorted(by_cluster[k]) for k in sorted(by_cluster.keys())}

    def produce_messages(self, topic, message_list, schema=None, cluster_name=None):
        """
        Produce a list of messages (each of which is a dict with entries 'key', 'value', 'headers') to a topic.

        Must provide the schema if you haven't produced to that topic on this instance, or if using dude CLI.
        """
        # TODO extra producer error handling?
        if not self.producers.get(topic):
            if not schema:
                raise ValueError('Schema not provided and the topic producer instance was not previously configured. '
                                 'Please provide the schema!')
            if not cluster_name:
                cluster_name = self.topic_configs[topic]['cluster']
            self.add_admin_cluster_clients(cluster_name)
            if not self.schema_registry:
                self.schema_registry = init_schema_registry_configs(as_registry_object=True)
                self.producers.update(get_producers({topic: schema}, cluster_name, self.schema_registry, return_as_singular=False))
        # validate(message, schema)  # Not sure we need this?
        producer = self.producers[topic]
        for message in message_list:
            produce_message(
                producer=producer,
                producer_kwargs=message,
                metrics_manager=MagicMock())  # TODO: change NU to allow a None here? dunno
        producer.flush()

    def consume_messages(self, topics, transform_function=None, consumer=None):
        """
        Consume a list of messages (each of which is a dict with entries 'key', 'value', 'headers') from a topic.
        """
        # TODO: add easy way of changing the consumer group on the fly
        if isinstance(topics, str):
            topics = topics.split(',')
        dude_app = DudeConsumer(
            app_function=transform_function,
            consume_topics_list=topics,
            consumer=consumer,
            produce_topic_schema_dict={topic: "string" for topic in topics} # throwaway until I convert it to accept empty dict for consuming only.
        )
        return dude_app.consume_all_messages()


def _wait_on_futures_map(futures):
    for future in futures.values():
        future.result()
        assert future.done()
        sleep(.1)
