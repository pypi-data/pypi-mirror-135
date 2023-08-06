"""Contains the ValidationResult data structure."""
from typing import Iterable, Optional

from .messages import MessageData, Messages


class ValidationResult:
    """Contains information about whether a validation passes or fails."""

    def __init__(self, messages: Optional[Messages] = None) -> None:
        self._messages: Optional[Messages] = messages

    def __bool__(self) -> bool:
        return self.is_valid

    @property
    def is_valid(self):
        return not bool(self.messages)

    @property
    def messages(self) -> MessageData:
        if self._messages is None:
            return {}
        return self._messages.messages

    def add_message(self, subject: str, message: str) -> "ValidationResult":
        if self._messages is None:
            self._messages = Messages()
        self._messages.add_message(subject, message)
        return self

    def add_general_message(self, message: str) -> "ValidationResult":
        if self._messages is None:
            self._messages = Messages()
        self._messages.add_general_message(message)
        return self

    def has_failed_for(self, subject: str) -> bool:
        if not self._messages:
            return False
        return self._messages.has_message_for(subject)

    def has_failed_for_any(self, subjects: Iterable[str]) -> bool:
        for subject in subjects:
            if self.has_failed_for(subject):
                return True
        return False

    def union(self, other: "ValidationResult") -> "ValidationResult":
        messages = Messages().merge(self.messages).merge(other.messages)
        return ValidationResult(messages)

    @classmethod
    def success(cls) -> "ValidationResult":
        return ValidationResult()

    @classmethod
    def failed(cls, messages: Messages) -> "ValidationResult":
        return ValidationResult(messages)

    @classmethod
    def builder(cls) -> "ValidationResult":
        return ValidationResult()
