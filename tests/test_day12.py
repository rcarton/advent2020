import pytest

from advent.days import day12
from advent.days.day12 import Waypoint as Wp

EXAMPLE = """F10
N3
F7
R90
F11""".splitlines(
    keepends=True
)


def test_first():
    assert day12.first(EXAMPLE) == 25


def test_second():
    assert day12.second(EXAMPLE) == 286


@pytest.mark.parametrize(
    "waypoint, left_or_right, degrees, expected",
    [
        (Wp(-4, 10), "R", 90, Wp(10, 4)),
        (Wp(-4, 10), "L", 270, Wp(10, 4)),
    ],
)
def test_waypoint_rotate(waypoint: Wp, left_or_right: str, degrees: int, expected: Wp):
    waypoint.rotate(left_or_right, degrees)
    assert waypoint == expected
