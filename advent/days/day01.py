import itertools as its
from typing import Iterator


def first_combinations(expense_input: Iterator[str]) -> int:
    """
    The laziest approach.

    A smarter approach would be to keep track of the counts of each expense, and then
    for each value look for the complement to add up to 2020.

    This can be applied to the combination of 3 expenses by looking at an expense and
    then finding a 2-combination that adds to the complement for this first expense.

    The input is small enough that it's not worth the data structure gymnastics, but
    the complexity of looking at all the combinations would not be good for larger
    data sets.

    """

    expenses = [int(line) for line in expense_input]

    for c in its.combinations(expenses, 2):
        if sum(c) == 2020:
            return c[0] * c[1]

    raise ValueError("No combination of two expenses adds up to 2020")


def second_combinations(expense_input: Iterator[str]) -> int:
    """Same approach, but this looks at 3-combinations."""

    expenses = [int(line) for line in expense_input]

    for c in its.combinations(expenses, 3):
        if sum(c) == 2020:
            return c[0] * c[1] * c[2]
    raise ValueError("No combination of three expenses adds up to 2020")


first = first_combinations
second = second_combinations
