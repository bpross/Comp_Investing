'''
(c) 2011, 2012 Georgia Tech Research Corporation
This source code is released under the New BSD license.  Please see
http://wiki.quantsoftware.org/index.php?title=QSTK_License
for license details.

Created on January, 23, 2013

@author: Sourabh Bajaj
@contact: sourabhbajaj@gatech.edu
@summary: Event Profiler Tutorial

MODIFIED by: Benjamin Ross
Date: 09/18/2013
'''


import pandas as pd
import numpy as np
import math
import copy
import QSTK.qstkutil.qsdateutil as du
import datetime as dt
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkstudy.EventProfiler as ep
import re
from collections import namedtuple
import csv

"""
Accepts a list of symbols along with start and end date
Returns the Event Matrix which is a pandas Datamatrix
Event matrix has the following structure :
    |IBM |GOOG|XOM |MSFT| GS | JP |
(d1)|nan |nan | 1  |nan |nan | 1  |
(d2)|nan | 1  |nan |nan |nan |nan |
(d3)| 1  |nan | 1  |nan | 1  |nan |
(d4)|nan |  1 |nan | 1  |nan |nan |
...................................
...................................
Also, d1 = start date
nan = no information about any event.
1 = status bit(positively confirms the event occurence)
"""

Trade = namedtuple('Trade',['year','month','day','symbol','command','amount'])

def find_events(ls_symbols, d_data):
    ''' Finding the event dataframe '''
    df_close = d_data['actual_close']
    ts_market = df_close['SPY']
    trades = []

    # Creating an empty dataframe
    df_events = copy.deepcopy(df_close)
    df_events = df_events * np.NAN

    # Time stamps for the event range
    ldt_timestamps = df_close.index
    for s_sym in ls_symbols:
        for i in range(1, len(ldt_timestamps)):
            # Calculating the returns for this timestamp
            f_symprice_today = df_close[s_sym].ix[ldt_timestamps[i]]
            f_symprice_yest = df_close[s_sym].ix[ldt_timestamps[i - 1]]
            f_marketprice_today = ts_market.ix[ldt_timestamps[i]]
            f_marketprice_yest = ts_market.ix[ldt_timestamps[i - 1]]
            f_symreturn_today = (f_symprice_today / f_symprice_yest) - 1
            f_marketreturn_today = (f_marketprice_today / f_marketprice_yest) - 1

            # Event is found if the symbol is down more then 3% while the
            # market is up more then 2%
            if f_symprice_yest >= 5.0 and f_symprice_today < 5.0:
                buy_date = return_dt(str(ldt_timestamps[i]))
                sell_date = return_dt(str(ldt_timestamps[i+4]))
                buy_trade = Trade(buy_date.group(1), buy_date.group(2), buy_date.group(3), s_sym, "Buy", 100)
                sell_trade = Trade(sell_date.group(1), sell_date.group(2), sell_date.group(3), s_sym, "Sell", 100)
                trades.append(buy_trade)
                trades.append(sell_trade)

    return trades


def return_dt(date):
    """
    Takes a pandas timestamp object and returns a datetime object
    """
    regex = re.compile("(\d{4})-(\d{2})-(\d{2})")
    r = regex.search(date)
    return r

def trade_to_string(trades):
    """
    Takes a list of Trades and returns a list of strings
    """
    trade_str = []
    for trade in trades:
        t_str = [trade.year,trade.month,trade.day,trade.symbol, trade.command, trade.amount]
        trade_str.append(t_str)
    return trade_str

def trades_to_csv(trades):
    """
    Takes a list of trade strings and outputs to csv file
    """
    ofile = open('trades.csv',"wb")
    writer = csv.writer(ofile,skipinitialspace=True, quoting=csv.QUOTE_NONE)
    writer.writerows(trades)
    ofile.close()

if __name__ == '__main__':
    dt_start = dt.datetime(2008, 1, 1)
    dt_end = dt.datetime(2009, 12, 31)
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))

    dataobj = da.DataAccess('Yahoo')
    ls_symbols = dataobj.get_symbols_from_list('sp5002012')
    ls_symbols.append('SPY')

    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))

    for s_key in ls_keys:
        d_data[s_key] = d_data[s_key].fillna(method='ffill')
        d_data[s_key] = d_data[s_key].fillna(method='bfill')
        d_data[s_key] = d_data[s_key].fillna(1.0)

    trades = find_events(ls_symbols, d_data)
    tr_str = trade_to_string(trades)
    trades_to_csv(tr_str)

    #ep.eventprofiler(df_events, d_data, i_lookback=20, i_lookforward=20,
    #            s_filename='sp5002012_study_price6.pdf', b_market_neutral=True, b_errorbars=True,
    #            s_market_sym='SPY')
