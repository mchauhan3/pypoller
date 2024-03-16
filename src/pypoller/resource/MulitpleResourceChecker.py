from functools import reduce

from . import ResourceChecker
from pypoller.util.decorators import non_null_args
from .request import Request
from .response import Response


class MultipleResourceChecker(ResourceChecker):
    """
    A resource checker that aggregates multiple resource checkers.
    """

    @non_null_args
    def __init__(self, checkers: list):
        """
        Initialize the MultipleResourceChecker.

        Args:
            checkers (list): List of ResourceChecker instances to be aggregated.
        """
        self.checkers = checkers

    @non_null_args
    def check_resource(self, request: Request) -> Response:
        """
        Check the resource using all aggregated resource checkers.

        Args:
            request (Request): The request to be checked.

        Returns:
            Response: The aggregated response from all resource checkers.
        """
        return reduce(
            lambda x, y: x + y,
            [checker.check_resource(request) for checker in self.checkers],
        )

    def __add__(self, other):
        """
        Override the addition operator to combine MultipleResourceCheckers.

        Args:
            other (MultipleResourceChecker or ResourceChecker): Another MultipleResourceChecker or ResourceChecker
                instance to be combined.

        Returns:
            MultipleResourceChecker: A new MultipleResourceChecker instance containing the combined checkers.
        """
        if isinstance(other, MultipleResourceChecker):
            return MultipleResourceChecker(self.checkers + other.checkers)

        return MultipleResourceChecker(self.checkers + [other])
