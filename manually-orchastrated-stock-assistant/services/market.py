import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
from tenacity import retry, stop_after_attempt, wait_fixed
from indicators import rsi, sma, annualized_volatility, drawdown_stats
from loguru import logger

@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
def fetch_history(ticker: str, days: int = 180) -> pd.DataFrame:
    logger.info(f"[Market] downloading {ticker} history for {days} days")
    end = datetime.utcnow().date()
    start = end - timedelta(days=days + 5)
    df = yf.download(ticker, start=start.isoformat(), end=end.isoformat(), progress=False)
    if df is None or df.empty:
        raise RuntimeError(f"No data for {ticker}")
    df = df.rename(columns=str.title)
    return df

def compute_features(df: pd.DataFrame) -> dict:
    close = df['Close']
    feat = {}
    feat['last_price'] = float(close.iloc[-1].item())
    feat['sma_20'] = float(sma(close, 20).iloc[-1].item())
    feat['sma_50'] = float(sma(close, 50).iloc[-1].item()) if len(close) >= 50 else None
    feat['rsi_14'] = float(rsi(close, 14).iloc[-1].item())
    feat['ann_vol'] = float(annualized_volatility(close))

    dd = drawdown_stats(close)
    feat.update(dd)
    for d in (5,20,60,120):
        if len(close) > d:
            feat[f'ret_{d}d'] = float((close.iloc[-1] / close.iloc[-d-1]) - 1.0)
    return feat
