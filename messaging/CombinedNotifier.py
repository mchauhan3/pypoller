from . import Message, Contact, Notifier
from util.decorators import non_null_args


class CombinedNotifier(Notifier):
	@non_null_args
	def __init__(self, l_notifiers):
		self.l_notifier = l_notifiers

	def notify(self, msg: Message, receiver: Contact):
		list(map(lambda x: x.notify(msg, receiver), self.l_notifier))
