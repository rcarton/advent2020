import pytest

from advent.days import day07

EXAMPLE = """
light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
""".splitlines(
    keepends=True
)


def test_first():
    assert day07.first(EXAMPLE) == 4


EXAMPLE_2 = """shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.
""".splitlines(
    keepends=True
)


def test_second():
    assert day07.second(EXAMPLE_2) == 126


def test_parse_input():
    parse_input_s = """vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.""".splitlines(
        keepends=True
    )

    assert day07.parse_input(parse_input_s) == [
        ("vibrant plum", [(5, "faded blue"), (6, "dotted black")]),
        ("faded blue", []),
    ]


@pytest.mark.parametrize(
    "bag_match, expected",
    [
        ("1 bright white bag", (1, "bright white")),
        ("4 dotted black bags", (4, "dotted black")),
    ],
)
def test_get_count_and_color(bag_match, expected):
    assert day07.get_count_and_color(bag_match) == expected
