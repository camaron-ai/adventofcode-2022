from dataclasses import dataclass
from typing import List
from copy import deepcopy

RAW_INPUT = """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""


@dataclass
class Instruction:
    n: int
    from_id: int
    to_id: int

    @staticmethod
    def parse(plain_text: str) -> 'Instruction':
        """
         0    1   2      3       4    5
        move {n} from {from_id} to {to_id}
        """

        pieces = plain_text.strip().split(' ')
        assert len(pieces) == 6

        n = int(pieces[1])
        from_id = int(pieces[3]) - 1
        to_id = int(pieces[5]) - 1
        return Instruction(n, from_id, to_id)


def parse_stacks_from_text(plain_text: str) -> List[List[str]]:
    text_matrix = plain_text.splitlines()
    assert len(set(len(l) for l in text_matrix)) == 1
    ncols = len(text_matrix[-1])
    nrows = len(text_matrix)
    indices = [i for i in range(ncols) if text_matrix[-1][i].isnumeric()]

    stacks = [[] for _ in range(len(indices))]

    for row in range(nrows - 2, -1, -1):
        for i, col in enumerate(indices):
            token = text_matrix[row][col]
            if len(token.strip()):
                stacks[i].append(
                    token
                )
    return stacks


def parse_instructions_from_text(plain_text: str) -> List[Instruction]:
    return [
        Instruction.parse(line)
        for line in plain_text.splitlines()
        ]

@dataclass
class Puzzle:
    stacks: List[List[str]]
    instructions: List[Instruction]

    @staticmethod
    def parse(plain_text: str) -> 'Puzzle':
        stack_text, instruction_text = plain_text.split('\n\n')
        stacks = parse_stacks_from_text(stack_text)
        instructions = parse_instructions_from_text(instruction_text)
        return Puzzle(stacks, instructions)


    def apply_instructions_using_9000_model(self) -> str:
        stack = deepcopy(self.stacks)
        for inst in self.instructions:
            # pop from {from_id} stack and add to the end
            # of stack {to_id}
            for _ in range(inst.n):
                stack[inst.to_id].append(stack[inst.from_id].pop())
        return ''.join(s[-1] for s in stack)


    def apply_instructions_using_9001_model(self) -> str:
        stack = deepcopy(self.stacks)
        for inst in self.instructions:
            # move items in the same order
            stack[inst.to_id].extend(
                stack[inst.from_id][-inst.n:])
            # delete them from the end
            for _ in range(inst.n):
                stack[inst.from_id].pop()
        return ''.join(s[-1] for s in stack)
        

if __name__ == '__main__':
    test_pzl = Puzzle.parse(RAW_INPUT)
    test_top_crates_9000 = test_pzl.apply_instructions_using_9000_model()

    test_top_crates_9001 = test_pzl.apply_instructions_using_9001_model()
    assert test_top_crates_9000 == 'CMZ'
    assert test_top_crates_9001 == 'MCD'


    with open('data/input.txt') as f:
        plain_text = f.read()
    
    pzl = Puzzle.parse(plain_text)
    top_crates_9000 = pzl.apply_instructions_using_9000_model()
    print(f'answer1: {top_crates_9000}')

    top_crates_9001 = pzl.apply_instructions_using_9001_model()
    print(f'answer2: {top_crates_9001}')