from uuid import UUID
from pydantic import BaseModel, ConfigDict, field_validator, model_validator

from app.operations.factory import OperationType


class CalculationBase(BaseModel):
    a: float
    b: float
    type: OperationType


class CalculationCreate(CalculationBase):
    @model_validator(mode="after")
    def validate_divisor(cls, values):
        if values.type == OperationType.DIVIDE and values.b == 0:
            raise ValueError("Divisor cannot be zero")
        return values


class CalculationRead(CalculationBase):
    id: UUID
    result: float
    user_id: UUID | None = None

    model_config = ConfigDict(from_attributes=True)