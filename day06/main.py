from typing import List
from collections import Counter

TEST_INPUT_CASES = [
    'mjqjpqmgbljsphdztnvjfqwrcgsmlb',
    'bvwbjplbgvbhsrlpgdmjqwftvncz',
    'nppdvjthqldpwncqszvftbrmjlhg',
    'nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg',
    'zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw'
]
TEST_ANSWERS_LENGHT_4 = [7, 5, 6, 10, 11]
TEST_ANSWERS_LENGHT_14 = [19, 23, 23, 29, 26]



def find_start_marker(buffer: str, lenght: int = 4) -> int:
    assert len(buffer) >= lenght
    last_chars = Counter()
    for i, char in enumerate(buffer):
        if i > lenght - 1:
            last_chars[buffer[i - lenght]] -= 1
            if last_chars[buffer[i - lenght]] == 0:
                del last_chars[buffer[i - lenght]]
        last_chars[char] += 1
        if len(last_chars) == lenght:
            return i + 1

    raise ValueError('no lenght consecutive unique characters')

if __name__== "__main__":
    for i in range(len(TEST_INPUT_CASES)):
        assert find_start_marker(TEST_INPUT_CASES[i]) == TEST_ANSWERS_LENGHT_4[i]
        assert find_start_marker(TEST_INPUT_CASES[i], 14) == TEST_ANSWERS_LENGHT_14[i]

    
    with open('data/input.txt') as f:
        buffer = f.read().strip()
    start_marker_4 = find_start_marker(buffer)
    print(f'answer1: {start_marker_4}') 

    start_marker_14 = find_start_marker(buffer, lenght=14)
    print(f'answer2: {start_marker_14}') 