from pydoc import plain
from typing import List


RAW_INPUT = """
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
"""

def parse_input(plain_text: str) -> List[str]:
    return plain_text.strip().splitlines()


def compute_rucksack_intersection(rucksack: str) -> str:
    half = len(rucksack) // 2
    first_compartment = rucksack[: half]
    second_compartment = rucksack[half: ]

    unique_items_in_first_comp = set(first_compartment)

    unique_items_in_second_comp = set(second_compartment)

    intersection = list(unique_items_in_first_comp.intersection(unique_items_in_second_comp))
    assert len(intersection) == 1

    return intersection[0]


def compute_priority_score(char: str) -> int:
    base_score = ord(char.lower()) - ord('a') + 1
    return base_score + 26 * int(char.isupper())


def compute_total_priority_score(rucksacks: List[str]):
    score = 0
    for rucksack in rucksacks:
        intersection = compute_rucksack_intersection(rucksack)
        score += compute_priority_score(intersection)
    return score


def compute_group_intersection(
    r1: str, r2: str, r3: str):
    intersection = (
        set(r1).intersection(
            set(r2).intersection(
                set(r3)
            )
        )
    )

    assert len(intersection) == 1
    return list(intersection)[0]



def compute_group_priority_score(rucksacks: List[str]) -> int:
    score = 0
    for i in range(0, len(rucksacks), 3):
        intersection = (
            compute_group_intersection(rucksacks[i], rucksacks[i + 1], rucksacks[i + 2])
        )    
        score += compute_priority_score(intersection)
    return score    




if __name__ == '__main__':
    test_rucksacks = parse_input(RAW_INPUT)

    test_score = compute_total_priority_score(test_rucksacks)

    assert test_score == 157, test_score

    test_group_score = compute_group_priority_score(test_rucksacks)

    assert test_group_score == 70, test_group_score

    with open('data/input.txt') as f:
        plain_text = f.read()

    rucksacks = parse_input(plain_text)
    answer1 = compute_total_priority_score(rucksacks)
    print(f'answer1: {answer1}')

    answer2 = compute_group_priority_score(rucksacks)
    print(f'answer2: {answer2}')