import pytest


def addition(a, b):
    return a + b


def subtraction(a, b):
    return a - b


def multiplication(a, b):
    return a * b


def division(a, b):
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero!")
    return a / b


def test_addition():
    assert addition(2, 3) == 5


def test_subtraction():
    assert subtraction(2, 3) == -1


def test_multiplication():
    assert multiplication(2, 3) == 6


def test_division():
    assert division(2, 3) == 2 / 3


def test_division_by_zero():
    with pytest.raises(ZeroDivisionError):
        division(2, 0)
