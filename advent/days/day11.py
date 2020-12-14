from dataclasses import dataclass
from enum import Enum
from typing import Iterator, List, Optional


class Cell(Enum):
    EMPTY = 0
    OCCUPIED = 1
    FLOOR = 2

    @staticmethod
    def from_str(s: str):
        if s == ".":
            return Cell.FLOOR
        if s == "L":
            return Cell.EMPTY
        return Cell.OCCUPIED

    def __str__(self):
        if self == Cell.FLOOR:
            return "."
        if self == Cell.EMPTY:
            return "L"
        return "#"


@dataclass
class WaitingArea:
    width: int
    height: int
    grid: List[Cell]

    # Question specific parameters
    see_only_immediate: bool
    busy_count: int

    def step(self) -> None:
        """Update the waiting area after applying the rules once"""

        changes = []

        for n, cell in enumerate(self.grid):
            occupied_neighbors = self.count_occupied_neighbors(n)
            if cell == Cell.EMPTY and occupied_neighbors == 0:
                changes.append((n, Cell.OCCUPIED))
            elif cell == Cell.OCCUPIED and occupied_neighbors >= self.busy_count:
                changes.append((n, Cell.EMPTY))

        # Apply the changes
        for n, cell in changes:
            self.grid[n] = cell

        return len(changes)

    def get_cell(self, row: int, column: int) -> Optional[Cell]:
        """Get the content of a cell at a given row and column"""

        if 0 <= row < self.height and 0 <= column < self.width:
            return self.grid[row * self.width + column]

        return None

    def get_first_seat_in_direction(
        self, n: int, row_delta: int, column_delta: int
    ) -> Optional[Cell]:
        """Get the first seat seen in a given direction

        A direction is represented by row_delta, column_delta.

        For example the "top left" direction is:
            - row_delta = -1
            - column_delta = -1

        """

        row = n // self.width
        column = n % self.width

        row += row_delta
        column += column_delta
        cell = self.get_cell(row, column)

        while not self.see_only_immediate and cell is not None:
            if cell != Cell.FLOOR:
                break

            # If the cell is floor, we keep looking
            row += row_delta
            column += column_delta
            cell = self.get_cell(row, column)

        return cell

    def count_occupied_neighbors(self, n: int) -> int:
        neighbors = [
            self.get_first_seat_in_direction(n, -1, -1),
            self.get_first_seat_in_direction(n, -1, 0),
            self.get_first_seat_in_direction(n, -1, 1),
            self.get_first_seat_in_direction(n, 0, -1),
            self.get_first_seat_in_direction(n, 0, 1),
            self.get_first_seat_in_direction(n, 1, -1),
            self.get_first_seat_in_direction(n, 1, 0),
            self.get_first_seat_in_direction(n, 1, 1),
        ]

        return sum(1 for c in neighbors if c == Cell.OCCUPIED)

    @classmethod
    def from_input(
        cls, waiting_area_str: Iterator[str], see_only_immediate: bool, busy_count: int
    ):
        height = 0
        grid = []

        for line in waiting_area_str:
            line = line.strip()
            height += 1
            width = len(line)
            grid += [Cell.from_str(position) for position in line]

        return cls(width, height, grid, see_only_immediate, busy_count)

    def __repr__(self):
        """Return a printable string representing the status of the waiting area"""
        grid_s = [str(c) for c in self.grid]

        return "\n".join(
            "".join(grid_s[self.width * row : self.width * row + self.width])
            for row in range(self.height)
        )


def first(puzzle_input: Iterator[str]) -> int:
    waiting_area = WaitingArea.from_input(puzzle_input, True, 4)

    has_changes = True
    while has_changes:
        has_changes = waiting_area.step() > 0

    # Count the number of occupied seats
    return sum(1 for cell in waiting_area.grid if cell == Cell.OCCUPIED)


def second(puzzle_input: Iterator[str]) -> int:
    waiting_area = WaitingArea.from_input(puzzle_input, False, 5)

    has_changes = True
    while has_changes:
        has_changes = waiting_area.step() > 0

    # Count the number of occupied seats
    return sum(1 for cell in waiting_area.grid if cell == Cell.OCCUPIED)
