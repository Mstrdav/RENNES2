# Imports

# Classes et fonctions
class Point:
    def __init__(self, x=0, y=0):
        self.x, self.y = x, y

    def __repr__(self):
        return f'Point(x={self.x},y={self.y})'

    def dist(self, other):
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

class Intervalle:
    def __init__(self, a, b):
        self.a, self.b = min(a, b), max(a, b)

    def __repr__(self):
        return f'Intervalle({self.a},{self.b})'

    def __contains__(self, v):
        return self.a <= v <= self.b

class Fraction:
    def __init__(self, num=1, den=1):
        if den == 0:
            raise ValueError("Denominator cannot be zero.")
        self.num = abs(num)
        self.den = abs(den)
        self.signe = (num * den) >= 0

    def __repr__(self):
        return f'Fraction({"-" if not self.signe else ""}{self.num},{self.den})'

    def __neg__(self):
        return Fraction(-self.num if self.signe else self.num, self.den)

    def __add__(self, other):
        num = self.num * other.den + other.num * self.den
        den = self.den * other.den
        return Fraction(num if self.signe == other.signe else -num, den).simplify()

    def __mul__(self, other):
        num = self.num * other.num
        den = self.den * other.den
        return Fraction(num * -1 if self.signe != other.signe else 1, den).simplify()

    def simplify(self):
        # simplify fraction
        def gcd(a, b):
            while b:
                a, b = b, a % b
            return a
        common_divisor = gcd(self.num, self.den)
        self.num //= common_divisor
        self.den //= common_divisor
        return self

# Tests
if __name__ == "__main__":
    # Test Point
    p1 = Point(1, 2)
    p2 = Point(4, 6)
    print(p1)  # Point(x=1,y=2)
    print(p2)  # Point(x=4,y=6)
    print(p1.dist(p2))  # Distance between p1 and p2

    # Test Intervalle
    interval = Intervalle(3, 7)
    print(interval)  # Intervalle(3,7)
    print(5 in interval)  # True
    print(2 in interval)  # False

    # Test Fraction
    f1 = Fraction(3, 4)
    f2 = Fraction(-2, 5)
    print(f1)  # Fraction(3,4)
    print(f2)  # Fraction(-2,5)
    print(f1 + f2)  # Addition of fractions
    print(f1 * f2)  # Multiplication of fractions
    print(-f1)  # Negation of fraction
    f3 = Fraction(8, 12)
    print(f3.simplify())  # Simplified fraction
