"""Contains the StructuredTransaction class."""
# pylint: disable=unused-argument
from typing import Generic, Optional, TypeVar

from .policy_result import PolicyResult
from .transaction_result import TransactionResult
from .validation_result import ValidationResult

InputType = TypeVar("InputType")
StateType = TypeVar("StateType")


class TransactionBase(Generic[InputType, StateType]):
    """Allows child classes to define parts of a standard transaction life-cycle:
    - initialize
    - authenticate
    - find
    - authorize
    - validate
    - perform
    """

    async def execute(self, data: InputType) -> TransactionResult:
        """Calls and response properly to overridden methods to run a standard API request."""
        state = await self.map_input(data)

        is_authenticated = await self.authenticate(state)
        if not is_authenticated:
            return TransactionResult.not_authenticated()

        missing_entity_name = await self.find(state)
        if missing_entity_name:
            return TransactionResult.not_found(missing_entity_name)

        policy_result = await self.authorize(state)
        if not policy_result.is_valid:
            return TransactionResult.not_authorized(policy_result)

        validation_result = await self.validate(state)
        if not validation_result.is_valid:
            return TransactionResult.not_valid(validation_result)

        result = await self.perform(state)
        return result

    async def __call__(self, data: InputType) -> TransactionResult:
        return await self.execute(data)

    async def map_input(self, data: InputType) -> StateType:
        raise NotImplementedError()

    async def authenticate(self, state: StateType) -> bool:
        return True

    async def find(self, state: StateType) -> Optional[str]:
        return None

    async def authorize(self, state: StateType) -> PolicyResult:
        return PolicyResult.success()

    async def validate(self, state: StateType) -> ValidationResult:
        return ValidationResult.success()

    async def perform(self, state: StateType) -> TransactionResult:
        raise NotImplementedError()
