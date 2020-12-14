from advent.days import day13
import pytest

EXAMPLE = """939
7,13,x,x,59,x,31,19""".splitlines(keepends=True)


def test_first():
    assert day13.first(EXAMPLE) == 295


@pytest.mark.parametrize('busses, expected', [
    ('7,13,x,x,59,x,31,19', 1068781),
    ('17,x,13,19', 3417),
    ('67,7,59,61', 754018),
    ('67,x,7,59,61', 779210),
    ('67,7,x,59,61', 1261476),
    ('1789,37,47,1889', 1202161486),
])
def test_second(busses: str, expected: int):
    puzzle_input = ['1234', busses]
    assert day13.second(puzzle_input) == expected
