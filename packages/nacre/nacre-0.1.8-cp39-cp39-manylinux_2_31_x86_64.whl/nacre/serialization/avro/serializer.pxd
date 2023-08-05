from nacre.serialization.base cimport AsyncSerializer


cdef class AvroSerializer(AsyncSerializer):
    cdef object _async_serializer
    cdef object _client
