import os
from dotenv import load_dotenv

from Poller import Poller
from checker import ParksCanadaAvailabilityChecker
from constants import GREEN_POINT_ID
from messaging import Contact, TwilioSMSNotifier

load_dotenv()

twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID")
twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_phone_number = os.getenv("TWILIO_PHONE_NUMBER")

notifier = TwilioSMSNotifier(twilio_account_sid, twilio_auth_token, twilio_phone_number)
availabilityChecker = ParksCanadaAvailabilityChecker(resource_id=GREEN_POINT_ID)

contacts = []


def configure_contacts():
	add_contact = input("Add contact? Y/N")
	while add_contact == "Y":
		name = input("Contact name?")
		phone_number = input("Phone number?")
		email = input("Email?")
		notify_error = input("Should be notified on errors? Y/N") == "Y"
		contacts.append(Contact(name, phone_number, email, notify_error))
		print("Added contact!")
		add_contact = input("Add another contact? Y/N")


configure_contacts()

poller = Poller(notifier, availabilityChecker, contacts)

list_of_date_ranges = [
	("2024-08-01", "2024-08-05"),
	("2024-08-02", "2024-08-06"),
	("2024-08-03", "2024-08-07")
]

poller.poll(list_of_date_ranges)
