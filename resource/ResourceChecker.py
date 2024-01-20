from resource.request import Request


class ResourceChecker:
	def check_resource(self, request: Request):
		pass

	def __add__(self, other):
		from . import MultipleResourceChecker
		return MultipleResourceChecker([self, other])
