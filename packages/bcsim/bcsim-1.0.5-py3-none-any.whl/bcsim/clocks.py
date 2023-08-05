from bcsim import Ball
from bcsim import Rail


class Clock:
    """Abstract class to represent a rolling ball clock.

    The class initializer takes a *size* (int) which represents the
    number of balls in the clock reservoir.

    Arguments
    ---------
    size : `int`
        The number of simulated balls in the clock reservoir.

    Attributes
    ----------
    reservoir : `library.rail.Rail`
        The reservoir of simulated balls that feeds the clock mechanism.
    benchmark : `library.rail.Rail`
        A copy of the initial clock state that can be compared to the
        current clock state to determine when all the balls in the
        reservoir are in their original (starting) positions.
    elapsedDays : float
        A count of the elapsed number of days of clock time. One
        complete 12-hr sequence (from 1:00 to 1:00) represents 0.5
        days.
    rail_1 : `library.rail.Rail`
        The simulated 1-minute rail in the clock.
    rail_5 : `library.rail.Rail`
        The simulated 5-minute rail in the clock.
    rail_hr : `library.rail.Rail`
        The simulated hour rail in the clock.
    """

    def __init__(self, size):
        self.reservoir = Rail(0)
        self.benchmark = Rail(0)
        for i in range(size):
            self.reservoir.append(Ball(i))
        # The benchmark needs to have separate ball objects from the reservoir
        for i in range(size):
            self.benchmark.append(Ball(i))
        self.elapsedDays = 0.0
        self.rail_1 = Rail(4)
        self.rail_5 = Rail(11)
        self.rail_hr = Rail(11)
        return

    # ------------------------------------------------------------------

    def tick(self):
        """Simulate the movement of the clock.

        This method simulates the clock advancing one minute. When a
        trigger ball initiates the transition from 12:59 to 1:00, the
        return to the reservoir is modeled in the following order: 1-min
        rail; trigger ball; 1-hr rail; 5-min rail.
        """
        ball = self.reservoir.draw()
        carry_5 = None
        carry_1 = self.rail_1.append(ball, self.reservoir)

        if carry_1 is not None:
            if (self.rail_5.size == self.rail_5.maxsize and
                    self.rail_hr.size == self.rail_hr.maxsize):
                self.reservoir.append(carry_1)
                self.rail_hr.dump(self.reservoir)
                self.rail_5.dump(self.reservoir)
                self.elapsedDays += 0.5
            else:
                carry_5 = self.rail_5.append(carry_1, self.reservoir)

        if carry_5 is not None:
            self.rail_hr.append(carry_5, self.reservoir)

        return

    # ------------------------------------------------------------------

    def inInitialState(self):
        """Determine if the clock is in its initial state.

        Returns
        -------
        result : `bool`
            `True` if the clock is in its initial state, `False`
            otherwise.
        """
        return (self.reservoir == self.benchmark)

    # ------------------------------------------------------------------

    def __str__(self):
        """Render the current clock state as a string.

        It includes all the rails: reservoir, 1-min, 5-min, hr, and
        shows the position of the balls in each one. This was mostly
        used for debugging during development.

        Returns
        -------
        clockstate : `str`
            Returns the state of the clock, rendered as a string.
        """
        L = []
        L.append('\nReservoir:\n' + str(self.reservoir))
        L.append('1-minute rail:\n' + str(self.rail_1))
        L.append('5-minute rail:\n' + str(self.rail_5))
        L.append('hour-rail:\n' + str(self.rail_hr))
        L.append(f'Elapsed Days: {self.elapsedDays}')

        divider = '\n------------------------------\n'

        return divider.join(L) + '\n'

# ====================================================================


class FastClock(Clock):
    """A fast-cycling subclass of `Clock`.

    The `FastClock` class takes advantage of a repeating pattern. At
    each 12-hr interval, all the balls in the clock are in the
    reservoir. If you start with a fresh clock and brute-force cycle it
    for 720 minutes (12-hrs), then you get what I call a permutation
    vector in the reservoir. You can now treat each ball number in the
    reservoir as an index (position) for the movement of balls every
    12-hrs.

    For example, if cycling a fresh clock 12-hrs results in ball #10
    ending up in position #2, that means every 12-hrs the ball in
    position #10 will migrate to position #2. Using two Python lists, we
    can now cycle the clock for 12-hrs each `tick()`, rather then
    1-minute for each `tick()`. The speed gains in clock cycling are
    dramatic.

    Arguments
    ---------
    size : `int`
        The number of simulated balls in the clock reservoir.

    Attributes
    ----------
    B : [`int`]
        On initialization, the benchmark reservoir is copied into a
        Python list as *B*.
    P : [`int`]
        After a fresh clock is cycled for 720 minutes, the reservoir
        (now the permutation vector) is copied into a Python list as
        *P*.
    R : [`int`]
        A copy of the initial state of the clock, with the balls in
        `0 -> n-1` order.
    T : [`int`]
        *T* is a list used to cycle a `FastClock` 1-day at a time. The
        reservoir is copied into *T* based on the permutation vector;
        *T* and *R* are then swapped; and the process is repeated.
    """

    def __init__(self, size):

        super().__init__(size)
        self.R = [int(i) for i in str(self.reservoir).split()]
        self.B = [int(i) for i in str(self.benchmark).split()]
        self.T = [0] * size
        # Brute force cycle clock for 720 minutes (12-hrs) to generate
        # permutation vector and reset the day counter when complete.
        for _ in range(720):
            super().tick()
        self.P = [int(i) for i in str(self.reservoir).split()]
        # After all the FastClock attributes are set, reset the clock using the
        # superclass initializer.
        super().__init__(size)
        return

    def tick(self):
        """Cycle the clock through 12-hours.

        This version of `tick()` takes advantage of the permutation
        vector to rapidly cycle the clock through a 12-hr period.
        """
        for i in range(len(self.P)):
            self.T[i] = self.R[self.P[i]]
        self.R, self.T = self.T, self.R
        self.elapsedDays += 0.5
        return

    def inInitialState(self):
        """Determine if the `FastClock` is in its initial state.

        If the `FastClock` version of the reservoir (*R*) is equal to
        the `FastClock` version of the benchmark (*B*), then all the
        balls in the clock are in their original positions.

        Returns
        -------
        result : `bool`
            `True` if the clock is in its initial state, `False`
            otherwise.
        """
        return self.R == self.B

# --------------------------------------------------------------------


if __name__ == '__main__':
    pass
