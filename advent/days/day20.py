import itertools as its
import math
import re
from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Dict, Iterator, List, Optional, Set, Tuple

# Edges are represented with an integer since they are '....##..' we can turn those into 0s and 1s
# This will speed up comparing if two edges are identical, and make it smaller in memory than a
# string
Edge = int
Edges = Dict[str, Edge]

# pylint: disable=trailing-whitespace
MONSTER = """                  # 
#    ##    ##    ###
 #  #  #  #  #  #   """

# Will be used to identify a monster
MONSTER_REGEXES = [
    re.compile("^" + line.replace(" ", ".")) for line in MONSTER.splitlines()
]
MONSTER_HEIGHT = len(MONSTER_REGEXES)


def get_row(data: List[str], num: int) -> int:
    return int("".join("0" if c == "." else "1" for c in data[num]), 2)


def get_column(data: List[str], num: int) -> int:
    return int(
        "".join("0" if data[y][num] ==
                "." else "1" for y in range(len(data))), 2
    )


def rotate(data: List[str]) -> List[str]:
    """Return the result of rotating the image once clockwise."""

    width = len(data)

    new_data = [[None for _ in range(width)] for _ in range(width)]
    for y in range(width):
        for x in range(width):
            new_data[x][-1 - y] = data[y][x]
    return ["".join(row) for row in new_data]


def flip(data: List[str]) -> List[str]:
    """Return the result of flipping the image."""
    return [line[::-1] for line in data]


@dataclass(eq=True, frozen=True)
class TileState:
    """One of the 8 possible states (flips/rotations) of a tile."""

    tile: Any
    state: str

    # Edges
    top: int
    right: int
    bottom: int
    left: int

    def __repr__(self):
        s = f"{self.tile.id} {self.state} top={self.top} right={self.right}"
        s += f" bottom={self.bottom} left={self.left}\n"
        s += "\n".join(self.data)
        return s

    @property
    def data(self):
        flip_count = int(self.state[1])
        rot_count = int(self.state[3])
        d = self.tile.data[:]
        for _ in range(flip_count):
            d = flip(d)
        for _ in range(rot_count):
            d = rotate(d)
        return d


class Tile:
    """
    Every Tile can be represented 8 different ways:
     - 4 rotations
     - flipped, with 4 more rotations
    """

    id: str
    data: List[str]
    states: Dict[str, TileState]

    def __init__(self, tile_id: str, data: List[str]):
        self.id = tile_id
        self.data = data

        self.store_all_states(data)

    def store_all_states(self, data: List[str]):
        self.states = {}
        d = data[:]
        rotated = 0

        for flipped in (False, True):
            for rotated in range(4):
                if rotated > 0:
                    d = rotate(d)
                state_name = f"f{1 if flipped else 0}r{rotated}"
                edges = {
                    "top": get_row(d, 0),
                    "right": get_column(d, -1),
                    "bottom": get_row(d, -1),
                    "left": get_column(d, 0),
                }

                self.states[state_name] = TileState(
                    tile=self, state=state_name, **edges
                )

            # Rotate one last time to go back to the initial state, but it's not really necessary
            # just easier to reason about if the flipped states start from the same state
            d = rotate(d)
            d = flip(d)


