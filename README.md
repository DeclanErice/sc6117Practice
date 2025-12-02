# sc6117Practice
This is the repository to track the team project for sc6117 course.

## Progress - 2025-11-26

- Set up the local Python virtual environment and verified required packages (`requests`, `ccxt`, `pandas`, `pyarrow`).
- Implemented `newsAcquision.py` to fetch crypto news from the Cryptopanic API.
	- Added a preprocessing function to normalize raw news into a clean JSON schema (id, title, body, url, source, symbols, timestamps, etc.).
	- Exported standardized news records to an NDJSON file with a date-stamped filename, e.g. `crypto_news_ETH_YYYY-MM-DD.ndjson`.
- Implemented `klineAcquision.py` to fetch OHLCV (K-line) data via `ccxt` from Binance.
	- Normalized OHLCV into a Pandas DataFrame with UTC timestamps, symbol, timeframe, and helper columns (`datetime`, `date`).
	- Saved standardized K-line data to a date-stamped parquet file, e.g. `kline_ETHUSDT_1h_YYYY-MM-DD.parquet`.
- Cleanly initialized this directory as an isolated Git repository (only tracking project files, not the whole home directory) and pushed the initial commit to GitHub at `DeclanErice/sc6117Practice`.

## Progress - 2025-12-02

- Built a sentiment-driven backtest notebook `Main.ipynb` that acts as both executable pipeline and project report.
- Defined core backtest dataclasses (`BacktestConfig`, `TradeRecord`, `BacktestResult`, `BacktestOutput`, etc.) to standardize inputs/outputs across modules.
- Implemented the full backtest pipeline in the notebook:
	- Load standardized K-line parquet data and simulate a random sentiment time series aligned to price.
	- Normalize and align sentiment data to price using `merge_asof` (backward direction to avoid look-ahead bias).
	- Generate simple long/short/flat signals from sentiment thresholds and run a bar-by-bar backtest engine.
	- Compute common performance metrics (total/annualized return, volatility, Sharpe ratio, max drawdown, win rate, trade count).
	- Implement a buy-and-hold benchmark and a top-level `run_backtest_with_benchmark` wrapper that returns a unified `BacktestOutput`.
	- Add a helper to transform backtest outputs into front-end friendly `dataPoints` (time, realPrice, predictionPrice, percentDifference).
- Documented the notebook with a clear 0–11 step structure so it can be handed in as a course assignment.
