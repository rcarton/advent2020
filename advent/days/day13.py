from typing import Iterator, Tuple, List


def first(puzzle_input: Iterator[str]) -> int:
    arrival_t, frequencies = parse_input(puzzle_input)

    # Remove the x's and cast to ints
    frequencies = [int(f) for f in frequencies if f != 'x']

    # For each bus find the smallest departure time >= arrival_t
    min_dep_times = [arrival_t if arrival_t %
                     f == 0 else ((arrival_t//f)+1) * f for f in frequencies]

    bus_id, departure_t = min(
        zip(frequencies, min_dep_times), key=lambda dt: dt[1])

    return (departure_t - arrival_t) * bus_id


def second(puzzle_input: Iterator[str]) -> int:

    _, frequencies = parse_input(puzzle_input)

    # Remove the x's and cast to ints
    frequencies = [int(f) if f != 'x' else 0 for f in frequencies]

    # 4 (bus id 59)
    largest_index, _ = max(enumerate(frequencies), key=lambda f: f[1])

    # List of tuples with the frequency and the time difference with the largest index
    # [(7, -4), (13, -3), (59, 0), (31, 2), (19, 3)]
    frequencies_with_delta = [(f, i - largest_index)
                              for i, f in enumerate(frequencies) if f]

    # Sort the bus ids by largest first
    sorted_fdelta = sorted(frequencies_with_delta,
                           key=lambda fwd: fwd[0], reverse=True)

    # This literally can't go wrong
    n = 1
    to_test = sorted_fdelta[1:]
    while True:
        if n % 1000000 == 0:
            print(n*sorted_fdelta[0][0])
        t = n * sorted_fdelta[0][0]
        if all((t + delta) % f == 0 for f, delta in to_test):
            break
        n += 1

    # The t we have includes the time delta to the largest (for ex. 4 minutes for 59)
    return t + frequencies_with_delta[0][1]

# https://math.stackexchange.com/questions/2218763/how-to-find-lcm-of-two-numbers-when-one-starts-with-an-offset


def parse_input(puzzle_input: Iterator[str]) -> Tuple[int, List[str]]:
    lines = [l.strip() for l in puzzle_input]
    return (
        int(lines[0]),
        [n for n in lines[1].split(',')]
    )
