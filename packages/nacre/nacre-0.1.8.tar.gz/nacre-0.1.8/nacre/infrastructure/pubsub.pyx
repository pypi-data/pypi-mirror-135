import asyncio
import re

from aiokafka import AIOKafkaProducer

from nacre.msgbus.pubsub cimport PubSub

from nacre.infrastructure.config import PubSubConfig

from nautilus_trader.common.logging cimport Logger
from nautilus_trader.core.correctness cimport Condition
from nautilus_trader.model.identifiers cimport TraderId

from nacre.serialization.avro.serializer cimport AvroSerializer


cdef class KafkaPubSub(PubSub):
    _SNAPSHOT_TOPIC = "events.snapshot"

    def __init__(
        self,
        loop not None: asyncio.AbstractEventLoop,
        TraderId trader_id not None,
        Logger logger not None,
        config: PubSubConfig = None,
    ):
        if config is None:
            config = PubSubConfig()
        Condition.type(config, PubSubConfig, "config")

        super().__init__(loop, trader_id, logger)

        self._key = trader_id.value.encode()
        self.config = config

        # init kafka producer
        self._producer = None
        self._consumer = None

        self._serializer = AvroSerializer(config.schema_registry)

        self._start_producer_task = None
        self._stop_producer_task = None

        self._filters = config.topic_filter.split(",")

    async def _handle_publish(self, str topic, object msg):
        cdef bytes value = b""
        try:
            value = await self._serializer.serialize(msg)
        except Exception as ex:
            self._log.exception(ex)
            return

        cdef str trader_name = self.trader_id.value
        if len(topic) > len(trader_name) and topic[-len(trader_name):] == trader_name:
            topic = topic[:(-len(trader_name)-1)]
            await self._producer.send_and_wait(topic, value=value, key=self._key)
        elif topic.startswith(self._SNAPSHOT_TOPIC):
            key = topic[len(self._SNAPSHOT_TOPIC)+1:].encode()
            await self._producer.send_and_wait(self._SNAPSHOT_TOPIC, value=value, key=key)
        else:
            await self._producer.send_and_wait(topic, value=value, key=self._key)

    cpdef void _on_start(self) except *:
        self._start_producer_task = self._loop.create_task(self._run_producer())

    cpdef void _on_stop(self) except *:
        self._stop_producer_task = self._loop.create_task(self._stop_producer())

    async def _run_producer(self):
        self._producer = AIOKafkaProducer(
            acks=1,
            loop=self._loop,
            bootstrap_servers=self.config.bootstrap_servers,
            security_protocol=self.config.security_protocol,
            client_id=self.trader_id.value,
        )

        await self._producer.start()
        self._log.info("Kafka pubsub started")

    async def _stop_producer(self):
        await self._producer.stop()
        await self._serializer.stop()
        self._log.info("Kafka pubsub stopped")

    cpdef bint can_handle(self, str topic) except *:
        if len(self._filters) == 1 and self._filters[0] == "*":
            return True

        for f in self._filters:
            if re.match(f, topic) is not None:
                return True

        return False

    cpdef bint check_connected(self) except *:
        return self._start_producer_task.done()

    cpdef bint check_disconnected(self) except *:
        if self._stop_producer_task:
            return self._stop_producer_task.done()
        return True
