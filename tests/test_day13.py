import pytest

from advent.days import day13

EXAMPLE = """939
7,13,x,x,59,x,31,19""".splitlines(
    keepends=True
)


def test_first():
    assert day13.first(EXAMPLE) == 295


@pytest.mark.parametrize(
    "busses, expected",
    [
        ("3,x,x,4,5", 21),
        ("7, 13, 5", 168),
        ("7,13,x,x,59,x,31,19", 1068781),
        ("17,x,13,19", 3417),
        ("67,7,59,61", 754018),
        ("67,x,7,59,61", 779210),
        ("67,7,x,59,61", 1261476),
        ("1789,37,47,1889", 1202161486),
    ],
)
def test_second(busses: str, expected: int):
    puzzle_input = ["1234", busses]
    assert day13.second(puzzle_input) == expected


@pytest.mark.parametrize(
    "busses, expected",
    [
        ("7,13,5", 168),
        ("17,x,13,19", 3417),
        ("67,7,59,61", 754018),
    ],
)
def test_second_brute(busses: str, expected: int):
    puzzle_input = ["1234", busses]
    assert day13.second_brute(puzzle_input) == expected
