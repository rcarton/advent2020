"""
AOC Day 17
~~~~~~~~~~

Multidimensional Conway!

"""
import itertools as its
from typing import Dict, Generator, Iterator, List

Pos = List[int]

ACTIVE = "#"


class World:
    """
    Represents a conway world with a set number of dimensions.

    Only active cells are stored in the state.

    This class keeps track of the minimum value for each dimension to optimize the
    space to look for neighbors in.

    """

    state: Dict[Pos, int]

    min_dims: List[int]
    max_dims: List[int]
    dimensions: int

    def __init__(self, dimensions=3):
        self.state = {}
        self.active_count = 0
        self.dimensions = dimensions
        self.min_dims = [None for _ in range(dimensions)]
        self.max_dims = [None for _ in range(dimensions)]

    @staticmethod
    def from_world(world):
        """Create a new empty world from an existing world."""

        new_world = World(dimensions=world.dimensions)
        new_world.dimensions = world.dimensions
        return new_world

    @staticmethod
    def from_puzzle_input(initial_state: Iterator[str], dimensions: int = 3):
        """Create a world from a puzzle input."""

        world = World(dimensions=dimensions)
        pos = [0 for _ in range(dimensions)]
        for line in initial_state:
            line = line.strip()

            for x, letter in enumerate(line):
                pos[0] = x
                if letter == ACTIVE:
                    world.set_cube(pos, 1)

            pos[1] += 1

        return world

    def set_cube(self, pos, value):
        # We're not storing inactive cubes
        if not value:
            return

        # We could also sum() the values of state to get this count
        self.active_count += 1

        # Keep track of the bounds of the space
        for i in range(self.dimensions):
            if self.min_dims[i] is None or pos[i] < self.min_dims[i]:
                self.min_dims[i] = pos[i]
            if self.max_dims[i] is None or pos[i] > self.max_dims[i]:
                self.max_dims[i] = pos[i]

        self.state[tuple(pos)] = value

    def get_cube(self, pos: Pos) -> int:
        return self.state.get(tuple(pos), 0)

    def count_active_neighbors(self, pos: Pos) -> int:
        ranges = (range(dim - 1, dim + 2) for dim in pos)

        # All the possible neighbors including the current cube
        neighbor_pos = its.product(*ranges)

        # We need to subtract the current cube since it's included in neighbors
        return sum(self.state.get(p, 0) for p in neighbor_pos) - self.state.get(pos, 0)

    def possible_active_cubes(self) -> Generator[Pos, None, None]:
        ranges = (
            range(min_dim - 1, max_dim + 2)
            for min_dim, max_dim in zip(self.min_dims, self.max_dims)
        )

        return its.product(*ranges)


def step(world: World) -> World:
    """
    Create a new world by applying the rules once to the input world.

    Consider every cube neighboring the current world:
        - if the cube has 3 neighbors, it should be active
        - if the cube is active and has 2 neighbors, it should be active
        - otherwise the cube is not active
    """

    new_world = World.from_world(world)

    for cube_pos in world.possible_active_cubes():
        active_neighbors = world.count_active_neighbors(cube_pos)

        if active_neighbors == 3 or world.get_cube(cube_pos) and active_neighbors == 2:
            new_world.set_cube(cube_pos, 1)

    return new_world


def first(puzzle_input: Iterator[str], cycles=6):
    world = World.from_puzzle_input(puzzle_input, dimensions=3)

    for _ in range(cycles):
        world = step(world)

    return world.active_count


def second(puzzle_input: Iterator[str], cycles=6) -> int:
    world = World.from_puzzle_input(puzzle_input, dimensions=4)

    for _ in range(cycles):
        world = step(world)

    return world.active_count
