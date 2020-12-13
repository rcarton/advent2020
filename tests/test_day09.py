from advent.days import day09

EXAMPLE = """35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576""".splitlines(
    keepends=True
)


def test_find_first_invalid_num():
    assert day09.find_first_invalid_num([int(num.strip()) for num in EXAMPLE], 5) == 127


def test_find_contiguous_sum_to():
    assert day09.find_contiguous_sum_to([int(num.strip()) for num in EXAMPLE], 127) == [
        15,
        25,
        47,
        40,
    ]
