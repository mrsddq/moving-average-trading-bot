from dataclasses import dataclass


@dataclass(frozen=True)
class BacktestResult:
    """Summary metrics for a simple long-only moving-average backtest."""

    final_cash: float
    final_position: int
    final_equity: float
    trades: int
    return_pct: float


def moving_average_signal(prices, short_window=3, long_window=5):
    """Return buy, sell, or hold from simple moving average crossover logic."""
    if short_window <= 0 or long_window <= 0:
        raise ValueError("window sizes must be positive")
    if short_window >= long_window:
        raise ValueError("short_window must be smaller than long_window")
    if not prices:
        raise ValueError("prices must not be empty")
    if any(price <= 0 for price in prices):
        raise ValueError("prices must all be positive")
    if len(prices) < long_window:
        return "hold"

    short_average = sum(prices[-short_window:]) / short_window
    long_average = sum(prices[-long_window:]) / long_window

    if short_average > long_average:
        return "buy"
    if short_average < long_average:
        return "sell"
    return "hold"


def backtest_moving_average(
    prices,
    short_window=3,
    long_window=5,
    starting_cash=10000.0,
    transaction_cost=0.0,
):
    """Run a deterministic long-only backtest with one-share position sizing."""
    if starting_cash <= 0:
        raise ValueError("starting_cash must be positive")
    if transaction_cost < 0:
        raise ValueError("transaction_cost must be non-negative")
    if not prices:
        raise ValueError("prices must not be empty")
    if any(price <= 0 for price in prices):
        raise ValueError("prices must all be positive")

    cash = float(starting_cash)
    position = 0
    trades = 0

    for index in range(long_window, len(prices) + 1):
        visible_prices = prices[:index]
        price = visible_prices[-1]
        signal = moving_average_signal(visible_prices, short_window, long_window)

        if signal == "buy" and position == 0 and cash >= price + transaction_cost:
            cash -= price + transaction_cost
            position = 1
            trades += 1
        elif signal == "sell" and position == 1:
            cash += price - transaction_cost
            position = 0
            trades += 1

    final_equity = cash + (position * prices[-1])
    return BacktestResult(
        final_cash=round(cash, 2),
        final_position=position,
        final_equity=round(final_equity, 2),
        trades=trades,
        return_pct=round(((final_equity - starting_cash) / starting_cash) * 100, 2),
    )
