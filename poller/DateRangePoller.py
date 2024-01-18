from messaging import Message
from poller import Poller


class DateRangePoller(Poller):
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
