from messaging import Notifier, Message, Contact


class ConsoleNotifier(Notifier):
	def notify(self, msg: Message, receiver: Contact):
		print(msg.body)
