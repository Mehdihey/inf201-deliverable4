""" Tempratur class supporting Celcious ("C"), Farenheit ("F"), and kelvin("K") """
TOLERANCE = 1e-9
VALID_UNITS = ("C", "F", "K")

def _normalise_unit(unit):
    """return the unit in upper case, or raise ValueError if it is not valid"""
    if not isinstance(unit, str) or unit.upper() not in VALID_UNITS:
        raise ValueError(f"Invalid unit {unit!r}. use one of {VALID_UNITS}.")
    return unit.upper()

def _to_kelvin(value, unit):
    """convert a value in the given ubit to kelvin"""
    if unit == "K":
        return value
    if unit == "C":
        return value + 273.15
    if unit == "F":
        return (value - 32) * 5 / 9 + 273.15


class Temperature:
    """A temperature with a value and a unit ("C", "K", "F")."""

    def __init__(self, value, unit = "C"):
        if isinstance(value, bool) or not isinstance(value,(int, float)):
            raise TypeError("Temperature value must be  a number.")

        unit = _normalise_unit(unit)
        value = float(value)

        # small negative numbers (e.g. -5e-14 K) come from floating-point
        #  rounding, so we only reject values clearly below absolute zero.

        if _to_kelvin(value, unit) < -TOLERANCE:
            raise ValueError("Temperature cannot be below absolute zero (0 k)")

        self._value = value
        self._unit = unit

    #Read-only attributes

    @property
    def value(self):
        return self._value

    @property
    def unit(self):
        return self._unit

    #conversions
    def to_kelvin(self) -> float:
        return _to_kelvin(self._value, self._unit)
    
    def to_celsius(self) -> float:
        if self._unit == "C":
            return self._value
        if self._unit == "K":
            return self._value - 273.15
        return (self._value - 32) * 5/9

    def to_fahrenheit(self) -> float:
        if self._unit == "F":
            return self._value
        if self._unit == "C":
            return self._value * 9 / 5 + 32
        return (self._value - 273.15) * 9 / 5 + 32

    def convert_to(self, target_unit:str) -> "Temperature":
        target_unit = _normalise_unit(target_unit)
        converters = {
            "C": self.to_celsius,
            "F": self.to_fahrenheit,
            "K": self.to_kelvin,
        }
        return Temperature(converters[target_unit](),target_unit)


    #Comparisons (all done in kelvin)
    def __eq__(self, other):
        if not isinstance(other, Temperature):
            return NotImplemented
        return abs(self.to_kelvin() - other.to_kelvin()) <= TOLERANCE

    def __ne__(self, other):
        if not isinstance(other, Temperature):
            return NotImplemented
        return not self == other

    def __lt__(self, other):
        if not isinstance (other, Temperature):
            return NotImplemented
        return self.to_kelvin() < other.to_kelvin() and not self == other

    def __le__(self, other):
        if not isinstance(other, Temperature):
            return NotImplemented
        return self.to_kelvin() < other.to_kelvin() or self == other

    def __gt__(self, other):
        if not isinstance(other, Temperature):
            return NotImplemented
        return self.to_kelvin() > other.to_kelvin() and not self == other

    def __ge__(self, other):
        if not isinstance(other, Temperature):
            return NotImplemented
        return self.to_kelvin() > other.to_kelvin() or self == other

    def __repr__(self) -> str:
        return f"Temperature({self._value!r}, '{self._unit}')"

    def __str__(self) -> str:
        return f"{self._value:.2f} °{self._unit}"
    