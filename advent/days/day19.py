import re
from dataclasses import dataclass
from typing import Dict, Iterator, Optional, Pattern


@dataclass
class Rule:
    raw: str
    expanded: Optional[str] = None
    compiled: Optional[Pattern] = None
    compiled_with_rec: Optional[Pattern] = None

    def match(self, rules, s: str) -> bool:
        if not s:
            return False
        m = self.compiled.match(s)

        if m:
            return True

        if self.compiled_with_rec is None:
            return False
        m = self.compiled_with_rec.match(s)

        if not m:
            return False

        groups = m.groupdict()
        if all(group is None for group in groups.values()):
            # No recursive group matches
            return False

        # What if r8 matches, but then it's invalid BUT there was also a match without the group?
        # Should we test without the group then?

        # import pdb
        # pdb.set_trace()
        return any(rules[k[1:]].match(rules, v) for k, v in groups.items())


def expand_rule(rules: Dict[int, Rule], rule_num: str):
    rule = rules[rule_num]
    if rule.expanded is not None:
        return

    rule_indices = re.findall("[0-9]+", rule.raw)

    # Make sure all the rules are expanded
    # Apply in descending order to avoid '1' being applied to 101
    rule.expanded = rule.raw
    for rule_i in sorted(rule_indices, key=int, reverse=True):
        if rule_i == rule_num:
            replacement = f"(?P<r{rule_num}>.+)"
        else:
            expand_rule(rules, rule_i)
            replacement = (
                f"(?:{rules[rule_i].expanded})"
                if rules[rule_i].expanded.find("|") >= 0
                else rules[rule_i].expanded
            )
        rule.expanded = rule.expanded.replace(rule_i, replacement)

    rule.expanded = rule.expanded.replace(" ", "")
    rule.compiled = re.compile(fr"^{rule.expanded.replace('.+', 'XXXX')}$")
    rule.compiled_with_rec = re.compile(fr"^{rule.expanded}$")


def parse_rules(puzzle_input: Iterator[str]) -> Dict[str, Rule]:
    rules = {}

    # Parse the rules
    line = next(puzzle_input).strip()

    while line:
        rule_num, rule_str = line.split(":")

        rules[rule_num] = Rule(raw=rule_str.strip(), expanded=None)
        m = re.match(r'^"(?P<letter>[a-z])"$', rules[rule_num].raw)
        if m:
            rules[rule_num].expanded = m.group("letter")

        line = next(puzzle_input).strip()
    return rules


def first(puzzle_input: Iterator[str]) -> int:

    rules = parse_rules(puzzle_input)
    messages = [line.strip() for line in puzzle_input]

    # Now that we're done parsing, expand the rules to have a regex for each
    rule = rules["0"]
    expand_rule(rules, "0")

    return sum(1 for message in messages if re.match(fr"^{rule.expanded}$", message))


def second(puzzle_input: Iterator[str]) -> int:
    """403 is no bueno."""

    rules = parse_rules(puzzle_input)
    messages = [line.strip() for line in puzzle_input]

    # A bit of a hack but I got tired of debugging my homemade implementation of a recursive
    # regex
    rules["8"].raw = "42 +"
    rules["11"].raw = "42 (?: 42 (?: 42 (?: 42 31 )? 31 )? 31 )? 31"

    # Now that we're done parsing, expand the rules to have a regex for each
    rule = rules["0"]
    expand_rule(rules, "0")
    print(f"{rule}")
    print(f"{rules['8']}")
    print(f"{rules['11']}")

    return sum(1 for message in messages if rule.match(rules, message))
