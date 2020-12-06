import re
from dataclasses import dataclass
from typing import Iterator, Optional


def first(entries: Iterator[str]) -> int:
    """Count the number of valid entries."""
    count = 0
    for entry in entries:
        if is_entry_valid_first(entry):
            count += 1

    return count


def second(entries: Iterator[str]) -> int:
    """Count the number of valid entries."""
    count = 0
    for entry in entries:
        if is_entry_valid_second(entry):
            count += 1

    return count


@dataclass
class PasswordPolicy:
    """This class represents a password policy."""

    first_value: int
    second_value: int
    letter: str


def parse_policy(policy_str: str) -> PasswordPolicy:
    """
    Parse the policy from a policy string.

    A policy string has the following format:

    <min count>-<max count> <letter>

    """
    m = re.match(
        r"(?P<first_value>\d+)-(?P<second_value>\d+) (?P<letter>[a-z])", policy_str
    )
    groups = m.groupdict()
    return PasswordPolicy(
        int(groups["first_value"]), int(groups["second_value"]), groups["letter"]
    )


def is_entry_valid_first(entry: str) -> bool:
    """Tests whether an entry is valid."""

    policy_str, password = entry.strip().split(": ")
    policy = parse_policy(policy_str)

    count = 0
    for letter in password:
        if letter == policy.letter:
            count += 1

    return policy.first_value <= count <= policy.second_value


def is_entry_valid_second(entry: str) -> bool:
    """Tests whether an entry is valid with the second password policy logic."""

    policy_str, password = entry.strip().split(": ")
    policy = parse_policy(policy_str)

    count_valid = 0
    if get_password_letter_safe(password, policy.first_value - 1) == policy.letter:
        count_valid += 1
    if get_password_letter_safe(password, policy.second_value - 1) == policy.letter:
        count_valid += 1

    return count_valid == 1


def get_password_letter_safe(password, index) -> Optional[str]:
    """Get the letter at the given index, or None if the index is invalid."""
    if index < 0 or index >= len(password):
        return None
    return password[index]
