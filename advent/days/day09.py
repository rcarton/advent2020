from typing import Iterator
from itertools import combinations


def first(puzzle_input: Iterator[str]) -> int:
    numbers = [int(line.strip()) for line in puzzle_input]
    return find_first_invalid_num(numbers, 25)

def second(puzzle_input: Iterator[str]) -> int:
    return 0


def find_first_invalid_num(numbers: Iterator[int], preamble_size: int) -> int:
    last_numbers = []
    for i, num in enumerate(numbers):
        if i < preamble_size:
            last_numbers.append(num)
            continue
        
        if not is_valid(num, last_numbers):
            return num
        
        last_numbers.pop(0)
        last_numbers.append(num)


def is_valid(num, last_numbers):
    for comb in combinations(last_numbers, 2):
        if sum(comb) == num:
            return True
    return False

            