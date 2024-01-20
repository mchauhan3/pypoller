from functools import reduce

from resource import ResourceChecker
from util.decorators import non_null_args
from .request import Request
from .response import Response


class MultipleResourceChecker(ResourceChecker):

	@non_null_args
	def __init__(self, checkers):
		self.checkers = checkers

	@non_null_args
	def check_resource(self, request: Request) -> Response:
		return reduce(lambda x, y: x + y, [checker.check_resource(request) for checker in self.checkers])

	def __add__(self, other):
		if isinstance(other, MultipleResourceChecker):
			return MultipleResourceChecker(self.checkers + other.checkers)

		return MultipleResourceChecker(self.checkers + [other])
