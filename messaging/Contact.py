class Contact:
	def __init__(self, name, phone_number=None, email=None, notify_error=False):
		self.name = name
		self.phone_number = phone_number
		self.email = email
		self.notify_error = notify_error
