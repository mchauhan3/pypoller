from dataclasses import dataclass, field
from typing import List

from . import Message


@dataclass
class CombinedMessage(Message):
	underlying_messages: List[Message] = field(default_factory=lambda: [])

	def __add__(self, other):
		if isinstance(other, CombinedMessage):
			return CombinedMessage(underlying_messages=self.underlying_messages + other.underlying_messages)

		return CombinedMessage(underlying_messages=self.underlying_messages + [other])
