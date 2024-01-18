class AvailabilityChecker:
	def check_availability(self, date_range):
		pass

	def __add__(self, other):
		from . import AnyAvailabilityChecker
		return AnyAvailabilityChecker([self, other])

	def __or__(self, other):
		from . import AnyAvailabilityChecker
		return AnyAvailabilityChecker([self, other])

	def __and__(self, other):
		from . import AllAvailabilityChecker
		return AllAvailabilityChecker([self, other])
