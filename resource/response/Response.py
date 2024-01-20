from dataclasses import dataclass

from messaging import Message


@dataclass(kw_only=True)
class Response:
	error: Exception = None

	def to_message(self) -> Message:
		raise NotImplementedError()

	def __add__(self, other):
		from .CombinedResponse import CombinedResponse
		return CombinedResponse([self, other])
