from dataclasses import dataclass


@dataclass(kw_only=True)
class Contact:
    """
    Data class representing a contact.

    Attributes:
        name (str): The name of the contact.
    """

    name: str
    notify_error: bool = False
