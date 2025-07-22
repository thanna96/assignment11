from enum import Enum
from typing import Callable, Dict

from . import add, subtract, multiply, divide

class OperationType(str, Enum):
    """Enumeration of supported calculation types."""
    ADD = "add"
    SUBTRACT = "subtract"
    MULTIPLY = "multiply"
    DIVIDE = "divide"


class CalculationFactory:
    """Factory to compute results based on operation type."""

    _operations: Dict[OperationType, Callable[[float, float], float]] = {
        OperationType.ADD: add,
        OperationType.SUBTRACT: subtract,
        OperationType.MULTIPLY: multiply,
        OperationType.DIVIDE: divide,
    }

    @classmethod
    def compute(cls, op_type: OperationType, a: float, b: float) -> float:
        """Return result for the given operation."""
        func = cls._operations.get(op_type)
        if not func:
            raise ValueError("Invalid calculation type")
        return func(a, b)