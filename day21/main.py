from typing import List, Dict
import operator
from collections import defaultdict, deque
from dataclasses import dataclass
from copy import deepcopy


RAW_INPUT = """root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32"""


OPERATOR_MAPPER = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv
    }


def get_inverse_operator(operator):
    operators_order = ['+', '-', '*', '/']
    inv_operators = ['-', '+', '/', '*']
    return inv_operators[operators_order.index(operator)]



def apply_operation(x, operator, y):
    return int(OPERATOR_MAPPER[operator](x, y))


@dataclass
class Graph:
    operation_mapper: Dict[str, str]
    dependencies: Dict[str, int]
    graph: Dict[str, List[str]]


    def solve_dependencies(self, dependencies: Dict[str, int]):
        yelled_numbers = {}
        queue = deque([
            monkey
            for monkey, n_d in dependencies.items()
            if n_d == 0
            ])

        while queue:
            curr_monkey = queue.popleft()
            operation = self.operation_mapper[curr_monkey]

            if dependencies[curr_monkey] == 0:
                if operation.isnumeric():
                    yelled_numbers[curr_monkey] = int(operation)
                else:
                    first_monkey, operator, second_monkey = operation.split(' ')
                    x = yelled_numbers[first_monkey]
                    y = yelled_numbers[second_monkey]
                    yelled_numbers[curr_monkey] = apply_operation(x, operator, y)

                # remove dependencies
                for neighbor in self.graph[curr_monkey]:
                    dependencies[neighbor] -= 1
                
                # if dependecies are complete, add it to the queue
                for neighbor in self.graph[curr_monkey]:
                    if dependencies[neighbor] == 0:
                        queue.append(neighbor)
        return yelled_numbers



    def find_root_number(self) -> int:
        dependencies = deepcopy(self.dependencies)
        yelled_numbers = self.solve_dependencies(dependencies)
        return yelled_numbers['root']


    def find_humn_number(self) -> int:
        dependencies = deepcopy(self.dependencies)
        dependencies['humn'] = 2
        self.operation_mapper['root'] = self.operation_mapper['root'].replace('+', '-').replace('*', '-').replace('/', '-')

        # solve all dependencies we can
        yelled_numbers = self.solve_dependencies(dependencies)

        current_node = 'root'
        current_value = 0

        while current_node != 'humn':
            # at each node, we will have one known and one unknown
            first_monkey, operator, second_monkey = self.operation_mapper[current_node].split(' ')
            known_monkey, unknown_monkey = (
                (first_monkey, second_monkey)
                if first_monkey in yelled_numbers else 
                (second_monkey, first_monkey)
            )
            inv_operator = get_inverse_operator(operator)
            known_value = yelled_numbers[known_monkey]

            if unknown_monkey == second_monkey and operator in ('-', '/'):
                current_value = apply_operation(known_value, operator, current_value)
            else:
                current_value = apply_operation(current_value, inv_operator, known_value)
            
            current_node = unknown_monkey
        
        return current_value


    @staticmethod
    def parse(plain_text: str) -> 'Graph':
        graph = defaultdict(list)
        operation_mapper = {}
        dependencies = {}
        for line in plain_text.strip().splitlines():
            monkey, operation = line.split(': ')
            operation_mapper[monkey] = operation
            if not operation.isnumeric():
                first_monkey, _, second_monkey = operation.split(' ')
                dependencies[monkey] = 2
                graph[first_monkey].append(monkey)
                graph[second_monkey].append(monkey)
            else:
                dependencies[monkey] = 0
        return Graph(operation_mapper, dependencies, graph)


if __name__ == '__main__':

    test_graph = Graph.parse(RAW_INPUT)
    test_root_number = test_graph.find_root_number()
    assert test_root_number == 152

    test_humn_number = test_graph.find_humn_number()
    assert test_humn_number == 301, test_humn_number

    with open('data/input.txt') as f:
        plain_text = f.read()

    graph = Graph.parse(plain_text)
    root_number = graph.find_root_number()
    print(root_number)

    root_number = graph.find_humn_number()
    print(root_number)

