from cpython.datetime cimport timedelta
from nautilus_trader.model.c_enums.order_side cimport OrderSide
from nautilus_trader.model.data.base cimport Data
from nautilus_trader.model.identifiers cimport InstrumentId
from nautilus_trader.model.instruments.base cimport Instrument
from nautilus_trader.model.objects cimport Price
from nautilus_trader.model.objects cimport Quantity


cpdef enum OrderType:
    MARKET = 1,
    LIMIT = 2,
    STOP_MARKET = 3,
    STOP_LIMIT = 4,
    TWAP = 5,

cdef class ManualOrder(Data):
    cdef readonly list orders

cdef class OrderParams:
    cdef readonly InstrumentId instrument_id
    cdef readonly Quantity amount
    cdef readonly OrderSide order_side
    cdef readonly Price price
    cdef readonly Price stop_price
    cdef readonly timedelta twap_interval
    cdef readonly Quantity twap_slice_amount
    cdef readonly OrderType order_type
