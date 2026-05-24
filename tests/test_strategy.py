from src.tradingbot.strategy import moving_average_signal


def test_buy_signal_when_short_average_is_above_long_average():
    assert moving_average_signal([1, 2, 3, 4, 5], short_window=2, long_window=4) == "buy"


def test_hold_signal_when_history_is_too_short():
    assert moving_average_signal([1, 2], short_window=2, long_window=4) == "hold"
