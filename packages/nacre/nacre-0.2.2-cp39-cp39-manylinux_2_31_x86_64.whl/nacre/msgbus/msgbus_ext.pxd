from nautilus_trader.msgbus.bus cimport MessageBus

from nacre.msgbus.pubsub cimport PubSub


cdef class MessageBusExt(MessageBus):
    cdef PubSub _pubsub

    cpdef void subscribe_ext(self, str topic, handler) except *
    cpdef void unsubscribe_ext(self, str topic, handler) except *

    cdef void publish_ext(self, str topic, msg) except *
