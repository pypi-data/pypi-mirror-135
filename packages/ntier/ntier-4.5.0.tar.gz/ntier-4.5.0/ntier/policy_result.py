"""Contains the PolicyResult data structure."""
from typing import Optional

from .messages import MessageData, Messages


class PolicyResult:
    """Contains information about whether a policy passes or fails."""

    def __init__(self, is_valid: bool, messages: Optional[Messages]) -> None:
        self.is_valid: bool = is_valid
        self._messages: Optional[Messages] = messages

    def __bool__(self) -> bool:
        return self.is_valid

    @property
    def messages(self) -> MessageData:
        if self._messages is None:
            return {}
        return self._messages.messages

    def union(self, other: "PolicyResult") -> "PolicyResult":
        messages = Messages().merge(self.messages).merge(other.messages)
        return PolicyResult(self.is_valid and other.is_valid, messages)

    @classmethod
    def success(cls) -> "PolicyResult":
        return PolicyResult(True, None)

    @classmethod
    def failed(cls, message: str) -> "PolicyResult":
        return PolicyResult(False, Messages().add_general_message(message))
