class Ball:
    """Abstract class representing a single ball in the clock.

    Balls in a rail are chained together as a linked list.

    Parameters
    ----------
    number : `int`
        A ball object's number. This will remain constant throughout
        the running of the clock.
    next : `Ball`
        A pointer to the next ball in the list (rail). Initialized to
        `None`.
    """

    def __init__(self, number):
        self.number = number
        self.next = None


class Rail:
    """Abstract class representing a rail in a rolling ball clock.

    The class initializer takes a *maxsize* (int) which represents the
    maximum number of balls the rail can hold: 4 for the 1-min rail, 11
    for the 5-min rail, and 11 for the hour rail. A *maxsize* of 0 (no
    limit) is used when creating the reservoir.

    As ball objects are added to the rail, they're stitched together
    into a linked list.

    Arguments
    ---------
    maxsize : int
        The maximum number of balls the rail can hold.

    Attributes
    ----------
    head : `Ball`
        A pointer to the first `Ball` object in a `Rail`.
    tail : `Ball`
        A pointer to the last `Ball` object in a `Rail`.
    size : `int`
        The current size (number of balls) in a `Rail`.
    """

    def __init__(self, maxsize):
        self.maxsize = maxsize
        self.reset()
        return

    def reset(self):
        """Reset a rail.

        This sets the *head* and *tail* pointers in a rail to `None`,
        and sets its *size* to 0.
        """
        self.head = None
        self.tail = None
        self.size = 0
        return

    # ------------------------------------------------

    def append(self, ball, reservoir=None):
        """Appends a new ball to the end of a rail.

        Arguments
        ---------
        ball : `Ball`
            A ball to be appended to the end of a rail.
        reservoir : `Rail`, optional
            This is a pointer to the clock's reservoir. If the rail
            would become over-full by adding *ball*, the rail has to
            be dumped back to the *reservoir* in reverse order.

        Returns
        -------
        ball : `Ball`
            If the ball being added over-fills the rail, it has to be
            returned for further processing. Otherwise, it's added to
            the rail and `None` is returned.
        """
        ball.next = None
        if self.size == self.maxsize and reservoir is not None:
            self.dump(reservoir)
            return ball
        else:
            if self.head is None:
                self.head = ball
                self.tail = ball
            else:
                self.tail.next = ball
                self.tail = ball
            self.size += 1
        return

    # ------------------------------------------------

    def draw(self):
        """Draw a new ball from the reservoir.
        """
        if self.head is not None:
            ball = self.head
            self.head = self.head.next
            self.size -= 1
            return ball
        return

    # ------------------------------------------------

    def __dump(self, ball, reservoir):
        if ball is None:
            return
        self.__dump(ball.next, reservoir)
        reservoir.append(ball, None)
        return

    def dump(self, reservoir):
        """Dump a full rail back to the reservoir.

        The dumping must be done in reverse order to the way the balls
        were added. This is achieved by using a helper method
        (`__dump()`) recursively on the rail. Once the rail is dumped,
        it is reset to bring it back to an initial (empty) state.

        Arguments
        ---------
        reservoir : `Rail`
            The clock's reservoir.
        """
        self.__dump(self.head, reservoir)
        self.reset()
        return

    # ------------------------------------------------

    def __eq__(self, rail):
        """Test if one rail is equal to another.

        In order to determine when a clock has returned to its initial
        state, the reservoir must be compared to a benchmark
        representing the balls in their original order. Both the
        reservoir and the benchmark are `Rail` objects.

        Arguments
        ---------
        rail : `Rail`
            The rail on the right side of `==` being compared to `self`.

        Returns
        -------
        result : `bool`
            `True` if two `Rail` objects are equal, `False` otherwise.
        """
        if self.size != rail.size:
            return False
        elif self.head is None:
            return True
        else:
            c1 = self.head
            c2 = rail.head
            while True:
                if c1 is None and c2 is None:
                    return True
                if c1.number != c2.number:
                    return False
                c1 = c1.next
                c2 = c2.next

    # ------------------------------------------------

    def __str__(self):
        """Render a rail as a string.

        The `Rail` object -- a linked list of `Ball` objects -- is
        traversed and stitched in to a string with a single space
        between ball numbers.

        Returns
        -------
        rail : `str`
            A `Rail` object rendered as a string.
        """
        L = []
        current = self.head
        while current is not None:
            L.append(str(current.number))
            current = current.next
        return ' '.join(L)

    # ------------------------------------------------


if __name__ == '__main__':
    pass
