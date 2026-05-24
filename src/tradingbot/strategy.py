def moving_average_signal(prices, short_window=3, long_window=5):
    """Return buy, sell, or hold from simple moving average crossover logic."""
    if short_window <= 0 or long_window <= 0:
        raise ValueError("window sizes must be positive")
    if short_window >= long_window:
        raise ValueError("short_window must be smaller than long_window")
    if len(prices) < long_window:
        return "hold"

    short_average = sum(prices[-short_window:]) / short_window
    long_average = sum(prices[-long_window:]) / long_window

    if short_average > long_average:
        return "buy"
    if short_average < long_average:
        return "sell"
    return "hold"
