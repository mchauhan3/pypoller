from typing import Iterable

from . import Message, Contact, Notifier
from util.decorators import non_null_args


class CombinedNotifier(Notifier):
	@non_null_args
	def __init__(self, notifiers):
		super().__init__()
		self.notifiers = notifiers

	def notify_inner(self, msg: Message):
		list(map(lambda x: x.notify(msg), self.notifiers))

	def add_contact(self, contact: Contact):
		for notifier in self.notifiers:
			notifier.add_contact(contacts)

	def add_contacts(self, contacts: Iterable[Contact]):
		for notifier in self.notifiers:
			notifier.add_contacts(contacts)
