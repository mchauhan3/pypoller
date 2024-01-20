from . import Message, Contact, Notifier
from util.decorators import non_null_args


class CombinedNotifier(Notifier):
	@non_null_args
	def __init__(self, notifiers):
		super().__init__()
		self.notifiers = notifiers

	def notify_inner(self, msg: Message):
		list(map(lambda x: x.notify(msg), self.notifiers))