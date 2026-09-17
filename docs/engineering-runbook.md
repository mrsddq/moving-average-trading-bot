# Offline simulator verification

```bash
python -m pip install -r requirements.txt
make test
python main.py
```

Regression tests enforce next-bar execution, finite positive prices, integer
window sizes, finite cash/fees, affordability, and exact two-sided fee accounting.
They also cover short series, where no trades execute but all inputs still need
validation. The final open position is marked to market without an invented exit.

No test contacts a broker, downloads market data, or sends orders. Main prints
synthetic example results. Real strategy research would require sourced data,
market calendars, spread/slippage assumptions, and an out-of-sample protocol.
