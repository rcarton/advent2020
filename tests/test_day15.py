import pytest

from advent.days import day15


@pytest.mark.parametrize(
    "puzzle_input, expected",
    [
        ("1,3,2", 1),
        ("2,1,3", 10),
        ("1,2,3", 27),
        ("2,3,1", 78),
        ("3,2,1", 438),
        ("3,1,2", 1836),
    ],
)
def test_first(puzzle_input, expected):
    assert day15.first([puzzle_input]) == expected
