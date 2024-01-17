class Message:
	def __init__(self, body, is_error=False):
		self.is_error = is_error
		self.body = body
