from advent.days import day08

EXAMPLE = """nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6""".splitlines(
    keepends=True
)


def test_first():
    assert day08.first(EXAMPLE) == 5


def test_second():
    assert day08.second(EXAMPLE) == 8
