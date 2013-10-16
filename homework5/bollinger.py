import pandas as pd
import sys
import numpy as np
import math
import copy
import QSTK.qstkutil.qsdateutil as du
import datetime as dt
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkstudy.EventProfiler as ep
from getopt import getopt

def main(argv):
    """
    Creates bollinger bands for the given symbol and dates
    will create a chart
    will conver to -1 to 1 range
    """
   
    dt_start = dt.datetime(2010, 1, 1)
    dt_end = dt.datetime(2010, 12, 31)
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))
    dataobj = da.DataAccess('Yahoo')
    ls_symbols = ['AAPL', 'GOOG', 'IBM', 'MSFT'] 

    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))
    
    for s_key in ls_keys:
        d_data[s_key] = d_data[s_key].fillna(method='ffill')
        d_data[s_key] = d_data[s_key].fillna(method='bfill')
        d_data[s_key] = d_data[s_key].fillna(1.0)


    df_close = d_data['close']
    ldt_timestamps = df_close.index

    lookback = 20

    bol_vals = get_bollinger_values(ls_symbols, d_data, lookback)
    print bol_vals

    #close_appl = df_close['MSFT']
    #roll_mean = pd.stats.moments.rolling_mean(close_appl,20)
    #roll_std = pd.stats.moments.rolling_std(close_appl,20)
    #for i in range(1, len(ldt_timestamps)):
    #    bol_val = (df_close['MSFT'].ix[ldt_timestamps[i]] - roll_mean[i])/roll_std[i]
    #    print str(ldt_timestamps[i]) + " " + str(bol_val)

def get_bollinger_values(symbols, d_data, lookback):
    """
    Computes the bollinger values of the symbols for each day of trading
    @param symbols: list of symbols
    @param d_data: dataframe to use for data
    @param lookback: number of days to lookback
    """
    roll_means = {}
    roll_stds = {}
    df_close = d_data['close']
    bollinger_vals = {}

    for sym in symbols:
        close = df_close[sym]
        roll_mean = pd.stats.moments.rolling_mean(close,lookback)
        roll_std = pd.stats.moments.rolling_std(close,lookback)
        roll_means[sym] = roll_mean
        roll_stds[sym] = roll_std
        bollinger_vals[sym] = []

    ldt_timestamps = df_close.index
    for i in range(1, len(ldt_timestamps)):
        for sym in symbols:
            sym_price_today = df_close[sym].ix[ldt_timestamps[i]]
            bol_val = (sym_price_today - roll_means[sym][i])/roll_stds[sym][i]
            bollinger_vals[sym].append(bol_val)

    return bollinger_vals


if __name__ =="__main__":
    main(sys.argv[1:])
