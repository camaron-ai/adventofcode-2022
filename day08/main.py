
from typing import List

RAW_INPUT = """30373
25512
65332
33549
35390"""


Grid = List[List[int]]


def parse_input(plain_text: str) -> Grid:
    return [list(map(int, row)) for row in plain_text.strip().splitlines()]


def find_number_of_visible_trees(grid: Grid):
    def compute_visible_trees(
        grid: Grid):
        n = len(grid)
        m = len(grid[0])

        is_visible = [
            [False for _ in range(m)] for _ in range(n)
             ]
        maximum_values = [float('-inf') for _ in range(n)]

        for i in range(n):
            for j in range(m):
                is_visible[i][j] = grid[i][j] > maximum_values[i]
                maximum_values[i] = max(grid[i][j], maximum_values[i])

        return is_visible

    mirror_grid = [row[::-1] for row in grid]
    tranpose_grid = list(zip(*grid))
    tranpose_mirror_grid = [row[::-1] for row in tranpose_grid]

    n, m = len(grid), len(grid[0])
    left_visible = compute_visible_trees(grid)
    right_visible = compute_visible_trees(mirror_grid)
    up_visible = compute_visible_trees(tranpose_grid)
    down_visible = compute_visible_trees(tranpose_mirror_grid)
    answer = 0

    for i in range(n):
        for j in range(m):
            is_visible = (
                left_visible[i][j] |
                right_visible[i][m - 1 - j] |
                up_visible[j][i] |
                down_visible[j][n - i - 1]
            )
            answer += is_visible
    return answer


                


def compute_maximum_scenic_score(grid: Grid):
    def scenic_score(
        grid: Grid):
        n = len(grid)
        m = len(grid[0])
        stacks = [[] for _ in range(n)]
        scores = [
            [0 for _ in range(m)]
            for _ in range(n)
             ]

        for i in range(n):
            for j in range(m):
                curr_stack = stacks[i]
                while curr_stack and grid[i][j] > grid[i][curr_stack[-1]]:
                    curr_stack.pop()
                
                last_index = curr_stack[-1] if curr_stack else 0
                scores[i][j] = j - last_index
                curr_stack.append(j)
        return scores
    
    n, m = len(grid), len(grid[0])
    
    mirror_grid = [row[::-1] for row in grid]
    tranpose_grid = list(zip(*grid))
    tranpose_mirror_grid = [row[::-1] for row in tranpose_grid]
    
    left_scores = scenic_score(grid)
    right_scores = scenic_score(mirror_grid)
    up_scores = scenic_score(tranpose_grid)
    down_scores = scenic_score(tranpose_mirror_grid)

    answer = 0
    for i in range(n):
        for j in range(m):
            curr_score = (
                left_scores[i][j] *
                right_scores[i][m - 1 - j] *
                up_scores[j][i] * 
                down_scores[j][n - i - 1]
            )
            answer = max(answer, curr_score)
    return answer


if __name__ == '__main__':
    test_grid = parse_input(RAW_INPUT)
    test_number_of_visible_trees = find_number_of_visible_trees(test_grid)
    assert test_number_of_visible_trees == 21, test_number_of_visible_trees

    test_max_scenic_score = compute_maximum_scenic_score(test_grid)
    assert test_max_scenic_score == 8, test_max_scenic_score

    with open('data/input.txt') as f:
        plain_text = f.read()

    grid = parse_input(plain_text)
    number_of_visible_trees = find_number_of_visible_trees(grid)
    print(number_of_visible_trees)
    max_scenic_score = compute_maximum_scenic_score(grid)
    print(max_scenic_score)