#!/usr/bin/env python3

import argparse
import curses
import sys
from datetime import datetime as dt
from pathlib import Path

from bcsim import clear
from bcsim import runSimulation

# --------------------------------------------------------------------


def numballs_type(n):
    msg = "min must be >= 27; max must be <= 1000"
    try:
        v = int(n)
        if v < 27 or v > 1000:
            raise argparse.ArgumentTypeError(msg)
    except ValueError:
        raise argparse.ArgumentTypeError("min and max must be integers")
    return v

# --------------------------------------------------------------------


def main():

    # Build a python argument parser

    msg = """Rolling ball clock simulator."""

    epi = "Version 1.0.5"

    parser = argparse.ArgumentParser(description=msg, epilog=epi)

    msg = """minimum number of balls in the clock - the smallest
    permissible minimum value is 27."""
    parser.add_argument('min',
                        help=msg,
                        type=numballs_type)

    msg = """maximum number of balls in the clock - the largest
    permissible maximum value is 1000."""
    parser.add_argument('max',
                        help=msg,
                        type=numballs_type)

    msg = """name of output file to hold simulation results. Results are
    saved in csv format (balls, number of simulated days, time to
    complete the simulated run)."""
    parser.add_argument('outfile',
                        type=argparse.FileType('w'),
                        help=msg)

    msg = """run the simulation in \'fast\' mode. In this mode, each
    incremental movement of the clock is 12-hrs. The default behavior is
    for each incremental movement of the clock to be 1-min."""
    parser.add_argument('-f', '--fast',
                        help=msg,
                        action='store_true')

    args = parser.parse_args()

    if args.max < args.min:
        parser.print_usage()
        print('error: max must be >= min')
        sys.exit(1)

    # Start the clock
    start = dt.now()

    # Launch simulation; stop the clock; close open file
    curses.wrapper(runSimulation, args)
    stop = dt.now()
    args.outfile.close()

    # Show post-simulation results
    clear()
    clocks = args.max - args.min + 1
    print('Simulation complete\n')
    print(f'        Total elapsed time: {str(stop-start)}')
    print(f'Number of clocks simulated: {clocks}')
    print(f'   Minimum number of balls: {args.min}')
    print(f'   Maximum number of balls: {args.max}')
    print(f'          Results saved to: {Path(args.outfile.name)}\n')

    return


# --------------------------------------------------------------------

if __name__ == '__main__':
    main()
