from . import AvailabilityChecker
from util.decorators import non_null_args


class AnyAvailabilityChecker(AvailabilityChecker):

	@non_null_args
	def __init__(self, ls_checkers):
		self.ls_checkers = ls_checkers

	@non_null_args
	def check_availability(self, date_range):
		return any([checker.check_availability(date_range) for checker in self.ls_checkers])
