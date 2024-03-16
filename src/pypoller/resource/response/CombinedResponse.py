from dataclasses import dataclass
from functools import reduce
from typing import List

from pypoller.messaging import Message
from . import Response


@dataclass
class CombinedResponse(Response):
    """
    A response class representing a combination of multiple responses.
    """

    underlying_responses: List[Response]

    def to_message(self) -> Message:
        """
        Convert the combined response to a message format.

        Returns:
            Message: The message containing the combined response body.
        """
        return reduce(
            (lambda x, y: x + y),
            [resp.to_message() for resp in self.underlying_responses],
        )

    def __add__(self, other):
        """
        Override the addition operator to combine CombinedResponses.

        Args:
            other: Another CombinedResponse instance or Response instance to be combined.

        Returns:
            CombinedResponse: A new CombinedResponse instance containing the combined responses.
        """
        if isinstance(other, CombinedResponse):
            return CombinedResponse(
                self.underlying_responses + other.underlying_responses
            )

        return CombinedResponse(self.underlying_responses + [other])
