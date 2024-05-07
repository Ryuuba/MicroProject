class DigitalClock:
    """A class to set a digital clock
    """
    def __init__(self, h: int = 0, m: int = 0, s: int = 0) -> None:
        """Default constructor that asserts input values are in the correct range.
        """
        assert h >= 0 and h < 24
        self._h = h
        assert m >= 0 and m < 60
        self._m = m
        assert s >= 0 and s < 60
        self._s = s

    def increment(self) -> None:
        """ Updates one second the current time
        """
        self._h = self._h + 1 if self._m == 59 and self._s == 59 else self._h
        self._h = 0 if self._h == 24 else self._h
        self._m = self._m + 1 if self._s == 59 else self._m
        self._m = 0 if self._m == 60 else self._m
        self._s = self._s + 1 if self._s < 59 else 0

    def get_time(self) -> tuple[int, int, int]:
        """Returns the current time

        Returns:
            tuple[int, int, int]: hours, minutes, seconds
        """
        return (self._h, self._m, self._s)

    