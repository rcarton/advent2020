from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, Iterator, List


@dataclass
class Group:
    answers: Dict[str, int]
    people_count: int


def parse_input(puzzle_input: Iterator[str]) -> List[Group]:
    """Get the count of answers per group."""

    groups = []

    people_count = 0
    answers = defaultdict(lambda: 0)
    for line in puzzle_input:
        line = line.strip()

        if not line:
            groups.append(Group(answers, people_count))
            # Reset
            answers = defaultdict(lambda: 0)
            people_count = 0
            continue

        people_count += 1
        for question in line:
            answers[question] += 1

    # Add the last group if needed
    if people_count:
        groups.append(Group(answers, people_count))

    return groups


def first(puzzle_input: Iterator[str]) -> int:
    return sum(len(g.answers.keys()) for g in parse_input(puzzle_input))


def second(puzzle_input: Iterator[str]) -> int:
    total = 0
    for group in parse_input(puzzle_input):
        for answer_count in group.answers.values():
            if answer_count == group.people_count:
                total += 1

    return total
