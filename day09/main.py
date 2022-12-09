from turtle import position
from typing import Tuple, List

RAW_INPUT = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""

LONGER_RAW_INPUT = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20"""

Coordinate = Tuple[int, int]

DIRECTION_TO_COORDINATE_MAPPER = {
    'R': (1, 0),
    'L': (-1, 0),
    'U': (0, 1),
    'D': (0, -1)
}



def parse_input(plain_text: str):
    lines = plain_text.splitlines()
    output = []

    for line in lines:
        direction, times = line.strip().split(' ')
        dir_coordinate = DIRECTION_TO_COORDINATE_MAPPER[direction]
        output.append((dir_coordinate, int(times)))
    return output



def distance(x1: Coordinate, x2: Coordinate) -> int:
    return max([abs(x1[i] -  x2[i]) for i in range(len(x1))])


def sign(x: int) -> int:
    return 1 if x >= 0 else -1

def move(
    head_p: Coordinate,
    tail_p: Coordinate) -> Coordinate:
    """move the tail to catch up the head"""

    x_diff = head_p[0] - tail_p[0]
    y_diff = head_p[1] - tail_p[1]
    x_distance = abs(x_diff)
    y_distance = abs(y_diff)
    max_distance = max(x_distance, y_distance)
    # they are touching
    if max_distance <= 1:
        return tail_p

    # correct direction
    x_correction = sign(x_diff) * min(x_distance, 1)
    y_correction = sign(y_diff) * min(y_distance, 1)

    return tail_p[0] + x_correction, tail_p[1] + y_correction 



def find_number_of_tail_position(
    moves: List[Tuple[Coordinate, int]],
    number_of_tails: int = 1):
    heap_p = (0, 0)
    tails = [heap_p for _ in range(number_of_tails)]

    visited_location = set()
    for (dx, dy), t in moves:
        for _ in range(t):
            heap_p = heap_p[0] + dx, heap_p[1] + dy

            current_head = heap_p
            for i in range(len(tails)):
                tails[i] = move(current_head, tails[i])
                current_head = tails[i]
            visited_location.add(tails[-1])
    return len(visited_location)


if __name__ == '__main__':
    test_moves = parse_input(RAW_INPUT)
    test_n_loc = find_number_of_tail_position(test_moves)
    assert test_n_loc == 13

    test_n_loc_visited_9_tails = find_number_of_tail_position(test_moves, number_of_tails=9)
    assert test_n_loc_visited_9_tails == 1


    longer_test_moves = parse_input(LONGER_RAW_INPUT)
    test_n_loc_visited_9_tails = find_number_of_tail_position(longer_test_moves, number_of_tails=9)
    assert test_n_loc_visited_9_tails == 36

    with open('data/input.txt') as f:
        plain_text = f.read()
    
    moves = parse_input(plain_text)

    n_visited_loc = find_number_of_tail_position(moves)
    print(n_visited_loc)


    n_loc_visited_9_tails = find_number_of_tail_position(moves, number_of_tails=9)
    print(n_loc_visited_9_tails)

