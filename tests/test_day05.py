import pytest

from advent.days.day05 import Seat, binary_partition_number, first


@pytest.mark.parametrize(
    "pos_str, size, expected",
    [
        ("LLL", 8, 0),
        ("RRR", 8, 7),
        ("BFFFBBF", 128, 70),
    ],
)
def test_binary_partition_number(pos_str, size, expected):
    assert binary_partition_number(pos_str, size) == expected


@pytest.mark.parametrize(
    "boarding_pass, row, column, seat_id",
    [
        ("BFFFBBFRRR", 70, 7, 567),
        ("FFFBBBFRRR", 14, 7, 119),
        ("BBFFBBFRLL", 102, 4, 820),
    ],
)
def test_seat_parse_boarding_pass(boarding_pass, row, column, seat_id):
    assert Seat.parse_boarding_pass(boarding_pass) == Seat(
        row=row, column=column, seat_id=seat_id
    )


EXAMPLE = """BFFFBBFRRR
BBFFBBFRLL
FFFBBBFRRR
""".splitlines(
    keepends=True
)


def test_first():
    assert first(EXAMPLE) == 820
