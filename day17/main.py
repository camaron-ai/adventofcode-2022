from dataclasses import dataclass
from email.header import decode_header
from typing import List
from collections import defaultdict

RAW_INPUT = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"

LEFT_DISTANCE = 2
HEIGHT_DISTANCE = 3
WIDTH = 7
RIGHT_EDGE_MASK = 1
LEFT_EDGE_MASK = 1 << (WIDTH - 1)


def shift_mask(mask: int, direction: int):
    if direction > 0:
        return mask >> 1
    elif direction < 0:
        return mask << 1


@dataclass
class Rock:
    masks: List[int]

    def shift(self, direction: int) -> 'Rock':
        if any(m & RIGHT_EDGE_MASK for m in self.masks) and direction == 1:
            return self
        elif any(m & LEFT_EDGE_MASK for m in self.masks) and direction == -1:
            return self

        shifted_masks = [shift_mask(mask, direction) for mask in self.masks]
        return Rock(shifted_masks)

    @staticmethod
    def from_binary(bit_matrix: List[int]) -> 'Rock':
        masks = []
        for bits in bit_matrix:
            x = 0
            for i, b in enumerate(bits):
                x += b << (WIDTH - LEFT_DISTANCE - i - 1)
            masks.append(x)
        return Rock(masks)
            

ROCK_M = [
    [[1, 1, 1, 1]],
    [[0, 1, 0], [1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [0, 0, 1], [0, 0, 1]],
    [[1], [1], [1], [1]],
    [[1, 1], [1, 1]],
]

ROCKS = [Rock.from_binary(m) for m in ROCK_M]

class Chamber:
    def __init__(self, moves: str, width: int = 7):
        self.width = width
        self.moves = moves

    @property
    def curr_move(self):
        move = self.moves[self.i]
        self.i = (self.i + 1) % len(self.moves)
        return move

    def rock_is_blocked(
        self, masks: List[int], curr_height: int):
        return any(
            [(m & self.heights[curr_height + i]) > 0
            for i, m in enumerate(masks)]
            )

    def let_rock_fall(self, rock_id: int):
        rock = ROCKS[rock_id]
        curr_height = self.current_top + HEIGHT_DISTANCE + 1

        while not self.rock_is_blocked(rock.masks, curr_height):
            curr_move = self.curr_move
            shifted_rock = rock.shift(curr_move)
            if not self.rock_is_blocked(shifted_rock.masks, curr_height):
                rock = shifted_rock
            curr_height -= 1
    
        for i, mask in enumerate(rock.masks):
            self.heights[curr_height + i + 1] |= mask
        self.current_top = max(self.current_top, curr_height + len(rock.masks))

        board_status = tuple(self.heights[self.current_top - i] for i in range(31))
        signature = (rock_id, curr_move, board_status)

        return signature

    def play(self, n_rocks: int):

        memo = {}
        additional_height = 0
        self.heights = defaultdict(int)
        self.heights[0] = (2 ** self.width) - 1
        self.i = 0
        self.current_top = 0
        t = 0

        while t < n_rocks:
            signature = self.let_rock_fall(t % len(ROCKS))
            if signature in memo:
                (last_time, last_height) = memo[signature]
                height_difference = self.current_top - last_height
                time_difference = t - last_time

                n_repeat = (n_rocks - t) // time_difference

                additional_height += height_difference * n_repeat
                t += time_difference * n_repeat
            memo[signature] = (t, self.current_top)

            t += 1
        return self.current_top + additional_height 

    @staticmethod
    def parse(plain_text: str) -> 'Chamber':
        moves = [1 if char == '>' else -1 for char in plain_text]
        return Chamber(moves)


if __name__ == '__main__':

    test_chamber = Chamber.parse(RAW_INPUT)

    test_maximum_height = test_chamber.play(2022)
    assert test_maximum_height == 3068, test_maximum_height

    test_maximum_height_after_insane_rocks = test_chamber.play(1000000000000)
    assert test_maximum_height_after_insane_rocks == 1514285714288


    with open('data/input.txt') as f:
        plain_text = f.read()

    chamber = Chamber.parse(plain_text)
    maximum_height = chamber.play(2022)
    print(maximum_height)

    maximum_height_after_insane_rocks = chamber.play(1000000000000)
    print(maximum_height_after_insane_rocks)


