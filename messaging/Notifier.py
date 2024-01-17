from . import Message
from . import Contact


class Notifier:

	def notify(self, msg: Message, receiver: Contact):
		raise Exception("Not implemented")
