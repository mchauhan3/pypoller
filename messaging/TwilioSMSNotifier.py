from typing import List

from twilio.rest import Client

from util.decorators import non_null_args
from . import Notifier, Contact, Message
from .NotificationException import NotificationException


class TwilioSMSNotifier(Notifier):
	@non_null_args
	def __init__(self, account_sid: str, auth_token: str, phone_number: str, contacts: List[Contact] = []):
		super().__init__(contacts)
		self.client = Client(account_sid, auth_token)
		self.phone_number = phone_number
		self.contacts = contacts

	@non_null_args
	def notify_inner(self, msg: Message):
		if len(msg.body) == 0:
			return

		for receiver in self.contacts:
			if not receiver.phone_number:
				print("Receiver phone number not provided, skipping")
				continue

			if msg.is_error and (not receiver.notify_error):
				print("Receiver not configured for errors, skipping")
				continue

			self.send_message(msg.body, receiver.phone_number)

	def send_message(self, message_body, phone_number):
		try:
			self.client.messages.create(
				from_=self.phone_number,
				to=phone_number,
				body=message_body
			)
		except Exception as e:
			raise NotificationException("Exception when calling Twilio", e)