class CandidateArrangement:
    """A candidate for an arrangement of tile states."""

    tiles: List[TileState]
    width: int
    outside_edges: Set[int]
    used: Set[Tile]

    def __init__(
        self,
        tiles: List[TileState],
        width: int,
        outside_edges: Optional[Set[int]] = None,
    ):
        self.width = width
        if outside_edges is None:
            outside_edges = set()
            for tile_i, tile in enumerate(tiles):
                if (tile_i % self.width) == 0:
                    outside_edges.add(tile.left)
                if (tile_i % self.width) == self.width - 1:
                    outside_edges.add(tile.right)
                if tile_i < self.width:
                    outside_edges.add(tile.top)
                if (tile_i + self.width) >= self.width ** 2:
                    outside_edges.add(tile.bottom)

        self.outside_edges = outside_edges
        self.used = {tilestate.tile for tilestate in tiles}
        self.tiles = tiles

    def with_tile(self, tile: TileState, tile_i: Optional[int] = None):
        """Constructor that returns a new instance with an added tile state."""

        outside_edges = self.outside_edges.copy()

        tile_i = len(self.tiles) if tile_i is None else tile_i
        if (tile_i % self.width) == 0:
            outside_edges.add(tile.left)
        if (tile_i % self.width) == self.width - 1:
            outside_edges.add(tile.right)
        if tile_i < self.width:
            outside_edges.add(tile.top)
        if (tile_i + self.width) >= self.width ** 2:
            outside_edges.add(tile.bottom)

        candidate = CandidateArrangement(
            tiles=self.tiles + [tile], width=self.width, outside_edges=outside_edges
        )

        return candidate

    def get_tile(self, index: int) -> Optional[TileState]:
        if 0 <= index < len(self.tiles):
            return self.tiles[index]
        return None


def find_corners(tiles: List[Tile]) -> Tuple[int, int, int, int]:
    """
    Find the corner tile ids.

    This only works because of conditions on the edges in the input data:
      - we know the edges are unique
      - edges are unique even across flips/rotations of the tiles

    Corner tiles have 2 unique edges, but this adds up to 4 because they're
    counted twice.
    """
    edge_counts = defaultdict(set)
    for tile in tiles:
        for tilestate in tile.states.values():
            for edge in (
                tilestate.bottom,
                tilestate.top,
                tilestate.left,
                tilestate.right,
            ):
                edge_counts[edge].add(tile.id)

    # Now find the 4 tiles that have 2 unique edges
    count_uniques = {}
    for edge_tiles in edge_counts.values():
        if len(edge_tiles) == 1:
            tile_id = next(iter(edge_tiles))
            count_uniques[tile_id] = count_uniques.get(tile_id, 0) + 1

    corners = set()
    for tile_id, count in count_uniques.items():
        if count == 4:
            corners.add(tile_id)
    return corners


def first(puzzle_input: Iterator[str]) -> int:
    """
    Solve the image and return the product of the ids of the corner tiles

    Technically since there is a hack/optimization to find the corners, we
    don't really need to solve the image, but we have to solve it for part
    2 anyway.

    """
    tiles = parse_input(puzzle_input)
    width = int(len(tiles) ** 0.5)

    image = solve_image(tiles)

    arrangement = [tilestate.tile for tilestate in image]
    top_left = arrangement[0]
    top_right = arrangement[width - 1]
    bottom_left = arrangement[-width]
    bottom_right = arrangement[-1]

    return math.prod(t.id for t in (top_left, top_right, bottom_left, bottom_right))


