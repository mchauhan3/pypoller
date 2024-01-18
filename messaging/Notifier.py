from . import Message, Contact


class Notifier:

	def notify(self, msg: Message, receiver: Contact):
		raise Exception("Not implemented")

	def __add__(self, other):
		from . import CombinedNotifier
		return CombinedNotifier([self, other])
