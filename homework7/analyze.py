import csv
import sys
import datetime as dt
from getopt import getopt
import numpy as np
from math import sqrt
from marketsim import get_close_data
import QSTK.qstkutil.tsutil as tsu

def main(argv):
    """
    Runs the logic of analyzing a portfolio
    Collects the command line arguments
    """
    value_file = ''
    benchmark = ''

    try:
        opts, args = getopt(argv, "hf:b:",["file=","benchmark="])
    except:
        print 'analyze.py -f <value_file> -b <benchmark>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'analyze.py -f <value_file> -b <benchmark>'
            sys.exit(2)
        elif opt in ("-f", "--file"):
            value_file = arg
        elif opt in ("-b", "--benchmark"):
            benchmark = [arg]

    print "Benchmark is: " + str(benchmark)
    print "Value file is: " + str(value_file)
    port_values, dates = read_values(value_file)

    close_prices, trading_days = get_close_data(dates[0], dates[-1], benchmark)
    
    std_daily_ret_port, avg_daily_ret_port, sharpe_ratio_port, cum_return_port = comp_metrics(port_values)
    std_daily_ret, avg_daily_ret, sharpe_ratio, cum_return = comp_metrics(close_prices)

    
    print "The final value of the portfolio using the sample file is -- " + str(dates[-1]) + "," + str(port_values[-1])
    print "\n"
    print "Details of the Performance of the portfolio : "
    print "\n"
    print "Date Range : " + str(dates[0]) + " to " + str(dates[-1])
    print "\n"
    print "Sharpe Ratio of Fund : " + str(sharpe_ratio_port)
    print "Sharpe Ratio of " + str(benchmark[0]) + " : " + str(sharpe_ratio)
    print "\n"
    print "Total Return of Fund : " + str(cum_return_port)
    print "Total Return of " + str(benchmark[0]) + " : " + str(cum_return)
    print "\n"
    print "Standard Deviation of Fund : " + str(std_daily_ret_port)
    print "Standard Deviation of " + str(benchmark[0]) + " : " + str(std_daily_ret)
    print "\n"
    print "Average Daily Return of Fund : " + str(avg_daily_ret_port)
    print "Average Daily Return of " + str(benchmark[0]) + " : " + str(avg_daily_ret)

def read_values(value_file):
    """
    Reads in the value file and returns a list of values and a list of dates
    @param value_file: the file to get the values from
    """
    values = []
    dates = []

    with open(value_file, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            value = float(row[-1])
            values.append(value)
            date = dt.datetime(int(row[0]),int(row[1]),int(row[2]),16,0,0)
            dates.append(date)
    values = np.array(values)
    return values, dates

def comp_metrics(daily_rets):
    """
    Compute the following metrics for the portfolio:
        avg_daily_return
        std_dev_daily_ret
        sharpe_ratio
        cum_return
    """
    _daily_rets = list(daily_rets)
    
    _daily_rets = _daily_rets / _daily_rets[0]
    #Calculate the cumulative return for the portfolio
    cum_return = _daily_rets[-1]-_daily_rets[0]/_daily_rets[0] + 1
    tsu.returnize0(_daily_rets)
    # Calculate average daily return
    avg_daily_ret = np.average(_daily_rets)
    # Calculate std dev of daily return (volatility) 
    std_daily_ret = np.std(_daily_rets)

    # Calculate sharpe ratio
    sharpe_ratio = (avg_daily_ret/std_daily_ret)*sqrt(252.0)

    return std_daily_ret, avg_daily_ret, sharpe_ratio, cum_return


if __name__ =="__main__":
    main(sys.argv[1:])
