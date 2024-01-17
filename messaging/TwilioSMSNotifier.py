from twilio.rest import Client
from . import Notifier


class TwilioSMSNotifier(Notifier):
	def __init__(self, account_sid, auth_token, phone_number):

		self.client = Client(account_sid, auth_token)
		self.phone_number = phone_number

	def notify(self, msg, receiver):
		if not receiver:
			print("Receiver not provided, skipping")
			return

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
