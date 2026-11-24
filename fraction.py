"""fraction class with integer numerator and strictly posiitive denominator"""

from math import gcd

class Fraction:
    """a fraction numerator/dominator, always stored in lowest terms"""

    def __init__(self, numeraotr, denominator = 1):
        # bool is a subclass of int, so reject it explicity

        for number in (numeraotr, denominator):
            if isinstance(number, bool) or not isinstance(number, int):
                raise TypeError("Numerator and denominator must beintegers.")

        if denominator == 0:
            raise ZeroDivisionError("Denominator cannot be zero.")
        
        #keep the denominator positive: 1/-2 becomes -1/2

        if denominator < 0:
            numeraotr = - numeraotr
            denominator = -denominator

        #reduce to lowest terms 2/4 becomes 1/2

        common = gcd(numeraotr, denominator)
        self._numerator = numeraotr // common
        self._denominator = denominator // common


    #read only attrubutes
    @property
    def denominator(self):
        return self._numinator
    

    @property
    def denominator(self):
        return self._denominator


    # Helper
    @staticmethod
    def _to_fraction(other):
        #Turn an int into a Fraction; return None for unsupported types
        if isinstance(other, Fraction):
            return other
        if isinstance(other, int) and not isinstance(other, bool):
            return Fraction(other)
        return None

    #Comprsion
    #a//b vs c/d -> compare a*d with c*b (safe because b and d are positive)
    def __eq__(self, other):
        other = self._to_fraction(other)
        if other is None:
            return NotImplemented
        return self._numerator * other._denominator == other._numerator * self._denominator

    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return NotImplemented
        return not result

    def __lt__(self, other):
        other = self._to_fraction(other)
        if other is None:
            return NotImplemented
        return self._numerator * other._denominator < other._numerator * self._denominator

    def __le__(self, other):
        other = self._to_fraction(other)
        if other is None:
            return NotImplemented
        return self._numerator * other._denominator <= other._numerator * self._denominator

    def __gt__(self, other):
        other = self._to_fraction(other)
        if other is None:
            return NotImplemented
        return self._numerator * other._denominator > other._numerator * self._denominator

    def __ge__(self, other):
        other = self._to_fraction(other)
        if other is None:
            return NotImplemented
        return self._numerator * other._denominator >= other._numerator * self._denominator


    #Arithmetic
    def __add__(self, other):
        other = self._to_fraction(other)
        if other is None:
            return NotImplemented
        # a/b + c/d = ((a*d +c*b)/ (b*d))
        return Fraction(self._numerator * other._denominator + other._numerator * self._denominator, self._denominator * other._denominator,)


    def __sub__(self, other):
        other = self._to_fraction(other)
        if other is None:
            return NotImplemented

        #a/b - c/d = (a*d - c*d)/(c*d)
        return Fraction(self._numerator * other._denominator - other._numerator * self._denominator, self._denominator * other._denominator)


    def __mul__(self, other):
        other = self._to_fraction(other)
        if other is None:
            return NotImplemented
        #a/b * c/d = (a*c) / (b*d)
        return Fraction(self._numerator * other._numerator, self._denominator * other._denominator,)

    def __truediv__(self, other):
        other = self._to_fraction(other)
        if other is None:
            return NotImplemented
        if other._numerator == 0:
            raise ZeroDivisionError("Cannot divide by a zero fraction")
        #(a/b) / (c/d) = (a*d) / (b*c): Fraction() fixes the sign if c < 0

        return Fraction(self._numerator * other._denominator, self._denominator * other._numerator,)


    def __neg__(self):
        return Fraction(-self._numerator, self._denominator)


    # Converions and string representations 

    def __float__(self):
        return self._numerator / self._denominator

    def __repr__(self):
        return f"Fraction({self._numerator}, {self._denominator})"

    def __str__(self):
        return f"{self._numerator}/{self._denominator}"