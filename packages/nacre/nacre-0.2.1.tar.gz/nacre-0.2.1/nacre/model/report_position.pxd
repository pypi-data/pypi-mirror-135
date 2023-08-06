from decimal import Decimal

from libc.stdint cimport int64_t
from libc.stdint cimport uint8_t
from nautilus_trader.core.message cimport Event
from nautilus_trader.model.c_enums.order_side cimport OrderSide

# from nautilus_trader.model.c_enums.position_side cimport PositionSide
from nautilus_trader.model.currency cimport Currency
from nautilus_trader.model.events.order cimport OrderFilled
from nautilus_trader.model.identifiers cimport AccountId
from nautilus_trader.model.identifiers cimport ClientOrderId
from nautilus_trader.model.identifiers cimport ExecutionId
from nautilus_trader.model.identifiers cimport InstrumentId
from nautilus_trader.model.identifiers cimport PositionId
from nautilus_trader.model.identifiers cimport StrategyId
from nautilus_trader.model.identifiers cimport TraderId
from nautilus_trader.model.objects cimport Money
from nautilus_trader.model.objects cimport Price
from nautilus_trader.model.objects cimport Quantity


cpdef enum SideWithMode:
    BOTH = 1
    LONG = 2
    SHORT = 3

cdef class SideWithModeParser:

    @staticmethod
    cdef str to_str(int value)

    @staticmethod
    cdef SideWithMode from_str(str value) except *

cdef class WalletBalance:
    cdef readonly Currency asset
    cdef readonly object total
    cdef readonly object margin
    cdef readonly object maint_margin
    cpdef str info(self)

cdef class ReportedAccount(Event):
    cdef readonly list positions
    cdef readonly list balances
    cdef readonly AccountId account_id

cdef class ReportedPosition:
    cdef readonly InstrumentId instrument_id
    cdef readonly PositionId position_id
    cdef readonly SideWithMode side
    cdef readonly object net_qty
    cdef readonly object multiplier
    cdef readonly object avg_px_open
    cdef readonly object unrealized_pnl
    cdef readonly object margin
    cdef readonly object maint_margin
    cdef readonly object liquidity_px

    cpdef str info(self)
