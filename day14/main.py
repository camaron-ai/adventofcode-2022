import itertools
from typing import Tuple, List, Dict, Set
from dataclasses import dataclass 

Coordinate = Tuple[int, int]
LinePoint = List[Coordinate]
Blocks = Dict[int, List[int]]

RAW_INPUT = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""

SAND_POINT = (500, 0)

def parse_line_points(line: str) -> LinePoint:
    return [tuple(map(int, coordinate.strip().split(',')))
                    for coordinate in line.split(' -> ')]


assert parse_line_points('498,4 -> 498,6 -> 496,6') == [(498, 4), (498, 6), (496, 6)]

def parse_input(plain_text: str) -> List[LinePoint]:
    return [parse_line_points(line) for line in plain_text.strip().splitlines()]


@dataclass
class Cave:
    blocks: Set[Coordinate]

    def get_possible_x_moves(self, x: int):
        yield from [x, x - 1, x + 1]


    def let_sand_fall_until_void(self) -> int:
        bottom = max([y for _, y in self.blocks]) + 1

        for i in itertools.count():
            currp = SAND_POINT
            while True:
                x, y = currp
                # we have reach the void, return i
                if y > bottom:
                    return i

                for next_x in self.get_possible_x_moves(x):
                    if (next_x, y + 1) not in self.blocks:
                        currp = (next_x, y + 1)
                        break
                else:
                    break
            self.blocks.add(currp)
    

    def fill_sand_until_start(self) -> int:
        bottom = max([y for _, y in self.blocks]) + 2
        # add bottom line
        for x in range(-2000, 2000):
            self.blocks.add((x, bottom))

        for i in itertools.count(1):
            currp = SAND_POINT
            while True:
                x, y = currp
                # we have reach the void, stop
                for next_x in self.get_possible_x_moves(x):
                    if (next_x, y + 1) not in self.blocks:
                        currp = (next_x, y + 1)
                        break
                else:
                    break

            if currp == SAND_POINT:
                return i
            self.blocks.add(currp)


    @staticmethod
    def parse_from_lines(lines: List[LinePoint]) -> 'Cave':
        blocks = set()
        def add_line_blocks(
            currp: Coordinate,
            nextp: Coordinate,
            ):

            dx = nextp[0] - currp[0]
            dy = nextp[1] - currp[1]
            x_sign = min(max(dx, -1), 1) 
            y_sign = min(max(dy, -1), 1) 
            lenght = max(abs(dx), abs(dy))

            for i in range(lenght + 1):
                next_x = currp[0] + i * x_sign
                next_y = currp[1] + i * y_sign
                blocks.add((next_x, next_y))

        for line in lines:
            for i in range(len(line) - 1):
                currp = line[i]
                nextp = line[i + 1] 
                add_line_blocks(currp, nextp)

        return Cave(blocks)

    @staticmethod
    def parse_from_plain_text(plain_text: str) -> 'Cave':
        line_points = parse_input(plain_text)
        return Cave.parse_from_lines(line_points)


if __name__ == '__main__':
    test_puzzle = Cave.parse_from_plain_text(RAW_INPUT)

    test_n_sand_until_void = test_puzzle.let_sand_fall_until_void()
    assert test_n_sand_until_void == 24, test_n_sand_until_void

    test_puzzle = Cave.parse_from_plain_text(RAW_INPUT)
    test_n_fill_sand = test_puzzle.fill_sand_until_start()
    assert test_n_fill_sand == 93, test_n_fill_sand

    with open('data/input.txt') as f:
        plain_text = f.read()
    

    cave = Cave.parse_from_plain_text(plain_text)
    n_sand_until_void = cave.let_sand_fall_until_void()
    print(n_sand_until_void)

    cave = Cave.parse_from_plain_text(plain_text)
    n_fill_sand = cave.fill_sand_until_start()
    print(n_fill_sand)

    