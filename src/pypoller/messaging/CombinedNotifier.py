from typing import Iterable
from . import Message, Notifier
from pypoller.util.decorators import non_null_args
from .contact import Contact


class CombinedNotifier(Notifier):
    """
    Notifier class for combining multiple notifiers into one.

    """

    @non_null_args
    def __init__(self, notifiers):
        """
        Initialize the CombinedNotifier with a list of notifiers.

        Args:
            notifiers: List of Notifier instances to be combined.
        """
        super().__init__()
        self.notifiers = notifiers

    def notify_inner(self, msg: Message):
        """
        Notify the contacts with the given message using all combined notifiers.

        Args:
            msg (Message): The message to be sent.
        """
        list(map(lambda x: x.notify(msg), self.notifiers))

    def add_contact(self, contact: Contact):
        """
        Add a single contact to all combined notifiers.

        Args:
            contact (Contact): The contact to be added.
        """
        for notifier in self.notifiers:
            notifier.add_contact(contact)

    def add_contacts(self, contacts: Iterable[Contact]):
        """
        Add multiple contacts to all combined notifiers.

        Args:
            contacts (Iterable[Contact]): The contacts to be added.
        """
        for notifier in self.notifiers:
            notifier.add_contacts(contacts)
