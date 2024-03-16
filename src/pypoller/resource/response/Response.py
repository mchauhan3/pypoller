from dataclasses import dataclass
from pypoller.messaging import Message


@dataclass(kw_only=True)
class Response:
    """
    Base class for representing a response.
    """

    error: Exception = None

    def to_message(self) -> Message:
        """
        Convert the response to a message format.

        Returns:
            Message: The message containing the response body.
        """
        raise NotImplementedError()

    def __add__(self, other):
        """
        Override the addition operator to combine responses.

        Args:
            other: Another Response instance to be combined.

        Returns:
            CombinedResponse: A new CombinedResponse instance containing the combined responses.
        """
        from .CombinedResponse import CombinedResponse

        return CombinedResponse([self, other])
