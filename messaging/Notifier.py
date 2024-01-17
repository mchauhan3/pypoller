from . import Message, Contact


class Notifier:

	def notify(self, msg: Message, receiver: Contact):
		raise Exception("Not implemented")
