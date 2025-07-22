import pytest

from app.models.calculation import Calculation
from app.operations.factory import OperationType, CalculationFactory


def test_calculation_persistence(db_session):
    calc = Calculation(a=2, b=3, type=OperationType.ADD)
    db_session.add(calc)
    db_session.commit()
    db_session.refresh(calc)

    assert calc.result == 5
    row = db_session.query(Calculation).filter_by(id=calc.id).first()
    assert row is not None
    assert row.result == 5


def test_divide_by_zero_model(db_session):
    with pytest.raises(ValueError):
        calc = Calculation(a=1, b=0, type=OperationType.DIVIDE)
        db_session.add(calc)
        db_session.commit()


def test_factory_invalid_type():
    with pytest.raises(ValueError):
        CalculationFactory.compute("invalid", 1, 2)  # type: ignore