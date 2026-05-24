# Tradingbot

A Python starter project for experimenting with rule-based trading signals.

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

## Status

Baseline structure is complete:

- strategy module
- command-line entry point
- tests
- dependency file
- README

## Quality Signals

- GitHub Actions pytest workflow
- risk and roadmap notes in [docs/risk-and-roadmap.md](docs/risk-and-roadmap.md)
- deterministic strategy function with tests

This is an engineering practice project, not a real trading system.
