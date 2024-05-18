class DigitalClock:
    """A class to set a digital clock
    """
    def __init__(self, h: int = 0, m: int = 0, s: int = 0) -> None:
        """Default constructor that asserts input values are in the correct range.
        """
        assert h >= 0 and h < 24
        self.__h = h
        assert m >= 0 and m < 60
        self.__m = m
        assert s >= 0 and s < 60
        self.__s = s

    def increment(self) -> None:
        """ Updates one second the current time
        """
        self.__h = self.__h + 1 if self.__m == 59 and self.__s == 59 else self.__h
        self.__h = 0 if self.__h == 24 else self.__h
        self.__m = self.__m + 1 if self.__s == 59 else self.__m
        self.__m = 0 if self.__m == 60 else self.__m
        self.__s = self.__s + 1 if self.__s < 59 else 0

    def get_time(self) -> tuple[int, int, int]:
        """Returns the current time

        Returns:
            tuple[int, int, int]: hours, minutes, seconds
        """
        return (self.__h, self.__m, self.__s)
    
    def clear_time(self) -> None:
        """Resets time
        """
        self.__h, self.__m, self.__s = 0, 0, 0

    def set_time(self, h: int, m: int, s: int) -> None:
        """Sets time

        Args:
            h (int): hours in 24 H format
            m (int): minutes
            s (int): seconds
        """
        assert h >= 0 and h < 24 and m >= 0 and m < 60 and s >= 0 and s < 60
        self.__h, self.__m, self.__s = h, m, s