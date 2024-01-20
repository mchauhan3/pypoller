from util.decorators import non_null_args
from . import Notifier, Message
from .NotificationException import NotificationException


class TryNextOnFailNotifier(Notifier):
	@non_null_args
	def __init__(self, notifiers):
		super().__init__()
		self.notifiers = notifiers

	def notify_inner(self, msg: Message):
		for notifier in self.notifiers:
			try:
				notifier.notify(msg)
				return
			except NotificationException:
				pass

		raise NotificationException("No successful notifiers")
