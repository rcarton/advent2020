from advent.days import day17

EXAMPLE = """.#.
..#
###""".splitlines(
    keepends=True
)


def test_first():
    assert day17.first(EXAMPLE) == 112


def test_second():
    assert day17.second(EXAMPLE) == 848
