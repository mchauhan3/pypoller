import datetime as dt
from dataclasses import dataclass

from .Request import Request


@dataclass
class DateRangeRequest(Request):
	start_date: dt.datetime
	end_date: dt.datetime
