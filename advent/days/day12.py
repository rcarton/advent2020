"""
AOC Day 12
~~~~~~~~~~

Latitude (North/South) and longitude (West/East) are expressed in units instead of degrees:
 lat = -10 means 10 units North
 lon = 40 means 40 units East

"""

import re
from dataclasses import dataclass
from typing import Iterator, List, Tuple


@dataclass
class Ship:
    """A ship with its course and position"""

    # Default course is East, 0 degrees is North
    course: int = 90
    lat: int = 0
    lon: int = 0

    def turn(self, left_or_right: str, degrees: int):
        """Turn the ship"""

        if degrees % 90 != 0:
            raise ValueError("This ship only makes 90 degree turns")

        if left_or_right == "L":
            self.course -= degrees
        else:
            self.course += degrees

        # Normalize the course
        self.course %= 360

    def get_cardinal_direction(self):
        """Translate the course into a cardinal direction"""

        if self.course == 0:
            return "N"
        if self.course == 90:
            return "E"
        if self.course == 180:
            return "S"
        return "W"


@dataclass
class Waypoint:
    """A fictional waypoint at the following position:

    lat: ship.lat + wp.delta_lat
    lon: ship.lon + wp.delta_lon
    """

    delta_lat: int = -1
    delta_lon: int = 10

    def rotate(self, left_or_right: str, degrees: int):
        # Because otherwise I have to do some long forgotten math
        if degrees % 90 != 0:
            raise ValueError(
                "This waypoint only rotates by multiples of 90 degrees")

        # Rotating left by n degrees is the same as rotating right by -n
        if left_or_right == "L":
            degrees *= -1

        # We're rotating right by a positive number of degrees
        degrees %= 360

        # Lazy solution, how many 90 degree rotations to the right are we doing
        for _ in range(degrees // 90):
            self.delta_lat, self.delta_lon = self.delta_lon, -self.delta_lat


Instruction = Tuple[str, int]


def first(puzzle_input: Iterator[str]) -> int:
    instructions = parse_input(puzzle_input)
    s = Ship()

    for instr, value in instructions:
        if instr in ("L", "R"):
            s.turn(instr, value)
        if instr == "F":
            instr = s.get_cardinal_direction()
        if instr == "N":
            s.lat -= value
        if instr == "S":
            s.lat += value
        if instr == "E":
            s.lon += value
        if instr == "W":
            s.lon -= value

    return abs(s.lon) + abs(s.lat)


def second(puzzle_input: Iterator[str]) -> int:
    instructions = parse_input(puzzle_input)
    s = Ship()
    wp = Waypoint()

    for instr, value in instructions:
        if instr in ("L", "R"):
            wp.rotate(instr, value)
        if instr == "F":
            s.lon += value * wp.delta_lon
            s.lat += value * wp.delta_lat
        if instr == "N":
            wp.delta_lat -= value
        if instr == "S":
            wp.delta_lat += value
        if instr == "E":
            wp.delta_lon += value
        if instr == "W":
            wp.delta_lon -= value

    return abs(s.lon) + abs(s.lat)


def parse_input(puzzle_input: Iterator[str]) -> List[Instruction]:
    """Turn the input into a set of instructions"""

    instructions = []

    for line in puzzle_input:
        line = line.strip()
        m = re.match(r"^(?P<instr>[NSEWLRF])(?P<value>\d+)$", line)
        instructions.append((m.group("instr"), int(m.group("value"))))

    return instructions
