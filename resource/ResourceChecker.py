from resource.request import Request
from resource.response import Response


class ResourceChecker:
    def check_resource(self, request: Request) -> Response:
        pass

    def __add__(self, other):
        from . import MultipleResourceChecker

        return MultipleResourceChecker([self, other])
