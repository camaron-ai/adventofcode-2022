from typing import List
from dataclasses import dataclass
import operator
import functools


OPERATOR_MAPPER = {'+': operator.add, '*': operator.mul}

RAW_SINGLE_MONKEY_INPUT = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3"""



@dataclass
class Monkey:
    items: List[int]
    operation: List[str]
    divisor: int
    if_true_id: int
    if_false_id: int
    n_inspected: int = 0

    @staticmethod
    def _parse_number(s: str, n: int) -> int:
        return n if s == 'old' else int(s)

    def apply_operation(self, old: int) -> int:
        first_number = self._parse_number(self.operation[0], old)
        second_number = self._parse_number(self.operation[2], old)
        return OPERATOR_MAPPER[self.operation[1]](first_number, second_number)

    @staticmethod
    def parse(plain_text: str) -> 'Monkey':
        lines = [l.strip() for l in plain_text.splitlines()]
        (_, items_str,
         operation_line, test_line,
         if_true_line, if_false_line) = lines
        
        items_str = items_str.split(': ')[1].strip()
        items = [int(item) for item in items_str.split(', ')]
        operation = operation_line.split('=')[1].strip().split(' ')
        divisor = int(test_line.split(' ')[-1])

        if_true_id = int(if_true_line.split(' ')[-1])
        if_false_id = int(if_false_line.split(' ')[-1])
        return Monkey(items, operation, divisor, if_true_id, if_false_id)



TEST_MONKEY = Monkey.parse(RAW_SINGLE_MONKEY_INPUT)
assert TEST_MONKEY.items == [79, 98]
assert TEST_MONKEY.operation == ['old', '*', '19']
assert TEST_MONKEY.divisor == 23
assert TEST_MONKEY.if_true_id == 2
assert TEST_MONKEY.if_false_id == 3


@dataclass
class KeepAwayGame:
    monkeys: List[Monkey]
    common_divisor: int
    worry_divisor: int = 1

    @property
    def n_monkeys(self) -> int:
        return len(self.monkeys)

    def inspect(self, i: int):
        monkey = self.monkeys[i]
        for worry_level in monkey.items:

            monkey.n_inspected += 1
            curr_worry_level = monkey.apply_operation(worry_level)
            curr_worry_level = curr_worry_level // self.worry_divisor
            curr_worry_level = curr_worry_level % self.common_divisor

            to_id = (
                monkey.if_true_id
                if curr_worry_level % monkey.divisor == 0 else
                monkey.if_false_id
            )
            self.monkeys[to_id].items.append(curr_worry_level)

        # reset seens monkeys
        monkey.items = list()
            

    def play_round(self):
        for monkey_id in range(self.n_monkeys):
            self.inspect(monkey_id)
        
    def get_monkey_level(self, n_rounds: int) -> int:
        for _ in range(n_rounds):
            self.play_round()
        inspected_items = sorted([m.n_inspected for m in self.monkeys], reverse=True)
        return inspected_items[0] * inspected_items[1]

    @staticmethod
    def parse(plain_text: str, worry_divisor: int = 1) -> 'KeepAwayGame':
        monkeys_plain_text = plain_text.strip().split('\n\n')
        monkeys = [Monkey.parse(s) for s in monkeys_plain_text]
        common_divisor = functools.reduce(lambda cd, x: cd * x, (m.divisor for m in monkeys))
        return KeepAwayGame(monkeys, common_divisor, worry_divisor)


if __name__ == '__main__':
    with open('data/test_case.txt') as f:
        test_plain_text = f.read()

    test_monkey_business_20 = KeepAwayGame.parse(test_plain_text, worry_divisor=3).get_monkey_level(20)
    assert test_monkey_business_20 == 10605, test_monkey_business_20

    test_monkey_business_10_000 = KeepAwayGame.parse(test_plain_text).get_monkey_level(10_000)
    assert test_monkey_business_10_000 == 2713310158, test_monkey_business_10_000

    with open('data/input.txt') as f:
        plain_text = f.read()

    monkey_business20 = KeepAwayGame.parse(plain_text, worry_divisor=3).get_monkey_level(20)
    print(monkey_business20)

    monkey_business_10_000 = KeepAwayGame.parse(plain_text, 1).get_monkey_level(10_000)
    print(monkey_business_10_000)
