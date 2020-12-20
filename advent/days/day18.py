"""
Interesting resource to implement this with an AST instead:
https://craftinginterpreters.com/parsing-expressions.html

This implementation works because there are only 2 precedences:
- if hitting a +, then consume an operand to the right and sum
- if hitting a *, then evaluate the rest of the tokens and multiply with the left operand

The tokenization could be applied, but the evaluation only works
because the grammar is simple.

"""

import re
from dataclasses import dataclass
from typing import Iterator

OP_PLUS = "+"
OP_MUL = "*"

SEP_OPENP = "("
SEP_CLOSEP = ")"

R_OPERATOR = fr"[{OP_PLUS}{OP_MUL}]"
R_LITERAL = r"[0-9]+"
R_SEPARATOR = fr"[{SEP_OPENP}{SEP_CLOSEP}]"

R_TOKEN = fr"{R_OPERATOR}|{R_LITERAL}|{R_SEPARATOR}"


OPERATOR = "OPERATOR"
LITERAL = "LITERAL"
SEPARATOR = "SEPARATOR"


@dataclass
class Token:
    type: str
    value: str


def tokenize(expr: str):
    raw_tokens = re.findall(R_TOKEN, expr)

    tokens = []
    for raw_token in raw_tokens:
        if re.match(fr"^{R_OPERATOR}$", raw_token):
            ttype = OPERATOR
        elif re.match(fr"^{R_LITERAL}$", raw_token):
            ttype = LITERAL
        elif re.match(fr"^{R_SEPARATOR}$", raw_token):
            ttype = SEPARATOR
        else:
            raise ValueError("Unable to parse token")
        tokens.append(Token(type=ttype, value=raw_token))

    return tokens


def evaluate(expr: str, eval_fn) -> int:
    """Evaluate an expression to produce an integer"""

    tokens = tokenize(expr)
    return eval_fn(iter(tokens))


def chomp_operand(tokens: Iterator[Token]):
    """
    Chomps from a list of tokens to form an operand

    An operand is either a literal like '4' or a parenthesis expression
    like '(3 + (4 * 2))'.

    """
    token = next(tokens)
    if token.type == LITERAL:
        return [token]

    operand_texpr = []
    # It has to be an open parenthesis
    assert token.value == SEP_OPENP
    paren_count = 1

    while True:
        token = next(tokens)

        if token.value == SEP_OPENP:
            paren_count += 1
        elif token.value == SEP_CLOSEP:
            paren_count -= 1
            if paren_count == 0:
                break

        operand_texpr.append(token)

    return operand_texpr


def eval_tokens(tokens: Iterator[Token]) -> int:
    """Evaluate a list of tokens into an integer"""

    # Chomp tokens until we have a full operand
    left_operand = chomp_operand(tokens)

    if len(left_operand) == 1:
        assert left_operand[0].type == LITERAL
        left = int(left_operand[0].value)
    else:
        left = eval_tokens(iter(left_operand))

    operator = next(tokens, None)
    while operator:
        # Keep aggregating into left
        right = eval_tokens(iter(chomp_operand(tokens)))
        if operator.value == OP_MUL:
            left *= right
        else:
            left += right
        operator = next(tokens, None)

    return left


def eval_tokens2(tokens: Iterator[Token]) -> int:
    """
    Evaluate a list of tokens into an integer.

    Additions have priority over multiplications.
    """

    # Chomp tokens until we have a full operand
    left_operand = chomp_operand(tokens)

    operator = next(tokens, None)
    if not operator:
        if len(left_operand) == 1:
            assert left_operand[0].type == LITERAL
            return int(left_operand[0].value)
        return eval_tokens2(iter(left_operand))

    left = eval_tokens2(iter(left_operand))
    while operator:
        if operator.value == OP_MUL:
            # Evaluate the rest of the tokens and add it to left
            right = eval_tokens2(tokens)
            return left * right

        # Evaluate immediately left + right then store in left and keep going
        right = eval_tokens2(iter(chomp_operand(tokens)))
        left += right

        operator = next(tokens, None)

    return left


def first(puzzle_input: Iterator[str]) -> int:
    return sum(evaluate(line.strip(), eval_tokens) for line in puzzle_input)


def second(puzzle_input: Iterator[str]) -> int:
    return sum(evaluate(line.strip(), eval_tokens2) for line in puzzle_input)
