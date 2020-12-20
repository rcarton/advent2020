import pytest

from advent.days import day18
from advent.days.day18 import Token


def test_tokenize():
    assert day18.tokenize("(2+3)*4+(7*45+(3*4))") == [
        Token(type="SEPARATOR", value="("),
        Token(type="LITERAL", value="2"),
        Token(type="OPERATOR", value="+"),
        Token(type="LITERAL", value="3"),
        Token(type="SEPARATOR", value=")"),
        Token(type="OPERATOR", value="*"),
        Token(type="LITERAL", value="4"),
        Token(type="OPERATOR", value="+"),
        Token(type="SEPARATOR", value="("),
        Token(type="LITERAL", value="7"),
        Token(type="OPERATOR", value="*"),
        Token(type="LITERAL", value="45"),
        Token(type="OPERATOR", value="+"),
        Token(type="SEPARATOR", value="("),
        Token(type="LITERAL", value="3"),
        Token(type="OPERATOR", value="*"),
        Token(type="LITERAL", value="4"),
        Token(type="SEPARATOR", value=")"),
        Token(type="SEPARATOR", value=")"),
    ]


@pytest.mark.parametrize(
    "tokens, expected",
    [
        (
            "(2 * (3 + 1)) + 4",
            [
                Token(type="LITERAL", value="2"),
                Token(type="OPERATOR", value="*"),
                Token(type="SEPARATOR", value="("),
                Token(type="LITERAL", value="3"),
                Token(type="OPERATOR", value="+"),
                Token(type="LITERAL", value="1"),
                Token(type="SEPARATOR", value=")"),
            ],
        ),
        ("2 + 4", [Token(type="LITERAL", value="2")]),
        ("1", [Token(type="LITERAL", value="1")]),
    ],
)
def test_chomp_operand(tokens, expected):
    tokens = iter(day18.tokenize(tokens))
    assert day18.chomp_operand(tokens) == expected


@pytest.mark.parametrize(
    "tokens, expected",
    [
        ("(2 * (3 + 1)) + 4", 12),
        ("2 + 4", 6),
        ("1", 1),
    ],
)
def test_eval_tokens(tokens, expected):
    assert day18.eval_tokens(iter(day18.tokenize(tokens))) == expected


EXAMPLE = """2 * 3 + (4 * 5)
5 + (8 * 3 + 9 + 3 * 4 * 3)
5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))
((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2""".splitlines(
    keepends=True
)


def test_first():
    assert day18.first(EXAMPLE) == 26 + 437 + 12240 + 13632


@pytest.mark.parametrize(
    "expression, expected",
    (
        [
            ("1 + 2 * 3 + 4 * 5 + 6", 71),
            ("2 * 3 + (4 * 5)", 26),
            ("5 + (8 * 3 + 9 + 3 * 4 * 3)", 437),
            ("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))", 12240),
            ("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2", 13632),
        ]
    ),
)
def test_evaluate(expression, expected):
    assert day18.evaluate(expression, day18.eval_tokens) == expected


@pytest.mark.parametrize(
    "expression, expected",
    (
        [
            ("1 + (2 * 3) + (4 * (5 + 6))", 51),
            ("2 * 3 + (4 * 5)", 46),
            ("5 + (8 * 3 + 9 + 3 * 4 * 3)", 1445),
            ("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))", 669060),
            ("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2", 23340),
        ]
    ),
)
def test_evaluate2(expression, expected):
    assert day18.evaluate(expression, day18.eval_tokens2) == expected
