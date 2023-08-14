I2cAddress = int

try:
    from typing import Callable

    TimeFunc = Callable[[], float]
except ImportError:
    Callable = ...
    TimeFunc = ...

try:
    from adafruit_blinka.microcontroller import generic_micropython

    Pin = generic_micropython.Pin
except ImportError:
    generic_micropython = ...
    Pin = ...

Angle = float
Length = float


class Point3D:
    x: float
    y: float
    z: float

    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self) -> str:
        return f'Point3D(x={self.x}, y={self.y}, z={self.z})'

    def __str__(self) -> str:
        return f'({self.x}, {self.y}, {self.z})'

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, Point3D)
            and self.x == other.x
            and self.y == other.y
            and self.z == other.z
        )

    def __abs__(self) -> 'Point3D':
        return Point3D(abs(self.x), abs(self.y), abs(self.z))

    def __add__(self, other) -> 'Point3D':
        if isinstance(other, Point3D):
            return Point3D(self.x + other.x, self.y + other.y, self.z + other.z)
        else:
            return Point3D(self.x + other, self.y + other, self.z + other)

    def __sub__(self, other) -> 'Point3D':
        if isinstance(other, Point3D):
            return Point3D(self.x - other.x, self.y - other.y, self.z - other.z)
        else:
            return Point3D(self.x - other, self.y - other, self.z - other)

    def __mul__(self, other) -> 'Point3D':
        if isinstance(other, Point3D):
            return Point3D(self.x * other.x, self.y * other.y, self.z * other.z)
        else:
            return Point3D(self.x * other, self.y * other, self.z * other)

    def __truediv__(self, other) -> 'Point3D':
        if isinstance(other, Point3D):
            return Point3D(self.x / other.x, self.y / other.y, self.z / other.z)
        else:
            return Point3D(self.x / other, self.y / other, self.z / other)

    def almost_equal(self, other, tolerance: float = 1e-6) -> bool:
        return isinstance(other, Point3D) and (self - other).norm() < tolerance

    def norm(self, p: float = 2) -> float:
        point = abs(self)
        return (point.x ** p + point.y ** p + point.z ** p) ** (1 / p)
