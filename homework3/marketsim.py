import sys
from getopt import getopt

def main(argv):
    """
    Runs the logic of the market sim
    Collects the command line arguments
    """
    trade_file = ''
    output_file = ''
    port_cash = 0
    print "Attempting to load args\n"
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

    print "Args loaded\nDumping args\n"
    print "Cash available in portfolio: " + str(port_cash) + "\n"
    print "Trade file: " + trade_file + "\n"
    print "Output file: " + output_file + "\n"

if __name__ =="__main__":
    main(sys.argv[1:])
