from nautilus_trader.common.logging cimport LoggerAdapter
from nautilus_trader.common.queue cimport Queue
from nautilus_trader.model.identifiers cimport TraderId


cdef class PubSub:
    cdef list _filters
    cdef object _loop
    cdef object _run_queues_task
    cdef Queue _queue
    cdef LoggerAdapter _log
    cdef readonly TraderId trader_id

    cdef readonly bint is_running

    cpdef int qsize(self) except *

    cpdef void start(self) except *
    cpdef void stop(self) except *
    cpdef void dispose(self) except *

    cpdef void _on_start(self) except *
    cpdef void _on_stop(self) except *

    cpdef void kill(self) except *
    cdef void _enqueue_sentinels(self) except *

    # cpdef void _handle_publish(self, str topic, object msg) except *
    cpdef void publish(self, str topic, msg) except *
    cpdef void subscribe(self, str topic, handler) except *
    cpdef void unsubscribe(self, str topic, handler) except *

    cpdef bint can_handle(self, str topic) except *
    cpdef bint check_connected(self) except *
    cpdef bint check_disconnected(self) except *
