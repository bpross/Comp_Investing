import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from math import sqrt

def simulate(start_date, end_date, symbols, allocation):
    """
    This function simulates a portfolio for the given symbols with the given allocation
    It does NOT rebalance daily
    @param start_date: the date to start the sym
    @param end_date: the date to end the sym
    @param symbols: list of symbols in the portfolio
    @param allocation: list of allocation percentages for symbols
    @return: vol, avg_daily_ret, sharpe, cum_return
    """
    
    # Set variables
    ls_symbols = symbols
    alloc = allocation
    dt_start = start_date
    dt_end = end_date
    dt_timeofday = dt.timedelta(hours=16)
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)

    # Grab data from QSTK data. Yahoo as the data source
    c_dataobj = da.DataAccess('Yahoo')
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    ldf_data = c_dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))

    # Grab the prices and normalize them
    na_price = d_data['close'].values
    na_normalized_price = na_price / na_price[0, :]

    # Adjust the prices based on allocation percentages
    alloc_normal_p = na_normalized_price * alloc

    # Calculate the daily returns for the portfolio
    na_portrets = np.sum(alloc_normal_p, axis=1)

    #Calculate the cumulative return for the portfolio
    cum_return = na_portrets[-1]-na_portrets[0]/na_portrets[0] + 1

    # Normalize returns
    tsu.returnize0(na_portrets)

    # Calculate average daily return
    avg_daily_ret = np.average(na_portrets)
    # Calculate std dev of daily return (volatility) 
    std_daily_ret = np.std(na_portrets)

    # Calculate sharpe ratio
    sharpe_ratio = (avg_daily_ret/std_daily_ret)*sqrt(252.0)

    return std_daily_ret, avg_daily_ret, sharpe_ratio, cum_return
