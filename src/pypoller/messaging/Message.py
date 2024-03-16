from dataclasses import dataclass


@dataclass
class Message:
    """
    Data class representing a message.

    Attributes:
        body (str): The body of the message.
        is_error (bool): Flag indicating whether the message represents an error. Defaults to False.
    """

    body: str = ""
    is_error: bool = False

    def __add__(self, other):
        """
        Override the addition operator to combine messages.

        Args:
            other: Another Message instance to be combined.

        Returns:
            CombinedMessage: A new CombinedMessage instance containing the combined messages.
        """
        from .CombinedMessage import CombinedMessage

        return CombinedMessage(underlying_messages=[self, other])
