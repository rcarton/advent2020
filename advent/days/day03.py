from dataclasses import dataclass
from typing import Iterator, List


@dataclass
class Position:
    row: int
    column: int


@dataclass
class Grid:
    """
    I'm going with a more functional representation as opposed to making the grid an object,
    although in this case it would work well with an OO approach too 🤷‍♂️.
    """

    data: List[str]
    width: int
    height: int


def first(grid_str: Iterator[str]) -> int:
    return count_trees_in_slope(get_grid(grid_str), 3, 1)


def second(grid_str: Iterator[str]) -> int:
    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]

    g = get_grid(grid_str)
    total = 1
    for right, down in slopes:
        total *= count_trees_in_slope(g, right, down)

    return total


def count_trees_in_slope(g: Grid, right: int, down: int) -> int:
    """Count the number of trees encountered with a given slope."""

    p = Position(0, 0)

    def is_tree(pt):
        return get_cell(g, pt) == "#"

    tree_count = 0
    while p.row < g.height:
        if is_tree(p):
            tree_count += 1
        p.column += right
        p.row += down

    return tree_count


def get_grid(grid_str: Iterator[str]) -> Grid:
    """Get a grid from a grid representation."""

    data = []
    width = None
    height = 0
    for row in grid_str:
        row = row.strip()
        if width is None:
            width = len(row)
        data.extend(row)
        height += 1

    return Grid(data, width, height)


def get_cell(grid: Grid, p: Position) -> str:
    """
    Get the value of the cell at position row, col.

    0,0 is the cell in the top left corner.
    """

    if p.row >= grid.height:
        raise ValueError("Row outside of the grid")

    row = p.row
    col = p.column % grid.width

    index = row * grid.width + col
    return grid.data[index]
