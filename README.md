# Tradingbot

A Python practice project for moving-average signals, deterministic long-only backtesting, and risk-aware engineering habits.

## Structure

```text
src/tradingbot/
  strategy.py
main.py
tests/
  test_strategy.py
requirements.txt
```

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pytest
python main.py
```

## Implemented Scope

- moving-average buy/sell/hold signal
- defensive validation for invalid inputs
- deterministic long-only backtest
- final cash, position, equity, trade count, and return percentage metrics
- command-line entry point
- pytest coverage for signal and backtest behavior
- dependency file

## Quality Signals

- GitHub Actions pytest workflow
- risk and roadmap notes in [docs/risk-and-roadmap.md](docs/risk-and-roadmap.md)
- deterministic strategy and backtest functions with tests

## Current Limitation

This is an engineering practice project, not a real trading system. It does not connect to a broker, use live market data, model slippage, or provide financial advice.
