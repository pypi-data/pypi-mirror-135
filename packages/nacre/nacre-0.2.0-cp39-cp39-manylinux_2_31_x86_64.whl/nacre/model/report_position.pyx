from decimal import Decimal

from libc.stdint cimport int64_t
from nautilus_trader.core.correctness cimport Condition
from nautilus_trader.core.message cimport Event
from nautilus_trader.core.uuid cimport UUID4
from nautilus_trader.model.c_enums.order_side cimport OrderSide
from nautilus_trader.model.c_enums.order_side cimport OrderSideParser

# from nautilus_trader.model.c_enums.position_side cimport PositionSide
# from nautilus_trader.model.c_enums.position_side cimport PositionSideParser
from nautilus_trader.model.currency cimport Currency
from nautilus_trader.model.events.order cimport OrderFilled
from nautilus_trader.model.identifiers cimport AccountId
from nautilus_trader.model.identifiers cimport ClientOrderId
from nautilus_trader.model.identifiers cimport ExecutionId
from nautilus_trader.model.identifiers cimport InstrumentId
from nautilus_trader.model.identifiers cimport PositionId
from nautilus_trader.model.identifiers cimport StrategyId
from nautilus_trader.model.identifiers cimport TraderId
from nautilus_trader.model.instruments.base cimport Instrument
from nautilus_trader.model.objects cimport Money
from nautilus_trader.model.objects cimport Price
from nautilus_trader.model.objects cimport Quantity


cdef class ReportedAccount(Event):
    def __init__(
        self,
        list positions not None,
        list balances not None,
        AccountId account_id not None,
        UUID4 event_id not None,
        int64_t ts_event,
        int64_t ts_init,
    ):
        super().__init__(event_id, ts_event, ts_init)

        self.account_id = account_id
        self.positions = positions
        self.balances = balances

cdef class WalletBalance:
    def __init__(
        self,
        Currency asset not None,
        total not None,
        margin=None,
        maint_margin=None,
    ):
        self.asset = asset
        self.total = total
        if margin:
            self.margin = margin
        if maint_margin:
            self.maint_margin = maint_margin

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.info()})"

    cpdef str info(self):
        return (
            f"{self.asset=} "
            f"{self.total=} "
            f"{self.margin=} "
            f"{self.maint_margin=} "
        )

cdef class ReportedPosition:
    def __init__(
        self,
        InstrumentId instrument_id not None,
        side not None,
        position_id=None,
        net_qty=None,
        multiplier=None,
        avg_px_open=None,
        unrealized_pnl=None,
        margin=None,
        maint_margin=None,
        liquidity_px=None,
    ):

        self.instrument_id = instrument_id
        self.side = side
        if position_id is not None:
            self.position_id = position_id
        if net_qty is not None:
            self.net_qty = net_qty
        if multiplier is not None:
            self.multiplier = multiplier
        if avg_px_open is not None:
            self.avg_px_open = avg_px_open
        if unrealized_pnl is not None:
            self.unrealized_pnl = unrealized_pnl
        if margin is not None:
            self.margin = margin
        if maint_margin is not None:
            self.maint_margin = maint_margin
        if liquidity_px is not None:
            self.liquidity_px = liquidity_px

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.info()})"

    cpdef str info(self):
        return (
            f"{self.instrument_id=} "
            f"{self.side=} "
            f"{self.multiplier=} "
            f"{self.position_id=} "
            f"{self.net_qty=} "
            f"{self.avg_px_open=} "
            f"{self.unrealized_pnl=} "
            f"{self.margin=} "
            f"{self.maint_margin=} "
            f"{self.liquidity_px=} "
        )


cdef class SideWithModeParser:

    @staticmethod
    cdef str to_str(int value):
        if value == 1:
            return "BOTH"
        elif value == 2:
            return "LONG"
        elif value == 3:
            return "SHORT"
        else:
            raise ValueError(f"value was invalid, was {value}")

    @staticmethod
    cdef SideWithMode from_str(str value) except *:
        if value == "BOTH":
            return SideWithMode.BOTH
        elif value == "LONG":
            return SideWithMode.LONG
        elif value == "SHORT":
            return SideWithMode.SHORT
        else:
            raise ValueError(f"value was invalid, was {value}")

    @staticmethod
    def to_str_py(int value):
        return SideWithModeParser.to_str(value)

    @staticmethod
    def from_str_py(str value):
        return SideWithModeParser.from_str(value)
