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

    def execute(self, list_of_date_ranges):
        msg = None

        try:
            available_dates = filter(self.availabilityChecker.check_availability, list_of_date_ranges)
            available_dates = [" to ".join(x) for x in available_dates]
            msg = Message(body="Found Available Dates: {}".format(", ".join(available_dates)))

        except Exception as e:
            print(e)
            msg = Message(body=str(e), is_error=True)

        list(map(lambda contact: self.notifier.notify(msg, contact), self.contacts))

    @non_null_args
    def poll(self, list_of_date_ranges, frequency=30, jitter=5):

        number_of_times_polled = 1

        while True:
            self.execute(list_of_date_ranges)
            print("Executed {} times".format(number_of_times_polled))
            number_of_times_polled += 1
            offset = random.randint(-jitter, jitter)
            time.sleep(frequency + offset)
