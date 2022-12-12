from typing import List, Tuple, Iterator, Union
from collections import deque

Grid = List[List[int]]
Pair = Tuple[int, int]

def char_to_int(char: str) -> int:
    return ord(char) - ord('a')


RAW_INPUT = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""

def parse_input(plain_text: str) -> Tuple[Grid, Pair, Pair]:
    grid = []
    start_index = None
    end_index = None
    lines = plain_text.strip().splitlines()

    for i, line in enumerate(lines):
        grid.append([])
        for j, char in enumerate(line):
            if char == 'S':
                start_index = i, j
                char = 'a'
            elif char == 'E':
                end_index = i, j
                char = 'z'
            grid[i].append(char_to_int(char)) 
    
    assert start_index is not None
    assert end_index is not None
    
    return grid, start_index, end_index

_, test_start, test_end = parse_input(RAW_INPUT)
assert test_start, test_end == ((0, 0), (2, 5))


def get_neighbors(i: int, j: int, nrows: int, ncols: int) -> Iterator[Pair]:
    # left, right, up, down
    neighbors = [(i, j - 1), (i, j + 1), (i + 1, j), (i - 1, j)]

    for ii, jj in neighbors:
        if 0 <= ii < nrows and 0 <= jj < ncols:
            yield ii, jj


def bfs(grid: Grid, start: Union[List[Pair], Pair], end: Pair):
    nrows, ncols = len(grid), len(grid[0])

    # Queue stores i, j, distance
    # allowed for multiple starts
    if not isinstance(start, list):
        start = [start]

    queue = deque([(s[0], s[1], 0) for s in start])
    seen =  set()

    while queue:
        i, j, distance = queue.popleft()
        if (i, j) == end:
            return distance
        
        for ii, jj in get_neighbors(i, j, nrows, ncols):
            if grid[ii][jj] - grid[i][j] <= 1 and (ii,jj) not in seen:
                
                seen.add((ii, jj))
                queue.append((ii, jj, distance + 1))
    

def shortest_distance_from_lowest_evelation(grid: Grid, end: Pair) -> int:
    nrows, ncols = len(grid), len(grid[0])
    starts = [
        (i, j) for i in range(nrows) for j in range(ncols)
        if grid[i][j] == 0
        ]

    return bfs(grid, starts, end)


if __name__ == '__main__':
    test_grid, test_start, test_end = parse_input(RAW_INPUT)
    
    test_shortest_distance = bfs(test_grid, test_start, test_end)

    assert test_shortest_distance == 31

    test_low_elevation_distance = shortest_distance_from_lowest_evelation(test_grid, test_end)

    assert test_low_elevation_distance == 29

    with open('data/input.txt') as f:
        plain_text = f.read()

    grid, start, end = parse_input(plain_text)
    
    shortest_distance = bfs(grid, start, end)

    print('answer1', shortest_distance)

    low_elevation_distance = shortest_distance_from_lowest_evelation(grid, end)

    print('answer2', low_elevation_distance)
    