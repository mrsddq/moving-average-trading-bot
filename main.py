from src.tradingbot.strategy import moving_average_signal


def main():
    prices = [100, 101, 102, 103, 104, 105]
    signal = moving_average_signal(prices, short_window=2, long_window=4)
    print(f"Signal: {signal}")


if __name__ == "__main__":
    main()
