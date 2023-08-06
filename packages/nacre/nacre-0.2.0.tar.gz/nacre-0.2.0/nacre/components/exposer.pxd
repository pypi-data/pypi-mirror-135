from nautilus_trader.cache.cache cimport Cache
from nautilus_trader.common.clock cimport Clock
from nautilus_trader.common.component cimport Component
from nautilus_trader.common.logging cimport Logger
from nautilus_trader.common.logging cimport LoggerAdapter
from nautilus_trader.core.correctness cimport Condition
from nautilus_trader.data.messages cimport DataCommand
from nautilus_trader.model.data.base cimport GenericData
from nautilus_trader.model.data.tick cimport QuoteTick
from nautilus_trader.model.data.tick cimport TradeTick
from nautilus_trader.model.identifiers cimport ComponentId
from nautilus_trader.model.identifiers cimport InstrumentId

from nacre.model.data.tick cimport MarkTick
from nacre.model.report_position cimport ReportedAccount


cdef class Exposer(Component):
    cdef Cache _cache
    cdef object _loop
    cdef object _runner
    cdef object _metric_manager

    cdef object _run_http_server_task
    cdef readonly bint is_running

    # -- ABSTRACT METHODS ------------------------------------------------------------------------------

    cpdef void _on_start(self) except *
    cpdef void _on_stop(self) except *

    cpdef void update_generic_data(self, GenericData data) except *
    cpdef void update_quote_tick(self, QuoteTick tick) except *
    cpdef void update_trade_tick(self, TradeTick tick) except *
    cpdef void update_report_position(self, ReportedAccount account) except *
