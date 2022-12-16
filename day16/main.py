from typing import List, Dict, Tuple
from dataclasses import dataclass
import re
RAW_LINE_INPUT = 'Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE'

Graph = Dict[int, List[str]]
RateMapper = Dict[int, int]

def parse_line(line: str) -> Tuple[str, int, List[int]]:
    match = re.search(r'Valve ([A-Z]+) has flow rate=(-?\d+)', line)
    node, rate = match.groups()

    match_string = 'valves' if 'valves' in line else 'valve'
    _, neighbors_str = line.split(f' {match_string} ')
    neighbors = neighbors_str.split(', ')

    return node, int(rate), neighbors

assert parse_line(RAW_LINE_INPUT) == ('DD', 20, ['CC', 'AA', 'EE'])



@dataclass
class ValvesMap:
    graph: Graph
    rate_mapper: RateMapper
    node_to_int_mapper: Dict[str, int]

    @property
    def n_nodes(self):
        return len(self.graph)

    def most_preasure(self, minutes: int = 30, n_players: int = 1):
        memo = {}
        start_node = self.node_to_int_mapper['AA']
        def dp(current_node: int, open_valves: int, time_left: int, n_players: int):
            if n_players == 0:
                return 0

            if time_left <= 0:
                return dp(start_node, open_valves, minutes, n_players - 1)

            if not (current_node, open_valves, time_left, n_players) in memo:
                answer = 0
                if not (open_valves & (1 << current_node)) and self.rate_mapper[current_node] > 0:
                    open_valve_score = self.rate_mapper[current_node] * (time_left - 1)
                    answer = max(answer, open_valve_score + dp(current_node, open_valves | 1 << current_node, time_left - 1, n_players))
                answer = max(answer, max([dp(neighbor, open_valves, time_left - 1, n_players)
                            for neighbor in self.graph[current_node]]))
                memo[(current_node, open_valves, time_left, n_players)] = answer
    
            return memo[(current_node, open_valves, time_left, n_players)]

        return dp(start_node, 0, minutes, n_players)

    @staticmethod
    def parse(plain_text: str) -> 'ValvesMap':
        rate_mapper = {}
        graph = {}
        node_to_int_mapper = {}
        for line in plain_text.strip().splitlines():
            node, rate, neighbors = parse_line(line)
            node_to_int_mapper[node] = node_to_int_mapper.get(node, len(node_to_int_mapper))
            encoded_node = node_to_int_mapper[node]
            encoded_neighbors = []
            for neighbor in neighbors:
                node_to_int_mapper[neighbor] = node_to_int_mapper.get(neighbor, len(node_to_int_mapper))
                encoded_neighbors.append(node_to_int_mapper[neighbor])

            graph[encoded_node] = encoded_neighbors
            rate_mapper[encoded_node] = rate
        
        return ValvesMap(graph, rate_mapper, node_to_int_mapper)


if __name__ == '__main__':
    with open('data/test_case.txt') as f:
        test_plain_text = f.read()

    test_valves = ValvesMap.parse(test_plain_text)
    test_most_preasure = test_valves.most_preasure(30)
    assert test_most_preasure == 1651

    test_most_preasure_2_players = test_valves.most_preasure(26, n_players=2)
    assert test_most_preasure_2_players == 1707

    with open('data/input.txt') as f:
        plain_text = f.read()
    valves = ValvesMap.parse(plain_text)
    most_preasure = valves.most_preasure(30)
    print(most_preasure)

    most_preasure_2_players = valves.most_preasure(26, n_players=2)
    print(most_preasure_2_players)