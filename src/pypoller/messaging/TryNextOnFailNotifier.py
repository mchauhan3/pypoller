from pypoller.util.decorators import non_null_args
from . import Notifier, Message
from .NotificationException import NotificationException


class TryNextOnFailNotifier(Notifier):
    """
    Notifier class that tries each notifier in sequence until one succeeds.

    If a notifier fails with a NotificationException, it moves to the next notifier in the list.
    """

    @non_null_args
    def __init__(self, notifiers):
        """
        Initialize the TryNextOnFailNotifier with a list of notifiers.

        Args:
            notifiers: List of Notifier instances to be tried in sequence.
        """
        super().__init__()
        self.notifiers = notifiers

    def notify_inner(self, msg: Message):
        """
        Notify the contacts with the given message, trying each notifier in sequence until one succeeds.

        Args:
            msg (Message): The message to be sent.

        Raises:
            NotificationException: If no successful notifiers are found.
        """
        for notifier in self.notifiers:
            try:
                notifier.notify(msg)
                return
            except NotificationException as e:
                print(e)
                pass

        raise NotificationException("No successful notifiers")
