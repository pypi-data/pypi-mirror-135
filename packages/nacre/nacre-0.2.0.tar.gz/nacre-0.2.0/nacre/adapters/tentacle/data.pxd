from nautilus_trader.live.data_client cimport LiveDataClient
from nautilus_trader.model.identifiers cimport TraderId

from nacre.model.data.manual_order cimport ManualOrder


cdef class TentacleDataClient(LiveDataClient):
    cdef object _channel
    cdef object _stub

    cdef object _watch_manual_order_task
    cdef object _watch_control_command_task


    cdef void subscribe_manual_order(self, str trader_id) except *
    cdef void subscribe_control_command(self, str trader_id) except *

    cdef void _on_manual_order(self, ManualOrder manual_order) except *
