import re
from dataclasses import dataclass
from typing import Iterator, List


@dataclass
class Instruction:
    operation: str
    argument: str


class Runner:
    def __init__(self, instructions):
        self.accumulator = 0
        self.instructions = instructions
        self.position = 0
        self._visited = set()
        self.successful = False

        self.supported_instructions = {
            "nop": self.instr_nop,
            "acc": self.instr_acc,
            "jmp": self.instr_jmp,
        }

    def run_until_loop(self) -> int:
        """
        Return the value in the accumulator before running an instruction a second time.
        """
        while self.position not in self._visited:
            if self.position >= len(self.instructions):
                self.successful = True
                break

            # Mark the line as already visited
            self._visited.add(self.position)
            self._next()

        return self.accumulator

    def _next(self) -> None:
        instruction = self.instructions[self.position]
        op = instruction.operation
        arg = instruction.argument

        self.supported_instructions[op](arg)

    def instr_nop(self, _: int):
        self.position += 1

    def instr_acc(self, arg: int):
        self.accumulator += arg
        self.position += 1

    def instr_jmp(self, arg: int):
        self.position += arg


def first(puzzle_input: Iterator[str]) -> int:
    runner = Runner(parse_instructions(puzzle_input))
    return runner.run_until_loop()


def second(puzzle_input: Iterator[str]) -> int:
    for program in possible_programs(parse_instructions(puzzle_input)):
        runner = Runner(program)
        runner.run_until_loop()

        if runner.successful:
            return runner.accumulator

    raise ValueError("Unable to find a successful program")


def possible_programs(program: List[Instruction]) -> Iterator[List[Instruction]]:
    """This generator will return all the possible programs that change a single
    nop to jmp or jmp to nop."""

    i = 0
    while i < len(program):
        op = program[i].operation
        arg = program[i].argument
        if op in ("jmp", "nop"):
            new_op = "jmp" if op == "nop" else "nop"
            yield program[:i] + [Instruction(new_op, arg)] + program[i + 1 :]
        i += 1


def parse_instructions(instructions: Iterator[str]) -> List[Instruction]:
    parsed = []
    for line in instructions:
        line = line.strip()

        m = re.match(r"(?P<operation>\w{3}) (?P<argument>[+-]\d+)", line)

        if not m:
            raise ValueError(f"Unable to parse instruction '{line}'")

        parsed.append(Instruction(m.group("operation"), int(m.group("argument"))))

    return parsed
