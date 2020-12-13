from advent.days import day10

SHORT_EXAMPLE = """16
10
15
5
1
11
7
19
6
12
4""".splitlines(
    keepends=True
)


EXAMPLE = """28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3""".splitlines(
    keepends=True
)

EXAMPLE_AS_NUMS = [int(n.strip()) for n in EXAMPLE]


def test_find_jolt_diff_counts():
    twoj_diff = len(EXAMPLE_AS_NUMS) - 22 - 10 + 1
    assert day10.find_jolt_diff_counts(EXAMPLE_AS_NUMS) == [22, twoj_diff, 10]


def test_count_arrangements_short():
    adapters = [int(n.strip()) for n in SHORT_EXAMPLE]
    assert day10.count_arrangements(adapters) == 8


def test_count_arrangements():
    adapters = [int(n.strip()) for n in EXAMPLE]
    assert day10.count_arrangements(adapters) == 19208
