from typing import List, Iterable

from util.decorators import non_null_args
from . import Message, Contact, CombinedMessage


class Notifier:

	@non_null_args
	def __init__(self, contacts: List[Contact] = []):
		self.contacts = contacts

	def notify(self, msg: Message):
		if isinstance(msg, CombinedMessage):
			list(map(self.notify, msg.underlying_messages))
		else:
			self.notify_inner(msg)

	def notify_inner(self, msg: Message):
		raise NotImplementedError()

	@non_null_args
	def __add__(self, other):
		from . import CombinedNotifier
		return CombinedNotifier([self, other])

	@non_null_args
	def add_contact(self, contact: Contact):
		self.contacts.append(contact)

	@non_null_args
	def add_contacts(self, contacts: Iterable[Contact]):
		self.contacts.extend(contacts)
