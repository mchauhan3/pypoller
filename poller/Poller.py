import random
import time

from checker import AvailabilityChecker
from messaging import Notifier, Contact, Message
from util.decorators import non_null_args


class Poller:
    def __init__(self, notifier: Notifier, availability_checker: AvailabilityChecker, contacts: [Contact]):
        self.notifier = notifier
        self.availabilityChecker = availability_checker
        self.contacts = contacts

    @non_null_args
    def poll(self, execution_input, frequency=30, jitter=5):

        number_of_times_polled = 1

        while True:
            msg = self.execute(execution_input)
            if msg:
                list(map(lambda x: self.notifier.notify(msg, x), self.contacts))

            print("Executed {} times".format(number_of_times_polled))
            number_of_times_polled += 1
            offset = random.randint(-jitter, jitter)
            time.sleep(frequency + offset)

    def execute(self, execution_input):
        raise NotImplementedError()
