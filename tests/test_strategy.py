import pytest

from src.tradingbot.strategy import backtest_moving_average, moving_average_signal


def test_buy_signal_when_short_average_is_above_long_average():
    assert moving_average_signal([1, 2, 3, 4, 5], short_window=2, long_window=4) == "buy"


def test_hold_signal_when_history_is_too_short():
    assert moving_average_signal([1, 2], short_window=2, long_window=4) == "hold"


def test_sell_signal_when_short_average_is_below_long_average():
    assert moving_average_signal([5, 4, 3, 2, 1], short_window=2, long_window=4) == "sell"


def test_backtest_returns_summary_metrics():
    result = backtest_moving_average([100, 101, 102, 103, 104, 99], short_window=2, long_window=4)

    assert result.trades >= 1
    assert result.final_equity > 0


def test_backtest_accounts_for_transaction_costs():
    prices = [100, 101, 102, 103, 104, 99]
    no_cost = backtest_moving_average(prices, short_window=2, long_window=4, transaction_cost=0)
    with_cost = backtest_moving_average(prices, short_window=2, long_window=4, transaction_cost=2)

    assert with_cost.final_equity < no_cost.final_equity


def test_flat_prices_do_not_trade():
    result = backtest_moving_average([100, 100, 100, 100, 100], short_window=2, long_window=4)

    assert result.trades == 0
    assert result.return_pct == 0


def test_signal_rejects_invalid_windows():
    with pytest.raises(ValueError):
        moving_average_signal([1, 2, 3], short_window=4, long_window=4)


def test_signal_rejects_non_positive_prices():
    with pytest.raises(ValueError, match="positive"):
        moving_average_signal([100, 0, 101], short_window=1, long_window=2)


@pytest.mark.parametrize("bad", [float("nan"), float("inf"), -float("inf"), True, "100"])
def test_non_finite_and_non_numeric_prices_rejected(bad):
    for operation in (moving_average_signal, backtest_moving_average):
        with pytest.raises(ValueError):
            operation([100, bad])


@pytest.mark.parametrize("kwargs", [
    {"short_window": 0}, {"short_window": True}, {"short_window": 1.5},
    {"long_window": 0}, {"short_window": 6, "long_window": 5},
    {"starting_cash": float("nan")}, {"starting_cash": float("inf")},
    {"transaction_cost": float("nan")}, {"transaction_cost": float("inf")},
])
def test_backtest_validates_even_when_history_is_short(kwargs):
    with pytest.raises(ValueError):
        backtest_moving_average([100], **kwargs)


def test_last_bar_signal_cannot_fill_at_the_price_that_created_it():
    result = backtest_moving_average([100, 101, 102, 103], short_window=2, long_window=4)
    assert result.trades == 0
    assert result.final_cash == 10000


def test_next_bar_execution_and_two_sided_fees_are_exact():
    # Signal [1, 2, 3] buys at 4; [3, 4, 3] sells at 2 on the next bar.
    result = backtest_moving_average(
        [1, 2, 3, 4, 3, 2, 1], short_window=1, long_window=3,
        starting_cash=100, transaction_cost=0.5,
    )
    assert result.trades == 2
    assert result.final_position == 0
    assert result.final_cash == 97
    assert result.final_equity == 97
    assert result.return_pct == -3


def test_open_position_is_marked_to_market_without_synthetic_exit_fee():
    result = backtest_moving_average(
        [1, 2, 3, 4, 5], short_window=1, long_window=3,
        starting_cash=10, transaction_cost=0.5,
    )
    assert result.trades == 1
    assert result.final_cash == 5.5
    assert result.final_position == 1
    assert result.final_equity == 10.5


def test_insufficient_cash_cannot_create_a_position():
    result = backtest_moving_average([1, 2, 3, 4], 1, 3, starting_cash=4, transaction_cost=1)
    assert result.trades == 0 and result.final_cash == 4
