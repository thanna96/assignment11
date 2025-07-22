from __future__ import annotations

import uuid
from sqlalchemy import Column, Float, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base
from app.operations.factory import OperationType, CalculationFactory


class Calculation(Base):
    """Persisted representation of a calculation."""

    __tablename__ = "calculations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    a = Column(Float, nullable=False)
    b = Column(Float, nullable=False)
    type = Column(Enum(OperationType, name="operation_type"), nullable=False)
    result = Column(Float, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)

    user = relationship("User", back_populates="calculations")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'result' not in kwargs:
            self.result = CalculationFactory.compute(self.type, self.a, self.b)
