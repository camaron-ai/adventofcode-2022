from typing import List
import heapq

RAW_INPUT = """
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
"""


def parse_input(plain_text: str) -> List[int]:

    elf_lines = plain_text.strip().split('\n\n')
    elf_calories = [
        list(map(int, raw_cal.split('\n')))
        for raw_cal in elf_lines
        ]
    return elf_calories


def max_calories(calories: List[List[int]]):
    # sum over the calories of each elf
    # to avoid use extra memory, we will do a for loop 
    # and keep track of the maximum so far
    answer = float('-inf')
    for elf_calories in calories:
        answer = max(answer, sum(elf_calories))
    return answer


def sum_top3_calories(calories: List[List[int]]):
    # to avoid use extra memory, we will replace
    # calories[i] = sum(calories[i])
    for i in range(len(calories)):
        calories[i] = sum(calories[i])
    # use a heap to get the top 3 largest calories and avoid sorting
    return sum(heapq.nlargest(3, calories))



if __name__ == '__main__':
    elf_calories = parse_input(RAW_INPUT)
    answer = max_calories(elf_calories)

    assert answer == 24000


    with open('data/input.txt') as f:
        plain_text = f.read()

    elf_calories = parse_input(plain_text)
    answer1 = max_calories(elf_calories)

    print(f'answer1, maximum calories: {answer1}')

    answer2 = sum_top3_calories(elf_calories)

    print(f'answer2, top 3 calories: {answer2}')
