class NotificationException(Exception):
	def __init__(self, message: str, underlying: Exception = Exception()):
		self.message = message
		self.underlying = underlying

	def __str__(self):
		return f'{self.message} + \n + Underlying exception: {self.underlying}'
