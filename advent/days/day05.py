from typing import Iterator
from dataclasses import dataclass

# 0 -> 127
PLANE_ROWS = 128

# 0 -> 8
PLANE_COLUMNS = 8


@dataclass
class Seat:
    seat_id: int
    row: int
    column: int

    @classmethod
    def parse_boarding_pass(cls, boarding_pass: str):
        assert len(boarding_pass) == 10

        row_data = boarding_pass[:7]
        col_data = boarding_pass[7:]

        row = binary_partition_number(row_data, PLANE_ROWS)
        col = binary_partition_number(col_data, PLANE_COLUMNS)

        return cls(seat_id=row * 8 + col, row=row, column=col)


def first(puzzle_input: Iterator[str]) -> int:
    return max(Seat.parse_boarding_pass(b.strip()).seat_id for b in puzzle_input)


def second(puzzle_input: Iterator[str]) -> int:
    seat_ids = sorted(Seat.parse_boarding_pass(b.strip()).seat_id for b in puzzle_input)
    for i in range(1, len(seat_ids)):
        if seat_ids[i - 1] + 2 == seat_ids[i]:
            return seat_ids[i - 1] + 1

    raise ValueError("Boarding pass not found")


def binary_partition_number(pos_str: str, num: int) -> int:
    """
    Return the position described by the position string.

    Position must be a string like 'LRL' or 'FBFB'.
    The input string length must be log2(n).
    """
    pos = 0
    for lrfb in pos_str:
        if lrfb in ("R", "B"):
            pos += num / 2
        num /= 2
    return int(pos)
