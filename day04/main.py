from typing import List, Tuple
RangePair = Tuple[int, int]
PairTuple = Tuple[RangePair, RangePair]


RAW_INPUT = """
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""


def parse_input(plain_text: str) -> List[RangePair]:
    lines = plain_text.strip().splitlines()
    output = [
    [list(map(int, r.split('-'))) for r in pair.split(',') ]
        for pair in lines        
    ]
    return output


def does_fully_pairs_overlap(p1: RangePair, p2: RangePair) -> bool:
    s1, e1 = p1
    s2, e2 = p2
    return ((s1 <= s2) and (e2 <= e1)) or ((s2 <= s1) and (e1 <= e2)) 


def compute_num_fully_overlap_ranges(pairs: List[RangePair]) -> int:
    score = 0

    for p in pairs:
        score += int(does_fully_pairs_overlap(*p))
    
    return score


def does_pairs_overlap(p1: RangePair, p2: RangePair) -> bool:
    s1, e1 = p1
    s2, e2 = p2

    not_overlap = (e1 < s2) or (e2 < s1)
    
    return not not_overlap
    # return (s1 <= e2 <= e1) or (s2 <= e1 <= e2)


def compute_num_overlap_ranges(pairs: List[RangePair]) -> int:
    score = 0

    for p in pairs:
        score += int(does_pairs_overlap(*p))
    
    return score


if __name__ == '__main__':
    test_pairs = parse_input(RAW_INPUT)
    test_num_fully_overlap = compute_num_fully_overlap_ranges(test_pairs)
    assert test_num_fully_overlap == 2

    test_num_overlap = compute_num_overlap_ranges(test_pairs)
    assert test_num_overlap == 4

    with open('data/input.txt') as f:
        plain_text = f.read()

    pairs = parse_input(plain_text)
    num_fully_overlap = compute_num_fully_overlap_ranges(pairs)
    print(f'answer1: {num_fully_overlap}')


    num_overlap = compute_num_overlap_ranges(pairs)
    print(f'answer2: {num_overlap}')