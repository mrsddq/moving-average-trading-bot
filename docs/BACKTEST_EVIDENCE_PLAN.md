# Backtest Evidence Plan

This project should stay framed as engineering practice unless it receives a reproducible market-data and risk-analysis layer.

## Evidence To Add

- Deterministic sample CSV under `data/sample_prices.csv`.
- Backtest output under `outputs/backtest_summary.json`.
- Equity curve under `assets/equity_curve.png`.
- Trade log with timestamps, signal, price, position, and cash.
- Risk notes covering slippage, fees, survivorship bias, and overfitting.

## Demo Command

```bash
pytest
python main.py
```

## Claim Boundary

Do not present this as financial advice, a profitable strategy, or a broker-connected trading system.
