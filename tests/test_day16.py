from advent.days import day16
from advent.days.day16 import FieldRule


def test_parse_rule():
    assert day16.parse_rule("departure time: 48-702 or 719-955") == FieldRule(
        "departure time", (48, 702), (719, 955)
    )


def test_fieldrule_valid():
    rule = FieldRule("departure time", (48, 702), (719, 955))
    assert rule.validate(48) is True
    assert rule.validate(702) is True
    assert rule.validate(3000) is False
    assert rule.validate(703) is False
    assert rule.validate(-7) is False
    assert rule.validate(720) is True


EXAMPLE = """class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12""".splitlines(
    keepends=True
)


def test_parse_input():
    assert day16.parse_input(iter(EXAMPLE)) == (
        [
            FieldRule(name="class", low_range=(1, 3), high_range=(5, 7)),
            FieldRule(name="row", low_range=(6, 11), high_range=(33, 44)),
            FieldRule(name="seat", low_range=(13, 40), high_range=(45, 50)),
        ],
        [7, 1, 14],
        [[7, 3, 47], [40, 4, 50], [55, 2, 20], [38, 6, 12]],
    )


def test_first():
    assert day16.first(iter(EXAMPLE)) == 71


EXAMPLE_2 = """class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9""".splitlines(
    keepends=True
)


def test_second():
    assert day16.second(iter(EXAMPLE_2)) == 1
