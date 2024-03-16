from . import Notifier, Message


class ConsoleNotifier(Notifier):
    """
    Notifier class for printing messages to the console.

    """

    def notify_inner(self, msg: Message):
        """
        Print the message body to the console.

        Args:
            msg (Message): The message to be printed.
        """
        print(msg.body)
