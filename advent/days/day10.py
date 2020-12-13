from typing import Iterator, List


def first(puzzle_input: Iterator[str]) -> int:
    counts = find_jolt_diff_counts(int(n.strip()) for n in puzzle_input)
    return counts[0] * counts[2]


def second(puzzle_input: Iterator[str]) -> int:
    return count_arrangements(int(n.strip()) for n in puzzle_input)


def find_jolt_diff_counts(adapters: List[int]) -> List[int]:
    """Get the count of jolt differences (1, 2, 3) when using all the adapters."""
    nums = sorted(adapters)
    counts = [0, 0, 0]
    curr_j = 0

    for n in nums:
        diff = n - curr_j

        if diff > 3:
            raise ValueError(f"No valid adapter found for joltage {curr_j}")

        counts[diff - 1] += 1
        curr_j = n

    # The device's joltage is 3j more than the last adapter
    counts[2] += 1

    return counts


def count_arrangements(adapters: List[int]) -> int:
    """
    Find all arrangements.

    For adapter value n, the number of arrangements

    """

    nums = sorted(adapters)

    count1 = 0
    count2 = 0
    count3 = 0

    # n is the joltage for count3, there are count3 ways to arrange adapters to have a joltage of n
    n = 0

    for curr in nums:
        # print(f'curr={curr} n={n} counts=[{count1}, {count2}, {count3}]')
        while n < curr - 1:
            n += 1
            # shift to the left
            count1 = count2
            count2 = count3
            count3 = 0
        tmp = count1 + count2 + count3
        count1 = count2
        count2 = count3
        count3 = tmp

        if curr <= 3:
            count3 += 1

        n = curr
        # print(f'curr={curr} n={n} counts=[{count1}, {count2}, {count3}]')

    return count3
