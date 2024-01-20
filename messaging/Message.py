from dataclasses import dataclass


@dataclass
class Message:
	body: str = ""
	is_error: bool = False

	def __add__(self, other):
		from .CombinedMessage import CombinedMessage
		return CombinedMessage(underlying_messages=[self, other])
