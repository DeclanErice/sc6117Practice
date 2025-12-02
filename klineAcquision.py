import ccxt
import pandas as pd
from datetime import datetime, timezone


def get_raw_ohlcv(symbol='BTC/USDT', timeframe='1h', limit=1000):
    """
    从 Binance 获取原始 OHLCV 列表（ccxt 格式）。
    """
    exchange = ccxt.binance()
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    return ohlcv


def normalize_ohlcv(ohlcv, symbol='BTC/USDT', timeframe='1h'):
    """
    将原始 OHLCV 列表标准化为适合本项目使用的 DataFrame。
    """
    df = pd.DataFrame(
        ohlcv,
        columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']
    )

    # 1. 转换时间戳为 UTC 时间
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms', utc=True)

    # 2. 添加元数据字段
    df['symbol'] = symbol
    df['timeframe'] = timeframe
    df['datetime'] = df['timestamp'].dt.strftime('%Y-%m-%dT%H:%M:%S%z')
    df['date'] = df['timestamp'].dt.date.astype(str)

    # 3. 排序 & 去重
    df = df.sort_values('timestamp').drop_duplicates(subset=['timestamp', 'symbol'])
    df = df.reset_index(drop=True)

    # 4. 将 timestamp 设为索引（方便后续按时间切片）
    df = df.set_index('timestamp')

    return df


def get_price_data(symbol='BTC/USDT', timeframe='1h', limit=1000):
    """
    对外主函数：获取并标准化 K 线数据。
    """
    ohlcv = get_raw_ohlcv(symbol=symbol, timeframe=timeframe, limit=limit)
    df = normalize_ohlcv(ohlcv, symbol=symbol, timeframe=timeframe)

    print("\n=== 标准化后的第一行 K 线数据 ===")
    print(df.iloc[0])

    return df


if __name__ == "__main__":
    symbol = 'BTC/USDT'
    timeframe = '1m'  # 或 '5m'，根据你想要的颗粒度修改
    df = get_price_data(symbol=symbol, timeframe=timeframe, limit=2000)

    today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    out_path = f"kline_{symbol.replace('/', '')}_{timeframe}_{today_str}.parquet"
    df.to_parquet(out_path)
    print(f"\n标准化后的K线数据已保存到: {out_path}")