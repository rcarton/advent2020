import math
import re
from dataclasses import dataclass
from typing import Iterator, List, Tuple


@dataclass(eq=True, frozen=True)
class FieldRule:
    """A rule for a field in a ticket"""

    name: str
    low_range: Tuple[int, int]
    high_range: Tuple[int, int]

    def validate(self, num: int) -> bool:
        """Tests whether a number is valid against the rule"""
        return (
            self.low_range[0] <= num <= self.low_range[1]
            or self.high_range[0] <= num <= self.high_range[1]
        )

    def __repr__(self):
        return f"{self.name} [{self.low_range}, {self.high_range}]"


Ticket = List[int]


def parse_rule(rule_str: str) -> FieldRule:
    """
    Parse a string rule into a FieldRule object

    Sample rule: 'departure time: 48-702 or 719-955'
    """

    m = re.match(r"^(?P<name>[a-z ]+): (?P<ranges>.*)$", rule_str)
    if not m:
        raise ValueError(f"Error parsing rule={rule_str}")

    name = m.group("name")
    low_low, low_high, high_low, high_high = re.findall(
        r"(\d+)", m.group("ranges"))

    return FieldRule(
        name=name,
        low_range=(int(low_low), int(low_high)),
        high_range=(int(high_low), int(high_high)),
    )


def parse_ticket(ticket_str: str) -> Ticket:
    """Parse a ticket"""
    return [int(n) for n in ticket_str.split(",")]


def parse_input(
    puzzle_input: Iterator[str],
) -> Tuple[List[FieldRule], Ticket, List[Ticket]]:
    """Parse the input into: (rules, my_ticket, nearby_tickets)"""

    rules = []

    # My version of black doesn't seem to support the assignment operator (:=)
    line = next(puzzle_input).strip()
    while line:
        rules.append(parse_rule(line))
        line = next(puzzle_input).strip()

    # Done with rules, skip 'your ticket'
    next(puzzle_input)

    # Parse my ticket
    my_ticket = parse_ticket(next(puzzle_input).strip())

    # Skip the empty line and 'nearby tickets'
    next(puzzle_input)
    next(puzzle_input)

    # Parse nearby tickets, that's the rest of the puzzle input
    nearby_tickets = [parse_ticket(line.strip()) for line in puzzle_input]

    return (rules, my_ticket, nearby_tickets)


def find_rules_for_tickets(
    tickets: List[Ticket], rules: List[FieldRule]
) -> List[FieldRule]:
    """
    Go through all the ticket values and eliminate candidate rules for every field
    in the ticket until there is a single matching rule.

    There is a trick when eliminating a rule: if the rule that was eliminated results
    in the field only having a single valid rule, then this rule must be eliminated
    from all the other fields.
    """
    candidate_rules = [set(rules) for _ in range(len(tickets[0]))]

    def remove_rule(rule, candidate_rules_i):
        if rule not in candidate_rules_i:
            return
        candidate_rules_i.remove(rule)

        # It's now the last rule, which means it can't be the rule for others
        if len(candidate_rules_i) == 1:
            rule_to_remove = next(iter(candidate_rules_i))
            for cri in candidate_rules:
                if cri is candidate_rules_i:
                    continue
                remove_rule(rule_to_remove, cri)

    # For every rule of every ticket validate it against the set of rules
    # Eventually candidate_rules should only contain single element sets
    for ticket in tickets:

        # Escape hatch if we've found all the rules
        if all(len(cr) == 1 for cr in candidate_rules):
            # We found the only valid rule for every position
            break

        for i, value in enumerate(ticket):
            for rule in list(candidate_rules[i]):
                # Every time a rule is broken at a give i, it is no longer a candidate
                # we won't have to check it again for this i
                if not rule.validate(value):
                    remove_rule(rule, candidate_rules[i])

    # Sanity check
    if not all(len(cr) == 1 for cr in candidate_rules):
        raise ValueError(
            "Could not find a single matching rule for every field in the tickets."
        )

    return [next(iter(candidates)) for candidates in candidate_rules]


def first(puzzle_input: Iterator[str]) -> int:
    rules, _, nearby_tickets = parse_input(puzzle_input)

    # Flatten all the ticket fields since we're considering them individually
    flattened_ticket_values: List[int] = []
    for ticket_values in nearby_tickets:
        flattened_ticket_values += ticket_values

    return sum(
        n for n in flattened_ticket_values if not any(r.validate(n) for r in rules)
    )


def second(puzzle_input: Iterator[str]) -> int:
    rules, my_ticket, nearby_tickets = parse_input(puzzle_input)

    def is_valid_ticket(ticket):
        return all(any(r.validate(num) for r in rules) for num in ticket)

    # Remove invalid tickets
    valid_tickets = [
        ticket for ticket in nearby_tickets if is_valid_ticket(ticket)]

    # Identify the rule that applies to every field
    rules_per_field = find_rules_for_tickets(valid_tickets, rules)

    # Find 'departure' rules indices
    departure_fields = set(
        i for i, rule in enumerate(rules_per_field) if rule.name.startswith("departure")
    )

    # Keep only departure field values
    my_ticket_departure_values = [
        value for i, value in enumerate(my_ticket) if i in departure_fields
    ]

    return math.prod(my_ticket_departure_values)
