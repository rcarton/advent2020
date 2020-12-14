from advent.days import day11

EXAMPLE = """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL""".splitlines(
    keepends=True
)


def test_first():
    assert day11.first(EXAMPLE) == 37


def test_second():
    assert day11.second(EXAMPLE) == 26


def test_get_first_seat_in_direction():
    puzzle_input = """.............
.L.L.#.#.#.#.
.............""".splitlines(
        keepends=True
    )
    waiting_area = day11.WaitingArea.from_input(puzzle_input, False, 5)
    assert waiting_area.get_first_seat_in_direction(13, 0, 1) == day11.Cell.EMPTY
