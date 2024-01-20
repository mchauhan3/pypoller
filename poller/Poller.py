import random
import time
from typing import List

from resource import ResourceChecker
from messaging import Notifier, ConsoleNotifier
from util.decorators import non_null_args


class Poller:
    def __init__(self, checker: ResourceChecker, notifier: Notifier = ConsoleNotifier()):
        self.notifier = notifier
        self.checker = checker

    @non_null_args
    def poll(self, request, frequency=30, jitter=5):

        number_of_times_polled = 1

        while True:
            msg = self.checker.check_resource(request).to_message()
            self.notifier.notify(msg)
            print("Executed {} times".format(number_of_times_polled))
            number_of_times_polled += 1
            offset = random.randint(-jitter, jitter)
            time.sleep(frequency + offset)

    def execute(self, execution_input):
        raise NotImplementedError()
