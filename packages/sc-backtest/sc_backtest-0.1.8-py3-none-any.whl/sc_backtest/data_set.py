import pandas as pd
import os
import datetime


def index_futures_close(frequency=1):
    dirname, _ = os.path.split(os.path.abspath(__file__))
    path = os.path.join(dirname, 'dataset', '_close.csv')
    output = pd.read_csv(path, index_col=0, header=0)
    output.index = pd.to_datetime(output.index)
    if 240 % frequency != 0:
        print(F'240%frequency should be 0')
        return

    if frequency <= 240:
        output = output[frequency-1::frequency]
    elif frequency == 240:
        output = output[239::240]
        output.index = output.index.to_series().apply(lambda x: datetime.datetime(x.year, x.month, x.day))

    return output


def index_futures_adj(frequency=1):
    dirname, _ = os.path.split(os.path.abspath(__file__))
    path = os.path.join(dirname, 'dataset', '_adj_close.csv')
    output = pd.read_csv(path, index_col=0, header=0)
    output.index = pd.to_datetime(output.index)
    if 240 % frequency != 0:
        print(F'240%frequency should be 0')
        return

    if frequency <= 240:
        output = output[frequency-1::frequency]
    elif frequency == 240:
        output = output[239::240]
        output.index = output.index.to_series().apply(lambda x: datetime.datetime(x.year, x.month, x.day))

    return output


def index_futures_volume(frequency=1):
    dirname, _ = os.path.split(os.path.abspath(__file__))
    path = os.path.join(dirname, 'dataset', '_volume.csv')
    output = pd.read_csv(path, index_col=0, header=0)
    output.index = pd.to_datetime(output.index)
    if 240 % frequency != 0:
        print(F'240%frequency should be 0')
        return

    if frequency <= 240:
        output = output[frequency-1::frequency]
    elif frequency == 240:
        output = output[239::240]
        output.index = output.index.to_series().apply(lambda x: datetime.datetime(x.year, x.month, x.day))

    return output
