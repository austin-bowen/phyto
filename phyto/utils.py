from math import cos, sin

from phyto.types import Point3D


def rotate_point(point: Point3D, angle: float) -> Point3D:
    return Point3D(
        point.x * cos(angle) - point.y * sin(angle),
        point.x * sin(angle) + point.y * cos(angle),
        point.z
    )
