from dataclasses import dataclass
from . import Contact


@dataclass
class PhoneContact(Contact):
    """
    Represents a phone contact, extending the base Contact class.

    Attributes:
        phone_number (str): The phone number associated with the contact.
    """

    phone_number: str
