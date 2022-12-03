from typing import List, Tuple

RAW_INPUT = """
A Y
B X
C Z
"""

SCORES_MATRIX = [
    [3, 6, 0], # rock
    [0, 3, 6], # paper
    [6, 0, 3], # scissors
]

HAND_SHAPE_OUTCOME_MATRIX = [
    [2, 0, 1], # rock
    [0, 1, 2], # paper
    [1, 2, 0], # scissors
]

HAND_SHAPE_TO_INT = {
    # rock, paper, scissors
    "A": 0, "B": 1, "C":2,
    "X": 0, "Y": 1, "Z": 2
}

def parse_input(plain_text: str) -> List[Tuple[int, int]]:
    strategies = plain_text.strip().splitlines()
    return [
        [HAND_SHAPE_TO_INT[shape] for shape in strat.strip().split(' ')]
        for strat in strategies]


def compute_guide_score(strategies: List[Tuple[int, int]]):
    score = 0
    for op, move in strategies:
        score += SCORES_MATRIX[op][move] + move + 1
    
    return score

def compute_guide_based_on_outcome(strategies: List[Tuple[int, int]]):
    score = 0
    for op, outcome in strategies:
        move = HAND_SHAPE_OUTCOME_MATRIX[op][outcome]
        score += outcome * 3 + move + 1
    return score


if __name__ == '__main__':
    strategies = parse_input(RAW_INPUT)
    expected_score = compute_guide_score(strategies)
    assert expected_score == 15

    expected_score_based_outcome = compute_guide_based_on_outcome(strategies)
    assert expected_score_based_outcome == 12

    with open('data/input.txt') as f:
        plain_text = f.read()
    strategies = parse_input(plain_text)

    score = compute_guide_score(strategies)
    print(f'asnwer1: {score}')

    score_based_outcome = compute_guide_based_on_outcome(strategies)
    print(f'asnwer2: {score_based_outcome}')
