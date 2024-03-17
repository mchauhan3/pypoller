from typing import List, Iterable
from . import Notifier, Message
from pypoller.util.decorators import non_null_args
from .NotificationException import NotificationException
from .contact import Contact
from rocketchat_API.rocketchat import RocketChat
from .contact import RCContact


class RocketChatNotifier(Notifier):
    """
    A notifier for sending messages to Rocket.Chat channels.

    Attributes:
        rc_client (RocketChat): rocketchat_API client to communicate to rocket chat
    """

    def __init__(
        self, user: str, password: str, server_url: str, contacts: List[Contact] = []
    ):
        """
        Initializes a RocketChatNotifier instance.

        Args:
            user (str): The username for authenticating with the Rocket.Chat server.
            password (str): The password for authenticating with the Rocket.Chat server.
            server_url (str): The URL of the Rocket.Chat server.
            contacts (List[Contact], optional): List of Rocket.Chat contacts to notify. Defaults to [].
        """
        super().__init__(contacts)
        self.rc_client = RocketChat(user=user, password=password, server_url=server_url)
        self.contacts = list(
            filter(lambda contact: isinstance(contact, RCContact), self.contacts)
        )

    @non_null_args
    def add_contact(self, contact: Contact):
        """
        Adds a Rocket.Chat contact to the list of contacts.

        Args:
            contact (Contact): The Rocket.Chat contact to add.
        """
        if isinstance(contact, RCContact):
            self.contacts.append(contact)

    @non_null_args
    def add_contacts(self, contacts: Iterable[Contact]):
        """
        Adds multiple Rocket.Chat contacts to the list of contacts.

        Args:
            contacts (Iterable[Contact]): The Rocket.Chat contacts to add.
        """
        self.contacts.extend(
            filter(lambda contact: isinstance(contact, RCContact), contacts)
        )

    @non_null_args
    def notify_inner(self, msg: Message):
        """
        Notifies Rocket.Chat contacts with the given message.

        Args:
            msg (Message): The message to send.
        """
        if len(msg.body) == 0:
            return
        
        for contact in self.contacts:
            if msg.is_error and not contact.notify_error:
                continue
            try:
                self.rc_client.chat_post_message(msg.body, channel=contact.channel)
            except Exception as e:
                raise NotificationException("Exception when posting to RocketChat", e)
