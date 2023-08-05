import curses
import multiprocessing as mp
import os
from datetime import datetime as dt

from bcsim import Clock
from bcsim import FastClock


def clear():
    """Clear the screen

    This is an os-agnostic version, which will work with both Windows
    and Linux.
    """
    return os.system('clear' if os.name == 'posix' else 'cls')

# --------------------------------------------------------------------


def runClock(balls, q, fast=False):
    """Cycle an individual clock until it returns to its initial state.

    Arguments
    ---------
    balls : `int`
        The number of balls to be loaded into the reservoir at the
        start. For rolling ball clocks, the minimum number of balls
        permitted is 27.
    q : managed queue
        *q* is a [managed queue](https://docs.python.org/3/library/\
        multiprocessing.html#multiprocessing.Queue) from
        Python's [multiprocessing module](https://docs.python.org/3/\
        library/multiprocessing.html). As individual processes start
        cycling clocks, they will provide an updated status of the
        number of simulated days achieved on regular intervals. Those
        status updates are put into a managed queue, to be retrieved by
        the main simulation code and displayed on screen. The
        periodicity for reports is called `stride` and is set at 1,000
        days for a regular `library.clocks.Clock` and 10,000 days for a
        `library.clocks.FastClock.`
    fast : `bool`, optional
        If set to `False`, a regular `library.clocks.Clock` is created
        and cycled. If set to `True`, a `library.clocks.FastClock` is
        used.

    Returns
    -------
    result : (int, int)
        The result of a running clock is a tuple containing the number
        of balls in the clock, and the elapsed number of days it took to
        cycle back to its initial state.
    """
    pid = os.getpid()
    start = dt.now()
    if fast:
        c = FastClock(balls)
        stride = 10000
    else:
        c = Clock(balls)
        stride = 1000
    while True:
        if c.elapsedDays % stride == 0:
            q.put((pid, balls, int(c.elapsedDays), False))
        if fast:
            c.tick()
        else:
            for _ in range(720):
                c.tick()
        if c.inInitialState():
            q.put((pid, balls, int(c.elapsedDays), True))
            break
    stop = dt.now()
    return balls, c.elapsedDays, (stop-start)

# ---------------------------------------------------------------


def runSimulation(stdscr, args):

    stdscr.clear()
    curses.curs_set(0)

    # Baseline values
    counter = args.max - args.min + 1
    y0 = 3
    x0 = 5
    workers = mp.cpu_count()
    bannerlines = 2

    # Field widths: pw = pid width; sw = status width; bw = ball width, dw =
    # days width; tw = total width (including internal spaces and a single
    # trailing space)
    pw = 6
    sw = 10
    bw = 6
    dw = 19
    tw = pw + sw + bw + dw + 4

    # Grid positions for on-screen elements
    ban_y0 = y0
    ban_x0 = x0
    ban_w = 50
    hdr_y0 = y0 + bannerlines + 1
    hdr_x0 = x0 + 2
    box_y0 = hdr_y0 + 1
    box_x0 = x0
    box_h = workers + 2
    box_w = tw + 3

    # Banner lines printed before status box
    ban_win1 = curses.newwin(1, ban_w, ban_y0, ban_x0)
    ban_win2 = curses.newwin(1, ban_w, ban_y0+1, ban_x0)
    ban_1 = "Number of process workers: {0}"
    ban_2 = "Number of clocks in queue: {0}"
    ban_win1.addstr(0, 0, ban_1.format(workers))
    ban_win2.addstr(0, 0, ban_2.format(counter))
    ban_win1.refresh()
    ban_win2.refresh()

    # Header labels for status box
    h1 = 'pid'
    h2 = 'status'
    h3 = 'balls'
    h4 = 'simulated days'
    s = f"{h1:<{pw}} {h2:<{sw}} {h3:<{bw}} {h4:<{dw}}"
    hdr_win = curses.newwin(1, tw, hdr_y0, hdr_x0)
    hdr_win.addstr(0, 0, s)
    hdr_win.refresh()

    # Box
    box = curses.newwin(box_h, box_w, box_y0, box_x0)
    box.box()
    box.refresh()

    # Create a queue and build/fill a pool with jobs
    q = mp.Manager().Queue()
    results = []
    workers_D = {}
    poolData = [(i, q, args.fast) for i in range(args.min, args.max+1)]
    p = mp.Pool(workers)
    for data in poolData:
        results.append(p.apply_async(runClock, data))
    p.close()

    # Cycle through the queue, grabbing and posting the status of jobs
    row = 1
    while True:
        # This blocks until something is in the queue
        t = q.get()
        pid, balls, days, done = t[0], t[1], t[2], t[3]
        if pid not in workers_D:
            workers_D[pid] = curses.newwin(1, tw, box_y0+row, hdr_x0)
            row += 1
        if done:
            counter -= 1
            status = 'Done'
            s = f"{pid:<{pw}} {status:<{sw}} {0:<{bw},d} {0:->{dw},d}"
            ban_win2.erase()
            ban_win2.addstr(0, 0, ban_2.format(counter))
            ban_win2.refresh()
        else:
            status = 'Working'
            s = f"{pid:<{pw}} {status:<{sw}} {balls:<{bw},d} {days:->{dw},d}"
        workers_D[pid].erase()
        workers_D[pid].addstr(0, 0, s)
        workers_D[pid].refresh()
        if counter == 0:
            break

    p.join()
    for result in results:
        t = result.get()
        args.outfile.write(f'{str(t[0])},{str(t[1])},{str(t[2])}\n')

    curses.curs_set(1)
    return

# --------------------------------------------------------------------


if __name__ == '__main__':
    pass
