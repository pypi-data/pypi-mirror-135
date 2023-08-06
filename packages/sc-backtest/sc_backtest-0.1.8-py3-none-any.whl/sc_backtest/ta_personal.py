import math
import pandas as pd
import numpy as np
import chinese_calendar as cc
import datetime


# z-score
def z_score(x, window=20):
    ss = pd.Series(x)
    return (ss - ss.rolling(window).mean()) / ss.rolling(window).std()


# Simple ma
def sma(x, window=10):
    return pd.Series(x).rolling(window).mean()


# Linear weighted ma
def wma(x, window=10):
    coef = 2.0 / (window * (window + 1.0))  # sum of weights in a fancy way n(n+1)/2
    weights = list(float(i) for i in range(1, window + 1))
    return pd.Series(x).rolling(window).apply(lambda x: np.sum(weights * x) * coef, raw=True)


# Exponential ma
def ema(x, window=10):
    return pd.Series(x).ewm(span=window, adjust=False).mean()


# N is replaced in the code by window
def mma(x, window):
    return x.rolling(window).median()


def gma(x, window):
    return x.rolling(window).apply(lambda u: (np.prod(u)) ** (1 / window))


def qma(x, window):
    return x.rolling(window).apply(lambda u: (np.sum(u ** 2) / window) ** 0.5)


def hama(x, window):
    return x.rolling(window).apply(lambda u: (window / np.sum(1 / u)))


def trima(serie, window):
    return sma(sma(serie, window), window)


def swma(serie, window):
    weights = np.arange(1, window + 1) * (np.pi / 6)
    tmp = pd.Series(weights).apply(lambda x: round(math.sin(x)))
    #     return serie.rolling(window).apply(lambda x: np.dot(x, weights) / weights.sum())
    return serie.rolling(window).apply(lambda x: np.dot(x, tmp) / tmp.sum())


def zlema(serie, window):
    lag = (window - 1) / 2
    p = serie + serie.diff(lag)
    return ema(p, window)


def hma(serie, window):
    half_window = int(window / 2)
    sqrt_window = int(math.sqrt(window))
    wma_f = wma(serie, window=half_window)
    wma_s = wma(serie, window=window)
    return wma(2 * wma_f - wma_s, window=sqrt_window)


def ehma(serie, window):
    half_window = int(window / 2)
    sqrt_window = int(math.sqrt(window))
    ema_f = ema(serie, window=half_window)
    ema_s = ema(serie, window=window)
    return ema(2 * ema_f - ema_s, window=sqrt_window)


# First implementation
def gd(serie, window):
    ema1 = ema(serie, window)
    ema2 = ema(ema1, window)
    v = 0.618
    return (1 + v) * ema1 - ema2 * v


def tima(serie, window):
    gd1 = gd(serie, window)
    gd2 = gd(gd1, window)
    gd3 = gd(gd2, window)
    return gd3


# another implementation
def tima_2(serie, window):
    ema1 = ema(serie, window)
    ema2 = ema(ema1, window)
    ema3 = ema(ema2, window)
    ema4 = ema(ema3, window)
    ema5 = ema(ema4, window)
    ema6 = ema(ema5, window)
    a = 0.618
    t3 = -(a ** 3) * ema6 + 3 * (a ** 2 + a ** 3) * ema5 + (-6 * (a ** 2) - 3 * a - 3 * (a ** 3)) * ema4 + (
            1 + 3 * a + a ** 3 + 3 * (a ** 2)) * ema3
    return t3


# The Kaufman Efficiency indicator
def er(serie, window):
    x = serie.diff(window).abs()
    y = serie.diff().abs().rolling(window).sum()
    return x / y


