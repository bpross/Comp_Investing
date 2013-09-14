import datetime as dt
from simulate import simulate

symbols = ['GOOG','AAPL','GLD','XOM']
allocations = [0.0,0.4,0.4,0.2]
dt_start = dt.datetime(2011, 1, 1)
dt_end = dt.datetime(2011, 12, 31)

vol, daily_ret, sharpe, cum_ret = simulate(dt_start, dt_end, symbols, allocations)

print "Portfolio Symbols: " + str(symbols)
print "Portfolio Allocations: " + str(allocations)
print "Volatility (stdev of daily returns): " + str(vol)
print "Average Daily Return: " + str(daily_ret)
print "Sharpe Ratio: " + str(sharpe)
print "Cumulative Return " + str(cum_ret)

symbols = ['AXP','HPQ','IBM','HNZ']
allocations = [0.0,0.0,0.0,1.0]
dt_start = dt.datetime(2010, 1, 1)
dt_end = dt.datetime(2010, 12, 31)

vol, daily_ret, sharpe, cum_ret = simulate(dt_start, dt_end, symbols, allocations)

print "Portfolio Symbols: " + str(symbols)
print "Portfolio Allocations: " + str(allocations)
print "Volatility (stdev of daily returns): " + str(vol)
print "Average Daily Return: " + str(daily_ret)
print "Sharpe Ratio: " + str(sharpe)
print "Cumulative Return " + str(cum_ret)
