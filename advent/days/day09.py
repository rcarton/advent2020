from itertools import combinations
from typing import Iterator, List


def first(puzzle_input: Iterator[str]) -> int:
    numbers = [int(line.strip()) for line in puzzle_input]
    return find_first_invalid_num(numbers, 25)


def second(puzzle_input: Iterator[str]) -> int:
    numbers = [int(line.strip()) for line in puzzle_input]
    first_invalid_num = find_first_invalid_num(numbers, 25)
    contiguous_numbers = find_contiguous_sum_to(numbers, first_invalid_num)
    return min(contiguous_numbers) + max(contiguous_numbers)


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

    raise ValueError("No invalid number found.")


def is_valid(num, last_numbers):
    for comb in combinations(last_numbers, 2):
        if sum(comb) == num:
            return True
    return False


def find_contiguous_sum_to(numbers: Iterator[int], target: int) -> List[int]:
    """Find a list of at least 2 contiguous numbers that add up to target."""

    for i in range(len(numbers) - 1):
        curr_sum = numbers[i]
        j = i + 1
        while j < len(numbers) and curr_sum < target:
            curr_sum += numbers[j]
            j += 1

            if curr_sum == target:
                return numbers[i:j]

    raise ValueError("Target value not found in a contiguous sum.")
