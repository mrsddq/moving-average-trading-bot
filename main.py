from src.tradingbot.strategy import backtest_moving_average, moving_average_signal


def main():
    prices = [100, 101, 102, 103, 104, 105, 103, 101, 99, 102, 106]
    signal = moving_average_signal(prices, short_window=2, long_window=4)
    result = backtest_moving_average(prices, short_window=2, long_window=4)
    print(f"Signal: {signal}")
    print(f"Final equity: ${result.final_equity}")
    print(f"Return: {result.return_pct}%")
    print(f"Trades: {result.trades}")


if __name__ == "__main__":
    main()
