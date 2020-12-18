import pytest

from advent.days import day14

EXAMPLE = """mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0""".splitlines(
    keepends=True
)


EXAMPLE_2 = """mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1""".splitlines(
    keepends=True
)


def test_first():
    assert day14.first(EXAMPLE) == 165


def test_second():
    assert day14.second(EXAMPLE_2) == 208


def test_runner_mask():
    mask = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X"
    runner = day14.DockingProgramRunner([])

    runner.instr_update_mask(mask)

    assert runner.mask_0s == day14.binstr_to_int(mask.replace("X", "1"))
    assert runner.mask_1s == day14.binstr_to_int(mask.replace("X", "0"))

    assert runner.apply_mask(11) == 73
    assert runner.apply_mask(101) == 101
    assert runner.apply_mask(0) == 64


def test_get_v2_masked_values():
    address = 42
    mask = "000000000000000000000000000000X1001X"

    expected = set([26, 27, 58, 59])

    runner = day14.DockingProgramRunner([], version=2)
    runner.instr_update_mask(mask)

    assert set(runner.get_v2_masked_values(address)) == expected


@pytest.mark.parametrize(
    "num_str, bit_value, bit_position, expected",
    [
        ("010", 1, 0, "011"),
        ("110", 0, 2, "010"),
        ("1000000", 1, 2, "1000100"),
    ],
)
def test_overwrite_bit(num_str, bit_value, bit_position, expected):
    num = day14.binstr_to_int(num_str)
    assert str(bin(day14.overwrite_bit(num, bit_value, bit_position))) == str(
        bin(day14.binstr_to_int(expected))
    )
