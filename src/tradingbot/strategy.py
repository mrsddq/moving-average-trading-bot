from dataclasses import dataclass
from math import isfinite
from numbers import Real


@dataclass(frozen=True)
class BacktestResult:
    """End-of-series equity; an open position is marked to the final price."""

    final_cash: float
    final_position: int
    final_equity: float
    trades: int
    return_pct: float


def _finite_number(value, name, *, allow_zero=False):
    if isinstance(value, bool) or not isinstance(value, Real):
        raise ValueError(f"{name} must be a finite number")
    try:
        valid = isfinite(value)
    except OverflowError:
        valid = False
    if not valid or value < 0 or (not allow_zero and value == 0):
        condition = "non-negative" if allow_zero else "positive"
        raise ValueError(f"{name} must be finite and {condition}")


def _validate_inputs(prices, short_window, long_window):
    for window in (short_window, long_window):
        if isinstance(window, bool) or not isinstance(window, int) or window <= 0:
            raise ValueError("window sizes must be positive integers")
    if short_window >= long_window:
        raise ValueError("short_window must be smaller than long_window")
    if not prices:
        raise ValueError("prices must not be empty")
    for price in prices:
        _finite_number(price, "prices")


def _signal(prices, short_window, long_window):
    if len(prices) < long_window:
        return "hold"
    # Divide before summing to avoid overflowing on large, finite prices.
    short_average = sum(price / short_window for price in prices[-short_window:])
    long_average = sum(price / long_window for price in prices[-long_window:])
    if short_average > long_average:
        return "buy"
    if short_average < long_average:
        return "sell"
    return "hold"


def moving_average_signal(prices, short_window=3, long_window=5):
    """Return buy/sell/hold from the current moving-average relationship."""
    _validate_inputs(prices, short_window, long_window)
    return _signal(prices, short_window, long_window)


def backtest_moving_average(
    prices,
    short_window=3,
    long_window=5,
    starting_cash=10000.0,
    transaction_cost=0.0,
):
    """Simulate one share, filling each historical signal at the NEXT bar price.

    Signals use only earlier observations. A flat per-fill fee is charged on
    both buys and sells. Final holdings are marked to market, not liquidated.
    This is an offline educational simulation, not a brokerage execution model.
    """
    _validate_inputs(prices, short_window, long_window)
    _finite_number(starting_cash, "starting_cash")
    _finite_number(transaction_cost, "transaction_cost", allow_zero=True)
    cash = float(starting_cash)
    position = 0
    trades = 0

    for index in range(long_window, len(prices)):
        # The execution bar is deliberately excluded from the signal window.
        signal = _signal(prices[index - long_window:index], short_window, long_window)
        price = prices[index]
        if signal == "buy" and position == 0 and cash >= price + transaction_cost:
            cash -= price + transaction_cost
            position = 1
            trades += 1
        elif signal == "sell" and position == 1:
            cash += price - transaction_cost
            position = 0
            trades += 1

    final_equity = cash + position * prices[-1]
    return BacktestResult(
        final_cash=round(cash, 2),
        final_position=position,
        final_equity=round(final_equity, 2),
        trades=trades,
        return_pct=round(((final_equity - starting_cash) / starting_cash) * 100, 2),
    )
