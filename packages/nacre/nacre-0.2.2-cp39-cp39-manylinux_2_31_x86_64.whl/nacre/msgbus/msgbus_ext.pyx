from typing import Any, Callable

import cython

from nautilus_trader.common.clock cimport Clock
from nautilus_trader.common.logging cimport Logger
from nautilus_trader.core.correctness cimport Condition
from nautilus_trader.model.identifiers cimport TraderId
from nautilus_trader.msgbus.bus cimport MessageBus
from nautilus_trader.msgbus.subscription cimport Subscription

from nacre.msgbus.pubsub cimport PubSub


cdef class MessageBusExt(MessageBus):

    def __init__(
        self,
        TraderId trader_id not None,
        Clock clock not None,
        Logger logger not None,
        PubSub pubsub not None,
        str name=None,
    ):
        super().__init__(
            trader_id=trader_id,
            clock=clock,
            logger=logger,
            name=name,
        )

        self._pubsub = pubsub

    cpdef void subscribe_ext(self, str topic, handler: Callable[[Any], None]) except *:
        self._pubsub.subscribe(topic, handler)

    cpdef void unsubscribe_ext(self, str topic, handler: Callable[[Any], None]) except *:
        self._pubsub.unsubscribe(topic, handler)

    @cython.boundscheck(False)
    @cython.wraparound(False)
    cdef void publish_c(self, str topic, msg: Any) except *:
        Condition.not_none(topic, "topic")
        Condition.not_none(msg, "msg")

        # Get all subscriptions matching topic pattern
        cdef Subscription[:] subs = self._patterns.get(topic)
        if subs is None:
            # Add the topic pattern and get matching subscribers
            subs = self._resolve_subscriptions(topic)

        # Send message to all matched subscribers
        cdef int i
        for i in range(len(subs)):
            subs[i].handler(msg)

        self.pub_count += 1

        self.publish_ext(topic, msg)

    cdef void publish_ext(self, str topic, msg: Any) except *:
        if self._pubsub.can_handle(topic):
            self._pubsub.publish(topic, msg)
