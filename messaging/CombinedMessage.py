from dataclasses import dataclass, field
from typing import List
from . import Message


@dataclass
class CombinedMessage(Message):
    """
    Message class representing a combination of multiple messages.
    """

    underlying_messages: List[Message] = field(default_factory=list)

    def __add__(self, other: Message):
        """
        Override the addition operator to combine CombinedMessages.

        Args:
            other: Another Message instance to be combined.

        Returns:
            CombinedMessage: A new CombinedMessage instance containing the combined messages.
        """
        if isinstance(other, CombinedMessage):
            return CombinedMessage(
                underlying_messages=self.underlying_messages + other.underlying_messages
            )

        return CombinedMessage(underlying_messages=self.underlying_messages + [other])
