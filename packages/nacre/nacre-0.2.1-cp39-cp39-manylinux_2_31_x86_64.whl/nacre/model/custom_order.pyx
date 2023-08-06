from cpython.datetime cimport timedelta
from nautilus_trader.core.uuid cimport UUID4
from nautilus_trader.model.c_enums.order_side cimport OrderSide
from nautilus_trader.model.identifiers cimport ClientOrderId
from nautilus_trader.model.instruments.base cimport Instrument
from nautilus_trader.model.objects cimport Quantity
from nautilus_trader.model.orders.base cimport Order


cdef class TwapOrder:
    def __init__(
        self,
        UUID4 id,
        Instrument instrument,
        OrderSide order_side,
        Quantity quantity,
        timedelta twap_interval,
        Quantity twap_slice_amount,
    ):
        self.id = id
        self.instrument = instrument
        self.order_side = order_side
        self.quantity = quantity
        self.twap_interval = twap_interval
        self.twap_slice_amount = twap_slice_amount

        floor = int(quantity // twap_slice_amount)
        self.count = floor if quantity % twap_slice_amount == 0 else floor + 1  # noqa: S001
        self.client_suborder_ids = []  # type: list[ClientOrderId]

    cpdef void append_suborder(self, Order sub_order) except *:
        self.client_suborder_ids.append(sub_order.client_order_id)

    cpdef bint is_completed(self):
        return len(self.client_suborder_ids) == self.count
