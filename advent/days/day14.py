import itertools as its
import math
import re
from typing import Generator, Iterator

PROGRAM_INT_BIT_SIZE = 36
ALL_ONES = (1 << PROGRAM_INT_BIT_SIZE) - 1


def binstr_to_int(binstr: str) -> int:
    return sum(int(j) << i for i, j in enumerate(reversed(binstr)))


def overwrite_bit(value: int, bit_value: int, bit_position: int) -> int:
    """
    Overwrite a bit at a given position (0 means replace the least significant bit).

    I could have inlined this code in the class, but this makes it easier to unit
    test it.
    """

    if bit_value == 1:
        # OR with a number that's all 0s except a 1 at pos
        return value | (1 << bit_position)

    if bit_value == 0:
        # AND with a number that's all 1s except a 0 at pos
        return value & (ALL_ONES ^ (1 << bit_position))

    raise ValueError("Invalid bit replacement, value={bit_value}")


class DockingProgramRunner:
    def __init__(self, program: Iterator[str], version: int = 1):
        self.memory = {}
        self.version = version

        # This mask is all 0s except the values that should be switched to 1s
        # it will be OR'd with the values written
        self.mask_1s = 0

        # This mask is all 1s for all 36 bits except the values that should be switched to 0s
        # it will AND'd with the values written
        self.mask_0s = int(math.pow(2, PROGRAM_INT_BIT_SIZE)) - 1
        self.mask = ""

        self.parse_program(program)

    def run(self):
        # Run all the things
        for cmd_fn, args in self.instructions:
            cmd_fn(*args)

    def get_sum(self):
        return sum(v for v in self.memory.values())

    def parse_program(self, program):
        self.instructions = []

        for line in program:
            line = line.strip()
            m = re.match(r"^(?P<command>[a-z]+)", line)

            if not m:
                raise ValueError(f"Unable to parse line `{line}`")

            command = m.group("command")

            if command == "mem":
                m = re.match(r"^mem\[(?P<address>\d+)\] = (?P<value>\d+)$", line)
                if not m:
                    raise ValueError(f"Unable to parse line `{line}`")

                address = m.group("address")
                value = m.group("value")

                self.instructions.append((self.instr_write, [int(address), int(value)]))

            elif command == "mask":
                m = re.match(r"^mask = (?P<value>[X01]+)$", line)
                if not m:
                    raise ValueError(f"Unable to parse line `{line}`")

                value = m.group("value")
                self.instructions.append((self.instr_update_mask, [value]))

    def instr_write(self, address: int, value: int) -> None:

        if self.version == 1:
            masked_value = self.apply_mask(value)
            self.memory[address] = masked_value
        else:
            for addr in self.get_v2_masked_values(address):
                self.memory[addr] = value

    def instr_update_mask(self, value: str) -> None:
        # All 0s except the values that should be turned to 1s
        self.mask_1s = binstr_to_int(value.replace("X", "0"))

        # All 1s except the values that should be turned to 0s
        self.mask_0s = binstr_to_int(value.replace("X", "1"))

        # Store the string representation of the mask
        self.mask = value

    def apply_mask(self, value: int) -> int:
        # The 1 mask is all 0s except numbers that should be forced to 1
        value |= self.mask_1s

        # The 0 mask is all 1s except numbers that should be forced to 0
        value &= self.mask_0s

        return value

    def get_v2_masked_values(self, value: int) -> Generator[int, None, None]:
        x_count = sum(1 if c == "X" else 0 for c in self.mask)

        # Position from the right of the mask so we reverse it
        x_pos = [i for i, c in enumerate(self.mask[::-1]) if c == "X"]

        # Apply the 1s from the mask
        for i, c in enumerate(self.mask[::-1]):
            if c == "1":
                value = overwrite_bit(value, 1, i)

        for combination in its.product([0, 1], repeat=x_count):
            new_value = value
            for pos, x_value in zip(x_pos, combination):
                new_value = overwrite_bit(new_value, x_value, pos)

            yield new_value


def first(puzzle_input: Iterator[str]) -> int:
    runner = DockingProgramRunner(puzzle_input)
    runner.run()

    return runner.get_sum()


def second(puzzle_input: Iterator[str]) -> int:
    runner = DockingProgramRunner(puzzle_input, version=2)
    runner.run()

    return runner.get_sum()
