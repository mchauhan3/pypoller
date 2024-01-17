from dataclasses import dataclass


@dataclass
class Message:
	body: str
	is_error: bool = False
