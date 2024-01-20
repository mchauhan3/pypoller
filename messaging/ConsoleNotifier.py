from messaging import Notifier, Message


class ConsoleNotifier(Notifier):
	def notify_inner(self, msg: Message):
		print(msg.body)
