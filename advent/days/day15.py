from collections import defaultdict
from typing import Iterator, List


def number_spoken(starting_numbers: List[int], target_n: int) -> int:
    """
    See rules in the online prompt

    At every turn a number is spoken which is the number of turns since
    the last spoken numbers was said and the time before that.

    Really, see the rules, it's a little too convoluted to explain.
    """
    spoken = defaultdict(lambda: (None, None))

    # Initial numbers
    for k, num in enumerate(starting_numbers):
        spoken[num] = (k + 1, None)

    count = len(starting_numbers)
    last_spoken = starting_numbers[-1]

    while count < target_n:
        count += 1

        last_time, time_before_that = spoken.get(last_spoken)
        if last_time is None or time_before_that is None:
            current = 0
        else:
            current = last_time - time_before_that

        spoken[current] = (count, spoken[current][0])

        last_spoken = current

    return last_spoken


def first(puzzle_input: Iterator[str]) -> int:
    starting_numbers = [int(n) for n in list(puzzle_input)[0].strip().split(",")]

    return number_spoken(starting_numbers, 2020)


def second(puzzle_input: Iterator[str]) -> int:
    starting_numbers = [int(n) for n in list(puzzle_input)[0].strip().split(",")]

    return number_spoken(starting_numbers, 30000000)
