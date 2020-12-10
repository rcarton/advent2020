import re
from dataclasses import dataclass
from functools import lru_cache
from typing import Dict, Iterator, List, Tuple

ParsedInput = List[Tuple[str, List[Tuple[int, str]]]]


@dataclass
class BagRule:
    color: str
    can_be_contained_by: List[str]
    must_contain: List[Tuple[int, str]]


def first(puzzle_input: Iterator[str]) -> int:

    parsed_input = parse_input(puzzle_input)
    rules = make_rules(parsed_input)

    target_color = "shiny gold"

    # Find all possible colors that can contain a shiny gold bag
    # by traversing the graph until the bags can't be contained
    # In practice this subgraph is a tree, with the target color as
    # root and the outer # container bags as leaves.
    # All the intermediate nodes are potential containers
    found = set()
    to_explore = [target_color]
    while to_explore:
        # Since we pop the first, and append it's a BFS
        current = rules[to_explore.pop(0)]

        found.add(current.color)
        if not current.can_be_contained_by:
            # This is a leaf
            continue

        # Not a leaf, add the containers to the list to explore
        for color in current.can_be_contained_by:
            # Since we're appending to the ending and pop'ing from
            # the beginning, that's a BFS
            to_explore.append(color)

    found.remove(target_color)

    return len(found)


def second(puzzle_input: Iterator[str]) -> int:
    parsed_input = parse_input(puzzle_input)
    rules = make_rules(parsed_input)

    @lru_cache
    def total_contained(color: str) -> int:
        return sum(
            count + count * total_contained(c) for count, c in rules[color].must_contain
        )

    return total_contained("shiny gold")


def make_rules(parsed_input: ParsedInput) -> Dict[str, BagRule]:
    """
    Make the set of bag rules.

    The rules are indexed by the bag color, it's a graph of the bag
    relationships where the edges are either 'can be contained by'
    or 'must contain', the latter being the actual rule, while the
    former makes it easy to navigate towards an outer container.
    """

    rules = {}
    for container, containees in parsed_input:
        if rules.get(container, None) is None:
            rules[container] = BagRule(container, [], [])

        for count, containee in containees:
            rules[container].must_contain.append((count, containee))
            if rules.get(containee, None) is None:
                rules[containee] = BagRule(containee, [], [])
            rules[containee].can_be_contained_by.append(container)

    return rules


def parse_input(puzzle_input: Iterator[str]) -> ParsedInput:
    """This method parses the input into a list of tuples."""

    parsed = []
    for line in puzzle_input:
        line = line.strip()
        if not line:
            continue
        # shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags
        m = re.match(r"^(?P<container>.*?) bags contain (?P<contained>.*?)\.$", line)

        if not m:
            raise ValueError(f"Unable to parse line '{line}'")

        # 1 dark olive bag, 2 vibrant plum bags
        bag_counts = re.findall(r"\d.*?bag", m.group("contained"))
        contained_bags = [get_count_and_color(bag_match) for bag_match in bag_counts]

        parsed.append((m.group("container"), contained_bags))
    return parsed


def get_count_and_color(bag_match: str) -> Tuple[int, str]:
    # 5 faded blue bag
    m = re.match(r"^(?P<count>\d+) (?P<color>.*) bags?$", bag_match)
    if not m:
        raise ValueError(f"Unable to parse bag '{bag_match}'")
    return (int(m.group("count")), m.group("color"))
