# Moving Average Trading Bot

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
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest
python main.py
```

## Implemented Scope

- moving-average buy/sell/hold signal
- defensive validation for invalid inputs
- deterministic long-only backtest with next-bar execution and per-fill fees
- final cash, position, equity, trade count, and return percentage metrics
- command-line entry point
- pytest coverage for signal and backtest behavior
- dependency file

## Quality Signals

- GitHub Actions pytest workflow
- risk and roadmap notes in [docs/risk-and-roadmap.md](docs/risk-and-roadmap.md)
- backtest evidence plan in [docs/BACKTEST_EVIDENCE_PLAN.md](docs/BACKTEST_EVIDENCE_PLAN.md)
- deterministic strategy and backtest functions with tests

## Current Limitation

This is an engineering practice project, not a real trading system. It does not connect to a broker, use live market data, model slippage, or provide financial advice.

## Execution contract

Signals use the short/long moving-average **relationship**, not only the instant
of a crossover. A signal from observations through bar `t` can fill only at bar
`t+1`; it cannot fill at the same observed price that generated it. The last bar
therefore cannot generate an executable trade. No future observations enter the
signal window.

The simulator holds at most one share, checks cash including the entry fee, and
charges a flat fee on each fill. An open position is valued at the final observed
price; no forced sale or hypothetical exit fee is included. A trade count counts
fills, so a completed round trip counts as two. Calculations retain float
precision internally and round only the reported results.

Tests check exact cash accounting, next-bar timing, short-history validation,
NaN/Infinity rejection, affordability, and mark-to-market behavior. `python -m
pytest` runs offline. The code uses only the standard library at runtime.

This model omits bid/ask spreads, slippage, partial fills, corporate actions,
market impact, and borrowing. Example returns are synthetic test output, not
performance evidence. Runtime is O(n × long_window); this favors an inspectable
reference implementation over a vectorized research engine.
