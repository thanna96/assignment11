import pytest

from app.operations.factory import CalculationFactory, OperationType
from app.schemas.calculation import CalculationCreate


def test_factory_add():
    assert CalculationFactory.compute(OperationType.ADD, 2, 3) == 5


def test_factory_subtract():
    assert CalculationFactory.compute(OperationType.SUBTRACT, 5, 2) == 3


def test_factory_multiply():
    assert CalculationFactory.compute(OperationType.MULTIPLY, 4, 2) == 8


def test_factory_divide():
    assert CalculationFactory.compute(OperationType.DIVIDE, 6, 3) == 2


def test_create_schema_divide_by_zero():
    with pytest.raises(ValueError):
        CalculationCreate(a=1, b=0, type=OperationType.DIVIDE)