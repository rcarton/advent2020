from typing import Iterator, Deque, Tuple, Set, Optional
from collections import deque

Deck = Deque[int]


def parse_input(puzzle_input: Iterator[str]) -> Tuple[Deck, Deck]:
    lines = "".join(list(puzzle_input))
    player_lines = lines.split("\n\n")

    players = []
    for cards in player_lines:
        cards = deque([int(c) for c in cards.splitlines()[1:]])
        players.append(cards)

    return players[0], players[1]


def play_round(p1_deck: Deck, p2_deck: Deck) -> None:
    """
    Play one round of Combat.

    Both players draw their top card, and the player with the higher-valued card wins
    the round. The winner keeps both cards, placing them on the bottom of their own deck
    so that the winner's card is above the other card. If this causes a player to have
    all of the cards, they win, and the game ends.
    """
    card1 = p1_deck.popleft()
    card2 = p2_deck.popleft()

    if card1 > card2:
        p1_deck.append(card1)
        p1_deck.append(card2)
    else:
        p2_deck.append(card2)
        p2_deck.append(card1)


def score(deck: Deck) -> int:
    """Compute the score for a given deck."""
    deck = list(deck)
    deck.reverse()

    return sum((i + 1) * card_value for i, card_value in enumerate(deck))


def first(puzzle_input: Iterator[str]) -> int:
    """Play the game of Combat and calculate the score of the winning player."""

    p1_deck, p2_deck = parse_input(puzzle_input)

    while p1_deck and p2_deck:
        play_round(p1_deck, p2_deck)

    winning_deck = p1_deck if p1_deck else p2_deck

    return score(winning_deck)


def hash_round(p1_deck: Deck, p2_deck: Deck) -> str:
    """Lazy hash implementation."""
    return str((p1_deck, p2_deck))


def copy_deck_cards(deck: Deck, count: int) -> Deck:
    """Copy the first `count` cards from the deck into a new deck."""
    return deque(deck[i] for i in range(count))


def play_recursive_combat_round(p1_deck: Deck, p2_deck: Deck) -> None:
    """Play a round of Recursive Combat."""
    card1 = p1_deck.popleft()
    card2 = p2_deck.popleft()

    should_play_recursive = len(p1_deck) >= card1 and len(p2_deck) >= card2

    if should_play_recursive:
        p1_wins, _ = play_recursive_combat(
            copy_deck_cards(p1_deck, card1), copy_deck_cards(p2_deck, card2), fast=True
        )
    else:
        p1_wins = card1 > card2

    if p1_wins:
        p1_deck.append(card1)
        p1_deck.append(card2)

    else:
        p2_deck.append(card2)
        p2_deck.append(card1)


def can_recurse(p1_deck: Deck, p2_deck: Deck) -> bool:
    """
    Return True if it's possible that the game would require recursing.

    A game will recurse if both cards are smaller or equal to the length of their
    respective decks.

    This means that if the sum of the two smallest cards is less than the lengh of the
    decks, then this condition cannot ever be true.

    There may be other optimizations for this method.
    """
    return min(p1_deck) + min(p2_deck) <= len(p1_deck) + len(p2_deck)


def play_recursive_combat(
    p1_deck: Deck, p2_deck: Deck, previous_rounds: Optional[Set[str]] = None, fast=False
) -> Tuple[bool, Deck]:
    """
    Play a game of Recursive Combat.

    This method supports a "fast" mode if the resulting deck does not matter. In this
    situation we can short circuit the game if the following two conditions are true:

    - player 1's deck has the highest card value
    - no recursion can occur because the smallest card values are too large

    """
    previous_rounds: Set[str] = previous_rounds if previous_rounds else set()

    if fast:
        # Play the fast version because we don't need the resulting deck
        cant_recurse = not can_recurse(p1_deck, p2_deck)
        player1_has_largest_card = max(p1_deck) > max(p2_deck)

        # If there is no recursion possible and the first player has the biggest card
        # then they cannot lose since they can't lose a round and a repeat results in a
        # win in their favor
        if cant_recurse and player1_has_largest_card:
            # The deck is incorrect, but it doesn't matter, it's a fast game
            return True, p1_deck

    while p1_deck and p2_deck:
        round_hash = hash_round(p1_deck, p2_deck)

        # This round has already been played, player 1 wins
        if round_hash in previous_rounds:
            return True, p1_deck

        previous_rounds.add(round_hash)
        play_recursive_combat_round(p1_deck, p2_deck)

    if p1_deck:
        return True, p1_deck

    return False, p2_deck


def second(puzzle_input: Iterator[str]) -> int:

    p1_deck, p2_deck = parse_input(puzzle_input)
    _, winning_deck = play_recursive_combat(p1_deck, p2_deck)

    return score(winning_deck)
