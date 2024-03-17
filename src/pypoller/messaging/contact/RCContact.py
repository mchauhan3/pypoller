from dataclasses import dataclass
from . import Contact


@dataclass
class RCContact(Contact):
    """
    Represents a contact for a rocket chat channel, extending the base Contact class.

    Attributes:
        channel (str): The rocket chat channel associated with the contact.
    """

    channel: str
