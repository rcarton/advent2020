import pytest

from advent.days import day02
from advent.days.day02 import PasswordPolicy

EXAMPLE = """1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc""".splitlines()


def test_first():
    assert day02.first(EXAMPLE) == 2


def test_second():
    assert day02.second(EXAMPLE) == 1


@pytest.mark.parametrize(
    "policy_str, expected",
    [
        ("1-3 a", PasswordPolicy(1, 3, "a")),
        ("1-3 b", PasswordPolicy(1, 3, "b")),
        ("2-9 c", PasswordPolicy(2, 9, "c")),
    ],
)
def test_parse_policy(policy_str, expected):
    assert day02.parse_policy(policy_str) == expected


@pytest.mark.parametrize(
    "entry, expected",
    [
        ("1-3 a: abcde", True),
        ("1-2 x: xxxx", False),
        ("1-20 x: xxxx", True),
    ],
)
def test_is_entry_valid_second(entry, expected):
    assert day02.is_entry_valid_second(entry) == expected
