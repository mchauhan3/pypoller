import random
import time
from pypoller.resource import ResourceChecker
from pypoller.messaging import Notifier, ConsoleNotifier
from pypoller.util.decorators import non_null_args


class Poller:
    """
    Class for polling a resource checker and notifying a notifier periodically.

    Attributes:
        checker (ResourceChecker): The resource checker to be polled.
        notifier (Notifier, optional): The notifier to be used for notifications. Defaults to ConsoleNotifier().
    """

    def __init__(
        self, checker: ResourceChecker, notifier: Notifier = ConsoleNotifier()
    ):
        """
        Initialize the Poller with a resource checker and a notifier.

        Args:
            checker (ResourceChecker): The resource checker to be polled.
            notifier (Notifier, optional): The notifier to be used for notifications. Defaults to ConsoleNotifier().
        """
        self.notifier = notifier
        self.checker = checker

    @non_null_args
    def poll(self, request, frequency=30, jitter=5):
        """
        Poll the resource checker periodically and notify the notifier.

        Args:
            request: The request to be used for polling.
            frequency (int, optional): The polling frequency in seconds. Defaults to 30.
            jitter (int, optional): The jitter in polling frequency in seconds. Defaults to 5.
        """
        number_of_times_polled = 1
        while True:
            msg = self.checker.check_resource(request).to_message()
            self.notifier.notify(msg)
            print("Executed {} times".format(number_of_times_polled))
            number_of_times_polled += 1
            offset = random.randint(-jitter, jitter)
            time.sleep(frequency + offset)
