from typing import List, Tuple
import itertools

RAW_INPUT = """noop
addx 3
addx -5
"""

ROWS = 6
COLS = 40

Instruction = List[Tuple[int, int]]
def parse_input(plain_text: str) -> Instruction:

    output = [] 
    for line in plain_text.strip().splitlines():
        output.append(0)
        if not line.strip() == 'noop':
            _, value = line.strip().split(' ')
            output.append(int(value))
    return output

assert parse_input(RAW_INPUT) == [0, 0, 3, 0, -5]

def compute_register_state(
    instructions: Instruction,
    ) -> int:
    register = list(itertools.accumulate(instructions, initial=1))
    return register

assert compute_register_state(parse_input(RAW_INPUT)) == [1, 1, 1, 4, 4, -1]


def compute_signal_strength(instructions) -> int:
    register = compute_register_state(instructions)
    strength = [register[i] * (i + 1) for i in range(19, 220, 40)]
    return sum(strength)


def display_crt(instructions):
    register = compute_register_state(instructions)
    display = [
        [0 for _ in range(COLS)]
        for _ in range(ROWS)]

    for cycle in range(240):
        is_on = int(abs(register[cycle] - cycle % COLS) <= 1)
        display[cycle // COLS][cycle % COLS] = is_on 

    str_display = '\n'.join([
        ''.join([('.', '#')[i] for i in row])
        for row in display])
    print(str_display)



if __name__ == '__main__':
    with open('data/test_case.txt') as f:
        test_plain_text = f.read()
    test_case = parse_input(test_plain_text)
    assert compute_signal_strength(test_case) == 13140
    print('test case display')
    display_crt(test_case)

    with open('data/input.txt') as f:
        plain_text = f.read()
    instructions = parse_input(plain_text)

    signal_strength = compute_signal_strength(instructions)
    print(f'answer1: {signal_strength}')

    print('part 2')
    display_crt(instructions)





