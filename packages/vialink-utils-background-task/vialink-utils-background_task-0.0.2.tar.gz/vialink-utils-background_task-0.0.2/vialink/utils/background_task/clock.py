import datetime

from .abstract import ClockAbstract


class Clock(ClockAbstract):
    def get_timestamp(self) -> float:
        return datetime.datetime.now().timestamp()
