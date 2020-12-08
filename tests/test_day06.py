from advent.days import day06

EXAMPLE = """abc

a
b
c

ab
ac

a
a
a
a

b""".splitlines(
    keepends=True
)


def test_first():
    assert day06.first(EXAMPLE) == 11


def test_second():
    assert day06.second(EXAMPLE) == 6
