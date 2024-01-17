from dataclasses import dataclass


@dataclass
class Contact:
	name: str
	phone_number: str
	email: str
	notify_error: bool = False
