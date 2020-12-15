from typing import Iterator, List, Tuple


def first(puzzle_input: Iterator[str]) -> int:
    arrival_t, frequencies = parse_input(puzzle_input)

    # Remove the x's and cast to ints
    frequencies = [int(f) for f in frequencies if f != "x"]

    # For each bus find the smallest departure time >= arrival_t
    min_dep_times = [
        arrival_t if arrival_t % f == 0 else ((arrival_t // f) + 1) * f
        for f in frequencies
    ]

    bus_id, departure_t = min(zip(frequencies, min_dep_times), key=lambda dt: dt[1])

    return (departure_t - arrival_t) * bus_id


def second_brute(puzzle_input: Iterator[str]) -> int:

    _, frequencies = parse_input(puzzle_input)

    # Remove the x's and cast to ints
    frequencies = [int(f) if f != "x" else 0 for f in frequencies]

    # 4 (bus id 59)
    largest_index, _ = max(enumerate(frequencies), key=lambda f: f[1])

    # List of tuples with the frequency and the time difference with the largest index
    # [(7, -4), (13, -3), (59, 0), (31, 2), (19, 3)]
    frequencies_with_delta = [
        (f, i - largest_index) for i, f in enumerate(frequencies) if f
    ]

    # Sort the bus ids by largest first
    sorted_fdelta = sorted(frequencies_with_delta, key=lambda fwd: fwd[0], reverse=True)

    # This literally can't go wrong
    n = 1
    to_test = sorted_fdelta[1:]
    while True:
        if n % 1000000 == 0:
            print(n * sorted_fdelta[0][0])
        t = n * sorted_fdelta[0][0]
        if all((t + delta) % f == 0 for f, delta in to_test):
            break
        n += 1

    # The t we have includes the time delta to the largest (for ex. 4 minutes for 59)
    return t + frequencies_with_delta[0][1]


def crt_progression(x, p) -> int:
    n = 0
    while True:
        yield x + n * p
        n += 1


def second_crt(puzzle_input: Iterator[str]) -> int:

    _, frequencies = parse_input(puzzle_input)

    # Remove the x's and cast to ints
    frequencies = [int(f) if f != "x" else 0 for f in frequencies]

    # List of tuples with the frequency and the time difference with the largest index
    # [(7, 0), (13, 1), (59, 4), (31, 6), (19, 7)]
    frequencies_with_delta = [(f, i) for i, f in enumerate(frequencies) if f]

    # Sort the bus ids by largest first
    sorted_fdelta = sorted(frequencies_with_delta, key=lambda fwd: fwd[0], reverse=True)

    # Number theory, not something I knew, so I got stuck on the brute force solution
    # https://en.wikipedia.org/wiki/Chinese_remainder_theorem#Search_by_sieving

    sorted_fdelta = [(n, a if n > a else a % n) for n, a in sorted_fdelta]
    p, x = sorted_fdelta[0]
    for n, a in sorted_fdelta[1:]:
        for possible in crt_progression(x, p):
            if possible % n == a:
                x = possible
                p *= n
                break

    # If the frequencies are denoted n0 -> nm, with m the number of bus lines (including the x's)
    # and the offset is a0 -> am for each bus (corresponding to its position)
    # Then the chinese number theorem allows us to find x that satisfies x % nm = am
    # x is also the smallest number < N, where N = n0*n1*..*nm

    # In the cases of our buses, they will all depart at the same time at time t=0 and then
    # the next time they all depart at the same time is time tN=lcm(n0,n1,...,nm)=n0*n1*...*nm
    # since the bus frequencies (the n values) are coprime, which means their lowest common
    # multiple is the product of all the numbers in the set.

    # So we have 3 times, t0, tx and tN:
    # [t0 --------- tx -------- tN]
    # bus 0 leaves at tx + a0, with a frequency n0: x % n0 = a0
    # bus 1 leaves at tx + 1: x % n1 = a1
    # all the buses leave at tN
    # etc.
    # and x is the time between tx and tN. t0 is 0, tN is N, thus tx = tN - x

    return p - x


second = second_crt


def parse_input(puzzle_input: Iterator[str]) -> Tuple[int, List[str]]:
    lines = [l.strip() for l in puzzle_input]
    return (int(lines[0]), lines[1].split(","))
