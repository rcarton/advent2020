import re
from typing import Any, Iterator, List, Tuple

REQUIRED_FIELDS = set(
    [
        "byr",
        "iyr",
        "eyr",
        "hgt",
        "hcl",
        "ecl",
        "pid",
        "cid",
    ]
)


def valid_hgt(value: str) -> bool:
    """
    hgt (Height) - a number followed by either cm or in:
    If cm, the number must be at least 150 and at most 193.
    If in, the number must be at least 59 and at most 76.
    """
    m = re.match(r"^(?P<measure>\d+)(?P<unit>cm|in)$", value)
    if not m:
        return False

    unit = m.group("unit")
    measure = int(m.group("measure"))
    if unit == "cm":
        return 150 <= measure <= 193
    return 59 <= measure <= 76


# List of rules for every password property
RULES = {
    "byr": lambda value: 1920 <= int(value) <= 2002,
    "iyr": lambda value: 2010 <= int(value) <= 2020,
    "eyr": lambda value: 2020 <= int(value) <= 2030,
    "hgt": valid_hgt,
    "hcl": lambda value: re.match(r"^#[0-9a-f]{6}$", value),
    "ecl": lambda value: re.match(r"^(amb|blu|brn|gry|grn|hzl|oth)$", value),
    "pid": lambda value: re.match(r"^[0-9]{9}$", value),
}


def first(passports_str: Iterator[str]) -> int:
    return sum(is_valid_first(p) for p in get_passports_from_input(passports_str))


def second(passports_str: Iterator[str]) -> int:
    return sum(is_valid_second(p) for p in get_passports_from_input(passports_str))


def is_valid_first(passport: str) -> bool:
    fields = {f[0] for f in get_fields(passport)}

    # A passport is valid if it has all the required fields
    # or if the only missing field is `cid`
    missing_fields = REQUIRED_FIELDS - fields

    return len(missing_fields) == 0 or missing_fields == {
        "cid",
    }


def is_valid_second(passport: str) -> bool:
    fields = get_fields(passport)
    fields_found = {f[0] for f in get_fields(passport)}

    missing_fields = REQUIRED_FIELDS - fields_found

    # If required fields are missing, the passport is invalid
    if not (
        len(missing_fields) == 0
        or missing_fields
        == {
            "cid",
        }
    ):
        return False

    # Fields without rules are ok
    def valid_fn(_: Any):
        return True

    # Validate the rules for every field
    for field, value in fields:
        validation_fn = RULES.get(field, valid_fn)
        if not validation_fn(value):
            # print(f'{passport} Rule {field}={value} failed')
            return False
    return True


def get_passports_from_input(passports_dirty: List[str]) -> List[str]:
    """
    The input data is separated by empty lines, this method returns a list
    of passports represented as single line strings.
    """
    passports = []
    passport = ""
    for line in passports_dirty:
        line = line.strip()
        if not line:
            if passport:
                passports.append(passport.strip())
                passport = ""
        else:
            passport += " " + line

    # Add the last one
    if passport:
        passports.append(passport.strip())

    return passports


def get_fields(passport: str) -> List[Tuple[str, str]]:
    """Extract the fields from a passport string"""
    fields_str = passport.strip().split(" ")
    fields = []
    for field_str in fields_str:
        # Skip empty fields
        if not field_str:
            continue
        field, value = field_str.split(":")
        fields.append((field, value))

    return fields
