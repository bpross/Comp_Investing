import sys
from collections import namedtuple, OrderedDict
import datetime as dt
import csv
from getopt import getopt
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from math import sqrt

def main(argv):
    """
    Runs the logic of the market sim
    Collects the command line arguments
    """
    trade_file = ''
    output_file = ''
    port_cash = 0

    try:
        opts, args = getopt(argv, "hc:t:o:",["cash=","trades=","outfile="])
    except:
        print 'marketsim.py -c <cash> -t <trades.csv> -o <outfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'marketsim.py -c <cash> -t <trades.csv> -o <outfile>'
            sys.exit(2)
        elif opt in ("-c", "--cash"):
            port_cash = arg
        elif opt in ("-t", "--trades"):
            trade_file = arg
        elif opt in ("-o", "--outfile"):
            output_file = arg

    start_date, end_date, symbols, trades = read_trades(trade_file)

    print "Trading Starts on: " + str(start_date)
    print "Trading Ends on: "  + str(end_date)
    print "Trading these symbols: " + str(symbols)

    close_prices, trading_days = get_close_data(start_date, end_date, symbols)

    trades_copy = list(trades)
    index = []
    position = {'cash': port_cash}
    for symbol in symbols:
        position[symbol] = 0
    daily_values = []
    for i in range (0,len(trading_days)):
        for j in range(0,len(trades)):
            if trades[j].date == trading_days[i]:
                index.append(j)
                if trades[j].command == "Buy":
                    print "buy"
                    price = close_prices[i][symbols.index(trades[j].symbol)]
                    value = float(price) * float(trades[j].amount)
                    position[trades[j].symbol] = float(trades[j].amount)
                    position['cash'] = float(position['cash']) - float(value)
                elif trades[j].command == "Sell":
                    print "sell"
                    price = close_prices[i][symbols.index(trades[j].symbol)]
                    if trades[j].amount > position[trades[j].symbol]:
                        print "Not enough shares!"

        for k in range(0,len(index)):
            trades.pop(index[k])
        index = []

def read_trades(trade_file):
    """
    Reads in the trade file and returns relevant info
    returns: start_date, end_date, symbols, trades
    @start_date: date object for start of trading
    @end_date: date object for end of trading
    @symbols: list of symbols being traded
    @trades: list of trades being executed
    """
    trades = []

    # Read in the csv file and create tuples for each trade
    # this way we can access each trade like: trade[0].symbol, etc
    with open(trade_file, 'rb') as f:
        reader = csv.reader(f)
        Trade = namedtuple('Trade',['date','symbol','command','amount'])
        for row in reader:
            date = dt.datetime(int(row[0]),int(row[1]),int(row[2]),16,0,0)
            trades.append(Trade(date,row[3],row[4],row[5]))

    # Now we want to sort the trades by date, just in case they are not in
    # correct order
    trades.sort(key=lambda tup: tup.date)
    
    # Grab the start and end date of the trades
    start_date = trades[0].date
    end_date = trades[-1].date

    # Grab all of the symbols from the orders
    symbols = [x.symbol for x in trades]
    symbols = OrderedDict.fromkeys(symbols).keys()

    return start_date, end_date, symbols, trades

def get_close_data(start_date, end_date, symbols):
    """
    Returns the adjusted close prices of the symbols passed in
    @param start_date: start date to grab data from
    @param end_date: end date to grab data from
    @param time_of_day: nubmer of hours in the day
    @param symbols: symbols to get data for
    @return: list of adjust close prices, indexed by symbol and list of
    dates for trading
    """
    
    # Grab the number of trading days
    dt_timeofday = dt.timedelta(hours=16)
    ldt_timestamps = du.getNYSEdays(start_date, end_date, dt_timeofday)

    # Grab data from QSTK data. Yahoo as the data source
    c_dataobj = da.DataAccess('Yahoo')
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    ldf_data = c_dataobj.get_data(ldt_timestamps, symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))

    close_price = d_data['close'].values

    return close_price, ldt_timestamps

if __name__ =="__main__":
    main(sys.argv[1:])
