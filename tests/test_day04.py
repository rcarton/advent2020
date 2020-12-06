from advent.days.day04 import first, get_passports_from_input, second

EXAMPLE = """ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in""".splitlines(
    keepends=True
)


def test_first() -> None:
    assert first(EXAMPLE) == 2


def test_second() -> None:
    assert second(EXAMPLE) == 2


def test_get_passports_from_input() -> None:
    assert get_passports_from_input(EXAMPLE) == [
        "ecl:gry pid:860033327 eyr:2020 hcl:#fffffd byr:1937 iyr:2017 cid:147 hgt:183cm",
        "iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884 hcl:#cfa07d byr:1929",
        "hcl:#ae17e1 iyr:2013 eyr:2024 ecl:brn pid:760753108 byr:1931 hgt:179cm",
        "hcl:#cfa07d eyr:2025 pid:166559648 iyr:2011 ecl:brn hgt:59in",
    ]
