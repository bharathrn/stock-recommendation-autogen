import numpy as np
import pandas as pd

def rsi(series: pd.Series, window: int = 14) -> pd.Series:
    delta = series.diff()
    up = delta.clip(lower=0)
    down = -1 * delta.clip(upper=0)
    roll_up = up.ewm(alpha=1/window, adjust=False).mean()
    roll_down = down.ewm(alpha=1/window, adjust=False).mean()
    rs = roll_up / (roll_down + 1e-9)
    return 100 - (100 / (1 + rs))

def sma(series: pd.Series, window: int = 20) -> pd.Series:
    return series.rolling(window).mean()

def annualized_volatility(series: pd.Series, trading_days: int = 252) -> float:
    returns = series.pct_change().dropna()
    return float(returns.std() * np.sqrt(trading_days))

def drawdown_stats(series: pd.Series) -> dict:
    cummax = series.cummax()
    dd = (series / cummax) - 1.0
    max_dd = dd.min()
    try:
        end = dd.idxmin()
        start = (series.loc[:end]).idxmax()
    except Exception:
        end = None
        start = None
    return {"max_drawdown": float(max_dd), "start": str(start), "end": str(end)}
