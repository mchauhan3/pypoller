from dataclasses import dataclass
from functools import reduce
from typing import List

from messaging import Message
from . import Response


@dataclass
class CombinedResponse(Response):
	underlying_responses: List[Response]

	def to_message(self) -> Message:
		return reduce((lambda x, y: x + y), [resp.to_message() for resp in self.underlying_responses])

	def __add__(self, other):
		if isinstance(other, CombinedResponse):
			return CombinedResponse(self.underlying_responses + other.underlying_responses)

		return CombinedResponse(self.underlying_responses + [other])
