from .request import Request
from .response import Response


class ResourceChecker:
    """
    Base class for checking the availability of a resource.
    """

    def check_resource(self, request: Request) -> Response:
        """
        Check the availability of a resource based on the given request.

        Args:
            request (Request): The request object representing the resource to be checked.

        Returns:
            Response: The response object containing the result of the resource check.
        """
        pass

    def __add__(self, other):
        """
        Combine two resource checkers into a single MultipleResourceChecker.

        This method is used to create a new checker that combines the functionality of the current checker
        and another checker.

        Args:
            other (ResourceChecker): The other resource checker to be combined with.

        Returns:
            MultipleResourceChecker: Combined resource checker object.
        """
        from . import MultipleResourceChecker

        return MultipleResourceChecker([self, other])
