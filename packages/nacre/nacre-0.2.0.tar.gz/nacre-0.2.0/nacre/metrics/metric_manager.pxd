from prometheus_client import Counter
from prometheus_client import Gauge
from prometheus_client import Histogram

from nautilus_trader.model.data.tick cimport QuoteTick
from nautilus_trader.model.data.tick cimport TradeTick

from nacre.model.data.tick cimport MarkTick
from nacre.model.report_position cimport ReportedAccount


cdef class MetricManager:

    cdef readonly object quote_tick_price
    cdef readonly object trade_tick_price
    cdef readonly object mark_tick_price

    cdef readonly object account_maint_margin
    cdef readonly object account_margin
    cdef readonly object account_balance
    cdef readonly object position_margin
    cdef readonly object position_maint_margin
    cdef readonly object position_quantity
    cdef readonly object position_multiplier
    cdef readonly object position_entry_price
    cdef readonly object position_liquid_price
    cdef readonly object position_unrealized_pnl

    cpdef void apply_quote_tick(self, QuoteTick tick)
    cpdef void apply_trade_tick(self, TradeTick tick)
    cpdef void apply_mark_tick(self, MarkTick tick)
    cpdef void apply_report_position(self, ReportedAccount account)
