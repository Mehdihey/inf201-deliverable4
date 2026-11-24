""" Tests for the Fraction class. Run with: pytest -v test_fraction.py"""
import pytest
from fraction import Fraction


#Initialiser

def test_init_stores_numerrator_and_denominator():
    f = Fraction(3,4)
    assert f._numerator == 3
    assert f.denominator == 4


def test_default_denominator_is_one():
    f = Fraction(5)
    assert f._numerator == 5
    assert f.denominator == 1

@pytest.mark.parametrize("num, den, expected_num, expected_den", [(2, 4, 1, 2), (6, 9, 2, 3), (10, 5, 2, 1), (0, 7, 0, 1)],)
def test_init_reduces_to_lowest_terms(num, den, expected_num, expected_den):
    f = Fraction(num, den)
    assert(f._numerator, f.denominator) == (expected_num, expected_den)



@pytest.mark.parametrize("num, den, expected_num, expected_den",[(1, -2, -1, 2), (-1, -2, 1, 2), (3, -6, -1, 2)],)
def test_init_makes_denominator_positive(num, den, expected_num, expected_den):
    f = Fraction(num, den)
    assert (f._numerator, f.denominator) == (expected_num, expected_den)
    assert f.denominator > 0


def test_zero_denominator_raises():
    with pytest.raises(ZeroDivisionError):
        Fraction(1,0)


@pytest.mark.parametrize("num, den", [(1.5, 2), (1, 2.0), ("1", 2),(True, 2),(1, None)])
def test_non_integer_raises(num, den):
    with pytest.raises(TypeError):
        Fraction(num, den)

def test_attributes_are_read_only():
    f = Fraction(1, 2)
    with pytest.raises(AttributeError):
        f.numerator = 5
    with pytest.raises(AttributeError):
        f.denominator = 5


# Comprisons
def test_equal():
    assert Fraction(1, 2) == Fraction(2,4)
    assert Fraction(-1, 2) == Fraction(1, -2)
    assert Fraction (4, 2) == 2 #comparison with int


def test_not_equal():
    assert Fraction(1,2) != Fraction(1,3)
    assert Fraction(1,2) != 1
    assert not (Fraction( 1, 2) != Fraction(2,4))

def test_less_than():
    assert Fraction(1,3) < Fraction(1,2)
    assert Fraction(-1, 2) < Fraction(1,3)
    assert not (Fraction(1,2) < Fraction(1,2))


def test_less_than_or_equal():
    assert Fraction(1,3) <= Fraction(1,2)
    assert Fraction(1,2) <= Fraction(2,4)
    assert not (Fraction(1,2) <= Fraction(1,3))


def test_greater_than():
    assert Fraction(3,4) > Fraction(2,3)
    assert Fraction(1,2) > 0
    assert not (Fraction(1,2) > Fraction(1,2))


def test_greater_than_or_equal():
    assert Fraction(3, 4) >= Fraction(2,3)
    assert Fraction(2, 4) >= Fraction(1,2)
    assert not (Fraction(1, 3) >= Fraction(1, 2))


def test_comparison_with_unsupported_type():
    f = Fraction(1, 2)
    assert f.__eq__("1/2") is NotImplemented
    assert f.__lt__(0.5) is NotImplemented
    assert (f == "1/2") is False
    with pytest.raises(TypeError):
        f < "1/2"


#Arithmetic
def test_add():
    assert Fraction(1, 2) + Fraction(1, 3) == Fraction(5, 6)
    assert Fraction(1,2) + Fraction(1, 2) == Fraction(1, 1)
    assert Fraction(1, 2) + 1 == Fraction(3, 2)


def test_sub():
    assert Fraction(1, 2) - Fraction(1, 3) == Fraction(1, 6)
    assert Fraction(1, 3) - Fraction(1, 2) == Fraction(-1, 6)
    assert Fraction (1, 2) - Fraction(1, 2) == Fraction(0, 1)


def test_mul():
    assert Fraction(2,3) * Fraction(3, 4) == Fraction(1, 2)
    assert Fraction(-1, 2) * Fraction(2, 5) == Fraction(-1, 5)
    assert Fraction(2, 3) * 3 == Fraction(2, 1)


def test_truediv():
    assert Fraction(1, 2) / Fraction(1, 4) == Fraction(2, 1)
    assert Fraction(1, 2) / Fraction(-1, 3) == Fraction(-3, 2)
    assert (Fraction(1, 2) / Fraction(-1, 3)).denominator > 0

def test_truediv_by_zero_raises():
    with pytest.raises(ZeroDivisionError):
        Fraction(1, 2) / Fraction(0,1)

def test_arithmetic_returns_new_fracrion():
    a = Fraction(1, 2)
    b = Fraction(1, 3)
    result = a + b
    assert isinstance (result, Fraction)
    assert a == Fraction(1, 2) and b == Fraction(1, 3) #Originals unchanged


def test_arithmetic_with_unsupported_type_raises():
    with pytest.raises(TypeError):
        Fraction(1, 2) + "x"


def test_neg():
    assert -Fraction(1, 2) == Fraction(-1, 2)
    assert -Fraction(-3, 4) == Fraction(3, 4)


# Conversions and stings

def test_float():
    assert float(Fraction(1, 4)) == 0.25
    assert float(Fraction(-3, 2)) == -1.5

def test_repr():
    assert repr(Fraction(1, 2)) == "Fraction(1, 2)"
    assert repr(Fraction(2, -4)) == "Fraction(-1, 2)"

def test_str():
    assert str(Fraction(3, 4)) == "3/4"
    assert str(Fraction(-6, 8)) == "-3/4"