def solve_image(tiles: List[Tile]) -> List[TileState]:
    """
    Solve the image by finding a valid corner, and then going through all
    the valid combinations of tile states until one works.

    This method explores a list of candidate solutions by trying to complete
    them.

    At every iteration of the loop, a candidate is removed, and we add as many
    candidates as we were able to fit compatible tile states. If there is no
    valid solution we would eventually run out of candidates, but we know there
    is exactly one valid solution.

    """
    width = int(len(tiles) ** 0.5)

    tiles_by_id = {tile.id: tile for tile in tiles}

    states_by_edge = defaultdict(set)
    for tile in tiles:
        for tilestate in tile.states.values():
            states_by_edge[(tilestate.top, "top")].add(tilestate)
            states_by_edge[(tilestate.right, "right")].add(tilestate)
            states_by_edge[(tilestate.bottom, "bottom")].add(tilestate)
            states_by_edge[(tilestate.left, "left")].add(tilestate)

    # Find the corners ids
    corners = find_corners(tiles)

    # Pick a random top left corner
    top_left = tiles_by_id[next(iter(corners))]

    # Find a valid arrangement that starts this way
    candidates = [
        CandidateArrangement([state], width) for state in top_left.states.values()
    ]

    while candidates:
        candidate = candidates.pop()

        if len(candidate.used) == len(tiles):
            return candidate.tiles

        # Find the next tile position to add
        tile_i = len(candidate.tiles)

        # Is there a tile to the left
        left_tile = candidate.get_tile(
            tile_i - 1) if (tile_i % width) != 0 else None
        top_tile = candidate.get_tile(tile_i - width)

        possible_tilestates = set()

        if left_tile and top_tile:
            possible_tilestates = (
                states_by_edge[(left_tile.right, "left")]
                & states_by_edge[(top_tile.bottom, "top")]
            )
        elif left_tile:
            possible_tilestates = states_by_edge[(left_tile.right, "left")]
        elif top_tile:
            possible_tilestates = states_by_edge[(top_tile.bottom, "top")]

        if not possible_tilestates:
            # We can't find a matching tile for this arrangement, continue on
            continue

        possible_tilestates = {
            tilestate
            for tilestate in possible_tilestates
            if tilestate.tile not in candidate.used
        }

        # Add all the valid tile states as new candidates
        for tilestate in possible_tilestates:
            candidates.append(candidate.with_tile(tilestate))


def make_image(tilestates: List[TileState]) -> List[str]:
    """
    Return an image based on a solution to the tile puzzle.

    The tile states have to be trimmed and concatenated.
    """
    data = []

    width = int(len(tilestates) ** 0.5)
    tile_width = len(tilestates[0].data[0])

    for tile_row in range(0, width):
        tile_data = [
            t.data for t in tilestates[tile_row * width: tile_row * width + width]
        ]

        for i in range(1, tile_width - 1):
            row = ""
            for td in tile_data:
                row += td[i][1:-1]
            data.append(row)

    return data


def is_there_a_monster(data: List[str], row: int, column: int) -> bool:
    """
    This methods tries to match all the monster regexes at the given position.

    It does not verify the boundaries and will raise an error if the monster
    cannot fit in data for the given position.
    """

    for row_i, regex in enumerate(MONSTER_REGEXES):
        if not regex.match(data[row + row_i][column:]):
            return False

    return True


def second(puzzle_input: Iterator[str]) -> int:
    """
    Look for monsters through the solved and trimmed image.

    This method computes all 8 possible images (flips/rotations) and
    looks for a monster at every single position. We could optimize by
    looking for some rare pattersn, but the data set is small enough that
    it does not matter.

    """

    tiles = parse_input(puzzle_input)
    solution = solve_image(tiles)

    # Remove the borders for each tile
    image = make_image(solution)

    # The image is a square
    image_width = len(image[0])

    monster_coordinates = []

    # Now we don't really need to optimize since the space is small:
    # 8*8*144*8 = 73728 (144 tiles, 8*8 characters in a trimmed tile, 8 flip/rotations)
    for flip_count in (False, True):
        if flip_count:
            image = flip(image)

        for rotate_count in range(4):
            if rotate_count:
                image = rotate(image)

                for row, column in its.product(
                    range(image_width - MONSTER_HEIGHT), range(image_width)
                ):
                    if is_there_a_monster(image, row, column):
                        monster_coordinates.append((row, column))

            if monster_coordinates:
                break

    # Now count the #s without the monster's #

    # The monster weight is the number of pounds in the monster
    monster_weight = sum(1 for char in MONSTER if char == "#")
    monster_count = len(monster_coordinates)

    # Number of pound signs in the image
    pounds_in_image = sum(1 for line in image for char in line if char == "#")

    return pounds_in_image - (monster_weight * monster_count)


def parse_input(puzzle_input: Iterator[str]) -> List[Tile]:
    # Chomp through the input
    tiles_str = "".join(puzzle_input).split("\n\n")

    tiles = []
    for tile_str in tiles_str:
        t = tile_str.splitlines()
        tiles.append(Tile(tile_id=int(t[0][5:-1]), data=t[1:]))

    return tiles
