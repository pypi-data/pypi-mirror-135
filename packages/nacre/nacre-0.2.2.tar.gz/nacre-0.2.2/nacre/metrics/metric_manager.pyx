from nautilus_trader.model.data.tick cimport QuoteTick
from nautilus_trader.model.data.tick cimport TradeTick

from nacre.model.data.tick cimport MarkTick
from nacre.model.report_position cimport ReportedAccount
from nacre.model.report_position cimport ReportedPosition
from nacre.model.report_position cimport WalletBalance

from prometheus_client import Counter
from prometheus_client import Gauge
from prometheus_client import Histogram


cdef class MetricManager:
    def __init__(self):

        self.quote_tick_price = Gauge("nacre_quote_tick_price", "quote tick price", ["venue", "symbol", "side"])
        self.trade_tick_price = Gauge("nacre_trade_tick_price", "trade tick price", ["venue", "symbol"])
        self.mark_tick_price = Gauge("nacre_mark_tick_price", "mark tick price", ["venue", "symbol"])

        self.account_maint_margin = Gauge(
            "nacre_account_maint_margin", "account maint margin", ["account_id", "asset"]
        )
        self.account_margin = Gauge(
            "nacre_account_margin_balance", "account margin balance", ["account_id", "asset"]
        )
        self.account_balance = Gauge("nacre_account_balance", "account balance", ["account_id", "asset"])

        self.position_margin = Gauge(
            "nacre_position_margin", "position margin balance", ["account_id", "venue", "symbol", "side"]
        )
        self.position_maint_margin = Gauge(
            "nacre_position_maint_margin",
            "position maint margin",
            ["account_id", "venue", "symbol", "side"],
        )
        self.position_quantity = Gauge(
            "nacre_position_quantity", "position quantity total", ["account_id", "venue", "symbol", "side"]
        )
        self.position_multiplier = Gauge(
            "nacre_position_multiplier", "position multiplier", ["account_id", "venue", "symbol", "side"]
        )
        self.position_entry_price = Gauge(
            "nacre_position_entry_price", "position entry price", ["account_id", "venue", "symbol", "side"]
        )
        self.position_liquid_price = Gauge(
            "nacre_position_liquidity_price",
            "position liquidity price",
            ["account_id", "venue", "symbol", "side"],
        )
        self.position_unrealized_pnl = Gauge(
            "nacre_position_unpnl",
            "position unrealized profit and loss",
            ["account_id", "venue", "symbol", "side"],
        )

    cpdef void apply_quote_tick(self, QuoteTick tick):
        self.quote_tick_price.labels(
            venue=tick.instrument_id.venue, symbol=tick.instrument_id.symbol, side="bid"
        ).set(tick.bid.as_decimal())

        self.quote_tick_price.labels(
            venue=tick.instrument_id.venue, symbol=tick.instrument_id.symbol, side="ask"
        ).set(tick.ask.as_decimal())

    cpdef void apply_trade_tick(self, TradeTick tick):
        self.trade_tick_price.labels(
            venue=tick.instrument_id.venue, symbol=tick.instrument_id.symbol
        ).set(tick.price.as_decimal())

    cpdef void apply_mark_tick(self, MarkTick tick):
        self.mark_tick_price.labels(
            venue=tick.instrument_id.venue, symbol=tick.instrument_id.symbol
        ).set(tick.price.as_decimal())

    cpdef void apply_report_position(self, ReportedAccount account):  # noqa: C901
        account_id = account.account_id

        cdef WalletBalance balance
        for balance in account.balances:
            asset = balance.asset.code
            self.account_balance.labels(account_id=account_id, asset=asset).set(balance.total)
            if balance.maint_margin is not None:
                self.account_maint_margin.labels(account_id=account_id, asset=asset).set(
                    balance.maint_margin
                )
            if balance.margin is not None:
                self.account_margin.labels(account_id=account_id, asset=asset).set(balance.margin)

        cdef ReportedPosition po
        for po in account.positions:
            if po.margin is not None:
                self.position_margin.labels(
                    account_id=account_id,
                    venue=po.instrument_id.venue,
                    symbol=po.instrument_id.symbol,
                    side=po.side,
                ).set(po.margin)
            if po.maint_margin is not None:
                self.position_maint_margin.labels(
                    account_id=account_id,
                    venue=po.instrument_id.venue,
                    symbol=po.instrument_id.symbol,
                    side=po.side,
                ).set(po.maint_margin)
            if po.net_qty is not None:
                self.position_quantity.labels(
                    account_id=account_id,
                    venue=po.instrument_id.venue,
                    symbol=po.instrument_id.symbol,
                    side=po.side,
                ).set(po.net_qty)
            if po.multiplier is not None:
                self.position_multiplier.labels(
                    account_id=account_id,
                    venue=po.instrument_id.venue,
                    symbol=po.instrument_id.symbol,
                    side=po.side,
                ).set(po.multiplier)
            if po.avg_px_open is not None:
                self.position_entry_price.labels(
                    account_id=account_id,
                    venue=po.instrument_id.venue,
                    symbol=po.instrument_id.symbol,
                    side=po.side,
                ).set(po.avg_px_open)
            if po.liquidity_px is not None:
                self.position_liquid_price.labels(
                    account_id=account_id,
                    venue=po.instrument_id.venue,
                    symbol=po.instrument_id.symbol,
                    side=po.side,
                ).set(po.liquidity_px)
            if po.unrealized_pnl is not None:
                self.position_unrealized_pnl.labels(
                    account_id=account_id,
                    venue=po.instrument_id.venue,
                    symbol=po.instrument_id.symbol,
                    side=po.side,
                ).set(po.unrealized_pnl)
