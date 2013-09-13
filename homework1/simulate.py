import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from math import sqrt

ls_symbols = ["AAPL", "GLD", "GOOG", "XOM"]
alloc = [0.4,0.4,0.0,0.2]
dt_start = dt.datetime(2011, 1, 1)
dt_end = dt.datetime(2011, 12, 31)
dt_timeofday = dt.timedelta(hours=16)
ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)

c_dataobj = da.DataAccess('Yahoo')
ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
ldf_data = c_dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
d_data = dict(zip(ls_keys, ldf_data))

na_price = d_data['close'].values
na_normalized_price = na_price / na_price[0, :]

alloc_normal_p = na_normalized_price * alloc

na_portrets = np.sum(alloc_normal_p, axis=1)

cum_return = na_portrets[-1]-na_portrets[0]/na_portrets[0] + 1
print cum_return

tsu.returnize0(na_portrets)
avg_daily_ret = np.average(na_portrets)
print avg_daily_ret
std_daily_ret = np.std(na_portrets)
print std_daily_ret

sharpe_ratio = (avg_daily_ret/std_daily_ret)*sqrt(252.0)
print sharpe_ratio