def kama(serie, window, fast_win = 2, slow_win = 30):
    er_ = er(serie, window)
    fast_alpha = 2 / (fast_win + 1)  # = 0,6667
    slow_alpha = 2 / (slow_win + 1)  # = 0,0645
    sc = pd.Series((er_ * (fast_alpha - slow_alpha) + slow_alpha) ** 2)  ## smoothing constant
    sma_ = sma(serie, window)  ## first KAMA is SMA
    kama_ = []
    for s, ma, price in zip(
            sc.iteritems(), sma_.shift().iteritems(), serie.iteritems()):
        try:
            kama_.append(kama_[-1] + s[1] * (price[1] - kama_[-1]))
        except (IndexError, TypeError):
            if pd.notnull(ma[1]):
                kama_.append(ma[1] + s[1] * (price[1] - ma[1]))
            else:
                kama_.append(None)
    return pd.Series(kama_, index=sma_.index)


def bma(serie, window):
    serie = serie.dropna()
    beta = 2.415 * (1 - np.cos((2 / window) * np.pi))
    alpha = -beta + math.sqrt(beta ** 2 + 2 * beta)
    c_0 = (alpha ** 2) / 4
    a1 = 2 * (1 - alpha)
    a2 = -(1 - alpha) ** 2

    bma_ = [serie[0], serie[1], serie[2]]
    for i in range(3, len(serie)):
        bma_.append((serie[i] + 2 * serie[i - 1] + serie[i - 2]) * c_0 + a1 * bma_[-1] + a2 * bma_[-2])

    return pd.Series(bma_, index=serie.index)


def vidya(serie, window):
    serie = serie.tail(3 * window)
    win_f = window
    win_s = 2 * win_f
    vidya_tmp = [serie.iloc[win_s]]
    for i in range(win_s + 1, len(serie)):
        s = 0.2
        if serie.iloc[i - win_s:i].std() == 0:
            return pd.Series(np.nan)
        k = serie.iloc[i - win_f:i].std() / serie.iloc[i - win_s:i].std()
        alpha = k * s
        vidya_tmp.append(alpha * serie.iloc[i] + (1 - alpha) * vidya_tmp[-1])
    return pd.Series(vidya_tmp, index=serie[win_s:].index)


def is_trading_day(timestamp):
    if isinstance(timestamp, datetime.datetime) or \
            isinstance(timestamp, datetime.date):
        return cc.is_workday(timestamp) and timestamp.weekday() <= 4
    else:
        print('input type should be datetime.datetime or datetime.date')
        return False


def not_trading_day(timestamp):
    if isinstance(timestamp, datetime.datetime) or \
            isinstance(timestamp, datetime.date):
        return not (cc.is_workday(timestamp) and timestamp.weekday() <= 4)
    else:
        print('input type should be datetime.datetime or datetime.date')
        return False


def next_trading_day(timestamp):
    if isinstance(timestamp, datetime.datetime) or \
            isinstance(timestamp, datetime.date):
        dt = timestamp
        while True:
            dt += datetime.timedelta(days=1)
            if is_trading_day(dt):
                break
        return dt
    else:
        print('input type should be datetime.datetime or datetime.date')
        return None


def get_settle_day(s):
    """
    :param s: a str: 'IF1601', 'IC1701'
    :return: datetime.datetime: settle day
    """
    def str_clip(s):
        for i in range(len(s)):
            if s[i].isdecimal():
                break
        return s[i:] if i >= 0 else ''

    sd = datetime.strptime(f'20{str_clip(s)}01', '%Y%m%d')
    wd = sd.weekday()
    if wd <= 4:
        settle_day = datetime(sd.year, sd.month, 5 - wd + 14)
    else:
        settle_day = datetime(sd.year, sd.month, 7 - wd + 19)

    if cc.is_holiday(settle_day):
        i = 3
        while True:
            temp = settle_day + datetime.timedelta(days=i)
            if cc.is_workday(temp):
                settle_day = temp
                break
            else:
                i += 1
    return settle_day


def get_rank_delta(factor):
    delta = pd.DataFrame(factor)
    delta = delta.rank(axis=1)
    delta = delta.sub(delta.mean(axis=1), axis=0)
    delta = delta.div(delta.abs().sum(axis=1), axis=0) * 100
    return delta
