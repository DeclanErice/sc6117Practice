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
