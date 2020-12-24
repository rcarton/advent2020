import pytest

from advent.days.day20 import (find_corners, first, flip, is_there_a_monster,
                               make_image, parse_input, rotate, second,
                               solve_image)

EXAMPLE = """Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###...""".splitlines(
    keepends=True
)


def test_rotate():
    assert rotate(["ABC", "DEF", "GHI"]) == ["GDA", "HEB", "IFC"]


def test_flip():
    assert flip(["ABC", "DEF", "GHI"]) == ["CBA", "FED", "IHG"]


def test_parse_input():
    assert len(parse_input(iter(EXAMPLE))) == 9


def test_first():
    assert first(iter(EXAMPLE)) == 20899048083289


def test_find_corners():
    tiles = parse_input(iter(EXAMPLE))
    assert find_corners(tiles) == {3079, 1171, 2971, 1951}


EXPECTED_IMAGE = """.#.#..#.##...#.##..#####
###....#.#....#..#......
##.##.###.#.#..######...
###.#####...#.#####.#..#
##.#....#.##.####...#.##
...########.#....#####.#
....#..#...##..#.#.###..
.####...#..#.....#......
#..#.##..#..###.#.##....
#.####..#.####.#.#.###..
###.#.#...#.######.#..##
#.####....##..########.#
##..##.#...#...#.#.#.#..
...#..#..#.#.##..###.###
.#.#....#.##.#...###.##.
###.#...#..#.##.######..
.#.#.###.##.##.#..#.##..
.####.###.#...###.#..#.#
..#.#..#..#.#.#.####.###
#..####...#.#.#.###.###.
#####..#####...###....##
#.##..#..#...#..####...#
.#.###..##..##..####.##.
...###...##...#...#..###""".splitlines()


def test_make_image():
    tiles = parse_input(EXAMPLE)
    solution = solve_image(tiles)
    assert make_image(solution) == flip(EXPECTED_IMAGE)


@pytest.mark.parametrize(
    "row, column, expected",
    [
        (2, 2, True),
        (16, 1, True),
        (0, 0, False),
    ],
)
def test_is_there_a_monster(row, column, expected):
    # This matches the image in the example where the monster is found
    image_with_monsters = flip(rotate(EXPECTED_IMAGE))

    assert is_there_a_monster(image_with_monsters, row, column) == expected


def test_second():
    assert second(EXAMPLE) == 273
