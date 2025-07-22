from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.operations.factory import OperationType


class CalculationBase(BaseModel):
    a: float
    b: float
    type: OperationType


class CalculationCreate(CalculationBase):
    @field_validator("b")
    def validate_divisor(cls, v, info):
        if info.data.get("type") == OperationType.DIVIDE and v == 0:
            raise ValueError("Divisor cannot be zero")
        return v


class CalculationRead(CalculationBase):
    id: UUID
    result: float
    user_id: UUID | None = None

    model_config = ConfigDict(from_attributes=True)