import os
from dotenv import load_dotenv

from Poller import Poller
from checker import ParksCanadaAvailabilityChecker
from constants import GREEN_POINT_ID, TWILIO_AUTH_TOKEN_KEY, TWILIO_PHONE_NUMBER_KEY, TWILIO_ACCOUNT_SID_KEY
from messaging import Contact, TwilioSMSNotifier, ConsoleNotifier

load_dotenv()
notifier = None

# Null contact for default notifications to console
contacts = [None]

try:
	twilio_account_sid = os.getenv(TWILIO_ACCOUNT_SID_KEY)
	twilio_auth_token = os.getenv(TWILIO_AUTH_TOKEN_KEY)
	twilio_phone_number = os.getenv(TWILIO_PHONE_NUMBER_KEY)

	notifier = TwilioSMSNotifier(twilio_account_sid, twilio_auth_token, twilio_phone_number)
except ValueError as e:
	print(e)
	print("Twilio arguments not provided, using console notifier")
	notifier = ConsoleNotifier()

availabilityChecker = ParksCanadaAvailabilityChecker(resource_id=GREEN_POINT_ID)


def configure_contacts():
	add_contact = input("Add contact? Y/N \n")
	while add_contact == "Y":
		name = input("Contact name? \n")
		phone_number = input("Phone number? \n")
		email = input("Email?")
		notify_error = input("Should be notified on errors? Y/N \n") == "Y"
		contacts.append(Contact(name, phone_number, email, notify_error))
		print("Added contact!")
		add_contact = input("Add another contact? Y/N \n")


configure_contacts()

poller = Poller(notifier, availabilityChecker, contacts)

list_of_date_ranges = [
	("2024-08-01", "2024-08-05"),
	("2024-08-02", "2024-08-06"),
	("2024-08-03", "2024-08-07")
]

poller.poll(list_of_date_ranges)
