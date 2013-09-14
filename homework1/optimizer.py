from simulate import simulate
import datetime as dt
import itertools
import numpy as np

symbols = ['BRCM','AMD','ADI']
dt_start = dt.datetime(2011, 1, 1)
dt_end = dt.datetime(2011, 12, 31)

steps = np.linspace(0., 1., 11)

high_sharpe = 0
high_vol = 0
high_daily_ret = 0
high_cum_ret = 0
alloc_used = [0]*3
for allocations in itertools.product(steps, repeat=3):
    alloc_sum = allocations[0] + allocations[1] + allocations[2]
    if alloc_sum == 1.0:
        vol, daily_ret, sharpe, cum_ret = simulate(dt_start, dt_end, symbols, allocations)
        if sharpe > high_sharpe:
            high_vol = vol
            high_daily_ret = daily_ret
            high_sharpe = sharpe
            high_cum_ret = cum_ret
            alloc_used = allocations

print "Portfolio Symbols: " + str(symbols)
print "Portfolio Allocations: " + str(alloc_used)
print "Volatility (stdev of daily returns): " + str(high_vol)
print "Average Daily Return: " + str(high_daily_ret)
print "Sharpe Ratio: " + str(high_sharpe)
print "Cumulative Return " + str(high_cum_ret)
