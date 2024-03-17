from typing import List, Iterable
from pypoller.util.decorators import non_null_args
from . import Message, CombinedMessage
from .contact import Contact


class Notifier:
    """
    Base class for notifying contacts with messages.
    """

    def __init__(self, contacts: List[Contact] = []):
        """
        Initialize the Notifier with a list of contacts.

        Args:
            contacts (List[Contact], optional): List of contacts to be notified. Defaults to an empty list.
        """
        self.contacts = contacts

    def notify(self, msg: Message):
        """
        Notify the contacts with the given message.

        Args:
            msg (Message): The message to be sent.
        """
        if isinstance(msg, CombinedMessage):
            list(map(self.notify, msg.underlying_messages))
        else:
            self.notify_inner(msg)

    def notify_inner(self, msg: Message):
        """
        Abstract method to handle notification of a single message.

        Args:
            msg (Message): The message to be sent.
        """
        raise NotImplementedError()

    @non_null_args
    def __add__(self, other):
        """
        Override the addition operator to combine Notifiers.

        Args:
            other: Another Notifier instance to be combined.

        Returns:
            CombinedNotifier: A new CombinedNotifier instance containing the combined Notifiers.
        """
        from . import CombinedNotifier

        return CombinedNotifier([self, other])

    @non_null_args
    def add_contact(self, contact: Contact):
        """
        Add a single contact to the list of contacts.

        Args:
            contact (Contact): The contact to be added.
        """
        self.contacts.append(contact)

    @non_null_args
    def add_contacts(self, contacts: Iterable[Contact]):
        """
        Add multiple contacts to the list of contacts.

        Args:
            contacts (Iterable[Contact]): The contacts to be added.
        """
        self.contacts.extend(contacts)
