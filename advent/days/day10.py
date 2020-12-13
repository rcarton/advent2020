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
    Count all the arrangements

    This is a dynamic programming solution, as the count of possible arrangements
    for an adapter of value n, is the sum of the counts for the values: n-1, n-2, n-3.
    """

    nums = sorted(adapters)

    # We could keep an array of counts for all the possible values so far, but this is more
    # memory efficient as we only ever need to keep the values for the previous three joltages
    count1 = 0
    count2 = 0
    count3 = 0

    # n is the joltage for count3, there are count3 ways to arrange adapters to have a joltage of n
    n = 0

    for curr in nums:
        # Some adapter values are missing, so we shift the counts until our shifted values
        # are right before our desired joltage
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

        # For joltages under 3, you can use the adapter directly
        if curr <= 3:
            count3 += 1

        n = curr

    return count3
