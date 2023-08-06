from cpython.datetime cimport timedelta
from nautilus_trader.core.uuid cimport UUID4
from nautilus_trader.model.c_enums.order_side cimport OrderSide
from nautilus_trader.model.identifiers cimport ClientOrderId
from nautilus_trader.model.instruments.base cimport Instrument
from nautilus_trader.model.objects cimport Quantity
from nautilus_trader.model.orders.base cimport Order


cdef class TwapOrder:
    cdef readonly UUID4 id
    cdef readonly Instrument instrument
    cdef readonly OrderSide order_side
    cdef readonly Quantity quantity
    cdef readonly timedelta twap_interval
    cdef readonly Quantity twap_slice_amount
    cdef readonly int count

    cdef readonly list client_suborder_ids
    """list of suborders' client_order_id """

    cpdef void append_suborder(self, Order sub_order) except *
    cpdef bint is_completed(self)
