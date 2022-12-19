from typing import List, Tuple, Set
from collections import Counter, deque

Coor3D = Tuple[int, int, int]

RAW_INPUT = """2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5"""


def parse_line(line: str) -> Coor3D:
    return tuple(map(int, line.strip().split(',')))

assert parse_line('1,2,5') == (1, 2, 5)

def parse_input(plain_text: str) -> List[Coor3D]:
    return set([parse_line(l) for l in plain_text.strip().splitlines()])


def get_neighbors(pos: Coor3D):
    x, y, z = pos
    yield (x + 1, y, z)
    yield (x - 1, y, z)
    yield (x, y + 1, z)
    yield (x, y - 1, z)
    yield (x, y, z + 1)
    yield (x, y, z - 1)


def reaches_infinity(
    node: Coor3D,
    graph: Set[Coor3D],
    memo: Set[Coor3D]):

    if node in graph:
        return False
    
    if node in memo:
        return True

    seen = set()
    queue = deque([node])
    seen.add(node)

    while queue:
        curr_node = queue.popleft()
        # long enough to declare that node will reach infinity
        if len(seen) >= 5_000:
            memo.update(seen)
            return True

        for neighbor in get_neighbors(curr_node):
            if neighbor not in seen and neighbor not in graph:
                seen.add(neighbor)
                queue.append(neighbor)
    # the node could no space, so its trapped :)
    graph.update(seen)
    return False


def fill_graph(graph: Coor3D):
    candidates = set([
        neighbor
        for node in graph
        for neighbor in get_neighbors(node)
        if neighbor not in graph])

    memo = set()
    for node in candidates:
        reaches_infinity(node, graph, memo)
    return graph


def find_total_surface_area(graph: Set[Coor3D]) -> int:
    surface_area = 0
    for node in graph:
        surface_area += sum(neighbor not in graph for neighbor in get_neighbors(node))
    return surface_area


if __name__ == '__main__':
    test_cubes = parse_input(RAW_INPUT)

    test_total_surface = find_total_surface_area(test_cubes)
    assert test_total_surface == 64, test_total_surface

    test_total_surface = find_total_surface_area([(1, 0, 0), (0, -1, 0), (0, 0, 0)])
    assert test_total_surface == 14, test_total_surface

    test_total_surface_no_air = find_total_surface_area(fill_graph(test_cubes))
    assert test_total_surface_no_air == 58, test_total_surface_no_air

    with open('data/input.txt') as f:
        plain_text = f.read()
    
    cubes = parse_input(plain_text)

    total_surface = find_total_surface_area(cubes)
    print(total_surface)

    total_surface_no_air = find_total_surface_area(fill_graph(cubes))
    print(total_surface_no_air)

