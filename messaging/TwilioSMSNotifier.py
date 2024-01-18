from twilio.rest import Client

from util.decorators import non_null_args
from . import Notifier, Contact, Message


class TwilioSMSNotifier(Notifier):
	@non_null_args
	def __init__(self, account_sid, auth_token, phone_number):
		self.client = Client(account_sid, auth_token)
		self.phone_number = phone_number

	@non_null_args
	def notify(self, msg: Message, receiver: Contact):
		if not receiver.phone_number:
			print("Receiver phone number not provided, skipping")
			return

		if msg.is_error and (not receiver.notify_error):
			print("Receiver not configured for errors, skipping")
			return

		self.client.messages.create(
			from_=self.phone_number,
			to=receiver.phone_number,
			body=msg.body
		)
