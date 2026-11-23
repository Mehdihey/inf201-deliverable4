"""Test for the temperaturee class. run with: pytest -v test _temperaturee.py"""
import pytest
from temperature import Temperature

TOL = 1e-9

#1. initialisation
def test_default_unit_is_celsius():
    t = Temperature(25)
    assert t.unit == "C"
    assert t.value == 25.0


@pytest.mark.parametrize("unit, expected", [("c", "C"), ("f","F"), ("k", "K"), ("K", "K")])
def test_unit_is_case_insensitive(unit, expected):
    assert Temperature(300, unit).unit == expected



def test_value_is_read_only():
    t = Temperature(25, "C")
    with pytest.raises(AttributeError):
        t.value = 30


def test_unit_is_read_only():
    t = Temperature(25, "C")
    with pytest.raises(AttributeError):
        t.unit = "F"


#2.Validation
@pytest.mark.parametrize("bad_unit", ["X", "celsius", "", "CF", None, 5])
def test_invalid_unit_raises(bad_unit):
    with pytest.raises(ValueError):
        Temperature(10, bad_unit)


@pytest.mark.parametrize("value, unit", [(-273.16, "C"), (-459.68, "F"), (-0.01, "K")])
def test_below_absolute_zero_raises(value, unit):
    with pytest.raises(ValueError):
        Temperature(value, unit)

@pytest.mark.parametrize("value, unit", [(-273.15, "C"), (-459.67, "F"), (0, "K")])
def test_exactly_ablolute_zero_is_allowed(value, unit):
    Temperature(value, unit) #Should not raise

def test_convert_to_invalid_unit_raises():
    with pytest.raises(ValueError):
        Temperature(10, "C").convert_to("X")


#3.Conversions at reference points
REFERENCE_POINTS = [
    #( celsius, fahrenheit, kelvin)
    (-273.15, -459.67, 0.0), #Ablolute 0
    (-40.0, -40.0, 233.15), #Celsius-Fahrenheit crossover
    (0.0, 32.0, 273.15), # freezing point of water
    (37.0, 98.6, 310.15), #human body temperaturee
    (100.0, 212.0, 373.15), #boiling point of water
]

@pytest.mark.parametrize("c, f, k", REFERENCE_POINTS)
def test_conversions_from_celsius( c, f, k):
    t = Temperature(c, "C")
    assert t.to_celsius() == pytest.approx(c, abs=TOL)
    assert t.to_fahrenheit() == pytest.approx(f, abs=TOL)
    assert t.to_kelvin() == pytest.approx(k, abs=TOL)

@pytest.mark.parametrize("c, f, k", REFERENCE_POINTS)
def test_sonversions_from_fahrenheit(c, f, k):
    t = Temperature(f, "F")
    assert t.to_celsius() == pytest.approx(c, abs=TOL)
    assert t.to_fahrenheit() == pytest.approx(f, abs=TOL)
    assert t.to_kelvin() == pytest.approx(k, abs=TOL)

@pytest.mark.parametrize("c, f, k", REFERENCE_POINTS)
def test_conversions_from_kelvin(c, f, k):
    t = Temperature(k, "K")
    assert t.to_celsius() == pytest.approx(c, abs=TOL)
    assert t.to_fahrenheit() == pytest.approx(f, abs=TOL)
    assert t.to_kelvin() == pytest.approx(k, abs=TOL)

@pytest.mark.parametrize("c, f, k", REFERENCE_POINTS)
def test_convert_to_returns_new_temperaturee(c, f, k):
    original = Temperature(c, "C")
    in_f = original.convert_to("f")
    in_k = original.convert_to("K")
    assert isinstance(in_f, Temperature)
    assert in_f.unit == "F"
    assert in_f.value == pytest.approx(f, abs=TOL)
    assert in_k.unit == "K"
    assert in_k.value == pytest.approx(k, abs=TOL)
    assert original.unit == "C" #Original is unchanged


#4. Round-tripp conversions
@pytest.mark.parametrize("c, f, k", REFERENCE_POINTS)
def test_round_trip_c_f_k_c(c, f, k):
    original = Temperature(c, "C")
    back = original.convert_to("F").convert_to("K").convert_to("C")
    assert back.unit == "C"
    assert back == original
    assert back.value == pytest.approx(original.value, abs=TOL)


#5. cross-unit comprasions
@pytest.mark.parametrize("c, f, k", REFERENCE_POINTS)
def test_equality_across_units(c, f, k):
    assert Temperature(c, "C") == Temperature(f, "F")
    assert Temperature(f, "F") == Temperature(k, "k")
    assert Temperature(k, "K") == Temperature(c, "C")
    assert not (Temperature(c, "C") != Temperature(k, "K"))

def test_not_equal_across_units():
    assert Temperature(0, "C") != Temperature(0,"F")
    assert Temperature(100, "C") != Temperature(100, "K")


def test_ordering_across_units():
    cold = Temperature(0, "C") #273.15 k
    warm = Temperature(98.6, "F") #310.15 K
    hot = Temperature(373.15, "K") #100C

    assert cold < warm < hot
    assert hot > warm > cold
    assert cold <= warm and warm <= hot
    assert hot >= warm and warm >= cold

def test_ordering_with_equal_values():
    a = Temperature(0,"C")
    b = Temperature(32, "F")
    assert a <= b and a >= b
    assert not (a < b) and not (a > b)


def test_comparison_with_non_temperaturee():
    t = Temperature(0, "C")
    assert t.__eq__(5) is NotImplemented
    assert t.__lt__("hot") is NotImplemented
    assert t !=5
    with pytest.raises(TypeError):
        t < 5

#6. Formatting
def test_repr():
    assert repr(Temperature(25, "C")) == "Temperature(25.0, 'C')"
    assert repr(Temperature(98.6, "f")) == "Temperature(98.6, 'F')"

def test_str():
    assert str(Temperature(25, "C")) == "25.00 °C"
    assert str(Temperature(98.6, "F")) == "98.60 °F"
    assert str(Temperature(273.15, "K")) == "273.15 °K"
 
