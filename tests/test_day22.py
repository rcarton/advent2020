from collections import deque

from advent.days.day22 import (
    first,
    second,
    Deck,
    parse_input,
    score,
    play_recursive_combat,
    hash_round,
)

EXAMPLE = """Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10""".splitlines(
    keepends=True
)


def test_score():
    assert score(deque([3, 2, 10, 6, 8, 5, 9, 4, 7, 1])) == 306


def test_parse_input():
    p1_deck: Deck = deque([9, 2, 6, 3, 1])
    p2_deck: Deck = deque([5, 8, 4, 7, 10])

    assert parse_input(EXAMPLE) == (p1_deck, p2_deck)


def test_first():
    assert first(EXAMPLE) == 306


def test_play_recursive_combat():
    expected_deck = deque([7, 5, 6, 2, 4, 1, 10, 8, 9, 3])
    assert play_recursive_combat(*parse_input(EXAMPLE)) == (False, expected_deck)


def test_play_recursive_combat_previous_rounds():
    p1_deck: Deck = deque([3, 19])
    p2_deck: Deck = deque([30, 29, 14])
    previous_rounds = {hash_round(p1_deck, p2_deck)}
    assert play_recursive_combat(p1_deck, p2_deck, previous_rounds) == (True, p1_deck)
    assert play_recursive_combat(p1_deck, p2_deck) == (
        False,
        deque([14, 30, 3, 29, 19]),
    )


def test_second():
    assert second(EXAMPLE) == 291
