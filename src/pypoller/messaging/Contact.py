from dataclasses import dataclass


@dataclass
class Contact:
    """
    Data class representing a contact.

    Attributes:
        name (str): The name of the contact.
        phone_number (str): The phone number of the contact.
        email (str): The email address of the contact.
        notify_error (bool, optional): Flag indicating whether to notify the contact about errors. Defaults to False.
    """

    name: str
    phone_number: str
    email: str
    notify_error: bool = False
