from nacre.msgbus.pubsub cimport PubSub
from nacre.serialization.base cimport AsyncSerializer


cdef class KafkaPubSub(PubSub):
    cdef bytes _key
    cdef object _producer
    cdef object _consumer
    cdef object config
    cdef AsyncSerializer _serializer
    cdef object _start_producer_task
    cdef object _stop_producer_task
