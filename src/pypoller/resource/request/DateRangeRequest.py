import datetime as dt
from dataclasses import dataclass

from . import Request


@dataclass
class DateRangeRequest(Request):
    """
    A request class representing a date range request.
    """

    start_date: dt.datetime
    end_date: dt.datetime
