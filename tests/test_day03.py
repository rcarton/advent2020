from advent.days.day03 import (
    Grid,
    Position,
    count_trees_in_slope,
    first,
    get_cell,
    get_grid,
    second,
)

EXAMPLE = """..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#""".splitlines()


def test_first() -> None:
    assert first(EXAMPLE) == 7


def test_second() -> None:
    assert second(EXAMPLE) == 336


def test_count_trees_in_slope() -> int:
    g = get_grid(EXAMPLE)
    assert count_trees_in_slope(g, 3, 1) == 7


def test_get_grid() -> None:
    s = "...\nXXX\nX.X\n..XX".splitlines()
    g = get_grid(s)

    assert g.data == list("...XXXX.X..XX")
    assert g.width == 3
    assert g.height == 4


def test_get_cell() -> None:
    p = Position(1, 2)
    g = Grid("..X.", 2, 2)

    assert get_cell(g, p) == "X"
