import time
import logging

from confluent_kafka import Message
from confluent_kafka.serialization import StringDeserializer
from jlab_jaws.avro.serde import AlarmInstanceSerde, AlarmClassSerde, AlarmActivationUnionSerde, \
    AlarmLocationSerde, AlarmOverrideUnionSerde, AlarmOverrideKeySerde, EffectiveActivationSerde, \
    EffectiveAlarmSerde, EffectiveRegistrationSerde
from jlab_jaws.eventsource.table import EventSourceTable
from jlab_jaws.eventsource.listener import EventSourceListener
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


def log_exception(e):
    logger.exception(e)


class CachedTable(EventSourceTable):

    def __init__(self, config):
        self._cache: Dict[Any, Message] = {}

        super().__init__(config)

        self._listener = CacheListener(self)

        self.add_listener(self._listener)

    def update_cache(self, msgs: Dict[Any, Message]) -> None:
        for msg in msgs.values():
            if msg.value() is None:
                if msg.key() in self._cache:
                    del self._cache[msg.key()]
            else:
                self._cache[msg.key()] = msg

    def await_get(self, timeout_seconds) -> List[Message]:
        """
        Synchronously get messages up to highwater mark.  Blocks with a timeout.

        :param timeout_seconds: Seconds to wait for highwater to be reached
        :return: List of Message
        :raises TimeoutException: If highwater is not reached before timeout
        """
        self.await_highwater(timeout_seconds)
        return self._cache


class CacheListener(EventSourceListener):

    def __init__(self, parent: CachedTable):
        self._parent = parent

    def on_highwater(self):
        self._parent._highwater_signal.set()

    def on_highwater_timeout(self):
        pass

    def on_batch(self, msgs: Dict[Any, Message]):
        self._parent.update_cache(msgs)


class CategoryCachedTable(CachedTable):
    def __init__(self, bootstrap_servers):
        key_deserializer = StringDeserializer('utf_8')
        value_deserializer = StringDeserializer('utf_8')

        ts = time.time()

        config = {'topic': 'alarm-categories',
                  'bootstrap.servers': bootstrap_servers,
                  'key.deserializer': key_deserializer,
                  'value.deserializer': value_deserializer,
                  'group.id': 'category-cached-table' + str(ts)}

        super().__init__(config)


class LocationCachedTable(CachedTable):
    def __init__(self, bootstrap_servers, schema_registry_client):
        key_deserializer = StringDeserializer('utf_8')
        value_deserializer = AlarmLocationSerde.deserializer(schema_registry_client)

        ts = time.time()

        config = {'topic': 'alarm-locations',
                  'bootstrap.servers': bootstrap_servers,
                  'key.deserializer': key_deserializer,
                  'value.deserializer': value_deserializer,
                  'group.id': 'location-cached-table' + str(ts)}

        super().__init__(config)


class InstanceCachedTable(CachedTable):
    def __init__(self, bootstrap_servers, schema_registry_client):
        key_deserializer = StringDeserializer('utf_8')
        value_deserializer = AlarmInstanceSerde.deserializer(schema_registry_client)

        ts = time.time()

        config = {'topic': 'alarm-instances',
                  'bootstrap.servers': bootstrap_servers,
                  'key.deserializer': key_deserializer,
                  'value.deserializer': value_deserializer,
                  'group.id': 'instance-cached-table' + str(ts)}

        super().__init__(config)


class ClassCachedTable(CachedTable):
    def __init__(self, bootstrap_servers, schema_registry_client):
        key_deserializer = StringDeserializer('utf_8')
        value_deserializer = AlarmClassSerde.deserializer(schema_registry_client)

        ts = time.time()

        config = {'topic': 'alarm-classes',
                  'bootstrap.servers': bootstrap_servers,
                  'key.deserializer': key_deserializer,
                  'value.deserializer': value_deserializer,
                  'group.id': 'class-cached-table' + str(ts)}

        super().__init__(config)


class ActivationCachedTable(CachedTable):
    def __init__(self, bootstrap_servers, schema_registry_client):
        key_deserializer = StringDeserializer('utf_8')
        value_deserializer = AlarmActivationUnionSerde.deserializer(schema_registry_client)

        ts = time.time()

        config = {'topic': 'alarm-activations',
                  'bootstrap.servers': bootstrap_servers,
                  'key.deserializer': key_deserializer,
                  'value.deserializer': value_deserializer,
                  'group.id': 'activation-cached-table' + str(ts)}

        super().__init__(config)


class OverrideCachedTable(CachedTable):
    def __init__(self, bootstrap_servers, schema_registry_client):
        key_deserializer = AlarmOverrideKeySerde.deserializer(schema_registry_client)
        value_deserializer = AlarmOverrideUnionSerde.deserializer(schema_registry_client)

        ts = time.time()

        config = {'topic': 'alarm-overrides',
                  'bootstrap.servers': bootstrap_servers,
                  'key.deserializer': key_deserializer,
                  'value.deserializer': value_deserializer,
                  'group.id': 'override-cached-table' + str(ts)}

        super().__init__(config)


class EffectiveRegistrationCachedTable(CachedTable):
    def __init__(self, bootstrap_servers, schema_registry_client):
        key_deserializer = StringDeserializer('utf_8')
        value_deserializer = EffectiveRegistrationSerde.deserializer(schema_registry_client)

        ts = time.time()

        config = {'topic': 'effective-registrations',
                  'bootstrap.servers': bootstrap_servers,
                  'key.deserializer': key_deserializer,
                  'value.deserializer': value_deserializer,
                  'group.id': 'effective-registration-cached-table' + str(ts)}

        super().__init__(config)


class EffectiveActivationCachedTable(CachedTable):
    def __init__(self, bootstrap_servers, schema_registry_client):
        key_deserializer = StringDeserializer('utf_8')
        value_deserializer = EffectiveActivationSerde.deserializer(schema_registry_client)

        ts = time.time()

        config = {'topic': 'effective-activations',
                  'bootstrap.servers': bootstrap_servers,
                  'key.deserializer': key_deserializer,
                  'value.deserializer': value_deserializer,
                  'group.id': 'effective-activation-cached-table' + str(ts)}

        super().__init__(config)


class EffectiveAlarmCachedTable(CachedTable):
    def __init__(self, bootstrap_servers, schema_registry_client):
        key_deserializer = StringDeserializer('utf_8')
        value_deserializer = EffectiveAlarmSerde.deserializer(schema_registry_client)

        ts = time.time()

        config = {'topic': 'effective-alarms',
                  'bootstrap.servers': bootstrap_servers,
                  'key.deserializer': key_deserializer,
                  'value.deserializer': value_deserializer,
                  'group.id': 'effective-alarm-cached-table' + str(ts)}

        super().__init__(config)
