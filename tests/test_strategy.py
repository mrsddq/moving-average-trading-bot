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


def test_signal_rejects_invalid_windows():
    with pytest.raises(ValueError):
        moving_average_signal([1, 2, 3], short_window=4, long_window=4)
