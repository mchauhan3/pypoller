from dataclasses import dataclass
from . import Contact


@dataclass
class EmailContact(Contact):
    """
    Represents an email contact, extending the base Contact class.

    Attributes:
        email (str): The email address associated with the contact.
    """

    email: str
